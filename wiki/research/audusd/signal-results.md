---
type: setup
updated: 2026-06-10
confidence: high
tags: [audusd, signals, backtest, mean-reversion, research]
related: [../../system/audusd/confluence_criteria, ../../system/audusd/audusd_profile, ../eurusd/signal-results]
---

# AUDUSD — Signal Edge Scan (P3-style, D024 pair #1)

**Runner:** `scripts/backtest_signals.py --instrument audusd` — D1/H4 2010→now (4288/9786 bars),
H1 2020→now (39209 bars). Raw tables: `signal-scan-raw.txt`. Same catalogue as EUR/GBP scans.

## Verdict: GO — mean-reverting, H4-centric fade (EURUSD family)

AUDUSD behaves like the other USD-quote majors: **fade extremes, never trend-follow.**
- **H4 fade edges (core frame):** Keltner-low long +5.0pp t=3.52; RSI<35 long +5.2 t=3.41;
  CCI>+100 short +4.5 t=3.12; BB-lower long +6.3 t=2.80; CCI<−100 long +4.0 t=2.71;
  near-20d-HIGH short +2.8 t=2.65; near-20d-LOW long +2.4 t=2.11.
- **H1 = short-side oscillator machine:** CCI>+100 short t=6.54; Keltner-high short t=5.30;
  RSI>65 short t=5.23; Stoch>80 t=4.54; RSI>70 t=3.47; BB-upper/z>+2 t=3.38. Long-side H1 thin.
  Big-figure magnet LONG t=2.85. London-open short bias t=2.67.
- **Trend-following = measured anti-edge** (H1 Donchian-up −4.8pp t=−4.84; Supertrend both
  t≈−4.4; Aroon −4.05; H4 EMA-regime t≈−2.1..−2.5; B2r/B1r reversal rows confirm fade direction).
- **D1 price rows are THIN** (RSI<35 t=−0.71!) — unlike GBP's D1-reversal edge. AUD fades live
  on H4/H1, D1 supplies regime only (BB-squeeze long +4.8 t=2.54; September short t=2.31 noted,
  non-structural).

## 🔑 Macro — EUR/GBP gates do NOT all transfer

| Gate (EUR/GBP evidence) | AUDUSD result | Action |
|---|---|---|
| **DXY 1d jump>0.5 → short** (EUR t=9.29, GBP 7.27) | **DEAD** (t=−0.85) | do NOT score, do NOT veto |
| US2Y (DGS2) 20d slope | slope<0 long t=2.28 / slope>0 short t=2.12 | score (direction leg) |
| VIX 1d spike>3 → short (GBP −22pp) | **DEAD** (t=0.04) | no FX VIX-veto-LONGS for AUD |
| 2s10s curve | dead (t≈−0.8..−1.1) | ignore (as everywhere) |
| **VIX LEVEL regime** (new for AUD) | **VIX>20 → LONG +8.7pp t=6.14; VIX<15 → SHORT +6.8pp t=5.29** | score as regime tilt |

**VIX polarity is INVERTED vs the EUR/GBP veto logic.** High-VIX regimes = AUD already
sold/cheap → mean-revert UP; low-VIX = AUD rich → fade DOWN. This is a *level/regime* signal
(N≈1250/1500 D1 days), not an event spike. Consequence: the FX VIX-veto-LONGS rule **must not**
be applied to AUDUSD; instead VIX level scores as a tilt in Z5 (see [[confluence_criteria]]
in `wiki/system/audusd/`).

## Costs
D1 ATR14: 16yr p25/med/p75 = 61/74/99 pips; last-5yr med 63; now ~51. H4 med 25, now ~22.
Spread ~0.6–1.2 pips ≈ 5–10× covered by H4 edges (similar economics to EURUSD). GO.

## Not onboarded as edges
DXY-jump (dead), VIX-spike (dead), carry/policy-diff (no daily RBA series; dead family per
D021), seasonality (Sep short t=2.31 — noted, not scored), engulf/pin as standalone (≤|1.3|).
