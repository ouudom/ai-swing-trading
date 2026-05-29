"""
Log a trade fill or exit to the SQLite DB, then re-export trades_log.csv.

Schema:
  date,week,instrument,setup,direction,entry,sl,tp,lots,stop_dist,r_planned,
  fill_time,exit_time,exit_px,exit_reason,r_actual,mfe,mae,notes

Usage (two-stage: log fill first, update on exit):

  # When limit fills
  .venv/bin/python scripts/log_trade.py fill \
      --instrument xauusd --setup A --direction SELL --entry 4590.24 --sl 4615.64 --tp 4501.11 \
      --lots 0.78 --stop-dist 25.40 --r-planned 3.51 --fill-time "2026-05-26 14:30"

  # When trade exits (matches latest open row for that setup)
  .venv/bin/python scripts/log_trade.py exit \
      --setup A --exit-time "2026-05-27 09:15" --exit-px 4501.11 \
      --exit-reason TP --r-actual 3.51 --mfe 3.55 --mae -0.40 \
      --notes "PCE day, exited 30min before release"
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

# Allow imports from project root
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from db import init_db
from db.crud import create_trade, get_open_trades, update_trade_exit
from render.trade_csv import export_trades_to_csv
from schemas import Direction, ExitReason, SetupLetter, Trade

CSV_PATH = Path("data/trades_log.csv")


def cmd_fill(args):
    init_db()
    today = date.today()
    iso_week = today.isocalendar()
    week = f"{iso_week[0]}-W{iso_week[1]:02d}"

    trade = Trade(
        date=today,
        week=week,
        instrument=args.instrument,
        setup=SetupLetter(args.setup),
        direction=Direction(args.direction),
        entry=float(args.entry),
        sl=float(args.sl),
        tp=float(args.tp),
        lots=float(args.lots),
        stop_dist=float(args.stop_dist),
        r_planned=float(args.r_planned),
        fill_time=datetime.fromisoformat(args.fill_time),
    )
    created = create_trade(trade)
    export_trades_to_csv(CSV_PATH, get_open_trades() + [created])
    print(f"✅ Logged fill: {args.setup} {args.direction} @ {args.entry} | {args.lots} lots | DB id={created.id}")


def cmd_exit(args):
    init_db()
    open_trades = get_open_trades()
    # Find latest open trade matching setup letter
    target = None
    for t in reversed(open_trades):
        if t.setup.value == args.setup:
            target = t
            break
    if target is None:
        print(f"❌ No open trade for setup {args.setup}.")
        sys.exit(1)

    updated = update_trade_exit(
        trade_id=target.id,
        exit_time=datetime.fromisoformat(args.exit_time),
        exit_px=float(args.exit_px),
        exit_reason=args.exit_reason,
        r_actual=float(args.r_actual) if args.r_actual else None,
        mfe=float(args.mfe) if args.mfe else None,
        mae=float(args.mae) if args.mae else None,
        notes=args.notes,
    )
    if updated is None:
        print(f"❌ Failed to update trade {target.id}.")
        sys.exit(1)

    # Re-export full trade history to CSV
    from db.crud import get_all_trades
    export_trades_to_csv(CSV_PATH, get_all_trades())
    print(f"✅ Closed trade {args.setup}: {args.exit_reason} @ {args.exit_px} | R={args.r_actual}")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fill", help="Log a new fill")
    f.add_argument("--instrument", required=True, help="Instrument symbol (e.g. xauusd)")
    for arg in ["--setup", "--direction", "--entry", "--sl", "--tp",
                "--lots", "--stop-dist", "--r-planned", "--fill-time"]:
        f.add_argument(arg, required=True)
    f.set_defaults(func=cmd_fill)

    e = sub.add_parser("exit", help="Update existing fill with exit details")
    for arg in ["--setup", "--exit-time", "--exit-px", "--exit-reason", "--r-actual"]:
        e.add_argument(arg, required=True)
    e.add_argument("--mfe")
    e.add_argument("--mae")
    e.add_argument("--notes")
    e.set_defaults(func=cmd_exit)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
