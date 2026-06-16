---
type: daily_validation
instrument: eurgbp
date: 2026-06-16
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
# Validation — 2026-06-16 (eurgbp, [[2026-W25]])

Fresh pull 02:25 UTC; re-validated 03:16 UTC (hourly run). Only non-USD pair this week, so checked in full. Re-run: spot ~0.8645 (latest closed H4 0.86407), still mid-range between zones; V1b intact both sides (LONG thr 0.86040 / SHORT thr 0.86860); no shock in news (Iran-US deal optimism, ECB-hike tilt — all known). Verdict unchanged → NO TRADE.

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 0.86458 | mid-range, between zones |
| H4 ATR (trading) | 0.00117 | SL floor = H4 ATR (0.5×D1 0.00114 < H4) |
| D1 ATR | 0.00228 | median 0.00329 → COMPRESSED |
| ADX(14) D1 | 14.3 | RANGING → floor 6.0 |
| D1 structure | DOWN (BOS @0.86312) | H4 CHoCH UP @0.86406 |
| TTM squeeze | ON — D1 (2b) + H4 (16b) | compression, no expansion |

## Q1+Q2 — Hard Blocks
- **V1** intact (no D1 close beyond either zone). **V1b** intact both: LONG thr 0.86040 ✅ / SHORT thr 0.86860 ✅.
- **V3 — pre-event carry block.** UK CPI y/y **2026-06-17 06:00 UTC** is a UK tier-1 release on eurgbp's hard-block list; BoE 06-18; FOMC 06-17 (caution, transmits). A limit filled today carries **unattended into UK CPI tomorrow morning** → NO new order in this automated run.
- No VIX veto (cross). No macro flip (cross macro non-scoring; rate-diff thin).

## Q3 — Re-Forecast
No price/macro trigger fired (counter-move <1.5%, no shock). Action: NONE.

## Q4 — Entry Confluence (both below floor anyway)
- **LONG 0.8608–0.8625 (best, ZC 8.5)** — price ~21p **above** zone top; no at-zone bullish E0; D1 Stoch 27/W%R −64 (mid, not oversold). EC well under floor 6.0 → ❌.
- **SHORT 0.8664–0.8682** — price ~18p **below** zone bottom; no at-zone bearish E0 (H4 CCI 139 overbought is the only lean, but price not at zone). EC under floor → ❌.

## Result
NO TRADE — pre-UK-CPI (06-17) / pre-FOMC carry block; both zones also untriggered (price mid-range, no E0, EC below floor). Zones remain **PENDING**, V1b intact.

> _Hourly re-run 2026-06-16 05:09 UTC — gates re-confirmed (CB calendar: BoJ+RBA today, FOMC 06-17 18:00 blocks all 8 USD pairs, BoE+SNB 06-18; eurgbp pre-UK-CPI 06-17). No fresh T4-X shock (news store 06-15 carryover, US-Iran deal calming/ongoing). No new D1 close mid-session; zones intact. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 06:09 UTC — gates re-confirmed unchanged (BoJ+RBA today, FOMC 06-17 18:00 blocks all 8 USD pairs, BoE+SNB 06-18). No fresh T4-X shock; no new D1 close since prior run. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 07:09 UTC — gates re-confirmed unchanged (BoJ+RBA today, FOMC 06-17 18:00 blocks all 8 USD pairs, BoE+SNB 06-18; eurgbp pre-UK-CPI 06-17; JPY trio MoF HARD_BLOCK longs + NO ZONES). No fresh T4-X shock; no new D1 close since prior run. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 08:09 UTC — gates re-confirmed unchanged (CB cal: BoJ+RBA today, FOMC 06-17 18:00 blocks all 8 USD pairs, BoE+SNB 06-18; econ cal: BoJ presser today, UK Bank Rate 06-18, NZ GDP 06-17; JPY trio MoF HARD_BLOCK longs + NO ZONES). No fresh T4-X shock (US-Iran deal carryover). No new D1 close since prior run; zones intact. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 09:10 UTC — gates re-confirmed via scripts, unchanged (CB cal: BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal: UK CPI 06-17 06:00, NZ GDP 06-17 22:45, FOMC presser 06-17 18:30; intervention watch: usdjpy/eurjpy/gbpjpy MoF jawboning CAUTION + JPY trio NO ZONES/BoJ HARD). No fresh T4-X shock (US-Iran deal carryover, news store latest 06-15 21:20). No new D1 close since prior run (next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 10:11 UTC — gates re-confirmed via scripts, unchanged (CB cal: BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal: UK CPI 06-17 06:00, NZ GDP 06-17 22:45, FOMC presser 06-17 18:30; intervention watch: usdjpy/eurjpy/gbpjpy MoF jawboning CAUTION + JPY trio NO ZONES/BoJ HARD). No fresh T4-X shock (US-Iran deal carryover, news store latest 06-15 21:20). No new D1 close since prior run (next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Verdict unchanged → NO TRADE._
> _Hourly re-run 2026-06-16 11:44 UTC (new-DB canonical-read verification) — gates re-confirmed via scripts against `data/database/index.db` (rebuilt 11:32 UTC): CB cal BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal UK CPI 06-17 06:00, NZ GDP 06-17 22:45, FOMC presser 06-17 18:30; intervention watch usdjpy/eurjpy/gbpjpy MoF jawboning CAUTION + JPY trio NO ZONES/BoJ HARD. DB read path verified (db.read_ohlc / read_slice serve fresh OHLC+macro+market for all instruments; trade table clean, no open positions). No fresh T4-X shock; no new D1 close since prior run (next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 13:58 UTC — gates re-confirmed via scripts, unchanged (CB cal: BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal: UK CPI 06-17 06:00, NZ GDP 06-17 22:45, FOMC presser 06-17 18:30; intervention watch: usdjpy/eurjpy/gbpjpy MoF HARD_BLOCK longs + JPY trio NO ZONES/BoJ HARD). BoJ HIKED today, yen steady (no MoF slam — news 06-16 09:32); no fresh T4-X shock. No new D1 close since prior run (next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 16:06 UTC — gates re-confirmed via scripts, unchanged (CB cal: BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal: UK CPI 06-17 06:00, FOMC presser 06-17 18:30; intervention watch: usdjpy @154 clear of band, MoF jawboning CAUTION + JPY trio NO ZONES/BoJ HARD). BoJ HIKED, yen steady (no MoF slam); no fresh T4-X shock (news latest 06-16 10:38). No new D1 close since prior run (last D1 bar 06-16 00:00, next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Trade table clean (no open positions). Verdict unchanged → NO TRADE._

> _Hourly re-run 2026-06-16 17:13 UTC — gates re-confirmed via scripts, unchanged (CB cal: BoJ+RBA today HARD, FOMC 06-17 18:00 → all 8 USD pairs pre-event carry block, BoE+SNB 06-18; econ cal: UK CPI 06-17 06:00, FOMC presser 06-17 18:30; intervention watch: usdjpy ~154 clear of band, MoF jawboning CAUTION + JPY trio NO ZONES/BoJ HARD). BoJ HIKED, yen steady (no MoF slam); no fresh T4-X shock (news store latest 06-16 carryover, US-Iran deal calming). No new D1 close since prior run (next 00:00 UTC 06-17); zones intact, V1/V1b unchanged. Trade table clean (no open positions). Verdict unchanged → NO TRADE._

> **— D028 LIVE PASS 2026-06-16 18:50 UTC (carry block relaxed → per-zone EC) —** NO TRADE — SECONDARY SHORT 0.8660–0.8682 (1.21 H4ATR below spot 0.86472): D1 mildly OVERSOLD (Stoch27/W%R−65/CCI−29 — wrong side for a short), no E0; EC < 6.0 floor. PRIMARY LONG 0.8608–0.8625 far (2.1 ATR). _Gates: VIX 16.2 (no veto); FOMC Wed 18:00 = forward-carry (allow+flatten 17:00 Wed), gbpusd/eurgbp gated earlier by UK CPI Wed 06:00 (flatten 05:00 Wed); own-CB-today (RBA→audusd) + JPY NO ZONES stay hard. No fresh T4-X shock; no new D1 close (next 00:00 UTC 06-17)._
