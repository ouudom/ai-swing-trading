#!/usr/bin/env python3
"""FX currency-leg netting ledger — Architecture B core (D022, see wiki/system/core/currency_exposure.md).

The EUR/GBP/USD triangle (EURGBP = EURUSD/GBPUSD) has exactly TWO degrees of freedom,
so all FX-major + cross exposure collapses onto two orthogonal risk axes:

  USD axis    — "bet USD down"  = Σ dir over {eurusd, gbpusd}     (eurgbp has no USD leg → 0)
  CROSS axis  — "bet EURGBP up" = eurusd_dir − gbpusd_dir + eurgbp_dir

dir = +1 (long) / −1 (short); each order weighted by risk_units = risk_usd / 2000.

Risk unit = $2000 per AXIS (not per instrument). |axis units| > 1 ⇒ concentration:
two "separate" trades that load the same factor = one bet at >1×, never two.

  same-direction majors  → USD axis stacks   (±2)  → doubled USD bet
  opposite-direction majors → CROSS axis stacks (±2) → EURGBP cross bet
  explicit eurgbp on an implied cross → CROSS axis → 3×, invisible to pairwise gate

This module is the N-order/N-axis generalization of the pairwise /validate netting gate,
and the prerequisite for ever trading EURGBP directly (EG0 in the onboarding plan).

Usage:
  bash scripts/pyrun.sh scripts/fx_exposure.py --orders "eurusd:long:2000,gbpusd:short:2000"
  bash scripts/pyrun.sh scripts/fx_exposure.py --live "eurusd:short:2000" --candidate "gbpusd:short:2000" --new-ec 6.5 --live-ecs "eurusd:7.5"
  bash scripts/pyrun.sh scripts/fx_exposure.py --selftest
"""
from __future__ import annotations
import argparse
import sys
from dataclasses import dataclass

RISK_UNIT = 2000.0          # $ per axis (one unit)
EPS = 1e-9
CAP_UNITS = 1.0             # max |axis units| before concentration

# Per-instrument contribution to each axis for a LONG position (short = negate).
# USD axis = "bet USD down"; CROSS axis = "bet EURGBP up" (long EUR / short GBP).
AXIS = {
    "eurusd": {"usd": +1, "cross": +1},   # long EUR vs USD: USD down, EUR up → +cross
    "gbpusd": {"usd": +1, "cross": -1},   # long GBP vs USD: USD down, GBP up → −cross
    "eurgbp": {"usd":  0, "cross": +1},   # long EUR vs GBP: no USD leg → +cross
}
# Raw currency legs (audit view only — the axes above are what the cap acts on).
LEGS = {
    "eurusd": {"EUR": +1, "USD": -1},
    "gbpusd": {"GBP": +1, "USD": -1},
    "eurgbp": {"EUR": +1, "GBP": -1},
}
FX_INSTRUMENTS = set(AXIS)


@dataclass
class Order:
    instrument: str
    direction: str   # "long" | "short"
    risk: float      # $ at risk

    @property
    def dir_sign(self) -> int:
        return +1 if self.direction.lower() in ("long", "buy") else -1

    @property
    def units(self) -> float:
        return self.risk / RISK_UNIT


def parse_orders(spec: str) -> list[Order]:
    """'eurusd:long:2000,gbpusd:short' → [Order, ...]. Risk defaults to 2000."""
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        inst = parts[0].strip().lower()
        direction = parts[1].strip().lower() if len(parts) > 1 else "long"
        risk = float(parts[2]) if len(parts) > 2 and parts[2] else RISK_UNIT
        if inst not in FX_INSTRUMENTS:
            raise ValueError(f"Unknown FX instrument '{inst}'. Known: {sorted(FX_INSTRUMENTS)}")
        out.append(Order(inst, direction, risk))
    return out


def axis_net(orders: list[Order]) -> dict[str, float]:
    """Net exposure on each risk axis, in risk-units."""
    net = {"usd": 0.0, "cross": 0.0}
    for o in orders:
        for ax, w in AXIS[o.instrument].items():
            net[ax] += o.dir_sign * w * o.units
    return net


def currency_net(orders: list[Order]) -> dict[str, float]:
    """Net per-currency legs in risk-units (human audit)."""
    net = {"EUR": 0.0, "GBP": 0.0, "USD": 0.0}
    for o in orders:
        for ccy, w in LEGS[o.instrument].items():
            net[ccy] += o.dir_sign * w * o.units
    return net


def concentration(orders: list[Order]) -> dict:
    """Classify the portfolio: which axes breach the 1-unit cap, and by how much."""
    net = axis_net(orders)
    flags = []
    for ax, u in net.items():
        if abs(u) > CAP_UNITS + EPS:
            label = ("USD" if ax == "usd" else "EURGBP cross")
            side = _axis_side(ax, u)
            flags.append({"axis": ax, "label": label, "units": u, "side": side,
                          "excess_risk": (abs(u) - CAP_UNITS) * RISK_UNIT})
    return {"axis_net": net, "currency_net": currency_net(orders),
            "flags": flags, "concentrated": bool(flags)}


def _axis_side(ax: str, u: float) -> str:
    if ax == "usd":
        return "short USD (pair-up bias)" if u > 0 else "long USD (pair-down bias)"
    return "long EURGBP" if u > 0 else "short EURGBP"


def gate(candidate: Order, live: list[Order],
         new_ec: float | None = None, live_ecs: dict[str, float] | None = None) -> dict:
    """Pairwise/N-order netting gate (Architecture A/B resolution: keep best, drop weaker).

    Would placing `candidate` alongside `live` breach a cap? If so, resolve by Entry Confluence.
    Returns the verdict + which live order(s) to cancel, if any.
    """
    live_ecs = live_ecs or {}
    before = concentration(live)
    after = concentration(live + [candidate])
    if not after["concentrated"]:
        return {"verdict": "PLACE", "reason": "no concentration — candidate is independent",
                "axis_net_after": after["axis_net"], "cancel": []}

    # Concentration. Resolve keep-best-drop-weaker on the breached axis.
    # Find the live order(s) that contribute to the same breached axis with the same sign.
    breached_axes = {f["axis"] for f in after["flags"]}
    contributors = []
    for o in live:
        for ax in breached_axes:
            w = AXIS[o.instrument][ax]
            if w != 0 and (o.dir_sign * w) == (candidate.dir_sign * AXIS[candidate.instrument][ax]):
                contributors.append(o)
                break

    cand_ec = new_ec if new_ec is not None else -1.0
    worst = None
    for o in contributors:
        ec = live_ecs.get(o.instrument, -1.0)
        if worst is None or ec < worst[1]:
            worst = (o, ec)

    if worst and cand_ec > worst[1] + EPS:
        return {"verdict": "PLACE_CANCEL_OTHER",
                "reason": f"concentration on {[f['label'] for f in after['flags']]}; "
                          f"candidate EC {cand_ec} > live {worst[0].instrument} EC {worst[1]} → cancel live, place candidate",
                "cancel": [worst[0].instrument], "axis_net_after": after["axis_net"],
                "flags": after["flags"]}
    return {"verdict": "SKIP",
            "reason": f"concentration on {[f['label'] for f in after['flags']]}; "
                      f"candidate EC {cand_ec} ≤ live → SKIP (stays PENDING, lost tie-break)",
            "cancel": [], "axis_net_after": after["axis_net"], "flags": after["flags"]}


def _fmt(orders: list[Order]) -> str:
    return ", ".join(f"{o.instrument} {o.direction} ${o.risk:.0f}" for o in orders)


def report(orders: list[Order]) -> str:
    c = concentration(orders)
    lines = [f"Orders: {_fmt(orders)}", ""]
    lines.append("Currency legs (audit):  " +
                 "  ".join(f"{k}{v:+.2f}" for k, v in c["currency_net"].items()))
    lines.append("Risk axes (capped at ±1 unit = ±$2000):")
    for ax, u in c["axis_net"].items():
        label = "USD" if ax == "usd" else "EURGBP cross"
        mark = "  ⚠️ BREACH" if abs(u) > CAP_UNITS + EPS else ""
        lines.append(f"  {label:13s} {u:+.2f} units (${u*RISK_UNIT:+,.0f}){mark}")
    if c["concentrated"]:
        lines.append("")
        for f in c["flags"]:
            lines.append(f"⚠️  CONCENTRATION: {f['units']:+.2f} units on {f['label']} "
                         f"= {f['side']}. Excess ${f['excess_risk']:,.0f} over the 1-unit cap.")
        lines.append("→ This is ONE bet at >1×, not independent trades. Net first; keep best zone, drop weaker.")
    else:
        lines.append("\n✅ No axis breaches the 1-unit cap — exposure within budget.")
    return "\n".join(lines)


def _selftest() -> int:
    cases = [
        ("eurusd:long,gbpusd:short", "cross", 2.0),    # opposite → CROSS ±2
        ("eurusd:short,gbpusd:long", "cross", -2.0),
        ("eurusd:long,gbpusd:long", "usd", 2.0),       # same → USD ±2
        ("eurusd:short,gbpusd:short", "usd", -2.0),
        ("eurusd:long", None, None),                   # single → no breach
        ("eurusd:long,gbpusd:short,eurgbp:long", "cross", 3.0),  # explicit on implied → 3×
    ]
    ok = True
    for spec, ax, expect in cases:
        c = concentration(parse_orders(spec))
        net = c["axis_net"]
        if ax is None:
            passed = not c["concentrated"]
            got = "no breach"
        else:
            passed = abs(net[ax] - expect) < 1e-6 and c["concentrated"]
            got = f"{ax}={net[ax]:+.2f}"
        ok &= passed
        print(f"[{'PASS' if passed else 'FAIL'}] {spec:42s} expect {ax}={expect} got {got}")
    print("\nSELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def _parse_ecs(spec: str | None) -> dict[str, float]:
    out = {}
    if spec:
        for chunk in spec.split(","):
            inst, ec = chunk.split(":")
            out[inst.strip().lower()] = float(ec)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="FX currency-leg netting ledger (D022).")
    ap.add_argument("--orders", help="comma list 'inst:dir:risk' — report net exposure")
    ap.add_argument("--live", help="existing live FX orders 'inst:dir:risk,...'")
    ap.add_argument("--candidate", help="prospective order 'inst:dir:risk' — run the netting gate")
    ap.add_argument("--new-ec", type=float, help="candidate Entry Confluence (for tie-break)")
    ap.add_argument("--live-ecs", help="live orders' EC 'inst:ec,...'")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if args.candidate:
        live = parse_orders(args.live) if args.live else []
        cand = parse_orders(args.candidate)[0]
        g = gate(cand, live, new_ec=args.new_ec, live_ecs=_parse_ecs(args.live_ecs))
        print(f"Live: {_fmt(live) or '(none)'}")
        print(f"Candidate: {_fmt([cand])} (EC {args.new_ec})")
        print(f"\nVERDICT: {g['verdict']}\n{g['reason']}")
        if g["cancel"]:
            print(f"Cancel live limit(s): {g['cancel']}")
        return 0
    if args.orders:
        print(report(parse_orders(args.orders)))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
