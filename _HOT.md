# _HOT — Session State
*Always current. Updated at end of every session.*
*RULE: hard cap **120 lines**. Current state + last session only. History lives in
`forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat. Prune every session.*

## System Status — v2 ACTIVE
Structured + AI-analysis entry-signal generation. Markdown-only (no DB). Unit = **Trading Zone**
(max 3/wk, ≤1 counter), Zone Confluence R1 + Entry Confluence R2 (max 10, floor 5, E0 confirm 3pt).
10 active instruments (11 incl. JPY trio). Per-instrument character → `constitution.md` multi-instrument
table + `wiki/system/{inst}/`. Never apply gold intuition to FX. Onboarding/sizing history → `decisions.md`.

## Active Forecasts — 2026-W25 (Mon 06-15 → Fri 06-19)
⚠ **HEAVY CB WEEK** — Tue: BoJ + RBA · Wed: FOMC (blocks 8 USD pairs) · Thu: BoE + SNB.
Most USD pairs tradeable **Mon + Fri only**; Wed fully blocked.
- **XAUUSD** [W25](forecasts/weekly/xauusd/2026-W25.md) — **BEARISH/MEDIUM (re-forecast 06-15, ceasefire-updated)**. SHORT 4360–4390 (7.0) + SHORT 4450–4485 (6.0). Spot 4327, both NO TRADE today (below zones). US–Iran ceasefire removed safe-haven bid → rate-bear reasserts; DXY↓ caps at MEDIUM. Inval D1>4435→flips bullish. No counter-long. FOMC Wed block.
- **EURUSD** [W25](forecasts/weekly/eurusd/2026-W25.md) — NEUTRAL/MEDIUM. LONG 1.1500–1.1520 (7.5) + SHORT 1.1618–1.1640 (7.0). Spot 1.1575. ECB hiked 2.25% (EUR+). FOMC Wed.
- **GBPUSD** [W25](forecasts/weekly/gbpusd/2026-W25.md) — NEUTRAL/MEDIUM. SHORT 1.3440–1.3465 (6.5) + COUNTER LONG 1.3304–1.3330 (7.0). Spot 1.3407. Squeeze ON. FOMC Wed + BoE Thu block.
- **EURGBP** [W25](forecasts/weekly/eurgbp/2026-W25.md) — NEUTRAL(long-tilt)/MEDIUM. LONG 0.8608–0.8625 (8.5, best) + SHORT 0.8660–0.8682 (6.0). Spot 0.8634. ECB favors long. BoE Thu block.
- **AUDUSD** [W25](forecasts/weekly/audusd/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.7065–0.7110 (6.5) **→ ✅ LIVE ORDER LIMIT SELL 0.70902 (EC 6.5, 07:16 UTC)** + COUNTER LONG 0.6980–0.7000 (7.0, NO TRADE). Spot 0.70734. ADX 28.9 (veto>30). RBA Tue event risk if filled.
- **NZDUSD** [W25](forecasts/weekly/nzdusd/2026-W25.md) — NEUTRAL/MEDIUM. SHORT 0.5855–0.5890 (6.5) + COUNTER LONG 0.5750–0.5790 (6.5, best, D1 OS). Spot 0.5831. Antipodean gate vs AUD. FOMC Wed.
- **USDCAD** [W25](forecasts/weekly/usdcad/2026-W25.md) — BULLISH/MEDIUM. LONG 1.3830–1.3875 (6.0). Spot 1.3987, RSI 75 OB. SHORT **ADX-vetoed** (34.8>30). VIX abort if >20. FOMC Wed.
- **USDCHF** [W25](forecasts/weekly/usdchf/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.8005–0.8025 (8.5, SNB-cap). Spot 0.7946. DXY slope flipped down. FOMC Wed + SNB Thu block. W24 long 0.79477 closed -1R (SL hit).
- **USDJPY/EURJPY/GBPJPY** [usdjpy](forecasts/weekly/usdjpy/2026-W25.md)·[eurjpy](forecasts/weekly/eurjpy/2026-W25.md)·[gbpjpy](forecasts/weekly/gbpjpy/2026-W25.md) — **⛔ NO ZONES**: BoJ 06-16 + active MoF intervention regime (spots 160.2/185.5/214.8 in/above bands, Mimura 06-10). gbpjpy also BoE. Reassess W26 post-BoJ.
- FX stack: USDCAD LONG + USDCHF SHORT + EUR/GBP fades + AUD/NZD shorts → run `fx_exposure.py` netting at /validate.

## Open Position / Carryover
- none. USDCHF W24 long 0.79477 → **SL HIT 0.79234, LOSS −1R** (logged to `data/trades_log.csv`,
  trade_id usdchf-2026-W24-PRIMARY). Position closed.

## Live Order Limits
**1 LIVE — AUDUSD.** `/validate all` re-ran 2026-06-15 **10:14 UTC** (hourly, fresh pulls 10:1x) →
**0 NEW limits; AUDUSD limit from 07:16 still LIVE & intact.**
- **AUDUSD SELL 0.70902** | 8.09 lots | SL 0.71149 | TP1 2.5R 0.70285 (manual) · TP2 3.0R 0.70161
  (limit) · BE +1.5R 0.70532 | EC **6.5/10** (E0✅ E1✅ E5✅; E2/E3/E4 ❌) | anchor confirm-close
  0.70729 | **expires 2026-06-15 21:00 UTC**. Spot 0.70689 still INSIDE SHORT 0.7065–0.7110;
  **V1b ✅ intact** (H4 closes 0.70719/0.70689, thr 0.71140), ADX 28.9 (<30). 09:00 1H = LONG engulf
  (wrong dir for short) → no new limit; resting order unchanged. ⚠ **Concentration**:
  long-USD overlap w/ open USDCHF long (advisory, keep-USDCHF by EC). ⚠ **RBA 06-16** — if filled, carries into it.
Other 7 USD/gold zones **NO TRADE** (price away / premature E0 below resistance / ADX-veto):
xauusd 4329 below both shorts · eurusd 1.1605 & gbpusd 1.3440 SHORT reclaims fired *below* zone
(not at-resistance; gbpusd+eurgbp TTM squeeze ON) · nzdusd 0.5845 below short, long away · usdcad
1.3978 LONG ~100p above + SHORT ADX-vetoed 34.8 · usdchf 0.7933 SHORT 72p below (H4 oversold, opp).
JPY trio NO ZONES (MoF HARD_BLOCK all 3 + BoJ 06-16). No V1/V1b invalidations; weekend gaps NOTE/NOISE
→ no re-forecast. VIX 19.44 stale (06-11) → veto suspended (n/a here).
Daily files: `forecasts/daily/*/2026-06-15.md` (re-stamped 10:14).

## Week Status
- Week: 2026-W25 | Trades: 0 | Risk allocated: $2000 (1 live limit, audusd, unfilled) | weekly_reforecast_count: 0

## Pending Actions
- **✅ Gold re-forecast + validate done** (06-15). NEUTRAL/MED-LOW; SHORT 4360–4390 / 4450–4485 both
  **NO TRADE today** (EC 3.0, spot 4327 below zones, no E0, ATR expanding + DXY slope against). PENDING —
  wait for rally into 4360–4390 + bearish 1H confirm. Inval D1>4435.
- **🌍 US–IRAN CEASEFIRE (Trump, Sun 06-14) + Hormuz reopening** — material new input, two-way:
  • **gold** safe-haven premium should UNWIND if it holds → rate-bear reasserts → *strengthens* the short
  zones (but data hasn't sold off yet, spot 4327; ceasefire fragile/on-off all year = headline-reversal tail).
  • **oil DOWN** (Hormuz supply back) → CAD-bearish → *supports* usdcad LONG bias. • **risk-ON** mild
  headwind to audusd/nzdusd shorts; JPY weak but MoF-capped. Watch for confirmation it holds before leaning.
- **/validate done for 06-15** (02:00 UTC, 0 limits). Re-run later in session or Mon evening if risk-pair
  shorts (audusd/eurusd/nzdusd) tag their zones with an at-zone E0. Wed = FOMC full block. Clean: Mon + Fri.
- **USDCAD:** VIX abort watch — VIX 19.44 <20 so LONG bias stands; a fresh close >20 flips to fade-USD
  SHORT and kills the 1.3830–1.3875 long. Also D1 RSI 75 OB → late-cycle, keep size honest.
- **AUDUSD:** ADX 28.9 — if D1 closes >30, the COUNTER LONG 0.6980–0.7000 is vetoed.
- **XAUUSD:** Iran/Hormuz headline risk is the two-way tail; D1 close >4435 (POC) reverses the short thesis.
- **MoF watch (JPY trio):** flat through BoJ 06-16. Post-BoJ washouts = W26 setups (usdjpy 158–159 long if
  calm; eurjpy 183–184 / short fade 185+; gbpjpy short fade 214–215). Spots currently IN intervention bands.
- **Shadow ledger:** 14 W25 zones registered (`zone_ledger.csv`). W24 resolved: 11 PENDING, 3 RUNNING,
  1 LOSS (gbpusd SEC −1R). Calibration n=1 → all edges UNPROVEN (INSUFFICIENT n<10). No DEAD flags.
- ⚠ **CB calendar:** SNB only verified through 06-18 in `cb_calendar_2026.json` — window extends past it;
  all W25 decisions ARE captured, but extend verification before next /weekly. Verify RBNZ H2 / SNB Sep-Dec.
- **✅ Econ-calendar (#1/#2) NOW ACTIVE — switched to Forex Factory free JSON (06-15).** Finnhub's
  `/calendar/economic` was premium-gated ("no access"); replaced `fetch_econ_calendar()` with the FF
  faireconomy feed (no key). `calendar.csv` populated: 103 events, 19 High-impact, coverage→06-19;
  gate now surfaces FOMC 06-17 + GB CPI 06-17 + UK jobs 06-18 etc. (in-sandbox the lastweek/nextweek
  feeds returned empty → `--retro` surprise + next-week coverage may need the operator's local run; thisweek
  is solid). News feed (`check_news`, Finnhub `/news`) **verified WORKING** (06-15, 101 headlines, free
  tier — only the calendar endpoint was gated). No change needed; FF is a calendar, not a news source.
- **E0 RECLAIM (D027, PENDING-VALIDATION):** RSI-reclaim primary E0; pin/engulf fallback still counts until
  ledger confirms on gated subset. Pull **ENTRY TRIGGERS** block computes them.

## Last Session
2026-06-15 10:14 UTC (**/validate ALL — 11 instruments, hourly**): fresh pulls 10:11–10:15, all 11.
Gates: CB (BoJ/RBA Tue 06-16, FOMC Wed 06-17, BoE/SNB Thu 06-18 — all future, today clean), econ-cal
(FOMC cluster 06-17 in window, none today within 2h of opens), JPY intervention HARD_BLOCK all 3 (spots
160.24/185.47/214.83 in/above bands, Mimura jawboning). **0 NEW order limits; AUDUSD SELL 0.70902 from
07:16 still LIVE** (V1b ✅ H4 0.70719/0.70689 < thr 0.71140, spot 0.70689 inside zone, ADX 28.9; 09:00 1H
= LONG engulf, wrong dir → no new short). All other zones NO TRADE (price away / premature E0 below
resistance / usdcad ADX-veto 34.8). No invalidations, no re-forecast. USDCHF open long 0.79477 ~−0.6R
(spot 0.79338), SL/BE intact. 11 daily files re-stamped 10:14. Also: added <45min freshness guard to the
hourly scheduled task (skips runs too close together). Telegram sent.
2026-06-15 09:50 & 08:16 UTC (**/validate ALL hourly**): 0 NEW limits both runs; AUDUSD SELL 0.70902
LIVE & intact (V1b ✅, spot inside zone, ADX 28.9); all other zones NO TRADE; no inval/re-forecast.
2026-06-15 07:16 UTC (**/validate ALL — 11 instruments, hourly**): fresh pulls 07:12, all 11 paced
(JPY trio pulled for intervention spots). Gates: CB (BoJ/RBA Tue, FOMC Wed, BoE/SNB Thu — all future,
today clean), econ-cal (only FOMC-cluster 06-17 in window), JPY intervention HARD_BLOCK all 3 (spots
160.1/185.8/215.1 IN bands + Mimura jawboning). **1 ORDER LIMIT: AUDUSD SELL 0.70902** (EC 6.5) — London
open fired the week's first E0 (06:00 1H bearish RSI-reclaim at resistance, spot inside SHORT zone).
Ledger flags long-USD concentration w/ open USDCHF long (advisory); RBA-06-16 event-risk flagged. All
other zones NO TRADE (price away / premature reclaim below resistance / usdcad ADX-veto). No
invalidations, no re-forecast. USDCHF open long 0.79477 now ~−0.7R (spot 0.79304), SL/BE intact. 11 daily
files stamped 07:16. Telegram summary sent.
2026-06-15 (**/weekly xauusd re-forecast + corrections**): weekend-gap re-forecast (gap voided Sunday
W25 gold) → NEUTRAL/MED-LOW, SHORT 4360–4390 (7.0) + 4450–4485 (6.0), no counter-long; ledger rows redrawn
in place (no dup), yield_environment + belief log updated. Diagnosed Finnhub: key present, **plan lacks
econ-calendar endpoint** (premium). Corrected USDCHF: operator **IS** long 0.79477 (real W24 fill, ≈flat) —
thesis flipped bearish, SNB Thu; decision pending. Files: `forecasts/weekly/xauusd/2026-W25.md`.
2026-06-14 (**/weekly ALL — 11 instruments, W25**): published **14 zones across 8 USD pairs**; JPY trio
NO ZONES (BoJ+MoF). ECB hike 2.25% → eurusd NEUTRAL + eurgbp long-favored; DXY slope down → usdchf flips
BEARISH (8.5 short); usdcad short ADX-vetoed (34.8); gold MEDIUM. Files: `forecasts/weekly/*/2026-W25.md`.
