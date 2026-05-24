# Trading Brain — Claude Code Operating Manual

## What This Is
XAUUSD swing trading system. Weekly forecast driven by multi-agent analysis.
Instrument: XAUUSD | Timeframes: Weekly → Daily → H4
Risk: $2000/trade (stop = max(structural pivot dist, 0.5×H4_ATR)) | TP: 3R full close (structural level)

## Memory Protocol — Read This Every Session

Context resets each session. Load state from these files in order:

```
1. _HOT.md                          — active forecast, open trades, pending actions
2. _INDEX.md                        — all file locations and current state
3. wiki/research/findings.md        — ALL backtest/research findings (read before any analysis)
4. wiki/system/constitution.md      — risk rules, entry rules, stop formula
5. wiki/system/confluence_criteria.md — pre-screen gates + scoring
```

**Before starting any research or backtest:** Read `wiki/research/findings.md` first.
Do not re-derive what is already proven. Build on existing findings.

**After completing any research or backtest:** Update `wiki/research/findings.md` with new results.
Never store findings only in chat — context will be lost.

## Session Start Protocol
1. Read `_HOT.md` — check active forecast and pending actions
2. Read `_INDEX.md` — orient to current file state
3. Read `wiki/research/xauusd/findings.md` — load all proven research before doing any analysis
   → Also read `wiki/research/xauusd/_INDEX.md` for data sources + pending work
4. Never create duplicate pages — update existing ones in place
5. End of session: update `_HOT.md` with what changed and what is pending
6. End of session: if any research/backtest done, update `wiki/research/findings.md`

## Commands

### /weekly
Run the full weekly forecast. Full steps in `.claude/commands/weekly.md`.

Summary: pull data → 5-agent analysis (macro / technical / confluence / scenarios / writer) →
save `forecasts/weekly/[YEAR]-W[WW].md` → update `wiki/system/macro/yield_environment.md` →
update `_HOT.md` (setups PENDING) → update `_INDEX.md`.
Agent 4 applies pre-screen gates G1–G3 before building each setup.
Stop formula: `max(structural_pivot_dist, 0.5×H4_ATR14)`.

### /validate [date]
Run daily validation (07:30 UTC, before London open). Full steps in `.claude/commands/validate.md`.

Summary: for each PENDING setup → hard blocks (V1/V3/G4) → validation score (G1 3.5 + G3 3.5 + G2 2.0 + V2 1.0, max 10.0) → H1 trigger.
Output is exactly one of: ✅ ORDER LIMIT (score ≥ 6.0 + H1 trigger) | 👁 WATCH (score ≥ 6.0, no trigger) | ❌ NO TRADE (score < 6.0 or hard block)
Save to `forecasts/daily/[DATE].md`. Update `_HOT.md`.

### /macro
Update wiki/system/macro/yield_environment.md with latest data from weekly_pull.txt.
Do not create a new file — rewrite the existing one in place.

### /status
Print: current week forecast summary, open position (if any),
week risk used, pending actions from _HOT.md.

## File Rules
- forecasts/weekly/: immutable after Monday open. Never edit a prior week.
- forecasts/daily/: append-style. One file per day.
- data/weekly_pull/: IMMUTABLE. Never edit weekly_pull_*.txt.
- wiki/: update in place. Never create a parallel page for an existing concept.
- One concept per wiki page. Cross-link with [[filename]] when referencing.
- After creating or significantly updating any file: update _INDEX.md.
- End of every session: update _HOT.md.
- End of every research session: update wiki/research/findings.md.

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
macro_confidence: HIGH | MEDIUM | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_setup: A | B | NONE
conviction: HIGH | MEDIUM | LOW
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
g4_session: true | false
# Validation score (max 10.0)
g1_mtf_structure: true | false   # 3.5 pts
g3_dfii10_slope: true | false    # 3.5 pts
g2_atr_compressed: true | false  # 2.0 pts
v2_macro_drift: true | false     # 1.0 pts
validation_score: 0.0
# Entry
h1_trigger_present: true | false
weekly_confluence_score: 0.0
stop_distance: 0.00
stop_type: structural | atr_fallback
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
- Rules + risk management: wiki/system/constitution.md
- Gold macro drivers + sessions: wiki/system/xauusd_profile.md
- Confluence scoring + pre-screen gates: wiki/system/confluence_criteria.md
- System decisions log: wiki/system/decisions.md
- Setup pattern library: wiki/system/setup_library.md
- Macro environment (current): wiki/system/macro/yield_environment.md
- Templates: wiki/system/templates/weekly_forecast.md, daily_validation.md
- Data fetch script: scripts/weekly_pull.py (requires API keys)

## Wiki Folder Structure

```
wiki/
  system/                        — core trading rules + reference
    constitution.md              — risk rules, entry rules, stop formula
    confluence_criteria.md       — pre-screen gates (G1–G4) + 7-signal scoring
    xauusd_profile.md            — instrument profile, sessions, ATR ranges
    decisions.md                 — system design belief log
    setup_library.md             — recurring setup patterns (grows with trades)
    macro/
      yield_environment.md       — current macro snapshot (rewritten weekly via /macro)
    templates/
      weekly_forecast.md         — canonical weekly forecast structure
      daily_validation.md        — canonical daily validation structure

  research/                      — all quantitative research
    xauusd/
      _INDEX.md                  — data sources, scripts, standards, pending research
      findings.md                — MASTER: all proven findings, read first every session
      concepts/
        mtf-market-structure.md  — swing trend alignment (HH/HL pivot detection)
        stop-loss.md             — stop placement: structural vs ATR
        macro-regime.md          — FRED macro vs gold: DFII10, DXY, VIX
        atr-compression.md       — volatility cycle detection, expansion probability
        r-target.md              — TP ratio optimization (2R vs 2.5R vs 3R)
        session-timing.md        — hour-of-day, day-of-week, session effects
```

## Research Wiki — findings.md Entry Schema

```markdown
## Finding N — <Name>
- **Date**: YYYY-MM-DD
- **Data**: source, TF, date range, N bars/rows
- **Method**: brief description
- **Result**: quantitative result (table if multiple)
- **Confidence**: high | medium | low
- **Actionable**: what system rule this supports or changes
- **Script**: scripts/[script name]
```
