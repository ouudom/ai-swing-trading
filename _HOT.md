# _HOT — Boot State (thin)
*First file read each session. Pointers + non-derivable judgment only.*
*RULE: **never store a value that can be computed from source** — no live R, SL-hit status, spot,
EC, ATR, ADX, V1b status, zone prices, lots. Those live in the replay tables / `forecasts/*` / the
pull and must be recomputed, never cached here. This file = current week + open human decisions +
watch notes + where to look. Hard cap **40 lines.** Prune every session.*

## Source of truth — read these, don't duplicate them here
- **System P&L / would-be R / gate accuracy** → `trade_outcome` table in `data/database/index.db`
  (`bash scripts/pyrun.sh scripts/trade_outcome.py`; entry-mechanics replay — no hand-logged trades).
- **Current zones / forecasts** → `forecasts/weekly/{inst}/2026-W26.md` (PENDING)
- **Shadow ledger / calibration** → `zone_ledger`/`zone_outcome` tables, `wiki/system/core/calibration.md`
- **Latest validations** → `forecasts/daily/{inst}/2026-06-26.md`
- **Macro baseline** → `wiki/system/core/macro/yield_environment.md`

## Current week — W26 LIVE (Mon 06-22 → Fri 06-26). weekly_reforecast_count = 0.
All 11 forecasts published 06-21. Macro: hawkish FOMC USD-bull regime (DGS2 4.20, DXY slope +1.65).
W26 zones PENDING (read forecasts/weekly for exact boxes — never cache numbers here):
- xauusd SHORT ×2 (nearer-resistance fix) · gbpusd SHORT + COUNTER-LONG
- eurgbp SHORT(top) · usdchf LONG + COUNTER-SHORT · gbpjpy LONG(weak,capped)
- **INVALIDATED:** nzdusd PRIMARY-LONG (V1b 06-23 <0.5696) · eurusd COUNTER-LONG (V1b 06-23, 2 H4 closes <1.1415) · eurgbp SECONDARY-LONG (V1b 06-24 04:00, 2 H4 closes <0.8621: 0.86124/0.86129)
- **NO ZONES:** audusd (ADX31 trend) · usdcad (RSI85 blow-off, ADX41) · usdjpy + eurjpy (MoF HARD-BLOCK longs)

## Open human decisions
- none open.

## Watch / judgment notes
- **T6 re-forecast trigger live (D029):** DGS2 drift >0.15% from 4.20 OR DXY slope20 sign-flip → re-forecast USD pairs; counters opposed by a confirmed flip void on sight. Offset retune = D030 OPEN (deferred, n=1).
- **MoF regime ACTIVE (Katayama "decisive action" G7 06-19):** usdjpy + eurjpy longs HARD-BLOCKED; gbpjpy oscillates around the 214 level → CAUTION when <214 (cap LONG MEDIUM), HARD-BLOCK when ≥214 — recheck spot each run (213.15 @04:14 UTC = CAUTION, not hard-block). intervention_watch verified_through 2026-06-28.
- **Recurring lesson (xauusd W24+W25):** far-resistance shorts never fill in fast selloffs → W26 PRIMARY placed at nearer resistance.
- **Recurring lesson (eurusd/gbpusd/nzdusd):** counter-macro dip-buys into strong USD keep getting stopped → all W26 long-fades capped + lower zones + mandatory E0 reclaim.
- **usdcad/audusd:** strong ADX (>30) starves fades both ways — correctly NO ZONES; re-arm only when ADX cools or extreme appears.
- **E0 reclaim (D027):** PENDING ledger validation (pin/engulf fallback still counts).

## Last session
2026-06-26 — **DB recovered + project cleanup.** `index.db` was badly corrupt (Tree-10/ohlc, not
just news) → `.recover` into fresh DB (integrity ok), parked corrupt as `index.corrupt_*.db`. news
re-pulled (10 rows). Calibration refreshed → **Overall DEAD −4.5R / 19% / n=16** (the stale 06-21
stamp lied "WORKING"). New durability guard `scripts/db_guard.py` (checkpoint→check→backup) wired as
MANDATORY Step 0b in /weekly + /validate; db.py now busy_timeout+synchronous=NORMAL. weekly_pull.py
immutability guard added (refuses prior-day overwrite; restored clobbered W25 JPY trio). Logs +
trade_outcomes.csv un-tracked (gitignored). Removed 7 scratch scripts + docs/ orphan.
