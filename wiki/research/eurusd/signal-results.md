---
type: research
updated: 2026-06-09
confidence: high
tags: [eurusd, signals, edge, independent-testing, mean-reversion]
related: [../xauusd/independent-signal-results.md, ../../system/eurusd/confluence_criteria.md]
---

# EURUSD — Independent Signal Results (P3)

Runner: `scripts/backtest_signals.py` (multi-instrument; extends gold Phase 0b catalogue).
Data: **D1 2010→2026 (16yr, 4279 bars)**; H4/H1 2020→2026 (~6.4yr, TwelveData free-tier
intraday depth cap); FRED macro (full history), ICE DXY (2009→now), CFTC 6E COT.
Forward windows: D1 fwd=5 (1wk), H4 fwd=6 (24h), H1 fwd=4 (4h). Macro = D1-only.
Baselines: D1 LNG 48.5% / SHT 51.4% · H4 LNG 49.3% / SHT 50.3% · H1 LNG 49.8% / SHT 48.7%.
Raw scan: `signal-scan-raw.txt`. (Original 2022-only scan was macro-null; the 16yr D1 sample
below revives the macro edges — the null was regime, not structural.)

---

## HEADLINE: EURUSD IS MEAN-REVERTING — THE OPPOSITE OF GOLD

Gold = momentum (RSI>70 continues up; fade fails). **EURUSD = mean-reversion: oscillator/band
extremes FADE, and trend-following is a measured ANTI-edge.** The gold confluence philosophy
must be INVERTED for EURUSD. Structural levels are FADE points, not breakout triggers.

---

## Confirmed edges (keep / promote) — strongest on H4

| Signal | TF | Dir | Edge | t | N | Note |
|---|---|---|---|---|---|---|
| A1 RSI(14)>70 | H4 | SHT | +10.4pp | **3.97** | 363 | Overbought FADE works (gold: this fails) |
| A4 RSI(14)<35 | H4 | LNG | +5.3pp | **3.16** | 895 | Oversold bounce |
| A3 RSI(14)>65 | H4 | SHT | +5.2pp | **2.92** | 792 | Earlier OB fade |
| A7 Stoch K>80 | H4 | SHT | +3.8pp | **2.77** | 1297 | Stoch OB fade |
| B10 Close>Keltner high | H4 | SHT | +4.3pp | **2.61** | 921 | Band over-extension fade |
| A11 CCI>+100 | H4 | SHT | +4.4pp | 2.56* | 860 | |
| A12 CCI<-100 | H4 | LNG | +4.2pp | 2.45* | 857 | |
| S1 Near big-figure (x.xx00) | H4 | LNG | +2.6pp | 2.35* | 2062 | FX round-number magnet |
| B9 Close<Keltner low | H4 | LNG | +3.6pp | 2.22* | 958 | |
| A8 Stoch K<20 | H4 | LNG | +2.9pp | 2.18* | 1381 | |
| B11 TTM squeeze on | H4 | LNG | +4.2pp | 2.16* | 655 | Compression precedes up-resolve |
| B5 BB squeeze (bw 20-low) | H4 | LNG | +3.1pp | 2.07* | 1109 | |
| A4 RSI<35 | H1 | LNG | +5.0pp | **4.93** | 2449 | Oversold long, very high N |
| A8 Stoch K<20 | H1 | LNG | +3.8pp | **4.73** | 3851 | |
| B9 Close<Keltner low | H1 | LNG | +4.1pp | **4.26** | 2666 | |
| A10 Williams%R<-80 | H1 | LNG | +2.8pp | **3.79** | 4447 | |
| S1 Near big-figure | D1 | LNG | +6.4pp | 2.43* | 358 | Strongest clean D1 signal |
| A4 RSI<35 | D1 | LNG | +9.3pp | 2.14* | 131 | |

## Strong ANTI-edges (trend-following fails — never use as pro-trend)

| Signal | TF | Dir | Edge | t | N |
|---|---|---|---|---|---|
| C26 ADX>25 & EMA20>50 (trend follow) | H4 | LNG | −6.6pp | **−5.17** | 1536 |
| C18 Aroon up>70 & down<30 | H4 | LNG | −4.4pp | **−3.32** | 1435 |
| C27 ADX>25 & EMA20<50 | H1 | SHT | −3.1pp | **−4.38** | 5040 |
| C19 Aroon down>70 & up<30 | H4 | SHT | −3.4pp | **−2.75** | 1592 |
| C20/C21 Supertrend (both dir) | H1 | — | ≈−1.3pp | **−2.6** | ~10k |
| C7 EMA20>EMA50 regime | H1 | LNG | −1.1pp | −2.24* | 10582 |
| S1s near big-figure as SHORT | D1 | SHT | −6.4pp | −2.43* | 358 |

**Reading:** every momentum/trend filter that *helped gold* (EMA regime, ADX-gated trend,
Supertrend, PSAR, Aroon, Donchian breakout) is negative on EURUSD. Mirror image of gold.

## Macro / intermarket — REAL on the 16yr D1 sample (was null on 2022-only)

| Signal | Dir | Edge | t | N | Verdict |
|---|---|---|---|---|---|
| **E10 DXY 1d jump>0.5** | **SHT** | **+23.0pp** | **9.29** | 409 | 🔑 strongest signal found. Dollar-spike day → EUR keeps falling next week. Intermarket momentum. |
| M4 US2Y(DGS2) 5d drop>0.15 | LNG | +9.3pp | 2.36* | 159 | Rate-easing shock → EUR up |
| M1 US2Y 20d slope<0 | LNG | +2.3pp | 2.06* | 2019 | Rate-momentum leg works (P2 driver vindicated) |
| M2 US2Y 20d slope>0 | SHT | +1.8pp | 1.70 | 2235 | mirror, near-sig |
| E16 VIX 1d spike>3 → long | LNG | −10.2pp | −2.56* | 159 | **FLIP: spike → EUR DOWN** (risk-off USD bid). Use as SHORT gate. |
| M7/M8 US−EZ carry slope | — | ≈0pp | <0.2 | ~2000 | DEAD — policy-rate diff carries no edge |
| M5/M6 2s10s curve | — | ≈0pp | <0.2 | ~2000 | DEAD even at 16yr |

**Verdict:** the rate-DIFFERENTIAL/carry/curve thesis stays dead, but **US 2Y slope (rate
momentum), DXY moves, and VIX spikes ARE directional** over 16yr. The 2022-only null was a
hawkish-regime artifact. Scoreable macro = {DXY 1d jump→short (dominant), US2Y slope, VIX
spike→short}. NOT carry diff, NOT 2s10s.

## Timeframe verdict
H4 is EURUSD's signal-richest frame (most |t|>2.6 edges, large N). D1 edges exist but small-N;
H1 oscillators strong but horizon too short for swing entries (trigger use only). **Score the
zone on D1 structure + H4 mean-reversion state.**
