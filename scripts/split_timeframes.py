#!/usr/bin/env python3
"""
DEPRECATED — HistData source removed. Use backfill_twelvedata.py + resample_twelvedata.py.

Previously split a local MT4 M1 CSV (data/ohlc/XAUUSD_M1_2018_2026.csv) into multiple TFs.
Source file and output directory (data/ohlc/) no longer exist.
"""
import sys
sys.exit("DEPRECATED. Use: backfill_twelvedata.py + resample_twelvedata.py")

import pandas as pd
from pathlib import Path

SRC = Path("data/ohlc/XAUUSD_M1_2018_2026.csv")
OUT_DIR = Path("data/ohlc/xauusd")
TIMEFRAMES = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1h",
    "H4": "4h",
    "D1": "1D",
}


def resample(df, rule):
    """Resample 1m OHLCV to a higher timeframe."""
    return df.resample(rule).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Split] Loading {SRC} ...")
    df = pd.read_csv(SRC)
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%Y.%m.%d %H:%M")
    df = df.set_index("datetime").sort_index()
    df = df.rename(columns=lambda c: c.lower().strip())

    for label, rule in TIMEFRAMES.items():
        out_path = OUT_DIR / f"XAUUSD_{label}.csv"
        if label == "M1":
            # Just copy with cleaned columns
            out_df = df[["open", "high", "low", "close", "volume"]].copy()
        else:
            out_df = resample(df, rule)

        out_df.to_csv(out_path)
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"  {label:3s} → {out_path} ({len(out_df):,} rows, {size_mb:.1f} MB)")

    print("[Split] Done.")


if __name__ == "__main__":
    main()
