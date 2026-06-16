"""
V1b — Intraday H4 invalidation checker (markdown-only, no DB).

Checks the last 2 H4 closes in data/twelvedata/{instrument}/4h.csv against a
trading-zone extreme. Flags 2 consecutive H4 closes >$BUFFER past the zone =
intraday invalidation (cancel limit before D1 close confirms).

Zone is passed on the CLI by /validate (read from _HOT.md active zones).
Run at each H4 boundary (00/04/08/12/16/20 UTC) — manually or via cron.

Usage:
    bash scripts/pyrun.sh scripts/check_v1b.py --direction SHORT --zone-top 3400 --zone-bottom 3380
    bash scripts/pyrun.sh scripts/check_v1b.py --direction LONG  --zone-top 3300 --zone-bottom 3280 --buffer 5

Exit codes: 0 intact / 2 breach.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instrument", default="xauusd")
    parser.add_argument("--direction", required=True, choices=["LONG", "SHORT"])
    parser.add_argument("--zone-top", type=float, required=True)
    parser.add_argument("--zone-bottom", type=float, required=True)
    parser.add_argument("--buffer", type=float, default=5.0,
                        help="$ past zone extreme that counts as a real breach (default 5.0)")
    parser.add_argument("--label", default="", help="optional zone label for output")
    args = parser.parse_args()

    h4 = None
    try:
        import db
        h4 = db.read_ohlc(args.instrument, "4h")          # canonical store
    except Exception:
        h4 = None
    if h4 is None or h4.empty:
        h4_csv = Path(f"data/twelvedata/{args.instrument}/4h.csv")   # CSV fallback
        if not h4_csv.exists():
            print(f"❌ Missing {h4_csv}")
            sys.exit(1)
        h4 = pd.read_csv(h4_csv)
    h4 = h4.copy()
    h4["datetime"] = pd.to_datetime(h4["datetime"])
    for c in ["open", "high", "low", "close"]:
        if c in h4.columns:
            h4[c] = pd.to_numeric(h4[c], errors="coerce")
    h4 = h4.sort_values("datetime")
    last2 = h4.tail(2)
    if len(last2) < 2:
        print("Not enough H4 bars.")
        return

    c1, c2 = float(last2["close"].iloc[0]), float(last2["close"].iloc[1])
    # Display precision: $-scale (gold, >=500) 2dp; JPY-scale (20–500, pip 0.01) 3dp; pip-scale FX 5dp.
    dp = 2 if args.zone_top >= 500 else (3 if args.zone_top >= 20 else 5)
    print(f"V1b check ({args.instrument}{' ' + args.label if args.label else ''}) — last 2 H4 closes: "
          f"{c1:.{dp}f} @ {last2['datetime'].iloc[0]} | "
          f"{c2:.{dp}f} @ {last2['datetime'].iloc[1]}")

    if args.direction == "SHORT":
        extreme = args.zone_top + args.buffer
        breach = (c1 > extreme) and (c2 > extreme)
    else:
        extreme = args.zone_bottom - args.buffer
        breach = (c1 < extreme) and (c2 < extreme)

    verdict = "❌ V1b BREACH — INVALIDATE" if breach else "✅ intact"
    print(f"{args.direction} zone {args.zone_bottom:.{dp}f}–{args.zone_top:.{dp}f} | "
          f"threshold {extreme:.{dp}f} | {verdict}")

    if breach:
        print("\n→ Cancel live limit for this zone. Remove zone from _HOT.md.")
        sys.exit(2)


if __name__ == "__main__":
    main()
