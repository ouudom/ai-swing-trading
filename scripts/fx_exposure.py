#!/usr/bin/env python3
"""FX currency-leg netting ledger — ADVISORY (D022 as amended by D024).

Generalized from the original 3-instrument / 2-axis cap model to a per-currency-leg
ledger over all FX instruments (8 currencies). Every pair = +base / −quote leg;
a SHORT flips the signs. Orders are weighted in R-multiples — every order risks 1R
by default (1R = that trade's SL distance), so risk_units = risk_r (no $ conversion).

OPERATOR DECISION (D024, 2026-06-10): this is a SIGNAL system, not a risk manager.
No hard cap is enforced. When two or more orders load the same currency leg in the
same direction (e.g. EURUSD short + GBPUSD short = 2× long USD), the ledger FLAGS the
concentration and SUGGESTS the cleaner trade (highest Entry Confluence). The operator
decides. Nothing is auto-skipped.

Soft advisory extras:
  - antipodean bloc: AUDUSD + NZDUSD same direction ≈ one bet (corr ~0.85) even though
    AUD and NZD are distinct legs — flagged as a note.
  - triangle identities (EURGBP=EURUSD/GBPUSD, EURJPY=EURUSD×USDJPY, GBPJPY=GBPUSD×USDJPY)
    fall out of the leg algebra automatically — an explicit cross stacking on an implied
    cross shows up as a doubled leg.

Gold (xauusd) stays OUT of the ledger — USD-priced but real-yield driven.

Usage:
  bash scripts/pyrun.sh scripts/fx_exposure.py --orders "eurusd:short:1,gbpusd:short:1"
  bash scripts/pyrun.sh scripts/fx_exposure.py --live "eurusd:short:1" --candidate "gbpusd:short:1" --new-ec 6.5 --live-ecs "eurusd:7.5"
  bash scripts/pyrun.sh scripts/fx_exposure.py --selftest
"""
from __future__ import annotations
import argparse
import sys
from dataclasses import dataclass

RISK_UNIT = 1.0              # 1R per order (reporting only — no cap enforced)
EPS = 1e-9

# Per-instrument currency legs for a LONG position (short = negate).
LEGS = {
    # USD-quote majors (long pair = short USD)
    "eurusd": {"EUR": +1, "USD": -1},
    "gbpusd": {"GBP": +1, "USD": -1},
    "audusd": {"AUD": +1, "USD": -1},
    "nzdusd": {"NZD": +1, "USD": -1},
    # USD-base pairs (long pair = long USD)
    "usdcad": {"USD": +1, "CAD": -1},
    "usdchf": {"USD": +1, "CHF": -1},
    "usdjpy": {"USD": +1, "JPY": -1},
    # Crosses (no USD leg)
    "eurgbp": {"EUR": +1, "GBP": -1},
    "eurjpy": {"EUR": +1, "JPY": -1},
    "gbpjpy": {"GBP": +1, "JPY": -1},
}
CURRENCIES = sorted({c for legs in LEGS.values() for c in legs})
FX_INSTRUMENTS = set(LEGS)


@dataclass
class Order:
    instrument: str
    direction: str   # "long" | "short"
    risk: float      # risk in R-multiples (default 1.0 = 1R)

    @property
    def dir_sign(self) -> int:
        return +1 if self.direction.lower() in ("long", "buy") else -1

    @property
    def units(self) -> float:
        return self.risk / RISK_UNIT

    def leg(self, ccy: str) -> float:
        """Signed leg contribution in risk-units for currency `ccy`."""
        return self.dir_sign * LEGS[self.instrument].get(ccy, 0) * self.units


def parse_orders(spec: str) -> list[Order]:
    """'eurusd:long:1,gbpusd:short' → [Order, ...]. Risk defaults to 1R."""
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


def currency_net(orders: list[Order]) -> dict[str, float]:
    """Net per-currency legs in risk-units."""
    net = {c: 0.0 for c in CURRENCIES}
    for o in orders:
        for ccy in LEGS[o.instrument]:
            net[ccy] += o.leg(ccy)
    return net


def shared_legs(orders: list[Order]) -> list[dict]:
    """Currencies where ≥2 orders contribute the SAME sign — the concentration signal.

    Net alone isn't enough (two opposite orders net to 0 but that's a cross bet on the
    OTHER legs, which this still catches on those legs).
    """
    flags = []
    for ccy in CURRENCIES:
        contribs = [(o, o.leg(ccy)) for o in orders if abs(o.leg(ccy)) > EPS]
        pos = [(o, u) for o, u in contribs if u > 0]
        neg = [(o, u) for o, u in contribs if u < 0]
        for side, group in (("long", pos), ("short", neg)):
            if len(group) >= 2:
                total = sum(u for _, u in group)
                flags.append({
                    "currency": ccy, "side": side, "units": total,
                    "orders": [o.instrument for o, _ in group],
                })
    return flags


def antipodean_note(orders: list[Order]) -> str | None:
    """AUD + NZD same direction ≈ one bet (corr ~0.85) even with distinct legs."""
    dirs = {o.instrument: o.dir_sign for o in orders}
    if "audusd" in dirs and "nzdusd" in dirs and dirs["audusd"] == dirs["nzdusd"]:
        d = "long" if dirs["audusd"] > 0 else "short"
        return (f"antipodean bloc: AUDUSD + NZDUSD both {d} — distinct legs but corr ~0.85, "
                f"effectively one bet.")
    return None


def advise(candidate: Order, live: list[Order],
           new_ec: float | None = None, live_ecs: dict[str, float] | None = None) -> dict:
    """ADVISORY gate (D024): no enforcement. Would `candidate` share a leg-direction with a
    live order? If so, flag it and suggest the cleaner trade (highest EC). Operator decides.
    """
    live_ecs = live_ecs or {}
    flags = shared_legs(live + [candidate])
    # Only flags the candidate participates in are advice-relevant.
    cand_flags = [f for f in flags if candidate.instrument in f["orders"]]
    note = antipodean_note(live + [candidate])

    if not cand_flags:
        return {"verdict": "INDEPENDENT",
                "reason": "no shared currency-leg direction with live orders",
                "flags": flags, "note": note, "suggest_keep": None}

    # Rank candidate + co-contributors by EC; suggest keeping the best.
    ecs = dict(live_ecs)
    if new_ec is not None:
        ecs[candidate.instrument] = new_ec
    involved = sorted({i for f in cand_flags for i in f["orders"]})
    ranked = sorted(involved, key=lambda i: ecs.get(i, -1.0), reverse=True)
    best = ranked[0]
    legs_txt = "; ".join(f"{f['units']:+.2f}u {f['side']} {f['currency']} via {'+'.join(f['orders'])}"
                         for f in cand_flags)
    return {"verdict": "CONCENTRATED",
            "reason": f"shared leg(s): {legs_txt}",
            "flags": cand_flags, "note": note, "suggest_keep": best,
            "ranking": [(i, ecs.get(i)) for i in ranked]}


def _fmt(orders: list[Order]) -> str:
    return ", ".join(f"{o.instrument} {o.direction} {o.risk:.2f}R" for o in orders)


def report(orders: list[Order]) -> str:
    net = currency_net(orders)
    flags = shared_legs(orders)
    note = antipodean_note(orders)
    lines = [f"Orders: {_fmt(orders)}", ""]
    nz = {k: v for k, v in net.items() if abs(v) > EPS}
    lines.append("Currency legs (risk-units, 1u = 1R):  " +
                 ("  ".join(f"{k}{v:+.2f}" for k, v in nz.items()) or "(flat)"))
    if flags:
        lines.append("")
        for f in flags:
            lines.append(f"⚠️  SHARED LEG: {f['units']:+.2f}u {f['side']} {f['currency']} "
                         f"from {' + '.join(f['orders'])} — one factor, not independent trades.")
        lines.append("→ ADVISORY (D024): consider keeping only the cleaner trade (higher EC). Operator decides.")
    else:
        lines.append("\n✅ No shared currency-leg direction — orders are leg-independent.")
    if note:
        lines.append(f"ℹ️  {note}")
    return "\n".join(lines)


def _selftest() -> int:
    def f(spec):
        return shared_legs(parse_orders(spec))

    cases = [
        # spec, expect_flag (ccy, side, units) or None
        ("eurusd:short,gbpusd:short", ("USD", "long", 2.0)),     # classic 2× long USD
        ("eurusd:long,gbpusd:long", ("USD", "short", -2.0)),     # 2× short USD
        ("eurusd:long,gbpusd:short", None),                      # opposite majors → implied cross, no shared leg
        ("eurusd:long,gbpusd:short,eurgbp:long", ("EUR", "long", 2.0)),  # explicit cross stacks implied
        ("usdjpy:long,eurusd:short", ("USD", "long", 2.0)),      # USD-base + USD-quote, same USD side
        ("usdjpy:long,eurjpy:long", ("JPY", "short", -2.0)),     # shared short-JPY leg
        ("gbpjpy:short,gbpusd:short", ("GBP", "short", -2.0)),   # shared short-GBP leg
        ("audusd:long,usdcad:short", ("USD", "short", -2.0)),    # long AUD/USD + short USD/CAD = 2× short USD
        ("eurusd:long", None),                                   # single order
        ("audusd:long,eurjpy:short", None),                      # no common leg
    ]
    ok = True
    for spec, expect in cases:
        flags = f(spec)
        if expect is None:
            passed = not flags
            got = "no flag" if not flags else f"{flags[0]['currency']} {flags[0]['units']:+.1f}"
        else:
            ccy, side, units = expect
            passed = any(fl["currency"] == ccy and fl["side"] == side and abs(fl["units"] - units) < 1e-6
                         for fl in flags)
            got = "; ".join(f"{fl['currency']}:{fl['side']}:{fl['units']:+.1f}" for fl in flags) or "no flag"
        ok &= passed
        print(f"[{'PASS' if passed else 'FAIL'}] {spec:42s} expect {expect} got {got}")

    # antipodean note
    note = antipodean_note(parse_orders("audusd:long,nzdusd:long"))
    passed = note is not None
    ok &= passed
    print(f"[{'PASS' if passed else 'FAIL'}] audusd:long,nzdusd:long{' ':19s} expect antipodean note got {bool(note)}")

    # advisory suggest-keep
    g = advise(parse_orders("gbpusd:short")[0], parse_orders("eurusd:short"),
               new_ec=6.5, live_ecs={"eurusd": 7.5})
    passed = g["verdict"] == "CONCENTRATED" and g["suggest_keep"] == "eurusd"
    ok &= passed
    print(f"[{'PASS' if passed else 'FAIL'}] advise gbpusd vs live eurusd (EC 6.5<7.5)   suggest_keep={g['suggest_keep']}")

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
    ap = argparse.ArgumentParser(description="FX currency-leg netting ledger — advisory (D024).")
    ap.add_argument("--orders", help="comma list 'inst:dir:risk_r' — report net exposure")
    ap.add_argument("--live", help="existing live FX orders 'inst:dir:risk_r,...'")
    ap.add_argument("--candidate", help="prospective order 'inst:dir:risk_r' — run the advisory")
    ap.add_argument("--new-ec", type=float, help="candidate Entry Confluence (ranking)")
    ap.add_argument("--live-ecs", help="live orders' EC 'inst:ec,...'")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if args.candidate:
        live = parse_orders(args.live) if args.live else []
        cand = parse_orders(args.candidate)[0]
        g = advise(cand, live, new_ec=args.new_ec, live_ecs=_parse_ecs(args.live_ecs))
        print(f"Live: {_fmt(live) or '(none)'}")
        print(f"Candidate: {_fmt([cand])} (EC {args.new_ec})")
        print(f"\nADVISORY: {g['verdict']}\n{g['reason']}")
        if g["verdict"] == "CONCENTRATED":
            print(f"Suggest keeping: {g['suggest_keep']} (EC ranking: {g['ranking']})")
            print("Operator decides — nothing is auto-skipped (D024).")
        if g.get("note"):
            print(f"Note: {g['note']}")
        return 0
    if args.orders:
        print(report(parse_orders(args.orders)))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
