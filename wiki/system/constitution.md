---
type: system
updated: 2026-05-24
confidence: high
tags: [rules, risk, core]
related: [xauusd_profile, confluence_criteria]
---

# Trading System Constitution

## Identity
- Instrument: XAUUSD
- Style: Swing trading, discretionary
- Hold period: 2–10 days
- Timeframes: Weekly (bias) → Daily (setup) → H4 (limit placement + offset)

## Risk Rules — Non-Negotiable
- Risk per trade: $2000
- **No calendar trade cap** — bounded by weekly risk only
- Max loss per week: $4000 (= 2 losing trades). Hit → cancel all live limits, no new trades until Monday.
- Max loss per month: $10000
- Drawdown circuit breaker: account drops 5% from peak → $1000/trade until recovered
- Never widen a stop after entry
- Never move stop against the trade

Multiple trades same week allowed if (a) each setup independently passes /validate, (b) cumulative open risk + closed loss ≤ $4000, (c) no two trades same direction stacking (treated as one position).

## TP Structure
- TP: 3R → close full position (single exit, no split)
- TP must land at a structural level (prior swing, weekly pivot, Fib extension)
- Never set TP at arbitrary R-multiple with nothing structural there
- After entry: stop is fixed — never trail, never widen

## Position Sizing
```
structural_dist = entry − last_pivot_low (long) | last_pivot_high − entry (short)
                  last pivot within 20 H4 bars
atr_floor       = 0.5 × H4 ATR(14)
stop_distance   = max(structural_dist, atr_floor)
                  fallback: min(H4_ATR14, 0.5×D1_ATR14) if no pivot found within 20 bars
cap: if structural_dist > 3 × H4 ATR(14) → skip trade (R:R collapses)

lots = $2000 / (stop_distance × 100), round DOWN
Minimum: 0.01 lots (micro)

Example: H4_ATR=$20, last pivot low $50 below entry → structural_dist=$50 > 3×$20=$60? No → valid
stop_distance = max($50, 0.5×$20=$10) = $50
lots = 2000/(50×100) = 0.40 → 0.40 lots
```

Stop distance and entry-offset buffer both use `stop_distance` as the base unit — see Entry Rules below.

## Entry Rules — Order Limit with Daily Validation Gate

All entries use **order limits** (buy limit for longs, sell limit for shorts).
No market orders. No bar-close confirmation entries.

**Order placement is gated by daily validation — never placed Sunday without validation.**
**Order-limit price (offset) is computed at /validate time using that day's H4 ATR and structural pivot — never frozen from /weekly.**

```
Daily workflow (runs 07:30 UTC, before London open):
  1. Run /validate [date]
  2. Hard blocks (any fail = stop immediately):
       V1: D1 close beyond zone? → INVALIDATED (remove setup)
       V3: Hard news event within 2h? → NO TRADE
       G4: Outside 08:00–17:00 UTC? → NO TRADE
  3. Validation score (max 10.0):
       G1 H4+H1 structure aligned   3.5 pts
       G3 DFII10 slope supports     3.5 pts
       G2 D1 ATR compressed         2.0 pts
       V2 Macro drift OK            1.0 pts
  4. H1 trigger check (pin bar / engulfing / B&R on H1 inside zone)?

  → OUTPUT (exactly one of):
     ✅ ORDER LIMIT: score ≥ 6.0 + H1 trigger present
     👁 WATCH: score ≥ 6.0, no H1 trigger yet
     ❌ NO TRADE: score < 6.0 or hard block triggered

  5. Order expires 21:00 UTC — re-validate next morning, never carry forward.
```

**Order limit price formula (tiered 10.0 scale):**
```
stop_distance     = max(structural_dist, atr_floor)        ← same value as Position Sizing
buffer_per_unit   = 0.10 × stop_distance                  ← per missing weight unit
missing_weight    = 10.0 - confluence_score
entry_offset      = missing_weight × buffer_per_unit
                  = (10 - score) × 0.10 × stop_distance

Short: limit_price = zone_top    - entry_offset
Long:  limit_price = zone_bottom + entry_offset

Hard cap: offset ≤ 50% of zone width (40% for counter). Exceeded → no trade.
```

Stop distance and offset buffer share the same `stop_distance` value — one structural change moves both consistently.

Minimum score to place order: **5.5/10**. Below 5.5 = no order placed, ever.
Counter (Setup C): **7.5/10** floor.

**H1 trigger (entry confirmation, not confluence):**
Pin bar, engulfing, or break-and-retest inside zone on H1. Observed at /validate time only.
Trigger present → record in daily file as confirmation. Does NOT alter score or offset.
Trigger absent → output **WATCH** (conditions met, awaiting confirmation). Do not place limit yet.
Trigger present → output **ORDER LIMIT** (place the limit). Trigger is the final gate.

## Stop Placement

**Formula (updated 2026-05-24, data-backed):**
```
structural_dist = distance from entry to last pivot low below entry zone (long)
                  distance from entry to last pivot high above entry zone (short)
                  → use last pivot within 20 H4 bars before entry

atr_floor       = 0.5 × H4 ATR(14)    ← hard minimum, never go tighter

stop_distance   = max(structural_dist, atr_floor)
lots            = $2000 / (stop_distance × 100), round DOWN
```

**Why structural > ATR:** Backtested on 10,454 H4 bars. ATR stop (old formula) exceeded by price within 10 bars 96.9% of the time — it was not protective. Structural stop (pivot low/high) exceeded only 64% of the time — sits beyond noise. Structural stop is wider than ATR stop ~79% of the time; lot size adjusts accordingly.

**Cap:** If structural_dist > 3 × H4 ATR(14) → zone too wide, skip the trade (structural level is too far, R:R collapses).
**Legacy formula** `min(H4_ATR14, 0.5×D1_ATR14)` retained as fallback if no valid pivot found within 20 bars.

## No-Trade Rules
- No new entries 2 hours before any red-folder Forex Factory event
- Gold: NFP, FOMC, CPI, US Retail Sales are hard blocks — cancel any live limit orders
- If weekly $4000 loss limit hit: cancel all open limit orders, no new trades until Monday

## Weekend Gap Gate (Monday /validate only)

Computed at /weekly run from H4 data: Friday 20:00 UTC close vs first bar after Sunday reopen.

| |gap_pct| | Action |
|---|---|
| < 0.20% | Noise. Log only. Proceed normally. |
| 0.20–0.50% | Note in Monday /validate. No bias change. |
| 0.50–1.00% | **Warning** — re-examine weekly bias before /validate. Setup zones may need redraw. |
| > 1.00% | **Hard re-forecast** — run /weekly again Monday morning. Sunday forecast voided. |

Gap direction matters: large gap *in direction of weekly bias* = momentum confirm but worse fills (zones distant). Large gap *against bias* = potential invalidation.

## Real-Yield Baseline Drift (every /validate)

Forecast frontmatter stores `baseline_dfii10` (real yield at Sunday data pull).
Daily DFII10 vs baseline:

| |Δ DFII10| | Action |
|---|---|
| < 0.05% | Macro unchanged. Pass Check 2. |
| 0.05–0.10% | Note in daily file. Still pass if direction supports bias. |
| > 0.10% | **Macro check 2 FAILS** if drift is against trade direction. HOLD. |
| > 0.15% any direction | **Force re-forecast** regardless of direction (regime shift). |

## Invalidation
A setup is cancelled when:
- Price closes beyond the setup zone on Daily
- Macro bias reverses (real yields spike against trade direction)
- Weekly structure breaks (trend structure violated)

> **Liquidity Sweep Exception:** A wick penetration of the setup zone that closes back inside (same candle or next) is NOT invalidation — it's a Wyckoff Spring / stop hunt. Require a Daily *close* beyond the zone before cancelling. A sweep followed by a strong rejection candle is a higher-conviction entry signal, not an exit.

## Setup Types

| Setup | Direction | Min Score (out of 10) | Extra Rules |
|---|---|---|---|
| A — Primary | With weekly bias | 5.5 | Best confluence zone |
| B — Secondary | With weekly bias | 5.5 | Alternative price path, distinct zone |
| C — Counter | Against weekly bias | 7.5 | Signal 3 mandatory; macro must be LOW/MEDIUM confidence only; cap 40% zone width |

Max 4 setups per week. If no valid setup for a slot → NONE (never force).
Trades executed bounded by $4000 weekly risk cap, not by setup count.
Priority A → B → C only governs entry preference if multiple fill same day. Independent setups may fill across the week.

## The Three Laws
1. Risk management > TA method
2. No confluence = no trade. Waiting is a position.
3. If you can't write the IF/THEN in one sentence, the setup isn't ready.
