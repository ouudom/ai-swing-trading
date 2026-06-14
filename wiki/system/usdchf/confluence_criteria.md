---
type: system
updated: 2026-06-10
confidence: medium
tags: [confluence, zone, entry, scoring, usdchf, mean-reversion, usd-base]
related: [constitution, usdchf_profile, ../../research/usdchf/signal-results]
---

# USDCHF — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — D024 pair #4 (2026-06-10). Second USD-base pair.**
> Derived from `wiki/research/usdchf/signal-results.md` (D1/H4 16yr, H1 2020→now).
> - **Zone Confluence** — at `/weekly`, rates a candidate FADE zone. Max 10, floor 5.
> - **Entry Confluence** — at `/validate`, rates whether today justifies the order. Max 10, floor 5.

## Headline research constraints

**USDCHF is MEAN-REVERTING — fade extremes; never pro-trend** (H1 momentum continuation all
anti-edge: Close>EMA20 long −2.72, NR7-long −3.35; H4 downtrend-continuation short −3.05).
**H1 is the evidence-rich TF** (short-side fades t 4.5–5.5); **H4 is thin** — zones anchor on
D1 structure + H1 oscillators, not H4 oscillators.

**USD-BASE polarity + pair-specific macro:**
1. Long USDCHF = LONG USD. **DXY 20d slope is the live macro** (rising → LONG t=2.32,
   falling → SHORT t=2.34) — only pair beyond EUR/GBP majors where DXY scores.
2. **VIX: NO gate, NO score** — haven-vs-haven washout. (Differs from AUD/NZD/CAD.)
3. US2Y slope flipped, weak tilt (t≈1.4) — half-point inside Z3 at most.
4. COT 6S reads INVERTED (spec long CHF = short USDCHF). DXY 1d jump = no block (anti, fade it).
5. **SNB regime:** short zones near multi-year lows (~0.78–0.80) fight the SNB → conviction
   cap MEDIUM; any SNB communication day = HARD block (see profile).

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (16yr D1/H4, H1 2020→) |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (20d/swing H/L, role-reversal). Draw box. **MANDATORY.** | H1 near-20d-LOW long t=2.92 |
| Z2 | **H1 Oscillator Extreme Cluster** | **2.0** | SHORT: H1 W%R>−20 / RSI>65 / Keltner-high / Stoch>80 (t 4.0–5.5). LONG: H1 W%R<−80 / RSI2<10 (t≈2.2), D1 W%R<−80 (t=2.22) | **strongest signals on the pair** |
| Z3 | **DXY 20d Slope Aligned** | **2.0** | DXY slope toward zone direction (rising=long, falling=short); +US2Y slope same way adds conviction note | +4.9pp t=2.3 both sides |
| Z4 | **Compression / Squeeze** | **1.5** | H1 TTM squeeze-on or ATR pctile<0.2 (calm) for LONG zones; H4 squeeze context | TTM long t=3.20; calm long t=3.03 |
| Z5 | **D1 Pattern / Extreme** | **1.0** | D1 bearish engulfing (short, t=2.14) or D1 oversold W%R (long); MACD-down (short, t=1.97) | D1 frame |
| Z6 | **H4 Band / Big-Figure** | **1.0** | H4 close beyond BB(20,2) on fade side (short t=1.92) or near x.xx00 big-figure for LONG (t=2.02) | H4 thin — capped at 1.0 |
| Z7 | **Non-Trend Gate (ADX<25)** | **0.5** | D1 ADX(14) < 25 | continuation anti-edge |
| | **Total** | **10.0** | | |

**0-point vetoes (hard risk only):**
- D1 ADX>30 AND trending against the fade → block the zone.
- SNB decision/communication day → block (quarterly: Mar/Jun/Sep/Dec Thu 08:30 UTC).
- **NO VIX veto/score, NO DXY-jump block** (VIX washout; DXY scores via slope in Z3 only).
- SHORT zone inside 0.78–0.80 historic-low band → conviction cap MEDIUM (SNB).

**Floor:** 5.0/10 to publish PENDING. Z1 mandatory.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone, 1H close: **PRIMARY RSI-reclaim** (35/65) · 2nd pin/engulf · 15M CHoCH AGAINST approach. **Avoid band-reclaim** (−0.003 here) | reclaim > pin (avgR +0.105 vs +0.087). PENDING live validation (D027) |
| E1 | **H1 Oscillator Still Extreme** | **2.5** | SHORT: W%R>−20/RSI>65/Keltner-high holds today (t 4.5–5.5). LONG: W%R<−80/RSI2<10 | core frame |
| E2 | **DXY Slope Aligned** | **1.5** | DXY 20d slope still toward zone | t=2.3 |
| E3 | **Squeeze / Calm Context** | **1.0** | H1 TTM squeeze-on or calm ATR pctile (esp. LONG) | t=3.2/3.0 |
| E4 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 holds | regime guard |
| E5 | **Structure Intact** | **1.0** | Zone level not broken on D1 close | invalidation guard |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond zone against the fade = dead. V1b: 2 consecutive H4 closes
>4 pips past zone.

**Session notes:** London open 07–09 UTC = H1 LONG drift (t=2.70) — best long-fade window.
US data (12:30–14:00 UTC) dominates the calendar; SNB days are rare but absolute blocks.
Overbought SHORT fades = the pair's best intraday stats — prefer them when DXY slope agrees.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
