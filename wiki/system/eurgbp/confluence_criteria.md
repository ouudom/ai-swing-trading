---
type: system
updated: 2026-06-09
confidence: medium
tags: [confluence, zone, entry, scoring, eurgbp, cross, mean-reversion]
related: [constitution, eurgbp_profile, currency_exposure, ../../research/eurgbp/signal-results]
---

# EURGBP — Zone & Entry Confluence Scoring (ACTIVE)

> **STATUS: ACTIVE — 2026-06-09.** Derived from `wiki/research/eurgbp/signal-results.md`
> (EG3 D1 16yr + H4/H1 2020→now). Same two-score shape as the USD-majors, but **macro demoted to a
> 0.5 tilt** (EG2: cross macro thin/dead) and **NO VIX veto** (inverted risk-off polarity). H1/H4
> oscillator rows **validated** on real intraday (H1 t up to 7.45, both directions). Sizing in USD,
> no GBP convert (operator). All EURGBP orders route through the netting ledger ([[currency_exposure]]).

## Headline research constraint — MEAN-REVERTING, MACRO-LIGHT, NO USD LEG

**EURGBP is MEAN-REVERTING** (EG3, same DNA as the majors). Fade extremes; never pro-trend.
Unlike the majors there are **no momentum exceptions** — macro carries no significant edge on a
cross (EG2). Anti-edges (never score):
- Donchian20 breakdown short (−13.7pp, t=−4.24) — it's a long-side fade zone
- Near-20d-LOW used as a SHORT (−9.2pp, t=−4.53) — long-side fade
- PSAR / EMA-regime / ROC / Supertrend continuation (all negative t)

Core edge: **buy 20d-low / oversold, sell 20d-high / overbought.** Structure = the fade point.
Long (oversold-fade) is the richer side on this range-bound cross.

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence (EG3 D1, 16yr) |
|---|---|---|---|---|
| Z1 | **Structural Zone (D1 extreme)** | **3.0** | Zone at 20d/swing HIGH (short) or LOW (long), D1/W1 S/R. **MANDATORY.** | Near 20d LOW long +9.3pp t=4.61 |
| Z2 | **Oscillator Extreme (D1)** | **2.5** | D1 RSI<35/<30 or Stoch<20 or CCI<−100 or Keltner-low (long); RSI>65 / CCI>+100 (short) | RSI<30 long +16.7 t=3.32; Keltner-low +11.9 t=4.51; CCI<−100 +9.8 t=4.32 |
| Z3 | **H1 Oscillator Confirm** | **1.5** | H1 RSI<35/<30 or Stoch<20 (long); RSI>65 / Stoch>80 (short) | RSI<30 long +7.7 t=6.47; %R<−80 long t=7.42; RSI>65 short t=3.42 |
| Z4 | **Macro / Sentiment Tilt** | **0.5** | EUR−GBP rate diff 5d widening → long, AND/OR VIX 1d spike>3 → long. **Tilt only.** | X3 long +7.5pp t=1.50; E16 long +6.7pp t=1.68 (both sub-significant) |
| Z5 | **Non-Trend Gate (ADX<25)** | **1.0** | D1 ADX(14) < 25 | trend-follow anti-edge (Donchian breakdown −13.7 t=−4.24) |
| Z6 | **Band / Compression (H4/D1)** | **0.5** | Keltner touch, D1 ATR<20-med, BB squeeze | mild timing edge |
| Z7 | **Williams / Stoch secondary confirm** | **1.0** | Williams%R<−80 (long) / >−20 (short), or Stoch K<20/>80 on fade side | %R<−80 long +5.4 t=3.52; %R>−20 short +3.9 t=2.22 |
| | **Total** | **10.0** | | |

**0-point vetoes:** D1 ADX>30 trending against the fade → block. **NO VIX veto** (risk-off favors
EURGBP UP — inverted vs majors). **NO DXY block** (USD index irrelevant to the cross).
**Floor:** 5.0/10. Z1 mandatory.
**Macro is NOT a gate** (EG2 dead) — scored only as the Z4 0.5 tilt. The ~1.5 pts freed vs the
majors' macro weighting were redistributed to structure (Z1 2.5→3.0) + oscillator (Z2 2.0→2.5).

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | At zone, 1H close: **PRIMARY pin/engulf** toward fade · 2nd band-reclaim / close-strength · 15M CHoCH AGAINST approach | pin wins backtest (avgR +0.143); RSI-reclaim weak here (+0.053). PENDING live validation (D027) |
| E1 | **D1 Oscillator Still Extreme** | **2.5** | D1 RSI/Stoch/CCI still beyond fade threshold | strongest live gate |
| E2 | **H1 Oscillator Extreme Today** | **1.5** | H1 RSI<30/>65 or Stoch<20/>80 on the fade side | H1 oscillators highly significant both sides (t up to 7.45) |
| E3 | **Still Non-Trending (ADX<25)** | **1.0** | D1 ADX<25 | |
| E4 | **Structure / Band Intact** | **1.0** | 20d extreme / band not broken on D1 close | |
| E5 | **Compression Holds** | **1.0** | D1 ATR<20-med | |
| | **Total** | **10.0** | | |

**Sizing reminder:** EURGBP lots = `$2000 / (SL_price × 100000)` — USD-sized like the majors, no
GBP convert (operator decision; see [[eurgbp_profile]]). **Netting:** route every order through
`scripts/fx_exposure.py` — EURGBP IS the cross axis (see [[currency_exposure]]).

**Invalidation:** D1 CLOSE beyond the zone in the fade-against direction = dead (became a
breakout/trend). V1b = 2 consecutive H4 closes >4 pips past zone.

**Output per zone:** ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.

## Status notes
- ✅ H4/H1 pulled + validated (2020→now): Z3/E2 H1 oscillator edges confirmed, both directions.
- ✅ EG5 wiring done (`/weekly`+`/validate` params, forecast dirs, netting gate).
- Short-side fades: D1 short signals are thinner — lean on **intraday** (H1/H4) oscillator extremes
  for the short E0/E2 trigger.
- COT (derived 6E vs 6B) remains context-only, not built — optional future enhancement.
