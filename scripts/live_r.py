"""
live_r.py — recompute live R + SL/TP status for OPEN positions from the latest OHLC.

The `trade` table stores r_actual only once a position is CLOSED. For OPEN rows this
recomputes, from the bars since fill_time, the current unrealized R, whether SL/TP1/TP2
were touched, and MFE/MAE in R — read off the actual bar highs/lows, never a cached
number. This is the source-of-truth fix for the 2026-06-15 USDCHF stale-R bug: R must
come from the bar that hit SL, not from `_HOT.md` or live spot.

Chronological scan per trade: the FIRST bar to touch SL (-1R) or TP2 (+R) ends the
position at that bar; otherwise it is still open and R is marked-to-market off the last
close. TP1 (manual, 2.5R) and BE (+1.5R) are human management decisions, so they are
surfaced as `tp1_touched` flags rather than auto-resolved. Intrabar SL+TP2 on the same
bar is ambiguous → resolved SL-first (conservative) and flagged.

Reusable: `live_metrics(trade_row, bars)` → dict — imported by the frontend export step.
CLI:
    bash scripts/pyrun.sh scripts/live_r.py [--tf 1h] [--include-pending] [--id <trade_id>]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # for `db` import
import db  # noqa: E402

OPEN_STATUSES = {"OPEN"}
PENDING_STATUSES = {"PENDING"}


def _f(v):
    """Parse a stored (text) numeric → float, or None if blank/garbage."""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _bars_since(bars: pd.DataFrame, fill_time: str) -> pd.DataFrame:
    """Bars at/after fill_time, chronological, with numeric H/L/C. ohlc datetimes are
    'YYYY-MM-DD HH:MM:SS'; fill_time is ISO 'YYYY-MM-DDTHH:MM:SSZ' — both → UTC."""
    if bars.empty:
        return bars
    b = bars.copy()
    b["dt"] = pd.to_datetime(b["datetime"], utc=True, errors="coerce")
    for c in ("high", "low", "close"):
        b[c] = pd.to_numeric(b[c], errors="coerce")
    b = b.dropna(subset=["dt", "high", "low", "close"]).sort_values("dt")
    if fill_time:
        ft = pd.to_datetime(fill_time, utc=True, errors="coerce")
        if pd.notna(ft):
            b = b[b["dt"] >= ft]
    return b


def live_metrics(row: dict, bars: pd.DataFrame) -> dict:
    """Recompute unrealized R + SL/TP touch state for one OPEN trade from `bars`
    (one symbol/tf slice, columns datetime,open,high,low,close,volume as strings).
    Returns a dict; `status` field describes the recompute outcome, not the trade table."""
    entry, sl, stop = _f(row.get("entry")), _f(row.get("sl")), _f(row.get("stop_dist"))
    tp, tp2 = _f(row.get("tp")), _f(row.get("tp2"))
    direction = (row.get("direction") or "").upper()
    out = {
        "r_current": None, "sl_status": "INTACT", "outcome": "OPEN",
        "tp1_touched": False, "tp2_touched": False, "mfe_r": None, "mae_r": None,
        "last_px": None, "as_of": None, "hit_time": None, "ambiguous": False,
    }
    if entry is None or sl is None or not stop or direction not in ("LONG", "SHORT"):
        out["outcome"] = "BAD_ROW"
        return out
    b = _bars_since(bars, row.get("fill_time") or "")
    if b.empty:
        out["outcome"] = "NO_BARS"
        return out

    sign = 1.0 if direction == "LONG" else -1.0

    def r_at(px: float) -> float:
        return round(sign * (px - entry) / stop, 3)

    mfe = mae = 0.0
    last_close = None
    for _, bar in b.iterrows():
        hi, lo, cl = bar["high"], bar["low"], bar["close"]
        last_close = cl
        out["as_of"] = str(bar["dt"])
        # excursion in R from this bar's extremes
        fav = r_at(hi) if direction == "LONG" else r_at(lo)
        adv = r_at(lo) if direction == "LONG" else r_at(hi)
        mfe, mae = max(mfe, fav), min(mae, adv)
        # touch detection
        sl_touch = (lo <= sl) if direction == "LONG" else (hi >= sl)
        tp2_touch = tp2 is not None and ((hi >= tp2) if direction == "LONG" else (lo <= tp2))
        tp1_touch = tp is not None and ((hi >= tp) if direction == "LONG" else (lo <= tp))
        if tp1_touch:
            out["tp1_touched"] = True
        if sl_touch and tp2_touch:
            out["ambiguous"] = True       # same bar hit both → SL-first
        if sl_touch:
            out.update(r_current=-1.0, sl_status="HIT", outcome="SL_HIT",
                       hit_time=str(bar["dt"]), mfe_r=round(mfe, 3), mae_r=round(mae, 3),
                       last_px=lo)
            return out
        if tp2_touch:
            out.update(r_current=r_at(tp2), tp2_touched=True, outcome="TP2_HIT",
                       hit_time=str(bar["dt"]), mfe_r=round(mfe, 3), mae_r=round(mae, 3),
                       last_px=tp2)
            return out
    # still open → mark to market off last close
    out.update(r_current=r_at(last_close), last_px=last_close,
               mfe_r=round(mfe, 3), mae_r=round(mae, 3))
    return out


def _symbol(instrument: str) -> str:
    return db.clean_symbol(instrument)


def cmd_run(args):
    df = db.read_table("trade")
    if df.empty:
        print("trade table empty")
        return
    want = set(OPEN_STATUSES)
    if args.include_pending:
        want |= PENDING_STATUSES
    if args.id:
        df = df[df["trade_id"] == args.id]
    else:
        df = df[df["status"].isin(want)]
    if df.empty:
        print(f"no {'/'.join(sorted(want))} trades" + (f" matching {args.id}" if args.id else ""))
        return

    rows = []
    for _, t in df.iterrows():
        if t["status"] in PENDING_STATUSES:
            rows.append((t["trade_id"], t["status"], "—", "PENDING(no fill)", "—", "—"))
            continue
        bars = db.read_ohlc(_symbol(t["instrument"]), args.tf)
        m = live_metrics(t.to_dict(), bars)
        rc = "—" if m["r_current"] is None else f'{m["r_current"]:+.2f}'
        rows.append((
            t["trade_id"], t["status"], rc,
            m["outcome"] + ("*" if m["ambiguous"] else ""),
            "—" if m["mae_r"] is None else f'{m["mae_r"]:+.2f}',
            (m["hit_time"] or m["as_of"] or "—"),
        ))
    w = max(len(r[0]) for r in rows)
    print(f'{"trade_id":<{w}}  {"db_status":<10} {"liveR":>7} {"recompute":<12} {"MAE_R":>7}  as_of')
    for tid, st, rc, oc, mae, ts in rows:
        print(f"{tid:<{w}}  {st:<10} {rc:>7} {oc:<12} {mae:>7}  {ts}")
    if any(r[3].endswith("*") for r in rows):
        print("\n* intrabar SL+TP2 on one bar — resolved SL-first (conservative)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tf", default="1h", choices=["15min", "1h", "4h", "1day"],
                    help="OHLC timeframe for the recompute (default 1h)")
    ap.add_argument("--include-pending", action="store_true",
                    help="also list PENDING (unfilled) orders")
    ap.add_argument("--id", default="", help="recompute a single trade_id (any status)")
    ap.set_defaults(func=cmd_run)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
