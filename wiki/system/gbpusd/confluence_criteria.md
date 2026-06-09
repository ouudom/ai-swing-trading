---
type: system
updated: 2026-06-09
confidence: high
tags: [confluence, zone, entry, scoring, gbpusd, mean-reversion]
related: [constitution, gbpusd_profile, ../../research/gbpusd/signal-results]
---

# GBPUSD — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — operator-approved 2026-06-09 (D021).**
> Derived from `wiki/research/gbpusd/signal-results.md` (16yr D1 scan, `scripts/backtest_signals.py`).
> Same two-score shape as XAUUSD. GBP is mean-reverting like [[../eurusd/confluence_criteria|EURUSD]]
> but its cleanest swing edges sit on **D1 reversal + H1 oscillators** (EUR's concentrate on H4).

## Headline research constraint — INVERSE OF GOLD

**GBPUSD is MEAN-REVERTING.** Fade extremes; never pro-trend. **Two MOMENTUM exceptions**
(intermarket): DXY 1d jump→short, VIX spike→short — both follow through hard on GBP. Anti-edges
(never score):
- ADX>25 + EMA20>50 trend-follow long (−8.2pp D1 t=−2.38; −4.9pp H4 t=−3.61)
- EMA-regime / Supertrend / PSAR continuation (H1 all t<−2.6)
- Near-20d-LOW used as a SHORT (−17.9pp, t=−3.02) — it's a long-side fade

Core edge: **buy 20d-low / oversold, sell 20d-high / overbought.** Structure = fade point.

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (16yr D1 / H1) |
|---|---|---|---|---|
| Z1 | **Structural Zone (D1 extreme)** | **2.5** | Zone at 20d/swing HIGH (short) or LOW (long), D1/W1 S/R. **MANDATORY.** | Near 20d LOW long +13.8pp t=4.61; 20d HIGH short +7.2pp t=2.72 |
| Z2 | **Oscillator Extreme (D1)** | **2.0** | D1 RSI>65 (short) / RSI<35 or Stoch<20 (long), or Keltner-high short | RSI>65 short +12.5pp t=4.88; RSI>70 +19pp t=4.49; Keltner-high short +10.3pp t=4.16 |
| Z3 | **H1 Oscillator Confirm** | **1.5** | H1 RSI<35/<30 or Stoch<20 (long); RSI>65 (short) | H1 RSI<35 long +3.0pp t=4.07; RSI>65 short +2.7pp t=3.84 |
| Z4 | **Macro / Intermarket Gate** | **1.5** | DXY 1d jump>0.5 aligns SHORT, AND/OR US2Y(DGS2) 20d slope toward zone, AND/OR VIX 1d spike>3 → short bias | **DXY jump short +18.0pp t=7.27**; US2Y slope long +2.7pp t=2.39 / short +2.3pp t=2.15 |
| Z5 | **Non-Trend Gate (ADX<25)** | **1.0** | D1 ADX(14) < 25 | trend-follow anti-edge (ADX+EMA long −12.0pp t=−5.62) |
| Z6 | **Band / Compression (H4/D1)** | **0.5** | Keltner touch, D1 ATR<20-med, or BB squeeze | mild timing edge |
| Z7 | **Seasonal / Williams Confirm** | **1.0** | September (short, +11.1pp t=2.06) OR Williams%R (<−80 long / >−20 short) | |
| | **Total** | **10.0** | | |

**0-point vetoes:** D1 ADX>30 trending against fade → block. **DXY 1d jump>0.5 against the zone → block.**
VIX>30 OR VIX 1d spike>3 → block LONG GBP (risk-off → GBP crashes, spike→long tested −22pp t=−5.60).
**Floor:** 5.0/10. Z1 mandatory.
**Macro scored as Z4** (16yr): DXY jump→short, US2Y slope, VIX spike→short. **NOT** carry-diff /
2s10s (dead, t<0.3). Snapshot still reports policy diff as context.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone: H1 reversal pin (tail≥2.5×body) / engulfing / 15M CHoCH turning AGAINST the approach, on close | reversal trigger |
| E1 | **D1 Oscillator Still Extreme** | **2.5** | D1 RSI/Stoch still beyond fade threshold | strongest live GBP gate |
| E2 | **H1 Oscillator Extreme Today** | **1.5** | H1 RSI<30/>65 or Stoch<20/>80 on the fade side | H1 edges high-N, high-t |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 | |
| E4 | **Structure / Band Intact** | **1.0** | 20d extreme / band not broken on D1 close | |
| E5 | **Compression Holds** | **1.0** | D1 ATR<20-med | |
| | **Total** | **10.0** | | |

**Invalidation:** D1 CLOSE beyond the zone in the fade-against direction = dead (became a breakout/trend).

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.
