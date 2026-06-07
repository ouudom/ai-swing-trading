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

> **Naming lineage:** entries before D019 use the pre-v2 gate labels (weekly `S1–S7`,
> daily `G1–G6`). v2 replaced these with **Zone Confluence (Z1–Z7)** + **Entry Confluence
> (E0–E5)** — see `confluence_criteria.md`. Old labels are kept in dated entries as
> historical record only; they are not active rule names.

---

## D019 — v2 Reconstruction: Trading Zones, markdown-only, gold-only
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

## D001 — XAUUSD as Primary Instrument
**Decision:** Start with XAUUSD only before adding forex pairs.
**Rationale:** Real volume on CME enables AVWAP. Clear macro drivers (real yields, DXY). High liquidity, tight spreads. One instrument → faster mastery of its character.
**belief_log:**
- date: 2026-05-21
  belief: "XAUUSD only — single-instrument focus"
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

## D009 — Drop All Trade Caps — Signal Quality Gate Only
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

## D014 — Entry-mechanism cleanup: offset 0.3→0.25, delete inert gates
**Decision:** (1) `entry_offset = (10 − score) × 0.25 × stop_distance` (was 0.3). (2) Deleted two inert rules proven never to bind in backtest: H1 trigger recency cap (≤8 bars; got_trigger==fresh_trigger always) and the R≥1.8 floor (filled==passed_R always). G1 stays SCORED (3.5 pts), NOT mandatory — a G1-fail week can still clear 6.0 via other gates; user opted to keep that flexibility.
**Rationale:** Phase-0 backtest research (2020–2026). Outward offset is load-bearing — fill-at-trigger loses (PF 0.64); per-trade PF rises monotonically with offset. 0.25 chosen for quality over frequency (user: "fine with no trade than losing; this is backtest not live"). Method is intentionally selective; usable frequency must come from instrument breadth, NOT from loosening gates. Open question flagged: strict 2-pivot fractal on H1 may over-filter vs the human "both trending" intent — revisit G1 H1 definition before relying on live frequency.
**belief_log:**
- date: 2026-05-25
  belief: "0.3 coefficient, recency cap + R-floor active"
  trigger: "D013 + later /validate additions"
- date: 2026-05-28
  belief: "0.25 coefficient, inert gates removed; G1 stays scored (not mandatory)"
  trigger: "Phase-0 edge research + user-directed config"

---

## D013 — Outward offset coefficient 0.2 → 0.3
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

## D018 — Weekly confluence reweight from Phase 0b signal research (2026-05-29)
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
**Decision:** Three audit outcomes recorded as belief: (1) XAUUSD's real edge is THIN — Phase-0 backtest showed the prior "edge" was a hardcoded structure-gate stub; real signal ≈ 2 trades/yr/instrument, carried by the outward-offset (load-bearing: fill-at-trigger PF 0.64, PF rises monotonically with offset) + mandatory structural. Frequency must come from instrument breadth, never from loosening gates. (2) The ADX(14) regime filter, previously a floating doc rule, is now WIRED: transitional regime (ADX 20–25) raises the daily-validation floor 6.0→6.5; /weekly biases setup type by regime. (3) Corrected a wrong doc claim — daily floor 6.0 needs **at least one** of G1/G3, not both; G1 is scored (3.5) but NOT individually mandatory (a G1-fail week clears 6.0 via G3+G5+G2+V2+G6=6.5).
**Rationale:** Honest framing prevents over-trusting the confluence score. Dead/floating rules erode doc trust — wire them or delete them. G5 (VIX 1.5) + G6 (Asia 0.5) remain PROVISIONAL pending backtest-loader validation (D-pending, task X1).
**belief_log:**
- date: 2026-05-28
  belief: "XAUUSD edge thin but real (offset + structure); ADX now a live floor modifier; G1 non-mandatory by design and by floor math"
  trigger: "Deep system audit — weakness review"

---


---

## D004 — No ICT/SMC Concepts
**Decision:** System uses market structure, S/R, RSI, EMA, Fibonacci, ATR. No order blocks, FVGs, liquidity grabs.
**Rationale:** Zero peer-reviewed validation. Cultish community dynamics. Same underlying concepts expressible with classical TA vocabulary that has partial empirical support.
**belief_log:**
- date: 2026-05-21
  belief: "Classical TA with macro filter > SMC vocabulary without empirical backing"
  trigger: "Explicit decision in system design"
