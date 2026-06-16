#!/usr/bin/env python3
"""
test_db_parity.py — assert the repointed loaders return identical data whether they
read from data/index.db or fall back to CSV. Offline gate for the CSV→SQLite reader
migration (step 4). Run after a cold rebuild: csv_to_sqlite.py && this.

Run: bash scripts/pyrun.sh scripts/test_db_parity.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import weekly_pull as wp  # noqa: E402


def _both(fn, *a):
    """Run loader via DB then via CSV-fallback (db forced None); return (db_df, csv_df)."""
    saved = wp.db
    try:
        wp.db = saved
        db_df = fn(*a)
        wp.db = None
        csv_df = fn(*a)
    finally:
        wp.db = saved
    return db_df, csv_df


def _assert_equal(label, a, b):
    a2 = a.reset_index().astype(str).reset_index(drop=True)
    b2 = b.reset_index().astype(str).reset_index(drop=True)
    if a2.equals(b2):
        print(f"  ✓ {label:28s} {len(a):>7d} rows  DB==CSV")
        return True
    print(f"  ✗ {label:28s} MISMATCH  db={len(a)} csv={len(b)}")
    # show first diverging row for debugging
    n = min(len(a2), len(b2))
    for i in range(n):
        if not a2.iloc[i].equals(b2.iloc[i]):
            print(f"      row {i}\n      DB : {a2.iloc[i].to_dict()}\n      CSV: {b2.iloc[i].to_dict()}")
            break
    return False


def main():
    ok = True
    print("OHLC (twelvedata):")
    for sym in ("xauusd", "eurusd"):
        for tf in ("1day", "1h", "4h", "15min"):
            p = wp.TD_DIR.parent / sym / f"{tf}.csv"
            if not p.exists():
                continue
            db_df, csv_df = _both(wp.load_ohlc, p)
            ok &= _assert_equal(f"{sym}/{tf}", db_df, csv_df)

    print("FRED macro series:")
    for sid in ("DGS10", "DFF", "VIXCLS"):
        if (wp.FRED_DIR / f"{sid}.csv").exists():
            db_df, csv_df = _both(wp.load_fred_local, sid)
            ok &= _assert_equal(sid, db_df, csv_df)

    print("Market series:")
    db_df, csv_df = _both(wp.load_dxy_local)
    ok &= _assert_equal("yahoo/DXY", db_df, csv_df)
    db_df, csv_df = _both(wp.load_commodity_local, "copper")
    if db_df is not None and csv_df is not None:
        ok &= _assert_equal("commodities/copper", db_df, csv_df)

    print("\n" + ("ALL PARITY OK" if ok else "PARITY FAILED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
