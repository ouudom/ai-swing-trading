---
type: setup
updated: 2026-06-10
confidence: medium
tags: [nzdusd, signals, backtest, mean-reversion, research]
related: [../../system/nzdusd/confluence_criteria, ../../system/nzdusd/nzdusd_profile, ../audusd/signal-results]
---

# NZDUSD — Signal Edge Scan (D024 pair #2)

**Runner:** `scripts/backtest_signals.py --instrument nzdusd` — D1/H4 2010→now (4288/9789 bars),
H1 2020→now (39227 bars). Raw tables: `signal-scan-raw.txt`.

## Verdict: GO, but MARGINAL — weakest edge set scanned so far

Same mean-reversion family as the other USD-quote majors (trend-following = anti-edge:
H1 Supertrend t=−3.1/−3.4, Aroon −2.70, EMA-regime −2.5..−2.7; H4 big-figure-short −2.68,
20d-extreme continuation REV rows negative). But **edges run ~half of AUDUSD's**:

- **H4 (best frame):** TTM squeeze long +4.8pp t=3.25; big-figure LONG magnet +2.6 t=2.77;
  CCI>+100 short +3.7 t=2.51; RSI2>90 short +6.9 t=2.41; bullish pin long +3.0 t=2.40;
  Keltner-high short / Keltner-low long ≈ +2.8 t≈2.05; CCI<−100 long +2.9 t=2.03.
- **H1 (short-side, modest):** near-20d-HIGH short t=3.09; Keltner-high short t=3.00;
  Stoch>80 / W%R short t≈2.9; RSI>65 short t=2.45; CCI>+100 t=2.12; London-open short t=2.12.
- **D1 thin:** BB/TTM squeeze long t≈2.1–2.35; oscillator fades NOT significant on D1.

## 🔑 Macro — nearly everything is DEAD for NZD

| Gate | AUDUSD | NZDUSD | Action |
|---|---|---|---|
| VIX LEVEL regime (inverted) | t=6.14/5.29 | **VIX>20→LONG t=2.18; VIX<15→SHORT t=2.38** | score, low weight |
| US2Y (DGS2) 20d slope | t≈2.2 | **DEAD (t=−0.64/−0.76)** | do NOT score |
| DXY 1d jump | dead | **DEAD (t=0.24)** | no score, no block |
| VIX 1d spike | dead | dead/negative (t=−1.72) | no veto |
| 2s10s | dead | dead | ignore |

NZDUSD is effectively **price/structure-only with a weak VIX-level tilt** — closer to EURGBP's
macro-light profile than to AUD's.

## Costs + redundancy
D1 ATR14 16yr p25/med/p75 = 58/71/90 pips (5yr med 60, now ~54); H4 med 23. Spread ~1–1.5 pips =
larger cost fraction than AUD on half the edge. **AUDUSD strictly dominates NZDUSD** (same class,
same direction exposure, ~2× edge): when both set up, the fx_exposure antipodean advisory should
normally resolve to AUD. Trade NZD on its own clean setups; expect fewer publishable zones
(floor 5.0 will be harder to reach — that is correct behaviour, not a bug).
