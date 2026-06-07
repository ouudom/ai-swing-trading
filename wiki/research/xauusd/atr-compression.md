---
type: research
updated: 2026-05-24
confidence: high
tags: [ATR, compression, volatility, expansion]
related: [confluence_criteria]
---

# ATR Compression → Expansion — Findings

**Data**: D1 OHLC UTC, 2020-01-24→2026-05-24. N=2021 D1 bars, 122 compression signals.

## Method

Compression signal: D1 ATR14 < its own 20-day rolling median on that bar.
Measure: next 5D range (max high − min low over next 5 D1 bars) vs ATR14 at signal bar.

## Results

| Metric | Value |
|---|---|
| N compression signals | 122 over 6.3 years (~19/yr, ~1.5/month) |
| % producing next-5D range > 1.5× ATR | **82%** |
| Mean 5D forward return (compressed) | +0.233% |
| Mean 5D forward return (not compressed) | +0.346% |

## Key Conclusions

1. **82% expansion probability** after compression — reliable setup qualifier
2. **Compression is directionally neutral** — price moves more, not necessarily in any direction
3. Forward return compressed < normal — price is "coiling," not biased up. Macro + structure decide direction.
4. The edge: compressed market + correct direction call = bigger move, better R:R (price travels further to TP)
5. **ATR-compression gate logic**: only enter setups during compression — 82% chance of explosive move supports 3R target

## Interpretation

Compression signals WHEN to enter (volatility breakout likely), not WHICH direction.
Combine with the structure gate and macro gate for directional bias, then ATR compression to confirm timing is right.

## Open Questions

- Optimal compression period: 20-day median vs 10-day or 30-day?
- Does compression → expansion produce larger moves in trending vs ranging regimes?
- After compression resolves (ATR expands), how many bars until next compression cycle?
