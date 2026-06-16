---
type: system
updated: 2026-06-16
confidence: low
tags: [calibration, edge-validation, shadow-ledger]
related: [zone_outcomes, zone_ledger, constitution]
---

# Calibration — Edge Performance

> **AUTO-GENERATED** by `scripts/calibration.py` at 2026-06-16 11:18Z. Do not hand-edit — re-run the script. Source: `data/zone_outcomes.csv`.

Zones tracked: **29** · completed shadow trades: **4** · invalidated-before-fill (capital saved): **0** · min-n for verdicts: **10**.

## Overall (completed shadow trades)

n=4 · win 0% · -4.0R (avg -1.00) · **INSUFFICIENT (n<10)**

## Status mix (all tracked zones)

| status | count |
|---|---|
| PENDING | 12 |
| NO_TOUCH | 7 |
| LOSS_SL | 4 |
| TOUCH_NO_FILL | 4 |
| RUNNING | 2 |

> INVALIDATED before fill = the system refused a zone that later broke its kill level — a capital-saving outcome, not a loss.

### By R1 confluence bucket

| R1 confluence bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| 7.0–7.9 | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |
| <7.0 | 2 | 0% | -2.0 | -1.00 | INSUFFICIENT (n<10) |
| >=8.0 | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By instrument

| instrument | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| eurusd | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |
| gbpusd | 2 | 0% | -2.0 | -1.00 | INSUFFICIENT (n<10) |
| usdchf | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By direction

| direction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| LONG | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |
| SHORT | 3 | 0% | -3.0 | -1.00 | INSUFFICIENT (n<10) |

### By conviction

| conviction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| MEDIUM | 3 | 0% | -3.0 | -1.00 | INSUFFICIENT (n<10) |
| MEDIUM-HIGH | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By fill session

| fill session | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| London | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |
| NY | 3 | 0% | -3.0 | -1.00 | INSUFFICIENT (n<10) |

### By instrument × direction

| instrument | dir | n | win% | total R | verdict |
|---|---|---|---|---|---|
| eurusd | SHORT | 1 | 0% | -1.0 | INSUFFICIENT (n<10) |
| gbpusd | SHORT | 2 | 0% | -2.0 | INSUFFICIENT (n<10) |
| usdchf | LONG | 1 | 0% | -1.0 | INSUFFICIENT (n<10) |

## R2 Entry Confluence (real trades only)

_2 real trades logged — extend this section to bucket by R2._

---
_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not final, below ~20 trades._
