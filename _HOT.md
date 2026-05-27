# _HOT — Session State
*Always current. Updated at end of every session.*

## Open Position
None

## Active Forecast
[2026-W22](forecasts/weekly/2026-W22.md) — BEARISH / MEDIUM-HIGH macro, ALIGNED MTF, conviction MEDIUM-HIGH.

- **Setup A** [8.0/10]: SELL limit $4590.24 — ❌ **EXPIRED UNFILLED** 2026-05-26 21:00 UTC. Today's high $4561.36 (28.88 below limit). Direction thesis ✅ (D1 close $4504.56 dropped through zone) but entry missed. Risk $2000 released.
- **Setup B** [5.5/10]: SELL zone $4690–$4720 | TP $4607.50 — **WATCH** (val 10.0/10 but zone unreachable, spot $4504 = ~$186 below)
- **Setup C**: NONE — macro MEDIUM-HIGH disqualifies; no RSI divergence

`stop_distance = avg(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)`. Today 17:38 UTC: D1_ATR $96.04 → 0.5×D1 $48.02. H4_ATR trading $26.44. Setup A structural $5.94 (pivot $4580.94). avg = $26.80. Offset $16.08, revised limit $4591.08/SL $4617.88/0.74 lots — drift <$1 on limit, live order kept ($4590.24/$4615.64/0.78 lots).

## Week Status
- Week: 2026-W22
- Trades taken: 0 filled (Setup A limit expired unfilled 2026-05-26 21:00 UTC)
- Risk allocated: $0 / $4000 cap

## Pending Actions
- Setup A closed (expired). Bearish move ran without retest — review: 0.3 offset coef priced fill above realized high $4561.36. Consider tighter offset or H1-trigger-only entry for next setup.
- Setup B WATCH — no action unless price rallies $186+ into $4690–$4720 zone.
- **HARD BLOCK Thu 2026-05-28 12:30 UTC**: PCE Deflator + GDP 2nd Release — cancel any live limits by 10:30 UTC
- Mon 2026-05-25: US Memorial Day — reduced CME liquidity, wider spreads expected
- Watch DFII10: above 2.25% = strengthens BEARISH; below 2.00% = softens
- Watch DXY (ICE): above 100 = additional pressure; below 98 = relief
- **COT context (as of 2026-05-19):** Spec net +148,660 — crowded long, declining from peak +165,174 (May 12). Unwind in progress. BEARISH-supportive. Was showing N/A due to bug — now fixed.
- **GLD holdings:** 1,052.56t, AUM $153.5B — no ETF capitulation. Neutral (no outflows = spec longs not yet exiting en masse).
- ~~Repair COT + GLD fetch~~ ✅ Fixed 2026-05-26: COT via CFTC yearly zip (`deahistfo{year}.zip`), GLD via yfinance totalAssets + spot → tonnes, history accumulated in `data/gld_holdings.csv`.
- ~~Repair TD rate limit~~ ✅ Verified 2026-05-26: only 1 TD call per pull (15M, resampled locally). Original "9 credits/min" claim was stale/wrong.

## Last Session
2026-05-27 (/validate 09:06 UTC) — Spot $4505.42. Setup A gone (expired 05-26). Setup B WATCH 10.0/10 (G1✅ G3✅ G2✅ V2✅) but zone $4690–$4720 unreachable ($185+ above spot). H4 ATR $26.73, D1 ATR $92.11<97.40 compressed, DFII10 2.16% slope +0.25 drift −0.02 vs baseline 2.18. V1/V1b/V3/G4 all pass. Thu 05-28 12:30 UTC PCE+GDP = hard block — cancel any future limit by 10:30 UTC. D018 saved to forecasts/daily/2026-05-27.md.

2026-05-26 (/validate 23:53 UTC EOD review) — Setup A limit $4590.24 EXPIRED UNFILLED at 21:00 UTC. Today's high $4561.36 = $28.88 below limit. D1 close $4504.56 dropped through zone_bottom $4530 — bearish thesis ✅ but entry missed. Outward 0.3 offset priced fill above realized high. Setup A removed from pending; $2000 risk released. Setup B still WATCH (zone $4690-$4720 unreachable, spot ~$186 below). Week: 0 trades filled. D017 logged.

2026-05-26 (/validate 17:38 UTC re-check) — Fresh pull. Spot $4536.48. V1 ✅ (D1 May 25 close $4561.87 in zone; today's D1 forming $4536.48 above zone_bottom). V1b ✅ (H4 closes 00/04/08 = $4542/$4538/$4536, all below $4575). V3 ✅ (no NFP/FOMC/CPI/Retail today). G4 — outside 17:00 cutoff but limit already placed, monitoring only. Score 10.0/10. Fresh H1 trigger 08:00 UTC bearish engulfing ($4538→$4523, engulfs $6 bull body). D1 ATR jumped $88.77→$96.04 (today's $48 sweep range). Stop drift $25.40→$26.80, revised limit $4591.08 — <$1 diff from placed $4590.24, kept live. ORDER LIMIT CONFIRMED. D016 logged.

2026-05-26 (/validate 06:16 UTC re-check) — Fresh pull (10 new 15M bars to 06:15 UTC). Spot $4531.14. V1 ✅ (D1 close May 25 $4561.87 inside zone; intraday low $4524 = Wyckoff spring, closed back above $4530), V1b ✅ (H4 closes $4542/$4531 both below zone_top), V3 ✅, 10.0/10 score unchanged. NEW H1 trigger: 04:00 bearish engulfing ($18 body engulfs $9 prior) at bar #3 — supersedes the 23:00 May 25 trigger at recency boundary. Stop drift: $25.40→$25.60 (+$0.20, immaterial). ORDER LIMIT $4590.24 CONFIRMED. $59 below spot — rally needed to fill. D015 appended to 2026-05-26.md.

2026-05-26 (COT analysis + bug fix) — fetch_cot() was mixing main GOLD + MICRO GOLD rows (same date, different contracts). Bug caused spurious net_prev = -24k vs net +148k = fake +172k swing. Fixed: exact match "GOLD - COMMODITY EXCHANGE INC." only. Real W/W change: −16,514 (DECLINING from peak 165k May 12). COT BEARISH-supportive, not conflicting. W22 forecast Positioning section + frontmatter corrected. DXY baseline corrected FRED 119 → ICE 99.239 in W22 frontmatter.

2026-05-26 (system improvements) — Implemented: (1) COT fetch via CFTC yearly zip `deahistfo{year}.zip` → working, latest 2026-05-19 spec net +148,660 BULLISH (conflicts BEARISH thesis — investigate). (2) GLD fetch via yfinance totalAssets + spot → 1052t, AUM $153.5B, history in `data/gld_holdings.csv`. (3) DXY migrated to ICE via yfinance `DX-Y.NYB` → 99.239. Dropped FRED DTWEXBGS. (4) Pivot window widened 20 H4 bars → 5 trading days (~30 H4 bars). (5) V1b mid-day H4 invalidation rule + `scripts/check_v1b.py`. (6) H1 trigger recency cap ≤8 bars. (7) New backtest strategy `s_weekly_swing_v1` mirrors live formula — 22 trades 2020-2026, +$18k from $100k. (8) `scripts/log_trade.py` + `data/trades_log.csv`. (9) Stale TD rate-limit pending action removed (verified 1 call/pull). #10 backtest divergence resolved.

2026-05-26 (/validate) — Spot $4536.27 inside Setup A zone. Validation 10.0/10 (G1 H4+H1 LH+LL ✅, G3 DFII slope +0.29 ✅, G2 D1 ATR 88.77<97.40 ✅, V2 drift 0.000 ✅). H1 trigger ✅ bearish engulfing at 2026-05-25 23:00 (body $13.91 engulfs prior $4.32 bullish, closes inside zone). Stop $25.40, offset $15.24, limit $4590.24, SL $4615.64, TP $4501.11, 3.51R, 0.78 lots. **ORDER LIMIT PLACED**. Setup B WATCH (zone unreachable). D014 logged.

2026-05-25 (/validate formula update v3) — Offset coefficient 0.2 → 0.3. Setup A: offset $16.98, limit $4591.98, SL $4620.28, 0.70 lots, 3.21R. Setup B: offset $44.86, limit $4764.86, SL $4798.09, 0.60 lots, 4.74R. Both WATCH. D013 logged.

2026-05-25 (/validate formula update v2) — Stop formula `avg(...)` arithmetic mean. Offset reinstated outward at 0.2 coef. D012 logged.

2026-05-25 (/validate formula update v1) — Stop formula `max(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)`. H4 ATR computed on trading-day bars only (range>=$1 filter, drops weekend/holiday flatline). Order limit at zone extreme (no inward offset). Setup A: limit $4575 / SL $4610.24 / 0.56 lots / 2.10R. Setup B: limit $4720 / SL $4755.24 / 0.56 lots / 3.19R. Both WATCH. Constitution + confluence_criteria + validate.md + weekly.md + templates + stop-loss research doc + CLAUDE.md all updated.

2026-05-25 (/validate re-run with fresh Twelve Data pull) — Spot $4563.16 (was stale $4505.72 in earlier pull). Sun-CME +1.46% gap-up (Fri $4505.73 → Mon open $4571.57) put price inside Setup A zone pre-confirmation. G1 broken: H1 = bullish breakout/consolidation, not LH+LL. Score downgraded to 6.5/10 (G1 ❌, G3/G2/V2 ✅). V1 still intact (D1 close $4568.58 inside zone, today wick $4577.53 closed back to $4563.16). Setup A → WATCH pending bearish H1 trigger. Setup B unreachable. INVALIDATION line: D1 close > $4593.46.

2026-05-25 (/validate, stale data) — Both setups WATCH. Validation 10.0/10 (G1 H4 LH+LL ✅, G3 DFII10 slope +0.290 ✅, G2 D1 ATR compressed ✅, V2 drift 0.000 ✅). Hard blocks all pass (V1 D1 close $4505.72 below zones, V3 Memorial Day no news, G4 session). H1 trigger absent — tape frozen since Sat 22:00 UTC through Memorial Day. H4 ATR live calc $5.42 distorted by flatline weekend bars → used $27.51 from last active period. Setup A limit $4570.38 / 0.86 lots / SL $4593.46 / TP $4501.11 ready to place on H1 trigger. Setup B zone unreachable ($200 above spot). Re-validate 08:00 UTC.

2026-05-25 (automated /weekly re-run) — Forecast file was missing (deleted). Re-ran full 5-agent analysis. Pull successful: price $4505.72, RSI 39.6 (no div), ADX 26.3 (trending), D1 ATR compressed ($72.46 < median $75.58), EMA200 $4541.88 above price, weekend gap −0.001% (noise). COT/GLD fetch both failed again. Core PCE Q1 +4.3% YoY confirmed via web search — materially above Fed 2% target, strengthens Warsh hike case. Setup A recalculated: limit $4570.38, SL $4593.46 (structural), stop_dist $23.08, TP $4501.11 (2.89R). Setup B unchanged. Forecast saved to forecasts/weekly/2026-W22.md.

2026-05-22 — Major speed optimization on `backtest.py` (4-5× faster). Replaced pandas datetime slicing with numpy `searchsorted` + boolean arrays in `ExecutionEngine`. Per-week M1 slicing instead of scanning full 2.8M-row dataframe. Weekend gap check also vectorized. 2-year backtest: ~20s → ~5s. 8-year backtest: ~5.5min → ~1.5min expected.
