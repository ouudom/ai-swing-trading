---
type: system
updated: 2026-06-11
confidence: high
tags: [gbpjpy, signals, backtest, onboarding, cross, jpy]
related: [signal-scan-raw.txt, gbpjpy_profile, confluence_criteria]
---

# GBPJPY Signal Edge Scan — Results & Verdict

**Verdict: ✅ GO — extension-fade pair, SHORT-side dominant, on the strongest long-drift
floor in the book.**
Sample: D1 1,159 bars (2010→, macro-aligned window), H4 6,845 / H1 27,388 trading-day
bars (2020→). Baselines: D1 LNG 56.7% / H4 54.8% / H1 52.4% — highest D1 long baseline
of all 10 instruments (GBP carry vs JPY, widest live rate gap ~4% vs ~0.5%).

Raw output: [[signal-scan-raw.txt]]. Scan run 2026-06-11, fwd horizons D1=5 / H4=6 / H1=4.

## Character — FOURTH template (not eurjpy's, despite both being JPY crosses)

| | USDJPY | EURJPY | **GBPJPY** |
|---|---|---|---|
| Extension fade (short) | D1 only | ✅ all TFs | ✅ **all TFs, STRONGEST (H4 B10 t=4.64)** |
| Dip-buy at extremes | 20d-low only | ✅ strong (Stoch t=3.10) | ✅ moderate (RSI<35 t=2.26/2.43) |
| Calm/squeeze long engine | ✅ | ✅ (t=3.96) | ❌ **DEAD (D6 1.42, B11 −0.32)** |
| Macro gate | DXY 20d slope | NONE | ❌ **NONE (SONIA t=0.58, VIX dead)** |
| Session structure | NY drift long | two-sided | **NY long-only; London DEAD** |

The expected "carry-trend Beast" did NOT show: every trend/momentum row is anti.
GBPJPY is a **fade-the-extension pair** — short overbought spikes, buy washouts,
never chase, no calm-compression engine to lean on.

## Short side (extension fade — the dominant engine)
| Code | Signal | TF | t | Note |
|---|---|---|---|---|
| B10 | Close>Keltner high | H4/D1/H1 | **4.64 / 4.01 / 2.42** | best rows in scan |
| A11 | CCI>+100 | H4/D1 | 4.12 / 3.22 | |
| A7 | Stoch K>80 | H4 | 3.80 | |
| A3 | RSI>65 | D1/H4/H1 | 3.69 / 3.58 / 2.59 | overbought fade, every TF |
| B1/B8 | Close>BB upper / z>+2 | D1/H4 | 3.02 / 3.44 | D1: 63.2% win, avg +0.42% |
| A1 | RSI>70 | H4 | 3.18 | |
| A9 | Williams%R>−20 | H4/H1 | 3.09 / 2.07 | |
| C11 | Near 20d HIGH | D1/H4 | 2.40 / 2.12 | |
| C14 | MACD cross down | H4 | 2.24 | |
| G7 | September | D1 | 2.34 | seasonal short tilt |

Shorts fight a 56.7% long baseline — strictly extreme-fade, take profits early
(H4/H1 short avg% ≈ 0: edge is win-rate, not run length). D1 band shorts (B1/B8)
are the exception: +0.42%/trade real run.

## Long side (washout dip-buy — secondary)
| Code | Signal | TF | t | Note |
|---|---|---|---|---|
| H4o | NY/London overlap 12–16 | H1 | **4.20** | core long drift window |
| H3 | NY open 13–15 | H1 | 3.75 | |
| D5 | Inside bar | H1 | 2.62 | |
| C12 | Near 20d LOW | H1/H4 | 2.56 / 2.00 | dip-buy structure |
| A4 | RSI<35 | H4/D1 | 2.43 / 2.26 | D1: 73.3% win, +0.65% |
| B9 | Close<Keltner low | H4/D1 | 2.33 / 2.27 | D1: 69.9% win, +0.56% |
| A12 | CCI<−100 | D1 | 2.18 | |

**No calm engine**: D6 calm-long H4 t=1.42, B11 TTM −0.32 (H4), B5 squeeze ~0.
Compression carries no directional information here — unlike usdchf/usdjpy/eurjpy.

## Macro — DEAD (second fully price-driven pair)
- **X9/X10 SONIA slope: nothing** (t=0.58 / 0.29). One-leg cross macro = non-scoring,
  as built (live leg rides the `RATE_EUR` slot = IUDSOIA).
- **VIX: dead** — E13 VIX>20 long t=0.89, E15 0.12, E16 spike −1.81 (mildly anti:
  don't buy VIX spikes). No VIX veto, no VIX criterion. Crash tail handled by
  MoF/BoJ event blocks.
- No DXY/US2Y rows (cross). **Confluence = 100% price/structure/session.**

## Anti-edges (vetoes)
| Code | Signal | TF | t | Lesson |
|---|---|---|---|---|
| C26 | ADX>25 & EMA20>50 (chase ext.) | H4/H1/D1 | **−5.00 / −4.69 / −2.57** | NEVER chase extension long |
| H3s | NY open short | H1 | **−3.84** | never short the NY drift window |
| C8 | EMA20<EMA50 short | D1 | −3.75 | momentum shorts fail |
| B1r | BB-upper breakout long | H4/D1 | −3.36 / −3.02 | band break = fade it, not ride it |
| G9 | Turn of month long | D1 | −2.99 | same anti as usdjpy/eurjpy |
| C27 | ADX>25 & EMA20<50 short | D1 | −2.83 | no momentum shorts either |
| C21/C20 | Supertrend rows | D1/H4 | −2.65…−2.90 | trend-following dead |
| G6 | January long | D1 | −2.28 | seasonal anti |
| C9/C10 | Donchian breakout/down | D1 | −1.86 / −1.93 | breakout chasing anti |

## Sessions — NY long-only (NOT eurjpy's two-sided structure)
- **NY/London overlap 12–16 UTC = LONG drift** (H1 t=4.20; NY open 13–15 t=3.75).
- **NY open SHORT = hard anti (−3.84)** — short entries must avoid 13–15 UTC.
- **London open 07–09: DEAD both directions** (+0.71 / −0.46) — no London fade edge,
  unlike eurjpy.

## Costs & ATR (JPY pips, 1 pip = 0.01)
| | p25 | median | p75 | now (2026-06-11) |
|---|---|---|---|---|
| D1 ATR14 | 125 | 151 | 186 | **93 — deep compression** |
| H4 ATR14 (trading-day, range≥0.05) | 44 | 54 | 70 | **36** |

Highest-ATR pair in the book (1.28× eurjpy on both TFs). Spread ~2.5–4 pips (Exness)
≈ 5–7% median H4 ATR — fine for H4/D1 swing; H1 edges (avg ≈ 1–4 pips) are NOT
standalone tradeable — timing only. V1B_BUFFER 0.05 (10% median H4 ATR).

## MoF/BoJ regime (inherited — interventions slam ALL JPY crosses, GBPJPY hardest)
Spot **214.62** — record territory alongside USDJPY 160.5 / EURJPY 185.2. MoF
intervention targets USDJPY but GBPJPY slams are the LARGEST of the crosses
(vol-amplified). Hard blocks: BoJ decision days, active MoF jawboning, BoE decision
days. Fresh-high longs in intervention-watch regimes cap MEDIUM.

## COT
**NO direct CFTC GBP/JPY cross contract** (2026 disagg zip carries only EUR/GBP and
EUR/JPY XRATEs). `COT_ENABLED=False` — no 6B/6J synthesis (different question, noisy).
First pair in the book with no COT section at all.

## Cross-pair macro map (final, 8 scans)
- DXY 1d jump: EUR/GBP. VIX-level fade-USD: AUD/NZD/CAD. DXY 20d slope: CHF/JPY
  (USD-base havens). VIX washout: CHF/JPY. **Crosses (EURGBP, EURJPY, GBPJPY): NO
  macro at all — all three fully price-driven.**
- Calm/squeeze long engine: CHF/JPY/EURJPY yes — **GBPJPY no** (only JPY pair without it).
- Sessions: London-open drift AUD/NZD/CAD/CHF; USDJPY+GBPJPY = NY drift-long;
  EURJPY = two-sided (London fade + NY drift).
