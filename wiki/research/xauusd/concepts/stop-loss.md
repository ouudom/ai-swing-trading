---
type: research
updated: 2026-05-24
confidence: high
tags: [stop, ATR, structural, MAE]
related: [constitution]
---

# Stop Loss Placement — Findings

**Data**: H4+D1 UTC, 2020-01-24→2026-05-24. N=802 sampled H4 bars (every 10th).

## Method

Two stop types computed per bar:
- **ATR stop**: `min(H4_ATR14, 0.5×D1_ATR14)` — old formula
- **Structural stop**: distance from close to last pivot low/high within 20 H4 bars
- **MAE test**: % of bars where price exceeds stop within next 10 H4 bars (both directions)

## Results

| Metric | ATR stop | Structural stop (long) | Structural stop (short) |
|---|---|---|---|
| Mean distance | $13.96 | $34.34 | $30.25 |
| Median | $10.19 | $21.54 | $18.25 |
| P25–P75 | $8.17–$14.84 | $11.22–$40.02 | $8.90–$34.32 |
| MAE exceedance (10 bars) | **96.9%** | **64.0%** | **68.6%** |
| Wider than ATR stop | — | 79.8% of bars | 73.1% of bars |
| > 2× ATR stop | — | 47.8% | 38.3% |

## Key Conclusions

1. **ATR stop fails 97% of the time** — not protective. Too tight. Structural zone is doing all the work.
2. **Structural stop survives 36% of the time** (long) vs 3% for ATR — 12× better
3. Structural stop is wider 79% of the time — lot size adjusts, but stop quality improves dramatically
4. The `min()` formula was undersizing stop distance; structural `max()` formula is correct

## Recommended Formula (updated 2026-05-25, in constitution.md)

```
structural_dist = entry − last_pivot_low (long) | last_pivot_high − entry (short)
                  last pivot within 20 H4 bars

H4_ATR14        = ATR(14) on trading-day H4 bars only (filter: bar range >= $1
                  — drops weekend/holiday flatline that collapses ATR)
D1_ATR14        = ATR(14) on D1 bars

stop_distance   = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean

cap: if structural_dist > 3 × H4_ATR14 → skip trade (R:R collapses)
fallback: avg(0.5 × D1_ATR14, H4_ATR14) if no pivot within 20 bars
```

**Why arithmetic-mean of three:** Single-max gave too-wide stops on high-structural setups (lot size shrunk excessively); single-min gave too-tight stops in low-vol regimes. Mean balances volatility (H4 + 0.5×D1) and structure (pivot) — stop never pinned to one extreme. Lot size scales smoothly.

## Open Questions

- What pivot lookback (currently 20 H4 bars = ~3.3 days) is optimal?
- Does placing stop 1–2 ticks beyond pivot low/high vs at the pivot change survival rate?
- Trailing stop after 1R profit — does it improve overall EV vs fixed stop?
