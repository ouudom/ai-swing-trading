Run daily validation on PENDING Trading Zones (XAUUSD), 07:30 UTC before London open.

Argument: date (YYYY-MM-DD). If omitted, use today.

**The four questions /validate answers, per zone:**
1. **Is the forecast still valid?** (V1/V1b structure intact, V3 news clear)
2. **Has bias flipped?** (macro drift / counter-move — real-yield + DXY vs baseline)
3. **Should we re-forecast?** (mid-week trigger tree — constitution "Mid-Week Re-Forecast Triggers")
4. **Can we set an order limit?** (Entry Confluence ≥ 5.0 → ORDER LIMIT, else NO TRADE)

Output per zone is exactly one of: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.

## Step 1 — Load State
Read `_HOT.md` — all PENDING zones (box, direction, zone confluence score, baseline values, macro
confidence, linked weekly file). Read linked weekly frontmatter. No PENDING zones → log and stop.

## Step 2 — Fetch Market Data
```bash
bash scripts/pyrun.sh scripts/weekly_pull.py --instrument xauusd   # orchestrator (canonical for /validate)
# or: bash scripts/pyrun.sh scripts/fetch.py (network only) | bash scripts/pyrun.sh scripts/compute.py (recompute, no TD/FRED net)
```
Fail → stop (never validate on stale data). Cache: refetch unless pull <15min old OR market closed.
Then read the pull file + CSVs and compute live values:

```python
import pandas as pd
INSTRUMENT = "xauusd"
h4 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/4h.csv", parse_dates=["datetime"]).sort_values("datetime")
d1 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/1day.csv", parse_dates=["datetime"]).sort_values("datetime")
h1 = pd.read_csv(f"data/twelvedata/{INSTRUMENT}/1h.csv", parse_dates=["datetime"]).sort_values("datetime")
m15= pd.read_csv(f"data/twelvedata/{INSTRUMENT}/15min.csv", parse_dates=["datetime"]).sort_values("datetime")
dfii = pd.read_csv("data/fred/DFII10.csv").dropna()
macro_now  = round(float(dfii.value.iloc[-1]), 3)
macro_prev = round(float(dfii.value.iloc[-2]), 3)
macro_slope = round(float(dfii.value.iloc[-1]) - float(dfii.value.iloc[-20]), 3)

def atr(df, p=14):
    tr = pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(p).mean()
def drop_open_bar(df, hrs):
    now = pd.Timestamp.utcnow().tz_localize(None); last = pd.Timestamp(df["datetime"].iloc[-1])
    return df.iloc[:-1] if now < last + pd.Timedelta(hours=hrs) else df

h4_trading = h4[(h4.high - h4.low) >= 1.0].copy().reset_index(drop=True)   # trading-day filter
h4_closed  = drop_open_bar(h4_trading, 4); d1_closed = drop_open_bar(d1, 24)
h4_atr = round(atr(h4_closed).iloc[-1], 2)
d1_atr_ser = atr(d1_closed); d1_atr = round(d1_atr_ser.iloc[-1], 2)
d1_median  = round(d1_atr_ser.iloc[-20:].median(), 2); compressed = d1_atr < d1_median
spot = round(h4.close.iloc[-1], 2)
print(spot, h4_atr, d1_atr, d1_median, compressed, macro_now, macro_slope)
```

## Step 3 — News + Mid-Week Re-Forecast Check
**Query A (V3 hard block):** economic calendar [DATE] — NFP/FOMC/CPI/US Retail Sales. Hard-block
events within 2h of 08:00 or 13:00 UTC.
**Query B (T4-X):** breaking news [DATE] — central-bank emergency / war / sanctions / Fed-chair
removal / sovereign default / political shock (Reuters/Bloomberg/AP). If qualifying → write
`data/news_events/[DATE]_t4x.json` (schema enforced by `scripts/check_structured_news_event.py`)
and mirror to `_HOT.md`.

Then run the **Mid-Week Re-Forecast** precondition gate + trigger tree per
`wiki/system/core/constitution.md` (T1 DFII10 jump, T2 DXY jump, T3 gold counter-move, T4 shock,
T5 cumulative drift). REFORECAST_NOW → cancel limits, void PENDING zones, run `/weekly`, increment
`weekly_reforecast_count`, halt today. WARN_LOG → log pending check, continue. NONE → continue.
**Weekend gap gate (Monday only):** apply constitution table using `weekend_gap_pct`.

## Per-Zone Validation

### Q1+Q2 — Hard Blocks (any fail = stop)
- **V1** — D1 close beyond zone? → ❌ INVALIDATED (remove from `_HOT.md`). Wick close-back-inside = sweep, not invalidation.
- **V1b** — 2 consecutive H4 closes >$5 past zone extreme? `scripts/check_v1b.py --direction <DIR> --zone-top <T> --zone-bottom <B>` → ❌ INVALIDATED, cancel limit.
- **V3** — NFP/FOMC/CPI/US Retail Sales within 2h of London/NY open? → ❌ NO TRADE, cancel live limit.
- **VETO** — VIX>35 (fresh) → all SHORT zones NO TRADE. (FRED VIXCLS freshness guard: if latest date < today−1, suspend the veto, log `vix_stale=true`.)
- **Macro flip** — DFII10/DXY vs baseline (constitution drift table): >0.15% any dir → force re-forecast.

### Q4 — Entry Confluence (max 10, floor 5.0 — confluence_criteria.md R2)
| # | Signal | Wt | Pass |
|---|---|---|---|
| E0 | Entry confirmation | 3.0 | see below |
| E1 | H4+H1 structure aligned today | 2.5 | both HH+HL (long) / LH+LL (short) |
| E2 | DFII10 20d slope supports | 2.0 | slope<0 long / >0 short |
| E3 | Macro drift OK | 1.0 | \|DFII10 now − baseline\| < 0.10 against direction |
| E4 | D1 ATR compressed today | 1.0 | `compressed == True` |
| E5 | DXY 20d slope supports | 0.5 | slope<0 long / >0 short |

**E0 entry confirmation (confirm on candle CLOSE, toward zone direction):**
- 1H engulfing candle (body engulfs prior body), OR
- 1H pin bar (rejection wick ≥ 2.5× body), OR
- 15M CHoCH over 60-candle structure — **must break structure in the zone's direction** (long zone:
  bullish CHoCH = price breaks the most recent lower-high of the 60-candle down-structure; short zone:
  bearish CHoCH = breaks the most recent higher-low of the 60-candle up-structure). A CHoCH against
  the zone direction does NOT count.

### Output
```
entry_confluence ≥ 5.0 AND E0 present → ✅ ORDER LIMIT, anchor = confirmation candle CLOSE
entry_confluence ≥ 5.0 AND no E0     → ✅ ORDER LIMIT, anchor = 50% zone midpoint
entry_confluence < 5.0               → ❌ NO TRADE
```

### Order Limit Calculation (score ≥ 5.0)
```python
# Stop (v2 — no structural pivot)
d1_floor = 0.5 * d1_atr
SL = h4_atr if d1_floor < h4_atr else round((d1_floor + h4_atr) / 2, 2)
lots = int((2000) // (SL * 100))   # round down

# Anchor + outward offset
anchor = confirmation_close if E0_present else round((zone_top + zone_bottom) / 2, 2)
offset = max(SL/3, (10 - entry_confluence_score) * 0.2 * SL)
limit_price = anchor - offset if direction == "LONG" else anchor + offset
sl_price    = limit_price - SL if direction == "LONG" else limit_price + SL
# TP locked from weekly structural anchor: TP1 2.5R (manual), TP2 3.0R (limit), BE at 1.5R
```
Expires: [DATE] 21:00 UTC.

## Output Format
**✅ ORDER LIMIT:**
```
ORDER LIMIT: BUY/SELL [limit_price] | [lots] lots | SL [sl_price] | TP1 2.5R [p] (manual) | TP2 3.0R [p] (limit) | BE @1.5R | expires 21:00 UTC
Entry Confluence: [score]/10 (E0:[✅/❌] E1:[✅/❌] E2:[✅/❌] E3:[✅/❌] E4:[✅/❌] E5:[✅/❌])
Anchor: [confirmation close / 50% zone] | SL $[SL] | offset $[offset] | R:R [computed]
"If price reaches [limit_price], order triggers. Cancel if not hit by 21:00 UTC."
```
**❌ NO TRADE:**
```
NO TRADE — [hard block / score < 5.0]: [specific reason]
[If INVALIDATED: remove zone from _HOT.md]
```

## Save + Update
Save `forecasts/daily/xauusd/[DATE].md` using `wiki/system/templates/daily_validation.md` (Claude
writes markdown directly — no DB). Then update `_HOT.md`: per-zone verdict; remove INVALIDATED;
record limit/SL/TP/expiry on ORDER LIMIT; move filled to Open Position; update Week Risk Used.

## Multi-Zone Handling
Validate every PENDING zone independently. Multiple ORDER LIMITs allowed if zones distinct AND
cumulative open risk + closed loss ≤ $4,000/week. Same-day fill priority: Primary → Secondary → Counter.
