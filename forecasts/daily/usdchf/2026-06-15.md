---
type: daily_validation
instrument: usdchf
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
| Spot | 0.79461 | — |
| H4 ATR (trading) | 0.00198 | — |
| D1 ATR | 0.00523 | median 0.00455 → EXPANDING |
| VIX | 19.44 | no FX veto (<35, spike<3) |
| ADX(14) D1 | 23.3 | TRANSITIONAL → floor 6.5 |
| Weekend gap | -0.401% | NOTE |
| DXY 20d slope | DOWN | aligns SHORT (the pair's live macro) |

## Q1+Q2 Hard Blocks
V1 intact · V1b intact · V3 clear (CB events Tue/Wed/Thu — today's limits expire 21:00 UTC tonight,
before any decision; today's London/NY opens are clear) · no VIX veto · no macro flip.

## Q3 Re-Forecast
Monday weekend-gap gate: -0.401% → NOTE. No re-forecast.

## Q4 Entry Confluence — per zone
**SHORT 0.8005–0.8025 (SNB-cap, 8.5)** — EC **3.5/10** (floor 6.5) → ❌ NO TRADE. DXY 20d slope down aligns short (E2✅1.5) + ADX<25 (E4✅) + structure (E5✅) — but price ~60–80p below zone falling AWAY, H1 oversold not overbought (E1 fail), no E0. SNB Thu. E2+E4+E5.

> Econ-calendar CSV stale → web-search fallback used; no tier-1 data within 2h of
> today's opens. CB decisions (the hard events) covered by the static CB-calendar gate: all Tue+.

## Result
NO TRADE on every zone — Entry Confluence below floor. Price mid-range / away from zones with no
at-zone reversal confirmation (E0) and D1/H1 oscillators not aligned. Zones remain PENDING.

---
### Hourly re-validation — 2026-06-15 03:14 UTC
spot 0.79421 — well below SHORT 0.8005–0.8025; open operator LONG 0.79477 ≈flat (SL/BE intact, decision pending). NO TRADE (no new limit).

### Hourly re-validation — 2026-06-15 07:16 UTC
Fresh pull 07:12. Spot **0.79304**. SHORT 0.8005–0.8025: ~75p BELOW zone; H4 W%R −93.7 / CCI −167.6 OVERSOLD = bounce setup (opposite of short), LONG RSI-reclaim+band-reclaim E0 fired → **NO TRADE** (no long zone published). ⚠ **Open long 0.79477**: spot 0.79304 now ~−17p (≈−0.7R) below entry, still above SL 0.79234, BE not hit; thesis flipped bearish — operator exit decision pending. ADX 23.3 transitional. FOMC Wed + SNB Thu block.

### Hourly re-validation — 2026-06-15 08:16 UTC
Fresh pull. Spot **0.79330**, ~72p BELOW SHORT 0.8005–0.8025 (price away); H4 oversold (Stoch 17, W%R −95) = wrong side for a short entry. E0 none. **NO TRADE**. Operator open long 0.79477 now ~−14.7p (~−0.6R); SL 0.79234 + BE intact.

---
### 2026-06-15 09:50 UTC hourly re-validate
Spot 0.79321. SHORT 0.8005–0.8025 ❌ NO TRADE (~72p below zone; H4 oversold = opposite extreme, no bearish E0). Open long 0.79477 carry ~−0.6R, SL/BE intact, operator decision pending. SNB Thu + FOMC Wed.

---
### 2026-06-15 10:14 UTC hourly re-validate
Fresh pull (10:13). Spot **0.79338**. SHORT 0.8005–0.8025 ~70p above (price away; 09:00 1H pin-bull = OS bounce, opposite dir) ❌ NO TRADE. ADX 23.3 transitional. FOMC Wed + SNB Thu. ⚠ Open operator LONG 0.79477 ~−0.6R (spot 0.79338), SL 0.79234/BE 0.79842 intact — thesis flipped bearish, decision pending.

---
### 2026-06-15 11:21 UTC hourly re-validate
Fresh pull. Spot **0.79310** — ~74p below SHORT 0.8005–0.8025 → ❌ NO TRADE (price away). H4 oversold (Stoch 17/W%R −95, opp — needs bounce into zone). DXY 20d slope down = bearish thesis intact. ADX 23.3. FOMC Wed + SNB Thu. Open long 0.79477 carryover unchanged (operator decision pending).

---
### 2026-06-15 12:30 UTC hourly re-validate
Fresh pull (12:28). Spot **0.79344**. COUNTER SHORT 0.8005–0.8025 ~70p above (price away); H4 oversold (Stoch 7.5 / W%R −89) = opposite extreme, no bearish E0 → ❌ NO TRADE. (12:00 1H LONG E0 fired — RSI/band/Stoch reclaim — but no long zone published.) DXY 20d slope down = bearish thesis intact. ADX 23.3. FOMC Wed + SNB Thu.
> **Correction:** the W24 operator LONG (0.79477) is **already CLOSED** — bar low pierced SL 0.79234 @ **10:30 UTC** (low 0.79225), logged LOSS −1.0R in `trades_log.csv` (exit 11:18:57Z). The earlier 11:21 "SL intact / decision pending" note was stale (read off spot, not the bar low — the CLAUDE.md-documented failure mode). No open USDCHF position remains.

---
### 2026-06-15 14:11 UTC hourly re-validate
Fresh pull (14:0x). Spot **0.79243**. PRIMARY SHORT 0.8005–0.8025 ~81p ABOVE spot — price has dropped off resistance and H4 is now OVERSOLD (Stoch 7.5 / W%R −89 / CCI −154), the opposite extreme; no at-zone short setup → ❌ NO TRADE. (W24 long already stopped out 11:18, no open position.) FOMC Wed, SNB Thu. PENDING.


---

## Hourly re-validation — 2026-06-15 15:14 UTC
Spot **0.79309**. LONG-confirm E0 (RSI-reclaim 35→38) + H4 OVERSOLD (Stoch 7.5 / W%R −89 / CCI −154) — but only W25 zone is SHORT 0.8005–0.8025 (~74p above); bullish E0 wrong direction, no long zone (W24 long stopped out 11:18). **❌ NO TRADE**.
