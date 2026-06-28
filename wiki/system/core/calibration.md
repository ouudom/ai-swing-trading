---
type: system
updated: 2026-06-28
confidence: low
tags: [calibration, edge-validation, shadow-ledger]
related: [zone_outcomes, zone_ledger, constitution]
---

# Calibration — Edge Performance

> **AUTO-GENERATED** by `scripts/calibration.py` at 2026-06-28 04:40Z. Do not hand-edit — re-run the script. Source: `data/zone_outcomes.csv`.

Zones tracked: **54** · completed shadow trades: **24** · invalidated-before-fill (capital saved): **0** · min-n for verdicts: **10**.

## Overall (completed shadow trades)

n=24 · win 42% · +16.0R (avg +0.67) · **WORKING**

## Status mix (all tracked zones)

| status | count |
|---|---|
| PENDING | 18 |
| WIN_TP1 | 10 |
| NO_TOUCH | 9 |
| LOSS_SL | 9 |
| BREAKEVEN | 5 |
| RUNNING | 3 |

> INVALIDATED before fill = the system refused a zone that later broke its kill level — a capital-saving outcome, not a loss.

### By R1 confluence bucket

| R1 confluence bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| 7.0–7.9 | 10 | 30% | +3.5 | +0.35 | WORKING |
| <7.0 | 11 | 55% | +10.0 | +0.91 | WORKING |
| >=8.0 | 3 | 33% | +2.5 | +0.83 | INSUFFICIENT (n<10) |

### By instrument

| instrument | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| audusd | 3 | 67% | +5.0 | +1.67 | INSUFFICIENT (n<10) |
| eurgbp | 2 | 50% | +1.5 | +0.75 | INSUFFICIENT (n<10) |
| eurusd | 4 | 25% | +0.5 | +0.12 | INSUFFICIENT (n<10) |
| gbpusd | 5 | 20% | +0.5 | +0.10 | INSUFFICIENT (n<10) |
| nzdusd | 4 | 50% | +3.0 | +0.75 | INSUFFICIENT (n<10) |
| usdchf | 4 | 25% | +0.5 | +0.12 | INSUFFICIENT (n<10) |
| xauusd | 2 | 100% | +5.0 | +2.50 | INSUFFICIENT (n<10) |

### By direction

| direction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| LONG | 11 | 18% | -2.0 | -0.18 | DEAD |
| SHORT | 13 | 62% | +18.0 | +1.38 | WORKING |

### By conviction

| conviction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| MEDIUM | 17 | 47% | +16.0 | +0.94 | WORKING |
| MEDIUM-HIGH | 3 | 67% | +4.0 | +1.33 | INSUFFICIENT (n<10) |
| MEDIUM-LOW | 4 | 0% | -4.0 | -1.00 | INSUFFICIENT (n<10) |

### By fill session

| fill session | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| Asia | 9 | 56% | +9.5 | +1.06 | INSUFFICIENT (n<10) |
| London | 8 | 50% | +8.0 | +1.00 | INSUFFICIENT (n<10) |
| NY | 7 | 14% | -1.5 | -0.21 | INSUFFICIENT (n<10) |

### By instrument × direction

| instrument | dir | n | win% | total R | verdict |
|---|---|---|---|---|---|
| audusd | LONG | 2 | 50% | +2.5 | INSUFFICIENT (n<10) |
| audusd | SHORT | 1 | 100% | +2.5 | INSUFFICIENT (n<10) |
| eurgbp | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<10) |
| eurgbp | SHORT | 1 | 100% | +2.5 | INSUFFICIENT (n<10) |
| eurusd | LONG | 2 | 0% | -2.0 | INSUFFICIENT (n<10) |
| eurusd | SHORT | 2 | 50% | +2.5 | INSUFFICIENT (n<10) |
| gbpusd | LONG | 2 | 0% | -1.0 | INSUFFICIENT (n<10) |
| gbpusd | SHORT | 3 | 33% | +1.5 | INSUFFICIENT (n<10) |
| nzdusd | LONG | 3 | 33% | +0.5 | INSUFFICIENT (n<10) |
| nzdusd | SHORT | 1 | 100% | +2.5 | INSUFFICIENT (n<10) |
| usdchf | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<10) |
| usdchf | SHORT | 3 | 33% | +1.5 | INSUFFICIENT (n<10) |
| xauusd | SHORT | 2 | 100% | +5.0 | INSUFFICIENT (n<10) |

## R2 — Entry Confluence (trade_outcome replay)

Replayed fills: completed **14** · LIMIT_MISSED (offset never reached = D030 near-miss) **11** · min-n **10**.

n=14 · win 29% · +0.0R (avg +0.00) · **DEAD**

### By Entry Confluence (EC) bucket

| EC bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| >=8.0 | 7 | 29% | +0.0 | +0.00 | INSUFFICIENT (n<10) |
| 6.5–7.9 | 3 | 33% | +0.5 | +0.17 | INSUFFICIENT (n<10) |
| 5.0–6.4 | 2 | 50% | +1.5 | +0.75 | INSUFFICIENT (n<10) |
| <5.0 (sub-floor) | 2 | 0% | -2.0 | -1.00 | INSUFFICIENT (n<10) |

### Gate accuracy (was the block correct?)

> Counterfactual: each zone is filled in replay **despite** the gate. A gate KEEPS EDGE when its blocked trades net ≤0R (loss avoided); COSTING EDGE when they net >0R (winner refused). Replaces the old unverified "INVALIDATED = capital saved" assumption.

| gate | n blocked | would-be win% | would-be total R | verdict |
|---|---|---|---|---|
| V1 | 4 | 0% | -4.0 | INSUFFICIENT (n<10) |
| V1b | 4 | 0% | -4.0 | INSUFFICIENT (n<10) |
| V3 | 11 | 0% | -3.0 | INSUFFICIENT (n<10) |
| VETO_VIX | 0 | — | — | INSUFFICIENT |
| VETO_ADX | 4 | 50% | +1.5 | INSUFFICIENT (n<10) |
| INTERVENTION | 0 | — | — | INSUFFICIENT |
| EC_FLOOR | 2 | 0% | -2.0 | INSUFFICIENT (n<10) |

> D030 offset watch: **11** zones filled at the zone midpoint in `zone_outcome` but the entry-mechanics offset limit was never reached — the offset is leaving fills (often the winners) on the table.

---
_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not final, below ~20 trades._
