# Index — Trading Brain (v2)
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md`

## System — Core
- `wiki/system/core/constitution.md` — risk, SL/TP/offset, zone rules, re-forecast triggers (v2)
- `wiki/system/core/decisions.md` — key system choices belief log
- `wiki/system/core/setup_library.md` — recurring zone patterns (grows with experience)
- `wiki/system/core/macro/yield_environment.md` — current Fed posture, real-yield trend, DXY structure

## System — XAUUSD
- `wiki/system/xauusd/xauusd_profile.md` — gold drivers, sessions, ATR ranges, sizing
- `wiki/system/xauusd/confluence_criteria.md` — Zone Confluence (R1) + Entry Confluence (R2) (v2, PROPOSED weights)

## Templates
- `wiki/system/templates/weekly_forecast.md` — skeleton for forecasts/weekly/xauusd/YYYY-WNN.md (zones)
- `wiki/system/templates/daily_validation.md` — skeleton for forecasts/daily/xauusd/YYYY-MM-DD.md (entry confluence)
- `wiki/system/templates/paper_review.md` — research paper review template

## Research — XAUUSD
- `wiki/research/xauusd/_INDEX.md` — data sources, scripts, standards, pending research
- `wiki/research/xauusd/mtf-market-structure.md` — swing trend alignment (HH/HL pivots)
- `wiki/research/xauusd/stop-loss.md` — stop placement: structural vs ATR
- `wiki/research/xauusd/macro-regime.md` — FRED macro vs gold: DFII10, DXY, VIX
- `wiki/research/xauusd/atr-compression.md` — volatility cycle, expansion probability (82%)
- `wiki/research/xauusd/r-target.md` — TP ratio optimization
- `wiki/research/xauusd/session-timing.md` — hour/day/session effects
- `wiki/research/xauusd/independent-signal-results.md` — Phase 0b: gold = momentum; measured edges
- `wiki/research/xauusd/entry-confirmation.md` — H1 trigger ablation: pin+offset PF 3.38
- `wiki/research/xauusd/phase0b_signal_plan.md` — Phase 0b methodology

## Research — Source Papers
- `wiki/research/source/_INDEX.md` — external paper index

## Forecasts — XAUUSD
- `forecasts/weekly/xauusd/2026-W23.md` — BEARISH/MEDIUM-HIGH; 2 SHORT zones ($4367–$4390, $4450–$4485), conviction HIGH.

## Daily Validations — XAUUSD
- `forecasts/daily/xauusd/2026-06-08.md` — both SHORT zones ORDER LIMIT, EC 6.0/10 (no E0, midpoint). SL $51.08, lots 0.39.

## Scripts — Pipeline
- `scripts/weekly_pull.py` — orchestrator: cache gate → fetch → compute → weekly_pull txt
- `scripts/fetch.py` — network only: TD 15M + FRED → CSVs
- `scripts/compute.py` — indicators + snapshot from CSVs (aux VP/COT/GLD network only)
- `scripts/backfill_twelvedata.py` — one-off util (not in weekly pipeline): pull/update OHLC backward from TD
- `scripts/resample_twelvedata.py` — one-off util (not in weekly pipeline): M15 → H1/H4/D1
- `scripts/backfill_fred.py` — one-off util (not in weekly pipeline): pull/update FRED macro series

## Scripts — Validation
- `scripts/check_v1b.py` — V1b intraday H4 invalidation checker (CLI zone args, no DB)
- `scripts/check_structured_news_event.py` — T4-X structured news event check
- `scripts/structure.py` — shared fractal pivots, MTF structure helpers

## Scripts — Config & Lib
- `scripts/config/xauusd/config.py` — XAUUSD instrument config
- `scripts/lib/ohlc_store.py` — shared OHLC loading/caching utilities

## Data
- `data/trades_log.csv` — manual trade log (plain CSV)
- `data/gld_holdings.csv` — daily GLD ETF tonnage (auto-appended by weekly_pull)
- `data/weekly_pull/xauusd/` — IMMUTABLE weekly pull text files
- `data/twelvedata/xauusd/` — OHLC CSVs (M15 master, resampled H1/H4/D1)
- `data/fred/` — macro series CSVs (DFII10, VIXCLS, DGS10, T5YIE, FEDFUNDS, etc.)
- `data/yahoo/` — ICE DXY daily
- `data/cftc/deahistfo{year}.zip` — COT yearly archives (24h refresh)
- `data/news_events/` — T4-X structured event JSONs
