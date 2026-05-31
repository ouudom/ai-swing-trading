---
type: paper_review
paper: ssrn-4834097.pdf
title: "Rough Gaps Exist? Opening Gaps Help to Surge Returns in Swing and Intraday Trading"
authors: "Sagar Baniya (MSc dissertation, Oxford Brookes)"
year: 2024
venue: "MSc Finance dissertation / SSRN"
tier: 1
updated: 2026-05-31
confidence: medium
tags: [gaps, weekend-gap, mean-reversion, swing, intraday, gold, dollar]
related: [forex-price-overreactions, confluence_criteria]
---

# Opening Gaps in Swing & Intraday Trading

**One-liner**: Large opening gaps tend to mean-revert (bigger gap → bigger reversal/retracement); gap behaviour links to gold and USD.

## Why we kept it
We already capture `weekend_gap_pct` in the weekly frontmatter but don't trade off it. This tests the gap edge directly and explicitly ties gaps to gold + dollar — our macro axis.

## Method
- Market / instrument: S&P 500 + NASDAQ indices (US equities).
- Data range + N: 2019–2021, ~750 gap samples; pre-test / post-test design.
- Technique: bucket gaps by size, measure post-gap direction-from-open; correlate with volume + macro vars (gold, USD).

## Key values
- H1 **supported**: larger gaps → larger market reversals (big gaps produce bigger retracements). Reversion strength scales with gap size.
- H2 (gap size ↔ volume): only **weak** correlation.
- H3: gap behaviour **is** affected by economic variables incl. gold and US dollar.
- Gap buckets analysed: >2%, 1–2%, 0.5–1%, −0.5 to 1%, < −2% (appendix shows post-gap direction paths per bucket).

## Apply to us
- Treat a large weekend gap as a **fade/mean-revert** prior, not a continuation signal — could become a confluence modifier on `weekend_gap_pct`.
- Test on XAUUSD: does a big Monday gap retrace within the week? Bucket by gap size as the paper does.
- Macro tie-in (gold/USD ↔ gaps) supports keeping gap + DXY in the same view.

## Caveats
- Equity indices, not gold/FX — transfer unproven; XAUUSD weekend gaps are a different microstructure (Sun open).
- Short, recent, volatile window (2019–2021, COVID); costs excluded; dissertation rigor.

**Verdict**: borrow the "large gap = fade" hypothesis; must re-test on XAUUSD before trusting.
