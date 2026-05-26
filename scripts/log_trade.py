"""
Append a row to data/trades_log.csv when an order fills or closes.

Schema:
  date,week,setup,direction,entry,sl,tp,lots,stop_dist,r_planned,
  fill_time,exit_time,exit_px,exit_reason,r_actual,mfe,mae,notes

Usage (two-stage: log fill first, update on exit):

  # When limit fills
  .venv/bin/python scripts/log_trade.py fill \
      --setup A --direction SELL --entry 4590.24 --sl 4615.64 --tp 4501.11 \
      --lots 0.78 --stop-dist 25.40 --r-planned 3.51 --fill-time "2026-05-26 14:30"

  # When trade exits (matches latest open row for that setup)
  .venv/bin/python scripts/log_trade.py exit \
      --setup A --exit-time "2026-05-27 09:15" --exit-px 4501.11 \
      --exit-reason TP --r-actual 3.51 --mfe 3.55 --mae -0.40 \
      --notes "PCE day, exited 30min before release"
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("data/trades_log.csv")
COLUMNS = [
    "date", "week", "setup", "direction", "entry", "sl", "tp", "lots",
    "stop_dist", "r_planned", "fill_time", "exit_time", "exit_px",
    "exit_reason", "r_actual", "mfe", "mae", "notes",
]


def ensure_header():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        with LOG_PATH.open("w", newline="") as f:
            csv.writer(f).writerow(COLUMNS)


def read_all():
    if not LOG_PATH.exists():
        return []
    with LOG_PATH.open() as f:
        return list(csv.DictReader(f))


def write_all(rows):
    with LOG_PATH.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in COLUMNS})


def cmd_fill(args):
    ensure_header()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    iso = datetime.strptime(today, "%Y-%m-%d").isocalendar()
    week = f"{iso[0]}-W{iso[1]:02d}"
    row = {
        "date": today, "week": week, "setup": args.setup,
        "direction": args.direction, "entry": args.entry, "sl": args.sl,
        "tp": args.tp, "lots": args.lots, "stop_dist": args.stop_dist,
        "r_planned": args.r_planned, "fill_time": args.fill_time,
    }
    rows = read_all()
    rows.append(row)
    write_all(rows)
    print(f"✅ Logged fill: {args.setup} {args.direction} @ {args.entry} | {args.lots} lots | {LOG_PATH}")


def cmd_exit(args):
    rows = read_all()
    if not rows:
        print("❌ No trades logged.")
        return
    # find latest open row matching setup
    target_idx = None
    for i in range(len(rows) - 1, -1, -1):
        if rows[i]["setup"] == args.setup and not rows[i].get("exit_time"):
            target_idx = i
            break
    if target_idx is None:
        print(f"❌ No open trade for setup {args.setup}.")
        return
    rows[target_idx].update({
        "exit_time": args.exit_time, "exit_px": args.exit_px,
        "exit_reason": args.exit_reason, "r_actual": args.r_actual,
        "mfe": args.mfe or "", "mae": args.mae or "",
        "notes": args.notes or "",
    })
    write_all(rows)
    print(f"✅ Closed trade {args.setup}: {args.exit_reason} @ {args.exit_px} | R={args.r_actual}")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fill", help="Log a new fill")
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
    args.r_planned = getattr(args, "r_planned", None)
    args.func(args)
