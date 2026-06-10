---
type: system
updated: 2026-06-10
confidence: medium
tags: [audusd, fx, macro, sessions, mean-reversion, commodity-fx]
related: [constitution, confluence_criteria, ../../research/audusd/signal-results, ../core/currency_exposure]
---

# AUDUSD Instrument Profile

> **Character: MEAN-REVERTING, H4-centric fade** (EURUSD family — inverse of gold). Fade
> extremes; never trend-follow. D1 price rows are thin — D1 supplies regime (ADX, squeeze,
> VIX level), H4/H1 supply the fade. See [[confluence_criteria]] and
> [[../../research/audusd/signal-results]]. D024 expansion pair #1.

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 (std lot = 100k AUD, $10/pip — USD-quoted, exact) | lot sizing |
| pip | 0.0001 | thresholds, ATR display |
| `PRICE_DP` | 5 | price rounding |
| `MIN_BAR_RANGE` (H4 ATR filter) | 0.0003 (3 pips) | drop flatline bars |
| **V1b threshold** | **0.0004 (4 pips)** past zone, 2 consecutive H4 closes | invalidation |
| `USD_BETA_SIGN` | −1 (USD-quote major) | fx_exposure ledger |
| Market hours | Globex Sun 22:00 → Fri 22:00 UTC | session filter |

## Primary macro drivers (ranked, from 16yr scan — D024)
1. **VIX LEVEL regime (🔑 inverted vs EUR/GBP veto logic):** VIX>20 → LONG tilt (+8.7pp t=6.14);
   VIX<15 → SHORT tilt (+6.8pp t=5.29). High-VIX = AUD already sold → mean-revert up.
   **NO FX VIX-veto-LONGS for AUDUSD.** VIX *spike* (1d>3) is dead (t=0.04) — level, not event.
2. **US 2Y (DGS2) 20d slope** — slope<0 → long (t=2.28); slope>0 → short (t=2.12).
3. **DEAD (do not score): DXY 1d jump** (t=−0.85 — the strongest EUR/GBP gate does NOT transfer),
   2s10s curve, carry/policy diff (no daily RBA series anyway — `RATE_FOREIGN=None`).
4. Commodity/China beta (iron ore, copper, China PMI) — no free daily series; narrative context
   only, never scored.

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | rate-momentum leg (scored) |
| US 10Y | DGS10 | 2s10s context (not scored) |
| Fed Funds | DFF | US carry (context) |
| RBA cash rate | — none daily on FRED | carry leg DISABLED (monthly OECD only) |
| VIX | VIXCLS | **level regime tilt** (scored, inverted) |
| ICE DXY | DX-Y.NYB (yahoo) | context only (jump signal dead for AUD) |
| COT | CME AUD 6A | positioning context |

## Event blocks (hard = NO TRADE within 2h; rest caution)
- **US tier-1** (CPI, NFP, FOMC, PCE) — shared with all USD pairs. HARD.
- **RBA cash rate decision** (~8/yr, Tue 04:30 UTC) — HARD.
- **AU quarterly CPI** (~04:30 UTC) + monthly employment (~01:30 UTC) — HARD.
- **China tier-1** (PMI, trade, GDP, stimulus headlines) — caution → upgrade to hard if zone is
  China-sensitive (commodity-driven move in progress).
- RBNZ — caution only (antipodean sympathy moves).

## Sessions (UTC)
| Session | Hours | Behaviour |
|---|---|---|
| Sydney/Asia | 22:00–07:00 | AUD's home session — livelier than EUR's Asia; AU/China data lands here |
| London open | 07:00–09:00 | H1 SHORT drift (t=2.67) — fade rallies into London |
| NY overlap | 12:00–16:00 | Peak liquidity, best fills |

## Daily ATR reference (pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 50–61 | p10–p25; current ~51 sits here |
| Normal | 61–99 | 16yr p25–p75, median 74 (last-5yr median 63) |
| High vol | 99–125 | p75–p90; RBA/CPI/China-shock weeks |
| Crisis | 125+ | halve risk to $1000 |
H4 ATR median ≈ 25 pips (≈80% of EURUSD — slightly tighter stops/offsets).

## Portfolio notes
- **Antipodean bloc:** AUDUSD + NZDUSD same direction ≈ one bet (corr ~0.85) — fx_exposure
  emits an advisory note (D024). Suggest keeping the cleaner setup.
- Shares the USD leg with all USD pairs — ledger advisory on same-direction stacks.
