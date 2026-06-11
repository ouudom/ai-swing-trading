---
type: daily_validation
instrument: nzdusd
date: 2026-06-11
week: 2026-W24
active_zone: NONE
v1_structure_intact: true
v1b_intact: true
v3_news_clear: false
vix_veto: false
vix_stale: true
reforecast_action: NONE
reforecast_triggers: []
entry_confluence_score: 0.0
order_limit: NO_TRADE
limit_direction: N/A
h4_atr: 0.00172
d1_atr: 0.00550
d1_atr_compressed: false
adx_val: 18.5
macro_now: 4.13
macro_slope: 0.13
---

# Validation — 2026-06-11 (ALL zones from [[2026-W24]])

**Verdict: ❌ NO TRADE — all zones (V3 hard block). Zones held PENDING (none invalidated). No live limits to cancel.**

## Market Snapshot
| | Value | vs Baseline / Note |
|---|---|---|
| Spot | 0.57926 | — |
| DGS2(context) | 4.13 | baseline 4.0, 20d slope +0.13 |
| H4 ATR (trading) | 0.00172 | — |
| D1 ATR | 0.00550 | median 0.00548 → compressed ❌ |
| VIX | 19.87 | stale (2026-06-09 < today−1) → veto suspended; <35 anyway |
| ADX(14) D1 | 18.5 | ranging |
| D1 last close | 0.57934 | inside/short of all zones — no V1 break |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ intact | no zone breached |
| V1b | 2 consec H4 closes past extreme | ✅ intact | spot short of all zones |
| V3 | Hard news within 2h London/NY | ❌ **FAIL** | PPI (US tier-1) 12:30 UTC — within 2h of NY open |
| VETO | VIX>35 / spike>3 | ✅ pass | VIX 19.87 (stale), spike +0.95 |
| Macro flip | vs baseline | ✅ pass | macro-light — US2Y/DXY dead for NZD |

## Q3 — Re-Forecast Check
Triggers fired: none (T1–T5 all sub-threshold) → action: **NONE**

## Q4 — Entry Confluence
Not scored — **V3 hard block stops at Q1/Q2.**

## Per-Zone Result
| Zone | Dir | Box | V1 | V1b | Verdict | Note |
|---|---|---|---|---|---|---|
| PRIMARY | SHORT | 0.58550–0.58900 | ✅ intact | ✅ intact | ❌ NO TRADE (V3) | unreached +97 pip |
| COUNTER | LONG | 0.57500–0.57900 | ✅ intact | ✅ intact | ❌ NO TRADE (V3) | unreached, MEDIUM cap |

## Result
```
NO TRADE — V3 hard block: PPI (US tier-1) 12:30 UTC — within 2h of NY open
All zones held PENDING (structure intact, no invalidation). No re-forecast. 0 order limits placed.
```
> [!note] Antipodean advisory vs AUDUSD (same-dir SHORT ≈ one bet). Weakest edges; both zones held PENDING.
