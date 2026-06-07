---
type: research
updated: 2026-05-24
confidence: high
tags: [macro, FRED, DFII10, DXY, VIX, regime]
related: [xauusd_profile, constitution, confluence_criteria]
---

# Macro Regime — Findings

**Data**: FRED daily + D1 OHLC UTC, 2020-01-24→2026-05-24. N=2021 D1 bars.

## Finding 1 — DFII10 Slope Regime Split

Method: DFII10 20-day rolling mean → slope = diff(). Falling slope (<0) = bullish for gold.

| Regime | N weeks | Mean weekly return | Std | Pct positive weeks |
|---|---|---|---|---|
| Real yields falling (slope < 0) | ~155 | **+0.679%** | ~1.8% | ~56% |
| Real yields rising (slope > 0) | ~135 | **−0.082%** | ~2.0% | ~47% |

**Delta: 0.76%/week** between regimes. Clear regime split. This is the primary macro gate.

## Finding 2 — DXY Rolling Correlation

- Rolling 60-day correlation between DTWEXBGS and XAUUSD D1 close
- Inverse (negative correlation) holds **>60% of rolling windows**
- Correlation breaks during risk-off spikes (both gold AND dollar rally simultaneously)
- Mean correlation: approximately −0.35 to −0.45

## Finding 3 — VIX Buckets

| VIX | N weeks | Mean weekly return | Edge |
|---|---|---|---|
| < 15 (calm) | ~120 | ~+0.25% | modest positive |
| 15–25 (normal) | ~140 | ~+0.40% | positive |
| > 25 (fear) | ~30 | **+0.009%** | **near zero** |

**Key insight**: Gold fear-bid (VIX spike) = spike-and-reverse pattern. Not sustained edge.
Do NOT use VIX as hard gate. Use for context only.

## Finding 4 — Combined Signal (yields↓ + DXY↓ + VIX↑)

- N occurrences: 205 D1 bars
- Fwd 5D return: +0.234% (≈baseline +0.287%) — **no short-term edge**
- Fwd 20D return: **+1.646%** vs baseline +1.166% — **+41% better at 20D**
- Interpretation: combined signal = longer-duration tail wind, not day-trade signal
- Relevant for swing holds (2–10 days) — boosts weekly conviction level

## Key Conclusions

1. **Macro gate = DFII10 slope only** (not combined signal). Simple, high-impact.
2. VIX >25 = danger, not opportunity. Don't counter a fear spike without RSI divergence.
3. Combined signal useful for weekly forecast **conviction level** (supports HIGH confidence), not daily gate.
4. DXY inverse is real but breaks — use as secondary confirmation in weekly write-up, not hard gate.

## Open Questions

- Directional confirmation: does falling yields favor LONG gold specifically, or just more movement? (2×2 regime×direction table pending)
- DFII10 slope lag: does 10-day slope work better than 20-day for shorter swings?
- Oil (DCOILWTICO) regime: does oil rising add to or detract from gold edge?
