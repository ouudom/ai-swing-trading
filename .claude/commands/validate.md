Run daily validation on PENDING Trading Zones, 07:30 UTC before London open.

Arguments: `[instrument] [date]`. Instrument ∈ {xauusd, eurusd, gbpusd} (default xauusd).
Date YYYY-MM-DD (default today). Validate one instrument per invocation.

**The four questions /validate answers, per zone:**
1. **Is the forecast still valid?** (V1/V1b structure intact, V3 news clear)
2. **Has bias flipped?** (macro drift / counter-move vs baseline)
3. **Should we re-forecast?** (mid-week trigger tree — constitution "Mid-Week Re-Forecast Triggers")
4. **Can we set an order limit?** (Entry Confluence ≥ 5.0 → ORDER LIMIT, else NO TRADE)

Output per zone is exactly one of: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.

## Step 0 — Instrument parametrization (set ALL of these first)
| Param | xauusd | eurusd | gbpusd |
|---|---|---|---|
| `TICK_MULTIPLIER` | 100 | 100000 | 100000 |
| `MIN_BAR_RANGE` (H4 filter) | 1.0 | 0.0003 | 0.0003 |
| `PRICE_DP` | 2 | 5 | 5 |
| `V1B_BUFFER` | 5.0 | 0.0005 | 0.0006 |
| Character | momentum | mean-reversion | mean-reversion |
| Confluence R2 | xauusd | eurusd | gbpusd |
| Macro baseline field | `baseline_dfii10` | `baseline_dgs2` | `baseline_dgs2` |
| VIX veto blocks | SHORTs | LONGs | LONGs |

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
else:
    s = pd.read_csv("data/fred/DGS2.csv").dropna()      # US 2Y = rate-momentum leg
macro_now  = round(float(s.value.iloc[-1]), 3)
macro_prev = round(float(s.value.iloc[-2]), 3)
macro_slope = round(float(s.value.iloc[-1]) - float(s.value.iloc[-20]), 3)
dxy = pd.read_csv("data/yahoo/DXY.csv").dropna(); dxy_jump = round(float(dxy.value.iloc[-1]) - float(dxy.value.iloc[-2]), 3)
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
**Query A (V3 hard block):** economic calendar [DATE]. xauusd/FX share US events (NFP/FOMC/CPI/
Retail). FX also: ECB rate decision (eurusd), BoE rate decision (gbpusd) — instrument's own central
bank. Hard-block events within 2h of 08:00 or 13:00 UTC.
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
  - FRED VIXCLS freshness guard: latest date < today−1 → suspend veto, log `vix_stale=true`.
- **Macro flip** — macro series vs baseline (constitution drift table): >0.15% any dir → force re-forecast.
  Also FX: DXY 1d jump > 0.5 AGAINST a zone → that zone NO TRADE (strongest measured signal).

### Q4 — Entry Confluence (max 10, floor 5.0)
**Use `wiki/system/{INSTRUMENT}/confluence_criteria.md` R2 — the table differs by instrument.**

- **xauusd (momentum):** E0 entry confirm 3.0 | E1 H4 structure 2.5 | E2 DFII10 slope 2.0 |
  E3 macro drift 1.0 | E4 ATR compression 1.0 | E5 DXY slope 0.5.
- **eurusd / gbpusd (mean-reversion):** E0 reversal confirm 3.0 | E1 oscillator still extreme 2.5 |
  E2 band touch / H1 oscillator 1.5 | E3 still non-trending ADX<25 1.0 | E4 structure/band intact 1.0 |
  E5 compression holds 1.0. (Exact rows per the pair's R2.)

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
