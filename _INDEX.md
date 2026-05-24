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

## Scripts
- `scripts/weekly_pull.py` — Twelve Data + FRED data fetch. Output → data/weekly_pull/weekly_pull_{YEAR}_W{WEEK_NUM}.txt
- `scripts/split_timeframes.py` — splits master 1m CSV into M1/M5/M15/M30/H1/H4/D1 files under data/ohlc/xauusd/
- `scripts/backtest.py` — synthetic walk-forward backtest engine. Reads pre-split timeframes from data/ohlc/xauusd/. 1m execution, Monte Carlo mode, full constitution rule enforcement. Output → results/
