---
type: system
updated: 2026-05-24
confidence: high
tags: [confluence, entry, scoring]
related: [constitution, xauusd_profile]
---

# Confluence Scoring Criteria

## Daily Validation — Scoring System

At /validate time (07:30 UTC), three hard blocks are checked first, then a 10-point validation score determines order placement.

### Hard Blocks (binary — checked first, any fail = NO TRADE / INVALIDATED)

| | Block | Fail action |
|---|---|---|
| V1 | D1 close beyond zone | INVALIDATED — remove setup from _HOT.md entirely |
| V3 | NFP / FOMC / CPI / US Retail Sales within 2h of London or NY open | NO TRADE — cancel any live limit |
| G4 | Outside 08:00–17:00 UTC session window | NO TRADE — re-validate at London open |

### Validation Score (max 10.0)

Data-backed via 6.3 years XAUUSD backtest (2020–2026).

| # | Condition | Weight | Pass when |
|---|---|---|---|
| G1 | **H4+H1 Market Structure** | **3.5** | Both H4 and H1 show HH+HL (long) or LH+LL (short) |
| G3 | **DFII10 Slope** | **3.5** | 20-day slope < 0 for longs, > 0 for shorts. Setup C exempt. |
| G2 | **ATR Compression** | **2.0** | D1 ATR14 < 20-day median |
| V2 | **Macro Drift OK** | **1.0** | DFII10 drift vs baseline < 0.10% against direction |

### Thresholds

```
Hard blocks pass AND score ≥ 6.0 AND H1 trigger present  → ORDER LIMIT
Hard blocks pass AND score ≥ 6.0, no H1 trigger          → WATCH
Hard blocks pass AND score < 6.0                          → NO TRADE
Any hard block fails                                      → NO TRADE / INVALIDATED
```

Minimum 6.0 requires at least G1+G3 (the two strongest signals). Cannot place on macro alone without structure, or structure alone without macro.

**H1 trigger** (replaces H4): pin bar, engulfing, or break-and-retest on H1 inside the setup zone. Observed at /validate time. Does not alter weekly confluence score or entry offset.

**G3 note**: Counter-trend setups (Setup C) exempt — they already require RSI divergence + macro LOW/MEDIUM confidence.
**G4 note**: Validate runs 07:30 UTC → London open always in-session. Fails only on out-of-hours re-runs.

---

## Regime Filter — Run Before Scoring

ADX(14) on Daily chart:

| ADX | Regime | Implication |
| --- | --- | --- |
| > 25 | Trending | Favor continuation/breakout setups |
| 20–25 | Transitional | Require 6.5/10+ score minimum |
| < 20 | Ranging | Favor reversal setups at zone edges |

## Tiered Weighting — Max Score 10.0

Signals weighted by empirical independence + info value. Weight inflation from price-derived overlap (Fib/EMA/pivot all anchored to same swing) is the main fake-confluence vector — Tier C weighted low to neutralize.

| Tier | # | Signal | Weight | Notes |
| --- | --- | --- | --- | --- |
| **A — Anchor** | 1 | Structural Level | **2.5** | MANDATORY. Strongest empirical edge (S/R, swing). |
| **A — Anchor** | 6 | Fundamental Alignment | **2.5** | Real yields = #1 gold driver per xauusd_profile. |
| **B — Independent confirm** | 3 | RSI Divergence (Daily) | **1.5** | Independent momentum. Mandatory for counter. |
| **B — Independent confirm** | 7 | Volume Profile (CME GC) | **1.5** | Real liquidity, actual volume (not derived). |
| **C — Price-derived overlap** | 2 | Fibonacci | **0.75** | Overlaps Signal 1 (same swing anchor). |
| **C — Price-derived overlap** | 4 | EMA Confluence | **0.75** | Self-fulfilling, partial overlap. |
| **C — Price-derived overlap** | 5 | Pivot Level | **0.5** | Arithmetic formula, weakest support. |
| | | **Total possible** | **10.0** | |

## The Rule

Minimum 5.5/10 score to take a trade.
Signal 1 (structural level) is ALWAYS mandatory.
Below 5.5/10 = NO TRADE, no exceptions.

## Signals

### 1 — Structural Level [MANDATORY, 2.5]

Price at a significant Daily or Weekly S/R zone.
Valid: prior weekly swing H/L, prior daily swing H/L (2+ reactions), role-reversal retest, round number coinciding with structure.
Draw as zones (boxes), not lines.

### 2 — Fibonacci Confluence [0.75]

Setup level at 38.2%, 50%, or 61.8% of most recent significant Daily swing.
Within $5 of zone boundary = confluent.

### 3 — RSI Divergence (Daily) [1.5]

Price new extreme + RSI not confirming.
Bullish div: lower low price + higher low RSI.
Bearish div: higher high price + lower high RSI.
Overbought/oversold alone = NOT valid.

### 4 — EMA Confluence (Daily) [0.75]

50 EMA or 200 EMA within $10 of setup zone.
Both EMAs at zone = still 1 signal (same family).

### 5 — Pivot Level [0.5]

Weekly or monthly pivot (PP, R1/R2, S1/S2) within $8 of zone.
Daily pivots only if weekly/monthly unavailable.

### 6 — Fundamental Alignment [2.5]

Macro bias supports trade direction at MEDIUM or HIGH confidence.
Neutral macro = does NOT count.

### 7 — Volume Profile Level (CME GC) [1.5]

Weekly POC, VAH, or VAL from CME Gold futures (GC) within $8 of setup zone.
Source: TradingView → symbol `COMEX:GC1!` → Volume Profile (VPVR), set to Weekly.
POC + VAH/VAL both at zone = still 1 signal.

## Scoring → Conviction + Entry Offset

H1 trigger patterns (pin bar, engulfing, break-and-retest) are NOT a confluence signal.
They are entry confirmation observed at /validate time only — see [[constitution]].

**Offset is computed at /validate time** using that day's H4 ATR + structural pivot — never frozen from /weekly. Recompute every morning.

```
structural_dist   = entry → last pivot low (long) | last pivot high → entry (short), within 20 H4 bars
atr_floor         = 0.5 × H4 ATR(14)
stop_distance     = max(structural_dist, atr_floor)        ← same as Position Sizing
                    fallback: min(H4_ATR14, 0.5×D1_ATR14) if no pivot within 20 bars
buffer_per_unit   = 0.10 × stop_distance                   ← per missing weight unit
missing_weight    = 10.0 - score
entry_offset      = missing_weight × buffer_per_unit
                  = (10 - score) × 0.10 × stop_distance

Short: limit_price = zone_top    - entry_offset
Long:  limit_price = zone_bottom + entry_offset

Hard cap: entry_offset must not exceed 50% of zone width (40% for Setup C).
If offset > 50% zone width → NO TRADE (zone too thin for conviction level).
```

| Score | Conviction | Missing Weight | Offset (× risk_unit) | Risk |
| --- | --- | --- | --- | --- |
| 10.0 | HIGH | 0 | 0× | $2000 |
| 7.5–9.5 | MEDIUM-HIGH | 0.5–2.5 | 0.05–0.25× | $2000 |
| 5.5–7.0 | MEDIUM | 3.0–4.5 | 0.30–0.45× | $2000 |
| < 5.5 | LOW | — | NO TRADE | — |

**Example:** Zone $4,660–$4,700 (width $40), score 7.0/10 (Signals 1+6+4+5+7 = 2.5+2.5+0.75+0.5+1.5 = 7.75 → call it 7.5 conservative), H4 ATR = $32.52 → atr_floor $16.26, last structural pivot $35 above entry → structural_dist $35. stop_distance = max($35, $16.26) = $35.
```
missing     = 10.0 - 7.5    = 2.5
offset      = 2.5 × 0.10 × $35 = $8.75
limit_price = $4,700 - $8.75    = $4,691.25
cap check   = $8.75 < 50% × $40 = $20 → VALID
```

## Counter-Trend Setup (Setup C) — Additional Rules

Counter-trend = direction opposite to weekly macro bias.

- Minimum score: **7.5/10** (not 5.5/10)
- Signal 3 (RSI divergence) is MANDATORY — without divergence, no counter-trend setup
- Signal 6 (fundamental) will NOT score for counter-trend direction — macro works against it
  → counter-trend setups max at 7.5/10 (Signal 6 weight 2.5 unavailable)
- Only valid when macro confidence is LOW or MEDIUM
- If macro confidence is HIGH → no Setup C regardless of technical score
- Counter-trend offset uses same formula but raises hard cap to **40% zone width** (tighter — less room to be wrong)

Counter to reach 7.5 ceiling requires ALL of: Signal 1 (2.5) + Signal 3 (1.5) + Signal 7 (1.5) + Tier C (2.0 total). Tight by design.

## Fake Confluence — Never Double-Count

- RSI + Stochastic + CCI = ONE momentum signal (count under Signal 3 only)
- Multiple EMAs at same level = ONE EMA signal
- Two Fib levels near zone = ONE Fib signal (use strongest)
- Two S/R zones at same price = ONE structural level

## Migration Note — Old 7-Signal Floor

Prior system: max 7, floor 4/7. New system: max 10.0, floor 5.5/10. Mapping for reference only — re-score zones under new weights, do not back-translate scores.

| Old | Approx New | Status |
| --- | --- | --- |
| 4/7 | ~5.5/10 | Floor |
| 5/7 | ~7.0/10 | MEDIUM-HIGH |
| 6/7 | ~8.5/10 | Counter floor |
| 7/7 | 10.0/10 | All signals |
