---
type: system
updated: 2026-06-09
confidence: high
tags: [confluence, zone, entry, scoring, eurusd, mean-reversion]
related: [constitution, eurusd_profile, ../../research/eurusd/signal-results]
---

# EURUSD — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — operator-approved 2026-06-09 (D021).**
> Derived from measured edges in `wiki/research/eurusd/signal-results.md` (16yr D1 scan,
> `scripts/backtest_signals.py`). Two scores, same shape as XAUUSD:
> - **Zone Confluence** — at `/weekly`, rates a candidate FADE zone. Max 10, floor 5.
> - **Entry Confluence** — at `/validate`, rates whether today justifies the order. Max 10, floor 5.

## Headline research constraint — INVERSE OF GOLD

**EURUSD is MEAN-REVERTING.** Fade extremes; never pro-trend. **Two exceptions are MOMENTUM
gates** (intermarket, not the pair's own price): DXY 1d jump→short, VIX spike→short — these
follow through. Measured anti-edges that must NEVER score (all |t|>2.5):
- ADX>25 + EMA20>50 trend-follow long (−6.6pp, t=−5.17) — trend-following fails
- Aroon / Supertrend / PSAR / EMA-regime continuation — all negative
- Donchian breakout as continuation — negative
- Big-figure proximity used as a SHORT (−6.4pp) — it's a long-side magnet

Structural levels are FADE points (price reverses there), the opposite of gold's breakout behaviour.
Best signal frame = **H4**.

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

Scores each candidate fade zone (price reverts at a D1/W1 level). Max 3 zones/week.

| # | Signal | Weight | Pass when | Evidence (16yr D1 / H4) |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (20d/swing H/L, role-reversal, round#). Draw box. **MANDATORY.** | Near 20d HIGH→short +10.1pp t=3.58; 20d LOW→long +5.9pp t=2.28 |
| Z2 | **Oscillator Extreme (H4)** | **2.0** | H4 RSI>65 (short) / RSI<35 (long), or Stoch>80/<20, CCI±100, Williams toward fade | RSI>70 short +10.0pp t=4.66; RSI>65 +5.5pp t=3.82; CCI +4.0pp t=2.84 |
| Z3 | **Band Over-Extension (H4)** | **1.5** | Close beyond Keltner(20,1.5) or BB(20,2) on fade side | Keltner high short +4.3pp t=3.12; BB upper short +4.5pp t=2.10 |
| Z4 | **Big-Figure Proximity** | **1.0** | Zone within ~15 pips of x.xx00 / x.xx50 (LONG side) | +3.6pp H4 t=3.90; +6.4pp D1 |
| Z5 | **Macro / Intermarket Gate** | **1.5** | DXY 1d jump>0.5 aligns SHORT, AND/OR US2Y(DGS2) 20d slope toward zone (slope<0=long), AND/OR VIX 1d spike>3 → short bias | **DXY jump short +23.0pp t=9.29** (dominant); US2Y slope<0 long +2.3pp t=2.06; VIX spike→short |
| Z6 | **Non-Trend Gate (ADX<25)** | **1.0** | D1 ADX(14) < 25 (range regime — fades work) | trend-follow anti-edge (ADX+EMA long −6.6pp t=−5.17) needs non-trend |
| Z7 | **Compression / Squeeze (H4)** | **1.0** | TTM squeeze on, BB bw at 20-low, or D1 ATR<20-med | TTM long +4.2pp t=2.16 |
| | **Total** | **10.0** | | |

**0-point vetoes (hard risk only):**
- D1 ADX>30 AND trending against the fade → block the zone (don't fade a strong trend).
- **DXY 1d jump>0.5 AGAINST the zone** → block (strongest measured momentum, t=9.29).
- VIX>30 OR VIX 1d spike>3 → block LONG EUR zones (risk-off USD bid drives EUR down).

**Floor:** 5.0/10 to publish PENDING. Z1 mandatory.

**Macro scored as Z5** (16yr sample): scoreable = DXY 1d jump→short (dominant), US2Y slope,
VIX spike→short. **NOT** the rate-DIFFERENTIAL / policy-carry slope / 2s10s curve — those stay
measured-DEAD even at 16yr (t<0.3). The P2 snapshot still *reports* carry/policy-diff as context.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone, 1H close: **PRIMARY RSI-reclaim** (RSI back through 35/65 toward fade) · 2nd band-reclaim (Keltner re-entry) · fallback pin/engulf / 15M CHoCH AGAINST approach | reclaim > pin (avgR +0.143 vs +0.021); pin retained. PENDING live validation (D027) |
| E1 | **H4 Oscillator Still Extreme** | **2.5** | H4 RSI/Stoch still beyond fade threshold today | strongest live signal |
| E2 | **Band Touch Today (H4)** | **1.5** | Price tagged Keltner/BB band on fade side today | live over-extension |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 holds | regime guard |
| E4 | **Compression Holds** | **1.0** | D1 ATR<20-med, or squeeze still on | |
| E5 | **Big-Figure / Structure Intact** | **1.0** | Zone level not broken on D1 close | invalidation guard |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond the zone in the fade-against direction = zone dead (mean-reversion
thesis broken → it became a breakout). This is the key FX risk: fades fail when they turn into trends.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
