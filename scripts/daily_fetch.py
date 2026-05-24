"""
Daily data fetch — fetch 15M bars from Twelve Data, resample to H1/H4/D1.
Also updates FRED series CSVs.

Usage:
    .venv/bin/python scripts/daily_fetch.py           # append new bars only
    .venv/bin/python scripts/daily_fetch.py --force   # re-fetch last 800 15M bars

Pipeline:
    TD 15M fetch → append data/twelvedata/xauusd/15min.csv
                 → resample → 1h.csv, 4h.csv, 1day.csv (rebuilt from full 15min)
    FRED fetch   → append data/fred/{DFII10,DGS10,T5YIE,DFF,DTWEXBGS,VIXCLS}.csv

Output: concise status table for Technical Analyst.
"""

import os, sys, json, argparse
import requests, pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from ohlc_store import upsert, load_manifest, last_dt as manifest_last_dt

load_dotenv()

TWELVE_KEY = os.getenv("TWELVE_DATA_KEY")
FRED_KEY   = os.getenv("FRED_KEY")

SYMBOL     = "XAU/USD"
SYM_CLEAN  = "xauusd"
TD_DIR     = Path(f"data/twelvedata/{SYM_CLEAN}")
FRED_DIR   = Path("data/fred")
FRED_MANIFEST = FRED_DIR / "_manifest.json"

FRED_SERIES = ["DFII10", "DGS10", "T5YIE", "DFF", "DTWEXBGS", "VIXCLS"]

TF_RESAMPLE = {
    "1h":   "1h",
    "4h":   "4h",
    "1day": "1D",
}

# ---------------------------------------------------------------------------
# Twelve Data — 15M fetch

def fetch_15m(force=False):
    """Fetch new 15M bars from Twelve Data. Returns DataFrame of new rows only."""
    last = manifest_last_dt("twelvedata", SYMBOL, "15min")
    outputsize = 800 if (force or last is None) else 200

    r = requests.get("https://api.twelvedata.com/time_series", params={
        "symbol":     SYMBOL,
        "interval":   "15min",
        "outputsize": outputsize,
        "timezone":   "UTC",
        "apikey":     TWELVE_KEY,
    }, timeout=20)
    data = r.json()
    if "code" in data:
        raise ValueError(f"TD 15min: {data.get('message', data)}")

    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col])
    df["volume"] = pd.to_numeric(df.get("volume", 0))
    df = df.sort_values("datetime").reset_index(drop=True)

    # filter to new rows only (unless force)
    if not force and last is not None:
        new = df[df["datetime"] > last]
    else:
        new = df

    return new

# ---------------------------------------------------------------------------
# Resample 15min CSV → higher TFs

def resample_all():
    """Read full 15min.csv and resample to H1, H4, D1. Upsert each."""
    src_path = TD_DIR / "15min.csv"
    if not src_path.exists():
        raise FileNotFoundError(f"Missing {src_path}")

    src = pd.read_csv(src_path, parse_dates=["datetime"]).sort_values("datetime")
    src = src.set_index("datetime")

    results = []
    for tf, rule in TF_RESAMPLE.items():
        agg = src.resample(rule, label="left", closed="left").agg({
            "open":   "first",
            "high":   "max",
            "low":    "min",
            "close":  "last",
            "volume": "sum",
        }).dropna(subset=["open", "close"]).reset_index()

        info = upsert("twelvedata", SYMBOL, tf, agg)
        results.append((tf, len(agg), info["last_dt"]))

    return results

# ---------------------------------------------------------------------------
# FRED fetch

def load_fred_manifest():
    if FRED_MANIFEST.exists():
        return json.loads(FRED_MANIFEST.read_text())
    return {}

def save_fred_manifest(data):
    FRED_MANIFEST.write_text(json.dumps(data, indent=2))

def fetch_fred_series(series_id, last_date, force=False):
    if force or not last_date:
        obs_start = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
    else:
        obs_start = last_date

    r = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={
            "series_id":        series_id,
            "observation_start": obs_start,
            "api_key":          FRED_KEY,
            "file_type":        "json",
        },
        timeout=15,
    )
    obs = r.json().get("observations", [])
    df = pd.DataFrame(obs)[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().reset_index(drop=True)

def append_fred_csv(csv_path, new_df):
    if new_df.empty:
        return 0
    if csv_path.exists():
        existing = pd.read_csv(csv_path)
        combined = pd.concat([existing, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["date"], keep="last")
        combined = combined.sort_values("date").reset_index(drop=True)
    else:
        combined = new_df
    combined.to_csv(csv_path, index=False)
    return len(new_df)

def update_fred(force=False):
    manifest = load_fred_manifest()
    results  = []

    for series in FRED_SERIES:
        csv_path  = FRED_DIR / f"{series}.csv"
        last_date = manifest.get(series, {}).get("last_dt")

        try:
            new_rows = fetch_fred_series(series, last_date, force=force)
            # filter to truly new rows
            if not force and last_date:
                new_rows = new_rows[new_rows["date"] > last_date]
            appended = append_fred_csv(csv_path, new_rows)

            if appended > 0:
                updated = pd.read_csv(csv_path)
                manifest[series] = {
                    "first_dt":      str(updated["date"].iloc[0]),
                    "last_dt":       str(updated["date"].iloc[-1]),
                    "last_pull_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "rows":          len(updated),
                }
                save_fred_manifest(manifest)

            results.append((series, appended, manifest.get(series, {}).get("last_dt", "?")))
        except Exception as e:
            results.append((series, f"ERROR: {e}", last_date or "?"))

    return results

# ---------------------------------------------------------------------------
# Summary

def print_summary(m15_new, m15_last, resample_results, fred_results):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"\n{'='*62}")
    print(f"  Daily Fetch — {now}")
    print(f"{'='*62}")

    print(f"\n  Twelve Data (XAU/USD)")
    print(f"  {'Series':<12} {'New rows':>9}  {'Last bar'}")
    print(f"  {'-'*48}")
    print(f"  {'15min':<12} {m15_new:>9}  {m15_last}")
    for tf, rows, last in resample_results:
        print(f"  {tf:<12} {'→'+str(rows):>9}  {last}  (resampled)")

    print(f"\n  FRED")
    print(f"  {'Series':<14} {'New rows':>9}  {'Last obs'}")
    print(f"  {'-'*48}")
    for name, appended, last in fred_results:
        print(f"  {name:<14} {str(appended):>9}  {last}")

    print(f"\n  CSVs ready:")
    print(f"    data/twelvedata/xauusd/  → 15min  1h  4h  1day")
    print(f"    data/fred/               → DFII10  DGS10  VIXCLS ...")
    print(f"{'='*62}\n")

# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true",
                        help="Re-fetch last 800 15M bars and full FRED history (90d)")
    args = parser.parse_args()

    if not TWELVE_KEY or not FRED_KEY:
        print("ERROR: TWELVE_DATA_KEY or FRED_KEY not set. Check .env")
        sys.exit(1)

    # 1. Fetch 15M
    print("Fetching 15M bars from Twelve Data...")
    new_15m = fetch_15m(force=args.force)
    info_15m = upsert("twelvedata", SYMBOL, "15min", new_15m)
    m15_last = info_15m["last_dt"]

    # 2. Resample → H1, H4, D1
    print("Resampling 15min → 1h / 4h / 1day...")
    resample_results = resample_all()

    # 3. FRED
    print("Fetching FRED series...")
    fred_results = update_fred(force=args.force)

    print_summary(len(new_15m), m15_last, resample_results, fred_results)

if __name__ == "__main__":
    main()
