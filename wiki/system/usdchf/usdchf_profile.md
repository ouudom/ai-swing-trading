---
type: system
updated: 2026-06-10
confidence: medium
tags: [usdchf, fx, usd-base, safe-haven, snb, macro, sessions, mean-reversion]
related: [constitution, confluence_criteria, ../../research/usdchf/signal-results, ../core/currency_exposure]
---

# USDCHF Instrument Profile

> **Character: MEAN-REVERTING fade; H1 = overbought-fade SHORT machine; D1 carries the macro
> (DXY 20d slope — only pair beyond EUR/GBP with a live DXY signal). USD-BASE: long USDCHF =
> LONG USD.** See [[confluence_criteria]] + [[../../research/usdchf/signal-results]]. D024 pair #4.

## Engine constants (consumed by pipeline + constitution)
| Constant | Value | Used by |
|---|---|---|
| `TICK_MULTIPLIER` | 100000 — pip is CHF-quoted, no USD conversion applied (accepted, D024 no-convert) | R-distance conversion |
| pip / `PRICE_DP` | 0.0001 / 5 | thresholds, display |
| `MIN_BAR_RANGE` | 0.0003 (3 pips) | H4 flatline filter |
| **V1b threshold** | **0.0004 (4 pips)** past zone, 2 consecutive H4 closes | invalidation |
| `USD_BETA_SIGN` | **+1 (USD-base)** | fx_exposure ledger, scan row flips, macro labels |
| `COT_INVERTED` | True — spec long 6S = long CHF = **SHORT USDCHF** | snapshot reading |
| `VP_TICKER` | None (6S futures chart = pair upside-down) | VP disabled |

## Primary macro drivers (16yr scan — D024)
1. **DXY 20d slope (strongest, FLIPPED labels):** DXY rising → LONG USDCHF (+4.9pp t=2.32);
   falling → SHORT (t=2.34). USDCHF is the book's closest DXY proxy (CHF tracks the EUR bloc).
   DXY 1d *jump* is anti (t=−1.69 wrong-way) — no jump block, slope only.
2. **VIX = WASHOUT — no gate, no score.** USD and CHF are both havens; risk-off bids both
   legs and the net signal dies (VIX>20 long t=1.39 / VIX<15 short t=−1.97, incoherent).
   The commodity-FX fade-USD regime does NOT apply here.
3. **US 2Y (DGS2) slope, FLIPPED:** rising → LONG tilt (t=1.34/1.46) — half-point at most.
4. **DEAD:** VIX spike, 2s10s, carry (no daily SNB series — `RATE_FOREIGN=None`).

## ⚠ SNB intervention regime
SNB has a standing history of acting **against CHF strength** (= against USDCHF downside):
1.20 EURCHF floor 2011–2015, ongoing "smoothing" via sight deposits since. Spot ~0.80 is the
historic-low zone — LONG USDCHF fades near multi-year lows carry latent SNB tailwind; SHORT
zones near those lows fight a central bank. Conversely the 2015 floor-break is the canonical
reminder: when SNB *changes* regime, moves are instant and gap-through (V1b useless that day).
Treat any SNB communication day as a hard block.

## FRED / data series
| Series | ID | Role |
|---|---|---|
| US 2Y | DGS2 | rate leg, FLIPPED polarity (tilt) |
| VIX | VIXCLS | pulled for context — NOT scored (washout) |
| Fed Funds | DFF | context |
| SNB policy rate | — none daily | carry leg DISABLED |
| COT | CME CHF 6S | positioning, INVERTED read |

## Event blocks (hard = NO TRADE within 2h; rest caution)
- **US tier-1** (CPI, NFP, FOMC, PCE) — HARD.
- **SNB rate decision** (QUARTERLY — Mar/Jun/Sep/Dec, Thu 08:30 UTC) — HARD. Thin calendar
  otherwise; SNB speeches/intervention headlines = caution.
- **CH CPI** (monthly ~07:30 UTC) — caution only (low vol impact).
- ECB decisions — caution (CHF rides the EUR bloc).

## Sessions (UTC)
| Session | Hours | Behaviour |
|---|---|---|
| Asia | 22:00–07:00 | quiet |
| **London open** | 07:00–09:00 | **H1 LONG drift t=2.70** (4th pair with the London USD-long drift) |
| London/NY overlap | 12:00–16:00 | most volume; US data dominates |

## Daily ATR reference (pips)
| Regime | D1 ATR | Note |
|---|---|---|
| Low vol | 45–53 | current ~50 = compressed |
| Normal | 53–66 | last-500-bar p25–p75, median 60 |
| High vol | 66–85 | FOMC/SNB weeks |
| Crisis | 85+ | halve risk to $1000; SNB regime-change risk |
H4 ATR median ≈ 20 pips, H1 ≈ 8 pips.

## Portfolio notes
- **USD leg sign:** long USDCHF stacks with SHORT EURUSD/GBPUSD/AUDUSD/NZDUSD and LONG USDCAD
  (all = long USD). fx_exposure handles the sign — trust the ledger.
- CHF≈EUR-bloc correlation: USDCHF short + EURUSD long are near-duplicates — ledger flags the
  USD leg; prefer the higher-EC one.
