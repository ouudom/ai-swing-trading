# _HOT — Session State
*Always current. Updated at end of every session.*

## Open Position
None

## Active Forecast
[2026-W21](forecasts/weekly/2026-W21.md) — BEARISH / MEDIUM macro, ALIGNED MTF, conviction MEDIUM-HIGH (mid-week rewrite).

- **Setup A** [7.0/10]: SELL limit $4690.24 zone $4660–$4700 | SL $4722.76 | TP $4584 (3.27R) | 0.61 lots
- **Setup B** [6.25/10]: SELL limit $4627.80 zone $4606–$4640 | SL $4660.32 | TP $4530 (3.00R) | 0.61 lots
- Setup C: NONE — counter score 4.0 below 7.5 floor (only S1+S3 hit)

`stop_distance = max(structural_pivot_dist, 0.5×H4_ATR14)` (offset base, same as stop). `buffer = 0.10 × stop_distance` per missing weight unit. Tiered 10.0 scale. Offset recomputed every /validate (07:30 UTC) — never frozen from /weekly.

## Week Status
- Week: 2026-W21
- Trades taken: 0/∞ (bounded by $4000 risk cap)
- Risk used: $0 / $4000 cap

## Pending Actions
- Run /validate Fri 2026-05-22 — recompute offsets with that day's risk_unit
- PCE print Thu 2026-05-28 14:30 UTC — hard block, cancel live limits 2hrs prior
- Watch real yield: above 2.25% strengthens BEARISH; below 2.00% softens
- Repair COT + GLD fetch in `scripts/weekly_pull.py` (failed this pull)

## Last Session
2026-05-21 — Removed prior W21 file, regenerated mid-week with refreshed data (price $4520.72, RSI 39.4, ADX 33.1 trending). Tiered 10.0 confluence applied: Setup A $4690.24 (7.0/10, S1+S6+S2+S4+S5), Setup B $4627.80 (6.25/10, S1+S6+S2+S5). Counter NONE (4.0/10). risk_unit held at $32.52 (no widening per constitution). COT/GLD fetch failed — flagged for script repair.

2026-05-21 (late) — Built `scripts/backtest.py`: synthetic walk-forward backtest engine using real 1m OHLC 2018-2026. Auto-generates setups from price structure (swings, EMAs, pivots); randomizes macro bias, validation gates, and confluence signals. Full constitution execution: limit orders, daily validation, H4 ATR recalc, SL/TP tracking on 1m bars, weekly $4k cap, monthly $10k cap, drawdown breaker. Supports `--runs N` Monte Carlo. Tested on 2018-2020 (5-run MC: 100% profit probability, mean Sharpe 2.14, mean max DD 3.7%). Full 8-year single run: 12 trades, 58% WR, 3.16 PF, 1.23 Sharpe, final balance $121,556 from $100k. Trade frequency is low (~1.5/year) — synthetic zones often too far to fill within the week. Tuning knobs exposed in DEFAULTS config block.

2026-05-22 — Added `scripts/split_timeframes.py` + `data/ohlc/xauusd/` folder. Master 1m CSV split into M1/M5/M15/M30/H1/H4/D1 pre-computed files. Updated `backtest.py` to load from split files instead of resampling on-the-fly. Cleaner data architecture, slightly faster loads.

2026-05-22 — Removed weekly ($4k) and monthly ($10k) risk caps from `backtest.py`. Only remaining risk guard: drawdown circuit breaker (5% → $1k/trade) and same-direction stacking prevention.

2026-05-22 — Major speed optimization on `backtest.py` (4-5× faster). Replaced pandas datetime slicing with numpy `searchsorted` + boolean arrays in `ExecutionEngine`. Per-week M1 slicing instead of scanning full 2.8M-row dataframe. Weekend gap check also vectorized. 2-year backtest: ~20s → ~5s. 8-year backtest: ~5.5min → ~1.5min expected.
