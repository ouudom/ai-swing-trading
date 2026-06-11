---
type: system
updated: 2026-06-11
confidence: high
tags: [eurjpy, confluence, scoring, zones]
related: [eurjpy_profile, signal-results, constitution]
---

# EURJPY — Zone Confluence (R1) + Entry Confluence (R2) — ACTIVE

**Symmetric mean-reversion system on a long-drift floor** — both directions score the
same fade/washout logic; NO macro criterion (macro fully dead — first 100% price-driven
pair). Counter = SHORT (against D1 LNG 55.6% baseline): win-rate edge only, near-zero
avg run — take profits early. Evidence: [[signal-results]].
Max 10, floor 5.0, ≤3 zones/wk, ≤1 counter.

## R1 — Zone Confluence (weekly)
| # | Criterion | Wt | Evidence (t) |
|---|---|---|---|
| Z1 | Structural S/R zone (D1/H4 level, prior reaction) | 2.0 **MAND** | — |
| Z2 | **Extreme engine** — LONG: zone at washout (D1 Stoch<20 / H1 Keltner-low / near 20d low) · SHORT: zone at extension (D1/H4 Keltner-high / RSI>65–70) | 2.5 | 3.10/2.62/3.07 · 3.36/3.48/2.98 |
| Z3 | Calm/compression regime — H4 ATR pctile<0.2 or TTM squeeze on (LONG +full; SHORT half — calm favors longs) | 1.5 | D6 3.96, B11 2.71 |
| Z4 | Oscillator stack confirms zone side (CCI ±100 / Stoch / W%R aligned on H4) | 1.5 | A12 2.55, A11 2.36 |
| Z5 | D1 trigger pattern toward zone (inside-bar break / compression bar) | 1.0 | D5 2.18, D1 2.18 |
| Z6 | Big-figure confluence (x.00 within 20 pips) | 1.0 | structural anchor |
| Z7 | Not extended: ADX<25 or zone is a pullback, not extension chase | 0.5 | C26 anti −4.24 |

**Vetoes / caps**
- **BoJ decision day, active MoF jawboning, or ECB decision day → HARD BLOCK.**
- **LONG zone at fresh record highs during intervention watch → conviction cap MEDIUM**
  (spot 185+ regime; MoF slams hit crosses).
- Never publish a breakout/continuation zone (Donchian-up H1 −2.61, C26 −4.0/−4.2,
  momentum shorts C2 −3.3) — zones are REVERSION zones only, both sides.
- Turn-of-month (day ≥26) LONG zones → −0.5 (G9 −3.10).
- NO VIX veto, NO VIX score (dead). NO macro gate of any kind.

## R2 — Entry Confluence (daily, per zone)
| # | Criterion | Wt |
|---|---|---|
| E0 | Confirmation candle (1H engulf / 1H pin tail≥2.5×body / 15M CHoCH) toward zone dir, on close | 3.0 |
| E1 | Extreme still live — LONG: washout readings still present (Stoch/W%R/Keltner) · SHORT: H1/H4 still overbought (W%R>−20 t=4.21, RSI>65) | 2.5 |
| E2 | Session window — LONG: NY/London overlap 12–16 UTC · SHORT: London open 07–09 UTC | 1.5 |
| E3 | Calm regime intact (H4 ATR pctile<0.2 / squeeze on) — LONG full, SHORT 0.5 | 1.0 |
| E4 | Zone structure intact (no D1 close through zone) | 1.0 |
| E5 | Not extended at entry (ADX<25 or pullback entry, not breakout chase) | 1.0 |

Floor 5.0. E0 absent → no order (anchor rules in constitution).

## V1b (intraday invalidation)
2 consecutive H4 closes **>0.04 (4 JPY pips)** past zone extreme → invalidate, cancel limit.
`bash scripts/pyrun.sh scripts/check_v1b.py --instrument eurjpy --direction LONG --zone-top 184.50 --zone-bottom 184.00 --buffer 0.04`
⚠ Intervention days gap through V1b — BoJ/MoF hard block exists precisely for this.
