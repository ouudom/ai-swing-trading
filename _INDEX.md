# Index — Trading Brain (v2)
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md`

## System — Core
- `wiki/system/core/constitution.md` — risk, SL/TP/offset, zone rules, re-forecast triggers (v2)
- `wiki/system/core/decisions.md` — key system choices belief log
- `wiki/system/core/currency_exposure.md` — FX currency-leg netting (Architecture A); per-factor risk cap; B roadmap (D022)
- `wiki/system/core/setup_library.md` — recurring zone patterns (grows with experience)
- `wiki/system/core/macro/yield_environment.md` — current Fed posture, real-yield trend, DXY structure

## System — XAUUSD
- `wiki/system/xauusd/xauusd_profile.md` — gold drivers, sessions, ATR ranges, sizing
- `wiki/system/xauusd/confluence_criteria.md` — Zone Confluence (R1) + Entry Confluence (R2) (v2, PROPOSED weights)

## System — EURUSD / GBPUSD (ACTIVE, mean-reversion — D021)
- `wiki/system/eurusd/eurusd_profile.md` — EUR drivers, ATR regimes, pip econ, sessions, V1b 5pip
- `wiki/system/eurusd/confluence_criteria.md` — EUR R1/R2, H4-centric fade + macro gate (ACTIVE)
- `wiki/system/gbpusd/gbpusd_profile.md` — GBP drivers, ATR regimes, pip econ, sessions, V1b 6pip
- `wiki/system/gbpusd/confluence_criteria.md` — GBP R1/R2, D1-reversal + H1 + macro gate (ACTIVE)

## System — EURGBP (cross, ACTIVE — onboarding complete, no zones yet)
- `wiki/system/eurgbp/eurgbp_profile.md` — cross profile: low-vol ATR, USD sizing (no convert), no VIX-veto, ECB/BoE event blocks
- `wiki/system/eurgbp/confluence_criteria.md` — EURGBP R1/R2 ACTIVE: mean-reversion fade, macro 0.5 tilt, H1 rows validated

## System — AUDUSD (ACTIVE — D024 pair #1, no zones yet)
- `wiki/system/audusd/audusd_profile.md` — AUD profile: H4-centric fade, NO VIX-veto (level inverted), NO DXY block, RBA/AU/China events, V1b 4pip
- `wiki/system/audusd/confluence_criteria.md` — AUDUSD R1/R2 ACTIVE: H4 fade + VIX-level/US2Y regime tilt

## Templates
- `wiki/system/templates/weekly_forecast.md` — skeleton for forecasts/weekly/xauusd/YYYY-WNN.md (zones)
- `wiki/system/templates/daily_validation.md` — skeleton for forecasts/daily/xauusd/YYYY-MM-DD.md (entry confluence)
- `wiki/system/templates/paper_review.md` — research paper review template

## Research — EURUSD / GBPUSD (P3 signal scan)
- `wiki/research/eurusd/signal-results.md` — EUR edges: mean-reverting, H4-centric (+ raw scan)
- `wiki/research/gbpusd/signal-results.md` — GBP edges: mean-reverting, D1+H1 (+ raw scan)

## Research — EURGBP (EG3 go/no-go)
- `wiki/research/eurgbp/signal-results.md` — EURGBP cross: mean-reverting (same as majors), edge clears cost → **GO on D1**; macro placeholder dead (EG2 rebuild)

## Research — AUDUSD (D024 pair #1)
- `wiki/research/audusd/signal-results.md` — AUDUSD: mean-reverting H4-centric → **GO**; 🔑 DXY-jump DEAD, VIX LEVEL inverted (VIX>20→long t=6.14) (+ raw scan)

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

## Forecasts — EURUSD / GBPUSD / EURGBP
- `forecasts/weekly/eurusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT fade zones (1.1618–1.1640, 1.1574–1.1593), conviction MEDIUM.
- `forecasts/weekly/gbpusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT fade zones (1.3400–1.3447, 1.3370–1.3390), conviction MEDIUM.
- `forecasts/weekly/eurgbp/2026-W24.md` — NEUTRAL/range (ADX 13.8); LONG 0.8608–0.8624 (ZC 8.0) + SHORT 0.8664–0.8682 (ZC 7.5), conviction MEDIUM. First eurgbp forecast.

## Forecasts — XAUUSD
- `forecasts/weekly/xauusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT zones ($4367–$4390, $4450–$4485), conviction HIGH. (renamed W23→W24: files now named by trade week, not run week)

## Daily Validations
- `forecasts/daily/{xauusd,eurusd,gbpusd,eurgbp}/2026-06-10.md` — **CPI day, V3 HARD BLOCK** (US May CPI 12:30 UTC). 08:06 UTC London run: ALL 4 instruments, ALL zones = NO TRADE, held PENDING, no orders. XAU spot $4162 EC 6.0 (V3 override); EUR 1.1549 EC 2.0; GBP 1.33836 EC 2.0 (in-zone, bounce faded); EURGBP 0.86296 EC 3.0 (above LONG support, D1 osc not extreme).
- `forecasts/daily/xauusd/2026-06-09.md` — both SHORT zones ORDER LIMIT, EC 6.0/10 (no E0, midpoint). 13:47 UTC NY run: SL $46.45, lots 0.43, limits $4415.66 / $4504.66. VIX fresh.
- `forecasts/daily/xauusd/2026-06-08.md` — both SHORT zones ORDER LIMIT, EC 6.0/10 (no E0, midpoint). SL $51.08, lots 0.39.
- `forecasts/daily/eurusd/2026-06-09.md` — both SHORT zones NO TRADE, EC 2.0/10 (price below resistance, ADX 39.3 trending).
- `forecasts/daily/gbpusd/2026-06-09.md` — both SHORT zones NO TRADE, EC 4.5/10 (price IN primary short zone, H1 RSI 87.3, only E0 missing — near-trigger, watch).
- `forecasts/daily/eurgbp/2026-06-09.md` — first EURGBP validate; both zones NO TRADE (LONG 4.5 / SHORT 3.0, spot mid-range).

## Scripts — Pipeline
- `scripts/backtest_signals.py` — multi-instrument signal edge backtest (P3 runner; extended catalogue)
- `scripts/weekly_pull.py` — orchestrator: cache gate → fetch → compute → weekly_pull txt
- `scripts/fetch.py` — network only: TD 15M + FRED → CSVs
- `scripts/compute.py` — indicators + snapshot from CSVs (aux VP/COT/GLD network only)
- `scripts/backfill_twelvedata.py` — one-off util (not in weekly pipeline): pull/update OHLC backward from TD
- `scripts/resample_twelvedata.py` — one-off util (not in weekly pipeline): M15 → H1/H4/D1
- `scripts/backfill_fred.py` — one-off util (not in weekly pipeline): pull/update FRED macro series

## Scripts — Risk / Portfolio
- `scripts/fx_exposure.py` — FX currency-leg ledger, ADVISORY (D024): all 10 FX instruments / 8 currency legs; flags shared-leg concentration + suggests cleaner trade (highest EC); no caps, no auto-skip. `--selftest` / `--orders` / `--candidate`.

## Scripts — Validation
- `scripts/check_v1b.py` — V1b intraday H4 invalidation checker (CLI zone args, no DB)
- `scripts/check_structured_news_event.py` — T4-X structured news event check
- `scripts/structure.py` — shared fractal pivots, MTF structure helpers

## Scripts — Config & Lib
- `scripts/config/_fx_base.py` — shared FX-major defaults (rate_diff macro, COT on, ETF off, TICK 100000)
- `scripts/config/xauusd/config.py` — XAUUSD instrument config (real_yield macro)
- `scripts/config/eurusd/config.py` — EURUSD config (DGS2 + DFF−ECBDFR, COT 6E, VP 6E=F)
- `scripts/config/gbpusd/config.py` — GBPUSD config (DGS2 + DFF−SONIA, COT 6B, VP 6B=F)
- `scripts/config/eurgbp/config.py` — EURGBP CROSS config (EG1; no USD leg, macro PLACEHOLDER pending EG2, COT off)
- `scripts/config/audusd/config.py` — AUDUSD config (D024 pair #1; no daily RBA series → carry leg off, COT 6A, VP 6A=F)
- `scripts/lib/ohlc_store.py` — shared OHLC loading/caching utilities

## Data
- `data/trades_log.csv` — manual trade log (plain CSV)
- `data/gld_holdings.csv` — daily GLD ETF tonnage (auto-appended by weekly_pull)
- `data/weekly_pull/xauusd/` — IMMUTABLE weekly pull text files (also eurusd/, gbpusd/)
- `data/twelvedata/xauusd/` — OHLC CSVs (M15 master, resampled H1/H4/D1); also eurusd/, gbpusd/, eurgbp/, audusd/ (D1 2010→now, intraday 2020→now)
- `forecasts/{weekly,daily}/{eurusd,gbpusd,eurgbp,audusd}/` — FX forecast output dirs
- `data/fred/` — macro series CSVs (DFII10, VIXCLS, DGS10, T5YIE, FEDFUNDS, etc.)
- `data/yahoo/` — ICE DXY daily
- `data/cftc/deahistfo{year}.zip` — COT yearly archives (24h refresh)
- `data/news_events/` — T4-X structured event JSONs
