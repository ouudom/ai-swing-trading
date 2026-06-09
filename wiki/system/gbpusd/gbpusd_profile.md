---
type: system
updated: 2026-06-09
confidence: medium
tags: [gbpusd, fx, macro, sessions, mean-reversion]
related: [constitution, confluence_criteria, ../../research/gbpusd/signal-results]
---

# GBPUSD Instrument Profile

> **Character: MEAN-REVERTING** (inverse of gold). Fade extremes; never trend-follow. GBP's
> cleanest edges sit on **D1 reversal + H1 oscillators** (EUR's on H4). See [[confluence_criteria]]
> and [[../../research/gbpusd/signal-results]]. Carries per-instrument constants for [[constitution]].

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 (std lot = 100k units, $10/pip) | lot sizing |
| pip | 0.0001 | thresholds, ATR display |
| `PRICE_DP` | 5 | price rounding |
| `MIN_BAR_RANGE` (H4 ATR filter) | 0.0003 (3 pips) | drop weekend/holiday flatline |
| **V1b threshold** | **0.0006 (6 pips)** past zone, 2 consecutive H4 closes | invalidation |
| Market hours | Globex Sun 22:00 → Fri 22:00 UTC | session filter |

## Primary macro drivers (ranked, from 16yr scan — D021)
1. **DXY 1-day move** — `DXY 1d jump>0.5 → SHORT GBPUSD` (+18pp, t=7.27). Dollar-spike follow-through.
2. **VIX 1d spike>3 → SHORT** — GBP is a risk currency; spikes crash it (−22pp, t=−5.60, largest of the two pairs).
3. **US 2Y (DGS2) 20d slope** — slope<0 → long (+2.7pp t=2.39), slope>0 → short (+2.3pp t=2.15).
4. **DEAD (do not score):** US−UK policy diff (DFF−SONIA) slope, 2s10s curve — t<0.3. Context only.

Note: GBP is only ~12% of DXY, so DXY-slope is *less* circular than for EUR (t=1.42) — still sub-threshold, so not scored; the DXY 1-day jump is what carries.

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | rate-momentum leg (scored) |
| US 10Y | DGS10 | 2s10s context |
| Fed Funds | DFF | US carry (context) |
| UK SONIA | IUDSOIA | UK carry proxy (context) |
| VIX | VIXCLS | risk gate / spike short signal |
| ICE DXY | DX-Y.NYB (yahoo) | 1d jump short signal |
| COT | CME GBP 6B | positioning context |

## Sessions (UTC)
| Session | Hours | Behaviour |
|---|---|---|
| Asian | 22:00–07:00 | Low vol, GBP especially quiet |
| London open | 07:00–09:00 | Primary GBP session — vol spike |
| London | 07:00–16:00 | Most GBP range builds here |
| NY overlap | 12:00–16:00 | Peak liquidity, best fills |

## Daily ATR reference (2015→now, pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 80–95 | p10–p25 |
| Normal | 95–135 | median 112; ideal swing |
| High vol | 135–162 | p75–p90; BoE/CPI/FOMC weeks |
| Crisis | 162+ | p99 ~300 (2022 gilt crisis); halve risk |
H4 ATR median ≈ 36 pips.

## High-impact events
| Event | Rule |
|---|---|
| BoE rate decision + MPC minutes | no new entries; GBP-leg shock |
| US NFP / CPI / FOMC | hard block |
| UK CPI / GDP / jobs | no new entries 2h before |
| US Retail Sales | caution |

## Mid-week re-forecast triggers (GBPUSD instantiation)
| Trigger | Threshold |
|---|---|
| T1 — US2Y (DGS2) 1d jump | abs(Δ) > 0.10% |
| T2 — DXY 1d jump | abs(Δ) > 0.75 ICE pts |
| T3 — GBPUSD counter-move vs bias | D1 close > 1.5% against weekly bias |
| T4 — shock (X structured news OR Y VIX 1d jump>5) | as constitution |
| T5 — US2Y cumulative drift vs `baseline_dgs2` | abs > 0.15% |

## Position sizing quick reference
Formula: `lots = $2000 / (SL_price_distance × 100000)`, round DOWN to 0.01.
| SL (pips) | SL price | Lots (raw) | Actual risk |
|---|---|---|---|
| 30 | 0.0030 | 0.66 | $1980 |
| 45 | 0.0045 | 0.44 | $1980 |
| 60 | 0.0060 | 0.33 | $1980 |
| 90 | 0.0090 | 0.22 | $1980 |
Crisis ATR >162 pips → halve to $1000 risk.

## VIX veto direction (FX — opposite of gold)
- VIX > 35 OR VIX 1d spike > 3 → block **LONG** GBPUSD (risk-off → GBP crashes).
