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

Data-backed via 6.3 years XAUUSD backtest (2020–2026). **Reweighted 2026-05-28 (D017):** G5 (VIX)
and G6 (Asia) DEMOTED to 0-point veto/informational after `scripts/sweep_g5g6.py` could not confirm
their edge (see note); their 2.0 pts redistributed to the backtest-proven anchors G1/G3/G2/V2.

| # | Condition | Weight | Pass when |
|---|---|---|---|
| G1 | **H4+H1 Market Structure** | **4.0** | Both H4 and H1 show HH+HL (long) or LH+LL (short) |
| G3 | **DFII10 Slope** | **3.5** | 20-day slope < 0 for longs, > 0 for shorts. Setup C exempt. |
| G2 | **ATR Compression** | **1.5** | D1 ATR14 < 20-day median |
| V2 | **Macro Drift OK** | **1.0** | DFII10 drift vs baseline < 0.10% against direction |
| G5 | **VIX Regime** | **VETO, 0 pts** | No points. Hard veto only: VIX > 35 → all SHORT setups NO TRADE (safe-haven flow). Regime still logged in daily file. |
| G6 | **Asia Range Compression** | **0 pts, info** | No points. Logged in daily file as context (compressed = expansion likely at London) — does not score. |

> **Why G5/G6 demoted (D017, 2026-05-28):** `scripts/sweep_g5g6.py` added VIX + Asia-range to the
> backtest and tagged every executed trade. Result: the live-formula strategy fires only **~1.7
> trades/yr (11 in 6.3yr)** — far too few to validate a 2.0-pt sub-weight. What signal existed was
> null-to-contradictory: Asia-compressed trades avgR +0.86 vs normal +1.17 (compression did NOT
> help), and VIX>25 was a single lucky long (n=1). Per edge-first policy, an unconfirmable weight is
> removed, not assumed. VIX>35 short-block kept as RISK management (not edge). Frequency must come
> from instrument breadth, never from padding the score with unvalidated gates.

### Thresholds

```
Hard blocks pass AND score ≥ floor AND H1 trigger present  → ORDER LIMIT
Hard blocks pass AND score ≥ floor, no H1 trigger          → WATCH
Hard blocks pass AND score < floor                         → NO TRADE
Any hard block fails                                       → NO TRADE / INVALIDATED
floor = 6.5 if ADX(14) D1 in 20–25 (transitional) else 6.0  (see Regime Filter)
```

Minimum 6.0 requires **at least one of G1 or G3** (neither is individually mandatory):
- Without G1: G3+G2+V2 = 3.5+1.5+1.0 = 6.0 ✅ (exactly clears)
- Without G3: G1+G2+V2 = 4.0+1.5+1.0 = 6.5 ✅
- Without both G1 AND G3: max 2.5 < 6.0 ❌ → at least one of structure/macro must hold.

So G1 is NOT a hard-mandatory gate (flag intentionally not set); the floor math only forbids placing with neither structure nor macro support. (G5/G6 contribute 0 → cannot lift a sub-floor score.)

**H1 trigger** (replaces H4): pin bar, engulfing, or break-and-retest on H1 inside the setup zone. Observed at /validate time. Does not alter weekly confluence score or entry offset.

**G3 note**: Counter-trend setups (Setup C) exempt — they already require RSI divergence + macro LOW/MEDIUM confidence.

**G5 — VIX Regime (0-point VETO + logging only, D017):**

Awards NO score. Two uses remain: (1) a hard risk veto, (2) regime context logged in the daily file.

- **Hard veto:** VIX > 35 (panic) → all SHORT setups NO TRADE (safe-haven flow overwhelms structure).
- **Logged context:** <18 calm (yield-driven, G3 reliable) | 18–25 mixed | >25 risk-off (G3 can flip;
  gold rallies even on rising yields). Recorded as `vix` + regime in the daily file — informational.

VIX source: `data/fred/VIXCLS.csv` latest close.
**Freshness guard:** FRED VIXCLS lags — at 07:30 UTC the latest row may be 1–2 days old. If
`latest VIX date < today − 1`, set `vix_stale=true` and suspend the VIX>35 short veto (don't act on
stale data). Log `vix_stale` in the daily file. Optional upgrade: intraday VIX via Twelve Data `VIX`.

**G6 — Asia Range (0-point, informational only, D017):**

Awards NO score. Asia session = 22:00 UTC prior day → 07:00 UTC today (9 H1 bars),
range = `max(high) − min(low)`. Logged as `asia_range` context (compressed < $15 = expansion likely
at London; > $30 = possibly exhausted before London — flag). Does not affect the validation score.

(Legacy reference — the pass/penalty table below is retained for context but no longer scores:)

| Range | (was) | Reason |
|-------|------|--------|
| < $15 | ✅ | Compressed — expansion likely at London open |
| $15–$30 | ❌ (0 pts, no penalty) | Normal range, no edge |
| > $30 | ❌ + warn | Move possibly exhausted before London — flag in daily file |

---

## Regime Filter — ADX (wired into both /weekly and /validate)

ADX(14) on Daily chart (emitted by `weekly_pull.py` as `adx_val`). This is NOT a scored signal —
it is a **floor modifier + setup-bias filter**, applied as follows:

| ADX | Regime | /weekly bias | /validate floor |
| --- | --- | --- | --- |
| > 25 | Trending | Favor continuation/trend setups (A/B with bias) | 6.0 (normal) |
| 20–25 | Transitional | No regime preference | **6.5** (raised — chop risk) |
| < 20 | Ranging | Favor reversal/counter at zone edges; trend-continuation weaker | 6.0 (normal) |

**Wiring:**
- `/weekly` (Agent 3/4): read `adx_val` from pull; bias setup selection per table; note regime in forecast.
- `/validate`: read `adx_val` from pull. If 20 ≤ ADX ≤ 25 → required validation floor = **6.5** (else 6.0).
  Record `adx_regime` + the floor used in the daily file.

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
  entry_offset = (10 − confluence_score) × 0.25 × stop_distance
  Short: limit_price = zone_top    + entry_offset    ← above zone
  Long:  limit_price = zone_bottom − entry_offset    ← below zone

Direction: offset pushes limit AWAY from spot, BEYOND zone extreme. Lower score = bigger
overshoot required before fill. Confluence score gates GO/WATCH/NO-TRADE AND scales offset.
```

| Score | Conviction | Offset (× stop_distance) | Risk |
| --- | --- | --- | --- |
| 10.0 | HIGH | 0 (limit at zone extreme) | $2000 |
| 7.5–9.5 | MEDIUM-HIGH | 0.125–0.625× | $2000 |
| 5.5–7.0 | MEDIUM | 0.75–1.125× | $2000 |
| < 5.5 | LOW | — NO TRADE | — |

**Example:** Zone $4,660–$4,700, score 7.5/10. D1 ATR=$70 → 0.5×D1=$35. H4 ATR (trading) = $31. structural_dist = $35. stop_distance = avg($35, $31, $35) = $33.67.
```
offset      = (10 − 7.5) × 0.25 × $33.67 = 2.5 × 0.25 × $33.67 = $21.04
limit_price = zone_top + offset = $4,700 + $21.04 = $4,721.04   (short)
SL          = $4,721.04 + $33.67 = $4,754.71
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
