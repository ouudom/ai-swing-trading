# _HOT — Boot State (thin)
*First file read each session. Pointers + non-derivable judgment only.*
*RULE: **never store a value that can be computed from source** — no live R, SL-hit status, spot,
EC, ATR, ADX, V1b status, zone prices, lots. Those live in the replay tables / `forecasts/*` / the
pull and must be recomputed, never cached here. This file = current week + open human decisions +
watch notes + where to look. Hard cap **40 lines.** Prune every session.*

## Source of truth — read these, don't duplicate them here
- **System P&L / would-be R / gate accuracy** → `trade_outcome` table in `data/database/index.db`
  (`bash scripts/pyrun.sh scripts/trade_outcome.py`; entry-mechanics replay — no hand-logged trades).
- **Current zones / forecasts** → `forecasts/weekly/{inst}/2026-W25.md` (W26 pending)
- **Shadow ledger / calibration** → `zone_ledger`/`zone_outcome` tables, `wiki/system/core/calibration.md`
- **Latest validations** → `forecasts/daily/{inst}/2026-06-19.md`
- **Macro baseline** → `wiki/system/core/macro/yield_environment.md`

## Current week — W25 CLOSED → W26 starts Mon 06-22
W25: 0 order limits all week. **5 invalidations** (4 at 02:57 UTC + NZDUSD COUNTER LONG V1b at 05:11 UTC).
**W26 macro rebase required:** DGS2 4.05→4.20, DXY slope20 +1.646 (hawkish FOMC/Warsh week).
JPY trio: assess post-BoJ; MoF regime still active (spot above triggers).

## Open human decisions
- none open.

## Watch / judgment notes
- **W26 USD pairs:** rebase DGS2 to 4.20. DXY +1.646 slope20 = strong USD. All forecasts must reflect.
  **NEW (D029):** T6 re-forecast trigger live — DGS2 drift >0.15% OR DXY slope20 sign-flip forces re-forecast; counters opposed by a confirmed flip void on sight. Offset retune = D030 OPEN (deferred, n=1).
- **EURGBP:** D1 CHoCH UP (06-18) + ECB 2.25% vs BoE hold. SECONDARY SHORT V1-invalidated. W26 range may have shifted UP. Reassess PRIMARY LONG zone level.
- **USDCHF:** Both W25 zones invalidated. DXY slope reversal = no short thesis. W26 = neutral/long reassess.
- **NZDUSD COUNTER LONG:** V1b INVALIDATED at 05:11 UTC (H4 closes 0.57369+0.57256 below thr 0.57460). W26 reassess needed (spot ~0.572; strong USD week).
- **CB cal:** update to cover W26 window before /weekly. RBNZ H2 / SNB Sep–Dec dates needed.
- **E0 reclaim (D027):** PENDING ledger validation (pin/engulf fallback still counts).

## Last session
2026-06-19 16:13 UTC — /validate hourly (W25 late-session). **0 order limits. 0 new invalidations.** All 8 standing zones out of range (fresh 16:00 bars confirm AUDUSD/EURGBP nearest, still outside). No CB decisions + no high-impact US releases in window. AUDUSD COUNTER LONG out-of-range (also ADX hard-veto). W25 zones expire 21:00 UTC tonight.
Prior (15:01 UTC): 0 limits, 0 invalidations. W25 total = 5 invalidations, 0 fills.
