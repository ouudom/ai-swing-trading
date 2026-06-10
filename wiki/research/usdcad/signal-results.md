---
type: setup
updated: 2026-06-10
confidence: high
tags: [usdcad, signals, backtest, mean-reversion, usd-base, oil, research]
related: [../../system/usdcad/confluence_criteria, ../../system/usdcad/usdcad_profile, ../audusd/signal-results]
---

# USDCAD — Signal Edge Scan (D024 pair #3 — first USD-BASE pair)

**Runner:** `scripts/backtest_signals.py --instrument usdcad` — D1/H4 2010→now (4288/9789 bars),
H1 2020→now (39230 bars). Raw: `signal-scan-raw.txt`. First scan with the USD-base direction
flip (mechanical DXY/M-rows inverted via `USD_BETA_SIGN=+1`) + the new 🛢 W-rows (WTI).

## Verdict: GO — mean-reverting fade, H4 + H1, LONG-side richer intraday

- **H4 fade edges:** BB-upper/z>+2 short +6.9pp t=3.19; BB squeeze long +4.0 t=3.14;
  near-20d-LOW long +2.3 t=2.69; Stoch<20 long +2.8 t=2.53; CCI>+100 short +3.6 t=2.49;
  Keltner-low long t=2.03. Calm-ATR short t=2.39.
- **H1 = LONG-side fade machine** (mirror of AUD/NZD's short side — same *fade-the-USD-rally*
  trade expressed in a USD-base quote): W%R<−80 long t=3.45; CCI<−100 long t=3.10;
  CCI>+100 short t=3.08; RSI2<10 long t=2.89; **London open 07–09 LONG drift t=2.92**
  (AUD/NZD show short drift — consistent USD-direction across all three).
- **D1 thin:** Stoch>80 short t=2.38 only; D1 = regime frame.
- **Anti-edges (never score):** bearish-engulf continuation short −3.6pp t=−3.83; Donchian
  breakdown short −2.83; calm-ATR short −2.85; D1 Aroon-down short −2.77, EMA-regime −2.27.

## 🔑 Macro — VIX-level "fade the USD" regime transfers; the rest is thin

| Gate | Result (D1, 16yr) | Action |
|---|---|---|
| **VIX LEVEL (inverted, as USD-fade)** | raw rows: VIX>20→LNG t=−3.86, VIX<15→SHT t=−2.97 ⇒ **VIX>20 → SHORT USDCAD +5.5pp; VIX<15 → LONG +3.8pp** | score — same regime as AUD/NZD: high VIX = USD already bid → fade it |
| US2Y (DGS2) 20d slope (flipped rows) | slope<0 → short t=2.10; slope>0 → long t=1.97 | score small (mechanical USD leg works) |
| 🛢 WTI | only W5 (5d>+5% → short) t=1.67; slopes/1d-jumps dead | weak TILT only, never a gate; FRED oil lags ~1wk |
| DXY 1d jump (flipped) | t=−1.63 wrong-way sub-sig | dead — no score, no block |
| 2s10s / carry | dead | ignore |

**Cross-pair pattern now 3/3:** the *level* of VIX defines a fade-the-USD regime on commodity-FX
(AUD t=6.1, NZD t=2.2, CAD t=3.9 in USD-fade terms); the VIX *spike* and DXY-jump event gates
only ever worked for EUR/GBP. Polarity for USDCAD: **high VIX blocks nothing, favors SHORTs.**

## Costs
D1 ATR14 16yr p25/med/p75 = 69/84/103 pips (5yr med 76, now ~50 — compressed); H4 med 30.
Spread ~1.5–2 pips ≈ 5–8% of an H4 edge. V1b 5 pips, MIN_BAR_RANGE 3 pips. GO.

## Not onboarded
DXY-jump (dead), VIX-spike (dead t=−0.95), WTI slopes/1d (dead — W5 5d-spike kept as tilt),
COT 6C direct read (INVERTED — spec long CAD = short USDCAD; snapshot prints both).
