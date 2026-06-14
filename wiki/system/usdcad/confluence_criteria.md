---
type: system
updated: 2026-06-10
confidence: medium
tags: [confluence, zone, entry, scoring, usdcad, mean-reversion, usd-base]
related: [constitution, usdcad_profile, ../../research/usdcad/signal-results]
---

# USDCAD — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — D024 pair #3 (2026-06-10). FIRST USD-BASE PAIR.**
> Derived from `wiki/research/usdcad/signal-results.md` (D1/H4 16yr, H1 2020→now).
> - **Zone Confluence** — at `/weekly`, rates a candidate FADE zone. Max 10, floor 5.
> - **Entry Confluence** — at `/validate`, rates whether today justifies the order. Max 10, floor 5.

## Headline research constraints

**USDCAD is MEAN-REVERTING — fade extremes on H4/H1; never pro-trend** (bearish-engulf
continuation t=−3.83, Donchian breakdown −2.83, EMA/Aroon-regime anti-edge).

**USD-BASE polarity — three rules that flip vs the majors:**
1. Long USDCAD = LONG USD. US2Y slope RISING is *bullish* the pair (t=1.97/2.10, small).
2. **VIX>20 → SHORT bias** (+5.5pp t≈3.9); VIX<15 → LONG bias (t≈3.0). Same fade-the-USD
   regime as AUD/NZD, opposite sign in this quote. **NO VIX veto.**
3. COT 6C reads INVERTED (spec long CAD = short USDCAD); DXY-jump is DEAD (no score/block).

**🛢 Oil:** only WTI 5d>+5% → SHORT tilt (t=1.67, sub-sig, ~1wk data lag). Half-point max.

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (16yr D1/H4, H1 2020→) |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (20d/swing H/L, role-reversal). Draw box. **MANDATORY.** | H4 near-20d-LOW long +2.3 t=2.69 |
| Z2 | **Oscillator Extreme (H4)** | **2.0** | H4 Stoch<20/CCI<−100 (long), CCI>+100/Stoch>80 (short), RSI extremes toward fade | Stoch<20 long t=2.53; CCI>+100 short t=2.49 |
| Z3 | **Band Over-Extension (H4)** | **2.0** | Close beyond BB(20,2)/Keltner(20,1.5) on fade side | **BB-upper short +6.9 t=3.19**; Keltner-low long t=2.03 |
| Z4 | **Compression / Squeeze** | **1.5** | H4 BB squeeze (bw 20-low) or calm ATR pctile | squeeze long +4.0 t=3.14 |
| Z5 | **VIX Regime (fade-USD)** | **1.0** | VIX>20 aligns SHORT / VIX<15 aligns LONG | t≈3.9 / 3.0 (inverted vs majors) |
| Z6 | **US2Y Slope (flipped) + Oil Tilt** | **1.0** | US2Y 20d slope toward zone (rising=long, 0.5); WTI 5d>+5% aligns SHORT (0.5) | t≈2.0 / 1.67 |
| Z7 | **Non-Trend Gate (ADX<25)** | **0.5** | D1 ADX(14) < 25 | continuation anti-edge |
| | **Total** | **10.0** | | |

**0-point vetoes (hard risk only):**
- D1 ADX>30 AND trending against the fade → block the zone.
- **NO VIX veto, NO DXY block** (VIX scores directionally in Z5; DXY dead).

**Floor:** 5.0/10 to publish PENDING. Z1 mandatory.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone, 1H close: **PRIMARY band-reclaim** (close re-enters Keltner) · 2nd micro-BOS / RSI-reclaim · fallback pin/engulf / 15M CHoCH AGAINST approach | band wins backtest here (avgR +0.107). PENDING live validation (D027) |
| E1 | **H4 Oscillator/Band Still Extreme** | **2.5** | H4 Stoch/CCI/BB still beyond fade threshold today | core frame (BB-upper short t=3.19) |
| E2 | **H1 Oscillator Extreme** | **1.5** | LONG: H1 W%R<−80 / CCI<−100 / RSI2<10 (t 2.9–3.45). SHORT: H1 CCI>+100 (t=3.08) | H1 long-side machine |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 holds | regime guard |
| E4 | **Macro Regime Aligned** | **1.0** | VIX level (fade-USD) + US2Y slope (flipped) toward zone | Z5/Z6 logic live |
| E5 | **Structure Intact** | **1.0** | Zone level not broken on D1 close | invalidation guard |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond zone against the fade = dead. V1b: 2 consecutive H4 closes
>5 pips past zone.

**Session notes:** London open 07–09 UTC = H1 LONG drift (t=2.92) — best window for long-side
fades into support. CAD data + oil action land NY session; never hold a fresh limit through
BoC/CAD-CPI/jobs (HARD) — and CAD jobs often shares the 12:30 UTC slot with US data.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
