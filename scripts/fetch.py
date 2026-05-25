"""
Network-only data fetch — Twelve Data 15M bars + FRED series → CSVs.

Use when you need fresh market data. Does NOT compute indicators or write snapshot file.
Honors cache policy: skip refetch if <15min old OR market closed (Fri 22:00 → Sun 22:00 UTC).

Usage:
    .venv/bin/python scripts/fetch.py           # honors cache
    .venv/bin/python scripts/fetch.py --force   # always refetch full history

After running, indicators are stale. Run `scripts/compute.py` to rebuild snapshot.

Sister scripts:
    fetch.py    — network IO only (this file)
    compute.py  — indicator math + snapshot write, no TD/FRED network
    weekly_pull.py — orchestrator: fetch then compute
"""

import argparse
from weekly_pull import cache_check, fetch_and_update


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--force", action="store_true", help="Re-fetch full history (bypass cache)")
    args = ap.parse_args()

    _, hit = cache_check(force=args.force)
    if hit:
        return
    fetch_and_update(force=args.force)
    print("✅ Fetch complete. CSVs updated. Run scripts/compute.py to rebuild snapshot.")


if __name__ == "__main__":
    main()
