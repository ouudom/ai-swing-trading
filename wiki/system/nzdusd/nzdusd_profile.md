---
type: system
updated: 2026-06-10
confidence: medium
tags: [nzdusd, fx, macro, sessions, mean-reversion, commodity-fx]
related: [constitution, confluence_criteria, ../../research/nzdusd/signal-results, ../audusd/audusd_profile, ../core/currency_exposure]
---

# NZDUSD Instrument Profile

> **Character: MEAN-REVERTING, macro-light** (weakest edge set of the USD majors — edges ≈ half
> of AUDUSD's; expect fewer publishable zones). Fade extremes on H4/H1; never trend-follow.
> See [[confluence_criteria]] and [[../../research/nzdusd/signal-results]]. D024 expansion pair #2.

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 (USD-quoted, exact) | R-distance conversion |
| pip | 0.0001 | thresholds, ATR display |
| `PRICE_DP` | 5 | price rounding |
| `MIN_BAR_RANGE` (H4 ATR filter) | 0.0003 (3 pips) | drop flatline bars |
| **V1b threshold** | **0.0004 (4 pips)** past zone, 2 consecutive H4 closes | invalidation |
| `USD_BETA_SIGN` | −1 (USD-quote major) | fx_exposure ledger |
| Market hours | Globex Sun 22:00 → Fri 22:00 UTC | session filter |

## Primary macro drivers (16yr scan — D024)
1. **VIX LEVEL regime (inverted, WEAK):** VIX>20 → LONG tilt (t=2.18); VIX<15 → SHORT tilt
   (t=2.38). Same polarity as AUD at a third of the strength. **NO FX VIX-veto-LONGS.**
2. **DEAD (do not score): US2Y slope** (t=−0.7 — even the AUD gate fails for NZD), **DXY 1d
   jump** (t=0.24), VIX spike, 2s10s, carry (no daily RBNZ series — `RATE_FOREIGN=None`).
3. NZ-specific betas (dairy/GDT, China) — no free daily series; narrative context only.

⇒ NZDUSD trades on **price/structure + weak VIX tilt** — macro-light like EURGBP.

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | context only (NOT scored — dead for NZD) |
| Fed Funds | DFF | context |
| RBNZ OCR | — none daily on FRED | carry leg DISABLED |
| VIX | VIXCLS | level regime tilt (scored, weak, inverted) |
| ICE DXY | DX-Y.NYB (yahoo) | context only (dead) |
| COT | CME NZD 6N | positioning context |

## Event blocks (hard = NO TRADE within 2h; rest caution)
- **US tier-1** (CPI, NFP, FOMC, PCE) — shared. HARD.
- **RBNZ OCR decision** (~7/yr, Wed 02:00 UTC) — HARD.
- **NZ quarterly CPI (~22:45 UTC) + employment + GDT dairy auction** (fortnightly Tue, result
  ~mid-EU session) — CPI/jobs HARD; GDT = caution (can gap NZD ±30 pips).
- **China tier-1** — caution → hard if commodity move in progress. RBA — caution (antipodean sympathy).

## Sessions (UTC)
| Session | Hours | Behaviour |
|---|---|---|
| Wellington/Asia | 21:00–07:00 | NZ data lands 21:45–02:00; thin liquidity, spread widens |
| London open | 07:00–09:00 | H1 SHORT drift (t=2.12) — fade rallies |
| NY overlap | 12:00–16:00 | best fills |

## Daily ATR reference (pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 48–58 | p10–p25; current ~54 |
| Normal | 58–90 | 16yr p25–p75, median 71 (5yr med 60) |
| High vol | 90–115 | RBNZ/CPI/China weeks |
| Crisis | 115+ | halve risk to $1000 |
H4 ATR median ≈ 23 pips. Spread 1–1.5 pips = noticeable cost fraction — demand clean setups.

## Portfolio notes
- **Antipodean bloc (key):** AUDUSD strictly dominates NZD (same class, ~2× edge). Both set up
  same direction → fx_exposure advisory; default to AUD unless NZD setup is clearly cleaner.
- Shares USD leg with all USD pairs — ledger advisory on same-direction stacks.
