---
type: research
updated: 2026-05-24
confidence: high
tags: [R, TP, RR, expectancy]
related: [constitution]
---

# R:R Target Selection — Findings

**Data**: H4 UTC, 2020-01-24→2026-05-24. Stop = ATR stop (old formula). Both directions tested.

## Raw (unfiltered) results

| R target | TP hit rate | Breakeven | Edge | EV/trade |
|---|---|---|---|---|
| 2.0R | 33.3% | 33.3% | +0.0pp | −0.001R ❌ |
| 2.5R | 29.1% | 28.6% | +0.5pp | +0.019R |
| **3.0R** | **25.6%** | **25.0%** | **+0.6pp** | **+0.024R** ✅ |

## Filtered results (from filter combination study)

| Filter combo | TP% at 3R | Edge | EV/trade |
|---|---|---|---|
| None | 25.6–25.9% | +0.6–0.9pp | +0.024–0.036R |
| MTF aligned | 32.0% | +7.0pp | +0.280R |
| ATR compression (on MTF) | 36.5% | +11.5pp | **+0.460R** |
| All 4 filters | 30.5% | +5.5pp | +0.220R |

## Key Conclusions

1. **3R is optimal** — 2.0R is breakeven, 2.5R marginally worse than 3R
2. Without filters: EV near zero for all R targets — quality of entry is everything
3. Filters dramatically lift TP%: ATR compression alone takes 3R from 25.6% → 36.5% (11.5pp)
4. 2.5R not tested with filters applied — may change relationship if filters lift TP% to 35%+

## Open Questions

- 2.5R vs 3R with ATR compression filter applied? At 36.5% TP, 2.5R breakeven = 28.6% → 3R still wins
- Partial close (1R at 1.5R, remainder at 3R) vs single exit — EV comparison?
- Does TP at structural level vs arbitrary R-multiple change hit rate?
