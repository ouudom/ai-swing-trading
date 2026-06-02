# Trading Brain — Claude Code Operating Manual (v2)

## What This Is
Single-instrument (XAUUSD) swing trading system: **structured rules + AI (Claude) analysis →
high-quality entry signal generation.** Weekly forecast produces **Trading Zones**; daily
validation gates entries. Markdown-only — Claude writes forecasts/validations directly (no DB).

Timeframes: Weekly/Daily (bias) → Daily→H4→1H (top-down) → 1H/15M (entry confirmation)
Risk: $2000/trade. SL = `H4_ATR14` if `0.5×D1_ATR14 < H4_ATR14`, else `avg(0.5×D1_ATR14, H4_ATR14)`.
TP: TP1 2.5R (manual close), TP2 3.0R (limit close), BE at +1.5R. Structural TP anchor (compute R).

## Memory Protocol — Read Every Session
Context resets each session. Load state in order:
```
1. _HOT.md                                   — system status, open trades, pending actions
2. _INDEX.md                                 — file locations and current state
3. wiki/system/core/constitution.md          — risk, SL/TP/offset, zone + re-forecast rules
4. wiki/system/xauusd/confluence_criteria.md — Zone Confluence (R1) + Entry Confluence (R2)
5. wiki/system/core/macro/yield_environment.md — current macro baseline
```

## Session Start Protocol
1. Read `_HOT.md` — status, active zones, pending actions
2. Read `_INDEX.md` — orient to file state
3. Read `yield_environment.md` — macro baseline
4. Never create duplicate pages — update existing in place
5. End of session: update `_HOT.md` with what changed + what is pending

## Commands

### /weekly
Full weekly forecast. Steps in `.claude/commands/weekly.md`.
Pull data → 5-section analysis (Fundamental / News / Technical / Positioning & Flows / Top-Down
D→H4→1H) → score candidate **Trading Zones** with Zone Confluence (R1, max 10, floor 5.0) → publish
≤3 zones (≤1 counter) → write markdown `forecasts/weekly/xauusd/YYYY-WNN.md` → update
`yield_environment.md` → update `_HOT.md` (zones PENDING) → update `_INDEX.md`.

### /validate [date]
Daily validation (07:30 UTC, before London open). Steps in `.claude/commands/validate.md`.
Answers 4 questions per zone: (1) forecast still valid? (V1/V1b/V3 hard blocks) (2) bias flipped?
(macro drift vs baseline) (3) re-forecast? (mid-week trigger tree) (4) order limit? (**Entry
Confluence** R2, max 10, floor 5.0). Output per zone: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
Write markdown `forecasts/daily/xauusd/YYYY-MM-DD.md` → update `_HOT.md`.

## Core Formulas (v2)
```
SL:     H4_ATR14 if (0.5×D1_ATR14) < H4_ATR14 else avg(0.5×D1_ATR14, H4_ATR14)
        H4_ATR14 = ATR(14) on trading-day H4 bars only (range >= $1 filter)
lots:   floor($2000 / (SL × 100))
offset: max( SL/3 , (10 − entry_confluence_score) × 0.2 × SL )   ← OUTWARD beyond anchor
anchor: confirmation candle CLOSE (E0 present) | 50% zone midpoint (no E0)
limit:  long anchor − offset | short anchor + offset
TP:     TP1 2.5R (manual), TP2 3.0R (limit), BE at +1.5R; TP at structural anchor
```
Entry confirmation (E0): 1H engulfing | 1H pin (tail ≥ 2.5× body) | 15M CHoCH over 60-candle
structure — toward zone direction, confirmed on candle CLOSE.

## Architecture (markdown-only)
No database. Claude reads markdown for context and writes forecast/validation markdown directly.
Structured data engine = the `scripts/` pipeline producing the weekly pull text file:
- `scripts/weekly_pull.py` (orchestrator) → `scripts/fetch.py` (TD+FRED) + `scripts/compute.py` (indicators)
- `scripts/structure.py`, `scripts/lib/ohlc_store.py` — shared structure/OHLC helpers
- `scripts/check_v1b.py` — V1b intraday invalidation (CLI zone args)
- `scripts/check_structured_news_event.py` — T4-X validation

## File Rules
- `forecasts/weekly/xauusd/` — immutable after Monday open. Claude writes markdown.
- `forecasts/daily/xauusd/` — append-style. Claude writes markdown.
- `data/weekly_pull/xauusd/` — IMMUTABLE. Never edit `weekly_pull_*.txt`.
- `data/trades_log.csv` — plain manual trade log.
- `wiki/` — update in place. One concept per page. Never create a parallel page. Cross-link `[[filename]]`.
- After creating/updating any file: update `_INDEX.md`. End of every session: update `_HOT.md`.

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
- Risk + rules: `wiki/system/core/constitution.md`
- XAUUSD profile + sessions: `wiki/system/xauusd/xauusd_profile.md`
- Zone + Entry Confluence: `wiki/system/xauusd/confluence_criteria.md`
- Instrument config: `scripts/config/xauusd/config.py`
- Decisions log: `wiki/system/core/decisions.md`
- Zone pattern library: `wiki/system/core/setup_library.md`
- Macro (current): `wiki/system/core/macro/yield_environment.md`
- Templates: `wiki/system/templates/weekly_forecast.md`, `daily_validation.md`
- Data pipeline: `scripts/weekly_pull.py --instrument xauusd` (orchestrator), `fetch.py`, `compute.py`

## Wiki Folder Structure
```
wiki/
  system/
    core/                        — universal rules
      constitution.md            — risk, SL/TP/offset, zone + re-forecast rules
      decisions.md               — system design belief log
      setup_library.md           — recurring zone patterns
      macro/yield_environment.md — current macro snapshot (rewritten weekly by /weekly)
    templates/
      weekly_forecast.md         — canonical weekly (zones) structure
      daily_validation.md        — canonical daily (entry confluence) structure
      paper_review.md            — research paper review template
    xauusd/
      xauusd_profile.md          — instrument profile, sessions, ATR ranges
      confluence_criteria.md     — Zone Confluence (R1) + Entry Confluence (R2)
  research/
    xauusd/                      — quantitative research (signals, structure, macro, ATR, TP, sessions)
    source/                      — external research papers (markdown)
```
