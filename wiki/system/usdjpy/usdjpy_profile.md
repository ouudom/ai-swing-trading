---
type: system
updated: 2026-06-11
confidence: high
tags: [usdjpy, instrument, profile, jpy]
related: [confluence_criteria, signal-results, constitution]
---

# USDJPY — Instrument Profile

**Character: asymmetric carry-drift.** LONG = compression/dip continuation in a
structural uptrend (D1 baseline LNG 58.9%); SHORT = D1/H4 oscillator-extreme fade only.
NOT the FX fade template — H1 overbought fade is an anti-edge (t=−3.3). Evidence:
[[signal-results]].

## Engine constants (scripts/config/usdjpy/config.py) — FIRST JPY PAIR
| Field | Value | Note |
|---|---|---|
| PIP_SIZE | **0.01** | big figure = 1.00 = 100 pips; price 3dp |
| PRICE_DP | **3** | overrides weekly_pull TICK heuristic |
| TICK_MULTIPLIER | **650** | STATIC ≈100000/154 (D024 no-convert); drifts ±10% over 140–170 |
| V1B_BUFFER | 0.04 | 4 JPY pips ≈ 10% median H4 ATR |
| MIN_BAR_RANGE | 0.03 | vestigial (session filter time-based) |
| USD_BETA_SIGN | +1 | USD-base: long pair = long USD; labels + M-rows flip |
| COT | 6J **INVERTED** | spec long JPY futures = SHORT USDJPY |
| VP_TICKER | None | futures chart inverted vs pair |
| RATE_FOREIGN | None | no daily BoJ FRED series — carry leg skipped |

SL 0.40 (40 pips) at USDJPY 160.5 (JPY pip value calibrated at 154 spot, D024).

## Macro drivers (empirical, D1)
1. **DXY 20d slope** — the live macro (long t=2.21 / short 1.73). 3rd pair beyond
   EUR/GBP; pattern = USD-base havens (CHF, JPY).
2. **VIX = WASHOUT** — no gate, no veto, no score (haven-vs-haven, same as CHF).
3. **US2Y dead** (t≈0.1–0.6) — BoJ-era sample; carry lives in the baseline drift.
4. DXY 1d jump = anti (−1.32) — never block on it.

## MoF / BoJ intervention regime ⚠ (spot 160.5 = INSIDE the band)
- MoF intervened 2022 (146–152) and 2024 (153–162): 300–500 pip slams in hours.
- **LONG zones ≥158 with fresh multi-decade highs → conviction cap MEDIUM**, no chasing
  extension (ADX>25 uptrend-continuation long is an anti-edge anyway, t −3.3/−3.4).
- **BoJ decision days (~8/yr, calendar) + explicit MoF jawboning = hard block.**
- Intervention days gap through V1b — expect zone + buffer to be skipped, not closed through.

## Sessions
- **NY drift LONG**: NY/London overlap 12–16 UTC t=4.71, NY open 13–15 t=4.19 (H1).
- London open = FLAT (t≈0.1) — breaks the AUD/NZD/CAD/CHF London-USD-drift pattern.
- NY-session SHORT = anti (−3.97). Tokyo session not separately scanned.

## ATR (2026-06-11, pips = 0.01)
| TF | p25 | med | p75 | now |
|---|---|---|---|---|
| D1 | 63 | 86 | 118 | **42 (deep calm — squeeze-long regime)** |
| H4 | 25 | 40 | 54 | 14 |

Spread ~1–2 pips ≈ 4–8% of median H4 ATR.

## Events
- US tier-1 (CPI/NFP/FOMC) = HARD block (shared).
- **BoJ decision = HARD block**; MoF jawboning ("excessive moves", rate-check reports) = stand down.
- Tokyo CPI / national CPI = caution (BoJ-policy input).

## Portfolio notes
- usdjpy-long + usdchf-long + (eurusd|gbpusd)-short = stacked long USD — fx_exposure
  ledger flags shared legs (ADVISORY, D024).
- JPY crosses next (EURJPY/GBPJPY): usdjpy-long ≈ short JPY leg overlap.
