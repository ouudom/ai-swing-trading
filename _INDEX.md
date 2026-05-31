# Index — Trading Brain
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md` for protocol details

## System — Core (all instruments)
- `wiki/system/core/constitution.md` — risk rules, TP structure, entry/stop rules
- `wiki/system/core/decisions.md` — key system choices with belief log
- `wiki/system/core/setup_library.md` — recurring setup patterns (grows with experience)
- `wiki/system/core/adding_instruments.md` — 6-phase edge-first onboarding process
- `wiki/system/core/macro/yield_environment.md` — current Fed posture, real yield trend, DXY structure

## System — XAUUSD
- `wiki/system/xauusd/xauusd_profile.md` — gold macro drivers, sessions, ATR ranges, position sizing
- `wiki/system/xauusd/confluence_criteria.md` — 7-signal scoring rubric, gates, weights (D018)

## System — EURUSD
- `wiki/system/eurusd/profile.md` — instrument profile (scaffold)
- `wiki/system/eurusd/macro_drivers.md` — macro drivers + re-forecast trigger concepts (scaffold)
- `wiki/system/eurusd/confluence_criteria.md` — mean-reversion scoring gates (scaffold, calibrated E5)
- `wiki/system/eurusd/constitution_addendum.md` — EURUSD-specific overrides (scaffold)

## Templates
- `wiki/system/templates/weekly_forecast.md` — canonical skeleton for forecasts/weekly/YYYY-WNN.md
- `wiki/system/templates/daily_validation.md` — canonical skeleton for forecasts/daily/YYYY-MM-DD.md
- `wiki/system/templates/paper_review.md` — research paper review template

## Research — XAUUSD
- `wiki/research/xauusd/_INDEX.md` — data sources, scripts, standards, pending research
- `wiki/research/xauusd/mtf-market-structure.md` — swing trend alignment (HH/HL pivot detection)
- `wiki/research/xauusd/stop-loss.md` — stop placement: structural vs ATR
- `wiki/research/xauusd/macro-regime.md` — FRED macro vs gold: DFII10, DXY, VIX
- `wiki/research/xauusd/atr-compression.md` — volatility cycle detection, expansion probability
- `wiki/research/xauusd/r-target.md` — TP ratio optimization (2R vs 2.5R vs 3R)
- `wiki/research/xauusd/session-timing.md` — hour-of-day, day-of-week, session effects
- `wiki/research/xauusd/independent-signal-results.md` — Phase 0b: 50+ signals × 3 TFs. Gold = momentum.
- `wiki/research/xauusd/entry-confirmation.md` — H1 trigger ablation: pin+offset PF 3.38, trigger-only = loser
- `wiki/research/xauusd/phase0b_signal_plan.md` — Phase 0b methodology plan

## Research — EURUSD
- `wiki/research/eurusd/_INDEX.md` — EURUSD edge research index; EUR = mean-reverting

## Research — Source Papers
- `wiki/research/source/_INDEX.md` — external paper index

## Forecasts

### XAUUSD
- `forecasts/weekly/xauusd/2026-W22.md` — BEARISH/MEDIUM-HIGH. Both setups expired unfilled. W23 pending.

### EURUSD
*(none yet)*

## Daily Validations

### XAUUSD
- `forecasts/daily/xauusd/2026-05-25.md` — W22 setup init, stale data run
- `forecasts/daily/xauusd/2026-05-26.md` — Setup A ORDER LIMIT SELL $4590.24 (EXPIRED UNFILLED 21:00 UTC)
- `forecasts/daily/xauusd/2026-05-27.md` — Setup B WATCH 10.0/10, zone unreachable
- `forecasts/daily/xauusd/2026-05-28.md` — Setup B NO TRADE (V3 hard block PCE+GDP; zone ~$300 above spot)
- `forecasts/daily/xauusd/2026-05-29.md` — Setup B NO TRADE (score 4.5/10 < 6.0 floor; zone unreachable; W22 ends)

### EURUSD
*(none yet)*

## Scripts — Pipeline
- `scripts/weekly_pull.py` — orchestrator: cache gate → fetch → compute → weekly_pull txt
- `scripts/fetch.py` — network only: TD 15M + FRED → CSVs
- `scripts/compute.py` — indicators + snapshot from CSVs (no network except aux VP/COT/GLD)
- `scripts/backfill_twelvedata.py` — pull/update OHLC backward from TD
- `scripts/resample_twelvedata.py` — M15 → H1/H4/D1
- `scripts/backfill_fred.py` — pull/update FRED macro series

## Scripts — Validation & Trading
- `scripts/check_v1b.py` — V1b intraday H4 invalidation checker
- `scripts/check_structured_news_event.py` — T4-X structured news event check
- `scripts/log_trade.py` — append fills/exits to trades_log; subcommands: fill, exit
- `scripts/structure.py` — shared fractal pivots, MTF structure, structural_dist (live + backtest parity)


## Data
- `data/trading.db` — source of truth: forecasts, validations, trades, active setups, positions
- `data/trades_log.csv` — generated view of trades (from DB via render/)
- `data/gld_holdings.csv` — daily GLD ETF tonnage (auto-appended by weekly_pull)
- `data/weekly_pull/{instrument}/` — IMMUTABLE weekly pull text files
- `data/twelvedata/{instrument}/` — OHLC CSVs (M15 master, resampled H1/H4/D1)
- `data/fred/` — macro series CSVs (DFII10, VIXCLS, DGS2, ECBESTRVOLWGTTRMDMNRT, etc.)
- `data/yahoo/` — ICE DXY, EURUSD daily
- `data/cftc/deahistfo{year}.zip` — COT yearly archives (24h refresh)
