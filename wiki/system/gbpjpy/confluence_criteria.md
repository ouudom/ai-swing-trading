---
type: system
updated: 2026-06-11
confidence: high
tags: [gbpjpy, confluence, scoring, zones]
related: [gbpjpy_profile, signal-results, constitution]
---

# GBPJPY — Zone Confluence (R1) + Entry Confluence (R2) — ACTIVE

**Extension-fade system, SHORT-side dominant, on the strongest long-drift floor**
(D1 LNG 56.7%). Both directions score fade/washout logic; NO calm row (engine dead —
only JPY pair without it); NO macro criterion (second 100% price-driven pair).
Counter = SHORT: win-rate edge only on H4/H1, near-zero avg run — take profits early
(D1 band shorts are the exception, +0.42%/trade). Evidence: [[signal-results]].
Max 10, floor 5.0, ≤3 zones/wk, ≤1 counter.

## R1 — Zone Confluence (weekly)
| # | Criterion | Wt | Evidence (t) |
|---|---|---|---|
| Z1 | Structural S/R zone (D1/H4 level, prior reaction) | 2.0 **MAND** | — |
| Z2 | **Extreme engine** — SHORT: zone at extension (D1/H4 Keltner-high / BB-upper / RSI>65 / CCI>+100) · LONG: zone at washout (D1/H4 Keltner-low / RSI<35 / CCI<−100 / near 20d low) | 2.5 | 4.64/4.01/3.44/3.69 · 2.33/2.43/2.18/2.56 |
| Z3 | Multi-TF extreme alignment — same-side extreme live on ≥2 of D1/H4/H1 | 1.5 | B10 4.64+4.01+2.42, A3 all TFs |
| Z4 | H4 oscillator stack confirms zone side (Stoch >80/<20, CCI ±100, W%R) | 1.5 | A7 3.80, A11 4.12, A9 3.09 |
| Z5 | H4 reversal trigger toward zone (MACD cross / rejection pin at zone) | 1.0 | C14 2.24 |
| Z6 | Big-figure confluence (x.00 within 25 pips) | 1.0 | structural anchor |
| Z7 | Not extended: ADX<25 or zone is a pullback, not extension chase | 0.5 | C26 anti −5.00 |

**Vetoes / caps**
- **BoJ decision day, active MoF jawboning, or BoE decision day → HARD BLOCK.**
- **LONG zone at fresh record highs during intervention watch → conviction cap MEDIUM**
  (spot 214+ regime; MoF slams hit GBPJPY hardest of the crosses).
- Never publish a breakout/continuation zone (C26 −5.00/−4.69, B1r band-break long
  −3.36, Donchian −1.9, momentum shorts C8 −3.75) — REVERSION zones only, both sides.
- Turn-of-month (day ≥26) LONG zones → −0.5 (G9 −2.99). January LONG: caution (G6 −2.28).
- NO VIX veto, NO VIX score, NO macro gate of any kind (all dead).
- NO calm/squeeze criterion — compression carries no signal here (D6 1.42, B11 −0.32).

## R2 — Entry Confluence (daily, per zone)
| # | Criterion | Wt |
|---|---|---|
| E0 | Confirmation candle (1H engulf / 1H pin tail≥2.5×body / 15M CHoCH) toward zone dir, on close | 3.0 |
| E1 | Extreme still live — SHORT: H4 still overbought (Stoch>80 t=3.80 / W%R>−20 / RSI>65) · LONG: washout readings still present (Keltner-low / RSI<35 / 20d low) | 2.5 |
| E2 | Session — LONG: NY/London overlap 12–16 UTC (t=4.20) = 1.5 · SHORT: outside 12–16 UTC = 0.75; **inside 13–15 UTC = 0 (anti −3.84)** | 1.5 |
| E3 | H1 timing structure (LONG: inside-bar break t=2.62 / near 20d low · SHORT: H1 RSI>65 t=2.59 / Keltner-high) | 1.0 |
| E4 | Zone structure intact (no D1 close through zone) | 1.0 |
| E5 | Not extended at entry (ADX<25 or pullback entry, not breakout chase) | 1.0 |

Floor 5.0. E0 absent → no order (anchor rules in constitution).

## V1b (intraday invalidation)
2 consecutive H4 closes **>0.05 (5 JPY pips)** past zone extreme → invalidate, cancel limit.
`bash scripts/pyrun.sh scripts/check_v1b.py --instrument gbpjpy --direction SHORT --zone-top 215.50 --zone-bottom 215.00 --buffer 0.05`
⚠ Intervention days gap through V1b — BoJ/MoF/BoE hard block exists precisely for this.
