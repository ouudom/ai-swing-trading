"""
trade_outcome — entry-mechanics replay + gate-accuracy audit.

`zone_outcome` fills every zone at its MIDPOINT, ignoring E0/offset/EC — it measures
ZONE (R1) quality. This resolver applies the real ENTRY mechanics on top of the same
zone ledger and answers two things `zone_outcome` and the (retired) hand-logged `trade`
table cannot:

  1. SYSTEM P&L with realistic fills — detect E0, anchor at the E0 close (else zone
     midpoint), score Entry Confluence (R2, `entry_confluence.py`), place the outward
     offset limit = max(SL/3, (10 − EC) × 0.2 × SL), and fill only if a later bar pokes
     it. The midpoint-fill vs offset-limit-fill gap is the D030 "offset too wide / missed
     the fill" signal.

  2. GATE ACCURACY — every hard gate (V1/V1b/V3/VETO-VIX/VETO-ADX/INTERVENTION/EC-floor)
     is evaluated at the fill bar as a NON-SUPPRESSING FLAG: the trade fills regardless so
     we get the counterfactual R, then score whether refusing it was CORRECT_SAVED
     (would-be ≤0R) or COSTLY_REFUSED (would-be >0R). This replaces `zone_outcome`'s
     unverified "INVALIDATED = capital saved" assumption with a measured verdict.

Shadow model: SL = constitution formula on closed bars (reused from zone_outcomes);
manage = TP1 +2.5R / SL −1R / BE→entry after MFE +1.5R; same-bar SL+TP → SL (conservative).
E0 = 1H pin/engulf OR RSI-reclaim toward zone direction on a bar touching the zone.
All signal math reused from backtest_signals; no lookahead (signals at/before fill).

Usage:
  bash scripts/pyrun.sh scripts/trade_outcome.py
  bash scripts/pyrun.sh scripts/trade_outcome.py --week 2026-W25 --instrument audusd
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import db  # noqa: E402
import entry_confluence as ec  # noqa: E402
from zone_ledger import load_ledger, save_ledger  # noqa: E402
from zone_outcomes import (  # noqa: E402  (reuse — do not duplicate)
    week_window, atr14_before, load_tf, min_bar_range,
)
from backtest_signals import (  # noqa: E402
    rsi, pin_bull, pin_bear, bull_engulf, bear_engulf, adx, load_fred,
)

OUTCOMES_CSV = Path("data/trade_outcomes.csv")
OUTCOMES_TABLE = "trade_outcome"
TERMINAL = {"NO_TOUCH", "LIMIT_MISSED", "WIN_TP1", "LOSS_SL", "BREAKEVEN"}
COMPLETED = ["WIN_TP1", "LOSS_SL", "BREAKEVEN"]
EC_FLOOR = 5.0
TP_R = 2.5

OUT_COLS = [
    "zone_id", "instrument", "week", "label", "direction", "zone_confluence", "conviction",
    "status", "e0_present", "ec_score", "ec_flags", "anchor", "sl_dist", "offset", "limit_px",
    "entry", "fill_time", "r_result", "mfe_r", "mae_r", "exit_time",
    "block_flags", "block_verdict", "resolved_utc",
]

# currency → central bank (for the V3 carry flag)
_CCY_BANK = {"USD": "FOMC", "EUR": "ECB", "GBP": "BOE", "JPY": "BOJ",
             "AUD": "RBA", "NZD": "RBNZ", "CAD": "BOC", "CHF": "SNB"}
# instrument → the two currencies it touches
_PAIR_CCY = {
    "xauusd": ["USD"], "eurusd": ["EUR", "USD"], "gbpusd": ["GBP", "USD"],
    "eurgbp": ["EUR", "GBP"], "audusd": ["AUD", "USD"], "nzdusd": ["NZD", "USD"],
    "usdcad": ["USD", "CAD"], "usdchf": ["USD", "CHF"], "usdjpy": ["USD", "JPY"],
    "eurjpy": ["EUR", "JPY"], "gbpjpy": ["GBP", "JPY"],
}
# V1b buffer beyond the zone edge (per-pair, profile approximation)
_V1B_BUF = {"xauusd": 5.0}          # else set by quote convention below
_JPY = {"usdjpy", "eurjpy", "gbpjpy"}


def v1b_buffer(inst: str) -> float:
    if inst in _V1B_BUF:
        return _V1B_BUF[inst]
    return 0.05 if inst in _JPY else 0.0006   # ~5–6 pips


def _cb_dates(year: int) -> dict:
    p = ROOT / "scripts" / "config" / f"cb_calendar_{year}.json"
    if not p.exists():
        return {}
    banks = json.loads(p.read_text()).get("banks", {})
    out = {}
    for bank, b in banks.items():
        out[bank.upper()] = {d["date"] for d in b.get("dates", [])}
    return out


def cb_in_carry(inst: str, fill_time: pd.Timestamp, carry_days: int = 3) -> bool:
    """V3 flag: a relevant central-bank decision falls within the carry horizon after fill."""
    cal = _cb_dates(fill_time.year)
    if not cal:
        return False
    window = {(fill_time.normalize() + pd.Timedelta(days=k)).strftime("%Y-%m-%d")
              for k in range(carry_days + 1)}
    for ccy in _PAIR_CCY.get(inst, []):
        bank = _CCY_BANK.get(ccy)
        if bank and (cal.get(bank, set()) & window):
            return True
    return False


def e0_triggers(h1: pd.DataFrame):
    """Bullish / bearish E0 boolean Series on H1: pin OR engulf OR RSI-reclaim toward fade."""
    r = rsi(h1["close"], 14)
    rsi_up = (r >= 35) & (r.shift() < 35)      # reclaim up out of oversold
    rsi_dn = (r <= 65) & (r.shift() > 65)      # reclaim down out of overbought
    bull = pin_bull(h1) | bull_engulf(h1) | rsi_up
    bear = pin_bear(h1) | bear_engulf(h1) | rsi_dn
    return bull.fillna(False).values, bear.fillna(False).values


def resolve_trade(z: pd.Series, h1: pd.DataFrame, h4: pd.DataFrame, d1: pd.DataFrame,
                  mbr: float) -> dict:
    out = {c: "" for c in OUT_COLS}
    out.update({k: z[k] for k in ["zone_id", "instrument", "week", "label", "direction",
                                  "zone_confluence", "conviction"]})
    inst = z["instrument"]
    start, end = week_window(z["week"])
    top, bot = float(z["zone_top"]), float(z["zone_bottom"])
    mid = (top + bot) / 2
    is_long = z["direction"] == "LONG"
    sign = 1 if is_long else -1

    pub = str(z["published_utc"])
    if pub not in ("", "nan"):
        p = pd.Timestamp(pub)
        pub_ts = p.tz_convert("UTC").tz_localize(None) if p.tz is not None else p
    else:
        pub_ts = start
    live_from = max(start, pub_ts)

    now = h1["datetime"].iloc[-1]
    week_live = now < end
    win = h1[(h1["datetime"] >= live_from) & (h1["datetime"] < end)].reset_index(drop=True)
    touched_mask = (win["low"] <= top) & (win["high"] >= bot)
    if not touched_mask.any():
        out["status"] = "PENDING" if week_live else "NO_TOUCH"
        return out

    # ── signal bar: first E0 at the zone, else first touch (midpoint anchor) ──
    bull, bear = e0_triggers(win)
    trig = bull if is_long else bear
    e0_idx = next((i for i in range(len(win)) if touched_mask[i] and trig[i]), None)
    if e0_idx is not None:
        sig = win.iloc[e0_idx]
        anchor, e0_present, sig_i = float(sig["close"]), True, e0_idx
    else:
        sig_i = int(touched_mask.idxmax())
        anchor, e0_present = mid, False
    sig_time = win.iloc[sig_i]["datetime"]
    out["e0_present"] = e0_present

    # ── SL (constitution formula on closed bars) ──
    d1_atr = atr14_before(d1, pd.Timestamp(sig_time.date()))
    h4_trade = h4[(h4["high"] - h4["low"]) >= mbr]
    h4_atr = atr14_before(h4_trade, sig_time)
    if d1_atr is None or h4_atr is None:
        out["status"] = "PENDING"
        return out
    sl = h4_atr if 0.5 * d1_atr < h4_atr else (0.5 * d1_atr + h4_atr) / 2

    # ── structure_intact (no D1 close beyond zone DURING the zone's live week) ──
    dpre = d1[(d1["datetime"] >= start) & (d1["datetime"] <= sig_time)]
    broke = (dpre["close"] > top).any() if sign < 0 else (dpre["close"] < bot).any()
    structure_intact = not bool(broke)

    # ── EC score (R2) ──
    ec_score, ec_bd = ec.score(inst, is_long, sig_time, top, bot, h1, h4, d1,
                               e0_present, structure_intact)
    out["ec_score"] = ec_score
    out["ec_flags"] = ",".join(ec_bd["flags"])

    # ── offset + limit (outward beyond anchor) ──
    offset = max(sl / 3.0, (10.0 - ec_score) * 0.2 * sl)
    limit = anchor - sign * offset
    out.update({"anchor": round(anchor, 6), "sl_dist": round(sl, 6),
                "offset": round(offset, 6), "limit_px": round(limit, 6)})

    # ── fill: first bar after the signal that pokes the limit (limit re-placed daily
    #    in the live system, so search the rest of the week — fair vs zone_outcome's
    #    whole-week midpoint touch; a never-reached limit = genuine over-wide offset) ──
    after = win.iloc[sig_i + 1:]
    if is_long:
        hit = after[after["low"] <= limit]
    else:
        hit = after[after["high"] >= limit]
    if hit.empty:
        out["status"] = "PENDING" if week_live else "LIMIT_MISSED"
        v1b = _v1b_fired(h4, start, end, top, bot, sign, v1b_buffer(inst))
        out["block_flags"] = ",".join(_gates(
            inst, is_long, sig_time, top, bot, ec_score, h4, d1, structure_intact, v1b))
        out["block_verdict"] = "N/A"
        return out
    fill_time = hit.iloc[0]["datetime"]
    out["fill_time"], out["entry"] = str(fill_time), round(limit, 6)

    # ── manage forward: TP1 2.5R / SL −1R / BE@+1.5R (conservative same-bar = SL) ──
    stop = limit - sign * sl
    tp = limit + sign * TP_R * sl
    be_trigger = limit + sign * 1.5 * sl
    be_armed = False
    mfe = mae = 0.0
    walk = h1[h1["datetime"] >= fill_time]
    for _, bar in walk.iterrows():
        hi, lo = bar["high"], bar["low"]
        fav = (hi - limit) if is_long else (limit - lo)
        adv = (limit - lo) if is_long else (hi - limit)
        mfe, mae = max(mfe, fav / sl), max(mae, adv / sl)
        stopped = lo <= stop if is_long else hi >= stop
        hit_tp = hi >= tp if is_long else lo <= tp
        if stopped:
            out["status"] = "BREAKEVEN" if be_armed and stop == limit else "LOSS_SL"
            out["r_result"] = 0.0 if out["status"] == "BREAKEVEN" else -1.0
            out["exit_time"] = str(bar["datetime"])
            break
        if hit_tp:
            out["status"], out["r_result"] = "WIN_TP1", TP_R
            out["exit_time"] = str(bar["datetime"])
            break
        if not be_armed and (hi >= be_trigger if is_long else lo <= be_trigger):
            be_armed, stop = True, limit
    else:
        out["status"] = "RUNNING"
        out["r_result"] = round(sign * (walk["close"].iloc[-1] - limit) / sl, 2)
    out["mfe_r"], out["mae_r"] = round(mfe, 2), round(mae, 2)

    # ── gate-attribution audit (V1b scanned across the whole week = intra-trade too) ──
    v1b = _v1b_fired(h4, start, end, top, bot, sign, v1b_buffer(inst))
    flags = _gates(inst, is_long, fill_time, top, bot, ec_score, h4, d1, structure_intact, v1b)
    out["block_flags"] = ",".join(flags)
    if not flags or out["r_result"] == "":
        out["block_verdict"] = "CLEAN" if not flags else "N/A"
    else:
        r = float(out["r_result"])
        out["block_verdict"] = "CORRECT_SAVED" if r <= 0 else "COSTLY_REFUSED"
    return out


def _v1b_fired(h4, start, end, top, bot, sign, buf) -> bool:
    """Two consecutive H4 closes beyond zone+buffer anywhere in the zone's live week
    (entry OR intra-trade) — the mid-week invalidation gate."""
    win = h4[(h4["datetime"] >= start) & (h4["datetime"] < end)]
    if len(win) < 2:
        return False
    thr = (top + buf) if sign < 0 else (bot - buf)
    beyond = (win["close"] > thr) if sign < 0 else (win["close"] < thr)
    b = beyond.values
    return bool((b[:-1] & b[1:]).any())


def _gates(inst, is_long, t, top, bot, ec_score, h4, d1, structure_intact, v1b) -> list:
    """Hard gates as non-suppressing flags. V1/V3/VETO/EC at the fill bar; V1b is the
    week-scanned intra-trade invalidation (passed in)."""
    t = pd.Timestamp(t)
    sign = 1 if is_long else -1
    flags = []

    # V1 — D1 close beyond zone during the live week
    if not structure_intact:
        flags.append("V1")

    # V1b — mid-week intra-trade invalidation (computed across the week)
    if v1b and "V1" not in flags:
        flags.append("V1b")

    # V3 — relevant CB decision within the carry horizon
    if cb_in_carry(inst, t):
        flags.append("V3")

    # VETO-VIX (>35) — xauusd shorts / FX longs
    s = load_fred("VIXCLS")
    if s is not None:
        s = s[s.index <= t]
        if not s.empty and float(s.iloc[-1]) > 35:
            if (inst == "xauusd" and not is_long) or (inst != "xauusd" and is_long):
                flags.append("VETO_VIX")

    # VETO-ADX (D1 ADX>30 trending against a fade)
    dpre = d1[d1["datetime"] <= t]
    if len(dpre) >= 30 and float(adx(dpre, 14).iloc[-1]) > 30:
        flags.append("VETO_ADX")

    # INTERVENTION — JPY MoF band (static config)
    if inst in _JPY and _intervention_band(inst, t):
        flags.append("INTERVENTION")

    # EC floor
    if ec_score < EC_FLOOR:
        flags.append("EC_FLOOR")
    return flags


def _intervention_band(inst, t) -> bool:
    p = ROOT / "scripts" / "config" / "intervention_watch.json"
    if not p.exists():
        return False
    try:
        cfg = json.loads(p.read_text())
    except Exception:
        return False
    # advisory only: flag if the config marks the pair active (band check needs spot we lack here)
    pairs = cfg.get("pairs", cfg.get("instruments", {}))
    entry = pairs.get(inst) if isinstance(pairs, dict) else None
    return bool(entry and entry.get("active", entry.get("regime_active", False)))


def summarize(df: pd.DataFrame):
    print("\n── trade_outcome summary " + "─" * 38)
    print(df["status"].value_counts().to_string())
    done = df[df["status"].isin(COMPLETED)].copy()
    if not done.empty:
        r = pd.to_numeric(done["r_result"])
        wins = (done["status"] == "WIN_TP1").sum()
        print(f"\nSYSTEM P&L — filled {len(done)} | wins {wins} ({wins/len(done):.0%}) | "
              f"total {r.sum():+.1f}R | avg {r.mean():+.2f}R")

    # gate accuracy
    print("\n── gate accuracy (counterfactual: filled despite the gate) " + "─" * 4)
    print(f"{'gate':<14}{'nBlock':>7}{'win%':>7}{'totR':>8}  verdict")
    gates = ["V1", "V1b", "V3", "VETO_VIX", "VETO_ADX", "INTERVENTION", "EC_FLOOR"]
    fl = df["block_flags"].fillna("")
    for g in gates:
        m = fl.apply(lambda s: g in s.split(",") if s else False)
        sub = df[m & df["status"].isin(COMPLETED)]
        if sub.empty:
            print(f"{g:<14}{int(m.sum()):>7}{'—':>7}{'—':>8}  (no completed)")
            continue
        r = pd.to_numeric(sub["r_result"])
        w = (sub["status"] == "WIN_TP1").mean()
        verdict = "KEEPS EDGE" if r.sum() <= 0 else "COSTING EDGE"
        print(f"{g:<14}{int(m.sum()):>7}{w:>6.0%}{r.sum():>+8.1f}  {verdict}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", default="")
    ap.add_argument("--instrument", default="")
    args = ap.parse_args()

    ledger = load_ledger()
    if ledger.empty:
        sys.exit("ledger empty — register zones with zone_ledger.py first")
    todo = ledger.copy()
    if args.week:
        todo = todo[todo["week"] == args.week]
    if args.instrument:
        todo = todo[todo["instrument"] == args.instrument]

    rows, cache = [], {}
    for _, z in todo.iterrows():
        inst = z["instrument"]
        if inst not in cache:
            cache[inst] = (load_tf(inst, "1h"), load_tf(inst, "4h"),
                           load_tf(inst, "1day"), min_bar_range(inst))
        h1, h4, d1, mbr = cache[inst]
        out = resolve_trade(z, h1, h4, d1, mbr)
        out["resolved_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append(out)
        rr = f" ({out['r_result']:+.1f}R)" if out["r_result"] != "" else ""
        bf = f" [{out['block_flags']}]" if out["block_flags"] else ""
        print(f"{z['zone_id']:<32} {z['direction']:<5} EC{str(out['ec_score']):>4} "
              f"→ {out['status']}{rr}{bf}")

    res = pd.DataFrame(rows)[OUT_COLS]
    old = db.read_table(OUTCOMES_TABLE)
    if not old.empty and "zone_id" in old.columns:
        old = old[~old["zone_id"].isin(res["zone_id"])]
        if not old.empty:
            res = pd.concat([old.astype(str), res.astype(str)], ignore_index=True)
    db.write_table(OUTCOMES_TABLE, res, mirror_csv=OUTCOMES_CSV)
    print(f"\n→ {OUTCOMES_TABLE} table + {OUTCOMES_CSV} ({len(res)} rows)")
    summarize(res)


if __name__ == "__main__":
    main()
