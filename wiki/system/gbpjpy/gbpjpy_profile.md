---
type: system
updated: 2026-06-11
confidence: high
tags: [gbpjpy, instrument, profile, jpy, cross]
related: [confluence_criteria, signal-results, constitution]
---

# GBPJPY — Instrument Profile

**Character: extension-fade pair, SHORT-side dominant**, on the strongest long-drift
floor in the book (D1 baseline LNG 56.7%). Fade overbought spikes, buy washouts, NEVER
chase — every trend/momentum row is anti (the "carry-trend Beast" did not show).
**NO calm/squeeze engine** (only JPY pair without one) and **macro fully dead**
(SONIA leg ns, VIX dead, no USD leg). Second 100% price-driven pair after eurjpy.
Evidence: [[signal-results]].

## Engine constants (scripts/config/gbpjpy/config.py) — CROSS-JPY #2, HIGHEST ATR
| Field | Value | Note |
|---|---|---|
| PIP_SIZE | **0.01** | big figure = 1.00 = 100 pips; price 3dp |
| PRICE_DP | **3** | JPY-quoted |
| TICK_MULTIPLIER | **650** | STATIC ≈100000/USDJPY(154) — pip value depends on USDJPY, NOT GBPJPY |
| V1B_BUFFER | **0.05** | 5 JPY pips ≈ 10% median H4 ATR (54 pips) — largest in book |
| USD_BETA_SIGN | **0** | cross — no USD leg, no DXY rows, no USD correlation guard |
| MACRO_MODE | cross_rate_diff, RATE_GBP=None | one-leg (SONIA via RATE_EUR slot) — non-scoring, scans dead |
| COT | **DISABLED** | no CFTC GBP/JPY cross contract exists — first pair with no COT at all |
| VP_TICKER | None | no clean futures continuous |

Today: SL = avg(0.5×D1 0.754, H4 0.543) = 0.648 (65 pips) at USDJPY 154 (JPY pip value
drifts ±10% with USDJPY, D024).

## Macro — NONE (second fully price-driven pair)
1. SONIA leg (X9/X10): t = 0.58/0.29 — nothing. Non-scoring tilt in weekly pull only.
2. **VIX: DEAD** (E13 0.89, E15 0.12, spike −1.81 mildly anti). No veto, no score.
   Crash tails handled by MoF/BoJ event blocks instead.
3. No DXY, no US2Y rows (cross). Confluence = 100% price/structure/session.

## MoF / BoJ intervention regime ⚠ (spot 214.6 = record territory)
MoF intervention targets USDJPY (160.5, inside the 2022/2024 band) but slams ALL JPY
crosses — **GBPJPY slams are the LARGEST of the crosses (vol-amplified)**.
- **BoJ decision days + active MoF jawboning = HARD block** (shared with usdjpy/eurjpy).
- **BoE decision day = HARD block** (GBP leg, shared with gbpusd).
- **LONG zones at fresh record highs during intervention-watch → conviction cap MEDIUM.**
- Intervention days gap through V1b — the hard block exists precisely for this.

## Sessions (NY long-only — NOT eurjpy's two-sided structure)
- **NY/London overlap 12–16 UTC = drift-LONG window** (H1 t=4.20; NY open 13–15 t=3.75).
- **NY open 13–15 SHORT = ANTI (−3.84)** — short entries must AVOID 13–15 UTC.
- London open 07–09: DEAD both directions — no session edge, no London fade.

## ATR (2026-06-11, pips = 0.01)
| TF | p25 | med | p75 | now |
|---|---|---|---|---|
| D1 | 125 | 151 | 186 | **93 (compressed)** |
| H4 | 44 | 54 | 70 | 36 |

Highest-ATR pair in the book (1.28× eurjpy, ~1.9× usdchf D1). Spread ~2.5–4 pips
≈ 5–7% median H4 ATR — fine for H4/D1 swing; H1 edges are timing-only (cost-eaten).

## Events
- **BoJ decision + MoF jawboning = HARD block** (shared with usdjpy/eurjpy).
- **BoE decision = HARD block** (GBP leg, shared with gbpusd).
- UK CPI / Tokyo CPI = caution (policy inputs to each leg).
- US tier-1 (CPI/NFP/FOMC): no USD leg but both legs transmit —
  **CAUTION (stand down entries within 1h), not a hard block.**

## Portfolio notes (fx_exposure, ADVISORY — D024)
- gbpjpy-long = long GBP + short JPY: stacks with usdjpy-long AND eurjpy-long (shared
  short-JPY leg — ledger flags), and with gbpusd-long (shared long-GBP leg),
  inverse-overlaps eurgbp-long (short GBP).
- Three JPY pairs now live: usdjpy + eurjpy + gbpjpy same-direction = tripled
  MoF-intervention tail. When multiple signal, take the single cleanest zone.
