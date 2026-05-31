---
type: system
updated: 2026-05-28
confidence: high
tags: [process, instruments, onboarding, edge-first]
related: [constitution, confluence_criteria]
---

# Adding a New Instrument — Process

How to onboard a new tradeable instrument into the system, end to end. Derived from the
EURUSD build (2026-05). **Edge-first**: no live rule ships until it is *measured* to have edge
on THAT instrument — never assumed from XAUUSD. Same ARCHITECTURE for every instrument (weekly
forecast → daily validation → outward-offset limit), but the SIGNALS, WEIGHTS, and THRESHOLDS
are instrument-specific and research-derived.

## The invariants (never change per instrument)

These are universal — live in `wiki/system/core/constitution.md`, apply to every instrument:

- Risk model: $2,000/trade, $4,000/week, $10,000/month, 5% drawdown circuit breaker.
- Stop formula: `avg(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)` (arithmetic mean).
- Outward-offset limit entry: `entry_offset = (10 − score) × 0.25 × stop_distance`, placed
  OUTWARD beyond the zone extreme. **This is the live-execution edge — kept for every
  instrument regardless of backtest** (backtests understate real-fill quality).
- MTF stack: Weekly (bias) → Daily (setup) → H4 (limit + offset).
- Two-score gate: weekly confluence floor (quality) + daily validation floor (timing).
- Correlation guard via `USD_BETA_SIGN`.
- Re-forecast lifecycle: week-scoped, forward-only 12h event gate, 1/week cap.

## What is instrument-specific (must be defined per instrument)

- Confluence SIGNALS + WEIGHTS (which indicators have measured edge here).
- Daily validation GATES + WEIGHTS.
- All numeric THRESHOLDS, scaled to the instrument's unit (pips vs dollars).
- Macro driver (gold = DFII10; EUR = rate differential — and it may be NULL).
- Session windows (gold = Asia; EUR = London/NY overlap).
- Config constants: `TICK_MULTIPLIER`, `MIN_BAR_RANGE`, `G6_WINDOW_UTC`, `FRED_SERIES`,
  `COT_ENABLED`, `ETF_ENABLED`, `VP_TICKER`, `USD_BETA_SIGN`.

---

## Phase 0 — Decide it's worth attempting

- Is there a plausible, theory-grounded edge hypothesis? (Not "it trades, so we'll trade it.")
- Is free/affordable data available at sufficient history (target ≥ 6 yr for OOS split)?
- Does it share a macro driver with a live instrument? (→ correlation-guard implications.)

Output: a go/no-go note in `wiki/research/{instrument}/_INDEX.md`.

## Phase 1 — Scaffold (no live trading)

1. `instruments/{instrument}/config.py` — copy XAUUSD's, then set every constant for the new
   instrument. **Critical: `TICK_MULTIPLIER`** ($1 move → $/lot). Getting this wrong is a silent
   N× risk bug (EUR shipped 10000, was 10× over-risk; correct = 100000).
2. Register the instrument in `scripts/weekly_pull.py` `REGISTERED_INSTRUMENTS`.
3. Create `wiki/system/{instrument}/` with four scaffold pages:
   `profile.md`, `macro_drivers.md`, `confluence_criteria.md`, `constitution_addendum.md`.
   Mark `confidence: low` until research fills them.
4. Create `wiki/research/{instrument}/_INDEX.md` (data sources, planned concepts, standards).
5. Pull data: backfill TD M15 → resample to H1/H4/D1. Note free-tier history walls.

## Phase 2 — Research the edge (the long phase)

Measure, don't assume. For each candidate signal report: **N, win%, edge in pp vs the
instrument's OWN directional baseline, EV in R, trades/yr — tested LONG and SHORT separately.**

Test at minimum:
- Macro driver (slope/level vs forward return). **Test regime stability** (split by era) — a
  signal that flips sign across regimes is not tradeable. (EUR rate-diff did exactly this.)
- MTF structure (fractal HH/HL via `scripts/structure.py`) — symmetric on both sides?
- ATR compression → expansion probability.
- Session timing (which hours actually move).
- Momentum/mean-reversion indicators (RSI extreme, Bollinger, Donchian breakout).
- Positioning (COT) if a futures contract exists.

**Compute the instrument's own directional baseline first** — gold's 54%-up does NOT transfer
(EUR is 48.9%, no drift). Edge is measured against the instrument's baseline, not gold's.

Hard rule: a signal with ~0 or regime-unstable edge is NOT given positive confluence weight.
At most it becomes a low-weight *veto/context* gate (never-against), or it is dropped.

Beware:
- **Timezone**: verify any third-party feed against TD on an overlap window. (HistData "EST"
  tracks US Eastern WITH DST → convert via `America/New_York`, not a fixed offset.)
- **Small samples**: 3 yr lied for EUR (a fade edge that inverted on 6.4 yr). Get OOS split +
  two independent feeds agreeing before trusting a result.

Log every finding — including NULLs — in `wiki/research/{instrument}/_INDEX.md`.

## Phase 3 — Codify the system docs

Translate measured edge into the four wiki pages:
- `confluence_criteria.md` — weekly signals + weights (only measured-edge signals), daily gates.
- `macro_drivers.md` — drivers ranked, with honest confidence (null → "context only").
- `profile.md` — ATR ranges, sessions, lot sizing, baseline.
- `constitution_addendum.md` — instrument overrides only (pip thresholds, news blocks, T3 %).

Keep the architecture identical to XAUUSD; change only signals/weights/thresholds.

## Phase 4 — Wire the pipeline (instrument-aware execution)

This is where EUR currently has gaps — check ALL of:
- `scripts/weekly_pull.py` must compute the instrument's OWN indicators (e.g. Bollinger for a
  mean-reversion instrument), its OWN macro series (not gold's DFII10), and emit price levels at
  the instrument's PRECISION (pips need 4–5 dp; gold's 2 dp rounds FX to garbage). Labels must
  not be gold-hardcoded.
- `.claude/commands/weekly.md` — Agents 3/4 route to the instrument's confluence doc.
- `.claude/commands/validate.md` — gates route to the instrument's gate set; `MIN_BAR_RANGE`,
  `G6_WINDOW_UTC` read from config.
- Backtest (`scripts/backtest/`) and live `/validate` must share primitives (`scripts/structure.py`)
  so they cannot diverge.

## Phase 5 — Calibrate provisional thresholds

Replace every placeholder with a value derived from the instrument's data:
session-range cutoff, counter-move %, weekend-gap %, invalidation buffer, confluence pip
tolerances. Mark each `confidence: medium`+ only once calibrated.

## Phase 6 — Dry-run + paper

- Dry-run `/weekly {instrument}` and `/validate {instrument}`; verify output is correct-precision,
  correctly-labeled, uses the right signals.
- Paper-trade until live behavior matches backtest expectancy (especially fill quality on the
  offset — the part backtests understate).

## Definition of done

- [ ] Config constants all set + `TICK_MULTIPLIER` verified by a hand-checked lot calc.
- [ ] Research index logs measured edge (and nulls) with N/win%/pp/EV.
- [ ] Four wiki pages reflect measured edge, not copied gold rules.
- [ ] Pipeline emits instrument-correct precision, indicators, macro series, labels.
- [ ] Backtest ↔ live share structure primitives.
- [ ] No provisional threshold left uncalibrated.
- [ ] Dry-run of both commands produces a clean forecast + validation.
</content>
</invoke>
