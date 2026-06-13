---
type: system
updated: 2026-06-13
confidence: low
tags: [calibration, edge-validation, shadow-ledger]
related: [zone_outcomes, zone_ledger, constitution]
---

# Calibration — Edge Performance

> **AUTO-GENERATED** by `scripts/calibration.py` at 2026-06-13 06:34Z. Do not hand-edit — re-run the script. Source: `data/zone_outcomes.csv`.

Zones tracked: **15** · completed shadow trades: **1** · invalidated-before-fill (capital saved): **0** · min-n for verdicts: **10**.

## Overall (completed shadow trades)

n=1 · win 0% · -1.0R (avg -1.00) · **INSUFFICIENT (n<10)**

## Status mix (all tracked zones)

| status | count |
|---|---|
| PENDING | 11 |
| RUNNING | 3 |
| LOSS_SL | 1 |

> INVALIDATED before fill = the system refused a zone that later broke its kill level — a capital-saving outcome, not a loss.

### By R1 confluence bucket

| R1 confluence bucket | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| <7.0 | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By instrument

| instrument | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| gbpusd | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By direction

| direction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| SHORT | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By conviction

| conviction | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| MEDIUM | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By fill session

| fill session | n | win% | total R | avg R | verdict |
|---|---|---|---|---|---|
| London | 1 | 0% | -1.0 | -1.00 | INSUFFICIENT (n<10) |

### By instrument × direction

| instrument | dir | n | win% | total R | verdict |
|---|---|---|---|---|---|
| gbpusd | SHORT | 1 | 0% | -1.0 | INSUFFICIENT (n<10) |

## R2 Entry Confluence (real trades only)

_Awaiting live trades. Shadow trades fill at the zone midpoint with no E0/offset replay, so Entry Confluence (R2) cannot be calibrated from them — only from real fills in `data/trades_log.csv`._

---
_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not final, below ~20 trades._
