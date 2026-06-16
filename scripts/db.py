"""
db.py — shared SQLite access for the canonical store (data/database/index.db).

The DB is the source of truth for every tabular dataset; source CSVs were migrated in
and deleted. All values are kept as text (the old all-string CSV convention) — no dtype
churn, exact round-trip. `write_table(..., mirror_csv=)` can still dump a CSV mirror, but
callers no longer pass it (state registries are DB-only).

Used by: trade_log.py, zone_ledger.py, zone_outcomes.py, live_r.py, weekly_pull.py,
ohlc_store.py. Tables are written live by those scripts — there is no CSV import step.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB = Path("data/database/index.db")

# Index set for the state tables — re-applied after every replace.
INDEXES = {
    "trade": [("instrument", "status")],
    "zone_ledger": [("instrument", "week")],
    "zone_outcome": [("instrument", "week")],
}


def _con() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("PRAGMA journal_mode=WAL")
    return con


def _empty(columns) -> pd.DataFrame:
    if columns:
        return pd.DataFrame({c: pd.Series(dtype=str) for c in columns})
    return pd.DataFrame()


def table_exists(con: sqlite3.Connection, table: str) -> bool:
    row = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None


def read_table(table: str, columns=None) -> pd.DataFrame:
    """Read a table as all-string (NULL→''). Missing DB/table → empty frame."""
    if not DB.exists():
        return _empty(columns)
    con = _con()
    try:
        if not table_exists(con, table):
            return _empty(columns)
        df = pd.read_sql_query(f'SELECT * FROM "{table}"', con)
    finally:
        con.close()
    df = df.where(df.notna(), "").astype(str)
    if columns:                       # tolerate older/narrower stored schema
        for c in columns:
            if c not in df.columns:
                df[c] = ""
    return df


def write_table(table: str, df: pd.DataFrame, mirror_csv=None, columns=None):
    """Replace `table` with df, re-apply indexes, then dump the CSV mirror."""
    if columns:
        df = df[columns]
    con = _con()
    try:
        df.to_sql(table, con, if_exists="replace", index=False)
        for cols in INDEXES.get(table, []):
            idx = f"ix_{table}_{'_'.join(cols)}"
            con.execute(
                f'CREATE INDEX IF NOT EXISTS "{idx}" ON "{table}" ({", ".join(cols)})'
            )
        con.commit()
    finally:
        con.close()
    if mirror_csv:
        mirror_csv = Path(mirror_csv)
        mirror_csv.parent.mkdir(parents=True, exist_ok=True)
        tmp = str(mirror_csv) + ".tmp"
        df.to_csv(tmp, index=False)
        Path(tmp).replace(mirror_csv)


OHLC_COLUMNS = ["source", "symbol", "tf", "datetime", "open", "high", "low", "close", "volume"]


# ── reader helpers (return CSV-shaped frames; callers parse dtypes as before) ──

def clean_symbol(symbol: str) -> str:
    """Canonical ohlc-table symbol form: lowercase, no slash (e.g. EUR/USD → eurusd)."""
    return symbol.lower().replace("/", "")


def read_ohlc(symbol: str, tf: str, source: str = "twelvedata") -> pd.DataFrame:
    """Bars for one (source,symbol,tf) as columns datetime,open,high,low,close,volume
    (strings — caller parses). Empty frame if absent → caller can CSV-fallback."""
    symbol = clean_symbol(symbol)
    if not DB.exists():
        return _empty(["datetime", "open", "high", "low", "close", "volume"])
    con = _con()
    try:
        if not table_exists(con, "ohlc"):
            return _empty(["datetime", "open", "high", "low", "close", "volume"])
        df = pd.read_sql_query(
            "SELECT datetime,open,high,low,close,volume FROM ohlc "
            "WHERE source=? AND symbol=? AND tf=? ORDER BY datetime",
            con, params=(source, symbol, tf),
        )
    finally:
        con.close()
    return df


def last_ohlc_dt(symbol: str, tf: str, source: str = "twelvedata"):
    """MAX(datetime) for one ohlc slice as a string, or None. Replaces the _manifest.json bookmark."""
    symbol = clean_symbol(symbol)
    if not DB.exists():
        return None
    con = _con()
    try:
        if not table_exists(con, "ohlc"):
            return None
        row = con.execute(
            "SELECT MAX(datetime) FROM ohlc WHERE source=? AND symbol=? AND tf=?",
            (source, symbol, tf),
        ).fetchone()
    finally:
        con.close()
    return row[0] if row and row[0] else None


def last_series_date(table: str, where: dict):
    """MAX(date) for a macro_series/market_series slice as a string, or None."""
    if not DB.exists():
        return None
    con = _con()
    try:
        if not table_exists(con, table):
            return None
        clause = " AND ".join(f"{k}=?" for k in where)
        row = con.execute(
            f'SELECT MAX(date) FROM "{table}" WHERE {clause}', tuple(where.values())
        ).fetchone()
    finally:
        con.close()
    return row[0] if row and row[0] else None


def read_slice(table: str, where: dict, cols: list[str]) -> pd.DataFrame:
    """Generic slice read: SELECT cols FROM table WHERE <where> ORDER BY cols[0]."""
    blank = _empty(cols)
    if not DB.exists():
        return blank
    con = _con()
    try:
        if not table_exists(con, table):
            return blank
        clause = " AND ".join(f"{k}=?" for k in where)
        df = pd.read_sql_query(
            f'SELECT {",".join(cols)} FROM "{table}" '
            f'{"WHERE " + clause if where else ""} ORDER BY {cols[0]}',
            con, params=tuple(where.values()),
        )
    finally:
        con.close()
    return df


# ── DB-live sync helpers (canonical = DB; CSV mirror written by caller) ────────

def sync_slice(table: str, where: dict, df: pd.DataFrame, index_cols=None):
    """Replace the `where` slice of `table` with df (df already carries the key cols).
    Fail-soft is the CALLER's job. Used for macro_series/market_series per-series sync."""
    out = df.astype(str)
    con = _con()
    try:
        if table_exists(con, table):
            clause = " AND ".join(f"{k}=?" for k in where)
            con.execute(f'DELETE FROM "{table}" WHERE {clause}', tuple(where.values()))
            out.to_sql(table, con, if_exists="append", index=False)
        else:
            out.to_sql(table, con, if_exists="replace", index=False)
        if index_cols:
            idx = f"ix_{table}_{'_'.join(index_cols)}"
            con.execute(f'CREATE INDEX IF NOT EXISTS "{idx}" ON "{table}" ({", ".join(index_cols)})')
        con.commit()
    finally:
        con.close()


def sync_table(table: str, df: pd.DataFrame):
    """Replace a whole single-file table (gld_holdings/news/econ_calendar) from df.
    Fail-soft is the CALLER's job."""
    con = _con()
    try:
        df.astype(str).to_sql(table, con, if_exists="replace", index=False)
        con.commit()
    finally:
        con.close()


def replace_ohlc_slice(source: str, symbol: str, tf: str, bars: pd.DataFrame):
    """Replace the (source,symbol,tf) slice of the `ohlc` table with `bars`.

    `bars` carries datetime+open/high/low/close/volume for one series; source/symbol/tf
    are prepended. Values stored as text (the all-string convention used across the DB,
    so reads round-trip exactly). Called by ohlc_store.upsert.
    """
    symbol = clean_symbol(symbol)
    df = bars.copy()
    df.insert(0, "tf", tf)
    df.insert(0, "symbol", symbol)
    df.insert(0, "source", source)
    df = df[OHLC_COLUMNS].astype(str)
    con = _con()
    try:
        if table_exists(con, "ohlc"):
            con.execute(
                "DELETE FROM ohlc WHERE source=? AND symbol=? AND tf=?",
                (source, symbol, tf),
            )
            df.to_sql("ohlc", con, if_exists="append", index=False)
        else:
            df.to_sql("ohlc", con, if_exists="replace", index=False)
        con.execute(
            "CREATE INDEX IF NOT EXISTS ix_ohlc_symbol_tf_datetime "
            "ON ohlc (symbol, tf, datetime)"
        )
        con.commit()
    finally:
        con.close()
