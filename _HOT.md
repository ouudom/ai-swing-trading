# _HOT — Session State
*Always current. Updated at end of every session.*
*RULE: hard cap **120 lines**. Current state + last session only. History lives in
`forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat. Prune every session.*

## System Status — v2 ACTIVE (2026-06-02)
Structured + AI-analysis entry-signal generation. Markdown-only (no DB). Unit = **Trading Zone**
(max 3/wk, ≤1 counter), Zone Confluence R1 + Entry Confluence R2 (max 10, floor 5, E0 confirm 3pt).

## Instruments — 5 ACTIVE
| Inst | Status | Character | Key docs |
|---|---|---|---|
| XAUUSD | active | momentum (pro-trend), real-yield macro | wiki/system/xauusd/ |
| EURUSD | active | mean-reversion fade, H4-centric; DXY-jump/US2Y/VIX gate (D021) | wiki/system/eurusd/ |
| GBPUSD | active | mean-reversion fade, D1-reversal+H1; same macro gate | wiki/system/gbpusd/ |
| EURGBP | active | cross, mean-reversion fade, macro 0.5 tilt, NO VIX-veto, EU event blocks | wiki/system/eurgbp/ |
| AUDUSD | active | mean-reversion fade, H4-centric; 🔑 DXY-jump DEAD, VIX LEVEL inverted, NO vetoes except ADX>30; RBA/AU/China events | wiki/system/audusd/ |

Onboarding history (P1–P5 majors, EG0–EG5 cross), signal scans, sizing decisions → `decisions.md`
(D021/D022/D023) + `wiki/research/{pair}/signal-results.md`. Sizing all pairs: USD, no quote-CCY
convert (operator). FX netting: `scripts/fx_exposure.py` gate at /validate (D022).
Known: backfill forward catch-up throws non-fatal "No data available" at weekend edge — data lands fine.

## Active Forecasts — 2026-W24
- **XAUUSD** [W24](forecasts/weekly/xauusd/2026-W24.md) — BEARISH/MEDIUM-HIGH, conviction HIGH.
  PRIMARY SHORT $4367–$4390 (9.5), SECONDARY SHORT $4450–$4485 (9.5), no counter. Spot ~$4162,
  ADX 48 — zones ~$200 OTM, re-anchor likely Sunday. Invalidate: D1 close > zone top.
- **EURUSD** [W24](forecasts/weekly/eurusd/2026-W24.md) — SHORT 1.1618–1.1640 (7.5) + 1.1574–1.1593 (6.5). Spot 1.1549.
- **GBPUSD** [W24](forecasts/weekly/gbpusd/2026-W24.md) — SHORT 1.3400–1.3447 (8.0) + 1.3370–1.3390 (6.5). Spot 1.3384.
- **EURGBP** [W24](forecasts/weekly/eurgbp/2026-W24.md) — NEUTRAL/range. LONG 0.8608–0.8624 (8.0) +
  SHORT 0.8664–0.8682 (7.5). Spot 0.8630. Fade both edges; no VIX-veto; netting ledger required.
- FX strategy: sell bounce into resistance (USD strength); both majors SHORT → if both fill = 2× long
  USD → netting gate keeps best EC, skips other (D022).

## Open Position
None

## Live Order Limits — NONE (2026-06-10 08:06 UTC, CPI day = V3 HARD BLOCK)
XAUUSD limits expired 06-09 21:00 UTC, NOT re-placed (CPI block + spot ~$200 below zone). 0 FX orders.

## Week Status
- Week: 2026-W24 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **/validate daily 07:30 UTC** — no limits live; re-validate each morning.
- **CPI TODAY 06-10 12:30 UTC = V3 HARD BLOCK** (US-event instruments). PPI Thu, UMich Fri caution.
  Re-validate post-CPI; watch cool-print squeeze (oversold all TFs) — sell bounce, don't chase.
- **T5 drift watch:** DFII10 2.21 vs baseline 2.11 = +0.10 (WITH bias); >0.15 total forces re-forecast.
- **GBPUSD watch:** closest USD fade — fresh rally into 1.3400 + H1 OB + bearish E0 → ~7.5 ORDER LIMIT.
- **EURGBP watch:** primary LONG 0.8608–0.8624 — needs D1 oversold + in-zone + bullish E0.
- **FX netting gate (D022):** both majors ORDER LIMIT same day → keep higher EC, SKIP other.
- **EXPANSION (D024, 2026-06-10):** all 7, sequential. ✅ W0 advisory ledger (fx_exposure rewritten,
  selftest 12/12). ✅ **AUDUSD #1 DONE** (data 2010→/2020→, scan GO, confluence ACTIVE, wired, smoke-
  tested — ready for first `/weekly audusd`). ⏳ NEXT: **NZDUSD #2**, then USDCAD→USDCHF→USDJPY→
  EURJPY→GBPJPY. Rulings: USD sizing no convert (JPY pairs static TICK≈650); netting ADVISORY only.

## Last Session
2026-06-10 (expansion build): compacted _HOT (120-line rule → CLAUDE.md). **W0**: fx_exposure.py →
advisory per-currency ledger, 10 FX instruments (D024; selftest PASS); constitution + validate.md +
currency_exposure.md amended. **AUDUSD onboarded end-to-end**: config (carry off — no daily RBA
series; weekly_pull rate_diff branch now tolerates RATE_FOREIGN=None + USD-base label flip ready),
backfill D1 4288/H4 9786/H1 39209 bars, scan GO (research + raw saved), profile + confluence ACTIVE,
weekly/validate/constitution wired, smoke-tested (pull W24 ✅, COT 6A ✅, check_v1b ✅). CFTC names
verified for all 5 remaining currencies (+ direct EURJPY XRATE contract exists).
2026-06-10 (08:06 UTC, London scheduled `/validate all` — 4 instruments; supersedes 02:14 run).
**CPI day = V3 HARD BLOCK (US instruments). ALL ZONES ALL 4 = ❌ NO TRADE; all held PENDING; no orders.**
- XAUUSD $4162.04 (~$200 below zone); D1 ADX 48, RSI 24.6 deeply oversold; H4 ATR $43.63. EC 6.0, V3
  overrides. No re-forecast (T3 WITH bias; T5 +0.10<0.15; CPI <12h blocks precondition 3).
- EURUSD 1.15490 below short zones; RSI D1 32.7, ADX 39.6 trending → EC 2.0. NO TRADE + V3.
- GBPUSD 1.33836 inside secondary zone; H1 OB bounce faded (RSI 46.6) → EC 2.0. NO TRADE + V3.
- EURGBP 0.86296 ~6 pips above LONG support; H4 RSI 24 OS but D1 41.3 not extreme, no E0 → EC 3.0.
  NO TRADE (US CPI = caution only for cross).
- Hard blocks else pass all 4 (V1/V1b intact; VIX 18.92 stale/falling; DXY −0.106; DGS2 flat).
  Wrote/superseded all 4 daily files. Re-validate post-CPI / tomorrow AM.
