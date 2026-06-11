"""
Zone ledger — shadow-trade registry for every published Trading Zone.

Every zone from /weekly gets one row here at publish time, whether or not a real
trade ever fires. `zone_outcomes.py` later replays OHLC against these rows to
measure zone hit-rates, confluence-score calibration, and would-be R outcomes.
Without this, confluence scores are never validated against reality.

Ledger: data/zone_ledger.csv (append-style; resolver flips status OPEN→RESOLVED).
zone_id = {instrument}-{week}-{label}, e.g. gbpusd-2026-W24-PRIMARY.

Usage:
    bash scripts/pyrun.sh scripts/zone_ledger.py add \
        --instrument gbpusd --week 2026-W24 --label PRIMARY --direction SHORT \
        --zone-bottom 1.3400 --zone-top 1.3447 --score 8.0 --conviction MEDIUM \
        [--invalidation-level 1.3460] [--tp-anchor 1.32866] [--notes "..."]
    bash scripts/pyrun.sh scripts/zone_ledger.py list [--week 2026-W24] [--status OPEN]

`--invalidation-level` optional: when omitted, the resolver applies the default
rule (D1 close beyond the zone's far edge — top for SHORT, bottom for LONG).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

LEDGER_CSV = Path("data/zone_ledger.csv")

COLUMNS = [
    "zone_id", "instrument", "week", "label", "direction",
    "zone_bottom", "zone_top", "zone_confluence", "conviction",
    "invalidation_level", "tp_anchor", "published_utc", "source_file",
    "status", "notes",
]

LABELS = ["PRIMARY", "SECONDARY", "COUNTER"]


def load_ledger() -> pd.DataFrame:
    if LEDGER_CSV.exists():
        return pd.read_csv(LEDGER_CSV, dtype={"week": str})
    return pd.DataFrame(columns=COLUMNS)


def save_ledger(df: pd.DataFrame):
    LEDGER_CSV.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(LEDGER_CSV) + ".tmp"
    df[COLUMNS].to_csv(tmp, index=False)
    Path(tmp).replace(LEDGER_CSV)


def cmd_add(args):
    if args.zone_bottom >= args.zone_top:
        sys.exit(f"❌ zone_bottom {args.zone_bottom} must be < zone_top {args.zone_top}")
    zone_id = f"{args.instrument}-{args.week}-{args.label}"
    df = load_ledger()
    if (df["zone_id"] == zone_id).any():
        if not args.force:
            sys.exit(f"❌ {zone_id} already in ledger — use --force to overwrite")
        df = df[df["zone_id"] != zone_id]

    row = {
        "zone_id": zone_id,
        "instrument": args.instrument,
        "week": args.week,
        "label": args.label,
        "direction": args.direction,
        "zone_bottom": args.zone_bottom,
        "zone_top": args.zone_top,
        "zone_confluence": args.score,
        "conviction": args.conviction or "",
        "invalidation_level": args.invalidation_level if args.invalidation_level is not None else "",
        "tp_anchor": args.tp_anchor if args.tp_anchor is not None else "",
        "published_utc": args.published or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": args.source_file or f"forecasts/weekly/{args.instrument}/{args.week}.md",
        "status": "OPEN",
        "notes": args.notes or "",
    }
    new = pd.DataFrame([row])
    df = new if df.empty else pd.concat([df, new], ignore_index=True)
    save_ledger(df)
    print(f"✅ ledger += {zone_id}  {args.direction} {args.zone_bottom}–{args.zone_top} "
          f"(R1 {args.score}) → {LEDGER_CSV}")


def cmd_list(args):
    df = load_ledger()
    if df.empty:
        print("ledger empty")
        return
    for col, val in [("instrument", args.instrument), ("week", args.week), ("status", args.status)]:
        if val:
            df = df[df[col] == val]
    if df.empty:
        print("no matching rows")
        return
    cols = ["zone_id", "direction", "zone_bottom", "zone_top", "zone_confluence",
            "conviction", "status"]
    print(df[cols].to_string(index=False))
    print(f"\n{len(df)} rows | status: {df['status'].value_counts().to_dict()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="register a published zone")
    a.add_argument("--instrument", required=True)
    a.add_argument("--week", required=True, help="ISO trade week, e.g. 2026-W24")
    a.add_argument("--label", required=True, choices=LABELS)
    a.add_argument("--direction", required=True, choices=["LONG", "SHORT"])
    a.add_argument("--zone-bottom", type=float, required=True)
    a.add_argument("--zone-top", type=float, required=True)
    a.add_argument("--score", type=float, required=True, help="Zone Confluence R1 (0–10)")
    a.add_argument("--conviction", default="",
                   choices=["", "HIGH", "MEDIUM-HIGH", "MEDIUM", "MEDIUM-LOW", "LOW"])
    a.add_argument("--invalidation-level", type=float, default=None,
                   help="D1-close kill level (default: zone far edge)")
    a.add_argument("--tp-anchor", type=float, default=None)
    a.add_argument("--published", default="", help="ISO UTC timestamp (default: now)")
    a.add_argument("--source-file", default="")
    a.add_argument("--notes", default="")
    a.add_argument("--force", action="store_true", help="overwrite existing zone_id")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="show ledger rows")
    l.add_argument("--instrument", default="")
    l.add_argument("--week", default="")
    l.add_argument("--status", default="", choices=["", "OPEN", "RESOLVED"])
    l.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
