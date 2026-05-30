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
| `concepts/independent-signal-results.md` | **Phase 0b** — each signal tested independently D1/H4/H1. Key: gold=momentum not mean-reversion. DFII10 slope confirmed (+5.3pp). RSI>70 anti-fade. EMA regime confirmed. |
| `phase0b_signal_plan.md` | Phase 0b plan doc — signal catalogue, methodology, action thresholds |

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

- [ ] **CRITICAL — live edge UNVALIDATED (Phase 0 done 2026-05-28).** Replaced backtest stub
      `g1=3.5` (always-pass) with real fractal gate (`scripts/structure.py`). Swept pivot_n{2,3} ×
      struct_win{40,60,90,120} × g1_mode{both,h4_only,either} × r_floor 1.8
      (`scripts/sweep_structure.py`). **Result: 0/24 configs reach N>=30 trades.** Best by PnL:
      pivot_n2/either = +$11.8k but only **11 trades in 6 yr** (PF 3.58); pivot_n2/both = 3 trades
      −$2.2k. Trade frequency is structurally ~1.5–2.5/yr — too low to validate ANY edge.
      Findings: (a) struct_win irrelevant (last-2-pivots stable across windows); (b) bottleneck is
      the SERIAL entry funnel (weekly-bias → zone → in-session → pin-trigger≤8bars → outward-offset
      fill → R≥1.8), not G1 alone — each stage halves the sample. **Decision needed:** redesign the
      entry funnel for usable frequency (drop/relax pin-trigger, allow touch-fills, multiple
      setups/wk) OR accept rare-trade regime + validate over longer history. DO NOT clone to EURUSD
      until the method itself shows edge.
- [ ] **Funnel diagnosis (2026-05-28, `scripts/diag_funnel.py`).** 314 armed weeks →
      filled: LIVE 2 / best 9 / most 15. **Dominant killer = OUTWARD OFFSET:** fresh_trigger→filled
      drops ~85–95% (65→2, 80→9, 81→15). Pin triggers INSIDE zone but limit sits BEYOND zone extreme
      → price rejects, moves away, never fills. The "commitment filter" (constitution:103) is a
      never-trade filter. **Redesign target: entry fill mechanism** (fill at trigger bar / zero or
      inward offset). Inert rules to delete: recency cap ≤8 bars (got_trigger==fresh_trigger always)
      and R≥1.8 floor (filled==passed_R always). Also: G1 not truly mandatory — G1-fail + ATR-compressed
      scores exactly 5.5 and proceeds; 5.5 floor lets structure-less setups through.
- [x] **Entry-mechanism sweep (2026-05-28, `scripts/sweep_entry.py`).** OVERTURNS the fill-at-trigger
      fix. Outward offset is LOAD-BEARING, not a bug. Monotonic across sweep: more offset → fewer
      trades → higher win%/avgR/PF. fill_at_trigger: 63–77 trades, PF 0.64–0.71, **−$14.7k** (captures
      failed rejections). offset 0.00: still losing. **offset 0.15 = sweet spot:** PF ~2, +$9–10k,
      ~3 trades/yr. Current live 0.30 over-tuned (best quality, ~2 trades/yr, tiny N). Conclusion:
      method is inherently LOW-FREQUENCY (~2–3 quality trades/yr/instrument); aggregate frequency must
      come from multiple instruments, NOT from loosening any single gate. ACTIONS: (1) consider live
      offset_coef 0.30→0.15; (2) keep offset (do not fill-at-trigger); (3) low per-instrument freq is
      the rationale for multi-instrument breadth incl. EURUSD.
- [ ] **G5/G6 backtest gap.** Loader has no VIX or Asia-range data → G5 (1.5) + G6 (0.5) weights
      unvalidated (marked provisional in confluence_criteria). Add VIX + intraday-session to loader,
      run with/without comparison.
- [ ] NFP event drift (day before / day of / 3 days after)
- [ ] Trade duration: avg H4 bars to TP vs SL
- [ ] Consecutive loss / drawdown simulation — max drawdown characterization
- [ ] Structural level proxy: entries at 20-day swing H/L vs random (validates Signal 1 weight 2.5)
- [ ] Macro direction 2×2: falling yields × long vs falling yields × short
- [ ] D1 direct TD pull depth — does it extend before 2020?
