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
- **XAUUSD** [W25](forecasts/weekly/xauusd/2026-W25.md) — ⚠ **VOIDED — RE-FORECAST PENDING**. Weekend Globex gap **+1.882%** (4215→4316, Iran safe-haven) >1.00% → Sunday forecast voided. Run `/weekly xauusd` before validating. Both short zones held VOIDED. Spot 4316 (still <4435 POC).
- **EURUSD** [W25](forecasts/weekly/eurusd/2026-W25.md) — NEUTRAL/MEDIUM. LONG 1.1500–1.1520 (7.5) + SHORT 1.1618–1.1640 (7.0). Spot 1.1575. ECB hiked 2.25% (EUR+). FOMC Wed.
- **GBPUSD** [W25](forecasts/weekly/gbpusd/2026-W25.md) — NEUTRAL/MEDIUM. SHORT 1.3440–1.3465 (6.5) + COUNTER LONG 1.3304–1.3330 (7.0). Spot 1.3407. Squeeze ON. FOMC Wed + BoE Thu block.
- **EURGBP** [W25](forecasts/weekly/eurgbp/2026-W25.md) — NEUTRAL(long-tilt)/MEDIUM. LONG 0.8608–0.8625 (8.5, best) + SHORT 0.8660–0.8682 (6.0). Spot 0.8634. ECB favors long. BoE Thu block.
- **AUDUSD** [W25](forecasts/weekly/audusd/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.7065–0.7110 (6.5) + COUNTER LONG 0.6980–0.7000 (7.0). Spot 0.7045. ADX 28.9 (veto>30). RBA Tue + FOMC Wed block.
- **NZDUSD** [W25](forecasts/weekly/nzdusd/2026-W25.md) — NEUTRAL/MEDIUM. SHORT 0.5855–0.5890 (6.5) + COUNTER LONG 0.5750–0.5790 (6.5, best, D1 OS). Spot 0.5831. Antipodean gate vs AUD. FOMC Wed.
- **USDCAD** [W25](forecasts/weekly/usdcad/2026-W25.md) — BULLISH/MEDIUM. LONG 1.3830–1.3875 (6.0). Spot 1.3987, RSI 75 OB. SHORT **ADX-vetoed** (34.8>30). VIX abort if >20. FOMC Wed.
- **USDCHF** [W25](forecasts/weekly/usdchf/2026-W25.md) — BEARISH/MEDIUM. SHORT 0.8005–0.8025 (8.5, SNB-cap). Spot 0.7972. DXY slope flipped down. FOMC Wed + SNB Thu block. ⚠ reconcile W24 long.
- **USDJPY/EURJPY/GBPJPY** [usdjpy](forecasts/weekly/usdjpy/2026-W25.md)·[eurjpy](forecasts/weekly/eurjpy/2026-W25.md)·[gbpjpy](forecasts/weekly/gbpjpy/2026-W25.md) — **⛔ NO ZONES**: BoJ 06-16 + active MoF intervention regime (spots 160.2/185.5/214.8 in/above bands, Mimura 06-10). gbpjpy also BoE. Reassess W26 post-BoJ.
- FX stack: USDCAD LONG + USDCHF SHORT + EUR/GBP fades + AUD/NZD shorts → run `fx_exposure.py` netting at /validate.

## Open Position / Carryover
- **None — flat.** Operator confirmed no W24 orders were entered (2026-06-14). The USDCHF W24 long
  "RUNNING +0.8R" is **shadow-ledger only** (paper sim for calibration), NOT a real fill. The W25
  USDCHF SHORT 0.8005–0.8025 is therefore a clean fresh setup — nothing to reconcile.

## Live Order Limits
**None.** `/validate all` ran 2026-06-15 02:00 UTC → **0 order limits** (all zones PENDING/below floor).
Per-zone EC (floor in parens): audusd SHORT 5.0(6.0) ← closest · eurusd SHORT 4.5(6.5) · nzdusd SHORT
4.5(6.0) · usdchf SHORT 3.5(6.5) · gbpusd SHORT 3.0(6.0, gapped into zone then fell out) · eurgbp/
usdcad/counter-longs all ≤3.0. No E0 fired in zone direction on any pair; risk-pair shorts (H4-OB from
the weekend gap-up) are the watch list — may ripen later in session or Fri. JPY trio NO ZONES (MoF+BoJ).
Daily files: `forecasts/daily/*/2026-06-15.md`.

## Week Status
- Week: 2026-W25 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **🔴 RE-FORECAST GOLD:** `/weekly xauusd` — W25 forecast VOIDED by +1.882% weekend gap. Do before next
  /validate of gold. Spot 4316 < 4435 POC (thesis not yet broken, but Iran safe-haven bid is live).
- **/validate done for 06-15** (02:00 UTC, 0 limits). Re-run later in session or Mon evening if risk-pair
  shorts (audusd/eurusd/nzdusd) tag their zones with an at-zone E0. Wed = FOMC full block. Clean: Mon + Fri.
- **USDCHF:** flat (no W24 fill) — W25 SHORT 0.8005–0.8025 is a clean fresh setup.
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
- **Econ-calendar (#1/#2) still inactive:** no `FINNHUB_KEY` in `.env` → econ-cal CSV missing, web-search
  fallback used for data releases. Add key + `weekly_pull.py --force` to activate.
- **E0 RECLAIM (D027, PENDING-VALIDATION):** RSI-reclaim primary E0; pin/engulf fallback still counts until
  ledger confirms on gated subset. Pull **ENTRY TRIGGERS** block computes them.

## Last Session
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
