---
type: system
updated: 2026-06-11
confidence: high
tags: [eurjpy, instrument, profile, jpy, cross]
related: [confluence_criteria, signal-results, constitution]
---

# EURJPY — Instrument Profile

**Character: symmetric mean-reversion + calm-drift hybrid** on a long-drift floor
(D1 baseline LNG 55.6%). Buy washouts, fade extension, NEVER chase — two-sided fade
works on every TF (unlike usdjpy, where H1 fade-short is anti). Purest price-driven
pair in the book: **macro fully dead** (ECB leg anti, VIX dead, no USD leg).
Evidence: [[signal-results]].

## Engine constants (scripts/config/eurjpy/config.py) — FIRST CROSS-JPY PAIR
| Field | Value | Note |
|---|---|---|
| PIP_SIZE | **0.01** | big figure = 1.00 = 100 pips; price 3dp |
| PRICE_DP | **3** | JPY-quoted |
| TICK_MULTIPLIER | **650** | STATIC ≈100000/USDJPY(154) — pip value depends on USDJPY, NOT EURJPY |
| V1B_BUFFER | 0.04 | 4 JPY pips ≈ 10% median H4 ATR (42 pips) |
| USD_BETA_SIGN | **0** | cross — no USD leg, no DXY rows, no USD correlation guard |
| MACRO_MODE | cross_rate_diff, RATE_GBP=None | one-leg (ECBDFR only) — non-scoring, scans ANTI |
| COT | EUR/JPY XRATE, **DIRECT** read | thin (OI ~21k) — context only, extremes = noise |
| VP_TICKER | None | no clean futures continuous |

SL 0.50 (50 pips) at USDJPY 154 (JPY pip value drifts with USDJPY spot ±10%, accepted D024).

## Macro — NONE (first fully price-driven pair)
1. ECB leg (X9/X10): t = −1.23/−1.31 — mildly ANTI. Non-scoring tilt in weekly pull only.
2. **VIX: DEAD** (E13 0.91, E15 0.55, spike −0.42) — the "carry barometer" reputation
   does not show at swing horizon. No veto, no score. Crash tails handled by MoF/BoJ
   event blocks instead.
3. No DXY, no US2Y rows (cross). Confluence = 100% price/structure/session.

## MoF / BoJ intervention regime ⚠ (spot 185.2 = record territory)
MoF intervention targets USDJPY (160.5, inside the 2022/2024 band) but slams ALL JPY
crosses simultaneously — 300–500 USDJPY pips ⇒ comparable EURJPY moves.
- **BoJ decision days + active MoF jawboning = HARD block** (same as usdjpy).
- **LONG zones at fresh record highs during intervention-watch → conviction cap MEDIUM.**
- ECB decision = HARD block (EUR leg).
- Intervention days gap through V1b — the hard block exists precisely for this.

## Sessions (two-sided — unique so far)
- **London open 07–09 UTC = fade-SHORT window** (H1 t=2.77).
- **NY/London overlap 12–16 UTC = drift-LONG window** (H1 t=3.02; NY open 13–15 t=2.26).
- Pattern: fade the London pop, ride the NY drift.

## ATR (2026-06-11, pips = 0.01)
| TF | p25 | med | p75 | now |
|---|---|---|---|---|
| D1 | 95 | 118 | 152 | **76 (compressed — calm-long regime)** |
| H4 | 32 | 42 | 56 | 27 |

≈1.37× usdjpy D1 ATR (two-leg vol). Spread ~1.5–3 pips ≈ 4–7% median H4 ATR.

## Events
- **BoJ decision + MoF jawboning = HARD block** (shared with usdjpy).
- **ECB decision = HARD block** (EUR leg, shared with eurusd/eurgbp).
- US tier-1 (CPI/NFP/FOMC): not first-order (no USD leg) but both legs transmit —
  **CAUTION (stand down entries within 1h), not a hard block.**
- Tokyo CPI / national CPI = caution (BoJ-policy input).

## Portfolio notes (fx_exposure, ADVISORY — D024)
- eurjpy-long = long EUR + short JPY: stacks with usdjpy-long (shared short-JPY leg —
  ledger flags it) and with eurusd-long / eurgbp-long (shared long-EUR leg).
- usdjpy-long + eurjpy-long ≈ double short-JPY = doubled MoF-intervention tail. Prefer
  the cleaner of the two when both signal.
- gbpjpy (#7 next) overlaps the JPY leg again.
