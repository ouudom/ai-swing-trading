"""
Network-only data fetch — Twelve Data 15M bars + FRED series → CSVs.

Use when you need fresh market data. Does NOT compute indicators or write snapshot file.
Honors cache policy: skip refetch if <15min old OR market closed (Fri 22:00 → Sun 22:00 UTC).

Usage:
    bash scripts/pyrun.sh scripts/fetch.py                        # xauusd, honors cache
    bash scripts/pyrun.sh scripts/fetch.py --force                # always refetch full history
    bash scripts/pyrun.sh scripts/fetch.py --instrument xauusd    # explicit instrument

After running, indicators are stale. Run `scripts/compute.py` to rebuild snapshot.

Sister scripts:
    fetch.py    — network IO only (this file)
    compute.py  — indicator math + snapshot write, no TD/FRED network
    weekly_pull.py — orchestrator: fetch then compute
"""

import argparse
from weekly_pull import cache_check, fetch_and_update, load_instrument, REGISTERED_INSTRUMENTS


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--force", action="store_true", help="Re-fetch full history (bypass cache)")
    ap.add_argument("--instrument", default="xauusd",
                    choices=list(REGISTERED_INSTRUMENTS) + ["all"],
                    help="Instrument to fetch (default: xauusd). 'all' runs every registered instrument.")
    args = ap.parse_args()

    to_run = list(REGISTERED_INSTRUMENTS) if args.instrument == "all" else [args.instrument]
    for inst in to_run:
        if len(to_run) > 1:
            print(f"\n{'='*54}\n  {inst.upper()}\n{'='*54}")
        load_instrument(inst)
        _, hit = cache_check(force=args.force)
        if hit:
            continue
        fetch_and_update(force=args.force)
        print(f"✅ Fetch complete for {inst}. Run scripts/compute.py --instrument {inst} to rebuild snapshot.")


if __name__ == "__main__":
    main()
