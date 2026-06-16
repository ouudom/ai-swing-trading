"""
Backfill OHLC history from Twelve Data. Walks BACKWARD from now → since.
Resume-safe via manifest earliest_dt. Rate-limit safe (8 req/min).

Storage: data/twelvedata/{symbol_no_slash}/{tf}.csv  +  _manifest.json

Usage:
  bash scripts/pyrun.sh scripts/backfill_twelvedata.py --tf 15min
  bash scripts/pyrun.sh scripts/backfill_twelvedata.py --tf 15min --since 2020-01-01
  bash scripts/pyrun.sh scripts/backfill_twelvedata.py --tf 15min --forward-only
  bash scripts/pyrun.sh scripts/backfill_twelvedata.py --tf 1day --since 2005-01-01 --max-calls 5
"""
import os
import sys
import time
import argparse
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.ohlc_store import upsert, last_dt as _last_dt

load_dotenv()
KEY    = os.getenv("TWELVE_DATA_KEY")
SOURCE = "twelvedata"

PAGE      = 5000
THROTTLE  = 8.0    # seconds between calls (free tier: 8/min)
MAX_CALLS = 500    # global safety brake

# Approximate bars per day per TF (for chunk sizing)
BARS_PER_DAY = {"1min":1440,"5min":288,"15min":96,"30min":48,"1h":24,"4h":6,"1day":1,"1week":0.2}


def fetch_page(symbol: str, interval: str, start: str, end: str) -> pd.DataFrame:
    r = requests.get("https://api.twelvedata.com/time_series", params={
        "symbol":    symbol,
        "interval":  interval,
        "start_date": start,
        "end_date":   end,
        "outputsize": PAGE,
        "order":      "ASC",
        "apikey":     KEY,
        "format":     "JSON",
        "timezone":   "UTC",
    }, timeout=30)
    j = r.json()
    if isinstance(j, dict) and j.get("status") == "error":
        raise RuntimeError(j.get("message", str(j)))
    vals = j.get("values", []) if isinstance(j, dict) else []
    if not vals:
        return pd.DataFrame(columns=["datetime","open","high","low","close","volume"])
    df = pd.DataFrame(vals)
    if "volume" not in df.columns:
        df["volume"] = 0
    return df


def backfill(symbol: str, tf: str, since: str, forward_only: bool, max_calls: int):
    sym_clean = symbol.replace("/", "").lower()
    cur_last = _last_dt(SOURCE, symbol, tf)   # MAX(datetime) from the DB ohlc table
    now = pd.Timestamp(datetime.now(timezone.utc).replace(tzinfo=None))
    since_ts = pd.Timestamp(since)
    calls = 0

    # ── FORWARD-ONLY: fill gap from last_dt → now ─────────────────────────────
    if forward_only:
        if cur_last is None:
            print(f"[{tf}] no bars in DB, run full backfill first"); return
        start = pd.Timestamp(cur_last) - pd.Timedelta(minutes=1)
        end   = now
        print(f"[{tf}] forward-only {start} → {end}")
        while start < end and calls < max_calls:
            try:
                df = fetch_page(symbol, tf, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"))
            except RuntimeError as e:
                # e.g. "No data available" at the future/weekend edge — non-fatal, data already saved.
                print(f"  forward edge: {e} → done"); break
            calls += 1
            if df.empty: break
            info = upsert(SOURCE, symbol, tf, df)
            new_last = pd.Timestamp(info["last_dt"])
            print(f"  call {calls}: +{len(df)} rows  last_dt={new_last}  total={info['rows']}")
            if new_last <= start: break
            start = new_last + pd.Timedelta(seconds=1)
            if start < end: time.sleep(THROTTLE)
        print(f"[{tf}] forward done. calls={calls}")
        return

    # ── BACKWARD WALK: from now back to since ─────────────────────────────────
    # If partial backfill exists, resume from earliest_dt
    if mf.get("first_dt"):
        end = pd.Timestamp(mf["first_dt"]) + pd.Timedelta(seconds=1)
        print(f"[{tf}] resuming backward from manifest first_dt={mf['first_dt']}")
    else:
        end = now
        print(f"[{tf}] fresh backfill backward from {end} → {since_ts}")

    bpd  = BARS_PER_DAY.get(tf, 24)
    chunk_days = max(3, int(PAGE / bpd)) if bpd > 0 else 365
    total_added = 0
    prev_earliest = None   # progress guard — stop when first_dt stops decreasing

    while end > since_ts and calls < max_calls:
        start = max(end - pd.Timedelta(days=chunk_days), since_ts)
        s_str = start.strftime("%Y-%m-%d %H:%M:%S")
        e_str = end.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  call {calls+1:3d}: {s_str} → {e_str}", end="  ", flush=True)
        try:
            df = fetch_page(symbol, tf, s_str, e_str)
        except RuntimeError as e:
            print(f"STOP: {e}"); break
        calls += 1
        if df.empty:
            print("empty → done")
            end = start - pd.Timedelta(seconds=1)
            time.sleep(THROTTLE)
            continue
        info = upsert(SOURCE, symbol, tf, df)
        added = len(df)
        total_added += added
        earliest = pd.Timestamp(info["first_dt"])
        print(f"+{added} rows  first={earliest}  total={info['rows']}")
        # Progress guard: if the store's earliest bar didn't move earlier this call, the page only
        # returned the boundary bar we already have → we've reached the symbol's true history start.
        # Stop (otherwise `end` re-clamps to the same window and the loop spins forever — the EURGBP
        # 2010-edge bug that burned 240+ calls).
        if prev_earliest is not None and earliest >= prev_earliest:
            print(f"  no earlier data than {earliest} (history start reached) → done")
            break
        prev_earliest = earliest
        end = earliest - pd.Timedelta(seconds=1)
        if end > since_ts:
            time.sleep(THROTTLE)

    if calls >= max_calls:
        print(f"[{tf}] ⚠ hit max_calls={max_calls}. Re-run to continue (will resume from manifest).")
    else:
        print(f"[{tf}] done. calls={calls}  added={total_added}")

    # Fill forward gap: last DB bar → now (close any gap if resuming)
    last2 = _last_dt(SOURCE, symbol, tf)
    if last2 is not None:
        gap_start = pd.Timestamp(last2)
        if (now - gap_start).total_seconds() > 900:
            print(f"[{tf}] closing forward gap {gap_start} → {now}")
            backfill(symbol, tf, since, forward_only=True, max_calls=10)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol",       default="XAU/USD")
    ap.add_argument("--tf",           default="15min",
        help="Interval: 1min 5min 15min 30min 1h 4h 1day 1week")
    ap.add_argument("--since",        default="2015-01-01")
    ap.add_argument("--forward-only", action="store_true")
    ap.add_argument("--max-calls",    type=int, default=MAX_CALLS)
    args = ap.parse_args()
    if not KEY:
        sys.exit("TWELVE_DATA_KEY missing in .env")
    backfill(args.symbol, args.tf, args.since, args.forward_only, args.max_calls)
