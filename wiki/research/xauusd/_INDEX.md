---
type: research
updated: 2026-05-24
tags: [index, xauusd]
---

# XAUUSD Research Index

## Files

| File | What's in it |
|---|---|
| `concepts/mtf-market-structure.md` | H4+H1 swing structure win rates, pivot detection method |
| `concepts/stop-loss.md` | Structural vs ATR stop: MAE survival rates, recommended formula |
| `concepts/macro-regime.md` | DFII10 slope regime split, DXY correlation, VIX buckets |
| `concepts/atr-compression.md` | 82% expansion probability, directional neutrality, G2 gate rationale |
| `concepts/r-target.md` | 2R/2.5R/3R EV comparison, filter impact on TP% |
| `concepts/session-timing.md` | Session volatility by hour, day-of-week bias |

## Data Sources

| Source | TF | Range | Rows | Notes |
|---|---|---|---|---|
| Twelve Data (UTC) | M15 | 2020-01-24 → now | 156,394 | `data/twelvedata/xauusd/15min.csv` |
| Twelve Data (UTC) | H1 | 2020-01-24 → now | 39,220 | resampled from M15 |
| Twelve Data (UTC) | H4 | 2020-01-24 → now | 10,454 | resampled from M15 |
| Twelve Data (UTC) | D1 | 2020-01-24 → now | 2,021 | resampled from M15 |
| FRED DFII10 | daily | 2003→now | 5,851 | `data/fred/DFII10.csv` |
| FRED DTWEXBGS | daily | 2006→now | 5,107 | DXY proxy |
| FRED VIXCLS | daily | 1990→now | 9,191 | |
| FRED DCOILWTICO | daily | 1986→now | 10,163 | |

**TD history wall**: ~Jan 2020 for intraday (free tier). D1 direct pull depth unconfirmed.
**TD key param**: always include `timezone=UTC` — omitting returns wrong timezone.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/build_edge_report_v2.py` | Main research runner → `frontend/edge_report.html` |
| `scripts/backfill_twelvedata.py` | Pull/update OHLC backward from TD |
| `scripts/resample_twelvedata.py` | M15 → H1/H4/D1 |
| `scripts/backfill_fred.py` | Pull/update FRED macro series |
| `scripts/lib/ohlc_store.py` | OHLC storage: upsert, manifest, UTC normalization |

## Research Standards

- Always report: N, TP%, edge in pp, EV in R, trades/yr
- Random baseline (next-24H up): **~54.1%** (gold secular uptrend 2020–2026)
- Breakeven at 3R: **25.0%** TP hit rate
- Sample every 5th–10th H4 bar for heavy loops — note step
- Test both long AND short for each hypothesis

## Common Pitfalls

- Gold uptrend 2020–2026 biases random baseline to 54% — bear signal findings may be weaker in actual bear regimes
- No volume in TD data (volume=0) — CME GC volume profile requires TradingView manual check
- FRED is weekday-only — forward-fill onto OHLC date index before merging
- Structural pivot detection is mechanical proxy — actual S/R zones need visual confirmation

## Pending Research

- [ ] **CRITICAL — validate the live edge.** 2026-05-28: replaced backtest stub `g1=3.5` (always-pass)
      with real fractal structure gate (`scripts/structure.py`, N=2). `s_weekly_swing_v1` collapsed
      from "22 trades / +$18k" (stub artifact) to **3 trades / −$2419 / 0% win, 2020–2026**. The
      claimed XAUUSD edge was never tested — G1 was hardcoded. Must establish whether an objective
      structure gate has positive expectancy before trusting the system or cloning it to EURUSD.
      Tunable research params: pivot N, H1/H4 lookback window (60-bar H1 → "mixed" 60%+ of weeks),
      whether G1 should require BOTH TFs or weight them.
- [ ] **G5/G6 backtest gap.** Loader has no VIX or Asia-range data → G5 (1.5) + G6 (0.5) weights
      unvalidated (marked provisional in confluence_criteria). Add VIX + intraday-session to loader,
      run with/without comparison.
- [ ] NFP event drift (day before / day of / 3 days after)
- [ ] Trade duration: avg H4 bars to TP vs SL
- [ ] Consecutive loss / drawdown simulation — validate $4000/week cap
- [ ] Structural level proxy: entries at 20-day swing H/L vs random (validates Signal 1 weight 2.5)
- [ ] Macro direction 2×2: falling yields × long vs falling yields × short
- [ ] D1 direct TD pull depth — does it extend before 2020?
