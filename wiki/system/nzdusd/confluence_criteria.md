---
type: system
updated: 2026-06-10
confidence: medium
tags: [confluence, zone, entry, scoring, nzdusd, mean-reversion]
related: [constitution, nzdusd_profile, ../../research/nzdusd/signal-results]
---

# NZDUSD — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — D024 pair #2 (2026-06-10).**
> Derived from `wiki/research/nzdusd/signal-results.md` (D1/H4 16yr, H1 2020→now).
> - **Zone Confluence** — at `/weekly`, rates a candidate FADE zone. Max 10, floor 5.
> - **Entry Confluence** — at `/validate`, rates whether today justifies the order. Max 10, floor 5.

## Headline research constraints

**NZDUSD is MEAN-REVERTING but MARGINAL — the weakest USD-major edge set (≈half of AUD's).**
Floor 5.0 will be reached less often; publishing fewer/no NZD zones in a week is correct behaviour.
Never pro-trend (Supertrend/Aroon/EMA-regime anti-edge, t to −3.4).

**Macro is nearly all DEAD — do not import other pairs' gates:**
- **US2Y slope DEAD** (t=−0.7; scored for EUR/GBP/AUD — not here).
- **DXY 1d jump DEAD** (t=0.24). No score, no block.
- **VIX polarity INVERTED, weak:** VIX>20 → LONG tilt (t=2.18), VIX<15 → SHORT tilt (t=2.38).
  **NO VIX-veto.** VIX spike dead.
- NZDUSD = price/structure + weak VIX tilt (macro-light, EURGBP-style).

**Distinct NZD flavor:** squeeze/compression is the strongest single signal (H4 TTM t=3.25,
D1 BB squeeze t=2.35) and big-figure is a LONG magnet (H4 t=2.77, short side anti-edge −2.68).

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (16yr D1/H4, H1 2020→) |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (20d/swing H/L, role-reversal, round#). Draw box. **MANDATORY.** | H1 near-20d-HIGH short t=3.09 / LOW long t=2.02; H4 ≈1.9 |
| Z2 | **Oscillator Extreme (H4)** | **2.0** | H4 CCI±100, RSI2>90/<10, RSI>65/<35, Stoch toward fade | CCI>+100 short +3.7 t=2.51; RSI2>90 short +6.9 t=2.41; CCI<−100 long t=2.03 |
| Z3 | **Compression / Squeeze** | **2.0** | H4 TTM squeeze on, or D1 BB squeeze (bw 20-low) | **strongest NZD signal**: H4 TTM long +4.8 t=3.25; D1 squeeze t≈2.2–2.35 |
| Z4 | **Band Over-Extension (H4)** | **1.5** | Close beyond Keltner(20,1.5)/BB(20,2) on fade side | Keltner-high short / low long ≈+2.8 t≈2.05 |
| Z5 | **Big-Figure Proximity (LONG)** | **1.0** | Zone within ~15 pips of x.xx00/x.xx50, LONG side only | H4 +2.6 t=2.77 (short side = anti-edge −2.68) |
| Z6 | **Non-Trend Gate (ADX<25)** | **1.0** | D1 ADX(14) < 25 | trend-follow anti-edge across TFs |
| Z7 | **VIX Regime Tilt (weak)** | **0.5** | VIX>20 aligns LONG / VIX<15 aligns SHORT | t=2.18/2.38 (weak — half-point only) |
| | **Total** | **10.0** | | |

**0-point vetoes (hard risk only):**
- D1 ADX>30 AND trending against the fade → block the zone.
- **NO VIX veto, NO DXY block, NO US2Y gate** (all dead/inverted for NZD).

**Floor:** 5.0/10 to publish PENDING. Z1 mandatory.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone: H1 reversal pin (tail≥2.5×body) / engulfing / 15M CHoCH AGAINST the approach, confirmed on close | H4 bullish pin itself scans +3.0 t=2.40 |
| E1 | **H4 Oscillator Still Extreme** | **2.5** | H4 CCI/RSI2/RSI/Stoch still beyond fade threshold today | core fade frame |
| E2 | **H1 Oscillator Extreme (short) / Band Touch (long)** | **1.5** | SHORT: H1 Stoch>80/W%R/Keltner-high today (t≈2.9–3.0). LONG: H4 band tag on fade side | H1 short-side rows |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 holds | regime guard |
| E4 | **Squeeze / Compression Holds** | **1.0** | H4 TTM or D1 BB squeeze still on | NZD's strongest signal, re-checked live |
| E5 | **Structure Intact** | **1.0** | Zone level not broken on D1 close | invalidation guard |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond zone against the fade = dead. V1b: 2 consecutive H4 closes
>4 pips past zone.

**Session notes:** London open 07–09 H1 SHORT drift (t=2.12). NZ data lands 21:45–02:00 UTC in
thin liquidity — never hold a fresh limit through RBNZ/CPI (hard block).

**Antipodean gate (advisory):** if AUDUSD has a live same-direction order/limit, fx_exposure
flags it — AUD edge ≈ 2× NZD; default keep AUD unless NZD's EC is clearly higher.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
