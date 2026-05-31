# Trading Brain — Claude Code Operating Manual

## What This Is
Multi-instrument swing trading system. Weekly forecast driven by multi-agent analysis.
Active instruments: XAUUSD (live), EURUSD (scaffold — system TBD)
Timeframes: Weekly → Daily → H4 | Risk: $2000/trade (stop = avg(0.5×D1_ATR14, H4_ATR14_trading, structural_pivot_dist)) | TP: structural anchor (compute R)

## Memory Protocol — Read This Every Session

Context resets each session. Load state from these files in order:

```
1. _HOT.md                          — active forecast, open trades, pending actions
2. _INDEX.md                        — all file locations and current state
3. wiki/system/core/constitution.md      — universal risk rules, entry rules, stop formula
4. Instrument-specific confluence:
   - XAUUSD: wiki/system/xauusd/confluence_criteria.md
   - EURUSD:  wiki/system/eurusd/confluence_criteria.md
```

## Session Start Protocol
1. Read `_HOT.md` — check active forecast and pending actions
2. Read `_INDEX.md` — orient to current file state
3. Read `wiki/system/core/macro/yield_environment.md` — load current macro baseline
4. Never create duplicate pages — update existing ones in place
5. End of session: update `_HOT.md` with what changed and what is pending

## Commands

### /weekly [instrument]
Run the full weekly forecast. Full steps in `.claude/commands/weekly.md`.
Argument: `xauusd` | `eurusd` | `all`. Default: `xauusd`.

Summary: pull data → 5-agent analysis (macro / technical / confluence / scenarios / writer) →
build `WeeklyForecast` schema (`schemas/weekly.py`) → write to SQLite DB (`db/crud.py`) →
render markdown `forecasts/weekly/{instrument}/[YEAR]-W[WW].md` (`render/weekly_md.py`) →
update `wiki/system/core/macro/yield_environment.md` → upsert `ActiveSetup` rows in DB →
update `_HOT.md` (setups PENDING, tagged with instrument) → update `_INDEX.md`.
Agent 4 applies pre-screen gates G1–G3 before building each setup.
Stop formula: `avg(0.5×D1_ATR14, H4_ATR14, structural_pivot_dist)` (arithmetic mean) where H4_ATR14 uses trading-day bars only (range>=$1, drops weekend/holiday flatline). Order limit offset OUTWARD: `(10−score)×0.3×stop_distance`, applied beyond zone extreme (limit ABOVE zone_top for short, BELOW zone_bottom for long).

### /validate [date] [instrument]
Run daily validation (07:30 UTC, before London open). Full steps in `.claude/commands/validate.md`.
Arguments: date (YYYY-MM-DD), instrument (`xauusd` | `eurusd` | `all`). Default: all active instruments.

Summary: for each PENDING setup → hard blocks (V1/V3) → validation score [XAUUSD D017: G1 4.0 + G3 3.5 + G2 1.5 + V2 1.0, max 10.0; G5/G6 = 0-pt veto/info] → H1 trigger.
Output is exactly one of: ✅ ORDER LIMIT (score ≥ floor + H1 trigger) | 👁 WATCH (score ≥ floor, no trigger) | ❌ NO TRADE (score < floor or hard block). floor = 6.5 if ADX 20–25 else 6.0.
Build `DailyValidation` schema (`schemas/daily.py`) → write to SQLite DB (`db/crud.py`) →
render markdown `forecasts/daily/{instrument}/[DATE].md` (`render/daily_md.py`) → update `_HOT.md`.
On ORDER LIMIT: update `ActiveSetup` lifecycle to PLACED in DB.

## Database Architecture (Source of Truth)
Structured data lives in `data/trading.db` (SQLite). Markdown forecasts/validations and `trades_log.csv` are **generated views** from the DB.

**Write path:** Agent/scripts produce structured data → validated by Pydantic schemas (`schemas/`) → written to SQLite (`db/crud.py`) → rendered to markdown/CSV (`render/`).

**Read path:** Agents read markdown files for context. Scripts query the DB directly for structured operations.

Key packages:
- `schemas/` — Pydantic v2 models: `WeeklyForecast`, `DailyValidation`, `Trade`, `ActiveSetup`, `OpenPosition`
- `db/` — SQLite persistence: `init_db()`, CRUD operations
- `render/` — View generation: `render_weekly_forecast()`, `render_daily_validation()`, `export_trades_to_csv()`

**Migration:** Existing markdown/CSV data was imported via `scripts/migrate_to_db.py`. Run once.

## File Rules
- `data/trading.db` — source of truth. Never edit directly; use `db/crud.py`.
- `forecasts/weekly/{instrument}/` — immutable after Monday open. Rendered from DB.
- `forecasts/daily/{instrument}/` — append-style. Rendered from DB.
- `data/weekly_pull/{instrument}/` — IMMUTABLE. Never edit weekly_pull_*.txt.
- `wiki/` — update in place. Never create a parallel page for an existing concept.
- One concept per wiki page. Cross-link with [[filename]] when referencing.
- After creating or significantly updating any file: update _INDEX.md.
- End of every session: update _HOT.md.

## Frontmatter Schema
Every wiki page:
```yaml
---
type: system | macro | setup | decision
updated: YYYY-MM-DD
confidence: high | medium | low
tags: []
related: []
---
```

Every weekly forecast file:
```yaml
---
type: weekly_forecast
week: YYYY-WNN
generated: YYYY-MM-DD
macro_bias: BULLISH | BEARISH | NEUTRAL
macro_confidence: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_setup: A | B | NONE
conviction: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
baseline_dfii10: x.xx
baseline_dxy: xxx.xxx
weekend_gap_pct: x.xxx
cot_mm_net: ±xxxxx
cot_mm_net_chg: ±xxxxx
etf_gld_tonnes: xxxx.xx
etf_gld_wk_chg: ±xx.xx
---
```

Every daily validation file:
```yaml
---
type: daily_validation
date: YYYY-MM-DD
week: YYYY-WNN
active_setup: A | B | C | NONE
# Hard blocks
v1_structure_intact: true | false
v3_news_clear: true | false
# Validation score (max 10.0)
g1_mtf_structure: true | false   # 3.5 pts
g3_dfii10_slope: true | false    # 3.0 pts
g5_vix_regime: true | false      # 1.5 pts
g2_atr_compressed: true | false  # 1.0 pts
v2_macro_drift: true | false     # 0.5 pts
g6_asia_compressed: true | false # 0.5 pts
validation_score: 0.0
vix: 00.00
asia_range: 00.00
# Entry
h1_trigger_present: true | false
weekly_confluence_score: 0.0
stop_distance: 0.00
stop_type: structural | atr_fallback | reused_yesterday_pivot
pivot_price: 0000.00
structural_dist: 0.00
order_limit: PLACED | WATCH | NO_TRADE | INVALIDATED
limit_price: 0000.00
limit_direction: BUY | SELL | N/A
limit_expires: YYYY-MM-DD 21:00 UTC
h4_atr: 00.00
d1_atr: 00.00
d1_atr_compressed: true | false
dfii10_slope: 0.000
dfii10_drift: 0.000
---
```

## Contradiction Protocol
When macro bias conflicts with technical structure:
- Flag explicitly in forecast with > [!warning] Conflict callout
- Lower conviction to MEDIUM regardless of confluence score
- Note in _HOT.md as a pending question

## System Files Reference
- Universal rules + risk: wiki/system/core/constitution.md
- XAUUSD profile + sessions: wiki/system/xauusd/xauusd_profile.md
- XAUUSD confluence + gates: wiki/system/xauusd/confluence_criteria.md
- EURUSD scaffold: wiki/system/eurusd/ (profile, macro_drivers, confluence_criteria, constitution_addendum)
- Instrument configs: instruments/{instrument}/config.py
- System decisions log: wiki/system/core/decisions.md
- Setup pattern library: wiki/system/core/setup_library.md
- Macro environment (current): wiki/system/core/macro/yield_environment.md
- Templates: wiki/system/templates/weekly_forecast.md, daily_validation.md
- Data pipeline: scripts/weekly_pull.py --instrument {name} (orchestrator), scripts/fetch.py, scripts/compute.py

## Wiki Folder Structure

```
wiki/
  system/
    core/                        — universal rules (all instruments)
      constitution.md            — universal risk rules, entry rules, stop formula
      decisions.md               — system design belief log
      setup_library.md           — recurring setup patterns (grows with trades)
      adding_instruments.md      — 6-phase process for onboarding new instruments
      macro/
        yield_environment.md     — current macro snapshot (rewritten weekly by /weekly)
    templates/
      weekly_forecast.md         — canonical weekly forecast structure
      daily_validation.md        — canonical daily validation structure
      paper_review.md            — research paper review template
    xauusd/                      — XAUUSD-specific system docs
      xauusd_profile.md          — instrument profile, sessions, ATR ranges
      confluence_criteria.md     — daily validation gates + 7-signal weekly scoring
    eurusd/                      — EURUSD-specific system docs
      profile.md                 — instrument profile (scaffold)
      macro_drivers.md           — macro drivers + re-forecast trigger concepts (scaffold)
      confluence_criteria.md     — scoring gates (scaffold)
      constitution_addendum.md   — EURUSD-specific overrides (scaffold)

  research/                      — all quantitative research
    general/                     — cross-instrument research
    xauusd/
      _INDEX.md                  — data sources, scripts, standards, pending research
      concepts/
        mtf-market-structure.md  — swing trend alignment (HH/HL pivot detection)
        stop-loss.md             — stop placement: structural vs ATR
        macro-regime.md          — FRED macro vs gold: DFII10, DXY, VIX
        atr-compression.md       — volatility cycle detection, expansion probability
        r-target.md              — TP ratio optimization (2R vs 2.5R vs 3R)
        session-timing.md        — hour-of-day, day-of-week, session effects
        entry-confirmation.md    — H1 trigger ablation: pin vs engulf vs none
    eurusd/
      _INDEX.md                  — EURUSD research index
    source/                      — external research papers (PDFs reviewed as markdown)
      _INDEX.md                  — paper index
```

