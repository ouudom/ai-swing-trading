---
type: paper_review
paper: ssrn-4659866.pdf
title: "Optimizing Portfolio Performance: Swing Trading, Asset Allocation, and Enhanced Lazy Portfolio"
authors: "(unattributed working paper)"
year: 2023
venue: "SSRN working paper"
tier: 2
updated: 2026-05-31
confidence: low
tags: [swing, portfolio, market-risk-filter, diversification, sharpe, sortino, drawdown]
related: [deep-sector-rotation-swing-trading, constitution]
---

# Swing + Asset Allocation + Lazy Portfolio w/ Risk Filter

**One-liner**: Blending three low-correlation strategies (swing, asset allocation, lazy portfolio) under a market-risk filter raises risk-adjusted return vs any single strategy.

## Why we kept it
The "market risk filter" gating capital by regime mirrors our gate-stack concept. Diversification-of-strategies argument supports running multiple uncorrelated edges/instruments.

## Method
- Market / instrument: US equities/ETFs (SPY benchmark), monthly observations.
- Data range + N: historical monthly returns (period not precisely stated).
- Technique: combine 3 strategies in fixed mixes (33/33/33, 33-50, 50-50); apply market-risk filter; compare to SPY on Sharpe/Sortino/DD; Efficient Frontier framing.

## Key values

| | SWING | AssetAlloc | Lazy | Port 33 | Port 50-50 | SPY |
|---|---|---|---|---|---|---|
| Sharpe | 1.28 | 1.16 | 1.30 | 1.66 | 1.66 | 0.54 |
| Sortino | 2.13 | 2.17 | 2.28 | 2.83 | 2.89 | 0.74 |
| Ann. vol | 15.2% | 15.3% | 11.6% | 10.4% | 11.5% | 15.2% |
| Ann. return | 19.7% | 17.8% | 15.4% | 18.1% | 20.2% | 8.3% |
| Max DD | −19.4% | −17.0% | −16.2% | −11.3% | −12.9% | **−56.5%** |

- Strategy correlations low (SWING↔AssetAlloc 0.22, SWING↔SPY 0.30) → blends cut max DD roughly in half vs components and ~5× vs SPY.

## Apply to us
- Confirms the breadth thesis: combining uncorrelated edges/instruments improves Sharpe and slashes drawdown — rationale for XAUUSD + EURUSD together.
- "Market risk filter" = regime gate that scales exposure; analogous to using macro regime to scale conviction.

## Caveats
- Unattributed, no rigorous methodology/period; metrics likely cost-free and possibly in-sample.
- Equities/ETF monthly; "swing" here ≠ our intraweek swing.

**Verdict**: context only — supports multi-strategy breadth; don't rely on its numbers.
