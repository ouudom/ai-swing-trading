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
- **AUDUSD** [W25](forecasts/weekly/audusd/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.7065–0.7110 (6.5) + COUNTER LONG 0.6980–0.7000 (7.0). Spot 0.7045. ADX 28.9 (veto>30). RBA Tue + FOMC Wed block.
- **NZDUSD** [W25](forecasts/weekly/nzdusd/2026-W25.md) — NEUTRAL/MEDIUM. SHORT 0.5855–0.5890 (6.5) + COUNTER LONG 0.5750–0.5790 (6.5, best, D1 OS). Spot 0.5831. Antipodean gate vs AUD. FOMC Wed.
- **USDCAD** [W25](forecasts/weekly/usdcad/2026-W25.md) — BULLISH/MEDIUM. LONG 1.3830–1.3875 (6.0). Spot 1.3987, RSI 75 OB. SHORT **ADX-vetoed** (34.8>30). VIX abort if >20. FOMC Wed.
- **USDCHF** [W25](forecasts/weekly/usdchf/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.8005–0.8025 (8.5, SNB-cap). Spot 0.7946. DXY slope flipped down. FOMC Wed + SNB Thu block. ⚠ **operator IS long 0.79477 (W24) — thesis now flipped bearish; see Open Position.**
- **USDJPY/EURJPY/GBPJPY** [usdjpy](forecasts/weekly/usdjpy/2026-W25.md)·[eurjpy](forecasts/weekly/eurjpy/2026-W25.md)·[gbpjpy](forecasts/weekly/gbpjpy/2026-W25.md) — **⛔ NO ZONES**: BoJ 06-16 + active MoF intervention regime (spots 160.2/185.5/214.8 in/above bands, Mimura 06-10). gbpjpy also BoE. Reassess W26 post-BoJ.
- FX stack: USDCAD LONG + USDCHF SHORT + EUR/GBP fades + AUD/NZD shorts → run `fx_exposure.py` netting at /validate.

## Open Position / Carryover
- **⚠ USDCHF LONG — REAL FILL (corrected 06-15).** Operator confirms entry **0.79477** (8.23 lots,
  W24 order). SL **0.79234** · TP1 2.5R **0.80085** (manual) · TP2 3.0R **0.80206** (limit) · BE @+1.5R
  **0.79842**. R = 0.00243. Spot **0.79461 ≈ flat** (−1.6p, ~−0.07R). SL/TP intact, BE not triggered.
  **Thesis FLIPPED:** the long was justified by DXY 20d slope RISING; W25 that slope rolled DOWN and the
  pair flipped BEARISH (W25 SHORT zone 0.8005–0.8025). D1 overbought (Stoch 82.9). **SNB Thu 06-18 = event
  risk.** Operator decision pending: cut ~BE / move stop to BE / hold. Note: long's TP1 (0.80085) ≈ the new
  short zone — the long's exit = where bias flips short. (Supersedes the 06-14 "no fill" note, which was wrong.)

## Live Order Limits
**None.** `/validate all` re-ran 2026-06-15 **03:14 UTC** (hourly, fresh pulls) → **0 order limits**
(all zones PENDING/below floor; confirms the 02:00 + 02:48 runs). Spots barely moved (Asian session).
Gates clear: BoJ/RBA Tue, FOMC Wed, BoE/SNB Thu all future-dated, today's opens clean (limits expire
21:00 UTC tonight). Per-zone read: **audusd SHORT ≈4.5** (spot 0.70773 INSIDE zone, H4 Stoch 85.2 OB,
**no E0**, ADX 28.9 fails E3) ← still closest · gbpusd SHORT (spot 1.34395 just BELOW zone, TTM squeeze
ON = not at-resistance, no SHORT E0) · nzdusd SHORT (spot 0.585 below zone, D1 Stoch 19.5 OVERSOLD = wrong
side, no SHORT E0) · eurgbp LONG (spot 0.86314 ~6p above zone, short-pin = wrong dir) · eurusd between
zones · usdcad/usdchf/xauusd price away from zones. JPY trio NO ZONES (MoF HARD_BLOCK all 3 + BoJ 06-16).
No V1/V1b invalidations (intraday, D1 not closed); weekend gaps all NOTE/NOISE (<0.5%) → no re-forecast.
Daily files: `forecasts/daily/*/2026-06-15.md` (all stamped with 03:14 re-validation). VIX 19.44 stale
(06-11, 4d) → veto suspended but no order limit depends on it.

## Week Status
- Week: 2026-W25 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **🔴 USDCHF open long 0.79477 — operator decision:** thesis flipped bearish + SNB Thu. Cut ~BE / move
  stop to BE 0.79477 / hold to TP1 0.80085 (≈ new short zone). Disciplined read = exit-or-BE (don't hold a
  long against your own flipped signal). Claude will not place/close orders — operator executes.
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
2026-06-15 03:14 UTC (**/validate ALL — 11 instruments, hourly**): fresh pulls all 8 USD/gold (paced).
Gates: CB (BoJ/RBA Tue, FOMC Wed, BoE/SNB Thu — all future, today clean), econ-cal (only FOMC 06-17
high-impact in window), JPY intervention WATCH (all 3 clear-of-band but BoJ+jawboning = HARD_BLOCK).
**0 order limits.** Closest still audusd SHORT (spot 0.70773 inside zone, no E0, ADX 28.9 fails E3, EC≈4.5).
No invalidations, no re-forecast (gaps NOTE/NOISE). USDCHF open long 0.79477 ≈flat, unchanged. All 11
daily files stamped. Telegram summary sent.
2026-06-15 (**/weekly xauusd re-forecast + corrections**): weekend-gap re-forecast (gap voided Sunday
W25 gold) → NEUTRAL/MED-LOW, SHORT 4360–4390 (7.0) + 4450–4485 (6.0), no counter-long; ledger rows redrawn
in place (no dup), yield_environment + belief log updated. Diagnosed Finnhub: key present, **plan lacks
econ-calendar endpoint** (premium). Corrected USDCHF: operator **IS** long 0.79477 (real W24 fill, ≈flat) —
thesis flipped bearish, SNB Thu; decision pending. Files: `forecasts/weekly/xauusd/2026-W25.md`.
2026-06-15 02:00 UTC (**/validate ALL — 11 instruments, W25**): refreshed all pulls. CB gate (BoJ/RBA
Tue, FOMC Wed, BoE/SNB Thu — today's limits expire 21:00 UTC tonight so no V3 block today). Econ-cal CSV
still stale → web fallback, no tier-1 within 2h of opens. **0 order limits.** xauusd VOIDED (+1.882%
weekend gap → re-forecast). gbpusd short: price gapped into 1.3440–1.3465 at reopen then fell out the
bottom (no at-zone E0, V1b intact). Risk-pair shorts H4-overbought from the gap-up but below floor (no E0,
D1 not extreme). JPY trio NO ZONES confirmed (intervention-watch HARD_BLOCK all 3). All 11 daily files
written. No FX orders → exposure ledger n/a.
2026-06-14 (**/weekly ALL — 11 instruments, W25**): refreshed all pulls (force, Fri close), CB calendar
(heavy week: BoJ/RBA 06-16, FOMC 06-17, BoE/SNB 06-18), W24 outcomes resolved, JPY intervention gate (all 3
in bands). Published **14 zones across 8 USD pairs**; JPY trio NO ZONES (BoJ+MoF). Key shifts: ECB hike
2.25% → eurusd NEUTRAL + eurgbp long-favored; DXY slope rolled down → usdchf flips BEARISH (8.5 short);
usdcad short ADX-vetoed (34.8); gold MEDIUM (Iran safe-haven vs rising real yields). Ledger + calibration +
yield_environment + _INDEX updated. Files: `forecasts/weekly/*/2026-W25.md`.
2026-06-12 07:30 UTC (`/validate all`): first order limit USDCHF BUY 0.79477 (W24); detail → `forecasts/daily/*/2026-06-12.md`.
2026-06-13 (3 upgrades): calibration layer + /weekly Step 2b retrospective + econ-cal/intervention gates → `decisions.md`.
