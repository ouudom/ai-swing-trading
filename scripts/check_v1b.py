"""
V1b — Intraday H4 invalidation checker.

Reads active setups from the DB, checks last 2 H4 closes in data/twelvedata/{instrument}/4h.csv.
Flags any setup with 2 consecutive H4 closes >$5 past zone extreme.

Run at each H4 boundary (00/04/08/12/16/20 UTC) — manually or via cron.

Usage:
    .venv/bin/python scripts/check_v1b.py --instrument xauusd
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# Allow imports from project root
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from db import init_db
from db.crud import get_active_setups

BUFFER = 5.0  # $ past zone extreme that counts as a real breach (not noise)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instrument", default="xauusd", help="Instrument to check (default: xauusd)")
    args = parser.parse_args()

    init_db()
    setups = get_active_setups(instrument=args.instrument)
    if not setups:
        print(f"No active setups for {args.instrument}.")
        return

    h4_csv = Path(f"data/twelvedata/{args.instrument}/4h.csv")
    if not h4_csv.exists():
        print(f"❌ Missing {h4_csv}")
        sys.exit(1)

    h4 = pd.read_csv(h4_csv, parse_dates=["datetime"]).sort_values("datetime")
    last2 = h4.tail(2)
    if len(last2) < 2:
        print("Not enough H4 bars.")
        return

    print(f"V1b check ({args.instrument}) — last 2 H4 closes: "
          f"${last2['close'].iloc[0]:.2f} @ {last2['datetime'].iloc[0]} | "
          f"${last2['close'].iloc[1]:.2f} @ {last2['datetime'].iloc[1]}")
    print()

    any_breach = False
    for s in setups:
        c1, c2 = float(last2["close"].iloc[0]), float(last2["close"].iloc[1])
        if s.direction.value == "SHORT":
            breach = (c1 > s.zone_top + BUFFER) and (c2 > s.zone_top + BUFFER)
            extreme = s.zone_top + BUFFER
        else:
            breach = (c1 < s.zone_bottom - BUFFER) and (c2 < s.zone_bottom - BUFFER)
            extreme = s.zone_bottom - BUFFER
        verdict = "❌ V1b BREACH — INVALIDATE" if breach else "✅ intact"
        print(f"Setup {s.setup_letter.value} ({s.direction.value}) "
              f"zone ${s.zone_bottom:.2f}–${s.zone_top:.2f} | "
              f"threshold ${extreme:.2f} | {verdict}")
        if breach:
            any_breach = True

    if any_breach:
        print("\n→ Cancel live limits for breached setups. Update active_setups lifecycle to INVALIDATED.")
        sys.exit(2)


if __name__ == "__main__":
    main()
