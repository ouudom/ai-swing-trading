---
type: system
updated: 2026-06-02
confidence: high
tags: [rules, risk, core]
related: [xauusd_profile, confluence_criteria]
---

# Trading System Constitution (v2 — Trading Zones)

## Identity
- Instruments: **XAUUSD, EURUSD, GBPUSD** (per-instrument config + profile + confluence). XAUUSD = momentum; FX majors = mean-reversion (see D021).
- Style: Swing trading, discretionary, structured + AI-analysis driven
- Hold period: 2–10 days
- Timeframes: Weekly/Daily (bias) → Daily→H4→1H (top-down) → 1H/15M (entry confirmation)
- Output unit: **Trading Zone** (not "setup"). Max 3 zones/week per instrument, at most 1 counter-trend.

## Multi-Instrument Generalization (read first)
The rules below are written in their **XAUUSD instantiation** (gold $-units, real-yield macro,
momentum bias). They generalize via each instrument's profile — never hardcode gold values for FX:

| Generic rule term | XAUUSD | EURUSD / GBPUSD | EURGBP (cross) | AUDUSD | Source |
|---|---|---|---|---|---|
| Lot multiplier | ×100 | ×100000 | ×100000 (USD-sized, no GBP convert — operator) | ×100000 | `TICK_MULTIPLIER` |
| H4-ATR flatline filter | $1 | 0.0003 (3 pips) | 0.0002 (2 pips) | 0.0003 (3 pips) | `MIN_BAR_RANGE` |
| V1b "past zone" threshold | $5 | EUR 5 pips / GBP 6 pips | 4 pips | 4 pips | profile |
| Macro baseline (frontmatter) | `baseline_dfii10` | `baseline_dgs2` (+ `baseline_policy_diff`) | `baseline_rate_diff` (weak) | `baseline_dgs2` | snapshot |
| Macro direction model | real-yield (momentum) | DXY-jump→short + US2Y-slope + VIX-spike→short; carry-diff/2s10s DEAD | **thin/DEAD — price-only; macro = 0.5 tilt** | US2Y-slope + **VIX LEVEL (inverted)**; DXY-jump DEAD | profile / D021 / EG2 / D024 |
| VIX veto direction | block SHORTs (safe-haven) | block **LONGs** (risk-off USD bid) | **NONE** (risk-off → EURGBP UP, inverted) | **NONE** (VIX level scores, inverted) | profile / EG2 / D024 |
| Hard-block events | US tier-1 | US tier-1 (shared) | **ECB + BoE + UK/EZ data** (US = caution only) | US tier-1 + **RBA/AU CPI/jobs** (China = caution) | profile |
| Re-forecast T1/T5 series | DFII10 | US2Y (DGS2) | EUR−GBP rate diff (weak); leans on T3 price | US2Y (DGS2) | profile |
| Confluence philosophy | pro-trend / macro-gated | **fade extremes; never trend-follow** | **fade extremes; macro-light** | **fade extremes, H4-centric; never trend-follow** | per-pair confluence_criteria |

All formulas (SL, offset, TP, R) are unit-agnostic across instruments. EURGBP is nominally GBP-quoted
but — **operator decision** — is sized in USD with the same formula as the majors
(`lots = $2000/(SL × 100000)`, no GBP→USD conversion; assumes broker settles EURGBP pips in USD).
Every EURGBP order routes through the FX netting ledger (`scripts/fx_exposure.py`) — EURGBP IS the
cross risk-axis (see [[currency_exposure]]).

## Risk Rules — Non-Negotiable
- Risk per trade: $2000
- Max loss per month: $10000
- Drawdown circuit breaker: account drops 5% from peak → $1000/trade until recovered
- Never widen a stop after entry. Never move stop against the trade.
- All entries are **order limits** (buy limit long / sell limit short). No market orders.

## Portfolio Currency-Leg Netting — FX only, ADVISORY (D022 as amended by D024; see [[currency_exposure]])
Every FX pair = +base / −quote currency leg. Pairs sharing a leg in the same direction do NOT
diversify — they concentrate onto one factor (e.g. EURUSD short + GBPUSD short = 2× long USD;
USDJPY long + EURJPY long = 2× short JPY). The ledger `scripts/fx_exposure.py` decomposes all
live + candidate FX orders into per-currency legs and flags shared-leg concentration.

**D024 (operator): this system generates signals, it does not manage risk. No hard $ cap.**
The ledger is **advisory**: when ≥2 FX orders load the same leg-direction it emits a
`> [!warning] Concentration:` callout and **suggests keeping only the cleaner trade** (highest
Entry Confluence). The operator decides; nothing is auto-skipped or auto-cancelled.
Soft note: AUDUSD + NZDUSD same direction ≈ one bet (corr ~0.85) even though the legs differ.
**Scope:** FX only. Gold is NOT in the ledger (driver = real yields, not a clean USD leg) —
note its USD co-movement as context.

## Two scores — do not conflate (see [[confluence_criteria]])
- **Zone Confluence** (at `/weekly`, max 10, floor 5.0): rates a zone's inherent quality. Publishes PENDING zones.
- **Entry Confluence** (at `/validate`, max 10, floor 5.0): rates whether TODAY justifies the order.

## Stop Loss (v2)
```
H4_ATR14 = ATR(14) on trading-day H4 bars only (range >= MIN_BAR_RANGE; drop weekend/holiday flatline)
D1_ATR14 = ATR(14) on D1 bars

if (0.5 × D1_ATR14) < H4_ATR14 :  SL = H4_ATR14
else                           :  SL = avg(0.5 × D1_ATR14, H4_ATR14)

lots = $2000 / (SL × TICK_MULTIPLIER), round DOWN   (min 0.01)
       TICK_MULTIPLIER = 100 (XAUUSD) | 100000 (FX, non-JPY) | 650 (JPY-quoted, static ≈100000/154 — D024)
       MIN_BAR_RANGE   = $1 (XAUUSD)  | per-pair pips (profile)
```
**v2 change:** structural pivot removed from the stop formula. Stop is volatility-based:
H4 ATR is the floor; half-D1 ATR only lifts it when half-D1 exceeds H4. SL is the base unit for
sizing AND for the order-limit offset.

## Entry — Order Limit with Daily Validation Gate
Order placement is gated by `/validate` — never placed Sunday without validation. Offset and SL
are computed at `/validate` time from that day's ATR — never frozen from `/weekly`.

```
Daily workflow (07:30 UTC, before London open):
  1. /validate [date]
  2. Hard blocks (any fail = stop):
       V1  D1 close beyond zone           → INVALIDATED
       V1b 2 consecutive H4 closes > [V1b threshold] past zone → INVALIDATED (scripts/check_v1b.py)
           threshold = $5 (XAUUSD) | 5 pips EUR / 6 pips GBP (profile)
       V3  hard news event within 2h      → NO TRADE
       VETO VIX > 35 → XAUUSD: all SHORTs NO TRADE | FX: all LONGs NO TRADE (risk-off USD bid)
  3. Entry Confluence score (max 10, floor 5.0) — see confluence_criteria.md R2
       E0 entry confirmation 3.0 | E1 H4 struct 2.5 | E2 DFII10 slope 2.0
       E3 macro drift 1.0 | E4 ATR compression 1.0 | E5 DXY slope 0.5
  → OUTPUT (exactly one):
     ✅ ORDER LIMIT — score ≥ 5.0
        with E0 confirmation → anchor = confirmation candle CLOSE
        without confirmation → anchor = 50% zone midpoint
     ❌ NO TRADE — score < 5.0 or hard block
  4. Order expires 21:00 UTC — re-validate next morning, never carry forward.
```

### Entry confirmation (E0 — confirmed on candle CLOSE)
- 1H engulfing candle (body engulfs prior body, toward zone direction), OR
- 1H pin bar (rejection wick ≥ 2.5× body, toward zone direction), OR
- 15M CHoCH over a 60-candle structure window, **toward zone direction**.

### Order-limit outward offset (v2)
```
offset = max( SL/3 , (10 − entry_confluence_score) × 0.2 × SL )

anchor = confirmation close (E0 present) | 50% zone midpoint (no E0)
Long:  limit_price = anchor − offset       ← outward, below anchor
Short: limit_price = anchor + offset       ← outward, above anchor
SL price: long limit − SL | short limit + SL
```
Offset pushes the limit AWAY from spot (commitment filter). SL/3 floor guarantees a minimum
buffer even at a perfect score; coefficient 0.2 scales the rest by how much the score falls short.

## Take Profit (v2)
```
TP1 = 2.5R  → MANUAL close (awake → take it, win the trade)
TP2 = 3.0R  → LIMIT close (asleep → set-and-forget)
BE  = move stop to entry when +1.5R is reached
```
Rationale: TP1/TP2 split = "if I'm asleep the 3R limit + BE protect me; if I'm awake at 2.5R I
take the win." TP must land at a structural anchor (prior swing / weekly pivot / Fib extension) —
name it, compute R. After entry the stop is fixed except the one-time BE move at +1.5R.

## No-Trade Rules
- No new entries 2h before any red-folder Forex Factory event.
- NFP, FOMC, CPI, US Retail Sales are hard blocks — cancel any live limit orders.

## Invalidation
- **V1** — any D1 close beyond zone extreme → cancel.
- **V1b** — 2 consecutive H4 closes past zone extreme by > [V1b threshold] → cancel live limit,
  remove from `_HOT.md`. Threshold = $5 (XAUUSD) | 5 pips EUR / 6 pips GBP. Check at each H4
  boundary (00/04/08/12/16/20 UTC).
- Macro bias reverses (XAUUSD: real yields spike against direction; FX: DXY 1d jump or US2Y
  slope flips against direction) or weekly structure breaks.

> **Liquidity Sweep Exception:** a wick that penetrates the zone but CLOSES back inside (same or
> next candle) is NOT invalidation — it's a Wyckoff Spring / stop hunt. Require a D1 *close*
> beyond zone OR two consecutive H4 closes (V1b) before cancelling.

## Weekend Gap Gate (Monday /validate only)
Computed at `/weekly` (Fri 20:00 UTC close vs Sunday reopen).

| \|gap_pct\| | Action |
|---|---|
| < 0.20% | Noise. Log only. |
| 0.20–0.50% | Note in Monday /validate. No bias change. |
| 0.50–1.00% | Warning — re-examine bias before /validate; zones may need redraw. |
| > 1.00% | Hard re-forecast — re-run /weekly Monday. Sunday forecast voided. |

A weekend-gap re-forecast does NOT consume `weekly_reforecast_count` (separate path).

## Mid-Week Re-Forecast Triggers
Sunday `/weekly` bias is assumed valid through Friday close. Mid-week re-forecast is **destructive**
(cancels live limits, voids PENDING zones) — must be rare, rule-based, confirmed.

### Triggers (D1-close based)
| Trigger | Threshold | Source |
|---|---|---|
| T1 — DFII10 1-day jump | abs(today − yesterday) > 0.10% | `data/fred/DFII10.csv` |
| T2 — DXY 1-day jump | abs(today − yesterday) > 0.75 ICE points | `data/yahoo/DXY.csv` |
| T3 — Gold counter-move | D1 close moves >2.5% AGAINST weekly bias | `data/twelvedata/xauusd/1day.csv` |
| T4 — Unscheduled macro shock (X OR Y) | X: structured news event today / Y: VIX 1-day jump > 5.0 | X: web + `data/news_events/[DATE]_t4x.json` / Y: `data/fred/VIXCLS.csv` |
| T5 — DFII10 cumulative drift | abs(now − baseline) > 0.15% any direction | DFII10 vs `baseline_dfii10` in weekly frontmatter |

**T4-X** = tier-1 unscheduled event published today by Reuters/Bloomberg/AP, allowed categories
ONLY: central-bank emergency, declared war / major G20 sanctions, Fed chair removal, sovereign
default, major political shock. Requires valid `data/news_events/[DATE]_t4x.json` (schema enforced
by `scripts/check_structured_news_event.py`) + mirror to `_HOT.md`. No valid JSON → T4-X does not fire.

### Hard preconditions (re-forecast allowed iff ALL true)
1. No open positions (re-forecast acts only on PENDING zones + unfilled limits).
2. Day-of-week: NOT Monday, NOT Friday.
3. Event-proximity (forward-only 12h): >12h until next NFP/FOMC/CPI/Retail/GDP. Past events don't block.
4. Spacing: >48h since last `/weekly`.
5. Weekly cap: 0 prior mid-week re-forecasts this week.

### Trigger logic (when preconditions pass)
```
IMMEDIATE re-forecast if: two concurrent {T1,T2,T3,T4} same day, OR T5 alone.
CONFIRMATION re-forecast if: single {T1..T4} today → log WARN + pending_reforecast_check;
   recheck next /validate → still firing = re-forecast, mean-reverted = clear.
Preconditions fail → log fires as INFO only, no action.
```

### Protocol when re-forecast executes
1. Cancel ALL live limit orders. 2. Remove all PENDING/WATCH zones from `_HOT.md`.
3. Run `/weekly` with current data. 4. Annotate `_HOT.md`: `MID-WEEK RE-FORECAST [DATE],
trigger=[Tx], original [YYYY-WNN] voided`. 5. Increment `weekly_reforecast_count` (max 1).
6. New zones land PENDING — halt today's `/validate`, resume next morning. 7. Week-scoped: voided
at CME Globex Fri 22:00 UTC; new week always needs fresh Sunday `/weekly`; count resets to 0.

### Edge preservation
- Max ONE mid-week re-forecast/week. Second qualifying trigger → STOP trading until Monday.
- Re-forecast cannot revive an INVALIDATED zone. Open positions never auto-touched.
- No discretionary reset path. Lag is acceptable: a confirmed shift recognized 24h late beats a false reset.

## Real-Yield Baseline Drift (every /validate)
Forecast frontmatter stores `baseline_dfii10`. Daily DFII10 vs baseline:

| \|Δ DFII10\| | Action |
|---|---|
| < 0.05% | Macro unchanged. |
| 0.05–0.10% | Note in daily file. Pass if direction supports bias. |
| > 0.10% | E3 fails if drift is against direction. HOLD. |
| > 0.15% any direction | Force re-forecast (regime shift). |

## Zone Types
| Zone | Direction | Floor | Extra rules |
|---|---|---|---|
| Primary | With weekly bias | 5.0 | Best Zone Confluence |
| Secondary | With weekly bias | 5.0 | Distinct price path / level |
| Counter | Against weekly bias | 5.0 (from 6.0 max) | RSI divergence MANDATORY; macro must be LOW/MEDIUM conf; macro signals score 0 |

Max 3 zones/week, at most 1 counter. No valid zone for a slot → NONE (never force).
Trades execute whenever a zone independently passes `/validate`. No weekly count cap.

## The Three Laws
1. Risk management > TA method.
2. No confluence = no trade. Waiting is a position.
3. If you can't write the IF/THEN in one sentence, the zone isn't ready.
