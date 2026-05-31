---
type: paper_review
paper: ssrn-2133999.pdf
title: "Global Variance Risk Premium and Forex Return Predictability"
authors: "Arash Aloosh (Neoma Business School)"
year: 2016
venue: "SSRN working paper"
tier: 1
updated: 2026-05-31
confidence: high
tags: [VIX, VRP, variance-risk-premium, FX-predictability, carry, macro-gate, eurusd]
related: [macro-regime, asymmetric-volatility-connectedness-forex]
---

# Global Variance Risk Premium & Forex Predictability

**One-liner**: Equity variance risk premium (VRP = risk-neutral minus realized variance, VIX-derived) predicts FX returns at the 1-month horizon, beating standard carry predictors.

## Why we kept it
Quantitative backing for treating volatility/VIX as a macro signal (our G5 VIX-regime gate). Shows a VIX-family measure has genuine, out-of-sample FX predictive power — including EUR/USD.

## Method
- Market / instrument: major FX incl. EUR/USD, GBP/USD, JPY/USD; carry portfolios.
- Data range + N: monthly, Jan 2000 – Dec 2011; 5-yr initial training (2000–04), OOS 2005–11.
- Technique: predictive regressions of 1-mo FX excess returns on global VRP vs commodity factor (CRB) and FX-vol factor (FXV); long-run risk model with stochastic vol.

## Key values

| Test | Result |
|---|---|
| Global VRP predicts FX returns | significant **in- AND out-of-sample**, 1-mo horizon |
| GVRP vs carry predictors | GVRP has **more** predictive power |
| Equity-diff regression (US-UK), GVRP slope | **2.53*** (t 6.05), Adj R² 13.08% — vs CRB R² 4.88%, FXV R² 4.79% |
| OOS R² EUR/USD | **+2.44%** (significant) |
| OOS R² GBP/USD | **+17.06%** (significant) |
| OOS R² JPY/USD | −2.67% (not significant) |

## Apply to us
- Strong evidence to **keep VIX/VRP in the macro stack** — but note our own research found VIX is a context signal, not a hard gold gate ([[macro-regime]] G5). This paper is FX-return, monthly; reconcile horizons.
- For EURUSD: VRP is a candidate predictive feature (+2.44% OOS), modest but real.
- Use VRP = (risk-neutral var − realized var) construction, not raw VIX level, if we formalize it.

## Caveats
- Monthly horizon, 2000–2011 sample (pre-covers GFC, not recent regimes).
- Predicts FX excess returns, not gold; EUR/USD OOS R² small (2.44%); JPY insignificant — edge is uneven across pairs.

**Verdict**: study — validates VIX/VRP as a macro input, esp. for EURUSD; mind horizon mismatch.
