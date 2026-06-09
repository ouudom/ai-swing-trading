---
type: research
updated: 2026-06-09
confidence: high
tags: [gbpusd, signals, edge, independent-testing, mean-reversion]
related: [../xauusd/independent-signal-results.md, ../eurusd/signal-results.md, ../../system/gbpusd/confluence_criteria.md]
---

# GBPUSD — Independent Signal Results (P3)

Runner: `scripts/backtest_signals.py`. Data: **D1 2010→2026 (16yr, 4279 bars)**; H4/H1
2020→2026 (~6.4yr, TD free-tier intraday cap); FRED macro (full), ICE DXY (2009→now), CFTC 6B COT.
Forward windows: D1 fwd=5, H4 fwd=6, H1 fwd=4. Macro = D1-only.
Baselines: D1 LNG 49.2% / SHT 50.7% · H4 LNG 50.8% / SHT 48.8% · H1 LNG 50.1% / SHT 48.7%.
Raw scan: `signal-scan-raw.txt`.

---

## HEADLINE: GBPUSD IS MEAN-REVERTING (like EURUSD, opposite of gold)

Same character as [[../eurusd/signal-results]]: fade oscillator/band extremes, fade structure;
trend-following is anti-edge. **Difference vs EURUSD: GBP's cleanest edges sit on D1 (and H1),
while EUR's concentrate on H4.** GBP D1 reversal signals are large but lower-N — treat as
strong-but-wide.

## Confirmed edges (keep / promote)

| Signal | TF | Dir | Edge | t | N | Note |
|---|---|---|---|---|---|---|
| C12 Near 20d LOW | D1 | LNG | +18.0pp | **3.03** | 71 | Buy support (structure as FADE) |
| A1 RSI(14)>70 | D1 | SHT | +24.1pp | **2.77** | 33 | OB fade — huge but small-N |
| A8 Stoch K<20 | D1 | LNG | +9.5pp | 2.51* | 175 | Oversold bounce |
| A3 RSI(14)>65 | D1 | SHT | +10.7pp | 2.15* | 101 | |
| G7 September | D1 | SHT | +11.1pp | 2.06* | 86 | Seasonal weakness |
| A10 Williams%R<-80 | D1 | LNG | +6.8pp | 2.02* | 218 | |
| A3 RSI>65 | H1 | SHT | +3.3pp | **3.41** | 2711 | |
| C11 Near 20d HIGH | H1 | SHT | +1.5pp | **3.39** | 12539 | Resistance fade (high N) |
| A8 Stoch K<20 | H1 | LNG | +2.7pp | **3.32** | 3844 | |
| A2 RSI<30 | H1 | LNG | +4.8pp | **3.17** | 1110 | |
| A10 Williams%R<-80 | H1 | LNG | +2.4pp | **3.15** | 4444 | |
| A4 RSI<35 | H1 | LNG | +2.9pp | **2.81** | 2408 | |
| A5 RSI2<10 (Connors) | H1 | LNG | +1.8pp | **2.70** | 5861 | |
| D6s ATR pctile<0.2 (calm) | H4 | SHT | +4.1pp | **3.33** | 1647 | Calm → mild down drift |
| B9 Close<Keltner low | H4 | LNG | +4.1pp | 2.53* | 963 | |
| A4 RSI<35 | H4 | LNG | +4.1pp | 2.33* | 791 | |

## Strong ANTI-edges (trend-following fails)

| Signal | TF | Dir | Edge | t | N |
|---|---|---|---|---|---|
| C12r near 20d LOW as SHORT | D1 | SHT | −17.9pp | **−3.02** | 71 |
| C26 ADX>25 & EMA20>50 | D1 | LNG | −8.2pp | −2.38* | 210 |
| C4 Close<EMA50 | H1 | SHT | −1.9pp | **−3.78** | 10174 |
| C3 Close>EMA50 | H1 | LNG | −1.8pp | **−3.68** | 10998 |
| C20 Supertrend bull | H1 | LNG | −1.6pp | **−3.25** | 10803 |
| C26 ADX>25 & EMA20>50 | H4 | LNG | −4.9pp | **−3.61** | 1382 |
| D6 ATR calm as LONG | H4 | LNG | −4.3pp | **−3.51** | 1647 |
| C7/C8 EMA regime, C27 ADX trend | H1 | — | ≈−1.4pp | **<−2.6** | ~10k |

## Macro / intermarket — REAL on the 16yr D1 sample (was null on 2022-only)

| Signal | Dir | Edge | t | N | Verdict |
|---|---|---|---|---|---|
| **E10 DXY 1d jump>0.5** | **SHT** | **+18.0pp** | **7.27** | 409 | 🔑 dollar-spike day → GBP keeps falling |
| **E16 VIX 1d spike>3 → long** | LNG | **−22.2pp** | **−5.60** | 159 | **FLIP: spike → GBP CRASH** (risk-off). Strong SHORT gate. |
| M1 US2Y(DGS2) 20d slope<0 | LNG | +2.7pp | 2.39* | 2018 | Rate-momentum leg works |
| M2 US2Y 20d slope>0 | SHT | +2.3pp | 2.15* | 2236 | mirror, significant |
| M4 US2Y 5d drop>0.15 | LNG | +3.6pp | 0.91 | 159 | weaker than EUR |
| M5–M9 carry / 2s10s | — | ≈0pp | <0.3 | ~2000 | DEAD |

**Verdict (same as EURUSD):** carry-diff + 2s10s dead; **US 2Y slope, DXY moves, VIX spikes
are directional** over 16yr. GBP's VIX-spike crash edge is the largest of the two pairs (risk
currency). Scoreable macro = {DXY 1d jump→short, VIX spike→short, US2Y slope}.

## Timeframe verdict
GBP's actionable swing edges are on **D1 reversal (structure + oscillator extreme)** and H1
oscillators; H4 weaker than EURUSD's. Score the zone on D1 structure/oversold-overbought; use
H1 oscillator extreme as the entry-timing confirmation.
