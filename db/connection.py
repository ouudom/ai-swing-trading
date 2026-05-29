"""SQLite connection management and schema initialization."""

from __future__ import annotations

import sqlite3
from pathlib import Path

_DB_PATH: Path | None = None
_SCHEMA_SQL = Path(__file__).with_name("schema.sql").read_text()


def set_db_path(path: str | Path | None) -> None:
    """Override the default database file path. Pass None to reset."""
    global _DB_PATH
    _DB_PATH = Path(path) if path is not None else None


def get_db_path() -> Path:
    """Return the current database file path."""
    global _DB_PATH
    if _DB_PATH is None:
        # Project root is two levels up from db/
        root = Path(__file__).resolve().parents[1]
        _DB_PATH = root / "data" / "trading.db"
    return _DB_PATH


def get_conn() -> sqlite3.Connection:
    """Return a connection with row_factory=sqlite3.Row."""
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_conn() as conn:
        conn.executescript(_SCHEMA_SQL)
        conn.commit()
