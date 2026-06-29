---
type: system
updated: 2026-06-02
confidence: high
tags: [confluence, zone, entry, scoring]
related: [constitution, xauusd_profile]
---

# XAUUSD — Zone & Entry Confluence Scoring (v2)

> **STATUS: ACTIVE — operator-approved (R1/R2, 2026-06-02).**
> Derived fresh from measured edges in `wiki/research/xauusd/independent-signal-results.md`
> (6.3yr backtest 2020–2026). Replaces the old 6/7-signal setup system. Do NOT back-translate
> old scores. Two distinct scores now exist:
> - **Zone Confluence** — scored at `/weekly`, rates a TRADING ZONE's inherent quality. Max 10, floor 5.
> - **Entry Confluence** — scored at `/validate`, rates whether TODAY justifies placing the order. Max 10, floor 5.

## Headline research constraint

**Gold is MOMENTUM, not mean-reverting.** Every scored signal must be pro-trend or
macro-regime-gated — NEVER a fade. Measured anti-edges that must never score:
- RSI>70 as a short signal (−12.2pp — gold continues up at OB)
- Price above Bollinger upper as short (−13.0pp — breakout, not reversal)
- Near 20d HIGH as short (−10.2pp — gold breaks resistance)
- Crowded COT long (net>200k) as short (−12.3pp — momentum phase, not reversal)
- DFII10 *level* as a gate (regime contamination — use *slope* only)

Structural levels are ZONE LOCATORS (where price reacts), never standalone fade signals.

---

## R1 — Zone Confluence (at `/weekly`, max 10.0, floor 5.0)

Scores each candidate trading zone. Max 3 zones/week, at most 1 counter-trend.

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| Z1 | **Structural Zone** | **2.0** | Price at significant D1/W1 S/R (prior swing H/L w/ 2+ reactions, role-reversal retest, round# at structure). Draw as box. **MANDATORY.** | Zone anchor by role (weak standalone edge +2.2pp; required to locate zone) |
| Z2 | **Real-Yield Slope (DFII10 20d)** | **2.5** | slope<0 for longs / slope>0 for shorts | +5.3pp, t=2.95** — strongest measured D1 signal |
| Z3 | **DXY Slope (20d)** | **1.5** | slope<0 for longs / slope>0 for shorts | long +5.3pp t=2.19* ; short −12.8pp t=−4.97** (strong) |
| Z4 | **Top-Down MTF Alignment (D→H4→1H)** | **2.0** | D1, H4, H1 structure all toward zone direction (HH+HL long / LH+LL short) | H4+H1 +3.0pp; all-3 bear +10.2pp |
| Z5 | **EMA Regime (D1 20/50)** | **1.0** | EMA20>EMA50 for longs / EMA20<EMA50 for shorts | +4.7pp, t=3.13** |
| Z6 | **ATR Compression (D1)** | **0.5** | D1 ATR14 < 20-day median | 82% expansion probability (timing, directionally neutral) |
| Z7 | **Volume Profile Node (CME GC)** | **0.5** | Weekly POC/VAH/VAL within zone | Institutional-flow proxy (can't refute w/ free data) |
| | **Total** | **10.0** | | |

**0-point vetoes (no score, hard risk only):**
- VIX > 35 → all SHORT zones blocked (safe-haven flow). VIX otherwise null directional.
- RSI>70 / COT>200k → never permitted as a short signal (enforce anti-edge list above).

**Floor:** 5.0/10 to publish a zone as PENDING. Z1 always mandatory.

**Counter-trend zone (against weekly bias):**
- Z2 + Z3 (macro bundle, 4.0 pts) score **0** — macro works against the trade. Ceiling = 6.0.
- **RSI divergence (D1) is a HARD PREREQUISITE** — no divergence, no counter zone.
  (Bullish div: lower-low price + higher-low RSI. Bearish: higher-high price + lower-high RSI.
  Divergence ≠ level extreme.)
- Only valid when macro confidence is LOW or MEDIUM. Macro HIGH → no counter zone.
- Counter must still reach floor 5.0 from {Z1 2.0, Z4 2.0, Z5 1.0, Z6 0.5, Z7 0.5} — tight by design.

---

## R2 — Entry Confluence (at `/validate`, max 10.0, floor 5.0)

Re-checks at entry day whether the zone still deserves an order. Entry confirmation = 3.0;
the other 7.0 are daily-recomputable time-decay checks (conditions can shift between Sunday
`/weekly` and entry day).

| # | Signal | Weight | Pass when | Evidence |
|---|---|---|---|---|
| E0 | **Entry Confirmation** | **3.0** | One of: 1H engulfing candle / 1H pin bar (tail ≥ 2.5× body) / 15M CHoCH over 60-candle structure — **toward zone direction (CONTINUATION), confirmed on 1H CLOSE** | pin+offset = highest-quality cell (PF 3.38). Trigger alone has no edge — value is as a quality filter combined with the outward offset. **Fade RSI-reclaim does NOT apply (gold = momentum, D027).** |
| E1 | **H4 Structure Aligned (today)** | **2.5** | H4 HH+HL (long) / LH+LL (short) | +3.0pp gate. H1 dropped — pullback-into-zone entries run counter-trend on H1 at fill, so H1 alignment penalized valid discount entries; E0 governs the H1/15M trigger at the zone. |
| E2 | **Real-Yield Slope Still Supports** | **2.0** | DFII10 20d slope direction holds today | strongest macro signal, re-checked live |
| E3 | **Macro Drift OK** | **1.0** | \|DFII10 now − baseline\| < 0.10 against direction | regime-shift guard |
| E4 | **ATR Compression (today)** | **1.0** | D1 ATR14 < 20-day median | 82% expansion timing |
| E5 | **DXY Slope Still Supports** | **0.5** | DXY 20d slope direction holds today | confirms macro bundle intact |
| | **Total** | **10.0** | | |

**Output logic:**
```
floor = 5.0
hard blocks pass AND entry_confluence ≥ floor AND E0 confirmation present
    → ✅ ORDER LIMIT at (confirmation candle close ± outward offset)
hard blocks pass AND entry_confluence ≥ floor AND no E0 confirmation
    → ✅ ORDER LIMIT at (50% zone midpoint ± outward offset)   [set-and-forget]
hard blocks pass AND entry_confluence < floor
    → ❌ NO TRADE
any hard block fails
    → ❌ NO TRADE / INVALIDATED
```

> **Note — intentional overlap with Zone Confluence.** E1/Z4 (MTF structure), E2/Z2 (real-yield
> slope), E4/Z6 (ATR), E5/Z3 (DXY) re-measure the same dimensions. This is BY DESIGN: Zone
> Confluence asks "is this a good zone?" at forecast time; Entry Confluence asks "is it still
> good *today*?" at entry time. Same axis, different clock. Not double-counting within a single score.

**Hard blocks (binary, checked first — see [[constitution]]):**

| | Block | Fail action |
|---|---|---|
| V1 | D1 close beyond zone | INVALIDATED — remove zone from _HOT.md |
| V1b | 2 consecutive H4 closes >$5 past zone extreme | INVALIDATED — cancel limit (`scripts/check_v1b.py`) |
| V3 | NFP/FOMC/CPI/US Retail Sales within 2h of London (08:00) or NY (13:00) open | NO TRADE — cancel live limit |
| VETO | VIX > 35 | all SHORT zones NO TRADE |

---

## Stop Loss (v2 — at `/validate`, recompute daily)

```
H4_ATR14 = ATR(14) on trading-day H4 bars only (range >= $1 filter; drop weekend flatline)
D1_ATR14 = ATR(14) on D1 bars

if (0.5 × D1_ATR14) < H4_ATR14 :  SL = H4_ATR14
else                           :  SL = avg(0.5 × D1_ATR14, H4_ATR14)
```
Structural pivot is NO LONGER part of the stop formula (v2 change). Stop is pure volatility (H4
ATR floored, blended with half-D1 ATR only when half-D1 exceeds H4).

## Order Limit — outward offset (v2)

```
offset = max( SL/3 , (10 − entry_confluence_score) × 0.2 × SL )      ← OUTWARD beyond anchor

anchor (with E0 confirmation)    = confirmation candle CLOSE
anchor (no E0 confirmation)      = 50% zone midpoint

Long:  limit_price = anchor − offset
Short: limit_price = anchor + offset
SL price:  long  limit_price − SL  |  short  limit_price + SL
```
Offset always pushes the limit AWAY from spot (more commitment = better fills). Coefficient 0.2
with an SL/3 floor guarantees a minimum buffer even at a perfect score. Backtest confirmed the
outward offset is load-bearing (fill-at-trigger loses; per-trade PF rises with offset).

## Take Profit (v2)

```
TP1 = 2.5R  → MANUAL close (awake → take profit, win the trade)
TP2 = 3.0R  → LIMIT close (asleep → set-and-forget)
BE  = move stop to entry when +1.5R reached
```
TP must land at a structural anchor (prior swing / weekly pivot / Fib extension) — name it, compute R.

## Regime note — ADX(14) D1

Emitted by `weekly_pull.py` as `adx_val`. Informational in v2 (floor fixed at 5.0). Logged as
context: >25 trending (favor continuation) | 20–25 transitional (chop risk) | <20 ranging
(reversal/counter at edges more viable). Operator may tighten manually; not an automatic floor modifier.

## Fake confluence — never double-count (within one score)

- RSI + Stoch + CCI = ONE momentum read.
- Multiple EMAs at one level = ONE EMA signal.
- Two S/R zones at same price = ONE structural zone.
- Two Fib levels near zone = ONE (Fib is not separately scored in v2).
