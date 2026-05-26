# Index — Trading Brain
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md` for protocol details

## System
- `wiki/system/constitution.md` — risk rules, TP structure, entry/stop rules
- `wiki/system/xauusd_profile.md` — gold macro drivers, sessions, ATR ranges, position sizing
- `wiki/system/confluence_criteria.md` — 7-signal scoring rubric, fake confluence rules

## Templates
- `wiki/system/templates/weekly_forecast.md` — canonical skeleton for forecasts/weekly/YYYY-WNN.md
- `wiki/system/templates/daily_validation.md` — canonical skeleton for forecasts/daily/YYYY-MM-DD.md

## Macro (Living Pages)
- `wiki/system/macro/yield_environment.md` — current Fed posture, real yield trend, DXY structure

## Setups
- `wiki/system/setup_library.md` — recurring setup patterns (grows with experience)

## Decisions
- `wiki/system/decisions.md` — key system choices with belief log

## Research
- `wiki/research/xauusd/_INDEX.md` — data sources, scripts, standards, pending research
- `wiki/research/xauusd/concepts/mtf-market-structure.md` — swing trend alignment (HH/HL pivot detection)
- `wiki/research/xauusd/concepts/stop-loss.md` — stop placement: structural vs ATR
- `wiki/research/xauusd/concepts/macro-regime.md` — FRED macro vs gold: DFII10, DXY, VIX
- `wiki/research/xauusd/concepts/atr-compression.md` — volatility cycle detection
- `wiki/research/xauusd/concepts/r-target.md` — TP ratio optimization
- `wiki/research/xauusd/concepts/session-timing.md` — hour-of-day, day-of-week, session effects

## Forecasts
- `forecasts/weekly/2026-W21.md` — BEARISH/MEDIUM (mid-week rewrite). A sell $4690.24 (7.0/10, SL $4722.76, TP $4584, 0.61 lots). B sell $4627.80 (6.25/10, TP $4530). C NONE.
- `forecasts/weekly/2026-W22.md` — BEARISH/MEDIUM-HIGH (Warsh hawkish, ALIGNED). A sell $4570.38 (8.0/10, SL $4593.46, TP $4501.11 [D1 swing low 2.89R], 0.86 lots). B sell $4707.62 (5.5/10, TP $4607.50 [PP 3.64R], 0.72 lots). C NONE.

## Data Pulls
- `data/weekly_pull/weekly_pull_2026_W22.txt` — W22 pull (Twelve Data 1 call ok; COT/GLD failed)

## Scripts
- `scripts/weekly_pull.py` — Pipeline orchestrator. Cache gate (skip if <15min OR market closed) → fetch → compute. Output → data/weekly_pull/weekly_pull_{YEAR}_W{WEEK_NUM}.txt. Hosts all pipeline library functions.
- `scripts/fetch.py` — Network only: TD 15M (1 API call) + FRED → CSVs. Honors cache. Use to refresh data without rebuilding snapshot.
- `scripts/compute.py` — Indicators + snapshot rebuild from existing CSVs. No TD/FRED network (aux VP/COT/GLD only). Use when formulas change.
- `scripts/backtest/` — walk-forward backtest engine (cli.py, engine.py, strategies.py, data.py). Reads from data/ohlc/xauusd/. Run via `python -m scripts.backtest`. Output → results/
