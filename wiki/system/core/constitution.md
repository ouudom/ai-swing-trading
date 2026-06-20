---
type: system
updated: 2026-06-11
confidence: high
tags: [rules, risk, core]
related: [xauusd_profile, confluence_criteria]
---

# Trading System Constitution (v2 — Trading Zones)

## Identity
- Instruments: **10 active — XAUUSD, EURUSD, GBPUSD, EURGBP, AUDUSD, NZDUSD, USDCAD, USDCHF, USDJPY, EURJPY, GBPJPY** (per-instrument config + profile + confluence; see table below). XAUUSD = momentum; FX = mean-reversion variants (D021/D024); USDJPY = asymmetric carry-drift.
- Style: Swing trading, discretionary, structured + AI-analysis driven
- Hold period: 2–10 days
- Timeframes: Weekly/Daily (bias) → Daily→H4→1H (top-down) → 1H/15M (entry confirmation)
- Output unit: **Trading Zone** (not "setup"). Max 3 zones/week per instrument, at most 1 counter-trend.

## Multi-Instrument Generalization (read first)
The rules below are written in their **XAUUSD instantiation** (gold $-units, real-yield macro,
momentum bias). They generalize via each instrument's profile — never hardcode gold values for FX:

| Generic rule term | XAUUSD | EURUSD / GBPUSD | EURGBP (cross) | AUDUSD / NZDUSD | USDCAD / USDCHF (USD-base) | USDJPY (USD-base, JPY-quoted) | EURJPY (cross, JPY-quoted) | GBPJPY (cross, JPY-quoted) | Source |
|---|---|---|---|---|---|---|---|---|---|
| Lot multiplier | ×100 | ×100000 | ×100000 (USD-sized, no GBP convert — operator) | ×100000 | ×100000 (CAD pip ~28% under / CHF pip ~25% over; accepted) | **×650 STATIC** (≈100000/154; ±10% spot drift accepted) | **×650 STATIC** (pip value tracks USDJPY, not EURJPY) | **×650 STATIC** (pip value tracks USDJPY, not GBPJPY) | `TICK_MULTIPLIER` |
| H4-ATR flatline filter | $1 | 0.0003 (3 pips) | 0.0002 (2 pips) | 0.0003 (3 pips) | 0.0003 (3 pips) | 0.03 (3 JPY pips; pip=0.01, 3dp) | 0.03 (pip=0.01, 3dp) | 0.05 (pip=0.01, 3dp — highest ATR) | `MIN_BAR_RANGE` |
| V1b "past zone" threshold | $5 | EUR 5 pips / GBP 6 pips | 4 pips | 4 pips | CAD 5 pips / CHF 4 pips | 0.04 (4 JPY pips) | 0.04 (4 JPY pips) | 0.05 (5 JPY pips) | profile |
| Macro baseline (frontmatter) | `baseline_dfii10` | `baseline_dgs2` (+ `baseline_policy_diff`) | `baseline_rate_diff` (weak) | `baseline_dgs2` (NZD: context only) | `baseline_dgs2` (**polarity FLIPPED**) | `baseline_dgs2` (**DEAD** — context only) | `baseline_ecb_rate` (context only) | `baseline_sonia_rate` (context only) | snapshot |
| Macro direction model | real-yield (momentum) | DXY-jump→short + US2Y-slope + VIX-spike→short; carry-diff/2s10s DEAD | **thin/DEAD — price-only; macro = 0.5 tilt** | **VIX LEVEL (inverted)** + US2Y-slope (AUD only — dead for NZD); DXY-jump DEAD both | CAD: **VIX LEVEL fade-USD (VIX>20→short)** + US2Y-flipped + 🛢 oil tilt; DXY DEAD. CHF: **DXY 20d SLOPE** (only live DXY pair beyond EUR/GBP); VIX WASHOUT | **DXY 20d SLOPE** (live, like CHF); VIX WASHOUT; US2Y DEAD (carry = baseline drift) | **NONE — first 100% price-driven pair** (ECB leg anti, VIX dead, no USD leg) | **NONE — second 100% price-driven pair** (SONIA leg ns, VIX dead, no USD leg) | profile / D021 / EG2 / D024 |
| VIX veto direction | block SHORTs (safe-haven) | block **LONGs** (risk-off USD bid) | **NONE** (risk-off → EURGBP UP, inverted) | **NONE** (VIX level scores, inverted) | **NONE** (CAD: level scores — high VIX favors SHORTs. CHF: washout — no gate, no score) | **NONE** (washout — no gate, no score) | **NONE** (dead, t=0.91) | **NONE** (dead, t=0.89) | profile / EG2 / D024 |
| Hard-block events | US tier-1 | US tier-1 (shared) | **ECB + BoE + UK/EZ data** (US = caution only) | US tier-1 + **RBA/AU CPI/jobs** (AUD) / **RBNZ/NZ CPI/jobs** (NZD); China = caution | US tier-1 + **BoC/CAD CPI/jobs** (shared 12:30 slot!); OPEC/EIA = caution (CAD) / **SNB quarterly decision + SNB communication days** (CHF) | US tier-1 + **BoJ decision + active MoF jawboning** (intervention slams 300–500 pips); JP CPI = caution | **BoJ + MoF jawboning (slams hit crosses) + ECB**; US tier-1 = caution only | **BoJ + MoF jawboning (GBPJPY slams = largest) + BoE**; US tier-1 = caution only | profile |
| Re-forecast T1/T5 series | DFII10 | US2Y (DGS2) | EUR−GBP rate diff (weak); leans on T3 price | US2Y (DGS2) (NZD: drift context; leans on T3 price) | US2Y (DGS2), FLIPPED read (CHF: + watch DXY slope flip) | DXY 20d slope flip (US2Y dead; leans on T3 price) | NONE — T3 counter-move 1.5% + T4 shock only | NONE — T3 counter-move 1.5% + T4 shock only | profile |
| Confluence philosophy | pro-trend / macro-gated | **fade extremes; never trend-follow** | **fade extremes; macro-light** | **fade extremes; AUD H4-centric / NZD squeeze-led macro-light** | **fade extremes; USD-base sign discipline; CAD H1 long-rich / CHF H1 short-rich + SNB regime cap** | **ASYMMETRIC: LONG drift-continuation (squeeze/calm/dip/NY) / SHORT D1-H4 extreme fade; NO H1-only shorts; MoF cap ≥158** | **symmetric fade on long-drift floor: buy washouts / fade extension / NEVER chase; record-high longs cap MEDIUM** | **extension-fade, SHORT-dominant: fade spikes / buy washouts / NO calm engine; shorts avoid 13–15 UTC; record-high longs cap MEDIUM** | per-pair confluence_criteria |

> **Antipodean advisory (D024):** AUDUSD + NZDUSD same direction ≈ one bet (corr ~0.85); AUD edge
> ≈ 2× NZD — fx_exposure flags it, default keep AUD unless NZD EC clearly higher.

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

lots = $2000 / (SL × TICK_MULTIPLIER), floored to the 0.01-lot step (broker min 0.01) —
       lots = max(0.01, floor(raw × 100) / 100). Never integer-floor to whole lots.
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
       V3  event WINDOW (±30min / within 2h of open) → NO TRADE
           forward-carry event (later same hold)      → ALLOW, expiry = event−60min (D028 flatten)
       VETO VIX > 35 → XAUUSD: all SHORTs NO TRADE | FX: all LONGs NO TRADE (risk-off USD bid)
  3. Entry Confluence score (max 10, floor 5.0) — see confluence_criteria.md R2
       E0 entry confirmation 3.0 | E1 H4 struct 2.5 | E2 DFII10 slope 2.0
       E3 macro drift 1.0 | E4 ATR compression 1.0 | E5 DXY slope 0.5
  → OUTPUT (exactly one):
     ✅ ORDER LIMIT — score ≥ 5.0
        with E0 confirmation → anchor = confirmation candle CLOSE
        without confirmation → anchor = 50% zone midpoint
     ❌ NO TRADE — score < 5.0 or hard block
  4. Order expires 21:00 UTC (or event−60min if a hard event falls in the hold horizon, D028) —
     re-validate next morning, never carry the ORDER forward; a filled position flattens pre-event.
```

### Entry confirmation (E0 — confirmed on 1H candle CLOSE)
Trigger menu, **toward zone direction**, all on the latest CLOSED 1H bar (pull block ENTRY TRIGGERS).
Per-pair PRIMARY trigger is set in each `confluence_criteria.md` E0 row (ranked by the e0-variants
backtest, `wiki/research/general/e0-variants-backtest.md`). Any one listed for the pair satisfies E0:
- **Oscillator RECLAIM (preferred for FX mean-reversion fades):**
  - RSI(14) crosses back **through 35** (long) / **65** (short) — highest-R gate in backtest, OR
  - close re-enters the Keltner band (band-reclaim: above Keltner-low long / below Keltner-high short), OR
  - Stoch %K crosses back through 20 (long) / 80 (short).
- **Candle (retained fallback — primary only on gbpusd):** 1H engulfing (body engulfs prior body) OR
  1H pin (rejection wick ≥ 2.5× body).
- **15M CHoCH** over a 60-candle window (tactical fast-entry leg, unchanged).
- **xauusd (momentum) + usdjpy LONG (carry-drift):** E0 = CONTINUATION toward the zone (engulf/pin
  toward drift), NOT a reclaim — the fade reclaim does not apply.

> [!note] PENDING LIVE VALIDATION (added 2026-06-14, D027). The reclaim ranking is from an in-sample
> forward-return sim on the unfiltered extreme universe (2015+), 1H. The shadow ledger
> (`zone_outcomes.csv`) must confirm the reclaim-primary E0 on the confluence-gated subset before
> this is treated as settled; pin/engulf is retained as fallback so E0 is never worse than before.

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
- No new entries inside the **event window** itself — release ±30min, OR any hard event within 2h
  of the 08:00 London / 13:00 NY open. This is the V3 "entry-in-window" block and is unchanged.
- Scheduled central-bank decisions (FOMC/ECB/BoE/BoJ/SNB/RBA/RBNZ/BoC) come from the static
  calendar `scripts/config/cb_calendar_{year}.json` via `scripts/check_cb_calendar.py` —
  MANDATORY at /weekly (10-day window) and /validate (2-day window). Web search supplements
  the calendar, never replaces it. Rebuild the JSON every December.

### Pre-Event Flatten — carry policy (D028, replaces the binary carry block)
The risk a CB decision / tier-1 release poses is the **gap** — price jumps *through* the SL, so a
planned −1R becomes −3 to −5R (MoF intervention slams run 300–500 pips). The fix is to never **hold**
through the event, NOT to refuse the entry. So a leg facing a hard event later in the carry horizon is
**no longer auto-NO-TRADE.** Instead:
- **Entries are allowed** (subject to all other gates: V1/V1b, EC ≥ 5.0, the ±30min/2h window block,
  VETO, and standing per-pair rules such as the JPY-trio NO ZONES).
- Any resulting order limit **expires at `flatten_time = event_time − FLATTEN_BUFFER`** instead of the
  default 21:00 UTC, so a late fill cannot carry in.
- Any position still open at `flatten_time` is **closed at market** (manual when awake; the limit
  expiry + BE/TP bound it otherwise). Flat before the event = no gap exposure.
- `FLATTEN_BUFFER = 60min` (operator-tunable). Clears the ±30min window with margin.
- **Still a true HARD BLOCK (no entry at all)** — the event-window block above (±30min / within-2h-of-
  open), the JPY-trio NO ZONES standing rule + active MoF intervention regime, and the day-of CB
  decision for that pair's own bank. Pre-event flatten only relaxes the *forward-carry* case (e.g. a
  Tue entry that would otherwise carry into Wed FOMC), not the event hour itself.
- If multiple events bound a position, `flatten_time` uses the **earliest** affecting event.

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
| T6 — USD regime drift (nominal + slope) | DGS2 cumulative drift abs(now − `baseline_dgs2`) > 0.15%, **OR** DXY `slope20` sign-flips vs the published-bias direction | DGS2 (FRED) + DXY `slope20` from the weekly pull vs `baseline_dxy`/published bias |

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
CONFIRMATION re-forecast if: single {T1..T4} today, OR T6 alone → log WARN + pending_reforecast_check;
   recheck next /validate → still firing = re-forecast, mean-reverted = clear.
   (T6 = CONFIRMATION not IMMEDIATE: nominal/slope repricing is noisier than real-yield; a 1-day
   DGS2 spike or a borderline slope flip must persist one /validate before it voids zones.)
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

## USD Regime Drift — FX (every /validate)
xauusd drifts on DFII10 (above); USD-leg FX drifts on **nominal DGS2 + DXY `slope20`** — the W25 gap
was a hawkish DGS2/slope repricing (DGS2 4.05→4.20, slope20 +1.65) that moved neither DFII10 nor the
DXY 1-day *jump*, so nothing fired and stale USD-short zones rode into the flip. Frontmatter stores
`baseline_dgs2` + `baseline_dxy`. Daily check (mirrors T6):

| signal | Action |
|---|---|
| \|Δ DGS2\| < 0.10% **and** `slope20` sign unchanged | Macro unchanged. |
| \|Δ DGS2\| 0.10–0.15% **or** `slope20` flattening toward flip | Note in daily file; E3-equivalent (macro tilt) fails if against direction → HOLD that zone. |
| \|Δ DGS2\| > 0.15% **or** `slope20` sign-flipped vs published bias | T6 fires → CONFIRMATION re-forecast (recheck next /validate; persists = void zones). |

**Counter zones are voided immediately on a confirmed against-bias USD-regime flip** — counters are
the most fragile to a regime shift (W25: every counter-USD long lost or was saved only by a hard
block). Do not wait for the CONFIRMATION recheck to drop a counter that the flip now opposes.

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
