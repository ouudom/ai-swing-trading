---
type: daily_validation
instrument: eurgbp
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
h4_atr: 0.00102
d1_atr: 0.00252
d1_atr_compressed: true
adx_val: 15.4
macro_now: -1.73
macro_slope: -0.001
---

# Validation — 2026-06-11 (ALL zones from [[2026-W24]])

**Verdict: ❌ NO TRADE — all zones (V3 hard block). Zones held PENDING (none invalidated). No live limits to cancel.**

## Market Snapshot
| | Value | vs Baseline / Note |
|---|---|---|
| Spot | 0.86299 | — |
| EUR-GBP rate diff | -1.73 | baseline -1.73, 20d slope -0.001 |
| H4 ATR (trading) | 0.00102 | — |
| D1 ATR | 0.00252 | median 0.00329 → compressed ✅ |
| VIX | 19.87 | stale (2026-06-09 < today−1) → veto suspended; <35 anyway |
| ADX(14) D1 | 15.4 | ranging |
| D1 last close | 0.86324 | inside/short of all zones — no V1 break |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ intact | no zone breached |
| V1b | 2 consec H4 closes past extreme | ✅ intact | spot short of all zones |
| V3 | Hard news within 2h London/NY | ❌ **FAIL** | ECB rate decision 12:15 UTC — EUR-leg hard block within 2h of NY open (US PPI = caution only for cross) |
| VETO | VIX>35 / spike>3 | ✅ pass | VIX 19.87 (stale), spike +0.95 |
| Macro flip | vs baseline | ✅ pass | rate-diff flat (informational, not a gate) |

## Q3 — Re-Forecast Check
Triggers fired: none (T1–T5 all sub-threshold) → action: **NONE**

## Q4 — Entry Confluence
Not scored — **V3 hard block stops at Q1/Q2.**

## Per-Zone Result
| Zone | Dir | Box | V1 | V1b | Verdict | Note |
|---|---|---|---|---|---|---|
| PRIMARY | LONG | 0.86080–0.86240 | ✅ intact | ✅ intact | ❌ NO TRADE (V3) | spot above, unreached |
| SHORT | SHORT | 0.86640–0.86820 | ✅ intact | ✅ intact | ❌ NO TRADE (V3) | unreached +52 pip |

## Result
```
NO TRADE — V3 hard block: ECB rate decision 12:15 UTC — EUR-leg hard block within 2h of NY open (US PPI = caution only for cross)
All zones held PENDING (structure intact, no invalidation). No re-forecast. 0 order limits placed.
```
> [!note] Cross — ECB is a hard block. Both fade edges held PENDING; netting ledger applies if either fires later in week.
