---
type: paper_review
paper: ssrn-4574554.pdf
title: "Swing-Trading Risk Magnitude (STRM)"
authors: "Stoyan Angelov (NYU Stern)"
year: 2023
venue: "Extended abstract / SSRN (2 pp)"
tier: 1
updated: 2026-05-31
confidence: medium
tags: [risk, swing, volatility, autocorrelation, skew, position-comparison]
related: [mathematics-for-risk-management-in-forex, stop-loss]
---

# Swing-Trading Risk Magnitude (STRM)

**One-liner**: Single scalar risk score for a long-only multi-month swing position = volatility-vector magnitude scaled by autocorrelation (Durbin–Watson).

## Why we kept it
A compact, comparable per-instrument risk number. Could rank XAUUSD vs EURUSD risk, or sanity-check our ATR-based stop sizing against a momentum-persistence-aware measure.

## Method
- Market / instrument: stocks, ETFs, crypto (monthly % changes).
- Data range + N: per-asset monthly returns, ≥30 obs needed for valid skew.
- Technique: **STRM = DW · |[μ/σ, Sk]|** where DW = Durbin–Watson (0–4; <2 positive autocorr, >2 negative), μ mean monthly %, σ std, Sk Fisher–Pearson skew. Higher STRM = riskier to swing.

## Key values

| Asset | STRM | DW | μ | σ | Sk |
|---|---|---|---|---|---|
| QQQ | 1.20 | 0.172 | 1.45 | 6.81 | −0.384 |
| GOOGL | 1.36 | 0.166 | 1.72 | 8.01 | −0.433 |
| MSFT | 1.37 | 0.203 | 2.02 | 6.41 | −0.0514 |
| AMZN | 1.43 | 0.145 | 1.03 | 9.82 | −0.0289 |
| SPY | 1.82 | 0.306 | 0.92 | 5.84 | −0.561 |
| NVDA | 3.67 | 0.224 | 4.60 | 15.7 | −0.279 |
| AAPL | 3.69 | 0.372 | 2.52 | 9.60 | −0.194 |
| BTC | 4.00 | 0.184 | 4.49 | 21.3 | 0.394 |
| ETH | 5.23 | 0.185 | 6.85 | 27.5 | 0.502 |

- Crypto ~3–4× riskier than large-cap equity; low-autocorr assets get lower STRM (QQQ < SPY despite higher nominal vol).

## Apply to us
- Compute STRM on XAUUSD / EURUSD monthly returns → one risk number for cross-instrument allocation / breadth decisions.
- The DW (autocorrelation) factor formalizes "is this asset momentum-persistent" — aligns with our finding gold = momentum not mean-reversion.

## Caveats
- 2-page extended abstract; long-only, monthly horizon — NOT our weekly→H4 swing or shorts.
- Needs ≥30 monthly obs; skew invalid below that.

**Verdict**: borrow STRM as a coarse cross-instrument risk rank; not an entry/exit tool.
