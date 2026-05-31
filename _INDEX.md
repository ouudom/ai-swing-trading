# Index — Trading Brain
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md` for protocol details

## System
- `wiki/system/core/constitution.md` — risk rules, TP structure, entry/stop rules
- `wiki/system/xauusd/xauusd_profile.md` — gold macro drivers, sessions, ATR ranges, position sizing
- `wiki/system/xauusd/confluence_criteria.md` — 7-signal scoring rubric, fake confluence rules
- `wiki/system/adding_instruments.md` — end-to-end process for onboarding a new instrument (edge-first, 6 phases)

## Templates
- `wiki/system/templates/weekly_forecast.md` — canonical skeleton for forecasts/weekly/YYYY-WNN.md
- `wiki/system/templates/daily_validation.md` — canonical skeleton for forecasts/daily/YYYY-MM-DD.md

## Macro (Living Pages)
- `wiki/system/core/macro/yield_environment.md` — current Fed posture, real yield trend, DXY structure

## Setups
- `wiki/system/core/setup_library.md` — recurring setup patterns (grows with experience)

## Decisions
- `wiki/system/core/decisions.md` — key system choices with belief log

## Research
- `wiki/research/xauusd/_INDEX.md` — data sources, scripts, standards, pending research
- `wiki/research/eurusd/_INDEX.md` — EURUSD edge-first research index; macro driver = DGS2−ESTR differential (pending Phase-2 confirm)
- `wiki/research/xauusd/concepts/mtf-market-structure.md` — swing trend alignment (HH/HL pivot detection)
- `wiki/research/xauusd/concepts/stop-loss.md` — stop placement: structural vs ATR
- `wiki/research/xauusd/concepts/macro-regime.md` — FRED macro vs gold: DFII10, DXY, VIX
- `wiki/research/xauusd/concepts/atr-compression.md` — volatility cycle detection
- `wiki/research/xauusd/concepts/r-target.md` — TP ratio optimization
- `wiki/research/xauusd/concepts/session-timing.md` — hour-of-day, day-of-week, session effects

## Forecasts

### XAUUSD
- `forecasts/weekly/xauusd/2026-W22.md` — BEARISH/MEDIUM-HIGH (Warsh hawkish, ALIGNED). A sell $4570.38 (8.0/10, SL $4593.46, TP $4501.11 [D1 swing low 2.89R], 0.86 lots). B sell $4707.62 (5.5/10, TP $4607.50 [PP 3.64R], 0.72 lots). C NONE.

### EURUSD
- System = SAME architecture as XAUUSD (weekly forecast → daily validation → outward-offset limit, fundamental+news+technical confluence). EUR-specific signals/weights/pip-thresholds in `wiki/system/eurusd/{confluence_criteria,constitution_addendum,profile,macro_drivers}.md`.
- Adaptations: G6 Asia→London/pre-NY range; H4 trading filter $1→5pips; T3 2.5%→1.2%; fundamental=US-EU rate diff (context, not lone gate per research); offset coef 0.25 (kept — live edge).
- PENDING: command-level pip-scaling (/weekly /validate are gold-$-hardcoded) before EUR runs end-to-end.

## Data Pulls

### XAUUSD
- `data/weekly_pull/xauusd/weekly_pull_2026_W22.txt` — W22 pull (Twelve Data 1 call ok; COT/GLD failed)

### EURUSD
*(none yet)*

## Daily Validations

### XAUUSD
- `forecasts/daily/xauusd/2026-05-26.md` — Setup A ORDER LIMIT SELL $4590.24 / SL $4615.64 / TP $4501.11 / 0.78 lots / 3.51R, val 10.0/10, H1 bearish engulfing (EXPIRED UNFILLED 21:00 UTC)
- `forecasts/daily/xauusd/2026-05-27.md` — Setup B WATCH val 10.0/10, zone $4690–$4720 unreachable (spot $4505.42)
- `forecasts/daily/xauusd/2026-05-28.md` — Setup B NO TRADE (V3 hard block PCE+GDP 12:30 UTC; zone ~$300 above spot $4387.96)

### EURUSD
*(none yet)*

## Scripts
- `scripts/weekly_pull.py` — Pipeline orchestrator. Cache gate (skip if <15min OR market closed) → fetch → compute. Output → data/weekly_pull/weekly_pull_{YEAR}_W{WEEK_NUM}.txt. Hosts all pipeline library functions.
- `scripts/fetch.py` — Network only: TD 15M (1 API call) + FRED → CSVs. Honors cache. Use to refresh data without rebuilding snapshot.
- `scripts/compute.py` — Indicators + snapshot rebuild from existing CSVs. No TD/FRED network (aux VP/COT/GLD only). Use when formulas change.
- `scripts/backtest/` — walk-forward backtest engine (cli.py, engine.py, strategies.py, data.py). Reads from data/ohlc/xauusd/. Run via `python -m scripts.backtest`. Output → results/. Includes `s_weekly_swing_v1` (live formula).
- `scripts/check_v1b.py` — V1b intraday H4 invalidation checker. Reads `_HOT.md` zones, last 2 H4 closes. Run at each H4 boundary.
- `scripts/log_trade.py` — append fills/exits to `data/trades_log.csv`. Subcommands: `fill`, `exit`.
- `scripts/structure.py` — shared fractal pivots / MTF structure / structural_dist (live + backtest parity).
- `scripts/sweep_structure.py`, `sweep_entry.py`, `diag_funnel.py` — XAUUSD Phase-0 method research.
- `scripts/research_eurusd.py`, `research_eurusd_session.py` — EURUSD edge research (macro null, session edge).
- `scripts/ingest_histdata_eur.py` — HistData M1 → UTC merge with TD → `data/research/eurusd/`.
- `scripts/backtest_eur_session.py` — EURUSD overlap mean-reversion backtest (OOS split, cost sweep).

## Trades
- `data/trades_log.csv` — schema: date,week,setup,direction,entry,sl,tp,lots,stop_dist,r_planned,fill_time,exit_time,exit_px,exit_reason,r_actual,mfe,mae,notes
- `data/gld_holdings.csv` — daily GLD ETF tonnage snapshot (auto-appended by weekly_pull)
- `data/yahoo/DXY.csv` — ICE DXY daily (DX-Y.NYB via yfinance)
- `data/cftc/deahistfo{year}.zip` — CFTC COT yearly cache (24h refresh)
