Run daily validation on PENDING Trading Zones, 07:30 UTC before London open.

Arguments: `[instrument] [date]`. Instrument ∈ {xauusd, eurusd, gbpusd, eurgbp, audusd, nzdusd} (default xauusd).
Date YYYY-MM-DD (default today). Validate one instrument per invocation.
(eurgbp = CROSS: NO VIX-veto, European event blocks, macro-light. audusd: NO VIX-veto + NO DXY
block — dead/inverted for AUD. nzdusd: macro-light — NO VIX-veto, NO DXY block, NO US2Y gate;
weakest edges, fewer orders expected; antipodean advisory vs audusd.)

**The four questions /validate answers, per zone:**
1. **Is the forecast still valid?** (V1/V1b structure intact, V3 news clear)
2. **Has bias flipped?** (macro drift / counter-move vs baseline)
3. **Should we re-forecast?** (mid-week trigger tree — constitution "Mid-Week Re-Forecast Triggers")
4. **Can we set an order limit?** (Entry Confluence ≥ 5.0 → ORDER LIMIT, else NO TRADE)

Output per zone is exactly one of: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.

## Step 0 — Instrument parametrization (set ALL of these first)
| Param | xauusd | eurusd | gbpusd | eurgbp (cross) | audusd | nzdusd |
|---|---|---|---|---|---|---|
| `TICK_MULTIPLIER` | 100 | 100000 | 100000 | 100000 (USD sizing, no GBP convert — operator) | 100000 | 100000 |
| `MIN_BAR_RANGE` (H4 filter) | 1.0 | 0.0003 | 0.0003 | 0.0002 | 0.0003 | 0.0003 |
| `PRICE_DP` | 2 | 5 | 5 | 5 | 5 | 5 |
| `V1B_BUFFER` | 5.0 | 0.0005 | 0.0006 | 0.0004 | 0.0004 | 0.0004 |
| Character | momentum | mean-reversion | mean-reversion | mean-reversion, macro-light | mean-reversion, H4-centric | mean-reversion, macro-light (weakest edges) |
| Confluence R2 | xauusd | eurusd | gbpusd | eurgbp | audusd | nzdusd |
| Macro baseline field | `baseline_dfii10` | `baseline_dgs2` | `baseline_dgs2` | `baseline_rate_diff` (weak) | `baseline_dgs2` | `baseline_dgs2` (context only) |
| VIX veto blocks | SHORTs | LONGs | LONGs | **NONE** (risk-off→EURGBP up) | **NONE** (VIX level scores, inverted) | **NONE** (weak inverted tilt) |
| DXY-jump block | — | AGAINST zone | AGAINST zone | NONE (no USD leg) | **NONE** (dead, t=−0.85) | **NONE** (dead, t=0.24) |

Read the instrument's `wiki/system/{instrument}/confluence_criteria.md` (R2) and
`wiki/system/{instrument}/{instrument}_profile.md` before scoring. FX uses a DIFFERENT R2 than
gold (mean-reversion oscillators, not H4-structure + real-yield).

## Step 1 — Load State
Read `_HOT.md` — all PENDING zones for THIS instrument (box, direction, zone confluence score,
baseline values, macro confidence, linked weekly file). Read linked weekly frontmatter. No PENDING
zones for the instrument → log and stop.

## Step 2 — Fetch Market Data
```bash
bash scripts/pyrun.sh scripts/weekly_pull.py --instrument <INSTRUMENT>   # orchestrator
# or: scripts/fetch.py (network only) | scripts/compute.py (recompute, no net) — both take --instrument
```
Fail → stop (never validate on stale data). Cache: refetch unless pull <15min old OR market closed.
Then read the pull file + CSVs and compute live values (set `INSTRUMENT`, `MIN_BAR_RANGE`,
`TICK_MULTIPLIER`, `PRICE_DP` from Step 0):

```python
import pandas as pd
INSTRUMENT = "xauusd"          # ← set per Step 0
MIN_BAR_RANGE = 1.0            # ← gold 1.0 | FX 0.0003
TICK_MULTIPLIER = 100          # ← gold 100 | FX 100000
DP = 2                         # ← gold 2  | FX 5
h4 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/4h.csv", parse_dates=["datetime"]).sort_values("datetime")
d1 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/1day.csv", parse_dates=["datetime"]).sort_values("datetime")
h1 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/1h.csv", parse_dates=["datetime"]).sort_values("datetime")
m15= pd.read_csv(f"data/twelvedata/{INSTRUMENT}/15min.csv", parse_dates=["datetime"]).sort_values("datetime")

# Macro — branch on instrument
if INSTRUMENT == "xauusd":
    s = pd.read_csv("data/fred/DFII10.csv").dropna()   # real yield = primary driver
    macro_now = round(float(s.value.iloc[-1]),3); macro_prev = round(float(s.value.iloc[-2]),3)
    macro_slope = round(float(s.value.iloc[-1]) - float(s.value.iloc[-20]),3)
elif INSTRUMENT == "eurgbp":
    # CROSS macro = EUR−GBP rate diff (ECBDFR−SONIA). EG2: thin/DEAD → LOW-weight TILT, not a gate.
    eu = pd.read_csv("data/fred/ECBDFR.csv").dropna(); gb = pd.read_csv("data/fred/IUDSOIA.csv").dropna()
    macro_now  = round(float(eu.value.iloc[-1]) - float(gb.value.iloc[-1]), 3)          # EUR−GBP diff now
    macro_prev = round(float(eu.value.iloc[-2]) - float(gb.value.iloc[-2]), 3)
    macro_slope= round(macro_now - (float(eu.value.iloc[-20]) - float(gb.value.iloc[-20])), 3)  # 20d diff change
else:  # USD pairs (eurusd / gbpusd / audusd): US 2Y = rate-momentum leg
    s = pd.read_csv("data/fred/DGS2.csv").dropna()
    macro_now = round(float(s.value.iloc[-1]),3); macro_prev = round(float(s.value.iloc[-2]),3)
    macro_slope = round(float(s.value.iloc[-1]) - float(s.value.iloc[-20]),3)
# DXY jump: scored/blocked for eurusd+gbpusd ONLY. eurgbp = no USD leg; audusd = measured DEAD
# (t=−0.85) → compute for context, never block.
if INSTRUMENT != "eurgbp":
    dxy = pd.read_csv("data/yahoo/DXY.csv").dropna(); dxy_jump = round(float(dxy.value.iloc[-1]) - float(dxy.value.iloc[-2]), 3)
else:
    dxy_jump = None
vix = pd.read_csv("data/fred/VIXCLS.csv").dropna(); vix_now = float(vix.value.iloc[-1]); vix_spike = vix_now - float(vix.value.iloc[-2])

def atr(df, p=14):
    tr = pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(p).mean()
def drop_open_bar(df, hrs):
    now = pd.Timestamp.utcnow().tz_localize(None); last = pd.Timestamp(df["datetime"].iloc[-1])
    return df.iloc[:-1] if now < last + pd.Timedelta(hours=hrs) else df

h4_trading = h4[(h4.high - h4.low) >= MIN_BAR_RANGE].copy().reset_index(drop=True)   # trading-day filter
h4_closed  = drop_open_bar(h4_trading, 4); d1_closed = drop_open_bar(d1, 24)
h4_atr = round(atr(h4_closed).iloc[-1], DP)
d1_atr_ser = atr(d1_closed); d1_atr = round(d1_atr_ser.iloc[-1], DP)
d1_median  = round(d1_atr_ser.iloc[-20:].median(), DP); compressed = d1_atr < d1_median
spot = round(h4.close.iloc[-1], DP)
print(spot, h4_atr, d1_atr, d1_median, compressed, macro_now, macro_slope, dxy_jump, vix_now, vix_spike)
```

## Step 3 — News + Mid-Week Re-Forecast Check
**Query A (V3 hard block):** economic calendar [DATE]. xauusd + USD pairs share US events (NFP/FOMC/
CPI/Retail). Pairs also: ECB rate decision (eurusd), BoE rate decision (gbpusd), RBA decision +
AU CPI/employment (audusd), RBNZ OCR + NZ CPI/jobs (nzdusd; GDT dairy = caution) — own central
bank. China tier-1 = caution→hard for audusd/nzdusd if commodity move in progress.
**eurgbp (cross): hard blocks = ECB + BoE rate decisions + UK/EZ tier-1 (CPI/GDP/jobs/PMI). US
events = CAUTION ONLY, not a hard block (no USD leg).** Hard-block events within 2h of 08:00 or 13:00 UTC.
**Query B (T4-X):** breaking news [DATE] — central-bank emergency / war / sanctions / sovereign
default / political shock. Qualifying → write `data/news_events/[DATE]_t4x.json` + mirror `_HOT.md`.

Run the **Mid-Week Re-Forecast** precondition gate + trigger tree per constitution, using the
instrument's profile thresholds: T1 = US2Y/DFII10 1d jump, T2 = DXY 1d jump, T3 = pair/gold
counter-move (gold 2.5% / FX 1.5%), T4 = shock, T5 = cumulative macro drift vs baseline.
**Weekend gap gate (Monday only):** apply constitution table using `weekend_gap_pct`.

## Per-Zone Validation

### Q1+Q2 — Hard Blocks (any fail = stop)
- **V1** — D1 close beyond zone? → ❌ INVALIDATED (remove from `_HOT.md`). Wick close-back-inside = sweep, not invalidation.
- **V1b** — 2 consecutive H4 closes past zone extreme by > `V1B_BUFFER`?
  `scripts/check_v1b.py --instrument <INSTRUMENT> --direction <DIR> --zone-top <T> --zone-bottom <B> --buffer <V1B_BUFFER>` → ❌ INVALIDATED, cancel limit.
- **V3** — hard event within 2h of London/NY open? → ❌ NO TRADE, cancel live limit.
- **VETO (VIX>35 fresh, OR VIX 1d spike>3 for FX):**
  - xauusd → all SHORT zones NO TRADE (safe-haven bid)
  - eurusd/gbpusd → all LONG zones NO TRADE (risk-off USD bid drives pair down)
  - **eurgbp (cross) → NO VIX VETO** (risk-off bids EUR over GBP → EURGBP UP, inverted; EG2). VIX spike
    is instead a weak LONG *tilt* (Z4, 0.5). Only hard veto for eurgbp = D1 ADX>30 trending against the fade.
  - **audusd → NO VIX VETO** — polarity INVERTED as a *level* regime (VIX>20 → LONG tilt t=6.14,
    VIX<15 → SHORT tilt t=5.29; spike dead). VIX level scores in R2 E4 instead. Only hard veto for
    audusd = D1 ADX>30 trending against the fade.
  - **nzdusd → NO VIX VETO** — same inverted level polarity as AUD, weaker (t≈2.2–2.4); spike dead
    (t=−1.7). Only hard veto for nzdusd = D1 ADX>30 trending against the fade.
  - FRED VIXCLS freshness guard: latest date < today−1 → suspend veto, log `vix_stale=true`.
- **Macro flip** — macro series vs baseline (constitution drift table): >0.15% any dir → force re-forecast.
  eurusd/gbpusd: DXY 1d jump > 0.5 AGAINST a zone → that zone NO TRADE (strongest measured signal).
  **eurgbp: NO DXY block** (USD index irrelevant); rate-diff drift is weak/informational, not a flip gate.
  **audusd: NO DXY block** (DXY-jump measured DEAD for AUD, t=−0.85 — context only).
  **nzdusd: NO DXY block, NO US2Y gate** (both dead for NZD — t=0.24 / −0.7; DGS2 baseline = drift
  tracking context only).

### Q4 — Entry Confluence (max 10, floor 5.0)
**Use `wiki/system/{INSTRUMENT}/confluence_criteria.md` R2 — the table differs by instrument.**

- **xauusd (momentum):** E0 entry confirm 3.0 | E1 H4 structure 2.5 | E2 DFII10 slope 2.0 |
  E3 macro drift 1.0 | E4 ATR compression 1.0 | E5 DXY slope 0.5.
- **eurusd / gbpusd (mean-reversion):** E0 reversal confirm 3.0 | E1 oscillator still extreme 2.5 |
  E2 band touch / H1 oscillator 1.5 | E3 still non-trending ADX<25 1.0 | E4 structure/band intact 1.0 |
  E5 compression holds 1.0. (Exact rows per the pair's R2.)
- **eurgbp (cross, mean-reversion, macro-light):** E0 reversal confirm 3.0 | E1 D1 oscillator still
  extreme 2.5 | E2 H1 oscillator extreme 1.5 (validated — H1 t up to 7.45) | E3 non-trending ADX<25
  1.0 | E4 structure/band intact 1.0 | E5 compression holds 1.0. Macro NOT scored at entry. Short
  trigger leans on intraday extremes (D1 short thinner). (See eurgbp `confluence_criteria.md` R2.)
- **audusd (mean-reversion, H4-centric):** E0 reversal confirm 3.0 | E1 H4 oscillator still extreme
  2.5 | E2 H1 oscillator (short, t 5.2–6.5) / H4 band touch (long) 1.5 | E3 non-trending ADX<25 1.0 |
  E4 macro regime aligned (VIX level inverted + US2Y slope) 1.0 | E5 structure intact 1.0.
  D1 oscillators NOT scored (thin, t=−0.71). (See audusd `confluence_criteria.md` R2.)
- **nzdusd (mean-reversion, macro-light):** E0 reversal confirm 3.0 | E1 H4 oscillator still extreme
  2.5 | E2 H1 oscillator (short) / H4 band touch (long) 1.5 | E3 non-trending ADX<25 1.0 |
  E4 squeeze/compression holds 1.0 (NZD's strongest signal) | E5 structure intact 1.0. No macro at
  entry. **Antipodean advisory:** live same-dir audusd order → default keep AUD (≈2× edge) unless
  NZD EC clearly higher. (See nzdusd `confluence_criteria.md` R2.)

**E0 entry confirmation (confirm on candle CLOSE):**
- xauusd: 1H engulfing / 1H pin (wick ≥2.5×body) / 15M CHoCH — TOWARD zone direction (continuation).
- FX: same triggers but the reversal must turn AGAINST the approach INTO the zone (mean-reversion
  turn): long zone = bullish turn at support, short zone = bearish turn at resistance.

### Output
```
entry_confluence ≥ 5.0 AND E0 present → ✅ ORDER LIMIT, anchor = confirmation candle CLOSE
entry_confluence ≥ 5.0 AND no E0     → ✅ ORDER LIMIT, anchor = 50% zone midpoint
entry_confluence < 5.0               → ❌ NO TRADE
```

### Order Limit Calculation (score ≥ 5.0)
```python
d1_floor = 0.5 * d1_atr
SL = h4_atr if d1_floor < h4_atr else round((d1_floor + h4_atr) / 2, DP)
lots = int((2000) // (SL * TICK_MULTIPLIER))   # round down — gold ×100, FX ×100000
# NOTE (operator decision): eurgbp uses the SAME USD formula as the majors — NO GBP→USD pip
# conversion. Risk targeted in USD; broker assumed to settle EURGBP pip value in USD. (EURGBP is
# nominally GBP-quoted; if your broker settles pips in GBP this under-converts — revisit if so.)
anchor = confirmation_close if E0_present else round((zone_top + zone_bottom) / 2, DP)
offset = max(SL/3, (10 - entry_confluence_score) * 0.2 * SL)
limit_price = anchor - offset if direction == "LONG" else anchor + offset
sl_price    = limit_price - SL if direction == "LONG" else limit_price + SL
# TP locked from weekly structural anchor: TP1 2.5R (manual), TP2 3.0R (limit), BE at 1.5R
```
Expires: [DATE] 21:00 UTC.

## Output Format
**✅ ORDER LIMIT:**
```
[INSTRUMENT] ORDER LIMIT: BUY/SELL [limit_price] | [lots] lots | SL [sl_price] | TP1 2.5R [p] (manual) | TP2 3.0R [p] (limit) | BE @1.5R | expires 21:00 UTC
Entry Confluence: [score]/10 (E0:[✅/❌] E1:[✅/❌] E2:[✅/❌] E3:[✅/❌] E4:[✅/❌] E5:[✅/❌])
Anchor: [confirmation close / 50% zone] | SL [SL] | offset [offset] | R:R [computed]
"If price reaches [limit_price], order triggers. Cancel if not hit by 21:00 UTC."
```
**❌ NO TRADE:**
```
NO TRADE — [hard block / score < 5.0]: [specific reason]
[If INVALIDATED: remove zone from _HOT.md]
```

## Save + Update
Save `forecasts/daily/<INSTRUMENT>/[DATE].md` using `wiki/system/templates/daily_validation.md`
(Claude writes markdown directly — no DB). Then update `_HOT.md`: per-zone verdict; remove
INVALIDATED; record limit/SL/TP/expiry on ORDER LIMIT; move filled to Open Position; update Risk Used.

## Multi-Zone Handling
Validate every PENDING zone for the instrument independently. Multiple ORDER LIMITs allowed if zones
distinct (each risks $2000; no weekly cap). Same-day fill priority: Primary → Secondary → Counter.
To validate all instruments, invoke `/validate` once per instrument.

## FX Currency-Leg Netting — ADVISORY (D022 as amended by D024 — see [[currency_exposure]])
**Before writing ANY FX ORDER LIMIT**, run the ledger against today's other live FX orders —
pairs sharing a currency leg in the same direction concentrate onto one factor (e.g. two USD-pair
shorts = 2× long USD; usdjpy long + eurjpy long = 2× short JPY). Run:
```bash
bash scripts/pyrun.sh scripts/fx_exposure.py --live "<other live FX orders>" \
     --candidate "<this inst:dir:risk>" --new-ec <EC> --live-ecs "<inst:ec,...>"
```
- `INDEPENDENT` → no shared leg-direction, place normally.
- `CONCENTRATED` → **ADVISORY only (D024): no auto-skip, no auto-cancel.** Place the order if it
  passed Entry Confluence, but emit a `> [!warning] Concentration:` callout in the daily file
  naming the shared leg + the ledger's **suggested cleaner trade** (highest EC), and mirror to
  `_HOT.md`. The operator chooses whether to drop the weaker one.
Crosses (eurgbp/eurjpy/gbpjpy) can stack on an implied cross from held majors — always run the
ledger for them. Antipodean note: audusd + nzdusd same direction ≈ one bet (corr ~0.85).
