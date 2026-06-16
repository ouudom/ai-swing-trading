# Storage — SQLite migration

Tabular CSV under `data/` is mirrored into **`data/index.db`** (SQLite) for fast queries
+ the frontend. `data/` (incl. `index.db`, `-wal`, `-shm`) is gitignored — the DB is a
**rebuildable cache**, regenerated from the CSVs anytime.

## Rebuild
```
bash scripts/pyrun.sh scripts/csv_to_sqlite.py
```
Idempotent — each table fully reloaded from its CSV(s) (`if_exists="replace"`). Safe to re-run.

## Tables (Phase 0 — imported by `scripts/csv_to_sqlite.py`)

| Table | Source CSV | Notes |
|-------|------------|-------|
| `trade` | `trades_log.csv` | 1:1 columns |
| `zone_ledger` | `zone_ledger.csv` | 1:1 |
| `zone_outcome` | `zone_outcomes.csv` | 1:1 |
| `ohlc` | `twelvedata/{symbol}/{tf}.csv` | +`source,symbol,tf` cols; idx `(symbol,tf,datetime)` |
| `ohlc_quarantine` | `twelvedata/{symbol}/_quarantine.csv` | +`symbol` |
| `macro_series` | `fred/*.csv` | +`series_id` (filename); idx `(series_id,date)` |
| `market_series` | `yahoo/*.csv`, `commodities/*.csv` | +`source,symbol` |
| `gld_holdings` | `gld_holdings.csv` | 1:1 |
| `news` | `news/headlines.csv` | 1:1 |
| `econ_calendar` | `econ_calendar/calendar.csv` | 1:1 |

## NOT imported (not tabular / derived)
- `weekly_pull/*.txt` — immutable prose dumps (Claude reads as text).
- `cftc/*.zip` — raw provider archives.
- `calibration/summary.json`, `*/_manifest.json` — derived output / coverage; recomputed from data
  (e.g. last bar = `SELECT MAX(datetime) FROM ohlc GROUP BY symbol,tf`).

## Writer status (canonical store migration)
- ✅ **Importer** `csv_to_sqlite.py` — `--refresh` (CSV-canonical tables only) or full cold rebuild
  (all tables from CSV). Parity exact. DB ≈ 132 MB. Wired into /weekly + /validate ends (`--refresh`).
- ✅ **State registries DB-direct** (`scripts/db.py`): `trade_log.py`, `zone_ledger.py`,
  `zone_outcomes.py` read/write `data/index.db` as canonical + auto-dump the CSV mirror on every save.
  Cold-start falls back to CSV. Downstream (`calibration.py`) reads the mirror unchanged.
- ✅ **OHLC DB-live** (step 3): `ohlc_store.upsert` syncs each merged slice into the `ohlc` table
  (slice-replace on source+symbol+tf) right after writing the CSV mirror. DB stays fresh every pull —
  no bulk reload. CSV remains the reader-facing mirror (compute.py, check_v1b.py, zone_outcomes.py,
  backtests read it unchanged). DB sync is fail-soft — a DB error prints a warning, never breaks the pull.
- ✅ **All fetches DB-live** (step 4): every `weekly_pull` fetch (`update_fred`, `fetch_dxy`,
  `fetch_commodities_yf`, `fetch_gld_flows`, econ, news) now reads prior state from the DB and
  syncs the fresh slice into `data/index.db` after writing the CSV mirror — fail-soft via `_db_sync`.
  So the DB is fresh *mid-run*, before any reader runs.
- ✅ **All readers repointed to DB** (step 4, DB-first + CSV fallback): `weekly_pull.load_ohlc/
  load_fred_local/load_dxy_local/load_commodity_local` + news block, `ohlc_store.read_csv_utc` &
  `upsert` producer-read (backtests ride this), `zone_outcomes.load_tf`, `check_v1b`, `check_news`,
  `check_econ_calendar`. Verified by `scripts/test_db_parity.py` — DB-read == CSV-read on OHLC, FRED,
  market series (run after a cold rebuild).
- ⏳ **Still CSV-canonical:** only `ohlc_quarantine` (plain log written by
  `ohlc_store.quarantine_bad_ticks`; synced on `--refresh`).
- ✅ **DB-only cutover + deletion DONE (step 5).** All CSV writes removed (fetches sync DB only;
  `ohlc_store.upsert` writes the `ohlc` table, CSV only as an emergency fallback on DB error;
  state registries no longer mirror CSV). All migrated CSVs deleted — verified by a live `xauusd`
  pull (DB fresh through 2026-06-16, CSV stayed stale then removed) + post-deletion reader smoke
  (load_ohlc/fred/dxy/commodity, check_v1b, check_econ_calendar, calibration all return DB data).
  Symbol-casing bug fixed (`db.clean_symbol` — upsert was passing `XAU/USD` vs table `xauusd`).
  **Remaining files under `data/`:** `index.db`, `twelvedata/*/_manifest.json` + `_quarantine.csv`,
  `weekly_pull/*.txt`, `cftc/*.zip`, `calibration/summary.json`, `news_events/*.json`.
- ✅ **Legacy utils converted (DB-only):** `resample_twelvedata.py` (reads 15min from `ohlc`,
  writes via `upsert`), `backfill_twelvedata.py` (forward-gap from `db.last_ohlc_dt`),
  `backfill_fred.py` (→ `macro_series` via `db.sync_slice`). No CSV.
- ✅ **`_manifest.json` removed.** The incremental-fetch bookmark (`last_dt`) is now derived from
  the DB — `db.last_ohlc_dt` (MAX datetime) + `db.last_series_date` (MAX date). `ohlc_store.upsert`
  no longer writes a manifest; `update_fred` reads its bookmark from `macro_series`.
- ✅ **Backup:** `scripts/backup_db.py` — pg_dump-style gzipped SQL dump → `data/backups/
  index_<ts>.sql.gz`, prunes to `--keep` (default 14). Restore: `gunzip -c <dump> | sqlite3 data/index.db`.
  Run after each /weekly (or schedule). `data/backups/` is gitignored — copy off-machine for true DR.

## .gitignore (post-migration)
`data/` is no longer blanket-ignored. Ignored: `data/index.db`(+`-wal`/`-shm`), `data/backups/`.
Tracked: `weekly_pull/*.txt`, `twelvedata/*/_quarantine.csv`, `cftc/*.zip`, `calibration/summary.json`,
`news_events/*.json`. The DB itself is NOT in git — back it up via `backup_db.py` + off-machine copy.

## DB-canonical vs CSV-canonical (`csv_to_sqlite.py`)
- `DB_CANONICAL = {trade, zone_ledger, zone_outcome, ohlc, macro_series, market_series, news,
  econ_calendar, gld_holdings}` — live-written; `--refresh` skips them, only a full cold rebuild
  reloads from CSV. Only `ohlc_quarantine` is reloaded on every `--refresh`.

## db.py helper
`read_table` / `write_table(mirror_csv=…)` — all-string round-trip, auto-indexes, dumps CSV mirror.
`read_ohlc(symbol,tf,source)` / `read_slice(table,where,cols)` — reader helpers (CSV-shaped frames).
`replace_ohlc_slice(...)` / `sync_slice(table,where,df,...)` / `sync_table(table,df)` — DB-live sync.
Parity gate: `scripts/test_db_parity.py`.
