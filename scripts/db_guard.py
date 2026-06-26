#!/usr/bin/env python3
"""
db_guard.py — durability guard for the canonical SQLite store (data/database/index.db).

The DB is the source of truth (CSVs were migrated in and deleted), so a corrupt image is a
real data-loss event — the 2026-06-26 incident lost the `news` table and crashed every replay.
Run this at the start of /weekly and /validate (mandatory) and ad-hoc:

    bash scripts/pyrun.sh scripts/db_guard.py            # checkpoint -> check -> backup (default)
    bash scripts/pyrun.sh scripts/db_guard.py check      # integrity only (fast quick_check)
    bash scripts/pyrun.sh scripts/db_guard.py backup     # consistent VACUUM INTO snapshot + prune
    bash scripts/pyrun.sh scripts/db_guard.py checkpoint  # truncate the WAL
    bash scripts/pyrun.sh scripts/db_guard.py sweep       # delete orphaned .fuse_hidden* junk

Backups are consistent point-in-time copies via `VACUUM INTO` (not a file cp of a live WAL DB),
gzipped under data/database/backups/, last KEEP kept. Exit code is non-zero on a failed integrity
check so a caller (command preflight) can halt before writing into a corrupt store.
"""
from __future__ import annotations

import gzip
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path("data/database/index.db")
BACKUP_DIR = DB.parent / "backups"
KEEP = 7  # rotating backups retained


def _con(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(path, timeout=30)
    con.execute("PRAGMA busy_timeout=30000")
    return con


def check() -> bool:
    """quick_check (fast structural scan). Returns True iff 'ok'."""
    if not DB.exists():
        print(f"🛑 {DB} does not exist")
        return False
    con = _con(DB)
    try:
        rows = con.execute("PRAGMA quick_check").fetchall()
    finally:
        con.close()
    ok = len(rows) == 1 and rows[0][0] == "ok"
    if ok:
        print(f"✅ integrity ok: {DB} ({DB.stat().st_size // (1024*1024)}MB)")
    else:
        print(f"🛑 integrity FAILED: {DB}")
        for r in rows[:10]:
            print(f"   {r[0]}")
        print("   → recover with:  sqlite3 index.db .recover | sqlite3 index.fixed.db")
    return ok


def sweep_fuse() -> int:
    """Delete orphaned .fuse_hidden* files in the DB dir (Linux/FUSE sandbox artifact).

    On the FUSE-mounted scheduled-task sandbox, replacing index.db while another process
    holds it open renames the old inode to `.fuse_hidden*` instead of unlinking. These never
    get cleaned and accumulated to 7,871 files / 289MB by 2026-06-26. Unlinking is safe even
    if one is still held open (POSIX: name removed now, inode freed on last close)."""
    orphans = list(DB.parent.glob(".fuse_hidden*"))
    n = 0
    for f in orphans:
        try:
            f.unlink()
            n += 1
        except OSError:
            pass  # still held + FUSE refuses; next run gets it
    if n:
        print(f"🧹 swept {n} orphaned .fuse_hidden* files")
    return n


def checkpoint() -> None:
    con = _con(DB)
    try:
        con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        con.commit()
    finally:
        con.close()
    print("✅ WAL checkpointed (truncated)")


def backup() -> Path | None:
    """Consistent snapshot via VACUUM INTO, gzipped; prune to last KEEP."""
    if not DB.exists():
        print(f"🛑 {DB} does not exist — nothing to back up")
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw = BACKUP_DIR / f"index_{ts}.db"
    con = _con(DB)
    try:
        con.execute("VACUUM INTO ?", (str(raw),))
    finally:
        con.close()
    gz = raw.with_suffix(".db.gz")
    with raw.open("rb") as f_in, gzip.open(gz, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    raw.unlink()
    print(f"✅ backup: {gz.name} ({gz.stat().st_size // (1024*1024)}MB)")

    snaps = sorted(BACKUP_DIR.glob("index_*.db.gz"))
    for old in snaps[:-KEEP]:
        old.unlink()
        print(f"   pruned {old.name}")
    return gz


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "check":
        return 0 if check() else 1
    if cmd == "checkpoint":
        checkpoint()
        return 0
    if cmd == "sweep":
        sweep_fuse()
        return 0
    if cmd == "backup":
        return 0 if backup() else 1
    if cmd == "all":
        checkpoint()
        ok = check()
        if not ok:
            print("🛑 skipping backup — DB is corrupt; recover before backing up")
            return 1
        backup()
        sweep_fuse()
        return 0
    print(f"unknown command: {cmd!r} (use: check | checkpoint | backup | all)")
    return 2


if __name__ == "__main__":
    sys.exit(main())
