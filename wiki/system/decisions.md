---
type: decision
updated: 2026-05-21
confidence: high
tags: [decisions, system-design]
related: [constitution]
---

# System Decisions — Belief Log

## How to Use
Record key system choices here with reasoning.
When a decision changes, add a new belief_log entry — never delete old ones.

---

## D001 — XAUUSD as Primary Instrument
**Decision:** Start with XAUUSD only before adding forex pairs.
**Rationale:** Real volume on CME enables AVWAP. Clear macro drivers (real yields, DXY). High liquidity, tight spreads. One instrument → faster mastery of its character.
**belief_log:**
- date: 2026-05-21
  belief: "XAUUSD first, add EURUSD/GBPUSD after consistent profitability"
  trigger: "System design session — avoid correlation complexity on small account"

---

## D002 — TP Structure: 3R full close
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

## D003 — Minimum 4/7 Confluence
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

## D005 — Order Limit Execution with Daily Validation Gate + Entry Offset
**Decision:** All entries via order limits (buy limit / sell limit). No market orders, no bar-close entry. Order limit is placed only after daily /validate passes — not on Sunday, not pre-placed for the week. Expires 21:00 UTC same day. Re-validated and re-placed each morning if setup still valid.
**Rationale:** Bar close confirmation forces entry after the fact — price already $10–30 inside zone. Order limits get best-price fill at the zone. Daily validation gate ensures setup is still valid before capital is committed — macro can shift mid-week, structure can break. Offset (0.20 × H4 ATR × missing signals) recalculates daily using fresh ATR. Unproven zones never fill. No fill = no loss.
**belief_log:**
- date: 2026-05-21
  belief: "Order limit with daily gate — systematic entry without discretionary trigger watching, protected by daily re-validation"
  trigger: "System redesign — bar close confirmation replaced with daily-gated order limits"

---

## D006 — H4 Trigger Removed from Confluence (SUPERSEDED by D007)
**Decision (original):** H4 entry trigger was Signal 8, optional confluence.
**Status:** Superseded. See D007.
**belief_log:**
- date: 2026-05-21
  belief: "Trigger as Signal 8 — retains value as confluence without being a blocker"
  trigger: "Buy limit redesign — mandatory gate incompatible with pre-placed limit execution"
- date: 2026-05-21
  belief: "H4 trigger is not confluence — it is /validate-time entry confirmation only"
  trigger: "H4 patterns cannot form Sunday at forecast time, so scoring them in weekly forecast is incoherent"

---

## D007 — H4 Trigger is Entry Confirmation, Not Confluence
**Decision:** H4 trigger (pin bar, engulfing, break-and-retest inside zone) is removed from the confluence scoring rubric entirely. Confluence is 7 signals, not 8. Trigger is observed at /validate time as entry confirmation — recorded in daily file but does NOT alter score, offset, or whether the limit gets placed.
**Rationale:** A weekly forecast generated Sunday cannot score an H4 pattern that has not formed yet. Listing it as Signal 8 with "❌ Not formed yet" was scoring an event by its non-occurrence, which is incoherent. Removing it makes the weekly score a function only of weekly-derivable signals (structure, Fib, RSI, EMA, pivot, fundamental, volume profile). H4 trigger still has informational value at validation — kept in daily file as observation.
**belief_log:**
- date: 2026-05-21
  belief: "Confluence = 7 weekly-derivable signals. H4 trigger is daily observation."
  trigger: "User flagged: trigger cannot exist Sunday, should not be in weekly forecast"

---

## D008 — Tiered Confluence Weighting (max 10.0)
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

## D009 — Drop Calendar Trade Cap, Keep $ Risk Cap
**Decision:** Remove "max 1 trade per week" rule. Trades bounded only by $4000 weekly risk cap (= 2 losing trades). Multiple setups may fill same week if zones distinct and risk budget allows.
**Rationale:** Calendar cap is artificial — none of the trader-wizard literature (PTJ, Druckenmiller, Kovner, Brandt) trades by clock. Opportunity-driven beats time-boxed. The $4000 risk cap already enforces survival; the 1/wk rule adds nothing except missed independent setups.
**belief_log:**
- date: 2026-05-21
  belief: "1 trade/wk during single-instrument phase reduces overtrading risk"
  trigger: "Conservative phase opening"
- date: 2026-05-21
  belief: "Risk cap alone is sufficient. Calendar cap arbitrary and misses independent A+B fills."
  trigger: "System review — confluence floor + cap filter already restricts trade count organically"

---

## D010 — Add COT / GLD / Globex Gap / Baseline Drift as Forecast Inputs
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

## D012 — Stop = avg of three; outward offset reinstated at 0.2 coefficient
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

## D004 — No ICT/SMC Concepts
**Decision:** System uses market structure, S/R, RSI, EMA, Fibonacci, ATR. No order blocks, FVGs, liquidity grabs.
**Rationale:** Zero peer-reviewed validation. Cultish community dynamics. Same underlying concepts expressible with classical TA vocabulary that has partial empirical support.
**belief_log:**
- date: 2026-05-21
  belief: "Classical TA with macro filter > SMC vocabulary without empirical backing"
  trigger: "Explicit decision in system design"
