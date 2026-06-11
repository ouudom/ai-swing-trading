"""
Backfill full FRED series history. One file per series.

Storage: data/fred/{series_id}.csv  +  data/fred/_manifest.json

Usage:
  bash scripts/pyrun.sh scripts/backfill_fred.py                       # default series
  bash scripts/pyrun.sh scripts/backfill_fred.py --series DFII10 DGS10
  bash scripts/pyrun.sh scripts/backfill_fred.py --force               # refetch even if file exists
"""
import os
import sys
import json
import argparse
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

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

OUT_DIR = "data/fred"
MANIFEST = os.path.join(OUT_DIR, "_manifest.json")


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


def load_manifest() -> dict:
    if not os.path.exists(MANIFEST):
        return {}
    with open(MANIFEST) as f:
        return json.load(f)


def save_manifest(m: dict):
    tmp = MANIFEST + ".tmp"
    with open(tmp, "w") as f:
        json.dump(m, f, indent=2, sort_keys=True)
    os.replace(tmp, MANIFEST)


def run(series_list, force: bool):
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = load_manifest()
    for s in series_list:
        path = os.path.join(OUT_DIR, f"{s}.csv")
        if os.path.exists(path) and not force:
            print(f"[{s}] cache hit ({path}) — skip. Use --force to refetch.")
            continue
        print(f"[{s}] fetching...")
        df = fetch(s)
        tmp = path + ".tmp"
        df.to_csv(tmp, index=False)
        os.replace(tmp, path)
        manifest[s] = {
            "first_dt": df["date"].iloc[0].strftime("%Y-%m-%d"),
            "last_dt": df["date"].iloc[-1].strftime("%Y-%m-%d"),
            "rows": int(len(df)),
            "last_pull_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        print(f"  rows={len(df)}  range={manifest[s]['first_dt']} → {manifest[s]['last_dt']}")
    save_manifest(manifest)
    print(f"manifest: {MANIFEST}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", nargs="*", default=DEFAULT_SERIES)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if not KEY:
        sys.exit("FRED_KEY missing in .env")
    run(args.series, args.force)
