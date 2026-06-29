---
type: decision
updated: 2026-06-10
confidence: high
tags: [decisions, system-design]
related: [constitution]
---

# System Decisions — Belief Log

## How to Use
Record key system choices here with reasoning.
When a decision changes, add a new belief_log entry — never delete old ones.
Entries are ordered newest-first (descending D-number). Each carries a `Status:` line —
**ACTIVE** (current rule), **SUPERSEDED by Dxxx** (replaced), or **CARRIED** (folded into a
later decision but still in force).

> **Naming lineage:** entries before D019 use the pre-v2 gate labels (weekly `S1–S7`,
> daily `G1–G6`). v2 replaced these with **Zone Confluence (Z1–Z7)** + **Entry Confluence
> (E0–E5)** — see `confluence_criteria.md`. Old labels are kept in dated entries as
> historical record only; they are not active rule names.
>
> **Gap:** D016 (EURUSD instrument) was removed when the system descoped to gold-only (see D019).

---

## D033 — DB durability guard + weekly-pull immutability guard
**Status:** ACTIVE.

On 2026-06-26 `data/database/index.db` (the canonical source of truth — CSVs were migrated in and
deleted) was found **badly corrupt** (Tree-10/`ohlc` malformed pages, not the cosmetic news-only
glitch `_HOT` had assumed). `trade_outcome.py` crashed mid-run, so system P&L had been silently
blind for an unknown number of sessions, and the `calibration.md` on disk was a stale 06-21 snapshot
falsely reading "WORKING +0.5R" while the live picture was **DEAD −4.5R / 19% / n=16**. Recovered via
`sqlite3 .recover` (integrity ok); only `news` was lost (re-pulled from RSS).

Three durability changes:
1. **`scripts/db_guard.py`** — `checkpoint`→`check` (PRAGMA quick_check)→`backup` (consistent
   `VACUUM INTO` gzip, last 7). Non-zero exit on a corrupt image. Wired as **MANDATORY Step 0b** in
   /weekly + /validate so a command halts before writing into a bad store. Supersedes the SQL-dump
   `backup_db.py` (whose newest backup was 10 days stale at the incident) for routine guarding;
   `backup_db.py` was removed 2026-06-28 (db_guard is the sole backup tool).
2. **`db.py` connection hardening** — `busy_timeout=30000` + `synchronous=NORMAL` on top of WAL, so
   concurrent writers (hourly /validate + the frontend reader) wait on a lock instead of racing —
   the likely corruption cause.
3. **`weekly_pull.py` immutability guard** — refuses to overwrite a `weekly_pull_*.txt` first written
   on an earlier calendar day (`--rewrite-immutable` overrides). Closes the File-Rules violation where
   a Sunday `--force` re-pull clobbered the 2026-W25 JPY snapshots frozen since the prior Monday.
4. **`db_guard.py sweep` (added 2026-06-26 cleanup)** — the FUSE-mounted scheduled-task sandbox renames
   the old `index.db` inode to `.fuse_hidden*` (not unlink) on every swap while a reader holds it open;
   these never self-clean and had grown to **7,871 files / 289MB** under `data/database/`. `sweep`
   unlinks them (safe even if held — POSIX frees the inode on last close) and now runs at the tail of
   `db_guard all`, so the junk self-clears each preflight instead of silently bloating the store dir.

**Why:** the DB is the source of truth with no CSV fallback; a corrupt image is silent data loss and a
silently-stale calibration mis-reads the edge. Lesson reinforced: never cache a derived verdict
(calibration WORKING/DEAD) — recompute from the live store each session.

## D032 — Asymmetric 4h anchor lock on confirmed ORDER_LIMITs
**Status:** ACTIVE.
**Decision:** An **E0-confirmed** `ORDER_LIMIT` (anchor = confirmation candle CLOSE, passed via
`--e0`) **freezes its anchor (limit + EC) for 4h** in the `zone_ledger`, so the hourly `/validate`
re-run stops whipsawing the resting limit. A **no-E0** `ORDER_LIMIT` (anchor = 50% zone midpoint)
writes the verdict but is **never locked** — it keeps re-deriving every hour, since a midpoint
anchor is a fallback estimate, not a committed entry, and there is no confirmation signal to commit
to. The lock is **asymmetric**: a strictly higher EC *E0* ORDER_LIMIT re-anchors and resets the
clock (**UPGRADE**); an equal/lower EC E0 ORDER_LIMIT, a no-E0 (midpoint) ORDER_LIMIT, or a *soft*
`NO_TRADE` (E0 lapse / EC dipped below floor with no hard gate), is ignored and the locked limit is
kept (**HOLD**); `INVALIDATED` or `NO_TRADE --hard-block` (V1/V1b/V3/intervention/macro-flip) always
cancels and clears the lock (**CANCEL**). Lock window is clamped to the 21:00 UTC daily expiry.
Implemented in `scripts/zone_ledger.py validate` (cols `anchor_set_utc`, `anchor_locked_until`;
flags `--e0`, `--hard-block`, `--lock-hours`, `--now`).
**Rationale:** The entry signal re-derives every hour off the latest closed 1H E0; a single borderline
candle flipped the anchor between confirmation-close and 50%-midpoint, moving the limit ~25+ pts
run-to-run (e.g. xauusd 06-22 12:18→13:12→14:15: limit 4223.52→4258.08→4217.59 on E0 appearing /
lapsing / reappearing). Locking commits to a confirmed entry for one ATR-scale window instead of
chasing 1H noise, while the hard gates still recompute hourly so V1b / intervention can cancel
mid-window. Cheaper than the D030 offset retune (still OPEN, n=1) and targets the same churn symptom.
**Limit:** holds an order on a *stale* trigger if the move fully reverses inside 4h without tripping a
hard gate — accepted, since EC-below-floor with the zone still structurally valid is treated as noise
by design. Net effect on realized R is unmeasured (n too low); revisit once `trade_outcome` has enough
locked-vs-churned fills to compare. Procedure wiring lives in `.claude/commands/validate.md`
"Save + Update" (operator must paste — file is session-protected).
**belief_log:**
- 2026-06-23 — added after the 06-22 hourly churn surfaced the flip-flop; user-requested.
- 2026-06-26 — **E0-gated the lock** (`--e0` flag): only a confirmation-close anchor locks; a no-E0
  50%-midpoint ORDER_LIMIT now re-derives hourly instead of committing. Reason: a midpoint anchor is
  a fallback estimate with no entry signal — locking it pinned a resting order on guessed price for
  4h. User-requested.

---

## D029 — Re-forecast T6: nominal-yield + DXY-slope USD-regime drift trigger
**Status:** ACTIVE.
**Decision:** Add **T6** to the mid-week re-forecast trigger tree + a parallel FX "USD Regime Drift"
daily-drift table. T6 fires on `|Δ DGS2| > 0.15%` OR a DXY `slope20` sign-flip vs published bias.
CONFIRMATION-class (not IMMEDIATE) — must persist one /validate. Counter zones opposed by a confirmed
flip are voided immediately, without waiting for the recheck.
**Rationale:** W25 regime flip (hawkish FOMC/Warsh) repriced DGS2 4.05→4.20 and DXY slope20 +1.65, but
moved neither DFII10 (T1/T5 series) nor the DXY 1-day *jump* (T2) past threshold → **no trigger fired**,
and stale USD-short / counter-long zones rode into the flip. The trigger tree was blind to nominal +
slope repricing. Replay confirmed every counter-USD long lost or was saved only by a hard block.
**Limit:** still ONE re-forecast/week (D-edge-preservation unchanged); T6 is CONFIRMATION because
nominal/slope is noisier than real-yield. Does not relax the FOMC-day event-proximity precondition —
you still never re-forecast *into* the event; T6 catches the flip the morning after.
**belief_log:**
- date: 2026-06-19
  belief: "Re-forecast triggers must cover nominal DGS2 + DXY slope, not just real-yield + DXY jump"
  trigger: "W25 retro — hawkish repricing slipped every trigger; stale USD-short zones carried into flip"

---

## D031 — Retire the hand-logged `trade` table; system is replay-evaluated
**Status:** ACTIVE.
**Decision:** Remove `scripts/trade_log.py`, the `/log` skill (`.claude/commands/log.md`), and the
canonical `trade` table. Replace with **`trade_outcome.py`** — an entry-mechanics replay (E0 + outward
offset limit + EC score via new `entry_confluence.py`/`config/ec_spec.py`) over the zone ledger,
producing SYSTEM P&L (would-be R with realistic fills) + a **gate-accuracy audit** (every hard gate
V1/V1b/V3/VETO/INTERVENTION/EC filled-anyway → counterfactual R → was the block CORRECT_SAVED or
COSTLY_REFUSED). `calibration.py` R2 + Gate-Accuracy sections now read `trade_outcome`; api
(`/positions`, `/edge`, `/chart`) + frontend repointed (`midpoint_vs_entry` replaces `shadow_vs_real`).
**Rationale:** the real book was **n≈2** (1 LOSS, 1 EXPIRED) and would never reach the n to calibrate
Entry Confluence (R2) — the calibration R2 section sat permanently on "awaiting live trades." The
system doesn't execute real money; the question worth answering is "is the SYSTEM profitable," which a
replay answers with many samples. Also fixes the unverified "INVALIDATED = capital saved" assumption in
`zone_outcome` — gates are now measured, not assumed (W25 cross-check: V1b on nzdusd COUNTER → −1R →
KEEPS EDGE; V1/V3/EC all net-negative so far).
**Fidelity caveat:** `ec_spec.py` approximates each pair's `confluence_criteria.md` R2 prose to the
nearest deterministic predicate (generic fade thresholds); review per-pair before trusting R2.
**belief_log:**
- date: 2026-06-19
  belief: "Measure system profitability + gate accuracy by replay; stop pretending a 2-row real book is the truth"
  trigger: "User: 'remove real trade log table and command … I want to see the data of our system, if it is profitable'"

---

## D030 (OPEN) — Offset fill-rate vs entry-quality: deferred, n=1
**Status:** OPEN — no change applied. Tracking only.
**Observation:** W25 audusd PRIMARY SHORT (EC 6.5) replay = +2.5R, but the live offset limit 0.70902
never triggered — week high 0.70769, **missed by 13 pips**. Offset = max(SL/3, (10−EC)×0.2×SL) = 0.7×SL
outward; the wide outward placement put the limit past the reversal high.
**Why no change:** n=1. Tightening the offset constant changes fill-rate AND R-denominator on **every**
trade — a calibration decision, not a one-data-point bug. A single near-miss is not evidence to retune a
live edge parameter (cf. constitution "lag is acceptable / no discretionary reset").
**Trigger to revisit:** when `zone_outcomes` accumulates enough "replay-filled-at-zone but live-offset-
missed" near-misses (target n≥8) to show the offset is systematically over-wide. Until then: no edit.
**Update 2026-06-19 (D031):** the near-miss is now INSTRUMENTED — `trade_outcome.py` marks
`LIMIT_MISSED` when the offset limit is never reached, and `calibration.md` reports the count + the
midpoint-vs-entry R gap. W24–W25 already show 4 misses (incl. a usdchf LONG at EC 9.0). Watch the count
toward n≥8 before retuning the offset constant.
**belief_log:**
- date: 2026-06-19
  belief: "Do not retune offset on one near-miss; instrument the near-miss gap and let it accumulate"
  trigger: "W25 audusd short missed fill by 13 pips on a 0.7×SL outward offset"

---

## D028 — Pre-Event Flatten replaces the binary carry block (allow entries, force flat pre-event)
**Status:** ACTIVE (2026-06-16). Implemented in `constitution.md` (No-Trade Rules → "Pre-Event
Flatten") + `.claude/commands/validate.md` (V3 split + flatten-time expiry + Telegram flag).
**Decision:** A hard event (CB decision / tier-1 release) falling *later* in a position's hold horizon
is **no longer auto-NO-TRADE.** The entry is allowed (all other gates still apply); the order limit
expires at `flatten_time = event_time − FLATTEN_BUFFER` instead of 21:00 UTC, and any fill is closed at
market by `flatten_time`. `FLATTEN_BUFFER = 60min` (operator-tunable). What stays a true hard block: the
event WINDOW itself (release ±30min, or any hard event within 2h of the 08:00 London / 13:00 NY open),
the pair's OWN central bank deciding that day, the JPY-trio NO ZONES standing rule, and active MoF
intervention.
**Rationale:** The carry block conflated two different risks. (1) *Entry-in-window* risk — chaotic
fills/whipsaw in the ±30min around a release — is real and stays blocked. (2) *Carry/gap* risk —
holding through the event and eating the gap *through* the SL (intervention slams 300–500 pips → a
planned −1R becomes −3 to −5R) — was being managed by refusing the entry, which also throws away the
intraday mean-reversion edge on dense CB weeks (W25 had 4 decisions in 3 days → effectively every
instrument dead). Flattening before the event removes the gap exposure directly while preserving the
entry, so the edge is captured without the tail. Rejected alternatives: wider outward offset (wrong
lever — offset changes entry price/fill-prob only; SL distance and the post-event gap are unchanged, so
it does nothing for carry risk) and full-size carry-through (keeps the multi-R tail).
**Caveats:** caps trades that need multi-day runners to reach the 2.5R/3R TPs — a position force-closed
at `flatten_time` books whatever R it has, often < TP1. Operator may instead manage the close manually.
Pure forward-carry relaxation; does not touch any in-window or standing block. Re-evaluate buffer if
fills cluster too close to events.
**belief_log:**
- date: 2026-06-16
  belief: "Carry risk = flatten before the event, not refuse the entry; window/own-CB/JPY blocks stay"
  trigger: "W25 4-decisions-in-3-days dead week — carry block was throwing away the intraday edge"

## D027 — E0 entry-confirmation upgraded to oscillator RECLAIM (pin/engulf demoted to fallback)
**Status:** ACTIVE-PENDING-VALIDATION (2026-06-14). Implemented in pipeline + all rubrics; awaiting
live-ledger confirmation on the confluence-gated subset before "settled".
**Decision:** The E0 trigger is no longer "pin/engulf/15M-CHoCH" by default. Per-pair PRIMARY E0 is
now set by the e0-variants backtest: **RSI-reclaim** (RSI(14) crossing back through 35/65 toward the
fade) for most FX (eurusd, audusd, nzdusd, usdchf, eurjpy, gbpjpy, + usdjpy SHORT leg);
**pin/engulf** retained as primary only on gbpusd & eurgbp (the two pairs it wins); **band-reclaim**
(close re-entering Keltner) primary on usdcad. xauusd + usdjpy-LONG keep CONTINUATION E0 (momentum/
drift — the fade reclaim does not apply). Pin/engulf is kept as a **fallback everywhere** so E0 is
never weaker than before. New pull block **ENTRY TRIGGERS (E0, latest closed 1H)** computes all
triggers both directions (verifiable, not eyeballed) via `weekly_pull.entry_triggers_block`.
**Rationale:** Tier-2 entry-sim (`backtest_entry_sim.py`) showed E0's payoff is fill-price/R via the
outward offset, not win-rate (Tier-1 found no directional edge). The trigger bake-off
(`backtest_e0_variants.py`, 1H, 2015+) then showed the current pin/engulf is one of the *weakest*
gates — barely above a raw limit — while RSI-reclaim delivers ~3× the per-trade R (pooled avgR +0.104
vs +0.038, PF 1.15 vs 1.05) and wins 7/11 pairs. A reclaim confirms momentum actually turned, which
fits the mean-reversion thesis better than a single candle shape.
**Caveats / why PENDING:** in-sample forward-return sim on the *unfiltered* extreme universe, not the
live zone ledger (n=1). 15M tested — the edge collapses/flips (noisier, shorter 2024+ sample) → E0
stays on **1H close**. Validate on the gated subset + ledger before treating as final; pin/engulf
fallback bounds the downside. Reports: `wiki/research/general/e0-variants-backtest.md` (+ entry-sim,
entry-confirm). _(D025 = TA-engine compute round; D026 = indicator/E0 backtest research — logged in
research dir + _HOT, not as formal decisions.)_
**belief_log:**
- date: 2026-06-14
  belief: "E0 PRIMARY = oscillator reclaim (RSI 35/65), pin/engulf fallback; per-pair per backtest"
  trigger: "e0-variants bake-off — reclaim ~3× pin's per-trade R, wins 7/11 pairs (in-sample, 1H)"

## D024 — 7-pair expansion; netting demoted to ADVISORY; USD sizing everywhere (no quote-CCY convert)
**Status:** ACTIVE (2026-06-10). **COMPLETE 2026-06-11 — all 7 pairs onboarded, all scans GO,
10 instruments live.** The carry-trend NO-GO contingency was never needed: even GBPJPY scans as
extension-fade (all trend rows anti). Crosses (EURGBP/EURJPY/GBPJPY) all macro-dead → 100%
price-driven confluence. GBPJPY = first pair with COT disabled (no CFTC cross contract).
Amends D022 (netting enforcement dropped). See [[currency_exposure]].
**Decision:** Expand to **all 7 new pairs** — AUDUSD, NZDUSD, USDCAD, USDCHF, USDJPY, EURJPY,
GBPJPY — onboarded **sequentially, one at a time** (easy→hard: USD-quote clones → USD-base class →
JPY block), each gating on its own 16yr signal-scan GO before its confluence goes ACTIVE.
Operator rulings:
1. **No risk caps.** "This is a system to generate trading signals, not a risk-management system."
   `scripts/fx_exposure.py` rewritten: per-currency-leg ledger over all 10 FX instruments
   (8 currencies), **advisory only** — flags shared leg-direction between pairs (e.g. EURUSD +
   GBPUSD both short = 2× long USD) and **suggests the single cleaner trade** (highest EC).
   No auto-SKIP, no auto-cancel, no $/axis cap. D022's algebra kept, its enforcement dropped.
   Soft note: AUDUSD+NZDUSD same direction ≈ one bet (corr ~0.85).
2. **No quote-currency conversion — everything sized in USD (Exness).** Same formula all pairs:
   `lots = $2000/(SL × TICK_MULTIPLIER)`. CHF/CAD-quoted drift (~25–28%) accepted, like the
   EURGBP GBP pass (D023). **Exception forced by arithmetic, not policy:** JPY-quoted pairs
   (USDJPY/EURJPY/GBPJPY, pip=0.01, price ~155) get a **static `TICK_MULTIPLIER = 650`**
   (≈100000/154, pip ≈ $6.5/lot) — the majors' 100000 is wrong by ~155×, not a tolerable drift.
   Constant, no live spot lookup; revisit if USDJPY moves ±15% from ~154.
3. USD-base pairs (USDCAD/USDCHF/USDJPY) are a **new config class**: `USD_BETA_SIGN=+1`,
   DXY-jump/VIX polarity flipped vs USD-quote majors (USDJPY VIX polarity = open empirical
   question, JPY safe-haven), COT futures (6C/6S/6J) quoted inverted → sign-flip, VP disabled.
**Rationale:** operator wants breadth of signal coverage; risk discretion stays human. JPY
crosses are carry-trend pairs — mean-reversion template may scan NO-GO; scan decides, a NO-GO
pair keeps config+data+research but no active confluence.
> **2026-06-29 update:** Lot sizing (point 2 above) removed project-wide — the system tracks
> risk in R-multiples only, no $-denominated position sizing or lot output. `TICK_MULTIPLIER`
> values are retained here as historical record of the per-pair pip-economics ruling, not as a
> live formula input.

## D023 — EURGBP added as a tradable CROSS: mean-reversion, macro-light, no VIX-veto, USD-sized
**Status:** ACTIVE (2026-06-09). See `wiki/system/eurgbp/` + `wiki/research/eurgbp/signal-results.md`.
**Decision:** Onboarded EURGBP (EG0–EG5). It is a **cross, not a USD-major** — distinct rules:
(1) **Mean-reverting**, validated D1 16yr (near-20d-low long +9.3pp t=4.61, RSI<30 +16.7 t=3.32) +
H4/H1 2020→now (H1 t up to 7.45, both directions); edge clears cost despite low vol (D1 ATR ~half a
major; spread 1–1.5pip = 6–10% of edge). (2) **Macro thin/DEAD** (EG2): no free daily German/UK
market yields → ECB−BoE differential is one-sided; all rate slopes noise. Macro = 0.5 tilt, NOT a
gate. (3) **🔑 NO VIX-veto** — risk-off bids EUR over GBP → EURGBP UP, *inverted* vs the USD-majors'
USD-bid; the FX VIX-LONG-veto must not transfer. (4) **Hard-block events = ECB/BoE/UK/EZ**, US =
caution only (no USD leg). (5) **Netting prerequisite:** EURGBP IS the cross risk-axis (D022) — every
order routes through `scripts/fx_exposure.py` or it can stack on an implied cross. (6) **Sizing in
USD, no GBP→USD conversion** (operator decision; assumes broker settles EURGBP pips in USD — caveat
documented). Confluence ACTIVE; ready for first `/weekly eurgbp`.
**Rationale:** Triangular arbitrage (EURGBP=EURUSD/GBPUSD) is HFT-latency territory, not capturable
retail. But the triangle's mean-reverting relative-value structure IS tradable on a swing horizon,
and the netting ledger (D022) makes a third correlated instrument safe to add. Deferred: derived
6E/6B COT, EG2b Bund–Gilt daily macro gate (only if a macro gate is later wanted).

## D022 — FX risk is per currency-factor, not per instrument; EURUSD+GBPUSD net via leg algebra (Architecture A)
**Status:** ACTIVE (2026-06-09). See [[currency_exposure]] + constitution "Portfolio Currency-Leg Netting".
> **2026-06-29 update:** the "$2000 per currency-factor" risk unit below is historical — lot/$
> sizing was removed project-wide; risk is tracked in R-multiples only. The netting-gate logic
> (keep best, drop weaker by Entry Confluence) is unaffected and still ACTIVE.
**Decision:** EURUSD, GBPUSD, EURGBP form a triangle (`EURGBP = EURUSD/GBPUSD`) — two majors share
the USD leg, so two simultaneous orders concentrate onto ONE factor, never diversify. Risk unit for
FX becomes **$2000 per currency-factor**. `/validate` runs a netting gate before writing an FX
ORDER LIMIT: if the other major is already live today, resolve **keep best, drop weaker** by Entry
Confluence (new EC > existing → cancel+replace; else new = ❌ SKIP, a new verdict distinct from NO
TRADE — zone stays PENDING). Same direction → doubled-USD bet; opposite → EURGBP-cross bet. EURGBP
is **reference-only, never traded** (true triangular arb is HFT-latency territory, not capturable
on a retail feed). Scope = cross-instrument FX only; gold excluded (real-yield driver, not a USD
leg); within-instrument stacking + full exposure ledger deferred to **Architecture B** (planned).
**Rationale:** Both W24 FX forecasts are SHORT → SHORT+SHORT = 2× long USD. Without netting, filling
both = a $4000 single-factor bet masquerading as two independent $2000 trades. The gate closes a
live hidden-concentration hole the moment both pairs can fill. Chose A (pairwise tie-break, pure leg
algebra, zero new data/infra) over B (exposure accounting) and C (cointegration stat-arb engine) to
ship the safety fix immediately and reuse all existing infrastructure.

## D021 — FX majors (EURUSD/GBPUSD) are mean-reverting; macro = DXY-jump + US2Y-slope + VIX-spike, NOT carry-diff
**Status:** ACTIVE (research basis; confluence PROPOSED, pending operator approval).
**Decision (2026-06-09):** Reverses D001's gold-only scope — add EURUSD + GBPUSD. Their edge
structure is the **inverse of gold**: gold is momentum, FX majors are **mean-reverting**. Fade
oscillator/band/structure extremes; trend-following (EMA regime, ADX-gated trend, Supertrend,
PSAR, Aroon, Donchian breakout) is a measured ANTI-edge (|t| up to 5.6). Macro is NOT the
rate-differential carry model originally planned (P2): carry-diff slope + 2s10s curve are
measured DEAD (t<0.3 even on 16yr). The real macro/intermarket edges are **DXY 1d jump>0.5 →
short the pair** (dominant, EUR t=9.29 / GBP t=7.27), **US 2Y (DGS2) 20d slope** (t≈2.1–2.4),
and **VIX 1d spike>3 → short** (risk-off USD bid; GBP −22pp t=−5.60).
**Rationale:** Built `scripts/backtest_signals.py` (extended Phase-0b catalogue), ran D1 2010→now
(16yr) + H4/H1 2020→now. The 2022-only sample showed macro null — that was a hawkish-regime
artifact; the 16yr sample revives US2Y-slope/DXY/VIX. Carry-diff genuinely carries no edge at the
weekly horizon. Confluence rewritten as mean-reversion R1/R2 per pair.
**belief_log:**
- date: 2026-06-09
  belief: "FX majors mean-revert (opposite of gold); score fades, never trend-follow; macro = DXY-jump + US2Y-slope + VIX-spike, not carry-diff/2s10s"
  trigger: "P3 independent signal backtest, EURUSD + GBPUSD, 16yr D1 / 6.4yr intraday"
- date: 2026-06-09
  belief: "P2 rate-differential macro thesis is reporting-only context; not a scored direction gate"
  trigger: "carry-diff + 2s10s measured t<0.3 on both 3.5yr and 16yr samples"

**Related files:** `wiki/research/{eurusd,gbpusd}/signal-results.md`,
`wiki/system/{eurusd,gbpusd}/confluence_criteria.md`, `scripts/backtest_signals.py`,
`scripts/config/_fx_base.py`.

---

## D020 — Weekly-pull stays plain-text; add JSON only on first programmatic consumer
**Status:** ACTIVE.
**Decision (2026-06-07):** Keep `data/weekly_pull/xauusd/weekly_pull_{YEAR}_W{WW}.txt` as the
weekly-pull format. Do NOT convert to JSON now. When a *script* first needs the computed numbers
(e.g. `check_v1b` reusing ATR/slope instead of recomputing), switch `build_snapshot` to build one
dict and **dual-emit**: `weekly_pull_W{WW}.json` (canonical machine truth) + `.txt` rendered from
the same dict (keeps Claude's annotated view). Point the new script at the JSON.
**Rationale:** Today the txt has exactly one consumer — Claude (an LLM), which reads labeled prose
as well as JSON. The inline interpretation (`RISING ⚠ bearish gold`, `20d slope (falling trend)`)
is free reasoning scaffolding that plain JSON discards. No machine parses the file, so JSON's parse
advantage is currently unused; converting now = churn + risk for zero benefit. Dual-emit on the
first programmatic reader avoids a single-source/recompute drift between scripts and the snapshot.
**belief_log:**
- date: 2026-06-07
  belief: "txt format correct while Claude is sole consumer; add JSON via dual-emit when a script first needs the numbers"
  trigger: "Design review — whether to replace weekly_pull txt with another storage format"

---

## D019 — v2 Reconstruction: Trading Zones, markdown-only, gold-only
**Status:** ACTIVE — current system baseline. Supersedes the SL/TP/offset/confluence mechanics in
D002, D003, D005, D008, D009, D011, D012, D013, D014, D017, D018.
**Decision (2026-06-02):** Restart the system as structured rules + AI analysis for high-quality
entry signal generation. Markdown-only (Claude writes forecasts/validations
directly). New output unit = **Trading Zone** (max 3/week, ≤1 counter) scored by **Zone Confluence**
(max 10, floor 5.0). Added **Entry Confluence** at /validate (max 10, floor 5.0; E0 confirmation 3pt).
New SL (`H4_ATR` floored, blended with 0.5×D1_ATR only when 0.5×D1>H4 — structural pivot dropped),
new TP (TP1 2.5R manual / TP2 3.0R limit / BE 1.5R), new outward offset
`max(SL/3, (10−score)×0.2×SL)` anchored on confirmation close or 50% zone midpoint.
**Rationale:** Old setup/DB/app stack was overhead for a single discretionary operator. Zones +
two confluence scores keep the edge-first scoring while simplifying storage and execution.
**belief_log:**
- date: 2026-06-02
  belief: "Markdown + scripts pipeline is enough; DB/app removed; zones replace setups"
  trigger: "Operator restart — redefine system around high-quality entry signals"
- date: 2026-06-02
  belief: "Zone Confluence (R1) + Entry Confluence (R2) weights APPROVED by operator and ACTIVE. Pin tail ratio set to ≥2.5×body (between research 2× and stricter 3×)."
  trigger: "R1/R2 research pass on independent-signal-results.md; operator approved"

---

## D018 — Weekly confluence reweight from Phase 0b signal research (2026-05-29)
**Status:** SUPERSEDED by D019 (S1–S7 weekly confluence replaced by Zone Confluence Z1–Z7). The
underlying findings (gold = momentum; DFII10 slope dominant; EMA confirmed; Fib/Pivot no edge)
carried forward into the v2 weights.
**Decision:** XAUUSD weekly confluence (S1–S7) reweighted based on measured forward-return edge
from Phase 0b signal research (D1 fwd=5, 6.3yr, 50+ signals × 3 TFs).
Changes: Fundamental 2.5→**3.0** (strongest signal: DFII10 slope +5.3pp t=2.95**);
EMA 0.75→**1.0** (EMA regime +4.7pp t=3.13**); Fib 0.75→**0.5** (no standalone edge);
Pivot **removed** (0.5→0, no evidence + needed to maintain 10.0 cap). Max stays 10.0.
**Rationale:** Prior weights were theory-based (literature + Tier A/B/C logic), not measured.
Phase 0b tested each signal independently. Key findings:
gold is MOMENTUM not mean-reverting (RSI>70 continues, RSI<30 bounces — asymmetric);
DFII10 slope is the dominant signal; EMA regime is the strongest confirmed filter; Fib and
Pivot had zero measurable independent edge. Pivot subsumed by structural zone (if pivot
coincides with S/R, Signal 1 already scores it). COT crowded long is momentum signal, not
contrarian fade. RSI divergence (S3, 1.5) kept — divergence ≠ level extreme, not tested here.
**belief_log:**
- date: 2026-05-29
  belief: "Weight Fundamental 3.0 > Structure 2.5 > VP/RSI 1.5 > EMA 1.0 > Fib 0.5"
  trigger: "Phase 0b independent signal scan — first evidence-based weighting for gold weekly confluence"

---

## D017 — G5 (VIX) + G6 (Asia) demoted to 0-point veto; weight → G1/G3/G2/V2 (2026-05-28)
**Status:** SUPERSEDED by D019 (G1–G6 daily-validation rubric replaced by Entry Confluence E0–E5).
The VIX>35 short veto carried into v2 as the VETO hard block; Asia-range gate dropped entirely.
**Decision:** XAUUSD daily-validation reweight. G5 (VIX, was 1.5) and G6 (Asia range, was 0.5) now
award ZERO points. G5 retains a hard RISK veto (VIX>35 → shorts NO TRADE); G6 is informational/logged.
Their 2.0 pts redistributed to backtest-proven anchors: G1 3.5→4.0, G3 3.0→3.5, G2 1.0→1.5, V2 0.5→1.0.
Max stays 10.0; floor 6.0 still needs ≥1 of G1/G3.
**Rationale:** A Phase-0 backtest sweep added VIX + Asia-range and tagged every executed
trade. The live-formula strategy fires only ~1.7 trades/yr (11 in 6.3yr) → sample far too small to
validate a 2.0-pt sub-weight. What signal existed was null/contradictory: Asia-compressed avgR +0.86
vs normal +1.17 (compression did NOT help); VIX>25 was n=1 (one lucky long). Edge-first: an
unconfirmable weight is removed, not assumed. Resolves the X1 audit item — answer was (a) "keep only
if confirmed," and it was not confirmed.
**belief_log:**
- date: 2026-05-27
  belief: "G5 VIX 1.5 + G6 Asia 0.5 added via Path B redistribution (assumed weights)"
  trigger: "Daily-validation reweight — VIX/Asia hypothesized to add edge"
- date: 2026-05-28
  belief: "G5/G6 demoted to 0-pt veto/info; backtest can't validate sub-weights at ~1.7 trades/yr"
  trigger: "Phase-0 VIX/Asia backtest sweep — X1 audit; edge not confirmed"

---

## D015 — System-audit honesty + ADX wired + G1 floor-math correction (2026-05-28)
**Status:** PARTIALLY SUPERSEDED by D019. The gate floor-math (G1/G3, 6.0 floor) is replaced by the
v2 Z/E rubric; the ADX-as-floor-modifier wiring was dropped (ADX is informational in v2). The durable
beliefs — thin-but-real edge, frequency from breadth not loose gates — still hold.
**Decision:** Three audit outcomes recorded as belief: (1) XAUUSD's real edge is THIN — Phase-0 backtest showed the prior "edge" was a hardcoded structure-gate stub; real signal ≈ 2 trades/yr/instrument, carried by the outward-offset (load-bearing: fill-at-trigger PF 0.64, PF rises monotonically with offset) + mandatory structural. Frequency must come from instrument breadth, never from loosening gates. (2) The ADX(14) regime filter, previously a floating doc rule, is now WIRED: transitional regime (ADX 20–25) raises the daily-validation floor 6.0→6.5; /weekly biases setup type by regime. (3) Corrected a wrong doc claim — daily floor 6.0 needs **at least one** of G1/G3, not both; G1 is scored (3.5) but NOT individually mandatory (a G1-fail week clears 6.0 via G3+G5+G2+V2+G6=6.5).
**Rationale:** Honest framing prevents over-trusting the confluence score. Dead/floating rules erode doc trust — wire them or delete them. G5 (VIX 1.5) + G6 (Asia 0.5) remain PROVISIONAL pending backtest-loader validation (D-pending, task X1).
**belief_log:**
- date: 2026-05-28
  belief: "XAUUSD edge thin but real (offset + structure); ADX now a live floor modifier; G1 non-mandatory by design and by floor math"
  trigger: "Deep system audit — weakness review"

---

## D014 — Entry-mechanism cleanup: offset 0.3→0.25, delete inert gates
**Status:** SUPERSEDED by D019 (v2 offset = `max(SL/3, (10−score)×0.2×SL)`). The load-bearing-offset
and selective-by-design beliefs carried forward.
**Decision:** (1) `entry_offset = (10 − score) × 0.25 × stop_distance` (was 0.3). (2) Deleted two inert rules proven never to bind in backtest: H1 trigger recency cap (≤8 bars; got_trigger==fresh_trigger always) and the R≥1.8 floor (filled==passed_R always). G1 stays SCORED (3.5 pts), NOT mandatory — a G1-fail week can still clear 6.0 via other gates; user opted to keep that flexibility.
**Rationale:** Phase-0 backtest research (2020–2026). Outward offset is load-bearing — fill-at-trigger loses (PF 0.64); per-trade PF rises monotonically with offset. 0.25 chosen for quality over frequency (user: "fine with no trade than losing; this is backtest not live"). Method is intentionally selective; usable frequency must come from instrument breadth, NOT from loosening gates. Open question flagged: strict 2-pivot fractal on H1 may over-filter vs the human "both trending" intent — revisit the H1 structure definition before relying on live frequency.
**belief_log:**
- date: 2026-05-25
  belief: "0.3 coefficient, recency cap + R-floor active"
  trigger: "D013 + later /validate additions"
- date: 2026-05-28
  belief: "0.25 coefficient, inert gates removed; G1 stays scored (not mandatory)"
  trigger: "Phase-0 edge research + user-directed config"

---

## D013 — Outward offset coefficient 0.2 → 0.3
**Status:** SUPERSEDED by D014, then D019.
**Decision:** `entry_offset = (10 − score) × 0.3 × stop_distance` (was 0.2). Higher coefficient amplifies overshoot demand on lower-confluence setups.
**Rationale:** At 0.2, score-5.5 setup offset = 0.9×stop ≈ same as stop. At 0.3, score-5.5 offset = 1.35×stop — stronger commitment filter on weak setups, near-zero impact on high-confluence (score 8+ → 0.6×stop offset). Steeper score-to-overshoot gradient.
**belief_log:**
- date: 2026-05-25
  belief: "0.2 coefficient — moderate score-scaled overshoot buffer"
  trigger: "D012 initial outward-offset reinstatement"
- date: 2026-05-25
  belief: "0.3 coefficient — steeper gradient, stronger filter on low-confluence"
  trigger: "User-directed tightening"

---

## D012 — Stop = avg of three; outward offset reinstated at 0.2 coefficient
**Status:** SUPERSEDED by D019 (v2 SL drops the structural-pivot term; offset reworked with SL/3 floor).
**Decision:** Stop formula switched from triple-max to arithmetic mean: `stop_distance = avg(0.5 × D1_ATR14, H4_ATR14, structural_dist)`. Entry offset reinstated but reversed: `entry_offset = (10 − score) × 0.2 × stop_distance`, applied OUTWARD beyond zone extreme. Short: `limit_price = zone_top + entry_offset`. Long: `limit_price = zone_bottom − entry_offset`. Coefficient bumped from 0.1 → 0.2 to make offset meaningful on tighter stops.
**Rationale:** (a) Triple-max produced very wide stops when any one dimension was large, shrinking lots aggressively. Mean smooths regime extremes — each dimension contributes equally. (b) Outward offset = pure buffer from spot; price must overshoot zone extreme by offset amount before triggering. Low-confluence setups demand bigger overshoot (price has to commit harder). High-confluence setups fill near zone extreme. Earlier inward-offset (D010) gave premature fills; D011 zone-extreme placement gave no graduation by score. New rule restores score-scaled buffer in correct direction.
**belief_log:**
- date: 2026-05-25
  belief: "Triple-max stop + zero offset (limit at zone extreme)"
  trigger: "D011 — fix inward-offset early-fill problem"
- date: 2026-05-25
  belief: "Arithmetic-mean stop + outward score-scaled offset"
  trigger: "Triple-max collapsed lot sizing when structural pivot was far; zero-offset wasted confluence signal as fill-aggression gradient. User-directed change: mean for balance, outward offset for graduated commitment filter"

---

## D011 — Stop = triple-max; H4 ATR trading-day only; limit at zone extreme
**Status:** SUPERSEDED by D012, then D019. The trading-day-only H4 ATR filter (range ≥ $1) carried
into v2.
**Decision:** Stop formula upgraded to `stop_distance = max(0.5 × D1_ATR14, H4_ATR14, structural_dist)`. H4 ATR computed only on trading-day H4 bars (filter: bar range >= $1.00, drops weekend/holiday flatline). Order limit placed AT zone extreme (zone_top for short, zone_bottom for long) — `(10−score) × 0.10 × stop_distance` inward offset deprecated.
**Rationale:** (a) Triple-max ensures stop clears both intraday (H4 ATR) and daily (0.5×D1 ATR) volatility floors plus structural level — earlier `max(structural, 0.5×H4_ATR)` collapsed when H4 ATR was small. (b) Weekend/holiday H4 bars are flatline (~$0.27 range) — they destroyed rolling ATR(14) when included (computed $7.22 vs true $31.21 on 2026-05-25). Range≥$1 filter restores real-volatility ATR. (c) Inward offset pulled limit toward current spot, reducing buffer from spot and giving worse fill on confirmed-rejection trades. Limit at zone extreme = max buffer, requires price to commit to the extreme before triggering.
**belief_log:**
- date: 2026-05-25
  belief: "stop floor at 0.5×H4_ATR sufficient + (10−score) inward offset gives best fill"
  trigger: "Original system design"
- date: 2026-05-25
  belief: "Triple-max stop + trading-day-only H4 ATR + limit at zone extreme — buffer matters more than fill aggression"
  trigger: "Sun-CME +1.46% gap exposed: (a) H4 ATR collapsed to $7.22 due to weekend flatline bars making atr_floor meaningless, (b) inward offset placed limit $4570.38 only $7 above spot $4563.16 with rejection target at zone_top $4575 — fill probability good but stop $23.08 too tight vs $35.24 D1-implied volatility floor"

---

## D010 — Add COT / GLD / Globex Gap / Baseline Drift as Forecast Inputs
**Status:** ACTIVE — carried into v2. These inputs are still produced by the weekly pull and used by
/validate drift checks.
**Decision:** Weekly pull adds (a) CFTC COT non-commercial net for COMEX gold, (b) SPDR GLD daily tonnes (1w/4w Δ), (c) weekend Globex gap (Fri close → Sun open on H4), (d) `baseline_dfii10` + `baseline_dxy` stamped to weekly frontmatter. /validate checks DFII10 drift vs baseline (>0.10% against direction = fail check 2; >0.15% any direction = force re-forecast). Monday /validate also evaluates weekend gap (>0.50% warning, >1.00% re-forecast).
**Rationale:** COT = crowd-position warning (Soros/Kovner positioning awareness). GLD flows = real Western investor demand proxy. Weekend gap surfaces weekend news pricing before Monday London opens. Baseline drift converts vague "macro unchanged?" check into a numeric threshold (Simons-style measurement).
**belief_log:**
- date: 2026-05-21
  belief: "FRED + price data sufficient — positioning + flows + gaps optional"
  trigger: "Initial design — minimize data dependencies"
- date: 2026-05-21
  belief: "Positioning + flows + gap + baseline drift add measurable edge filters at low cost (all free/auto sources)"
  trigger: "System review — adopted Tier 4 data upgrades from trader research"

---

## D009 — Drop All Trade Caps — Signal Quality Gate Only
**Status:** SUPERSEDED by D019 (v2 caps zones at max 3/week, ≤1 counter). The quality-gate-as-primary-governor principle carried forward.
**Decision:** Remove all calendar and dollar-based weekly caps. Trades taken whenever a setup independently passes gates. No weekly count or risk-dollar ceiling.
**Rationale:** Caps are artificial filters that reject valid high-conviction setups. System focus is generating and acting on quality signals. Gate quality (confluence score, validation floor) is the only governor — not clock or dollar counting.
**belief_log:**
- date: 2026-05-21
  belief: "1 trade/wk during single-instrument phase reduces overtrading risk"
  trigger: "Conservative phase opening"
- date: 2026-05-21
  belief: "Risk cap alone is sufficient. Calendar cap arbitrary and misses independent A+B fills."
  trigger: "System review — confluence floor + cap filter already restricts trade count organically"

---

## D008 — Tiered Confluence Weighting (max 10.0)
**Status:** SUPERSEDED by D018, then D019 (v2 Z1–Z7 weights and floor 5.0). The fake-confluence /
tiering principle carried forward.
**Decision:** Replace flat 7-signal /4-floor scoring with tiered weights summing to 10.0. Tier A (Structural 2.5, Fundamental 2.5), Tier B (RSI div 1.5, Volume Profile 1.5), Tier C (Fib 0.75, EMA 0.75, Pivot 0.5). Floor 5.5/10. Counter floor 7.5/10. Offset formula `(10 - score) × 0.10 × risk_unit`.
**Rationale:** Flat weighting let three price-derived signals (Fib + EMA + Pivot, all anchored to same swing) inflate score to 3/7 from one underlying observation. Tiered weights neutralize fake confluence and give Structure + Macro the empirical weight literature supports (Hsu/Taylor/Wang 2016, gold real-yield primacy in xauusd_profile).
**belief_log:**
- date: 2026-05-21
  belief: "Flat 7-signal scoring sufficient; cap filter alone handles fake confluence"
  trigger: "Initial system design"
- date: 2026-05-21
  belief: "Tier signals by empirical edge + independence. Structural + Fundamental dominate (2.5 each); price-derived Tier C compressed to 0.5–0.75"
  trigger: "System review — recognized Fib+EMA+Pivot overlap inflates score from single underlying observation"

---

## D007 — H4 Trigger is Entry Confirmation, Not Confluence
**Status:** ACTIVE — carried into v2 as Entry Confluence E0 (entry confirmation at /validate, 3.0 pts).
**Decision:** H4 trigger (pin bar, engulfing, break-and-retest inside zone) is removed from the confluence scoring rubric entirely. Confluence is 7 signals, not 8. Trigger is observed at /validate time as entry confirmation — recorded in daily file but does NOT alter score, offset, or whether the limit gets placed.
**Rationale:** A weekly forecast generated Sunday cannot score an H4 pattern that has not formed yet. Listing it as Signal 8 with "❌ Not formed yet" was scoring an event by its non-occurrence, which is incoherent. Removing it makes the weekly score a function only of weekly-derivable signals (structure, Fib, RSI, EMA, pivot, fundamental, volume profile). H4 trigger still has informational value at validation — kept in daily file as observation.
**belief_log:**
- date: 2026-05-21
  belief: "Confluence = 7 weekly-derivable signals. H4 trigger is daily observation."
  trigger: "User flagged: trigger cannot exist Sunday, should not be in weekly forecast"

---

## D006 — H4 Trigger Removed from Confluence (SUPERSEDED by D007)
**Status:** SUPERSEDED by D007.
**Decision (original):** H4 entry trigger was Signal 8, optional confluence.
**belief_log:**
- date: 2026-05-21
  belief: "Trigger as Signal 8 — retains value as confluence without being a blocker"
  trigger: "Buy limit redesign — mandatory gate incompatible with pre-placed limit execution"
- date: 2026-05-21
  belief: "H4 trigger is not confluence — it is /validate-time entry confirmation only"
  trigger: "H4 patterns cannot form Sunday at forecast time, so scoring them in weekly forecast is incoherent"

---

## D005 — Order Limit Execution with Daily Validation Gate + Entry Offset
**Status:** PARTIALLY SUPERSEDED by D019. The order-limit + daily-validation-gate execution model is
ACTIVE; the specific offset formula (0.20 × H4 ATR × missing signals) is replaced by the v2 offset.
**Decision:** All entries via order limits (buy limit / sell limit). No market orders, no bar-close entry. Order limit is placed only after daily /validate passes — not on Sunday, not pre-placed for the week. Expires 21:00 UTC same day. Re-validated and re-placed each morning if setup still valid.
**Rationale:** Bar close confirmation forces entry after the fact — price already $10–30 inside zone. Order limits get best-price fill at the zone. Daily validation gate ensures setup is still valid before capital is committed — macro can shift mid-week, structure can break. Offset (0.20 × H4 ATR × missing signals) recalculates daily using fresh ATR. Unproven zones never fill. No fill = no loss.
**belief_log:**
- date: 2026-05-21
  belief: "Order limit with daily gate — systematic entry without discretionary trigger watching, protected by daily re-validation"
  trigger: "System redesign — bar close confirmation replaced with daily-gated order limits"

---

## D004 — No ICT/SMC Concepts
**Status:** ACTIVE — standing principle.
**Decision:** System uses market structure, S/R, RSI, EMA, Fibonacci, ATR. No order blocks, FVGs, liquidity grabs.
**Rationale:** Zero peer-reviewed validation. Cultish community dynamics. Same underlying concepts expressible with classical TA vocabulary that has partial empirical support.
**belief_log:**
- date: 2026-05-21
  belief: "Classical TA with macro filter > SMC vocabulary without empirical backing"
  trigger: "Explicit decision in system design"

---

## D003 — Minimum 4/7 Confluence
**Status:** SUPERSEDED by D008/D018, then D019 (v2 Zone/Entry Confluence, max 10, floor 5.0).
**Decision:** Never trade below 4/7 confluence score. 3/7 and below = NO TRADE.
**Rationale:** Research shows single-indicator rules have no edge in major FX post-2000. Confluence of independent signals is where modest edge survives. 4/7 floor with H4 trigger removed from scoring keeps the quality filter on weekly-derivable signals only.
**belief_log:**
- date: 2026-05-21
  belief: "3/6 minimum is the floor. Prefer 4+/6 in practice."
  trigger: "Based on Hsu, Taylor & Wang 2016 and system design"
- date: 2026-05-21
  belief: "4/8 minimum — trigger demoted to Signal 8, floor raised to compensate"
  trigger: "System redesign: order limit execution replaces bar close confirmation"
- date: 2026-05-21
  belief: "4/7 minimum — H4 trigger removed from confluence scoring entirely"
  trigger: "H4 trigger cannot exist at Sunday forecast time — moved to /validate as entry confirmation only"

---

## D002 — TP Structure: 3R full close
**Status:** SUPERSEDED by D019 (v2 TP1 2.5R manual / TP2 3.0R limit / BE at +1.5R).
**Decision:** Single TP at 3R. Close full position. No split.
**Rationale:** 3R minimum ensures positive expectancy at 40% win rate. Single exit removes partial-close decision fatigue. Structural TP required — no arbitrary R target with no level.
**belief_log:**
- date: 2026-05-21
  belief: "1.5R full close preferred over split-close for simplicity at this stage"
  trigger: "System design — small account, capital preservation priority"
- date: 2026-05-21
  belief: "Single 3R full close — removes split-close complexity, enforces structural TP discipline"
  trigger: "System review — TP1/TP2 split contradicted constitution, created confusion"

---

## D001 — XAUUSD as Primary Instrument
**Status:** SUPERSEDED by D021 (2026-06-09 — EURUSD + GBPUSD added). XAUUSD remains primary/most-mature.
**Decision:** Start with XAUUSD only before adding forex pairs.
**Rationale:** Real volume on CME enables AVWAP. Clear macro drivers (real yields, DXY). High liquidity, tight spreads. One instrument → faster mastery of its character.
**belief_log:**
- date: 2026-05-21
  belief: "XAUUSD only — single-instrument focus"
  trigger: "System design session — avoid correlation complexity on small account"
