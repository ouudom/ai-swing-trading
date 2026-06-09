---
type: system
updated: 2026-06-09
confidence: medium
tags: [eurgbp, fx, cross, sessions, mean-reversion]
related: [constitution, confluence_criteria, currency_exposure, ../../research/eurgbp/signal-results]
---

# EURGBP Instrument Profile (CROSS)

> **Character: MEAN-REVERTING, LOW-VOLATILITY CROSS.** Fade extremes; never trend-follow.
> EURGBP has **no USD leg** — driver is EUR-vs-GBP (ECB vs BoE), not DXY/US rates. Macro is
> **thin/dead on free daily data (EG2) → price/structure edge only**. Edges validated on D1 (16yr)
> + H4/H1 (2020→now). See [[confluence_criteria]], [[../../research/eurgbp/signal-results]], and
> [[currency_exposure]] (netting — EURGBP IS the cross factor, must route through the exposure ledger).
>
> **Status: confluence ACTIVE. Onboarding complete — ready for first `/weekly eurgbp`** (no zones
> published yet). Sizing in USD, no GBP convert (operator).

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 (std lot = 100k units) | lot sizing (USD, no GBP convert — operator) |
| pip | 0.0001 | thresholds, ATR display |
| `PRICE_DP` | 5 | price rounding |
| `MIN_BAR_RANGE` (H4 ATR filter) | **0.0002 (2 pips)** — tighter, low-vol cross | drop flatline |
| **V1b threshold** | **0.0004 (4 pips)** past zone, 2 consecutive H4 closes | invalidation |
| `QUOTE_CCY` | **GBP** | pip-value conversion |
| Market hours | Globex Sun 22:00 → Fri 22:00 UTC | session filter |

## Pip economics — sized in USD (operator decision: NO GBP convert)
EURGBP is nominally GBP-quoted (1 pip/lot = 10 GBP). **Operator decision: size in USD with the
same formula as the majors** — `lots = $2000 / (SL_price × 100000)`, no GBP→USD conversion.
| SL (pips) | SL price | Lots (raw) | Risk (USD-targeted) |
|---|---|---|---|
| 18 | 0.0018 | 0.61 | ~$2000 |
| 25 | 0.0025 | 0.44 | ~$2000 |
| 35 | 0.0035 | 0.31 | ~$2000 |
| 50 | 0.0050 | 0.22 | ~$2000 |
> Caveat: EURGBP P&L is intrinsically GBP. This assumes the broker settles EURGBP pip value in
> USD. If it settles in GBP, a "$2000" trade ≈ £2000 ≈ $2670 (~33% over) — revisit if so.

## Drivers (EG2 result — macro is NOT a gate)
1. **Price/structure mean-reversion = the edge** (EG3). Fade D1 oversold/overbought + 20d extremes.
2. **Macro thin/dead** on free daily data — no German/UK daily market yields, ECBDFR is a flat step.
   Only sub-significant hints: EUR−GBP rate diff 5d widen → long (t=1.50); VIX 1d spike → long (t=1.68).
   **Low-weight tilt only, never a scored gate or veto.**
3. **🔑 NO VIX-LONG-VETO** (unlike the USD-majors). VIX risk-off bids EUR over GBP → EURGBP **UP**
   (E16 long +6.7) — *inverted* polarity. The majors' VIX-veto-LONGS would block the wrong side.
4. **DEAD (do not score):** all 20d rate slopes, DXY (USD index — irrelevant to a non-USD cross).

## FRED / data series
| Series | ID | Role |
|---|---|---|
| ECB Deposit Rate | ECBDFR | EUR policy leg (flat step — weak) |
| UK SONIA | IUDSOIA | GBP rate leg (the differential's only mover) |
| VIX | VIXCLS | risk sentiment — spike → EURGBP UP (tilt, NOT veto) |
| GBP/USD spot | (gbpusd pipeline) | **pip→USD sizing conversion** |
| COT | derived 6E vs 6B | positioning context (no single EURGBP contract) |
| — DXY | — | NOT used (USD index, irrelevant) |

## Sessions (UTC) — London-dominant, both legs European
| Session | Hours | Behaviour |
|---|---|---|
| Asian | 22:00–07:00 | Very quiet — both EUR & GBP asleep; avoid |
| London open | 07:00–09:00 | Primary session — nearly all EURGBP range builds here |
| London | 07:00–16:00 | Best liquidity + fills |
| NY | 12:00–21:00 | Thin after London close; cross barely reacts to US data |

## Daily ATR reference (16yr D1, pips) — ~HALF a USD-major
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 36–47 | p10–p25 (now 25 = extreme compression) |
| Normal | 47–76 | median 60; ideal swing |
| High vol | 76–89 | p75–p90; BoE/ECB/UK-CPI weeks |
| Crisis | 89+ | Brexit/2022 spikes; halve risk |
1y median 36 pips (currently quiet regime).

## High-impact events — ECB + BoE + UK/EZ data (NOT US)
| Event | Rule |
|---|---|
| **BoE rate decision + MPC minutes** | no new entries; GBP-leg shock |
| **ECB rate decision + press conf** | no new entries; EUR-leg shock |
| UK CPI / GDP / jobs | no new entries 2h before |
| EZ CPI / flash PMI / German IFO | no new entries 2h before |
| US NFP / CPI / FOMC | **caution only — NOT a hard block** (no USD leg; cross barely reacts) |

This is a key cross difference: US tier-1 events are hard blocks for the USD-majors but only
*caution* for EURGBP. The cross's hard blocks are the **European** central banks + data.

## Mid-week re-forecast triggers (EURGBP instantiation)
Macro is dead → triggers lean on PRICE + shock, not rate drift.
| Trigger | Threshold |
|---|---|
| T1 — EUR−GBP rate diff 1d jump | abs(Δ) > 0.10% (weak — informational) |
| T2 — (no DXY) → BoE/ECB surprise same day | policy decision off-consensus |
| T3 — EURGBP counter-move vs bias | D1 close > 1.5% against weekly bias (primary) |
| T4 — shock (X structured news OR Y VIX 1d jump>5) | as constitution |
| T5 — rate-diff cumulative drift | abs > 0.15% (weak — informational) |

## Position sizing quick reference
`lots = $2000 / (SL_price × 100000)`, round DOWN to 0.01 (same as majors; no GBP convert).
Crisis ATR >89 pips → halve to $1000 risk.

## VIX veto direction — NONE (cross exception)
Unlike XAUUSD (block SHORTs) and the USD-majors (block LONGs), EURGBP has **no VIX veto** —
risk-off polarity is inverted and sub-significant. VIX-spike is a weak LONG *tilt*, not a veto.

## Netting (critical — see [[currency_exposure]])
EURGBP IS the cross risk-axis. A direct EURGBP order can stack on an *implied* cross from a held
EURUSD/GBPUSD pair. Every EURGBP order MUST route through `scripts/fx_exposure.py` (Architecture B
ledger) — per-axis $2000 cap, keep-best-drop-weaker. Do not size EURGBP in isolation.
