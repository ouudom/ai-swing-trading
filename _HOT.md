# _HOT — Session State
*Always current. Updated at end of every session.*
*RULE: hard cap **120 lines**. Current state + last session only. History lives in
`forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat. Prune every session.*

## System Status — v2 ACTIVE (2026-06-02)
Structured + AI-analysis entry-signal generation. Markdown-only (no DB). Unit = **Trading Zone**
(max 3/wk, ≤1 counter), Zone Confluence R1 + Entry Confluence R2 (max 10, floor 5, E0 confirm 3pt).

## Instruments — 10 ACTIVE (D024 expansion COMPLETE)
| Inst | Status | Character | Key docs |
|---|---|---|---|
| XAUUSD | active | momentum (pro-trend), real-yield macro | wiki/system/xauusd/ |
| EURUSD | active | mean-reversion fade, H4-centric; DXY-jump/US2Y/VIX gate (D021) | wiki/system/eurusd/ |
| GBPUSD | active | mean-reversion fade, D1-reversal+H1; same macro gate | wiki/system/gbpusd/ |
| EURGBP | active | cross, mean-reversion fade, macro 0.5 tilt, NO VIX-veto, EU event blocks | wiki/system/eurgbp/ |
| AUDUSD | active | mean-reversion fade, H4-centric; 🔑 DXY-jump DEAD, VIX LEVEL inverted, NO vetoes except ADX>30; RBA/AU/China events | wiki/system/audusd/ |
| NZDUSD | active | mean-reversion fade, macro-light squeeze-led; 🔑 US2Y+DXY DEAD, VIX level weak inverted; weakest edges (≈½ AUD) → fewer zones; RBNZ/NZ events; antipodean advisory | wiki/system/nzdusd/ |
| USDCAD | active | **USD-base** mean-reversion fade; 🔑 polarity flips (US2Y rising=bullish, VIX>20→SHORT bias t≈3.9, COT 6C inverted); 🛢 oil tilt weak; H1 long-side rich; BoC/CAD events (12:30 overlap!) | wiki/system/usdcad/ |
| USDCHF | active | **USD-base** mean-reversion fade, H1-centric; 🔑 DXY 20d slope = live macro (t=2.3, only pair beyond EUR/GBP), VIX WASHOUT (no gate/score), COT 6S inverted; H1 short-fade machine (t 4.5–5.5); ⚠ SNB regime — shorts near 0.78–0.80 cap MEDIUM, SNB days hard block | wiki/system/usdchf/ |
| USDJPY | active | **USD-base, FIRST JPY pair** (pip 0.01, 3dp, TICK 650 static); 🔑 **ASYMMETRIC carry-drift, NOT fade**: LONG = squeeze/calm/dip/NY-drift (t 3.3–4.7), SHORT = D1/H4 extremes only, **H1-only shorts PROHIBITED** (anti −3.3); DXY 20d slope live (t=2.2), VIX washout, US2Y dead, COT 6J inverted; ⚠ MoF regime — longs ≥158 cap MEDIUM, BoJ/MoF days hard block (spot 160.5 IN band) | wiki/system/usdjpy/ |
| EURJPY | active | **FIRST cross-JPY** (pip 0.01, 3dp, TICK 650 static); 🔑 **symmetric mean-reversion + calm-drift** on long-drift floor (D1 LNG 55.6%): buy washouts (Stoch<20 t=3.1), fade extension (Keltner-high t=3.4, H1 W%R t=4.2 — H1 fade WORKS, unlike usdjpy), NEVER chase (C26 anti −4.2); **macro NONE** (first 100% price-driven — ECB anti, VIX dead, no USD leg); sessions two-sided: London fade-short t=2.8 / NY drift-long t=3.0; COT XRATE direct but THIN (OI 21k); ⚠ MoF slams hit crosses — BoJ/MoF + ECB hard block, record-high longs cap MEDIUM (spot 185.2) | wiki/system/eurjpy/ |
| GBPJPY | active | **cross-JPY #2, LAST pair** (pip 0.01, 3dp, TICK 650 static, V1b 0.05 — highest ATR: D1 med 151p); 🔑 **extension-fade SHORT-dominant** on strongest long-drift floor (D1 LNG 56.7%): fade spikes (Keltner-high t=4.64/4.01, BB-upper 63%win +0.42%), buy washouts (RSI<35 t=2.4, 73%win); **NO calm engine** (only JPY pair without), **macro NONE** (SONIA ns, VIX dead), NEVER chase (C26 anti −5.0); sessions NY long-only (overlap t=4.2; SHORT 13–15 UTC = ANTI −3.84); **COT DISABLED** (no CFTC cross contract); ⚠ MoF slams largest of crosses — BoJ/MoF + BoE hard block, record-high longs cap MEDIUM (spot 214.6) | wiki/system/gbpjpy/ |

Onboarding history (P1–P5 majors, EG0–EG5 cross), signal scans, sizing decisions → `decisions.md`
(D021/D022/D023) + `wiki/research/{pair}/signal-results.md`. Sizing all pairs: USD, no quote-CCY
convert (operator). FX netting: `scripts/fx_exposure.py` gate at /validate (D022). Known: backfill
catch-up throws non-fatal "No data available" at weekend edge — data lands fine.

## Active Forecasts — 2026-W24
- **XAUUSD** [W24](forecasts/weekly/xauusd/2026-W24.md) — BEARISH/MEDIUM-HIGH, conviction HIGH.
  PRIMARY SHORT $4367–$4390 (9.5), SECONDARY SHORT $4450–$4485 (9.5), no counter. Spot ~$4080
  (fell further), ADX 42 — zones now ~$309–404 OTM, unreachable, re-anchor at next /weekly.
  Invalidate: D1 close > zone top (not breached).
- **EURUSD** [W24](forecasts/weekly/eurusd/2026-W24.md) — SHORT 1.1618–1.1640 (7.5) + 1.1574–1.1593 (6.5). Spot 1.1549.
- **GBPUSD** [W24](forecasts/weekly/gbpusd/2026-W24.md) — SHORT 1.3400–1.3447 (8.0) + 1.3370–1.3390 (6.5). Spot 1.3384.
- **EURGBP** [W24](forecasts/weekly/eurgbp/2026-W24.md) — NEUTRAL/range. LONG 0.8608–0.8624 (8.0) +
  SHORT 0.8664–0.8682 (7.5). Spot 0.8630. Fade both edges; no VIX-veto; netting ledger required.
- **AUDUSD** [W24](forecasts/weekly/audusd/2026-W24.md) — BEARISH/MEDIUM. PRIMARY SHORT 0.7065–0.7110 (7.0)
  + COUNTER LONG 0.6940–0.6996 (7.0, MEDIUM cap). Spot 0.7010. ADX 28.4 trending → floor 6.0.
- **NZDUSD** [W24](forecasts/weekly/nzdusd/2026-W24.md) — NEUTRAL range. PRIMARY SHORT 0.5855–0.5890 (6.5)
  + COUNTER LONG 0.5750–0.5790 (7.5, MEDIUM cap). Spot 0.5799. Antipodean gate vs AUDUSD.
- **USDCAD** [W24](forecasts/weekly/usdcad/2026-W24.md) — BULLISH/MEDIUM. PRIMARY LONG 1.3885–1.3905 (7.0).
  SHORT side VETOED (ADX 32.3>30 up). Spot 1.3938. Abort long if VIX closes >20 (fade-USD flip).
- **USDCHF** [W24](forecasts/weekly/usdchf/2026-W24.md) — BULLISH/MEDIUM-HIGH. PRIMARY LONG 0.7945–0.7960
  (7.5) + COUNTER SHORT 0.8005–0.8030 (5.5). Spot 0.7985. ADX 23.5 → validate floor 6.5. SNB 06-18 W25.
- **USDJPY / EURJPY / GBPJPY** [W24](forecasts/weekly/usdjpy/2026-W24.md) — **⛔ NO ZONES: active MoF
  intervention regime** (Apr-30 intervention ~160.7, Mimura jawboning June; spot 160.5 in trigger zone;
  crosses slam in sympathy). Reassess after BoJ 06-15/16. [eurjpy](forecasts/weekly/eurjpy/2026-W24.md) ·
  [gbpjpy](forecasts/weekly/gbpjpy/2026-W24.md)
- FX strategy: sell bounce into resistance (USD strength); USD-stack note: usdcad+usdchf LONG +
  audusd+nzdusd+majors SHORT all = long USD → netting gate keeps best EC (D022, advisory).

## Open Position
None

## Live Order Limits — NONE (2026-06-11 06:11 UTC, `/validate all` — ECB + PPI day = V3 HARD BLOCK)
All 10 instruments validated → **❌ NO TRADE across the board (V3)**. 0 order limits placed. All zones
held PENDING (structure intact, NONE invalidated). No re-forecast triggered (T1–T5 sub-threshold).
> [!warning] **ECB rate decision is TODAY 06-11 12:15 UTC (presser 12:45)** — confirmed 2026 schedule
> (Mar 19 / Apr 30 / **Jun 11** / Jul 23…). This was MISSED in the W24 weekly (only PPI was flagged).
> Hard-blocks EUR pairs (eurusd, eurgbp, eurjpy). **Re-validate EUR pairs after 12:45 UTC** — ECB
> outcome (possible rate-cut-cycle reversal on Iran oil/stagflation) can shift EUR bias for rest of W24.

## Week Status
- Week: 2026-W24 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **/validate daily 07:30 UTC** — no limits live; re-validate each morning.
- **TODAY 06-11: ECB 12:15 UTC (EUR pairs HARD) + PPI 12:30 UTC (US-leg HARD)** — both within 2h of
  NY open → all 10 pairs NO TRADE today. **Re-validate EUR pairs (eurusd/eurgbp) after 12:45 presser.**
  AU jobs Fri 01:30 UTC (audusd hard, nzdusd caution). UMich Fri 14:00 caution. W25: BoJ 06-15/16,
  FOMC 06-16/17, SNB+BoE 06-18.
- **✅ ECB-miss fix SHIPPED (2026-06-11):** static CB calendar `scripts/config/cb_calendar_2026.json`
  + `scripts/check_cb_calendar.py` now MANDATORY at /weekly (10d) + /validate (2d). ⚠ Verify RBNZ
  H2-2026 + SNB Sep/Dec dates on official sites (marked estimated/TBC in JSON).
- **T5 drift watch:** DFII10 2.21 vs baseline 2.11 = +0.10 (WITH bias); >0.15 total forces re-forecast.
- **GBPUSD watch:** closest USD fade — fresh rally into 1.3400 + H1 OB + bearish E0 → ~7.5 ORDER LIMIT.
- **EURGBP watch:** primary LONG 0.8608–0.8624 — needs D1 oversold + in-zone + bullish E0.
- **FX netting gate (D022):** both majors ORDER LIMIT same day → keep higher EC, SKIP other.
- **EXPANSION (D024) ✅ COMPLETE:** all 7 pairs onboarded + first /weekly published 2026-06-11
  (all 10 instruments forecast for W24). Rulings: USD sizing no convert; netting ADVISORY only.
- **MoF watch:** JPY trio blocked all W24. Post-BoJ (06-15/16) washout = A+ setups for W25
  (eurjpy squeeze long 183–184; gbpjpy washout 211–213; usdjpy dip 158–159 if calm holds).
- **Shadow ledger LIVE:** /weekly MUST register zones (`zone_ledger.py add`) + resolve prior week
  (`zone_outcomes.py --week`). nzdusd 1h/4h still carry the 04-29 bad tick — auto-clamps at next fetch.

## Last Session
2026-06-11 PM (**shadow ledger + bad-tick guard shipped**): (1) `zone_ledger.py` (registry, MANDATORY
at /weekly) + `zone_outcomes.py` (OHLC replay → would-be R + confluence calibration). W24 seeded 15
zones; first result: gbpusd SECONDARY would-be **−1R** (CPI spike; V3 block saved it), 14 open.
(2) `ohlc_store.upsert()` bad-tick guard (wick-clamp/bar-drop vs rolling-median, `_quarantine.csv` log);
found nzdusd 1.71632 tick still live in 1h/4h. Docs: CLAUDE/AGENTS/_INDEX/weekly.md.
2026-06-11 PM (**deep review + 12 fixes, operator-approved**): (1) weekly_pull risk_unit was
`min(H4, 0.5×D1)` — CONTRADICTED constitution (always ≤ H4 → lots ~9% oversized); now constitution
formula + 0.01-lot floor. (2) validate.md lots `int(2000//(SL×TICK))` gave 0 lots gold → floored
0.01-step formula. (3) ISO-year filename bug fixed (Dec/Jan boundary) + ALL time math now UTC,
reports add local tz. (4) 15M fetch now gap-aware (sizes request from last bar; >5000 bars → hard
fail with backfill instruction). (5) All indicators on CLOSED bars only. (6) CB calendar gate (see
Pending). (7) ohlc_store `vol>0` weekend-filter bypass deleted. (8) policy-diff prev now date-joined.
(9) VP cleanly disabled for USD-base. (10) CLAUDE.md/AGENTS.md/constitution de-staled (10
instruments). (11) requirements.txt trimmed to 5 real deps; pyrun --setup reads it. (12) removed
.venv-linux, legacy `.venv/bin/python` docstrings. All snapshots rebuilt + verified (xauusd SL
53.66 avg-branch ✓, usdchf VP-disabled ✓, gbpjpy 7.5 lots ✓, fx_exposure selftest PASS).
2026-06-11 06:11 UTC (**`/validate all` — 10 instruments, operator request**): all pulls refreshed.
**Result: ❌ NO TRADE on every zone — V3 hard block (ECB 12:15 + PPI 12:30, both <2h of NY open).**
0 limits placed; all zones held PENDING (structure intact, none invalidated); no re-forecast (T1–T5
sub-threshold; DFII10 drift +0.09<0.15, US2Y slope +0.13). 🔎 **Discovered ECB decision is TODAY** —
missed in W24 weekly; flagged for re-validate post-presser + /weekly event-scan fix. Gold $4080 (zones
$309–404 OTM). Files: `forecasts/daily/{inst}/2026-06-11.md` (all 10). JPY trio still NO ZONES (MoF).
2026-06-11 PM (**first /weekly for all 7 new pairs — W24 mid-week**, operator request): pulls
refreshed; zones published audusd (SHORT 0.7065–0.7110 7.0 + counter LONG 0.6940–0.6996 7.0),
nzdusd (SHORT 0.5855–0.5890 6.5 + counter LONG 0.5750–0.5790 7.5), usdcad (LONG 1.3885–1.3905
7.0; short VETOED ADX 32.3), usdchf (LONG 0.7945–0.7960 7.5 + counter SHORT 0.8005–0.8030 5.5).
**JPY trio = NO ZONES — active MoF intervention regime** (web-confirmed: Apr-30 intervention
~160.7, Katayama + Mimura jawboning into June; usdjpy spot 160.5 in trigger zone; crosses hard-
blocked in sympathy). 🔧 **nzdusd bad tick repaired**: D1 2026-04-29 high 1.71632 → 0.58853
(provider error; ADX was falsely 79.6 → true 18.5 RANGING); pull recomputed. yield_environment
+FX-pairs section updated. All zones PENDING — /validate gates orders.
2026-06-10/11 (expansion D024 #1–#7 COMPLETE → `decisions.md` D024) · 2026-06-10 (`/validate all`:
CPI V3 block, all NO TRADE → `forecasts/daily/*/2026-06-10.md`).
