"""
Central-bank decision-date check — mechanical event gate for /weekly + /validate.

Reads scripts/config/cb_calendar_{year}.json (static, rebuilt yearly) and reports every
scheduled central-bank decision inside the lookahead window, with the instruments each
one hard-blocks or flags as caution. Web search supplements this; it never replaces it
(the W24 ECB miss is why this file exists).

Usage:
    bash scripts/pyrun.sh scripts/check_cb_calendar.py                       # today, 7-day window
    bash scripts/pyrun.sh scripts/check_cb_calendar.py --date 2026-06-11
    bash scripts/pyrun.sh scripts/check_cb_calendar.py --days 10
    bash scripts/pyrun.sh scripts/check_cb_calendar.py --instrument eurusd   # filter

Exit codes: 0 = ran (events or not). 1 = calendar file missing/unreadable or query
date beyond a bank's verified_through (calendar can't be trusted for that window).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent / "config"

INSTRUMENTS = ["xauusd", "eurusd", "gbpusd", "eurgbp", "audusd", "nzdusd",
               "usdcad", "usdchf", "usdjpy", "eurjpy", "gbpjpy"]


def load_calendar(year: int) -> dict:
    path = CONFIG_DIR / f"cb_calendar_{year}.json"
    if not path.exists():
        print(f"❌ Missing {path} — build the {year} calendar before trading (see json _comment).")
        sys.exit(1)
    return json.loads(path.read_text())


def main() -> int:
    ap = argparse.ArgumentParser(description="Central-bank decision-date check")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today UTC)")
    ap.add_argument("--days", type=int, default=7, help="lookahead window in days (default 7)")
    ap.add_argument("--instrument", choices=INSTRUMENTS, help="filter to one instrument")
    args = ap.parse_args()

    start = (datetime.strptime(args.date, "%Y-%m-%d").date() if args.date
             else datetime.now(timezone.utc).date())
    end = start + timedelta(days=args.days)

    cal = load_calendar(start.year)
    banks = cal["banks"]

    unverified = []
    hits = []
    for code, bank in banks.items():
        vt = datetime.strptime(bank["verified_through"], "%Y-%m-%d").date()
        if end > vt:
            unverified.append((code, vt))
        for d in bank["dates"]:
            dt = datetime.strptime(d["date"], "%Y-%m-%d").date()
            if start <= dt <= end:
                hits.append((dt, code, bank, d["status"]))

    if args.instrument:
        hits = [h for h in hits if args.instrument in h[2]["hard_block"] + h[2]["caution"]]

    print(f"CB calendar check — window {start} → {end} (UTC)"
          + (f", instrument {args.instrument}" if args.instrument else ""))

    if not hits:
        print("✅ No scheduled central-bank decisions in window.")
    for dt, code, bank, status in sorted(hits):
        est = "  ⚠ ESTIMATED DATE — VERIFY on the bank's official calendar" if status == "estimated" else ""
        days_away = (dt - start).days
        when = "TODAY" if days_away == 0 else f"in {days_away}d"
        print(f"\n🔔 {dt} ({when}) — {bank['name']} [{code}]{est}")
        print(f"   {bank['time_note']}")
        if bank["hard_block"]:
            print(f"   HARD BLOCK: {', '.join(bank['hard_block'])}")
        if bank["caution"]:
            print(f"   caution:    {', '.join(bank['caution'])}")

    if unverified:
        print()
        for code, vt in unverified:
            print(f"❌ {code}: calendar only verified through {vt} — window extends past it. "
                  f"Update cb_calendar_{start.year}.json from the bank's official schedule.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
