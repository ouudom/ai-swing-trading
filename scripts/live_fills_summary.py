"""
live_fills_summary — Telegram-ready digest of zones that actually filled this week.

Reads the `trade_outcome` table (entry-mechanics replay, written by `trade_outcome.py`)
for one ISO week and prints one line per zone whose limit actually filled — status in
WIN_TP1 / WIN_TP2 / LOSS_SL / BREAKEVEN / RUNNING — plus a net-closed / running R
footer. PENDING / NO_TOUCH / LIMIT_MISSED zones never filled, so they're excluded.

A /validate snapshot only sees zones live RIGHT NOW; it cannot see a limit that filled
earlier in the week. This is the source of truth for what actually filled (run after
`trade_outcome.py --week <WK>` refreshes the table — see the `swing-validate-hourly`
scheduled task, step 2).

Plain text, no markdown — spliced verbatim into the hourly Telegram message
(`notify_telegram.py` sends with no parse_mode). Prints NOTHING (empty stdout) when no
zone filled this week — callers branch on empty/non-empty output, not on exit code.

Usage:
  bash scripts/pyrun.sh scripts/live_fills_summary.py --week 2026-W27
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # for `db` import
import db  # noqa: E402

TABLE = "trade_outcome"
NEEDED_COLS = ["week", "instrument", "label", "direction", "status", "r_result", "fill_time"]
QUALIFYING = ["WIN_TP1", "WIN_TP2", "LOSS_SL", "BREAKEVEN", "RUNNING"]
EMOJI = {"WIN_TP1": "🟢", "WIN_TP2": "🟢", "LOSS_SL": "🔴", "BREAKEVEN": "⚪", "RUNNING": "⏳"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", required=True, help="ISO trade week, e.g. 2026-W27")
    args = ap.parse_args()

    df = db.read_table(TABLE, columns=NEEDED_COLS)
    sub = df[(df["week"] == args.week) & df["status"].isin(QUALIFYING)].copy()
    if sub.empty:
        return

    sub["r_result"] = pd.to_numeric(sub["r_result"])
    sub = sub.sort_values("fill_time")

    lines = [f"📈 Filled {args.week}"]
    for _, z in sub.iterrows():
        tag = " (open)" if z["status"] == "RUNNING" else ""
        lines.append(f"{EMOJI[z['status']]} {z['instrument'].upper()}-{z['label']} "
                     f"{z['direction']} — {z['status']} {z['r_result']:+.1f}R{tag}")

    closed = sub[sub["status"] != "RUNNING"]
    running = sub[sub["status"] == "RUNNING"]
    foot = []
    if not closed.empty:
        foot.append(f"Net closed: {closed['r_result'].sum():+.1f}R")
    if not running.empty:
        foot.append(f"Running: {running['r_result'].sum():+.1f}R ({len(running)} open)")
    lines += ["", " · ".join(foot)]

    print("\n".join(lines))


if __name__ == "__main__":
    main()
