---
type: daily_validation
instrument: audusd
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
order_limit: ORDER_LIMIT
limit_direction: SELL
---
# Validation — 2026-06-15 (FX — all PENDING zones, [[2026-W25]])

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 0.70748 | — |
| H4 ATR (trading) | 0.00216 | — |
| D1 ATR | 0.00534 | median 0.00583 → COMPRESSED |
| VIX | 19.44 | no FX veto (<35, spike<3) |
| ADX(14) D1 | 28.9 | TRENDING → floor 6.0 |
| Weekend gap | +0.45% | NOTE |

## Q1+Q2 Hard Blocks
V1 intact · V1b intact · V3 clear (CB events Tue/Wed/Thu — today's limits expire 21:00 UTC tonight,
before any decision; today's London/NY opens are clear) · no VIX veto · no macro flip.

## Q3 Re-Forecast
Monday weekend-gap gate: +0.45% → NOTE. No re-forecast.

## Q4 Entry Confluence — per zone
**SHORT 0.7065–0.7110** — EC **5.0/10** (floor 6.0) → ❌ NO TRADE. Spot INSIDE zone; H4 overbought (E1✅2.5), H1 RSI 66 marginal (E2✅1.5), structure✅ — but no E0 and ADX 28.9 fails E3 (≥25) → 5.0 < 6.0 raised floor. Closest call of the day.
**COUNTER LONG 0.6980–0.7000** — EC **1.0/10** (floor 6.0) → ❌ NO TRADE. Price ~75p above zone; H4 overbought (wrong side); ADX trending. Also _HOT veto-watch if ADX>30 (28.9 now).

> Econ-calendar CSV stale → web-search fallback used; no tier-1 data within 2h of
> today's opens. CB decisions (the hard events) covered by the static CB-calendar gate: all Tue+.

## Result
NO TRADE on every zone — Entry Confluence below floor. Price mid-range / away from zones with no
at-zone reversal confirmation (E0) and D1/H1 oscillators not aligned. Zones remain PENDING.

---
### Hourly re-validation — 2026-06-15 03:14 UTC
spot 0.70773 — INSIDE SHORT 0.7065–0.7110, H4-OB but NO E0 + ADX 28.9 fails E3 (trending into fade); EC≈4.5 <floor. NO TRADE (closest).

### Hourly re-validation — 2026-06-15 07:16 UTC → ✅ ORDER LIMIT
Fresh pull (07:12). Spot **0.70734**, INSIDE SHORT 0.7065–0.7110 (lower third). **Decisive change:**
06:00 1H closed bar fired a **SHORT E0** — RSI-reclaim✦ (69→61, back through 65) + Stoch-reclaim
(87→79), a bearish turn AGAINST the upward (weekend-gap) approach into resistance. London open
07–09 UTC = the pair's best short-fade window (session note, H1 short drift t=2.67).

**Entry Confluence: 6.5/10** (E0✅3.0 E1✅2.5 E2❌ E3❌ E4❌ E5✅1.0)
- E0✅ 3.0 — at-zone bearish RSI-reclaim on 06:00 1H close.
- E1✅ 2.5 — H4 still extreme: Stoch 88.6 / W%R −4.4 / CCI 144.6 all overbought.
- E2❌ 0 — H1 RSI now 61 (<65, reclaimed out of extreme); no fresh H1 extreme.
- E3❌ 0 — D1 ADX 28.9 (>25, trending). NB still <30 → no hard ADX veto.
- E4❌ 0 — VIX 19.44 (neither >20 long-tilt nor <15 short-tilt); US2Y slope mixed (20d rising / 1d −0.08%).
- E5✅ 1.0 — zone not broken on D1 close (no close above 0.7110).

6.5 ≥ floor (5.0 base; 6.0 trending-regime) → **✅ ORDER LIMIT**, anchor = confirmation close 0.70729.

**Order Limit calc:** SL 0.00247 = avg(0.5×D1 0.00267, H4 0.00228). offset = max(SL/3 0.00082,
(10−6.5)×0.2×SL 0.00173) = **0.00173**. SHORT limit = anchor 0.70729 + 0.00173 = **0.70902**
(inside zone). SL = 0.70902 + 0.00247 = **0.71149** (above zone top 0.7110).
R = 0.00247. TP1 2.5R **0.70285** (manual) · TP2 3.0R **0.70161** (limit) · BE +1.5R **0.70532**.

```
AUDUSD ORDER LIMIT: SELL 0.70902 | SL 0.71149 | TP1 2.5R 0.70285 (manual) | TP2 3.0R 0.70161 (limit) | BE @1.5R 0.70532 | expires 2026-06-15 21:00 UTC
Entry Confluence: 6.5/10 (E0:✅ E1:✅ E2:❌ E3:❌ E4:❌ E5:✅)
Anchor: confirmation close 0.70729 | SL 0.00247 | offset 0.00173 | R:R structural ~2.5–3.0
"If price reaches 0.70902, SELL triggers. Cancel if not hit by 21:00 UTC."
```

> [!warning] Concentration (D024, advisory): audusd SHORT = long USD; stacks with operator's OPEN
> USDCHF long (also long USD) → ledger CONCENTRATED, +2.00u long USD. Suggested cleaner = USDCHF
> (EC 8.5 > 6.5) — but USDCHF thesis has flipped bearish and is under exit review, so the practical
> overlap is small. Operator decides; nothing auto-skipped.

> [!warning] Event risk: **RBA decision tomorrow 06-16** (audusd hard-block day). This order EXPIRES
> 21:00 UTC tonight, so it does not place an order live during RBA — but if it FILLS today the
> position carries into the RBA decision. Operator: consider flattening/managing before ~03:30 UTC 06-16.

### Hourly re-validation — 2026-06-15 08:16 UTC → LIVE LIMIT UNCHANGED
Fresh pull. Spot **0.70688**, INSIDE SHORT 0.7065–0.7110. Existing **LIVE ORDER LIMIT SELL 0.70902** (placed 07:16, EC 6.5) — **V1b ✅ intact** (last 2 H4 closes 0.70719/0.70688, threshold 0.71140), ADX 28.9 (<30 veto), no V3 today → limit stands, expires 21:00 UTC. No *fresh* short E0 this hour (07:00 1H: SHORT-confirm none, LONG-confirm pin-bull) → no new limit. COUNTER LONG 0.6980–0.7000 ~70p above → NO TRADE. ⚠ Concentration: long-USD overlap w/ open USDCHF long (advisory, keep-USDCHF by EC). ⚠ RBA 06-16.

---
### 2026-06-15 09:50 UTC hourly re-validate
Spot 0.70730 INSIDE SHORT 0.7065–0.7110. **Resting SELL 0.70902 (EC 6.5, from 07:16) still LIVE & intact** — V1b ✅ (H4 closes 0.70719/0.70730 < thr 0.71140), ADX 28.9 (<30). 08:00 1H = bearish pin (in-zone, order already working) → NO new order. COUNTER LONG 0.6980–0.7000 ❌ NO TRADE (away). ⚠ long-USD concentration w/ open USDCHF long (advisory). ⚠ RBA 06-16 if filled.

---
### 2026-06-15 10:14 UTC hourly re-validate
Fresh pull (10:13). Spot **0.70689** INSIDE SHORT 0.7065–0.7110. **Resting SELL 0.70902 (EC 6.5, from 07:16) still LIVE & intact** — V1b ✅ (H4 closes 0.70719/0.70689 < thr 0.71140), ADX 28.9 (<30 veto). 09:00 1H = LONG engulf (wrong dir for the short) → NO new order. COUNTER LONG 0.6980–0.7000 ❌ NO TRADE (~70p above). ⚠ long-USD concentration w/ open USDCHF long (advisory). ⚠ RBA 06-16 if filled.

---
### 2026-06-15 11:21 UTC hourly re-validate
Fresh pull (11:2x). Spot **0.70717** INSIDE SHORT 0.7065–0.7110. **Resting SELL 0.70902 (EC 6.5, from 07:16) still LIVE & intact** — V1b ✅ (H4 closes 0.70719/0.70717 < thr 0.71140), ADX 28.9 (<30 veto). 10:00 1H = no confirm fired (RSI 61) → NO new order. COUNTER LONG 0.6980–0.7000 ❌ NO TRADE (~70p above). ⚠ long-USD concentration w/ open USDCHF long (advisory). ⚠ RBA 06-16 if filled.

---
### 2026-06-15 12:30 UTC hourly re-validate → LIVE LIMIT UNCHANGED
Fresh pull (12:27). Spot **0.7067**, INSIDE SHORT 0.7065–0.7110 (drifted to zone bottom). **LIVE ORDER LIMIT SELL 0.70902** (placed 07:16, EC 6.5) — **NOT filled** (max high since placement < 0.70902 trigger), **V1b ✅ intact** (last 2 H4 closes 0.70717/0.7067 « threshold 0.7114), no V3 today → limit stands, expires 21:00 UTC. No fresh short E0 (12:00 1H RSI 59/Stoch 54 — no confirm). COUNTER LONG 0.6980–0.7000 ~67p above → NO TRADE. ⚠ Concentration: long-USD overlap (advisory, no auto-skip). ⚠ RBA 06-16 — if filled, flatten/manage before ~03:30 UTC (order expires 21:00 UTC tonight, won't place live into RBA).

---
### 2026-06-15 14:11 UTC hourly re-validate → LIVE LIMIT UNCHANGED
Fresh pull (14:07). Spot **0.70757**, INSIDE SHORT 0.7065–0.7110. **Resting SELL 0.70902 (EC 6.5, from 07:16) still LIVE & NOT filled** — max 1H high since placement 0.70769 « 0.70902 trigger; **V1b ✅ intact** (last 2 H4 closes 0.70717/0.70757 « thr 0.7114), ADX 28.9 (<30 veto), no V3 today → stands, expires 21:00 UTC. 13:00 1H: no SHORT confirm (RSI 61) → no new order. COUNTER LONG 0.6980–0.7000 ~76p above → ❌ NO TRADE.
> [!note] Concentration advisory now **CLEARED** — the open USDCHF long that this short stacked against was stopped out 11:18 UTC (see trades_log). fx_exposure: only AUDUSD short live → **INDEPENDENT**.
⚠ RBA 06-16 — order expires 21:00 UTC tonight (won't sit live into the decision); if it FILLS today, flatten/manage before ~03:30 UTC.


---

## Hourly re-validation — 2026-06-15 15:14 UTC
Spot **0.70859**. Live **SELL limit 0.70902 still WORKING** — max high since placement **0.70880** (tagged 0.70880 @15:00, ~2p short of fill), **NOT filled**. V1b ✅ intact (last 2 H4 closes 0.70717/0.70859 vs threshold 0.71140). No new E0. H4 Stoch 89 OB. Limit stands, expires 21:00 UTC. ⚠ If filled today, carries into RBA 06-16 — operator: consider flatten <03:30 UTC. **✅ ORDER LIMIT (working)**.
