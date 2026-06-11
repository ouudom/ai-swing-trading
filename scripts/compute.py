"""
Indicator computation + snapshot write — reads existing CSVs, no TD/FRED network.

Use when formulas change but data is current, or when you want to rebuild the snapshot
file without burning Twelve Data credits. Will make minor auxiliary network calls for
Volume Profile (yfinance), COT (CFTC), ETF flows — all free, no API key required.

Usage:
    bash scripts/pyrun.sh scripts/compute.py                        # xauusd (default)
    bash scripts/pyrun.sh scripts/compute.py --instrument xauusd    # explicit instrument

Reads:
    data/twelvedata/{instrument}/{15min,1h,4h,1day}.csv
    data/fred/{series}.csv
Writes:
    data/weekly_pull/{instrument}/weekly_pull_{YEAR}_W{WW}.txt

Sister scripts:
    fetch.py    — network IO only (TD + FRED → CSVs)
    compute.py  — indicator math + snapshot write (this file)
    weekly_pull.py — orchestrator: fetch then compute
"""

import argparse
from weekly_pull import build_snapshot, load_instrument, REGISTERED_INSTRUMENTS


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--instrument", default="xauusd",
                    choices=list(REGISTERED_INSTRUMENTS) + ["all"],
                    help="Instrument to compute (default: xauusd). 'all' runs every registered instrument.")
    args = ap.parse_args()

    to_run = list(REGISTERED_INSTRUMENTS) if args.instrument == "all" else [args.instrument]
    for inst in to_run:
        if len(to_run) > 1:
            print(f"\n{'='*54}\n  {inst.upper()}\n{'='*54}")
        load_instrument(inst)
        path = build_snapshot()
        print(f"✅ Snapshot rebuilt: {path}")


if __name__ == "__main__":
    main()
