---
type: system
updated: 2026-06-09
confidence: medium
tags: [eurusd, fx, macro, sessions, mean-reversion]
related: [constitution, confluence_criteria, ../../research/eurusd/signal-results]
---

# EURUSD Instrument Profile

> **Character: MEAN-REVERTING** (inverse of gold). Fade extremes; never trend-follow. See
> [[confluence_criteria]] and [[../../research/eurusd/signal-results]]. This profile carries the
> per-instrument constants the [[constitution]] references generically.

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 (units) | R-distance conversion |
| pip | 0.0001 | thresholds, ATR display |
| `PRICE_DP` | 5 | price rounding |
| `MIN_BAR_RANGE` (H4 ATR filter) | 0.0003 (3 pips) | drop weekend/holiday flatline bars |
| **V1b threshold** | **0.0005 (5 pips)** past zone, 2 consecutive H4 closes | invalidation |
| Market hours | Globex Sun 22:00 → Fri 22:00 UTC | session filter |

## Primary macro drivers (ranked, from 16yr scan — D021)
1. **DXY 1-day move** — `DXY 1d jump>0.5 → SHORT EURUSD` is the single strongest signal (+23pp, t=9.29). Dollar-spike days follow through.
2. **US 2Y (DGS2) 20d slope** — rate momentum. slope<0 → long (+2.3pp t=2.06). Mild but real.
3. **VIX 1d spike>3 → SHORT** (risk-off USD bid drives EUR down, −10pp t=−2.56). NOT a long.
4. **DEAD (do not score):** US−EZ policy-rate differential (DFF−ECBDFR) slope, 2s10s curve — t<0.3 even at 16yr. Reported in the snapshot as context only.

Note: DXY is ~58% euro-weighted → DXY *slope* is near-circular for EURUSD (don't score it), but a DXY *1-day jump* is a clean directional shock signal.

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | rate-momentum leg (scored) |
| US 10Y | DGS10 | 2s10s context (not scored) |
| Fed Funds | DFF | US carry (context) |
| ECB Deposit Rate | ECBDFR | EZ carry (context) |
| VIX | VIXCLS | risk gate / spike short signal |
| ICE DXY | DX-Y.NYB (yahoo) | 1d jump short signal |
| COT | CME EUR 6E | positioning context |

## Sessions (UTC) — directional edge weak; volatility map only
| Session | Hours | Behaviour |
|---|---|---|
| Asian | 22:00–07:00 | Low vol, tight range |
| London open | 07:00–09:00 | Vol spike; H1 mild SHORT drift (t=4.5 H1) |
| London | 07:00–16:00 | Most active |
| NY overlap | 12:00–16:00 | Peak liquidity, best fills |

## Daily ATR reference (2015→now, pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 50–70 | p10–p25; tight ranges |
| Normal | 70–105 | median 84; ideal swing |
| High vol | 105–130 | p75–p90; CPI/FOMC weeks |
| Crisis | 130+ | p99 ~182; halve risk to $1000 |
H4 ATR median ≈ 28 pips.

## High-impact events
| Event | Rule |
|---|---|
| US NFP / CPI / FOMC | no new entries 2h before; hard block |
| ECB rate decision + presser | no new entries; EUR-leg shock |
| US Retail Sales, EZ flash PMIs/HICP | caution |

## Mid-week re-forecast triggers (EURUSD instantiation)
| Trigger | Threshold |
|---|---|
| T1 — US2Y (DGS2) 1d jump | abs(Δ) > 0.10% |
| T2 — DXY 1d jump | abs(Δ) > 0.75 ICE pts (also a scored short signal) |
| T3 — EURUSD counter-move vs bias | D1 close > 1.5% against weekly bias |
| T4 — shock (X structured news OR Y VIX 1d jump>5) | as constitution |
| T5 — US2Y cumulative drift vs `baseline_dgs2` | abs > 0.15% |

## SL reference
| SL (pips) | SL price |
|---|---|
| 25 | 0.0025 |
| 40 | 0.0040 |
| 60 | 0.0060 |
| 80 | 0.0080 |

## VIX veto direction (FX — opposite of gold)
- VIX > 35 OR VIX 1d spike > 3 → block **LONG** EURUSD (risk-off = USD bid = EUR down).
  (Gold blocks shorts on high VIX; FX blocks longs.)
