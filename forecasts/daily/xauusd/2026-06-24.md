---
type: daily_validation
instrument: xauusd
date: 2026-06-24
week: 2026-W26
generated: 2026-06-24T04:14Z
spot: 4056.23
h4_atr: 36.62
d1_atr: 121.96
vix: 17.3
macro_dfii10: 2.28
macro_slope20d: 0.12
dxy_jump: 0.448
zones:
  - label: PRIMARY
    direction: SHORT
    zone: [4200.0, 4235.0]
    verdict: NO_TRADE
    entry_confluence: 1.5
    hard_block: false
  - label: SECONDARY
    direction: SHORT
    zone: [4300.0, 4340.0]
    verdict: NO_TRADE
    entry_confluence: 1.0
    hard_block: false
---

# XAUUSD Daily Validation — 2026-06-24

**Run:** 2026-06-24 03:15 UTC · Spot: $4056.23 · H4_ATR: 36.62 · D1_ATR: 121.96

## Gates
- ✅ CB calendar: no decisions in window (06-24 → 06-26)
- ⚠️ Econ: US Core PCE m/m + Final GDP 2026-06-25 12:30 UTC (HIGH) — D028 forward-carry (flatten by 11:30 UTC if filled today)
- ✅ No V3 event window today

## PRIMARY — SHORT 4200–4235 · ZC 8.5 · MEDIUM-HIGH

**Q1 (Valid?):** V1 intact (D1 close 4056.23 < zone bottom 4200 — not above zone). V1b: no H4 closes near zone. ✅

**Q2 (Bias flip?):** DFII10 2.28 (baseline 2.23, drift +0.05 < 0.15% threshold). DXY jump 0.448 (no xauusd block). Macro aligned. ✅

**Q3 (Re-forecast?):** No trigger (T1 DFII10 1d +0.07 < 0.15; T2 DXY 1d 0.448 < 0.6; T3 no 2.5% move; T5 drift +0.05 < 0.15). ✅

**Q4 (Entry Confluence?):**
- E0 entry confirm: ❌ (no SHORT confirm; price 144 pts below zone bottom — unreached)
- E1 DFII10 slope ↑: ✅ (2.5)
- E2 DXY slope ↑: ✅ (1.5 via weekly score; inline with z3) — but zone unreached, H4 not at resistance
- EC approximation: ~3.0 (structural + slope only; zone approach required for full score)

❌ **NO TRADE — zone unreached (spot $4056 vs zone $4200–4235, 144 pts below)**

---

## SECONDARY — SHORT 4300–4340 · ZC 7.5 · MEDIUM

**Q1–Q3:** All intact. No V1/V1b. No re-forecast. ✅

**Q4:** Zone unreached (spot $4056, 244+ pts below). No E0. EC ~1.0.

❌ **NO TRADE — zone unreached**

---

## Context
VIX 17.3 (no veto). DXY at 1yr high per news feeds. GLD ETF inflow +78t (counter to bias — monitor). PCE/GDP Thu 11:30 UTC flatten note if any zone fills before then. Spot near weekly S1 ($4058.16) — could be near-term base for an oversold bounce into the zones.
