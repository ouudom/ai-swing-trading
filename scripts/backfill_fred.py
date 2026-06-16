"""
Backfill full FRED series history into the `macro_series` table (data/index.db).

Usage:
  bash scripts/pyrun.sh scripts/backfill_fred.py                       # default series
  bash scripts/pyrun.sh scripts/backfill_fred.py --series DFII10 DGS10
  bash scripts/pyrun.sh scripts/backfill_fred.py --force               # refetch even if present
"""
import os
import sys
import argparse
import requests
import pandas as pd
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

load_dotenv()
KEY = os.getenv("FRED_KEY")

# Must match scripts/config/xauusd/config.py FRED_SERIES (the series the weekly pipeline consumes).
DEFAULT_SERIES = [
    "DFII10",     # 10Y real yield (TIPS)
    "DGS10",      # 10Y nominal
    "T5YIE",      # 5Y breakeven inflation
    "DFF",        # Fed Funds effective
    "VIXCLS",     # VIX
]

def fetch(series_id: str) -> pd.DataFrame:
    r = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={"series_id": series_id, "api_key": KEY, "file_type": "json"},
        timeout=30,
    )
    j = r.json()
    if "error_code" in j:
        raise RuntimeError(f"FRED {series_id}: {j.get('error_message')}")
    obs = j.get("observations", [])
    df = pd.DataFrame(obs)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date").reset_index(drop=True)


def run(series_list, force: bool):
    for s in series_list:
        if not force and db.last_series_date("macro_series", {"series_id": s}):
            print(f"[{s}] already in macro_series — skip. Use --force to refetch.")
            continue
        print(f"[{s}] fetching...")
        df = fetch(s)
        out = df.copy()
        out["date"] = out["date"].dt.strftime("%Y-%m-%d")
        out["series_id"] = s
        db.sync_slice("macro_series", {"series_id": s},
                      out[["series_id", "date", "value"]], index_cols=["series_id", "date"])
        print(f"  rows={len(df)}  range={out['date'].iloc[0]} → {out['date'].iloc[-1]} → macro_series")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", nargs="*", default=DEFAULT_SERIES)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if not KEY:
        sys.exit("FRED_KEY missing in .env")
    run(args.series, args.force)
