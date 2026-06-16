#!/usr/bin/env python3
"""
csv_to_sqlite.py — one-shot importer: all tabular CSV under data/ → data/index.db

Source of truth stays the CSVs (Claude/pipeline still write them). This builds a
rebuildable SQLite mirror for fast queries + the frontend. Idempotent: each table
is fully rebuilt from its CSVs on every run (if_exists="replace").

Scope (tabular only). NOT imported: weekly_pull/*.txt (prose), cftc/*.zip (archives),
calibration/summary.json + *_manifest.json (derived/coverage — recomputed from data).

Run:
  bash scripts/pyrun.sh scripts/csv_to_sqlite.py            # cold rebuild ALL tables from CSV
  bash scripts/pyrun.sh scripts/csv_to_sqlite.py --refresh  # sync CSV-canonical tables only

`--refresh` is wired into /weekly + /validate ends: it reloads the CSV-canonical tables (market
data + news/econ/gld) but SKIPS the DB-canonical tables (below), which are written live by
db.py-backed scripts and must not be clobbered from their CSV mirrors.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path("data")
DB = DATA / "database" / "index.db"

# Tables written live (canonical = DB) — `--refresh` leaves these untouched; only a full cold
# rebuild reloads them from CSV. trade/zone_* via scripts/db.py; `ohlc` via ohlc_store.upsert.
DB_CANONICAL = {
    "trade", "zone_ledger", "zone_outcome",          # state registries (db.py)
    "ohlc",                                           # ohlc_store.upsert → replace_ohlc_slice
    "macro_series", "market_series",                  # fred / yahoo / commodities (weekly_pull sync)
    "news", "econ_calendar", "gld_holdings",          # singletons (weekly_pull sync)
}
# Only ohlc_quarantine remains CSV-canonical (plain log written by ohlc_store.quarantine_bad_ticks).


def _read(path: Path, **kw) -> pd.DataFrame:
    """Read a CSV as all-string (no dtype churn); empty/missing → empty frame."""
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path, dtype=str, **kw).fillna("")
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def load_state_registries() -> dict[str, pd.DataFrame]:
    """The 3 trade/zone state CSVs → one table each (1:1 columns)."""
    return {
        "trade": _read(DATA / "trades_log.csv"),
        "zone_ledger": _read(DATA / "zone_ledger.csv"),
        "zone_outcome": _read(DATA / "zone_outcomes.csv"),
    }


def load_ohlc_bars() -> pd.DataFrame:
    """twelvedata/{symbol}/{tf}.csv → ohlc (cold rebuild only; live-written by ohlc_store)."""
    bars = []
    for sym_dir in sorted((DATA / "twelvedata").glob("*")):
        if not sym_dir.is_dir():
            continue
        symbol = sym_dir.name
        for tf_csv in sorted(sym_dir.glob("*.csv")):
            if tf_csv.name == "_quarantine.csv":
                continue
            df = _read(tf_csv)
            if df.empty:
                continue
            df.insert(0, "tf", tf_csv.stem)  # 15min / 1h / 4h / 1day
            df.insert(0, "symbol", symbol)
            df.insert(0, "source", "twelvedata")
            bars.append(df)
    return pd.concat(bars, ignore_index=True) if bars else pd.DataFrame()


def load_ohlc_quarantine() -> pd.DataFrame:
    """twelvedata/{symbol}/_quarantine.csv → ohlc_quarantine (small; refreshed every run)."""
    quar = []
    for sym_dir in sorted((DATA / "twelvedata").glob("*")):
        if not sym_dir.is_dir():
            continue
        df = _read(sym_dir / "_quarantine.csv")
        if not df.empty:
            df.insert(0, "symbol", sym_dir.name)
            quar.append(df)
    return pd.concat(quar, ignore_index=True) if quar else pd.DataFrame()


def load_macro_series() -> pd.DataFrame:
    """fred/*.csv (date,value) → macro_series with series_id from filename."""
    frames = []
    for csv in sorted((DATA / "fred").glob("*.csv")):
        df = _read(csv)
        if df.empty:
            continue
        df.insert(0, "series_id", csv.stem)
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_market_series() -> pd.DataFrame:
    """yahoo/* + commodities/* (date,value) → market_series with source+symbol."""
    frames = []
    for source in ("yahoo", "commodities"):
        for csv in sorted((DATA / source).glob("*.csv")):
            df = _read(csv)
            if df.empty:
                continue
            df.insert(0, "symbol", csv.stem)
            df.insert(0, "source", source)
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_singletons() -> dict[str, pd.DataFrame]:
    """One-file datasets that map straight to a table."""
    return {
        "gld_holdings": _read(DATA / "gld_holdings.csv"),
        "news": _read(DATA / "news" / "headlines.csv"),
        "econ_calendar": _read(DATA / "econ_calendar" / "calendar.csv"),
    }


# table -> list of (columns...) to index after load
INDEXES = {
    "ohlc": [("symbol", "tf", "datetime")],
    "ohlc_quarantine": [("symbol", "tf", "datetime")],
    "macro_series": [("series_id", "date")],
    "market_series": [("source", "symbol", "date")],
    "news": [("datetime_utc",)],
    "econ_calendar": [("date",)],
    "trade": [("instrument", "status")],
    "zone_ledger": [("instrument", "week")],
    "zone_outcome": [("instrument", "week")],
}


def write(con: sqlite3.Connection, tables: dict[str, pd.DataFrame], skip: set[str] = frozenset()):
    for name, df in tables.items():
        if name in skip:
            print(f"  keep {name:18s} (DB-canonical — not reloaded)")
            continue
        if df is None or df.empty:
            print(f"  skip {name:18s} (empty)")
            continue
        df.to_sql(name, con, if_exists="replace", index=False)
        for cols in INDEXES.get(name, []):
            idx = f"ix_{name}_{'_'.join(cols)}"
            con.execute(
                f'CREATE INDEX IF NOT EXISTS "{idx}" ON "{name}" ({", ".join(cols)})'
            )
        print(f"  load {name:18s} {len(df):>7d} rows")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true",
                    help="sync CSV-canonical tables only; skip DB-canonical tables")
    args = ap.parse_args()

    if not DATA.exists():
        raise SystemExit("data/ not found — run from repo root")

    skip = DB_CANONICAL if args.refresh else set()
    tables: dict[str, pd.DataFrame] = {}
    if not args.refresh:                       # DB-canonical loaded only on cold rebuild
        tables.update(load_state_registries())
        tables["ohlc"] = load_ohlc_bars()      # ~989k rows; live-written by ohlc_store.upsert
    # CSV-canonical — refreshed every run:
    tables["ohlc_quarantine"] = load_ohlc_quarantine()
    tables["macro_series"] = load_macro_series()
    tables["market_series"] = load_market_series()
    tables.update(load_singletons())

    print(f"→ {DB} ({'refresh' if args.refresh else 'full rebuild'})")
    con = sqlite3.connect(DB)
    try:
        con.execute("PRAGMA journal_mode=WAL")
        write(con, tables, skip=skip)
        con.commit()
    finally:
        con.close()
    print("done.")


if __name__ == "__main__":
    main()
