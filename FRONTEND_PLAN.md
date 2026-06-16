# Frontend + Storage Plan

Status: planning. No code yet. Read-only visual layer over the markdown trading brain.

## Principle
- **Claude Code stays the only author.** Writes markdown (forecasts) + SQLite (trade/zone state). Pipeline unchanged at the CLI level.
- **Frontend is read-only.** Shows numbers + charts, never raw markdown. Only short summary/note text columns surface as text.
- **Two stores, clear roles:**
  - **Markdown** = source of truth for forecasts/prose (git-tracked, human-diff, Claude authors).
  - **SQLite (`data/index.db`)** = canonical for the 3 state registries (trades, zone ledger, zone outcomes) after Phase 0, + derived display index parsed from markdown for the frontend. Auto-mirrored to git-tracked CSV on every write (diff/backup safety preserved).

---

## Phase 0 — CSV → SQLite migration (do FIRST, before any frontend)

**Rule: tabular (CSV) → `data/index.db`. Prose/config stay files.** Sequenced by blast radius: 0a state registries (isolated), then 0b market data (touches fetch pipeline).

### Stays a file (NOT migrated — not tabular)
- `weekly_pull/*.txt` — immutable prose dumps Claude reads as text (CLAUDE.md: IMMUTABLE).
- `*.json` config — `cb_calendar_*.json`, `intervention_watch.json`. Git-tracked config.
- `*.zip` — cftc archives.

---

### Phase 0a — state registries

Move the **3 state registries** into `data/index.db`.

| Migrate | Writer | Readers |
|---------|--------|---------|
| `trades_log.csv` | `scripts/trade_log.py` | validate, weekly, calibration.py |
| `zone_ledger.csv` | `scripts/zone_ledger.py` | zone_outcomes.py |
| `zone_outcomes.csv` | `scripts/zone_outcomes.py` | calibration.py |

### Why migration is low-risk
Each registry already routes all I/O through a thin DataFrame load/save pair:
- `trade_log.py` → `load()` / `save()`
- `zone_ledger.py` → `load_ledger()` / `save_ledger()`
- `zone_outcomes.py` → `pd.read_csv`/`to_csv` on OUTCOMES + ledger
Swap those internals from `pd.read_csv`/`to_csv` to `pd.read_sql`/`to_sql` against `data/index.db`. **CLI flags, argparse, and every downstream caller stay identical.** DataFrame in / DataFrame out — same shape.

### Canonical + mirror pattern (keeps git diff safety)
SQLite is canonical. On every `save()`, also dump a git-tracked CSV mirror (`data/trades_log.csv` etc.) — read-only, never hand-edited, exists purely for `git diff` + backup. Reverse of today (CSV was canonical). Best of both: SQL queries + versioned human-readable history.

### Steps
1. `scripts/db.py` — shared helper: open `data/index.db`, `df_read(table)`, `df_write(table, df, mirror_csv=path)`. WAL mode, `numeric`/TEXT cols (no float drift on R/SL/price).
2. **One-shot importer** `scripts/migrate_csv_to_db.py` — load existing 3 CSVs → create + populate tables. Idempotent (drop/recreate or upsert by id).
3. Repoint `trade_log.py` load/save → `db.py`. Verify: `order`/`fill`/`close`/`cancel`/`list` all work, mirror CSV matches old.
4. Repoint `zone_ledger.py` load/save → `db.py`.
5. Repoint `zone_outcomes.py` ledger-read + outcomes-write → `db.py`; keep mirror.
6. `calibration.py` read → `db.py` (or read mirror — unchanged).
7. `.gitignore`: `data/index.db` (+ `-wal`/`-shm`). Keep CSV mirrors tracked.
8. Validate end-to-end: dry-run `/validate` + `/log` against DB; diff mirror vs pre-migration CSV → must match.

### Schema (Phase 0 tables — supersede CSV columns 1:1)
```
trade        ← trades_log.csv columns (trade_id PK, instrument, ..., r_actual, notes)
zone_ledger  ← zone_ledger.csv columns (zone_id PK, ...)
zone_outcome ← zone_outcomes.csv columns (zone_id PK, ...)
```
Same column names → parsers/readers need no rename. R/SL/price → SQLite `NUMERIC`/text, not REAL.

---

### Phase 0b — market data (after 0a proven)

Move all tabular market-data CSV into the same `data/index.db`. Bigger blast radius — touches the fetch pipeline. ~60 OHLC files are the bulk.

| Migrate | Layer to repoint | Table |
|---------|------------------|-------|
| `twelvedata/{symbol}/{tf}.csv` (~60) | `scripts/lib/ohlc_store.py` (`upsert`/`last_dt`/`_paths`) | `ohlc(source, symbol, tf, ts, o,h,l,c,v)` |
| per-symbol `_quarantine.csv` | `ohlc_store.quarantine_bad_ticks` | `ohlc_quarantine` |
| per-symbol manifest `*.json` | `ohlc_store.load_manifest`/`_save_manifest` | `ohlc_manifest` |
| `fred/*.csv` (11) | `backfill_fred.py`, `fetch.py` | `macro_series(series_id, ts, value)` |
| `yahoo/`, `commodities/`, `gld_holdings.csv`, `cftc` | `fetch.py` | one table each |
| `news/headlines.csv` | `weekly_pull.fetch_news`, `check_news.py` | `news` |
| `econ_calendar/calendar.csv` | `check_econ_calendar.py` | `econ_calendar` |

**Key:** `ohlc_store.py` is already an abstraction over `data/{source}/{symbol}/{tf}.csv` → this is a **backend swap, not a rewrite**. Index `ohlc` on `(source, symbol, tf, ts)`. Readers in `compute.py`/`structure.py` switch `read_csv(path)` → `db.df_read_ohlc(symbol, tf)`.

**Steps:** repoint `ohlc_store.py` first (covers most files) → backfill importer reads existing CSVs into `ohlc` → verify `compute.py` output unchanged vs pre-migration (diff a weekly pull) → repoint fred/news/econ → drop CSV trees. Provider caches were git-noise; gitignored DB shrinks the repo.

---

### Sandbox note (CLAUDE.md cross-env)
`data/index.db` is a file in the repo → the Linux scheduled-task sandbox reaches it free. No server, no `DATABASE_URL`, no host decision. This is exactly why SQLite over Postgres for unattended `/validate`+`/weekly`.

---

## Architecture
```
Claude Code → markdown + CSV (source of truth, git)
                 │
   scripts/index_db.py   parse → extract display fields + recompute R/SL
                 │
            data/index.db   SQLite, rebuildable cache
                 │
   scripts/export_json.py → web/public/data/*.json
                 │
            web/   Vite + React + Tailwind, static, read-only
```
No backend. Static JSON. All compute happens in `index_db.py` (reuses `scripts/compute.py`) when the pipeline runs — never in the browser.

### Decisions locked
- Web app: `web/` in this repo. Vite + React + Tailwind. `npm run dev` local.
- R/SL freshness: rebuilt when pipeline runs (`/validate` + `/weekly`). Frontend shows that snapshot. Recomputing R/SL in `index_db.py` from the latest pulled OHLC kills the 06-15 USDCHF stale-R bug at the source — R is read off the bar low, not a cached `_HOT` number.

## Storage schema (SQLite — display fields only)
Text columns are short summaries/notes only. Everything else numeric/enum. Full markdown never enters the DB.
```
instrument(id, name, character, bias, conviction, macro_note[short])
zone(id, instrument, week, kind, status, price_lo, price_hi,
     r1_score, conviction, direction, summary[~140 char])
validation(id, zone_id, date, r2_score, verdict, note[short])
trade(id, instrument, side, entry, sl, tp1, tp2, status, lots,
      r_current, r_realized, sl_status, opened, closed)
ohlc(symbol, tf, ts, o, h, l, c, v)            # for charts (later phase)
calibration(slice, instrument, direction, session, n, win_rate, avg_r, verdict)
zone_outcome(zone_id, would_be_r, hit)
macro(date, summary[short], key fields)
```

### Source map
| Table | Source | Notes |
|-------|--------|-------|
| trade | `trade` table (native, post Phase 0) | recompute `r_current`/`sl_status` from latest OHLC via `compute.py` |
| zone | `forecasts/weekly/{instrument}/*` frontmatter | YAML → direct |
| validation | `forecasts/daily/{instrument}/*` frontmatter | YAML → direct |
| calibration | `data/zone_outcomes.csv` (rebuild direct, cleaner than parsing `calibration.md`) | |
| zone_outcome | `data/zone_outcomes.csv` | |
| ohlc | `data/{source}/{symbol}` | charts phase |
| macro | `yield_environment.md` frontmatter + summary line | |

Frontmatter is already YAML → parsing is trivial. If a display field is missing, tighten the template schema (`wiki/system/templates/*`) rather than scrape prose.

## Phases

### Phase 1 — Dashboard + positions (build first)
Backend:
1. `scripts/index_db.py` — parse `trades_log.csv` + weekly frontmatter → SQLite. Recompute live R/SL from latest pulled OHLC.
2. `scripts/export_json.py` — dump dashboard + positions JSON to `web/public/data/`.
3. Wire both into end of `/validate` + `/weekly` (one line each via `pyrun.sh`); manual run: `bash scripts/pyrun.sh scripts/index_db.py`.

Frontend (`web/`):
- **10-instrument grid** — tile per instrument: bias arrow, conviction color, zone status chips (PENDING / ORDER LIMIT / NO TRADE), spot-vs-zone distance bar.
- **Positions panel** — table from `trade`: side, entry, live R (color), SL status, TP1/TP2/BE flags, lots. Cumulative R footer.
- **Macro banner** — one-line summary, top.

### Phase 2 — Forecast + zone viewer
- Zone cards with confluence score breakdown (R1 / R2 sub-scores).
- Per-instrument timeline: weekly forecast → daily validation chain.

### Phase 3 — Charts
- Price + zones overlaid (D1/H4/1H) via TradingView lightweight-charts.
- ATR bands, SL/TP lines, entry anchor markers. OHLC from `ohlc` table.

### Phase 4 — Calibration + ledger
- `calibration` → sortable table + heatmap (WORKING / DEAD / UNPROVEN by instrument/direction/session).
- Scatter: confluence score vs realized R (does score predict edge?).
- Shadow ledger: would-be R (`zone_outcome`) vs real R (`trade`).
- Cumulative R equity curve.

### Phase 5 — Calendar strip
- CB dates + econ releases + JPY intervention watch from existing JSON gates. Color by instrument impact.

## Build order
Phase 1 → 2 → 3 → 4 → 5. Each phase: extend `index_db.py` parse + `export_json.py` + one frontend view. Static all the way; add a thin FastAPI backend only if on-demand recompute between scheduled runs is ever needed.

## Files to add
```
scripts/index_db.py          # markdown/CSV → SQLite
scripts/export_json.py       # SQLite → web/public/data/*.json
data/index.db                # gitignore — rebuildable
web/                         # Vite + React + Tailwind, static
```
Add `data/index.db` and `web/node_modules/` to `.gitignore`.
