---
type: system
updated: 2026-06-10
confidence: medium
tags: [usdcad, fx, usd-base, oil, macro, sessions, mean-reversion]
related: [constitution, confluence_criteria, ../../research/usdcad/signal-results, ../core/currency_exposure]
---

# USDCAD Instrument Profile

> **Character: MEAN-REVERTING fade, H4 + H1 (long-side richer intraday). FIRST USD-BASE pair:
> long USDCAD = LONG USD** — every USD-direction intuition flips vs the majors. See
> [[confluence_criteria]] + [[../../research/usdcad/signal-results]]. D024 pair #3.

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 — pip is CAD-quoted, no USD conversion applied (accepted, D024 no-convert) | R-distance conversion |
| pip / `PRICE_DP` | 0.0001 / 5 | thresholds, display |
| `MIN_BAR_RANGE` | 0.0003 (3 pips) | H4 flatline filter |
| **V1b threshold** | **0.0005 (5 pips)** past zone, 2 consecutive H4 closes | invalidation |
| `USD_BETA_SIGN` | **+1 (USD-base)** | fx_exposure ledger, scan row flips, macro labels |
| `COT_INVERTED` | True — spec long 6C = long CAD = **SHORT USDCAD** | snapshot reading |
| `VP_TICKER` | None (6C futures chart = pair upside-down) | VP disabled |

## Primary macro drivers (16yr scan — D024)
1. **VIX LEVEL = fade-the-USD regime (strongest):** VIX>20 → **SHORT** USDCAD (+5.5pp t≈3.9);
   VIX<15 → LONG (+3.8pp t≈3.0). High VIX = USD already bid → fade it. **No VIX veto** —
   level scores directionally (blocks nothing).
2. **US 2Y (DGS2) slope, FLIPPED:** slope>0 (US rates rising) → LONG USDCAD (t=1.97);
   slope<0 → SHORT (t=2.10). Small weight.
3. **🛢 WTI (oil leg):** only the 5d spike >+5% → SHORT tilt (t=1.67, sub-sig). Slopes/1d dead.
   Context tilt, never a gate. ⚠ FRED `DCOILWTICO` lags ~1 week — treat W-signals as stale at
   /validate; use live WTI awareness narratively.
4. **DEAD:** DXY 1d jump (t=−1.6 wrong-way), VIX spike, 2s10s, carry (no daily BoC series —
   `RATE_FOREIGN=None`).

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | rate leg, FLIPPED polarity (scored small) |
| WTI | DCOILWTICO | oil tilt (W5 only; ~1wk lag) |
| VIX | VIXCLS | level regime — fade-USD (scored) |
| Fed Funds | DFF | context |
| BoC overnight | — none daily | carry leg DISABLED |
| COT | CME CAD 6C | positioning, INVERTED read |

## Event blocks (hard = NO TRADE within 2h; rest caution)
- **US tier-1** (CPI, NFP, FOMC, PCE) — HARD.
- **BoC rate decision** (~8/yr, Wed 13:45 UTC) — HARD.
- **CAD CPI + employment** — HARD. ⚠ CAD jobs often lands 12:30/13:30 UTC **same slot as US
  data** (double-event days — treat as one big block).
- **OPEC meetings / oil inventory shocks (EIA Wed 14:30 UTC)** — caution; upgrade to hard if
  zone thesis is oil-driven.

## Sessions (UTC)
| Session | Hours | Behaviour |
|---|---|---|
| Asia | 22:00–07:00 | dead quiet — CAD trades NY hours |
| **London open** | 07:00–09:00 | **H1 LONG drift t=2.92** (fade USDCAD dips — USD-base mirror of AUD/NZD short drift) |
| NY | 12:00–21:00 | CAD home session: BoC/CAD data, oil settlement 18:30 — most volume |

## Daily ATR reference (pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 55–69 | current ~50 = below p10, very compressed |
| Normal | 69–103 | 16yr p25–p75, median 84 (5yr med 76) |
| High vol | 103–130 | BoC/CPI/oil-shock weeks |
| Crisis | 130+ | halve risk to $1000 |
H4 ATR median ≈ 30 pips.

## Portfolio notes
- **USD leg sign:** long USDCAD stacks with SHORT EURUSD/GBPUSD/AUDUSD/NZDUSD (all = long USD).
  fx_exposure handles the sign — trust the ledger, not intuition.
- Oil correlation links CAD loosely to AUD/NZD commodity bloc — narrative only, no ledger leg.
