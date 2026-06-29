---
description: Daily validation on PENDING Trading Zones — Entry Confluence gating, 07:30 UTC pre-London.
argument-hint: [instrument] [date]
model: claude-sonnet-4-6
---
Run daily validation on PENDING Trading Zones, 07:30 UTC before London open.

> **Model:** runs on Sonnet 4.6 — this command is mechanical (script-run gates + pure-formula
> SL/offset + programmatic EC). No Opus needed. If a run hits genuinely ambiguous judgment
> (contradiction protocol, a borderline re-forecast call), flag it for an Opus follow-up rather than
> forcing the call here.

Arguments: `[instrument] [date]`. Instrument ∈ {xauusd, eurusd, gbpusd, eurgbp, audusd, nzdusd,
usdcad, usdchf, usdjpy, eurjpy, gbpjpy} — **default (no arg) = ALL 11 instruments**, validated in the order listed. Date YYYY-MM-DD (default today). Pass a single instrument to validate just that one.
Batch run: do Step 0b (DB guard) ONCE up front; space the per-instrument `weekly_pull.py` calls ~8s apart (Twelve Data free tier = 8 req/min).

> Per-pair character / macro / VIX-veto / TICK / intervention rules are defined ONCE in
> `constitution.md` multi-instrument table + each pair's `confluence_criteria.md`. Step 0 table below
> + the VETO / macro-flip blocks carry only the command-specific deltas (operative gates + edge
> thresholds). Don't re-derive a pair's character here.

**The four questions /validate answers, per zone:**
1. **Is the forecast still valid?** (V1/V1b structure intact, V3 news clear)
2. **Has bias flipped?** (macro drift / counter-move vs baseline)
3. **Should we re-forecast?** (mid-week trigger tree — constitution "Mid-Week Re-Forecast Triggers")
4. **Can we set an order limit?** (Entry Confluence ≥ 5.0 → ORDER LIMIT, else NO TRADE)

Output per zone is exactly one of: ✅ ORDER LIMIT | ❌ NO TRADE / INVALIDATED.

## Step 0 — Instrument parametrization (set ALL of these first)
| Param | xauusd | eurusd | gbpusd | eurgbp (cross) | audusd | nzdusd | usdcad (USD-base) | usdchf (USD-base) | usdjpy (USD-base, JPY) | eurjpy (cross, JPY) | gbpjpy (cross, JPY) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `TICK_MULTIPLIER` | 100 | 100000 | 100000 | 100000 (USD sizing, no GBP convert — operator) | 100000 | 100000 | 100000 (~28% under, CAD pip — accepted) | 100000 (~25% over, CHF pip — accepted) | **650 STATIC** (≈100000/154; ±10% drift accepted) | **650 STATIC** (JPY-quoted — pip value tracks USDJPY) | **650 STATIC** (JPY-quoted — pip value tracks USDJPY) |
| `MIN_BAR_RANGE` (H4 filter) | 1.0 | 0.0003 | 0.0003 | 0.0002 | 0.0003 | 0.0003 | 0.0003 | 0.0003 | 0.03 | 0.03 | 0.05 |
| `PRICE_DP` | 2 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **3** (pip 0.01) | **3** (pip 0.01) | **3** (pip 0.01) |
| `V1B_BUFFER` | 5.0 | 0.0005 | 0.0006 | 0.0004 | 0.0004 | 0.0004 | 0.0005 | 0.0004 | **0.04** (4 JPY pips) | **0.04** (4 JPY pips) | **0.05** (5 JPY pips — highest ATR) |
| Character | momentum | mean-reversion | mean-reversion | mean-reversion, macro-light | mean-reversion, H4-centric | mean-reversion, macro-light (weakest edges) | mean-reversion, USD-base | mean-reversion, USD-base, H1-centric | **asymmetric carry-drift** (LONG drift / SHORT extreme-fade) | **symmetric mean-reversion + calm-drift**, macro NONE | **extension-fade, SHORT-dominant**, NO calm row, macro NONE |
| Confluence R2 | xauusd | eurusd | gbpusd | eurgbp | audusd | nzdusd | usdcad | usdchf | usdjpy (direction-aware) | eurjpy | gbpjpy |
| Macro baseline field | `baseline_dfii10` | `baseline_dgs2` | `baseline_dgs2` | `baseline_rate_diff` (weak) | `baseline_dgs2` | `baseline_dgs2` (context only) | `baseline_dgs2` (POLARITY FLIPPED) | `baseline_dgs2` (FLIPPED, weak; DXY slope = macro) | `baseline_dgs2` (DEAD; DXY slope = macro) | `baseline_ecb_rate` (context only — macro dead) | `baseline_sonia_rate` (context only — macro dead) |
| VIX veto blocks | SHORTs | LONGs | LONGs | **NONE** (risk-off→EURGBP up) | **NONE** (VIX level scores, inverted) | **NONE** (weak inverted tilt) | **NONE** (VIX>20 → SHORT bias scores) | **NONE** (washout — no gate, no score) | **NONE** (washout — no gate, no score) | **NONE** (dead, t=0.91 — no gate, no score) | **NONE** (dead, t=0.89 — no gate, no score) |
| DXY-jump block | — | AGAINST zone | AGAINST zone | NONE (no USD leg) | **NONE** (dead, t=−0.85) | **NONE** (dead, t=0.24) | **NONE** (dead) | **NONE** (jump anti; 20d SLOPE scores in E2) | **NONE** (jump anti; 20d SLOPE scores in E2) | NONE (no USD leg) | NONE (no USD leg) |

Read the instrument's `wiki/system/{instrument}/confluence_criteria.md` (R2) and
`wiki/system/{instrument}/{instrument}_profile.md` before scoring. FX uses a DIFFERENT R2 than
gold (mean-reversion oscillators, not H4-structure + real-yield).

## Step 0b — DB durability preflight (MANDATORY — never skip)
```bash
bash scripts/pyrun.sh scripts/db_guard.py all   # WAL checkpoint → integrity check → rotating backup
```
Non-zero exit = the canonical store is corrupt. **STOP** — do not write zones/ledger into a corrupt
DB. Recover first: `sqlite3 data/database/index.db .recover | sqlite3 fixed.db`, swap in, re-run.

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
import pandas as pd, sys
sys.path.insert(0, "scripts"); import db        # data/database/index.db is the canonical store
INSTRUMENT = "xauusd"          # ← set per Step 0
MIN_BAR_RANGE = 1.0            # ← gold 1.0 | FX 0.0003
TICK_MULTIPLIER = 100          # ← gold 100 | FX 100000
DP = 2                         # ← gold 2  | FX 5

def _ohlc(tf):                 # bars from the `ohlc` table (no more CSVs)
    df = db.read_ohlc(INSTRUMENT, tf)
    df["datetime"] = pd.to_datetime(df["datetime"])
    for c in ("open", "high", "low", "close", "volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values("datetime")
def _fred(sid):                # macro_series slice → frame with numeric `value`
    s = db.read_slice("macro_series", {"series_id": sid}, ["date", "value"])
    s["value"] = pd.to_numeric(s["value"], errors="coerce"); return s.dropna()
def _mkt(src, sym):            # market_series slice (yahoo DXY / commodities)
    s = db.read_slice("market_series", {"source": src, "symbol": sym}, ["date", "value"])
    s["value"] = pd.to_numeric(s["value"], errors="coerce"); return s.dropna()

h4, d1, h1, m15 = _ohlc("4h"), _ohlc("1day"), _ohlc("1h"), _ohlc("15min")

# Macro — branch on instrument
if INSTRUMENT == "xauusd":
    s = _fred("DFII10")   # real yield = primary driver
    macro_now = round(float(s.value.iloc[-1]),3); macro_prev = round(float(s.value.iloc[-2]),3)
    macro_slope = round(float(s.value.iloc[-1]) - float(s.value.iloc[-20]),3)
elif INSTRUMENT == "eurgbp":
    # CROSS macro = EUR−GBP rate diff (ECBDFR−SONIA). EG2: thin/DEAD → LOW-weight TILT, not a gate.
    eu = _fred("ECBDFR"); gb = _fred("IUDSOIA")
    macro_now  = round(float(eu.value.iloc[-1]) - float(gb.value.iloc[-1]), 3)          # EUR−GBP diff now
    macro_prev = round(float(eu.value.iloc[-2]) - float(gb.value.iloc[-2]), 3)
    macro_slope= round(macro_now - (float(eu.value.iloc[-20]) - float(gb.value.iloc[-20])), 3)  # 20d diff change
elif INSTRUMENT == "eurjpy":
    # CROSS-JPY: macro fully DEAD (ECB leg anti, no daily BoJ series). ECBDFR = context only.
    eu = _fred("ECBDFR")
    macro_now = round(float(eu.value.iloc[-1]),3); macro_prev = round(float(eu.value.iloc[-2]),3)
    macro_slope = round(float(eu.value.iloc[-1]) - float(eu.value.iloc[-20]),3)   # context, never gates
elif INSTRUMENT == "gbpjpy":
    # CROSS-JPY #2: macro fully DEAD (SONIA leg ns, no daily BoJ series). IUDSOIA = context only.
    gb = _fred("IUDSOIA")
    macro_now = round(float(gb.value.iloc[-1]),3); macro_prev = round(float(gb.value.iloc[-2]),3)
    macro_slope = round(float(gb.value.iloc[-1]) - float(gb.value.iloc[-20]),3)   # context, never gates
else:  # USD pairs (eurusd / gbpusd / audusd): US 2Y = rate-momentum leg
    s = _fred("DGS2")
    macro_now = round(float(s.value.iloc[-1]),3); macro_prev = round(float(s.value.iloc[-2]),3)
    macro_slope = round(float(s.value.iloc[-1]) - float(s.value.iloc[-20]),3)
# DXY jump: scored/blocked for eurusd+gbpusd ONLY. eurgbp = no USD leg; audusd = measured DEAD
# (t=−0.85) → compute for context, never block.
if INSTRUMENT not in ("eurgbp", "eurjpy", "gbpjpy"):     # crosses: no USD leg → no DXY
    dxy = _mkt("yahoo", "DXY"); dxy_jump = round(float(dxy.value.iloc[-1]) - float(dxy.value.iloc[-2]), 3)
else:
    dxy_jump = None
vix = _fred("VIXCLS"); vix_now = float(vix.value.iloc[-1]); vix_spike = vix_now - float(vix.value.iloc[-2])

def atr(df, p=14):
    tr = pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(p).mean()
def drop_open_bar(df, hrs):
    now = pd.Timestamp.now(tz="UTC").tz_localize(None); last = pd.Timestamp(df["datetime"].iloc[-1])
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
**Step 3.0 (MANDATORY, before any web query):** run the static central-bank calendar —
```bash
bash scripts/pyrun.sh scripts/check_cb_calendar.py --date [DATE] --days 2
```
Any reported decision today/tomorrow for this instrument's HARD BLOCK list = V3 candidate
regardless of what web search finds. Exit 1 = calendar unverified for the window — treat as
unknown event risk, do not place orders until `scripts/config/cb_calendar_{year}.json` is updated.

**Step 3.0b (MANDATORY) — scheduled data-release gate (#1/#2):**
```bash
bash scripts/pyrun.sh scripts/check_econ_calendar.py --instrument [INST] --date [DATE] --days 2
```
Any HIGH-impact release today/tomorrow for the pair's currency legs = V3 candidate (no-trade
release ±30min). Exit 1 = calendar CSV stale/missing → refetch via `weekly_pull.py` (or fall
back to web search) before trusting "no events". Complements 3.0 (decisions) with data releases.

**Step 3.0c (JPY pairs only, MANDATORY) — intervention watch (#4):**
```bash
bash scripts/pyrun.sh scripts/check_intervention_watch.py --instrument [usdjpy|eurjpy|gbpjpy] --spot [SPOT]
```
HARD_BLOCK new longs if spot in the MoF intervention zone; CAUTION (cap conviction MEDIUM) in the
band or if recent jawboning. Exit 1 = watch stale → refresh `intervention_watch.json` jawboning[]
from web search first. This is the structured form of the manual MoF read in Query A.

**Query A (V3 hard block):** economic calendar [DATE]. xauusd + USD pairs share US events (NFP/FOMC/
CPI/Retail). Pairs also: ECB rate decision (eurusd), BoE rate decision (gbpusd), RBA decision +
AU CPI/employment (audusd), RBNZ OCR + NZ CPI/jobs (nzdusd; GDT dairy = caution), BoC decision +
CAD CPI/jobs (usdcad — ⚠ CAD jobs often shares 12:30 UTC slot with US data; OPEC/EIA oil = caution),
SNB decision (usdchf — QUARTERLY Mar/Jun/Sep/Dec Thu 08:30 UTC = HARD; SNB speeches/intervention
headlines = caution; CH CPI = caution only), BoJ decision (usdjpy — ~8/yr = HARD; **active MoF
jawboning / rate-check headlines = HARD** — intervention slams 300–500 pips; Tokyo/national CPI = caution),
**eurjpy (cross-JPY): hard blocks = BoJ decision + MoF jawboning (interventions slam ALL JPY crosses)
+ ECB decision + EZ tier-1 CPI/GDP. US events = CAUTION ONLY (no USD leg, but both legs transmit)**,
**gbpjpy (cross-JPY #2): hard blocks = BoJ decision + MoF jawboning (GBPJPY slams = largest of the
crosses) + BoE decision + UK tier-1 CPI/jobs. US events = CAUTION ONLY; Tokyo CPI = caution**
— own central bank. China tier-1 = caution→hard for audusd/nzdusd if commodity move in progress.
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
- **V3 (two cases — see constitution "Pre-Event Flatten", D028):**
  - **Event WINDOW** — hard event within 2h of the 08:00 London / 13:00 NY open, OR a release ±30min
    away right now → ❌ NO TRADE, cancel live limit. (Entry-in-window risk — unchanged hard block.)
  - **Forward-carry** — a hard event (CB decision / tier-1 release) falls *later* in the hold horizon
    but is NOT in the window above → **ALLOW the entry** (score it normally); set
    `flatten_time = event_time − 60min` as the limit expiry instead of 21:00 UTC, and force-flatten
    any fill at `flatten_time`. If several events qualify, use the earliest.
  - **Still NO TRADE regardless of flatten** — the pair's OWN central bank deciding today, the JPY-trio
    NO ZONES standing rule, and active MoF intervention. Flatten only relaxes the forward-carry case
    (e.g. a Tue entry that would otherwise carry into Wed FOMC), never the event hour itself.
- **VETO** — trigger = VIX>35 fresh, OR VIX 1d spike>3 (FX). Gate per pair (justification/t-stats →
  constitution VIX-veto row + `confluence_criteria.md`):

  | Pair | VIX veto | VIX score | Other hard vetoes (beyond V1/V1b/V3) |
  |---|---|---|---|
  | xauusd | SHORTs NO TRADE | — | — |
  | eurusd / gbpusd | LONGs NO TRADE | — | — |
  | eurgbp | NONE (spike = weak LONG tilt Z4 0.5) | tilt only | D1 ADX>30 vs the fade |
  | audusd | NONE (level INVERTED, scores R2 E4) | level scores | D1 ADX>30 vs the fade |
  | nzdusd | NONE (level inverted, weaker) | level scores | D1 ADX>30 vs the fade |
  | usdcad | NONE (VIX>20→SHORT bias, scores R2 E4) | level scores | D1 ADX>30 vs the fade |
  | usdchf | NONE (washout) | none | D1 ADX>30 vs the fade; SNB decision/communication day |
  | usdjpy | NONE (washout) | none | BoJ day / active MoF jawboning; **H1-only SHORT setups prohibited** (need D1/H4 extreme); LONG ≥158 at fresh highs → cap MEDIUM |
  | eurjpy | NONE (washout) | none | BoJ day / MoF jawboning; ECB decision; D1 ADX>30 vs the fade; record-high LONG in intervention watch → cap MEDIUM |
  | gbpjpy | NONE (washout) | none | BoJ day / MoF jawboning; BoE decision; D1 ADX>30 vs the fade; **SHORT entry inside 13–15 UTC** NY open; record-high LONG in intervention watch → cap MEDIUM |

  FRED VIXCLS freshness guard: latest date < today−1 → suspend veto, log `vix_stale=true`.
- **Macro flip** — macro series vs baseline (constitution drift table): >0.15% any dir → force
  re-forecast. DXY/rate gate per pair (deadness justification → constitution macro-direction row):

  | Pair | DXY-jump block | Other macro-flip rule |
  |---|---|---|
  | eurusd / gbpusd | DXY 1d jump >0.5 AGAINST a zone → that zone NO TRADE | — |
  | eurgbp | NONE (no USD leg) | rate-diff drift = weak/informational, not a gate |
  | audusd | NONE (dead) | — |
  | nzdusd | NONE (dead) | NO US2Y gate (DGS2 baseline = drift-tracking context only) |
  | usdcad | NONE (dead) | US2Y drift FLIPPED polarity (US2Y rising = WITH long-USDCAD) |
  | usdchf | NONE (jump anti — fade it) | DXY 20d SLOPE flip AGAINST a zone = re-check bias (R2 E2); US2Y FLIPPED |
  | usdjpy | NONE (jump anti) | DXY 20d SLOPE flip AGAINST a zone = re-check bias (R2 E2); US2Y DEAD (context only) |
  | eurjpy / gbpjpy | NONE (cross, no USD leg) | NO macro-flip gate at all — price-driven only: T3 counter-move 1.5% + T4 shock |

### Q4 — Entry Confluence (max 10, floor 5.0)
**Use `wiki/system/{INSTRUMENT}/confluence_criteria.md` R2 — the table differs by instrument.**

> **E0 trigger (D027):** read the pull **ENTRY TRIGGERS (E0, latest closed 1H)** block — it computes
> RSI-reclaim / band-reclaim / Stoch-reclaim / pin / engulf both directions (no longer eyeballed).
> Each pair's **PRIMARY** E0 is set in its R2 E0 row (RSI-reclaim for most FX; pin/engulf for
> gbpusd/eurgbp; band-reclaim for usdcad; continuation for xauusd + usdjpy-LONG). Pin/engulf retained
> as fallback everywhere. **PENDING live-ledger validation** — pin/engulf still counts if reclaim absent.

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
- **usdcad (mean-reversion, USD-base):** E0 reversal confirm 3.0 | E1 H4 oscillator/band still
  extreme 2.5 | E2 H1 oscillator extreme (long: W%R/CCI/RSI2 t 2.9–3.45; short: CCI>+100 t=3.08)
  1.5 | E3 non-trending ADX<25 1.0 | E4 macro regime aligned (VIX fade-USD + US2Y flipped) 1.0 |
  E5 structure intact 1.0. Remember: USD leg sign — long usdcad stacks with SHORT majors in the
  fx_exposure ledger. (See usdcad `confluence_criteria.md` R2.)
- **usdchf (mean-reversion, USD-base, H1-centric):** E0 reversal confirm 3.0 | E1 H1 oscillator
  still extreme 2.5 (short: W%R>−20/RSI>65/Keltner-high t 4.5–5.5; long: W%R<−80/RSI2<10) |
  E2 DXY 20d slope aligned 1.5 | E3 squeeze/calm context 1.0 | E4 non-trending ADX<25 1.0 |
  E5 structure intact 1.0. NO VIX row. USD leg: long usdchf stacks with SHORT majors + LONG usdcad
  in the ledger; usdchf-short vs eurusd-long are near-duplicates (CHF≈EUR bloc) — prefer higher EC.
  (See usdchf `confluence_criteria.md` R2.)
- **usdjpy (asymmetric carry-drift, USD-base, DIRECTION-AWARE):** E0 confirm 3.0 | E1 side engine
  still live 2.5 (LONG: squeeze/calm still on, t 3.3–4.5; SHORT: H4 oscillator still extreme, t
  2.1–3.1) | E2 DXY 20d slope aligned 1.5 | E3 LONG only: NY-session entry window 12–16 UTC 1.0
  (H1 drift t=4.71; NY short = anti) | E4 structure intact 1.0 | E5 not extended (ADX<25 or
  pullback, no breakout chase) 1.0. NO VIX row. E0 for LONGS = continuation/dip-turn (drift, like
  xauusd), for SHORTS = reversal at D1/H4 extreme. USD leg: long usdjpy stacks with long usdchf/
  usdcad + SHORT majors in ledger. (See usdjpy `confluence_criteria.md` R2.)
- **eurjpy (cross-JPY, symmetric mean-reversion):** E0 reversal confirm 3.0 | E1 extreme still live
  2.5 (LONG: washout — Stoch/W%R/Keltner-low; SHORT: H1/H4 still overbought — W%R>−20 t=4.21,
  RSI>65 t=3.61) | E2 session window 1.5 (LONG: NY/London overlap 12–16 UTC t=3.02 · SHORT: London
  open 07–09 UTC t=2.77) | E3 calm regime intact 1.0 (LONG full, SHORT 0.5) | E4 structure intact
  1.0 | E5 not extended (ADX<25 / pullback, no breakout chase) 1.0. NO macro row, NO VIX row.
  JPY leg: long eurjpy stacks with long usdjpy (2× short JPY = doubled MoF tail — ledger flags);
  EUR leg stacks with eurusd/eurgbp longs. (See eurjpy `confluence_criteria.md` R2.)
- **gbpjpy (cross-JPY #2, extension-fade, SHORT-dominant):** E0 reversal confirm 3.0 | E1 extreme
  still live 2.5 (SHORT: H4 still overbought — Stoch>80 t=3.80, W%R>−20 t=3.09, RSI>65 t=3.58;
  LONG: washout still present — Keltner-low/RSI<35/20d low) | E2 session 1.5 (LONG: NY/London
  overlap 12–16 UTC t=4.20 = 1.5 · SHORT: outside 12–16 UTC = 0.75, **inside 13–15 UTC = 0,
  anti −3.84**) | E3 H1 timing structure 1.0 (LONG: inside-bar break t=2.62 / 20d low · SHORT:
  H1 RSI>65 t=2.59) | E4 structure intact 1.0 | E5 not extended (ADX<25 / pullback, no breakout
  chase) 1.0. NO macro row, NO VIX row, NO calm row (dead). JPY leg: long gbpjpy stacks with long
  usdjpy/eurjpy (3 JPY pairs live — tripled MoF tail when same-dir; take single cleanest); GBP leg
  stacks with gbpusd-long, inverse-overlaps eurgbp. (See gbpjpy `confluence_criteria.md` R2.)

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
**Forward-carry flatten (D028):** if a hard event falls in the hold horizon (V3 forward-carry case),
an ORDER LIMIT is still emitted but expiry = `flatten_time = event−60min`; add a `> [!warning]
Flatten:` callout in the daily file naming the event + flatten_time, and surface it as a Telegram
flag (`⏱ <PAIR> flatten by <HH:MM> UTC pre-<event>`).

### Order Limit Calculation (score ≥ 5.0)
```python
d1_floor = 0.5 * d1_atr
SL = h4_atr if d1_floor < h4_atr else round((d1_floor + h4_atr) / 2, DP)
anchor = confirmation_close if E0_present else round((zone_top + zone_bottom) / 2, DP)
offset = max(SL/3, (10 - entry_confluence_score) * 0.2 * SL)
limit_price = anchor - offset if direction == "LONG" else anchor + offset
sl_price    = limit_price - SL if direction == "LONG" else limit_price + SL
# TP locked from weekly structural anchor: TP1 2.5R (manual), TP2 3.0R (limit), BE at 1.5R
```
Expires: [DATE] 21:00 UTC — UNLESS a hard event falls in the hold horizon (D028 forward-carry),
in which case expiry = `event_time − 60min` (flatten_time) and any fill is force-flattened then.

## Output Format
**✅ ORDER LIMIT:**
```
[INSTRUMENT] ORDER LIMIT: BUY/SELL [limit_price] | SL [sl_price] | TP1 2.5R [p] (manual) | TP2 3.0R [p] (limit) | BE @1.5R | expires [21:00 UTC or flatten_time=event−60min]
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
(Claude writes the forecast markdown directly). Then update `_HOT.md`: per-zone verdict; remove
INVALIDATED; record limit/SL/TP/expiry on ORDER LIMIT; move filled to Open Position; update Risk Used.

Write each zone's verdict back to the ledger (one call per validated zone) so the frontend reads per-zone status/R2/limit from the `zone_ledger` table instead of scraping this markdown:
```
bash scripts/pyrun.sh scripts/zone_ledger.py validate \
    --zone-id <instrument>-<week>-<LABEL> --verdict ORDER_LIMIT|NO_TRADE|INVALIDATED \
    [--entry-confluence <R2>] [--limit-price <price on ORDER_LIMIT>] --date <DATE> \
    [--e0] [--hard-block]
```
Pass `--e0` whenever the ORDER_LIMIT anchor is a **confirmation candle CLOSE** (E0 present). Omit it when the anchor is the **50% zone midpoint** (no E0) — see the anchor branch at lines 311–312/330.

**Asymmetric anchor lock (D032) — the ledger applies this, you just feed + read it**
Only an **E0-confirmed** `ORDER_LIMIT` (`--e0`) locks its anchor (limit + EC) for 4h so the hourly re-run stops whipsawing the resting limit. A **no-E0 (50%-midpoint)** `ORDER_LIMIT` writes the verdict but is **never locked** — it keeps re-deriving every hour (midpoint anchors are not a committed entry). You always call `validate` with the freshly computed verdict/EC/limit; the ledger decides what to keep:

* ACCEPT (E0) — first `--e0` ORDER_LIMIT (no live lock): the fresh limit is stored, lock set to now+4h (clamped to 21:00 UTC).
* ACCEPT (no-E0) — ORDER_LIMIT without `--e0`: verdict/limit/EC written, **no lock** — re-derives next hour.
* UPGRADE — a strictly higher EC **E0** ORDER_LIMIT while locked: re-anchors to the new limit/EC and resets the 4h clock. (Anchor can only improve.)
* HOLD — an equal/lower EC E0 ORDER_LIMIT, a **no-E0 (midpoint)** ORDER_LIMIT, or a soft `NO_TRADE` (E0 lapsed / EC dipped below floor but no hard gate), while locked: the locked limit/EC/verdict are kept; your fresh numbers are ignored until the lock expires.
* CANCEL — `INVALIDATED`, or `NO_TRADE --hard-block`, always wins: writes the verdict and clears the lock.

You MUST pass `--hard-block` on a NO_TRADE that is a real gate failure — V3 event window, MoF intervention, or a macro-flip re-forecast (use `--verdict INVALIDATED` for a V1/V1b breach) — so the lock is cleared rather than silently held. A plain `NO_TRADE` (no `--hard-block`) is a soft downgrade and is ignored while a lock is live. When in doubt on a hard gate, pass it.

Read back the effective state. `validate` prints `effective: verdict=… EC=… limit=… lock=…` — that post-lock line is the source of truth. If the result is HOLD, write the LOCKED limit/EC into the daily markdown + `_HOT.md`, not your freshly-recomputed numbers, and add a one-line `> [!note] Anchor locked until <HH:MM> UTC (EC <locked>)` so the file matches the resting order. On a HELD soft-NO_TRADE the zone stays an ORDER LIMIT in the file (it is still live).

The DB (`data/database/index.db`) is otherwise written live by the pipeline (`db.py` state registries, `ohlc_store` OHLC, `weekly_pull.py` market/macro/news sync) — no import/refresh step.

## Multi-Zone Handling
Validate every PENDING zone for the instrument independently. Multiple ORDER LIMITs allowed if zones
distinct (each risks 1R; no weekly cap). Same-day fill priority: Primary → Secondary → Counter.
Default run validates every instrument in sequence; a single-instrument arg restricts to one.

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

## Telegram Summary Format (for scheduled/automated runs)
After a run completes, emit a concise plain-text summary and send it via
`printf '%s' "$MSG" | bash scripts/pyrun.sh scripts/notify_telegram.py` (helper reads
`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` from `.env`; fails safe if absent). This section is the
single source of truth for the message layout — automation references it, not its own copy.

Plain text only — the sender sets no `parse_mode`, so use emoji + blank lines + `•` bullets for
structure (no `*bold*` / `_italics_` / `<b>`; they render as literal characters). Put a blank line
between every block. Keep under ~20 lines / 4096 chars (Telegram cap; the helper truncates).

Layout (N ≥ 1 — one 🟢/🔴 block per ORDER LIMIT):
```
📋 VALIDATE · <YYYY-MM-DD> <HH:MM> UTC
━━━━━━━━━━━━━━━━
✅ Order limits: <N>

🟢 <PAIR> LONG @<limit>
   SL <sl> · TP1 <tp1> · EC <score>/10

🔴 <PAIR> SHORT @<limit>
   SL <sl> · TP1 <tp1> · EC <score>/10

⚠️ Flags
• <flag>

📌 <closing status>
```
Layout (N = 0 — no order blocks; reason on its own line):
```
📋 VALIDATE · <YYYY-MM-DD> <HH:MM> UTC
━━━━━━━━━━━━━━━━
🚫 Order limits: 0
<reason — e.g. hard-block week (FOMC), all below EC floor, all PENDING>

⚠️ Flags
• <flag>

📌 <closing status>
```
Rules:
- Header line + the `Order limits:` count line are always present (✅ if N≥1, 🚫 if N=0).
- One 🟢 (LONG) / 🔴 (SHORT) block per ORDER LIMIT; line 2 holds SL · TP1 · EC. Skip
  PENDING / NO-TRADE zones entirely.
- `N = 0` → omit all order blocks; put the reason on the line directly under the count.
- `⚠️ Flags` block: one `•` bullet per re-forecast trigger, V1/V1b/V3 INVALIDATION, or CONCENTRATED
  netting advisory. Omit the whole block (header + bullets) if there are none.
- Close with a `📌` status line (e.g. `All zones PENDING · none invalidated`, or open-position note).
