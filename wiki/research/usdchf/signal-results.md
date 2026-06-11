---
type: setup
updated: 2026-06-10
confidence: high
tags: [usdchf, signals, backtest, mean-reversion, usd-base, safe-haven, research]
related: [../../system/usdchf/confluence_criteria, ../../system/usdchf/usdchf_profile, ../usdcad/signal-results]
---

# USDCHF — Signal Edge Scan (D024 pair #4 — second USD-BASE pair)

**Runner:** `scripts/backtest_signals.py --instrument usdchf` — D1/H4 2010→now (4287/9774 bars),
H1 2020→now (39197 bars). Raw: `signal-scan-raw.txt`. USD-base direction flip via
`USD_BETA_SIGN=+1` (no oil leg — `FRED_SERIES_BASE` only).

## Verdict: GO — mean-reverting fade; H1 = overbought-fade SHORT machine; D1 carries the macro

- **H1 SHORT-side fade machine** (mirror of USDCAD's long side — both are *fade the move*
  intraday): W%R>−20 short +3.5pp **t=5.48**; RSI>65 short **t=4.57**; Keltner-high short
  **t=4.57**; Stoch>80 short t=4.01; RSI>70 short t=3.42; CCI>+100 short t=2.55.
- **H1 LONG side:** TTM squeeze-on long t=3.20; calm-ATR long t=3.03; near-20d-LOW long t=2.92;
  **London open 07–09 LONG drift t=2.70** (same USD-long London drift as USDCAD t=2.92 —
  4th pair confirming the London USD-direction drift).
- **D1:** W%R<−80 long t=2.22; bearish engulfing short t=2.14 (pattern *continuation* works
  here, unlike USDCAD where it was the top anti-edge); MACD-down short t=1.97 borderline.
- **H4 = weakest TF:** BB-expanding long t=2.33 and big-figure long t=2.02 only; fade edges
  sub-2 (BB-upper short 1.92, RSI2>90 short 1.89, Donchian-breakdown short 1.97). H4 scores
  thin — zones anchor on D1/H1 evidence.
- **Anti-edges (never score):** H1 NR7-long −3.35, near-20d-LOW-REV short −2.99, ALL momentum
  continuation (Close>EMA20 long −2.72, ROC10 ±, Donchian-UP long −2.62); H4 downtrend
  continuation (ADX>25 & EMA20<50 short) **t=−3.05** — fade H4 downtrends, never join them.

## 🔑 Macro — DXY 20d SLOPE is live (first pair beyond EUR/GBP); VIX is a washout

| Gate | Result (D1, 16yr) | Action |
|---|---|---|
| **DXY 20d slope (flipped rows)** | slope>0 → LONG +4.9pp t=2.32; slope<0 → SHORT +4.9pp t=2.34 | **score** — USDCHF is the closest DXY proxy in the book (CHF≈EUR bloc); first non-EUR/GBP pair with a live DXY signal |
| DXY 1d jump (flipped) | long after jump t=−1.69 — wrong-way | dead; if anything fade jumps. No block |
| **VIX (level + spike)** | VIX>20→long t=1.39, VIX<15→short t=−1.97 (i.e. weak LONG both regimes); spike t=1.04 | **no gate, no score** — haven-vs-haven washout: USD and CHF both catch risk-off bids, net signal dies. The commodity-FX fade-USD regime does NOT transfer |
| US2Y (DGS2) 20d slope (flipped) | rising → long t=1.34; falling → short t=1.46 | weak tilt only (½-point at most) |
| 2s10s / carry | dead | ignore (no daily SNB series anyway, RATE_FOREIGN=None) |

**Cross-pair macro map after 5 FX scans:** DXY-jump = EUR/GBP only. VIX-level fade-USD =
commodity FX only (AUD/NZD/CAD). DXY-slope = USDCHF (DXY proxy). NZD = macro-dark. Each pair
keeps only what its own scan proves.

## Costs
D1 ATR14 (last 500 bars) p25/med/p75 = 53/60/66 pips, now ~50 — compressed; H4 med ~20, H1 ~8.
Spread ~1.5–2 pips ≈ 8–10% of an H4 edge → H4 zones need the floor respected strictly.
V1b 4 pips, MIN_BAR_RANGE per `_fx_base`. Spot 0.797 — historic-low zone, SNB regime active
(see profile). GO.

## Not onboarded
VIX gates (washout), DXY 1d jump (anti), 2s10s/carry (dead), H4 trend-side anything
(C27 anti-edge −3.05). COT 6S direct read (INVERTED — spec long CHF = short USDCHF).
