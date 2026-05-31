---
type: paper_review
paper: ssrn-1912661.pdf
title: "Fundamentalist Exchange Rate Trading Performances"
authors: "Gianfranco Forte, Jacopo Mattei, Edmondo Tudini"
year: 2011
venue: "SSRN working paper"
tier: 2
updated: 2026-05-31
confidence: low
tags: [FX, fundamentals, PPP, carry-trade, equilibrium-models, eurusd, macro-drivers]
related: [fx-trading-strategy-evolution, macro-regime]
---

# Fundamentalist Exchange Rate Trading

**One-liner**: Tests whether trading on FX equilibrium models (PPP, interest-parity, etc.) — long undervalued / short overvalued currency — actually pays, against the carry trade.

## Why we kept it
EURUSD macro-driver input. Catalogues which fundamental relations carry tradable information vs the well-known Meese–Rogoff "fundamentals don't forecast" result.

## Method
- Market / instrument: major exchange rates (USD crosses incl. EUR).
- Data range + N: long historical (Penn World Table v7.0; through ~2011).
- Technique: build valuation signal per model, go long undervalued / short overvalued currency; compare trading performance vs carry trade (CT).

## Key values
- Frames the tension: Meese–Rogoff (1983) onward → fundamental models (PPP/CIP) forecast poorly out-of-sample; yet carry trade (high-yield appreciates) works empirically — opposite of covered interest parity.
- Carry returns show strong **left-skew** and turn **negative in high-volatility/crisis** periods (Brunnermeier–Nagel–Pedersen 2009) — carry = picking up pennies in front of a steamroller.
- Concludes fundamentals retain some informative power when traded as long-undervalued/short-overvalued.

## Apply to us
- For EURUSD macro_drivers: include a valuation/interest-differential (carry) signal, but gate it OFF in high-vol/crisis (left-skew blowup risk) — ties to VIX/VRP gates ([[global-vrp-fx-predictability]]).
- Reinforces: pure macro fundamentals are weak short-term predictors → keep technical/structure as primary, macro as bias/gate (our existing design).

## Caveats
- 2011 draft; methodology light by modern standards; no XAUUSD.
- Mostly a literature synthesis + modest empirical test.

**Verdict**: context only — informs EURUSD macro-driver design (carry + crisis gating).
