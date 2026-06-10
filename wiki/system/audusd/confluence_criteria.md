---
type: system
updated: 2026-06-10
confidence: high
tags: [confluence, zone, entry, scoring, audusd, mean-reversion]
related: [constitution, audusd_profile, ../../research/audusd/signal-results]
---

# AUDUSD — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — D024 pair #1 (2026-06-10).**
> Derived from measured edges in `wiki/research/audusd/signal-results.md` (D1/H4 16yr,
> H1 2020→now). Two scores, same shape as the other instruments:
> - **Zone Confluence** — at `/weekly`, rates a candidate FADE zone. Max 10, floor 5.
> - **Entry Confluence** — at `/validate`, rates whether today justifies the order. Max 10, floor 5.

## Headline research constraints

**AUDUSD is MEAN-REVERTING, H4-centric** (EURUSD family). Fade extremes; never pro-trend.
Measured anti-edges that must NEVER score: Donchian breakout (H1 −4.8pp t=−4.84), Supertrend /
Aroon / PSAR / EMA-regime continuation (t −2 to −4.4), ADX+EMA trend-follow.

**Differences vs EURUSD — do not copy its gates blindly:**
- **DXY 1d jump is DEAD** for AUD (t=−0.85). No DXY score, no DXY veto.
- **VIX polarity INVERTED:** VIX>20 favors LONG (+8.7pp t=6.14), VIX<15 favors SHORT (t=5.29).
  **The FX VIX-veto-LONGS rule does NOT apply to AUDUSD.** VIX spike (1d>3) is dead.
- **D1 oscillator fades are thin** (RSI<35 t=−0.71) — D1 contributes regime only; the fade
  evidence lives on H4 (both sides) and H1 (short side).

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (16yr D1/H4, H1 2020→) |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (20d/swing H/L, role-reversal, round#). Draw box. **MANDATORY.** | H4 near-20d-HIGH short +2.8 t=2.65; 20d-LOW long +2.4 t=2.11 |
| Z2 | **Oscillator Extreme (H4)** | **2.0** | H4 RSI<35 (long) / RSI>65 (short), CCI±100, Stoch>80/<20 toward fade | RSI<35 long +5.2 t=3.41; CCI>+100 short +4.5 t=3.12; CCI<−100 long +4.0 t=2.71 |
| Z3 | **Band Over-Extension (H4)** | **1.5** | Close beyond Keltner(20,1.5) or BB(20,2) on fade side | Keltner-low long +5.0 t=3.52; BB-lower long +6.3 t=2.80 |
| Z4 | **Big-Figure Proximity (LONG)** | **0.5** | Zone within ~15 pips of x.xx00/x.xx50, LONG side | H1 +1.3pp t=2.85 (long-side magnet) |
| Z5 | **Macro Regime Tilt** | **1.5** | VIX>20 aligns LONG / VIX<15 aligns SHORT (1.0); US2Y 20d slope toward zone (slope<0=long) (0.5) | VIX>20 long t=6.14; VIX<15 short t=5.29; US2Y slope t≈2.2 |
| Z6 | **Non-Trend Gate (ADX<25)** | **1.5** | D1 ADX(14) < 25 (range regime — fades work) | trend-follow = anti-edge across TFs |
| Z7 | **Compression / Squeeze** | **1.0** | D1 BB squeeze (bw 20-low) or ATR<20-med | D1 squeeze long +4.8 t=2.54 |
| | **Total** | **10.0** | | |

**0-point vetoes (hard risk only):**
- D1 ADX>30 AND trending against the fade → block the zone.
- **NO VIX veto** (polarity inverted — VIX level scores in Z5 instead).
- **NO DXY veto** (signal dead for AUD).

**Floor:** 5.0/10 to publish PENDING. Z1 mandatory.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone: H1 reversal pin (tail≥2.5×body) / engulfing / 15M CHoCH AGAINST the approach, confirmed on close | reversal trigger at extreme |
| E1 | **H4 Oscillator Still Extreme** | **2.5** | H4 RSI/CCI/Stoch still beyond fade threshold today | strongest live frame |
| E2 | **H1 Oscillator Extreme (short) / Band Touch (H4)** | **1.5** | SHORT: H1 RSI>65 / CCI>+100 / Keltner-high today (H1 t 5.2–6.5). LONG: H4 band tag on fade side | H1 short-side machine; H4 bands |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 holds | regime guard |
| E4 | **Macro Regime Still Aligned** | **1.0** | VIX level + US2Y slope (Z5 logic) still toward the zone today | regime tilt |
| E5 | **Structure Intact** | **1.0** | Zone level not broken on D1 close | invalidation guard |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond the zone in the fade-against direction = zone dead
(mean-reversion became breakout). V1b: 2 consecutive H4 closes >4 pips past zone.

**Session note:** London open 07–09 UTC has an H1 SHORT drift (t=2.67) — best window for
short-side fades; be slower to chase longs there.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
