---
type: daily_validation
instrument: eurgbp
date: 2026-06-15
week: 2026-W25
active_zone: NONE
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto: false
vix_stale: false
reforecast_action: NONE
entry_confluence_score: see-body
order_limit: NO_TRADE
limit_direction: N/A
---
# Validation — 2026-06-15 (FX — all PENDING zones, [[2026-W25]])

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 0.86314 | — |
| H4 ATR (trading) | 0.00111 | — |
| D1 ATR | 0.00231 | median 0.00329 → COMPRESSED |
| VIX | 19.44 | no FX veto (<35, spike<3) |
| ADX(14) D1 | 15.0 | RANGING → floor 6.0 |
| Weekend gap | -0.073% | NOISE |

## Q1+Q2 Hard Blocks
V1 intact · V1b intact · V3 clear (CB events Tue/Wed/Thu — today's limits expire 21:00 UTC tonight,
before any decision; today's London/NY opens are clear) · no VIX veto · no macro flip.

## Q3 Re-Forecast
Monday weekend-gap gate: -0.073% → NOISE. No re-forecast.

## Q4 Entry Confluence — per zone
**LONG 0.8608–0.8625 (best, 8.5)** — EC **3.0/10** (floor 6.0) → ❌ NO TRADE. Price ~10p above zone; D1 Stoch 24.4 near-but-not oversold, W%R-75.6 (>-80), no H1 extreme, no E0. E3+E4+E5.
**SHORT 0.8660–0.8682** — EC **3.0/10** (floor 6.0) → ❌ NO TRADE. Price ~35p below zone; D1 oversold (wrong side for short). E3+E4+E5 only.

> Econ-calendar CSV stale → web-search fallback used; no tier-1 data within 2h of
> today's opens. CB decisions (the hard events) covered by the static CB-calendar gate: all Tue+.

## Result
NO TRADE on every zone — Entry Confluence below floor. Price mid-range / away from zones with no
at-zone reversal confirmation (E0) and D1/H1 oscillators not aligned. Zones remain PENDING.

---
### Hourly re-validation — 2026-06-15 03:14 UTC
spot 0.86314 — ~6p above LONG 0.8608–0.8625 (not in zone), no LONG E0 (short-pin = wrong dir); D1 mid. NO TRADE.

### Hourly re-validation — 2026-06-15 07:16 UTC
Fresh pull 07:12. Spot **0.86379** (between zones). LONG 0.8608–0.8625 ~13p below spot; SHORT 0.8660–0.8682 ~22p above spot — neither tagged. **D1+H4 TTM squeeze ON** (compression, no expansion). Both pins fired but price mid-range → **NO TRADE** both. ADX 15 ranging. BoE Thu block.

### Hourly re-validation — 2026-06-15 08:16 UTC
Fresh pull. Spot **0.86414**. LONG 0.8608–0.8625 ~16p above (price away) → NO TRADE. SHORT 0.8660–0.8682 ~19p below (price away), E0 none → NO TRADE. ADX 15.0 ranging. Both **NO TRADE**.

---
### 2026-06-15 09:50 UTC hourly re-validate
Spot 0.86435 (between zones). LONG 0.8608–0.8625 + SHORT 0.8660–0.8682 → both ❌ NO TRADE (spot mid, no E0). BoE Thu block.

---
### 2026-06-15 10:14 UTC hourly re-validate
Fresh pull (10:13). Spot **0.86451**. LONG 0.8608–0.8625 ~20p below spot (price above zone, no at-zone trigger) ❌ NO TRADE. SHORT 0.8660–0.8682 ~15p above — E0 (band-reclaim+pin-bear) fired BELOW the zone = premature (not at-resistance) ❌ NO TRADE. ADX 15.0 ranging. BoE Thu.

---
### 2026-06-15 11:21 UTC hourly re-validate
Fresh pull. Spot **0.86473** — ~13p below SHORT 0.8660–0.8682, ~22p above LONG 0.8608–0.8625. No E0 fired; H4 not extreme → ❌ NO TRADE both. ADX 15.0 ranging, no VIX veto (cross). BoE Thu block.

---
### 2026-06-15 12:30 UTC hourly re-validate
Fresh pull (12:27). Spot **0.86476** — ~12p below SHORT 0.8660–0.8682, ~23p above LONG 0.8608–0.8625. 12:00 1H pin both dirs but mid-range (neither zone tagged). H4 W%R −8.9/CCI 209 OB but spot not at the short zone → ❌ NO TRADE both. ADX 15.0 ranging. BoE Thu.

---
### 2026-06-15 14:11 UTC hourly re-validate
Fresh pull (14:0x). Spot **0.86443** (mid-range). PRIMARY LONG 0.8608–0.8625 ~19p above; SECONDARY SHORT 0.8660–0.8682 ~16p below — H4 overbought (W%R −8.9 / CCI 209) but price not at the zone and **no E0** → ❌ NO TRADE both. ECB+BoE Thu, GB CPI Wed (not today). PENDING.


---

## Hourly re-validation — 2026-06-15 15:14 UTC
Spot **0.86366**. SHORT-confirm E0 fired (RSI-reclaim 65→48 · Stoch-reclaim 83→64) + H4 W%R −8.9 / CCI 209 OB — but E0 fired mid-range, ~24p BELOW short zone 0.8660–0.8682 → not an at-zone fade. LONG 0.8608–0.8625 ~12p below spot. **❌ NO TRADE** — E0 not at zone.
