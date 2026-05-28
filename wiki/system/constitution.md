---
type: system
updated: 2026-05-24
confidence: high
tags: [rules, risk, core]
related: [xauusd_profile, confluence_criteria]
---

# Trading System Constitution

## Identity
- Instrument: XAUUSD
- Style: Swing trading, discretionary
- Hold period: 2–10 days
- Timeframes: Weekly (bias) → Daily (setup) → H4 (limit placement + offset)

## Risk Rules — Non-Negotiable
- Risk per trade: $2000
- **No calendar trade cap** — bounded by weekly risk only
- Max loss per week: $4000 (= 2 losing trades). Hit → cancel all live limits, no new trades until Monday.
- Max loss per month: $10000
- Drawdown circuit breaker: account drops 5% from peak → $1000/trade until recovered
- Never widen a stop after entry
- Never move stop against the trade

Multiple trades same week allowed if (a) each setup independently passes /validate, (b) cumulative open risk + closed loss ≤ $4000, (c) no two trades same direction stacking (treated as one position).

## TP Structure
- TP: 3R → close full position (single exit, no split)
- TP must land at a structural level (prior swing, weekly pivot, Fib extension)
- Never set TP at arbitrary R-multiple with nothing structural there
- After entry: stop is fixed — never trail, never widen

## Position Sizing
```
structural_dist = entry − last_pivot_low (long) | last_pivot_high − entry (short)
                  last pivot within last 5 trading days (~30 H4 bars)

H4_ATR14        = ATR(14) computed on TRADING-DAY H4 bars only
                  (filter: bar range >= $1; excludes weekend/holiday flatline)
D1_ATR14        = ATR(14) on D1 bars

stop_distance   = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean of three
cap: if structural_dist > 3 × H4_ATR14 → skip trade (R:R collapses)
fallback: if no structural pivot within last 5 trading days (~30 H4 bars) → avg(0.5 × D1_ATR14, H4_ATR14)

lots = $2000 / (stop_distance × 100), round DOWN
Minimum: 0.01 lots (micro)

Example: D1_ATR=$70 → 0.5×D1=$35. H4_ATR (trading)=$31. structural pivot $50 below entry → structural_dist=$50.
stop_distance = avg($35, $31, $50) = $38.67
lots = 2000/(38.67×100) = 0.51 lots
```

Stop distance is the base unit for sizing AND for order-limit offset — see Entry Rules.

## Entry Rules — Order Limit with Daily Validation Gate

All entries use **order limits** (buy limit for longs, sell limit for shorts).
No market orders. No bar-close confirmation entries.

**Order placement is gated by daily validation — never placed Sunday without validation.**
**Order-limit price (offset) is computed at /validate time using that day's H4 ATR and structural pivot — never frozen from /weekly.**

```
Daily workflow (runs 07:30 UTC, before London open):
  1. Run /validate [date]
  2. Hard blocks (any fail = stop immediately):
       V1: D1 close beyond zone? → INVALIDATED (remove setup)
       V3: Hard news event within 2h? → NO TRADE
  3. Validation score (max 10.0) — XAUUSD (D017 reweight 2026-05-28):
       G1 H4+H1 structure aligned   4.0 pts
       G3 DFII10 slope supports     3.5 pts
       G2 D1 ATR compressed         1.5 pts
       V2 Macro drift OK            1.0 pts
       G5 VIX regime                VETO 0 pts (VIX>35 → shorts NO TRADE; logged)
       G6 Asia range                0 pts (logged as context)
  4. H1 trigger check (pin bar / engulfing / B&R on H1 inside zone)?

  → floor = 6.5 if ADX(14) D1 in 20–25 (transitional regime) else 6.0
  → OUTPUT (exactly one of):
     ✅ ORDER LIMIT: score ≥ floor + H1 trigger present
     👁 WATCH: score ≥ floor, no H1 trigger yet
     ❌ NO TRADE: score < floor or hard block triggered

  5. Order expires 21:00 UTC — re-validate next morning, never carry forward.
```

**Order limit placement — outward offset beyond zone extreme:**
```
entry_offset = (10 − confluence_score) × 0.25 × stop_distance

Short: limit_price = zone_top    + entry_offset    ← offset OUTWARD (above zone)
Long:  limit_price = zone_bottom − entry_offset    ← offset OUTWARD (below zone)

Direction: offset pushes limit AWAY from current spot, BEYOND zone extreme.
Lower confluence → bigger offset → price must overshoot zone further before fill.
Higher confluence → smaller offset → limit closer to zone extreme.

At score 10: offset = 0 → limit at zone extreme exactly.
At score 5.5: offset = 1.125 × stop_distance → limit 1.125 stop-units past extreme.
```

Rationale: offset = BUFFER. Forces price to commit OUTWARD (through zone extreme) before triggering. Earlier inward-offset (toward spot) produced premature fills on confirmed-rejection trades. Outward offset = strong-commitment filter — fewer fills, higher-quality entries. Backtest 2020–2026 (`scripts/sweep_entry.py`) confirmed: the offset is load-bearing — fill-at-trigger (no offset) loses money (PF 0.64), and per-trade PF rises monotonically with offset. Coefficient 0.25 chosen to favour trade quality over frequency (~2 trades/yr/instrument; aggregate frequency comes from running multiple instruments).

Stop distance drives sizing AND offset — see Position Sizing.

**Two distinct score thresholds — do not conflate:**
- Weekly confluence score (Signals 1–7, max 10.0): minimum **5.5/10** to include setup in forecast as PENDING. This is the setup quality floor — scored at /weekly time.
- Daily validation score (G1/G3/G5/G2/V2/G6, max 10.0): minimum **6.0/10** to place order. This is the daily gate — scored at /validate time.
A setup can score 5.5 weekly (barely qualifies) but still fail daily gate if market conditions deteriorate.
Counter (Setup C): **7.5/10** weekly floor + daily gate still applies.

**H1 trigger (entry confirmation, not confluence):**
Pin bar, engulfing, or break-and-retest inside zone on H1. Observed at /validate time only.
Trigger present → record in daily file as confirmation. Does NOT alter score or offset.
Trigger absent → output **WATCH** (conditions met, awaiting confirmation). Do not place limit yet.
Trigger present → output **ORDER LIMIT** (place the limit). Trigger is the final gate.

## Stop Placement

**Formula (updated 2026-05-25, triple-max):**
```
structural_dist = distance from entry to last pivot low below entry zone (long)
                  distance from entry to last pivot high above entry zone (short)
                  → use last pivot within last 5 trading days (~30 H4 bars) before entry

H4_ATR14        = ATR(14) on trading-day H4 bars only (range >= $1 filter)
D1_ATR14        = ATR(14) on D1 bars

stop_distance   = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)   ← arithmetic mean
lots            = $2000 / (stop_distance × 100), round DOWN
```

**Why arithmetic-mean of three:** Balances the three volatility/structure dimensions: intraday noise (H4 ATR), daily volatility (0.5×D1 ATR), and structural level (pivot). Single max-dominant or min-dominant approaches over- or under-shoot any one dimension. Average smooths regime extremes — stop never collapses to one signal alone.

**Trading-day filter for H4 ATR:** Weekend/holiday flatline bars (~$0.27 range) destroy the rolling ATR. Filter to bars with range >= $1.00 before computing — uses real movement only.

**Cap:** If structural_dist > 3 × H4_ATR14 → zone too wide, skip the trade (R:R collapses).
**Floor:** If structural_dist < 0.5 × H4_ATR14 → pivot inside noise, structurally irrelevant.
  1. First check yesterday's daily validation file (`forecasts/daily/[YESTERDAY].md`). If yesterday's `structural_dist` was valid (≥ 0.5 × H4_ATR14 at that time) AND the same pivot still exists in H4 data → **re-use yesterday's pivot reference** (setup zones are static through the week — pivot reference should be stable).
  2. If yesterday's also failed floor OR no prior validation file exists → fallback: `stop_distance = avg(0.5 × D1_ATR14, H4_ATR14)`.
**Fallback:** No structural pivot within last 5 trading days (~30 H4 bars) → stop_distance = avg(0.5 × D1_ATR14, H4_ATR14).

## Correlation Guard (multi-instrument)

Active once >1 instrument trades live. Prevents disguised double-bets on the same macro driver (USD).

```
usd_position(trade) = trade_dir(+1 long / −1 short) × USD_BETA_SIGN   (from instruments/{name}/config.py)
```
XAUUSD and EURUSD both have USD_BETA_SIGN = −1, so:
- XAUUSD short (+1) + EURUSD short (+1) = stacked LONG-USD bet.
- XAUUSD long (−1) + EURUSD long (−1) = stacked SHORT-USD bet.

**Rule:** across all open + pending/limit trades, two trades sharing the same `usd_position` sign = one correlated USD exposure, not two independent bets. When a new ORDER LIMIT would create same-sign stacking:
1. If combined risk would exceed $2000 → **halve both** to $1000 risk each (re-size lots), keeping net USD risk at one trade-unit; OR
2. reject the lower-confluence setup and keep the higher.
Opposite-sign trades (one long-USD, one short-USD) are a hedge — allowed at full size, no stacking penalty.

This guard is independent of the weekly $ risk cap — it bounds *correlation concentration*, not total dollars.

## No-Trade Rules
- No new entries 2 hours before any red-folder Forex Factory event
- Gold: NFP, FOMC, CPI, US Retail Sales are hard blocks — cancel any live limit orders
- If weekly $4000 loss limit hit: cancel all open limit orders, no new trades until Monday

## Weekend Gap Gate (Monday /validate only)

Computed at /weekly run from H4 data: Friday 20:00 UTC close vs first bar after Sunday reopen.

| |gap_pct| | Action |
|---|---|
| < 0.20% | Noise. Log only. Proceed normally. |
| 0.20–0.50% | Note in Monday /validate. No bias change. |
| 0.50–1.00% | **Warning** — re-examine weekly bias before /validate. Setup zones may need redraw. |
| > 1.00% | **Hard re-forecast** — run /weekly again Monday morning. Sunday forecast voided. |

Gap direction matters: large gap *in direction of weekly bias* = momentum confirm but worse fills (zones distant). Large gap *against bias* = potential invalidation.

**Cap exemption:** A weekend-gap re-forecast (>1.00% → Monday `/weekly` re-run) is a SEPARATE path from mid-week trigger re-forecasts. It runs BEFORE the week trades, replacing the Sunday forecast — it does NOT consume `weekly_reforecast_count`. The 1/week mid-week cap still leaves one mid-week re-forecast available after a Monday gap re-run.

## Mid-Week Re-Forecast Triggers

Sunday `/weekly` produces bias + setups assumed valid through Friday close. Mid-week re-forecast is **destructive** (cancels live limits, voids PENDING setups) — must be rare, rule-based, and confirmed, never feeling-based, to preserve edge.

### Triggers (all D1-close based, no intraday)

| Trigger | Threshold | Source |
|---|---|---|
| T1 — DFII10 1-day jump | abs(today − yesterday) > 0.10% | `data/fred/DFII10.csv` |
| T2 — DXY 1-day jump | abs(today − yesterday) > 0.75 ICE points | `data/yahoo/DXY.csv` (ICE DX-Y.NYB) |
| T3 — Gold counter-move | D1 close moves >2.5% AGAINST weekly bias | `data/twelvedata/xauusd/1day.csv` |
| T4 — Unscheduled macro shock (X OR Y, either fires) | X: structured news event today (see below) OR Y: VIX 1-day jump > 5.0 points | X: web search + operator log / Y: `data/fred/VIXCLS.csv` |
| T5 — DFII10 cumulative drift | abs(now − baseline) > 0.15% any direction | DFII10 vs `baseline_dfii10` in weekly frontmatter |

**T4 definition (X OR Y):**

**T4-X — Structured news event:**
- Tier-1 unscheduled event published TODAY by Reuters / Bloomberg / AP
- Allowed categories ONLY: central-bank emergency action (off-cycle rate move, QE/QT shock), declared war / major sanctions on G20 economy, Fed chair resignation or removal, sovereign default by major economy, major political shock (cancelled election, coup, impeachment vote)
- NOT allowed: analyst opinion, Fed-speak interpretation, rumor, scheduled commentary, "expected" events
- Trigger requires: write `data/news_events/[DATE]_t4x.json` (schema enforced by `scripts/check_structured_news_event.py`) + mirror summary to `_HOT.md` as `t4_x_event: {category, url, headline}`
- If operator cannot write valid JSON with source + headline → T4-X does NOT fire

**T4-Y — VIX jump:**
- `VIX(today) − VIX(yesterday) > 5.0 points`
- Pure data check, no operator input

T4 fires if X OR Y is true. Y catches market-priced shocks fast; X catches slow-moving geopolitical/policy events VIX hasn't priced yet. X's structured categories + verbatim logging requirement prevent discretion creep.

### Hard preconditions — re-forecast allowed if and only if ALL true

```
1. No open positions (filled trades). If any live position → never auto-reforecast.
   Re-forecast only acts on PENDING / WATCH setups and unfilled limit orders.

2. Day-of-week gate:
   - NOT Monday (Sunday's forecast is <24h old — let it settle)
   - NOT Friday (week ends in <48h — let setups expire naturally)

3. Event-proximity gate (forward-only, 12h):
   - >12h until next scheduled NFP / FOMC / CPI / US Retail Sales / GDP
   - Past events do NOT block — once the print is out, re-forecast may act on it.
   (block only the pre-event uncertainty window; post-event move is real, tradeable info)

4. Re-forecast spacing: >48h since last /weekly run.

5. Weekly cap: 0 prior mid-week re-forecasts this week.
   Second qualifying trigger same week → halt trading until Monday. System resets.
```

### Trigger logic — when preconditions pass

```
IMMEDIATE re-forecast if ANY of:
  (a) Two concurrent triggers fire same day from {T1, T2, T3, T4}
      (e.g., T1 + T3, or T2 + T4, etc — coherent multi-asset shift)
  (b) T5 fires alone (already-sustained cumulative drift)

CONFIRMATION re-forecast if:
  (c) Single trigger from {T1, T2, T3, T4} fires today
      → log as WARN in _HOT.md, set pending_reforecast_check = [TRIGGER, DATE]
      → at next /validate (next morning), recheck same trigger:
        - Still firing → re-forecast NOW
        - Mean-reverted → clear WARN, continue normally

If preconditions fail → log trigger fires to _HOT.md as INFO only, no action.
```

### Protocol when re-forecast executes

1. Cancel ALL live limit orders immediately
2. Remove all PENDING / WATCH setups from `_HOT.md`
3. Run `/weekly` with current data (overwrites week's macro environment file in place)
4. Original Sunday forecast file is **not** edited — annotate in `_HOT.md`:
   `MID-WEEK RE-FORECAST [DATE], trigger=[Tx/Tx], original [YYYY-WNN] voided`
5. Increment `weekly_reforecast_count` in `_HOT.md` (max 1)
6. New setups land as PENDING — halt today's `/validate`, resume normal flow next morning
7. Re-forecast is **week-scoped**: tagged to current `YYYY-WNN`, voided at week market close
   (CME Globex Fri 22:00 UTC). It carries NO weight into the next week.

### Re-forecast lifecycle / expiry

- A mid-week re-forecast inherits the current week (`YYYY-WNN`). Its setups + voiding of the
  original Sunday forecast apply ONLY through Friday market close (CME Globex Fri 22:00 UTC).
- New week ALWAYS requires a fresh Sunday `/weekly` — never carry a mid-week re-forecast forward.
- `weekly_reforecast_count` resets to 0 at each new week's `/weekly` run.
- At Friday close: all unfilled limits expire, PENDING/WATCH setups clear, count resets.

### Edge preservation rules

- Maximum **one** mid-week re-forecast per week. Second qualifying trigger → STOP trading until Monday.
- Re-forecast cannot revive an INVALIDATED setup — invalidation is final.
- Open positions are NEVER auto-touched by re-forecast. Stops manage live trades.
- No manual / discretionary mid-week reset path exists. Every override leaks edge over time.
- Lag is acceptable: confirmed regime shift recognized 24h late beats false reset 4× per year.

## Real-Yield Baseline Drift (every /validate)

Forecast frontmatter stores `baseline_dfii10` (real yield at Sunday data pull).
Daily DFII10 vs baseline:

| |Δ DFII10| | Action |
|---|---|
| < 0.05% | Macro unchanged. Pass Check 2. |
| 0.05–0.10% | Note in daily file. Still pass if direction supports bias. |
| > 0.10% | **Macro check 2 FAILS** if drift is against trade direction. HOLD. |
| > 0.15% any direction | **Force re-forecast** regardless of direction (regime shift). |

## Invalidation
A setup is cancelled when:
- **V1 — Daily close beyond zone:** any D1 close outside zone extreme → cancel.
- **V1b — Intraday H4 invalidation (added 2026-05-26):** TWO consecutive H4 closes beyond zone (>$5 past extreme) → cancel live limit, remove from `_HOT.md`. Check at each H4 boundary (00, 04, 08, 12, 16, 20 UTC). Catches breakouts before D1 close confirms.
- Macro bias reverses (real yields spike against trade direction)
- Weekly structure breaks (trend structure violated)

> **Liquidity Sweep Exception:** A wick penetration of the setup zone that closes back inside (same candle or next) is NOT invalidation — it's a Wyckoff Spring / stop hunt. Require either (a) D1 *close* beyond zone OR (b) TWO consecutive H4 closes beyond zone (V1b) before cancelling. A single H4 wick + close-back-inside = sweep, not invalidation.

## Setup Types

| Setup | Direction | Min Score (out of 10) | Extra Rules |
|---|---|---|---|
| A — Primary | With weekly bias | 5.5 | Best confluence zone |
| B — Secondary | With weekly bias | 5.5 | Alternative price path, distinct zone |
| C — Counter | Against weekly bias | 7.5 | Signal 3 mandatory; macro must be LOW/MEDIUM confidence only; cap 40% zone width |

Max 3 setups per week. If no valid setup for a slot → NONE (never force).
Trades executed bounded by $4000 weekly risk cap, not by setup count.
Priority A → B → C only governs entry preference if multiple fill same day. Independent setups may fill across the week.

## The Three Laws
1. Risk management > TA method
2. No confluence = no trade. Waiting is a position.
3. If you can't write the IF/THEN in one sentence, the setup isn't ready.
