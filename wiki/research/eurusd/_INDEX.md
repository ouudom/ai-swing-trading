---
type: research
updated: 2026-05-28
tags: [index, eurusd]
---

# EURUSD Research Index

Edge-first build. NO live rules until a signal is measured to have edge here (not assumed
from XAUUSD). Thresholds in **pips**, not dollars. See [[constitution]] for universal rules.

## Macro Driver Decision (2026-05-28)

Anchor = **US–EU short-rate differential: DGS2 − ESTR** (daily, independent of EUR price).
- German Bund is monthly-only on FRED → no daily 10y/2y differential feasible free.
- DXY rejected as primary: ~−0.95 corr with EURUSD → price-derived, not independent macro.
- DGS2 carries daily movement (US rate expectations = dominant EURUSD driver); ESTR
  (`ECBESTRVOLWGTTRMDMNRT`, daily) supplies the EU side.
- **Must be confirmed in Phase 2** (differential-slope vs forward EUR return) before weight is locked.
- Sign convention (to verify): rising differential → USD strength → EUR bearish. EUR long wants
  slope < 0; EUR short wants slope > 0 (mirrors XAUUSD G3).

## Planned Concepts (Phase 2 — fill with measured results)

| File | Hypothesis to test |
|---|---|
| `concepts/mtf-market-structure.md` | Does fractal HH/HL gate (scripts/structure.py) predict EUR direction? Win-rate vs random. |
| `concepts/macro-rate-differential.md` | DGS2−ESTR slope vs forward EUR return. Confirm/reject as G3-equivalent. Compare vs DXY slope + US-side-only (DFII10/DGS2). |
| `concepts/atr-compression.md` | EUR ATR compression → expansion probability. Pip thresholds. |
| `concepts/session-timing.md` | London/NY-overlap effect on EUR (NOT Asia — gold's G6 won't transfer). |
| `concepts/stop-loss.md` | Structural vs ATR stop on EUR; pip-scaled stop formula. |
| `concepts/dxy-correlation.md` | EUR–DXY rolling corr (feeds correlation guard USD_BETA_SIGN=-1). |

## Data Sources

| Source | TF | Notes |
|---|---|---|
| Twelve Data EUR/USD (UTC) | M15 | `data/twelvedata/eurusd/15min.csv` (backfill 2020→now) |
| → resampled | H1/H4/D1 | via `scripts/resample_twelvedata.py --symbol EUR/USD` |
| FRED DGS2 | daily | US 2y |
| FRED ECBESTRVOLWGTTRMDMNRT | daily | ESTR euro short-term rate |
| FRED DFII10, DGS10 | daily | US real/nominal 10y (context) |
| FRED DFF, VIXCLS | daily | policy + risk regime |

## Research Standards (inherit from xauusd)

- Report: N, win%, edge in pp, EV in R, trades/yr. Test long AND short.
- Thresholds in pips. EUR random-baseline TBD (compute; gold's 54% does not transfer).
- One TD call/pull (15M resampled locally).

## Pending Research

- [ ] Confirm DGS2−ESTR slope predicts EUR direction (gate Phase 3 on this)
- [ ] EUR ATR ranges by session (pip distributions) for stop + compression thresholds
- [ ] EUR random directional baseline (no secular trend like gold — expect ~50%)
- [ ] COT EURO FX contract name verify (`EURO FX - CHICAGO MERCANTILE EXCHANGE`) before enabling
