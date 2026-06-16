#!/usr/bin/env python3
"""
backup_db.py — pg_dump-style logical backup of data/index.db.

Writes a gzipped SQL dump (full schema + INSERTs, via sqlite3.iterdump) to
data/database/backups/index_YYYYMMDD_HHMMSS.sql.gz and prunes to the most recent --keep.
index.db is gitignored + rebuildable, but the source CSVs are gone — this dump is
the portable recovery artifact. Run it after each /weekly (or on a schedule).

Run:     bash scripts/pyrun.sh scripts/backup_db.py [--keep 14]
Restore: gunzip -c data/database/backups/index_<ts>.sql.gz | sqlite3 data/database/index.db
"""
from __future__ import annotations

import argparse
import gzip
import sqlite3
import time
from pathlib import Path

DB = Path("data/database/index.db")
OUT = Path("data/database/backups")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", type=int, default=14, help="retain this many newest dumps (default 14)")
    args = ap.parse_args()

    if not DB.exists():
        raise SystemExit(f"{DB} not found — nothing to back up")
    OUT.mkdir(parents=True, exist_ok=True)

    dest = OUT / f"index_{time.strftime('%Y%m%d_%H%M%S')}.sql.gz"
    con = sqlite3.connect(DB)
    try:
        rows = 0
        with gzip.open(dest, "wt", encoding="utf-8") as f:
            for line in con.iterdump():
                f.write(line + "\n")
                rows += 1
    finally:
        con.close()

    size_mb = dest.stat().st_size / 1e6
    print(f"→ {dest}  ({rows:,} stmts, {size_mb:.1f} MB gz)")

    backups = sorted(OUT.glob("index_*.sql.gz"))
    for old in backups[:-args.keep] if args.keep > 0 else []:
        old.unlink()
        print(f"  pruned {old.name}")


if __name__ == "__main__":
    main()
