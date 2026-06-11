"""
Resample stored Twelve Data OHLC to higher timeframes.

Input:  data/twelvedata/{symbol}/{src_tf}.csv
Output: data/twelvedata/{symbol}/{dst_tf}.csv  (+ manifest entry)

Usage:
  bash scripts/pyrun.sh scripts/resample_twelvedata.py --src 15min --dst 1h
  bash scripts/pyrun.sh scripts/resample_twelvedata.py --src 15min --dst 4h
  bash scripts/pyrun.sh scripts/resample_twelvedata.py --src 1h    --dst 1day
"""
import os
import sys
import argparse
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.ohlc_store import upsert

SOURCE = "twelvedata"

TF_RULE = {
    "1h":    "1h",
    "4h":    "4h",
    "1day":  "1D",
    "1week": "1W",
}


def resample(symbol: str, src_tf: str, dst_tf: str):
    sym_clean = symbol.replace("/", "").lower()
    src_path = os.path.join("data", SOURCE, sym_clean, f"{src_tf}.csv")
    if not os.path.exists(src_path):
        sys.exit(f"missing source: {src_path}")
    if dst_tf not in TF_RULE:
        sys.exit(f"unsupported dst_tf: {dst_tf} (allowed: {list(TF_RULE)})")

    df = pd.read_csv(src_path, parse_dates=["datetime"]).sort_values("datetime")
    df = df.set_index("datetime")
    agg = df.resample(TF_RULE[dst_tf], label="left", closed="left").agg({
        "open":  "first",
        "high":  "max",
        "low":   "min",
        "close": "last",
        "volume": "sum",
    }).dropna(subset=["open", "close"])
    agg = agg.reset_index()
    print(f"  src rows: {len(df):,}   dst rows: {len(agg):,}")
    info = upsert(SOURCE, symbol, dst_tf, agg)
    print(f"  written: data/{SOURCE}/{sym_clean}/{dst_tf}.csv  range={info['first_dt']} → {info['last_dt']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="XAU/USD")
    ap.add_argument("--src", default="15min")
    ap.add_argument("--dst", default="1h")
    args = ap.parse_args()
    resample(args.symbol, args.src, args.dst)
