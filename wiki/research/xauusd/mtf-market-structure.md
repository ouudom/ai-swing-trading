---
type: research
updated: 2026-05-24
confidence: high
tags: [mtf, structure, trend, HH-HL]
related: [confluence_criteria, constitution]
---

# MTF Market Structure — Findings

**Data**: H1/H4/D1 UTC, 2020-01-24→2026-05-24. Script: `build_edge_report_v2.py`

## Method

Pivot detection: bar i = pivot high if `series[i] == rolling max over 2n+1 bars centered at i`.
- n=5 for H4 and D1, n=3 for H1
- Trend state: HH+HL = uptrend (1), LH+LL = downtrend (−1), else ranging (0)
- Win rate = next-24H close > entry close (for bull); < entry close (for bear)
- Random baseline: 54.1% (overall up% across all H1 bars, 2020–2026)

## Results

| Alignment | N bars | Win/Edge rate | vs Baseline | Notes |
|---|---|---|---|---|
| H4+H1 both bull | 2,341 | 57.0% | **+3.0pp** | Recommended gate |
| H4+H1 both bear | 2,149 | 46.9% up (= 53.1% down) | +~1pp bear | Bear weaker than bull here |
| All-3 bull (D1+H4+H1) | 1,921 | 52.9% | −1.2pp | D1 filter too strict |
| All-3 bear | 687 | 43.8% up (= **56.2% down**) | **+10.2pp** | Strongest signal in dataset |
| Mixed/Ranging | 32,098 | 54.2% | +0.1pp | No edge — 82% of time |

## Key Conclusions

1. **Use H4+H1 only** for gate G1 — adding D1 cuts sample without improving edge
2. **All-bear strongest signal**: +10.2pp edge. When all 3 TFs show LH+LL, short bias well-supported
3. Market spends 82% of time mixed — the gate naturally restricts to high-quality windows
4. Bull edge (+3.0pp) is modest but real. Needs macro gate to amplify (see macro-regime findings)

## Open Questions

- Does structure-aligned entry at actual S/R zones outperform structure-only? (structural level proxy test pending)
- What is the persistence of structure state? Avg bars before regime flip?
- Does D1 structure add value for exits (not entry gate)?
