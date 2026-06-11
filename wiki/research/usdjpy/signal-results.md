---
type: setup
updated: 2026-06-11
confidence: high
tags: [usdjpy, research, signal-scan, backtest]
related: [usdjpy_profile, confluence_criteria, signal-scan-raw]
---

# USDJPY Signal Edge Scan — Results & Verdict

**Verdict: GO** — but the character is NOT the FX fade template. USDJPY is an
**asymmetric carry-drift instrument**: LONG side = compression/dip continuation
(closer to XAUUSD momentum), SHORT side = D1/H4 oscillator-extreme fade only.
H1 overbought fade — the CHF/CAD money-maker — is an **anti-edge** here.

Scan: `backtest_signals.py --instrument usdjpy` (raw: [[signal-scan-raw]]).
Data: D1 4288 bars (2010→), H4 9764 / H1 39179 (2020-01-29→). D1 baseline LNG 58.9% —
structural long drift (90→160 over the sample; carry). Edges below are baseline-adjusted.

## Long side (drift continuation)
| TF | Signal | t | Note |
|---|---|---|---|
| D1 | TTM squeeze on → LONG | **3.27** | +15.9pp edge, strongest D1 row |
| H4 | ATR pctile<0.2 (calm) → LONG | **4.51** | strongest H4 row; mirror short −4.54 |
| H1 | NY/London overlap 12–16 → LONG | **4.71** | session drift = NY, NOT London (H2 flat +0.02) |
| H1 | NY open 13–15 → LONG | **4.19** | NY short = anti (−3.97) |
| H1 | calm ATR → LONG | **3.22** | |
| H1 | near 20d LOW → LONG | **3.15** | dip-buy in uptrend (H4 1.85 same sign) |
| H1 | Close>BB upper REV → LONG | **3.08** | breakout CONTINUATION long; fading it = −3.33 |
| H1 | Donchian20 breakout UP → LONG | 2.05 | momentum upside confirmed |
| D1 | DXY 20d slope>0 → LONG | **2.21** | macro live — 3rd pair beyond EUR/GBP (with CHF) |

## Short side (D1/H4 extremes only)
| TF | Signal | t |
|---|---|---|
| H4 | CCI>+100 → SHORT | **3.11** |
| D1 | RSI>65 → SHORT | **2.66** |
| H4 | Keltner-high → SHORT | 2.35 |
| D1 | PSAR bear → SHORT | 2.36 |
| H4 | RSI>65 → SHORT | 2.09 |
| D1 | CCI>+100 → SHORT | 2.09 |
| H1 | NR7 → SHORT | 3.18 (odd; pairs with NR7-long anti −3.17) |

## Macro
- **DXY 20d slope = live** (D1 long 2.21 / short 1.73). Same finding as USDCHF — DXY
  slope works on USD-base havens. DXY 1d jump = anti (−1.32), never block.
- **VIX = WASHOUT** (VIX>20 long t=0.19, VIX<15 short −0.15, spike −0.54). Same as CHF:
  haven-vs-haven (carry unwind bids JPY, USD bid too). No gate, no score.
- **US2Y dead** (M2 t=0.15, M3 0.58) — BoJ-era sample swamps the rate story. Carry is
  in the baseline drift, not in 20d rate wiggles.

## Anti-edges (prohibited)
- **H1 overbought fade SHORT**: BB-upper/z>2 short t=−3.33, NY-open short −3.97,
  W%R>−20 short +1.13 only. Shorts must come from D1/H4 extremes, never H1-only.
- **Chasing extension LONG**: ADX>25 & EMA20>50 long negative all TFs (−1.21/−3.42/−3.27).
  Longs only from compression/dip, never from extension.
- D1 turn-of-month long −2.52, January long −2.28, BB-expanding long −2.40.
- H1/H4 calm-SHORT mirrors (−3.50/−4.54): calm = long-only signal.

## Costs & scale
Spot 160.56 (2026-06-11). D1 ATR14 p25/med/p75 = 63/86/118 pips (now 42 — deep calm,
squeeze-long regime active). H4 = 25/40/54 pips (now 14). Exness spread ~1–2 JPY pips
≈ 4–8% of median H4 ATR — better cost ratio than CHF.

## MoF intervention regime (spot is IN it)
2022/2024 MoF interventions at 152–162: violent 300–500 pip USDJPY slams within hours.
Spot 160.5 = inside the historic intervention band. LONG zones near/above 158 with fresh
multi-decade highs → conviction cap MEDIUM, no-chase; BoJ decision days (~8/yr) +
explicit MoF jawboning = hard block. V1b useless on intervention days (gap-through).

## Cross-pair macro map (6 FX scans)
- DXY 1d jump gate: EUR/GBP only.
- VIX-level fade-USD: commodity FX only (AUD/NZD/CAD).
- **DXY 20d slope: USD-base havens (CHF t≈2.3, JPY t≈2.2).**
- VIX washout: havens (CHF, JPY).
- London-open USD drift: AUD/NZD/CAD/CHF — **NOT JPY (NY drift instead, t=4.7)**.
- Mean-reversion fade template: all prior FX — **NOT JPY long side (drift/momentum)**.
