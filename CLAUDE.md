# Trading Brain — Claude Code Operating Manual (v2)

## What This Is
Multi-instrument swing trading system — **10 active instruments** (XAUUSD + 9 FX pairs):
**structured rules + AI (Claude) analysis → high-quality entry signal generation.** Weekly
forecast produces **Trading Zones**; daily validation gates entries. Markdown-only — Claude
writes forecasts/validations directly (no DB).

Instruments: xauusd (momentum) | eurusd, gbpusd, eurgbp, audusd, nzdusd, usdcad, usdchf
(mean-reversion variants) | usdjpy (asymmetric carry-drift) | eurjpy, gbpjpy (cross-JPY fades).
Per-instrument character/macro/vetoes: **constitution multi-instrument table** + each pair's
`wiki/system/{instrument}/` profile + confluence_criteria. Never apply gold intuition to FX.

Timeframes: Weekly/Daily (bias) → Daily→H4→1H (top-down) → 1H/15M (entry confirmation)
Risk: $2000/trade. SL = `H4_ATR14` if `0.5×D1_ATR14 < H4_ATR14`, else `avg(0.5×D1_ATR14, H4_ATR14)`.
TP: TP1 2.5R (manual close), TP2 3.0R (limit close), BE at +1.5R. Structural TP anchor (compute R).

## Memory Protocol — Read Every Session
Context resets each session. Load state in order:
```
1. _HOT.md                                       — system status, open trades, pending actions
2. _INDEX.md                                     — file locations and current state
3. wiki/system/core/constitution.md              — risk, SL/TP/offset, zone + re-forecast rules,
                                                   multi-instrument table (TICK/V1b/macro per pair)
4. wiki/system/{instrument}/confluence_criteria.md — Zone (R1) + Entry (R2) Confluence for the
                                                   instrument being worked
5. wiki/system/core/macro/yield_environment.md   — current macro baseline
```

## Session Start Protocol
1. Read `_HOT.md` — status, active zones, pending actions
2. Read `_INDEX.md` — orient to file state
3. Read `yield_environment.md` — macro baseline
4. Never create duplicate pages — update existing in place
5. End of session: update `_HOT.md` with what changed + what is pending

## Commands

### /weekly [instrument]
Full weekly forecast, one instrument per invocation. Steps in `.claude/commands/weekly.md`.
Pull data → **CB calendar check (mandatory, `scripts/check_cb_calendar.py`)** → 5-section analysis
(Fundamental / News / Technical / Positioning & Flows / Top-Down D→H4→1H) → score candidate
**Trading Zones** with Zone Confluence (R1, max 10, floor 5.0) → publish ≤3 zones (≤1 counter) →
write markdown `forecasts/weekly/{instrument}/YYYY-WNN.md` → update `yield_environment.md` →
update `_HOT.md` (zones PENDING) → update `_INDEX.md`.

### /validate [instrument] [date]
Daily validation (07:30 UTC, before London open), one instrument per invocation. Steps in
`.claude/commands/validate.md`. **CB calendar check first (mandatory)**, then 4 questions per
zone: (1) forecast still valid? (V1/V1b/V3 hard blocks) (2) bias flipped? (macro drift vs
baseline) (3) re-forecast? (mid-week trigger tree) (4) order limit? (**Entry Confluence** R2,
max 10, floor 5.0). Output per zone: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
Write markdown `forecasts/daily/{instrument}/YYYY-MM-DD.md` → update `_HOT.md`.
Before ANY FX order limit: run `scripts/fx_exposure.py` netting ledger (advisory, D022/D024).

## Core Formulas (v2)
```
SL:     H4_ATR14 if (0.5×D1_ATR14) < H4_ATR14 else avg(0.5×D1_ATR14, H4_ATR14)
        H4_ATR14 = ATR(14) on trading-day H4 bars only (range >= MIN_BAR_RANGE per pair)
lots:   max(0.01, floor($2000 / (SL × TICK_MULTIPLIER) × 100) / 100)   ← 0.01-lot step
        TICK_MULTIPLIER: 100 (xauusd) | 100000 (FX non-JPY) | 650 STATIC (JPY-quoted, D024)
offset: max( SL/3 , (10 − entry_confluence_score) × 0.2 × SL )   ← OUTWARD beyond anchor
anchor: confirmation candle CLOSE (E0 present) | 50% zone midpoint (no E0)
limit:  long anchor − offset | short anchor + offset
TP:     TP1 2.5R (manual), TP2 3.0R (limit), BE at +1.5R; TP at structural anchor
```
Entry confirmation (E0): 1H engulfing | 1H pin (tail ≥ 2.5× body) | 15M CHoCH over 60-candle
structure — confirmed on candle CLOSE. xauusd: toward zone direction (continuation); FX: reversal
against the approach into the zone. All time math UTC; reports may add local time.

## Running the pipeline (IMPORTANT — cross-environment)
Always invoke Python via the launcher: **`bash scripts/pyrun.sh <script> [args]`**.
Never hardcode `.venv/bin/python` — that venv is macOS-only and is a **dead symlink inside the
Linux scheduled-task sandbox**, which silently breaks unattended `/validate` and `/weekly` runs.
`pyrun.sh` auto-selects: macOS `.venv` locally → system `python3` + persistent `.pydeps` in the
sandbox. If `.pydeps` is missing (fresh sandbox), rebuild once with `bash scripts/pyrun.sh --setup`
(installs from `requirements.txt` — single source of truth for deps).
Keys live in `.env` (`TWELVE_DATA_KEY`, `FRED_KEY`).

## Architecture (markdown-only)
No database. Claude reads markdown for context and writes forecast/validation markdown directly.
Structured data engine = the `scripts/` pipeline producing the weekly pull text file:
- `scripts/weekly_pull.py` (orchestrator) → `scripts/fetch.py` (TD+FRED) + `scripts/compute.py` (indicators)
- `scripts/structure.py`, `scripts/lib/ohlc_store.py` — shared structure/OHLC helpers
- `scripts/check_v1b.py` — V1b intraday invalidation (CLI zone args)
- `scripts/check_cb_calendar.py` — central-bank decision dates (static JSON, mandatory gate)
- `scripts/check_structured_news_event.py` — T4-X validation
- `scripts/fx_exposure.py` — FX currency-leg netting ledger (advisory)
- `scripts/zone_ledger.py` — shadow-trade registry: every published zone → `data/zone_ledger.csv`
  (MANDATORY at /weekly publish, one `add` per zone)
- `scripts/zone_outcomes.py` — replays OHLC vs ledger → would-be R outcomes + confluence
  calibration → `data/zone_outcomes.csv` (run at /weekly for prior week)
- Bad-tick guard: `ohlc_store.upsert()` auto-quarantines provider spikes (wick-clamp or bar-drop,
  logged to `data/{source}/{symbol}/_quarantine.csv`) — never hand-repair ticks again

## File Rules
- `forecasts/weekly/{instrument}/` — immutable after Monday open. Claude writes markdown.
- `forecasts/daily/{instrument}/` — append-style. Claude writes markdown.
- `data/weekly_pull/{instrument}/` — IMMUTABLE. Never edit `weekly_pull_*.txt`.
- `data/trades_log.csv` — plain manual trade log.
- `data/zone_ledger.csv` / `data/zone_outcomes.csv` — shadow ledger; append via `zone_ledger.py`,
  resolve via `zone_outcomes.py` only (no hand edits).
- `wiki/` — update in place. One concept per page. Never create a parallel page. Cross-link `[[filename]]`.
- After creating/updating any file: update `_INDEX.md`. End of every session: update `_HOT.md`.
- `_HOT.md` — **hard cap 120 lines.** Current state + last session only; prune every session.
  History belongs in `forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat.

## Frontmatter Schemas
See `wiki/system/templates/weekly_forecast.md` and `wiki/system/templates/daily_validation.md`
for the canonical frontmatter (zones, Zone/Entry Confluence, SL/TP/offset fields).

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

## Contradiction Protocol
When macro bias conflicts with technical structure:
- Flag explicitly with `> [!warning]` Conflict callout
- Lower conviction to MEDIUM regardless of Zone Confluence score
- Note in `_HOT.md` as a pending question

## System Files Reference
- Risk + rules + multi-instrument table: `wiki/system/core/constitution.md`
- Per-instrument profile + sessions: `wiki/system/{instrument}/{instrument}_profile.md`
- Per-instrument Zone + Entry Confluence: `wiki/system/{instrument}/confluence_criteria.md`
- Instrument configs: `scripts/config/{instrument}/config.py` (+ `_fx_base.py`, `_fx_usd_base.py`)
- CB decision calendar: `scripts/config/cb_calendar_{year}.json` (rebuild every December)
- Decisions log: `wiki/system/core/decisions.md`
- Zone pattern library: `wiki/system/core/setup_library.md`
- Macro (current): `wiki/system/core/macro/yield_environment.md`
- Templates: `wiki/system/templates/weekly_forecast.md`, `daily_validation.md`
- Data pipeline: `scripts/weekly_pull.py --instrument {instrument}` (orchestrator), `fetch.py`, `compute.py`

## Wiki Folder Structure
```
wiki/
  system/
    core/                        — universal rules
      constitution.md            — risk, SL/TP/offset, zone + re-forecast rules, per-pair table
      decisions.md               — system design belief log
      setup_library.md           — recurring zone patterns
      currency_exposure.md       — FX currency-leg netting (advisory)
      macro/yield_environment.md — current macro snapshot (rewritten weekly by /weekly)
    templates/
      weekly_forecast.md         — canonical weekly (zones) structure
      daily_validation.md        — canonical daily (entry confluence) structure
      paper_review.md            — research paper review template
    {instrument}/                — one dir per instrument (xauusd, eurusd, ... gbpjpy)
      {instrument}_profile.md    — profile, sessions, ATR ranges, events, V1b
      confluence_criteria.md     — Zone Confluence (R1) + Entry Confluence (R2)
  research/
    {instrument}/                — quantitative research + signal-scan results per pair
    source/                      — external research papers (markdown)
```
