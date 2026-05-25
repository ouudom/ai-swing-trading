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

H4_ATR14        = ATR(14) computed on TRADING-DAY H4 bars only
                  (filter: bar range >= $1; excludes weekend/holiday flatline)
D1_ATR14        = ATR(14) on D1 bars

stop_distance   = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean of three
cap: if structural_dist > 3 × H4_ATR14 → skip trade (R:R collapses)
fallback: if no structural pivot within 20 H4 bars → avg(0.5 × D1_ATR14, H4_ATR14)

lots = $2000 / (stop_distance × 100), round DOWN
Minimum: 0.01 lots (micro)

Example: D1_ATR=$70 → 0.5×D1=$35. H4_ATR (trading)=$31. structural pivot $50 below entry → structural_dist=$50.
stop_distance = avg($35, $31, $50) = $38.67
lots = 2000/(38.67×100) = 0.51 lots
```

Stop distance is the base unit for sizing AND for order-limit offset — see Entry Rules.

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

**Order limit placement — outward offset beyond zone extreme:**
```
entry_offset = (10 − confluence_score) × 0.3 × stop_distance

Short: limit_price = zone_top    + entry_offset    ← offset OUTWARD (above zone)
Long:  limit_price = zone_bottom − entry_offset    ← offset OUTWARD (below zone)

Direction: offset pushes limit AWAY from current spot, BEYOND zone extreme.
Lower confluence → bigger offset → price must overshoot zone further before fill.
Higher confluence → smaller offset → limit closer to zone extreme.

At score 10: offset = 0 → limit at zone extreme exactly.
At score 5.5: offset = 1.35 × stop_distance → limit 1.35 stop-units past extreme.
```

Rationale: offset = BUFFER. Forces price to commit OUTWARD (through zone extreme) before triggering. Earlier inward-offset (toward spot) produced premature fills on confirmed-rejection trades. Outward offset = strong-commitment filter — fewer fills, higher-quality entries.

Stop distance drives sizing AND offset — see Position Sizing.

Minimum score to place order: **5.5/10**. Below 5.5 = no order placed, ever.
Counter (Setup C): **7.5/10** floor.

**H1 trigger (entry confirmation, not confluence):**
Pin bar, engulfing, or break-and-retest inside zone on H1. Observed at /validate time only.
Trigger present → record in daily file as confirmation. Does NOT alter score or offset.
Trigger absent → output **WATCH** (conditions met, awaiting confirmation). Do not place limit yet.
Trigger present → output **ORDER LIMIT** (place the limit). Trigger is the final gate.

## Stop Placement

**Formula (updated 2026-05-25, triple-max):**
```
structural_dist = distance from entry to last pivot low below entry zone (long)
                  distance from entry to last pivot high above entry zone (short)
                  → use last pivot within 20 H4 bars before entry

H4_ATR14        = ATR(14) on trading-day H4 bars only (range >= $1 filter)
D1_ATR14        = ATR(14) on D1 bars

stop_distance   = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean
lots            = $2000 / (stop_distance × 100), round DOWN
```

**Why arithmetic-mean of three:** Balances the three volatility/structure dimensions: intraday noise (H4 ATR), daily volatility (0.5×D1 ATR), and structural level (pivot). Single max-dominant or min-dominant approaches over- or under-shoot any one dimension. Average smooths regime extremes — stop never collapses to one signal alone.

**Trading-day filter for H4 ATR:** Weekend/holiday flatline bars (~$0.27 range) destroy the rolling ATR. Filter to bars with range >= $1.00 before computing — uses real movement only.

**Cap:** If structural_dist > 3 × H4_ATR14 → zone too wide, skip the trade (R:R collapses).
**Fallback:** No structural pivot within 20 H4 bars → stop_distance = avg(0.5 × D1_ATR14, H4_ATR14).

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

Max 3 setups per week. If no valid setup for a slot → NONE (never force).
Trades executed bounded by $4000 weekly risk cap, not by setup count.
Priority A → B → C only governs entry preference if multiple fill same day. Independent setups may fill across the week.

## The Three Laws
1. Risk management > TA method
2. No confluence = no trade. Waiting is a position.
3. If you can't write the IF/THEN in one sentence, the setup isn't ready.
