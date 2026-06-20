---
type: daily_validation
instrument: usdcad
date: 2026-06-17
week: 2026-W25
active_zone: NONE
v1_structure_intact: true
v1b_intact: true
v3_news_clear: false
vix_veto: false
vix_stale: false
reforecast_action: NONE
entry_confluence_score: see-body
order_limit: NO_TRADE
limit_direction: N/A
---
# Validation — 2026-06-17 (usdcad, [[2026-W25]])

Automated hourly run 2026-06-17 06:09 UTC. **FOMC decision day** (statement 18:00 UTC). FOMC = the USD leg's own central bank deciding **today** → the constitution Pre-Event Flatten carve-out does NOT relax this: own-CB-today is a hard NO-TRADE for every USD pair regardless of zone distance, score, or E0. Data pull skipped — the V3 hard block precedes Entry-Confluence scoring, so no fetch can change the verdict.

## Q1+Q2 — Hard Blocks
- **V3 — own-CB-today (HARD).** US Federal Reserve FOMC statement 2026-06-17 03:11 UTC. `check_cb_calendar.py` reports usdcad on the FOMC HARD-BLOCK list. No order limit may be emitted today.
- V1/V1b: zones carried PENDING from W25 weekly; not re-fetched (entry impossible today regardless). No mid-week D1 invalidation flagged in prior run.

## Q4 — Per-Zone
- **PRIMARY LONG 1.3830-1.3875 (ZC 6.0)** — V3 own-CB-today hard block → ❌ NO TRADE (not scored).

## Result
NO TRADE — FOMC own-CB-today hard block. All zones remain **PENDING** into Thu/Fri.
