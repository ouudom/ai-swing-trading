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

### Validation Score (max 10.0)

Data-backed via 6.3 years XAUUSD backtest (2020–2026). Reweighted 2026-05-27 — added G5 (VIX regime), G6 (Asia range), redistributed via Path B.

| # | Condition | Weight | Pass when |
|---|---|---|---|
| G1 | **H4+H1 Market Structure** | **3.5** | Both H4 and H1 show HH+HL (long) or LH+LL (short) |
| G3 | **DFII10 Slope** | **3.0** | 20-day slope < 0 for longs, > 0 for shorts. Setup C exempt. |
| G5 | **VIX Regime** *(provisional)* | **1.5** | Regime aligns with setup type — see VIX table below |
| G2 | **ATR Compression** | **1.0** | D1 ATR14 < 20-day median |
| V2 | **Macro Drift OK** | **0.5** | DFII10 drift vs baseline < 0.10% against direction |
| G6 | **Asia Range Compression** *(provisional)* | **0.5** | Asia session range (22:00–07:00 UTC, H1) < $15 |

> **Provisional weights (G5, G6):** the backtest (`s_weekly_swing_v1`) does NOT model VIX or
> Asia range — its loader has no VIX/intraday-session data. So the 1.5 + 0.5 weights are
> assumed, not empirically validated. Treat as provisional until the backtest loader carries
> VIX + Asia-range and a with/without comparison confirms edge. See research _INDEX pending item.

### Thresholds

```
Hard blocks pass AND score ≥ 6.0 AND H1 trigger present  → ORDER LIMIT
Hard blocks pass AND score ≥ 6.0, no H1 trigger          → WATCH
Hard blocks pass AND score < 6.0                          → NO TRADE
Any hard block fails                                      → NO TRADE / INVALIDATED
```

Minimum 6.0 requires at least G1+G3 (3.5+3.0=6.5). Cannot place on macro alone without structure, or structure alone without macro.

**H1 trigger** (replaces H4): pin bar, engulfing, or break-and-retest on H1 inside the setup zone. Observed at /validate time. Does not alter weekly confluence score or entry offset.

**G3 note**: Counter-trend setups (Setup C) exempt — they already require RSI divergence + macro LOW/MEDIUM confidence.

**G5 — VIX Regime Detail:**

| VIX | Regime | Gold behavior | G5 pass condition |
|-----|--------|---------------|-------------------|
| <18 | Calm — yield-driven | Real-yield slope dominant (G3 reliable) | ✅ for all primary setups (A/B) aligned with G3 |
| 18–25 | Mixed | Both yield + safe-haven flow | ✅ if G3 also passes; ❌ if G3 fails |
| >25 | Risk-off — safe-haven | G3 can flip (gold rallies even on rising yields) | ✅ for LONG setups regardless of G3; ✅ for SHORT only if G3 strongly supports; counter-trend (C) gets ✅ automatically |

VIX source: `data/fred/VIXCLS.csv` latest close. Hard-block edge case: VIX > 35 (panic regime) → all SHORT setups NO TRADE (safe-haven flow overwhelms structure).

**Freshness guard:** FRED VIXCLS is a prior-daily-close series and lags — at 07:30 UTC the latest row may be 1–2 days old. If `latest VIX date < today − 1`, set `vix_stale=true`: award G5 = 0 (no credit) AND suspend the VIX>35 short block (don't act on stale data). Log `vix_stale` in the daily file. Optional upgrade: fetch intraday VIX via Twelve Data `VIX` symbol when stale.

**G6 — Asia Range Detail:**

Asia session = 22:00 UTC prior day → 07:00 UTC today (9 H1 bars). Compute: `max(high) − min(low)` across those bars.

| Range | Pass | Reason |
|-------|------|--------|
| < $15 | ✅ | Compressed — expansion likely at London open |
| $15–$30 | ❌ (0 pts, no penalty) | Normal range, no edge |
| > $30 | ❌ + warn | Move possibly exhausted before London — flag in daily file |

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

## Scoring → Conviction + Order Limit

H1 trigger patterns (pin bar, engulfing, break-and-retest) are NOT a confluence signal.
They are entry confirmation observed at /validate time only — see [[constitution]].

**Stop + offset are computed at /validate time** using that day's H4 ATR (trading-day filter), D1 ATR, and structural pivot — never frozen from /weekly. Recompute every morning.

```
structural_dist   = entry → last pivot low (long) | last pivot high → entry (short), within last 5 trading days (~30 H4 bars)
H4_ATR14          = ATR(14) on trading-day H4 bars only (filter: range >= $1)
D1_ATR14          = ATR(14) on D1 bars
stop_distance     = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean
                    fallback: avg(0.5 × D1_ATR14, H4_ATR14) if no pivot within last 5 trading days
cap:   structural_dist > 3 × H4_ATR14   → NO TRADE (zone too wide)
floor: structural_dist < 0.5 × H4_ATR14 → pivot inside noise
       → check yesterday's validation file; reuse yesterday's pivot if still valid
       → else fallback to 2-component avg

Order limit (offset OUTWARD beyond zone extreme):
  entry_offset = (10 − confluence_score) × 0.3 × stop_distance
  Short: limit_price = zone_top    + entry_offset    ← above zone
  Long:  limit_price = zone_bottom − entry_offset    ← below zone

Direction: offset pushes limit AWAY from spot, BEYOND zone extreme. Lower score = bigger
overshoot required before fill. Confluence score gates GO/WATCH/NO-TRADE AND scales offset.

R:R floor (after offset): R = abs(TP − limit_price) / stop_distance. R < 1.8 → NO TRADE.
```

| Score | Conviction | Offset (× stop_distance) | Risk |
| --- | --- | --- | --- |
| 10.0 | HIGH | 0 (limit at zone extreme) | $2000 |
| 7.5–9.5 | MEDIUM-HIGH | 0.15–0.75× | $2000 |
| 5.5–7.0 | MEDIUM | 0.90–1.35× | $2000 |
| < 5.5 | LOW | — NO TRADE | — |

**Example:** Zone $4,660–$4,700, score 7.5/10. D1 ATR=$70 → 0.5×D1=$35. H4 ATR (trading) = $31. structural_dist = $35. stop_distance = avg($35, $31, $35) = $33.67.
```
offset      = (10 − 7.5) × 0.3 × $33.67 = 2.5 × 0.3 × $33.67 = $25.25
limit_price = zone_top + offset = $4,700 + $25.25 = $4,725.25   (short)
SL          = $4,725.25 + $33.67 = $4,758.92
lots        = $2000 / ($33.67 × 100) = 0.59 lots
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
