---
type: system
updated: 2026-06-19
confidence: low
tags: [calibration, edge-validation, shadow-ledger]
related: [zone_outcomes, zone_ledger, constitution]
---

# Calibration — Edge Performance

> **AUTO-GENERATED** by `scripts/calibration.py` at 2026-06-19 16:50Z. Do not hand-edit — re-run the script. Source: `data/zone_outcomes.csv`.

Zones tracked: **29** · completed shadow trades: **11** · invalidated-before-fill (capital saved): **0** · min-n for verdicts: **5**.

## Overall (completed shadow trades)

n=11 · win 27% · +0.5R (avg +0.05) · **WORKING**

## Status mix (all tracked zones)

| status | count |
|---|---|
| NO_TOUCH | 7 |
| LOSS_SL | 7 |
| PENDING | 5 |
| TOUCH_NO_FILL | 4 |
| WIN_TP1 | 3 |
| RUNNING | 2 |
| BREAKEVEN | 1 |

> INVALIDATED before fill = the system refused a zone that later broke its kill level — a capital-saving outcome, not a loss.

### By R1 confluence bucket

| R1 confluence bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| 7.0–7.9 | 4 | 25% | -0.5 | -0.12 | INSUFFICIENT (n<5) |
| <7.0 | 5 | 40% | +2.0 | +0.40 | WORKING |
| >=8.0 | 2 | 0% | -1.0 | -0.50 | INSUFFICIENT (n<5) |

### By instrument

| instrument | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| audusd | 1 | 100% | +2.5 | +2.50 | INSUFFICIENT (n<5) |
| eurusd | 2 | 0% | -2.0 | -1.00 | INSUFFICIENT (n<5) |
| gbpusd | 4 | 25% | -0.5 | -0.12 | INSUFFICIENT (n<5) |
| nzdusd | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<5) |
| usdchf | 2 | 0% | -1.0 | -0.50 | INSUFFICIENT (n<5) |
| xauusd | 1 | 100% | +2.5 | +2.50 | INSUFFICIENT (n<5) |

### By direction

| direction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| LONG | 4 | 0% | -4.0 | -1.00 | INSUFFICIENT (n<5) |
| SHORT | 7 | 43% | +4.5 | +0.64 | WORKING |

### By conviction

| conviction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| MEDIUM | 10 | 30% | +1.5 | +0.15 | WORKING |
| MEDIUM-HIGH | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<5) |

### By fill session

| fill session | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| Asia | 1 | 100% | +2.5 | +2.50 | INSUFFICIENT (n<5) |
| London | 2 | 50% | +1.5 | +0.75 | INSUFFICIENT (n<5) |
| NY | 8 | 12% | -3.5 | -0.44 | DEAD |

### By instrument × direction

| instrument | dir | n | win% | total R | verdict |
|---|---|---|---|---|---|
| audusd | SHORT | 1 | 100% | +2.5 | INSUFFICIENT (n<5) |
| eurusd | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |
| eurusd | SHORT | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |
| gbpusd | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |
| gbpusd | SHORT | 3 | 33% | +0.5 | INSUFFICIENT (n<5) |
| nzdusd | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |
| usdchf | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |
| usdchf | SHORT | 1 | 0% | +0.0 | INSUFFICIENT (n<5) |
| xauusd | SHORT | 1 | 100% | +2.5 | INSUFFICIENT (n<5) |

## R2 — Entry Confluence (trade_outcome replay)

Replayed fills: completed **9** · LIMIT_MISSED (offset never reached = D030 near-miss) **4** · min-n **5**.

n=9 · win 33% · +1.5R (avg +0.17) · **WORKING**

### By Entry Confluence (EC) bucket

| EC bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| >=8.0 | 4 | 25% | -0.5 | -0.12 | INSUFFICIENT (n<5) |
| 6.5–7.9 | 2 | 50% | +1.5 | +0.75 | INSUFFICIENT (n<5) |
| 5.0–6.4 | 2 | 50% | +1.5 | +0.75 | INSUFFICIENT (n<5) |
| <5.0 (sub-floor) | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<5) |

### Gate accuracy (was the block correct?)

> Counterfactual: each zone is filled in replay **despite** the gate. A gate KEEPS EDGE when its blocked trades net ≤0R (loss avoided); COSTING EDGE when they net >0R (winner refused). Replaces the old unverified "INVALIDATED = capital saved" assumption.

| gate | n blocked | would-be win% | would-be total R | verdict |
|---|---|---|---|---|
| V1 | 3 | 0% | -3.0 | INSUFFICIENT (n<5) |
| V1b | 2 | 0% | -2.0 | INSUFFICIENT (n<5) |
| V3 | 11 | 0% | -3.0 | INSUFFICIENT (n<5) |
| VETO_VIX | 0 | — | — | INSUFFICIENT |
| VETO_ADX | 2 | — | — | INSUFFICIENT |
| INTERVENTION | 0 | — | — | INSUFFICIENT |
| EC_FLOOR | 1 | 0% | -1.0 | INSUFFICIENT (n<5) |

> D030 offset watch: **4** zones filled at the zone midpoint in `zone_outcome` but the entry-mechanics offset limit was never reached — the offset is leaving fills (often the winners) on the table.

---
_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not final, below ~20 trades._
