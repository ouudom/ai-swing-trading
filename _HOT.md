# _HOT — Session State
*Always current. Updated at end of every session.*

## Open Position
None

## Active Forecast
[2026-W22](forecasts/weekly/2026-W22.md) — BEARISH / MEDIUM-HIGH macro, ALIGNED MTF, conviction MEDIUM-HIGH.

- **Setup A** [8.0/10]: SELL limit **$4590.24** ($4575 + $15.24 OUTWARD) zone $4530–$4575 | SL **$4615.64** | TP $4501.11 (**3.51R**) | **0.78 lots** — ✅ **ORDER LIMIT PLACED** (val 10.0/10, H1 bearish engulfing 2026-05-25 23:00). Expires 2026-05-26 21:00 UTC.
- **Setup B** [5.5/10]: SELL zone $4690–$4720 | TP $4607.50 — **WATCH** (val 10.0/10 but zone unreachable, spot $4536 = ~$154 below)
- **Setup C**: NONE — macro MEDIUM-HIGH disqualifies; no RSI divergence

`stop_distance = avg(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)`. Today: D1_ATR $88.77 → 0.5×D1 $44.38. H4_ATR trading-only $25.87. Setup A structural $5.94 (pivot $4580.94 May 25 20:00). avg($44.38, $25.87, $5.94) = $25.40. Offset (10−8)×0.3×25.40 = $15.24.

## Week Status
- Week: 2026-W22
- Trades taken: 0 filled / 1 live limit (Setup A)
- Risk allocated: $2000 / $4000 cap (Setup A active)

## Pending Actions
- Monitor Setup A live limit at $4590.24. Cancel if not hit by 21:00 UTC today.
- Setup B WATCH — no action unless price rallies $154+ into $4690–$4720 zone.
- **HARD BLOCK Thu 2026-05-28 12:30 UTC**: PCE Deflator + GDP 2nd Release — cancel any live limits by 10:30 UTC
- Mon 2026-05-25: US Memorial Day — reduced CME liquidity, wider spreads expected
- Watch DFII10: above 2.25% = strengthens BEARISH; below 2.00% = softens
- Watch DXY (ICE): above 100 = additional pressure; below 98 = relief
- **COT context (as of 2026-05-19):** Spec net +148,660 — crowded long, declining from peak +165,174 (May 12). Unwind in progress. BEARISH-supportive. Was showing N/A due to bug — now fixed.
- **GLD holdings:** 1,052.56t, AUM $153.5B — no ETF capitulation. Neutral (no outflows = spec longs not yet exiting en masse).
- ~~Repair COT + GLD fetch~~ ✅ Fixed 2026-05-26: COT via CFTC yearly zip (`deahistfo{year}.zip`), GLD via yfinance totalAssets + spot → tonnes, history accumulated in `data/gld_holdings.csv`.
- ~~Repair TD rate limit~~ ✅ Verified 2026-05-26: only 1 TD call per pull (15M, resampled locally). Original "9 credits/min" claim was stale/wrong.

## Last Session
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
