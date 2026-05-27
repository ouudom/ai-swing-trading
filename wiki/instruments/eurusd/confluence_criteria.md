---
type: system
updated: 2026-05-27
confidence: low
tags: [eurusd, confluence, scoring, gates]
related: [macro_drivers.md, profile.md, constitution_addendum.md]
---

# EURUSD Confluence Criteria

> **STATUS: SCAFFOLD — define before running /weekly eurusd.**
> Reference: `wiki/system/confluence_criteria.md` for XAUUSD equivalent.

## Weekly Scoring (TODO — define signals + weights)

XAUUSD uses 7 signals totaling 10.0 pts:
- S1 Structural Level: 2.5 (mandatory)
- S2 Fibonacci: 0.75
- S3 RSI Divergence: 1.5
- S4 EMA Confluence: 0.75
- S5 Pivot Level: 0.5
- S6 Fundamental Alignment: 2.5
- S7 Volume Profile: 1.5

EURUSD signals — adapt to instrument characteristics:
- S1 Structural Level: TBD (same concept, keep mandatory)
- S2 Fibonacci: TBD
- S3 RSI Divergence: TBD
- S4 EMA Confluence: TBD
- S5 Pivot Level: TBD
- S6 Fundamental Alignment: TBD (driven by rate differential, not DFII10)
- S7 Volume Profile: TBD (CME 6E=F volume — thinner than GC=F, adjust weight?)

## Daily Validation Gates (TODO — define G1-G6 equivalent)

XAUUSD gates:
- G1: H4+H1 structure aligned (3.5 pts)
- G3: DFII10 slope supports direction (3.0 pts)
- G5: VIX regime (1.5 pts)
- G2: D1 ATR compressed (1.0 pts)
- V2: Macro drift tolerance (0.5 pts)
- G6: Asia range compressed (0.5 pts)

EURUSD equivalent:
- G1: H4+H1 structure — same logic (TBD weight)
- G3-equivalent: rate differential slope / ECB posture — TBD
- G5: VIX regime — same (USD safe-haven applies)
- G2: D1 ATR compressed — same logic
- V2: rate differential drift — TBD threshold
- G6: Asia range — same concept, threshold may differ (pip-based)

## Hard Blocks (TODO — adapt V1/V1b/V3)

V1: D1 close beyond zone — same logic, same rule
V1b: 2 consecutive H4 closes beyond zone — same rule, threshold in pips not dollars
V3: scheduled events — add ECB meeting, EU CPI, German PMI as hard blocks

## Minimum Score
- Long bias setup: TBD (XAUUSD uses 5.5/10)
- Counter-trend setup: TBD (XAUUSD uses 7.5/10 + RSI divergence mandatory)
- Order limit threshold: TBD (XAUUSD uses 6.0/10)
