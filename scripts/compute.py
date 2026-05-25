"""
Indicator computation + snapshot write — reads existing CSVs, no TD/FRED network.

Use when formulas change but data is current, or when you want to rebuild the snapshot
file without burning Twelve Data credits. Will make minor auxiliary network calls for
Volume Profile (yfinance), COT (CFTC), GLD (SPDR) — all free, no API key required.

Usage:
    .venv/bin/python scripts/compute.py

Reads:
    data/twelvedata/xauusd/{15min,1h,4h,1day}.csv
    data/fred/{DFII10,DGS10,T5YIE,DFF,DTWEXBGS,VIXCLS}.csv
Writes:
    data/weekly_pull/weekly_pull_{YEAR}_W{WW}.txt

Sister scripts:
    fetch.py    — network IO only (TD + FRED → CSVs)
    compute.py  — indicator math + snapshot write (this file)
    weekly_pull.py — orchestrator: fetch then compute
"""

from weekly_pull import build_snapshot


def main():
    path = build_snapshot()
    print(f"✅ Snapshot rebuilt: {path}")


if __name__ == "__main__":
    main()
