"""
News-store query — pair-filtered headline readout for /weekly Section 2 + Step 2b (D025).

Reads data/news/headlines.csv (free RSS feeds, written by weekly_pull.fetch_news) and prints
recent headlines relevant to an instrument's currency legs / drivers. This is CONTEXT for the
News-Analysis section and the retrospective — not a gate (no exit-1 on empty; news is
supplementary, web search still allowed).

Usage:
    bash scripts/pyrun.sh scripts/check_news.py --instrument usdjpy --days 7
    bash scripts/pyrun.sh scripts/check_news.py --instrument audusd --days 5 --query "iron ore"
    bash scripts/pyrun.sh scripts/check_news.py --instrument eurusd --days 7 --limit 15
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

NEWS_CSV = Path("data/news/headlines.csv")

INSTRUMENTS = ["xauusd", "eurusd", "gbpusd", "eurgbp", "audusd", "nzdusd",
               "usdcad", "usdchf", "usdjpy", "eurjpy", "gbpjpy"]

# Mirrors weekly_pull._NEWS_KEYWORDS; US/Fed terms appended for every USD pair.
PAIR_KW = {
    "xauusd": ["gold", "bullion", "xau", "safe haven", "real yield"],
    "eurusd": ["euro", "ecb", "eurozone", "lagarde"],
    "gbpusd": ["pound", "sterling", "boe", "bank of england", "gilt"],
    "eurgbp": ["euro", "pound", "ecb", "boe"],
    "audusd": ["aussie", "australian dollar", "rba", "iron ore", "china", "copper"],
    "nzdusd": ["kiwi", "new zealand dollar", "rbnz", "dairy", "china"],
    "usdcad": ["loonie", "canadian dollar", "boc", "bank of canada", "oil", "crude", "wti"],
    "usdchf": ["franc", "swiss", "snb"],
    "usdjpy": ["yen", "boj", "bank of japan", "mof", "intervention", "ueda"],
    "eurjpy": ["yen", "euro", "boj", "ecb", "intervention"],
    "gbpjpy": ["yen", "pound", "boj", "boe", "intervention"],
}
US_KW = ["fed", "fomc", "rate", "inflation", "cpi", "powell", "treasury", "dollar"]


def main() -> int:
    ap = argparse.ArgumentParser(description="News-store query (pair-filtered)")
    ap.add_argument("--instrument", required=True, choices=INSTRUMENTS)
    ap.add_argument("--days", type=int, default=7, help="lookback window (default 7)")
    ap.add_argument("--query", help="extra substring filter (case-insensitive)")
    ap.add_argument("--limit", type=int, default=12, help="max headlines (default 12)")
    args = ap.parse_args()

    df = None
    try:
        import db
        df = db.read_table("news")                      # canonical store
    except Exception:
        df = None
    if (df is None or df.empty) and NEWS_CSV.exists():
        df = pd.read_csv(NEWS_CSV, dtype=str).fillna("")
    if df is None or df.empty:
        print(f"(no news store in data/index.db or {NEWS_CSV} — run weekly_pull.py to populate "
              f"from RSS; web-search fallback applies)")
        return 0
    df = df.fillna("")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%d")
    df = df[df["datetime_utc"].str[:10] >= cutoff]

    kws = PAIR_KW[args.instrument] + (US_KW if args.instrument != "eurgbp" else [])
    if args.query:
        kws = [args.query.lower()]
    mask = df["headline"].str.lower().apply(lambda h: any(k in h for k in kws))
    hits = df[mask].sort_values("datetime_utc").tail(args.limit)

    print(f"News — {args.instrument}, last {args.days}d"
          + (f", query '{args.query}'" if args.query else "") + f" ({len(hits)} hits)")
    if hits.empty:
        print("  (none — broaden --days or check the store populated)")
    for _, r in hits.iterrows():
        print(f"  {r['datetime_utc'][:16]} [{r['source']}] {r['headline']}")
        if r["summary"]:
            print(f"      {r['summary'][:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
