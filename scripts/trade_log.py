"""
Trade log — real order/fill/exit registry (distinct from the shadow zone ledger).

Lifecycle of one row, keyed by trade_id = {instrument}-{week}-{setup}:
    order  → status PENDING  (an order limit is live, awaiting fill)
    fill   → status OPEN      (the limit filled; a real position is on)
    close  → status WIN_TP1 | WIN_TP2 | LOSS | BE | exit reason (position flat)
    cancel → status CANCELLED (order expired / pulled, never filled)

This is the file calibration.py reads for REAL-trade (R2 / Entry Confluence) stats —
only rows with r_actual count. zone_ledger.py / zone_outcomes.py remain the *shadow*
side (every published zone, filled or not). Link the two via --zone-id.

Usage:
    bash scripts/pyrun.sh scripts/trade_log.py order \
        --instrument usdchf --week 2026-W24 --setup PRIMARY --direction LONG \
        --entry 0.79477 --sl 0.79234 --tp 0.80085 --tp2 0.80206 --lots 8.23 \
        [--expiry 2026-06-12T21:00:00Z] [--zone-id usdchf-2026-W24-PRIMARY] [--notes "..."]
    bash scripts/pyrun.sh scripts/trade_log.py fill   --id usdchf-2026-W24-PRIMARY [--fill-px 0.79477] [--fill-time ...]
    bash scripts/pyrun.sh scripts/trade_log.py close  --id usdchf-2026-W24-PRIMARY --status WIN_TP1 --exit-px 0.80085 [--r-actual 2.5] [--mfe ..] [--mae ..]
    bash scripts/pyrun.sh scripts/trade_log.py cancel --id usdchf-2026-W24-PRIMARY [--reason "expired no fill"]
    bash scripts/pyrun.sh scripts/trade_log.py list   [--instrument usdchf] [--status PENDING]

--id may be omitted on fill/close/cancel when exactly one matching live row exists
(filter with --instrument / --setup); the latest live row is then chosen.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

TRADES_CSV = Path("data/trades_log.csv")

COLUMNS = [
    "trade_id", "instrument", "date", "week", "setup", "direction", "status",
    "entry", "sl", "tp", "tp2", "lots", "stop_dist", "r_planned", "expiry",
    "zone_id", "fill_time", "exit_time", "exit_px", "exit_reason", "r_actual",
    "mfe", "mae", "notes",
]

# statuses where the order/position is still live and can be filled/closed/cancelled
LIVE = {"PENDING", "OPEN"}
CLOSE_STATUSES = ["WIN_TP1", "WIN_TP2", "LOSS", "BE", "MANUAL", "INVALIDATED"]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load() -> pd.DataFrame:
    if TRADES_CSV.exists() and TRADES_CSV.stat().st_size > 0:
        df = pd.read_csv(TRADES_CSV, dtype=str).fillna("")  # all-string: no dtype churn on edit
        for c in COLUMNS:            # tolerate older/narrower headers
            if c not in df.columns:
                df[c] = ""
        return df
    return pd.DataFrame({c: pd.Series(dtype=str) for c in COLUMNS})


def save(df: pd.DataFrame):
    TRADES_CSV.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(TRADES_CSV) + ".tmp"
    df[COLUMNS].to_csv(tmp, index=False)
    Path(tmp).replace(TRADES_CSV)


def resolve_id(df: pd.DataFrame, args) -> str:
    """Find the target trade_id for fill/close/cancel."""
    if getattr(args, "id", None):
        if not (df["trade_id"] == args.id).any():
            sys.exit(f"❌ no row trade_id={args.id}")
        return args.id
    live = df[df["status"].isin(LIVE)]
    if getattr(args, "instrument", None):
        live = live[live["instrument"] == args.instrument]
    if getattr(args, "setup", None):
        live = live[live["setup"] == args.setup]
    if live.empty:
        sys.exit("❌ no live (PENDING/OPEN) row matches — pass --id")
    if len(live) > 1:
        ids = ", ".join(live["trade_id"].tolist())
        sys.exit(f"❌ {len(live)} live rows match — pass --id ({ids})")
    return live.iloc[0]["trade_id"]


def cmd_order(args):
    stop_dist = args.stop_dist if args.stop_dist is not None else round(abs(args.entry - args.sl), 6)
    if stop_dist <= 0:
        sys.exit("❌ stop_dist is 0 — entry equals sl")
    r_planned = (args.r_planned if args.r_planned is not None
                 else round(abs(args.tp - args.entry) / stop_dist, 2))
    trade_id = f"{args.instrument}-{args.week}-{args.setup}"
    df = load()
    if (df["trade_id"] == trade_id).any():
        if not args.force:
            sys.exit(f"❌ {trade_id} already logged — use --force to overwrite")
        df = df[df["trade_id"] != trade_id]

    row = {c: "" for c in COLUMNS}
    row.update({
        "trade_id": trade_id, "instrument": args.instrument,
        "date": args.date or now_utc()[:10], "week": args.week, "setup": args.setup,
        "direction": args.direction, "status": "PENDING",
        "entry": args.entry, "sl": args.sl, "tp": args.tp,
        "tp2": args.tp2 if args.tp2 is not None else "", "lots": args.lots,
        "stop_dist": stop_dist, "r_planned": r_planned, "expiry": args.expiry or "",
        "zone_id": args.zone_id or trade_id, "notes": args.notes or "",
    })
    new = pd.DataFrame([row])
    df = new if df.empty else pd.concat([df, new], ignore_index=True)
    save(df)
    print(f"✅ ORDER LIMIT logged: {trade_id}  {args.direction} {args.entry} "
          f"| SL {args.sl} | TP {args.tp} | {args.lots} lots | {r_planned}R planned → {TRADES_CSV}")


def cmd_fill(args):
    df = load()
    tid = resolve_id(df, args)
    i = df.index[df["trade_id"] == tid][0]
    if df.at[i, "status"] != "PENDING":
        sys.exit(f"❌ {tid} is {df.at[i, 'status']}, not PENDING — cannot fill")
    df.at[i, "status"] = "OPEN"
    df.at[i, "fill_time"] = args.fill_time or now_utc()
    note = ""
    if args.fill_px is not None:
        prev = float(df.at[i, "entry"])
        df.at[i, "entry"] = args.fill_px
        if abs(args.fill_px - prev) > 1e-9:
            note = f" (filled {args.fill_px} vs limit {prev})"
    save(df)
    print(f"✅ FILLED → OPEN: {tid} @ {df.at[i, 'fill_time']}{note}")


def cmd_close(args):
    df = load()
    tid = resolve_id(df, args)
    i = df.index[df["trade_id"] == tid][0]
    if df.at[i, "status"] not in LIVE:
        sys.exit(f"❌ {tid} is {df.at[i, 'status']} — already closed")
    df.at[i, "status"] = args.status
    df.at[i, "exit_time"] = args.exit_time or now_utc()
    if args.exit_px is not None:
        df.at[i, "exit_px"] = args.exit_px
    df.at[i, "exit_reason"] = args.reason or args.status
    if args.r_actual is not None:
        df.at[i, "r_actual"] = args.r_actual
    if args.mfe is not None:
        df.at[i, "mfe"] = args.mfe
    if args.mae is not None:
        df.at[i, "mae"] = args.mae
    save(df)
    print(f"✅ CLOSED {tid}: {args.status} @ {df.at[i, 'exit_px'] or '?'} "
          f"| r_actual {df.at[i, 'r_actual'] or '—'}")


def cmd_cancel(args):
    df = load()
    tid = resolve_id(df, args)
    i = df.index[df["trade_id"] == tid][0]
    if df.at[i, "status"] != "PENDING":
        sys.exit(f"❌ {tid} is {df.at[i, 'status']}, not PENDING — only unfilled orders cancel")
    df.at[i, "status"] = "CANCELLED"
    df.at[i, "exit_time"] = now_utc()
    df.at[i, "exit_reason"] = args.reason or "cancelled"
    save(df)
    print(f"✅ CANCELLED {tid}: {args.reason or 'cancelled'}")


def cmd_list(args):
    df = load()
    if df.empty:
        print("trade log empty")
        return
    if args.instrument:
        df = df[df["instrument"] == args.instrument]
    if args.status:
        df = df[df["status"] == args.status]
    if df.empty:
        print("no matching rows")
        return
    cols = ["trade_id", "direction", "status", "entry", "sl", "tp",
            "lots", "r_planned", "r_actual"]
    print(df[cols].to_string(index=False))
    print(f"\n{len(df)} rows | status: {df['status'].value_counts().to_dict()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("order", help="log a placed order limit (PENDING)")
    o.add_argument("--instrument", required=True)
    o.add_argument("--week", required=True, help="ISO trade week, e.g. 2026-W24")
    o.add_argument("--setup", required=True, help="zone label, e.g. PRIMARY/SECONDARY/COUNTER")
    o.add_argument("--direction", required=True, choices=["LONG", "SHORT"])
    o.add_argument("--entry", type=float, required=True, help="order limit price")
    o.add_argument("--sl", type=float, required=True)
    o.add_argument("--tp", type=float, required=True, help="TP1 (2.5R, manual close)")
    o.add_argument("--tp2", type=float, default=None, help="TP2 (3.0R, limit close)")
    o.add_argument("--lots", type=float, required=True)
    o.add_argument("--stop-dist", type=float, default=None, help="default |entry-sl|")
    o.add_argument("--r-planned", type=float, default=None, help="default |tp-entry|/stop_dist")
    o.add_argument("--expiry", default="", help="ISO UTC, e.g. 2026-06-12T21:00:00Z")
    o.add_argument("--zone-id", default="", help="link to zone_ledger (default = trade_id)")
    o.add_argument("--date", default="", help="default today UTC")
    o.add_argument("--notes", default="")
    o.add_argument("--force", action="store_true")
    o.set_defaults(func=cmd_order)

    f = sub.add_parser("fill", help="mark an order filled (PENDING → OPEN)")
    f.add_argument("--id", default="", help="trade_id; omit to auto-match a single live row")
    f.add_argument("--instrument", default="")
    f.add_argument("--setup", default="")
    f.add_argument("--fill-px", type=float, default=None, help="actual fill (overrides limit)")
    f.add_argument("--fill-time", default="", help="ISO UTC; default now")
    f.set_defaults(func=cmd_fill)

    c = sub.add_parser("close", help="close an open position")
    c.add_argument("--id", default="")
    c.add_argument("--instrument", default="")
    c.add_argument("--setup", default="")
    c.add_argument("--status", required=True, choices=CLOSE_STATUSES)
    c.add_argument("--exit-px", type=float, default=None)
    c.add_argument("--exit-time", default="")
    c.add_argument("--r-actual", type=float, default=None)
    c.add_argument("--mfe", type=float, default=None, help="max favorable excursion (R)")
    c.add_argument("--mae", type=float, default=None, help="max adverse excursion (R)")
    c.add_argument("--reason", default="")
    c.set_defaults(func=cmd_close)

    x = sub.add_parser("cancel", help="cancel an unfilled order (PENDING → CANCELLED)")
    x.add_argument("--id", default="")
    x.add_argument("--instrument", default="")
    x.add_argument("--setup", default="")
    x.add_argument("--reason", default="")
    x.set_defaults(func=cmd_cancel)

    l = sub.add_parser("list", help="show trade-log rows")
    l.add_argument("--instrument", default="")
    l.add_argument("--status", default="")
    l.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
