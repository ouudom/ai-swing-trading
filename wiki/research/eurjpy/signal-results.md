---
type: system
updated: 2026-06-11
confidence: high
tags: [eurjpy, signals, backtest, onboarding, cross, jpy]
related: [signal-scan-raw.txt, eurjpy_profile, confluence_criteria]
---

# EURJPY Signal Edge Scan — Results & Verdict

**Verdict: ✅ GO — SYMMETRIC mean-reversion + calm-drift hybrid.**
Sample: D1 1,159 bars (2010→), H4 6,848 / H1 27,396 trading-day bars (2020→).
Baselines: D1 LNG 55.6% / H4 54.4% / H1 53.1% — persistent long drift (JPY structural
weakness, same carry regime as usdjpy but expressed through the EUR leg too).

Raw output: [[signal-scan-raw.txt]]. Scan run 2026-06-11, fwd horizons D1=5 / H4=6 / H1=4.

## Character — third template among the JPY/CHF set

| | USDCHF | USDJPY | **EURJPY** |
|---|---|---|---|
| H1 overbought fade | ✅ core edge | ❌ ANTI (−3.3) | ✅ **works (A9 t=4.21, A3 t=3.61)** |
| D1 dip-buy at extremes | weak | dip-at-20d-low only | ✅ **strong (A8 Stoch<20 t=3.10, 73% win)** |
| Calm/squeeze long engine | ✅ | ✅ | ✅ (H4 D6 t=3.96, B11 t=2.71) |
| Macro gate | DXY 20d slope | DXY 20d slope | ❌ **NONE — fully dead** |

EURJPY trades like a **two-sided fade pair on top of a long-drift floor**: buy washouts,
fade extension, never chase.

## Long side (drift + dip-buy)
| Code | Signal | TF | t | Note |
|---|---|---|---|---|
| D6 | ATR pctile<0.2 (calm) | H4 | **3.96** | calm grind-up — core long engine |
| A8 | Stoch K<20 | D1 | **3.10** | 73.1% win, avg +0.62% — best D1 row |
| C12 | Near 20d LOW | H1 | **3.07** | dip-buy structure |
| H4o | NY/London overlap 12–16 | H1 | **3.02** | long drift window (like usdjpy NY drift) |
| B11 | TTM squeeze on | H4/D1 | 2.71 / 2.47 | compression → drift resolution UP |
| B9 | Close<Keltner low | H1 | 2.62 | washout buy |
| A12 | CCI<−100 | H4 | 2.55 | |
| D5/D1 | Inside bar / compressed | H4 | 2.18 / 2.18 | |
| A2 | RSI<30 | H1 | 2.21 | |

## Short side (fade extension — works on ALL TFs, unlike usdjpy)
| Code | Signal | TF | t | Note |
|---|---|---|---|---|
| A9 | Williams%R>−20 | H1 | **4.21** | strongest row in scan |
| A3 | RSI>65 | H1/D1/H4 | 3.61 / 2.64 / 2.81 | overbought fade, every TF |
| B10 | Close>Keltner high | D1/H4/H1 | 3.36 / 3.48 / 2.82 | extension fade, every TF |
| A1 | RSI>70 | H4/D1 | 3.00 / 2.98 | |
| H2s | London open 07–09 | H1 | 2.77 | fade London-open pop |
| A11 | CCI>+100 | H4 | 2.36 | |

Shorts fight a 55.6% long baseline — counter-trend by construction. Fade rows clear it
anyway, but avg% sits near zero on H4/H1 shorts: edge is win-rate, not run length. Keep
shorts at extremes only, take profits early.

## Macro — DEAD (purest price-driven pair so far)
- **X9/X10 ECB-leg slope: NEGATIVE** (−1.23 / −1.31) — ECBDFR step function carries no
  signal, mildly anti. One-leg cross macro = non-scoring, as built.
- **VIX: DEAD** — E13 VIX>20 long t=0.91, E15 t=0.55, E16 spike t=−0.42. The "carry
  barometer" reputation does NOT show at the D1 5-bar horizon. No VIX veto, no VIX
  criterion. (Crash-day tail risk still real — handled by MoF/BoJ event blocks, not VIX.)
- No DXY rows (cross), no US2Y rows. **Confluence = 100% price/structure/session.**

## Anti-edges (vetoes)
| Code | Signal | TF | t | Lesson |
|---|---|---|---|---|
| C26 | ADX>25 & EMA20>50 (chase ext.) | D1/H4 | **−4.24 / −3.96** | NEVER chase extension long |
| D6s | calm-ATR short | H4 | −3.99 | never short compression |
| C2 | Close<EMA20 short | D1/H1 | −3.32 / −3.32 | momentum shorts fail |
| C19/C18 | Aroon trend rows | D1 | −3.18 / −2.90 | trend-following dead |
| G9 | Turn of month long | D1 | **−3.10** | same anti as usdjpy |
| C9 | Donchian20 breakout UP | H1 | −2.61 | breakout chasing anti |
| C12r | 20d-low REV short | H1 | −3.05 | don't short the dip |

## Sessions
- **NY/London overlap 12–16 UTC = LONG drift window** (H1 t=3.02; NY open long 2.26).
- **London open 07–09 = SHORT fade window** (H1 t=2.77) — two-sided session structure:
  fade the London pop, ride the NY drift. H4 London long 1.58 ns.

## Costs & ATR (JPY pips, 1 pip = 0.01)
| | p25 | median | p75 | now (2026-06-11) |
|---|---|---|---|---|
| D1 ATR14 | 95 | 118 | 152 | **76 — deep compression** |
| H4 ATR14 (trading-day) | 32 | 42 | 56 | **27** |

Spread ~1.5–3 pips (Exness) ≈ 4–7% median H4 ATR — fine for H4/D1 swing, tight-ish for
H1 scalps. ATR ≈ 1.37× usdjpy on D1; H4 medians nearly equal (42 vs 40). V1B_BUFFER 0.04.

## MoF/BoJ regime (inherited from usdjpy — interventions slam ALL JPY crosses)
Spot **185.21** — record territory, JPY weak across the board (USDJPY 160.5 inside the
2022/2024 intervention band). MoF intervention targets USDJPY but EURJPY moves
comparably (300–500 USDJPY pips ⇒ similar EURJPY slams). Same hard blocks: BoJ decision
days, active MoF jawboning. Fresh-high longs near intervention-watch regimes cap MEDIUM.

## COT
Direct CME contract `EURO FX/JAPANESE YEN XRATE` — DIRECT read (long = long EURJPY).
**Thin: OI ~21k** (vs 6J ~250k). Use as context only; extremes are small-number noise.

## Cross-pair macro map (updated, 7 scans)
- DXY 1d jump: EUR/GBP only. VIX-level fade-USD: AUD/NZD/CAD. DXY 20d slope: CHF/JPY
  (USD-base havens). VIX washout: CHF/JPY. **Crosses (EURGBP, EURJPY): NO macro at all.**
- London-open drift: AUD/NZD/CAD/CHF; USDJPY = NY drift; **EURJPY = both (London fade-short
  + NY drift-long).**
