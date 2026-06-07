---
type: research
updated: 2026-05-31
confidence: medium
tags: [xauusd, entry, trigger, ablation, offset]
related: [independent-signal-results.md, mtf-market-structure.md, ../_INDEX.md]
---

# XAUUSD — Entry Confirmation (H1 trigger ablation)

Script: H1 trigger-ablation sweep (removed in repo cleanup)
Data: TD 6.35yr 2020-01-24 → 2026-05-29 (D1/H4/H1)
Question: the system gates WATCH→ORDER LIMIT on an H1 trigger (pin/engulf/B&R).
That gate was never tested. Does requiring confirmation add edge, or just cut frequency?

Design: cross `trigger_mode` × `entry_mode` to **isolate the trigger from the offset**.
- `trigger_mode`: none (any in-zone bar) | pin | engulf | pin_or_engulf
- `entry_mode`: trigger_fill (fill at bar close) | offset 0.15 | offset 0.25
- g1_mode=either, pivot_n=2, struct_win=60, rr 2.5, be 1.5, cost $0.5.

## Results

| trigger | entry | coef | N | win% | PnL$ | avgR | PF | tr/yr |
|---|---|---|---|---|---|---|---|---|
| none | trigger_fill | – | 107 | 16.8 | −19,576 | −0.16 | 0.69 | 16.9 |
| none | offset | 0.15 | 51 | 17.6 | +12,310 | 0.30 | 1.39 | 8.0 |
| none | offset | 0.25 | 30 | 26.7 | +20,731 | 0.71 | 2.20 | 4.7 |
| **pin** | trigger_fill | – | 78 | 12.8 | −17,929 | −0.21 | 0.65 | 12.3 |
| **pin** | offset | 0.15 | 37 | 21.6 | +17,052 | 0.51 | 1.76 | 5.8 |
| **pin** | offset | 0.25 | 22 | 36.4 | +29,024 | 1.25 | **3.38** | 3.5 |
| engulf | trigger_fill | – | 60 | 11.7 | −16,678 | −0.26 | 0.52 | 9.4 |
| engulf | offset | 0.25 | 16 | 37.5 | +20,186 | 1.25 | 3.06 | 2.5 |
| pin_or_engulf | offset | 0.25 | 22 | 36.4 | +29,024 | 1.25 | 3.38 | 3.5 |

## Findings

**1. The trigger is NOT a directional edge by itself.** At `trigger_fill` every
trigger mode loses (PF 0.52–0.69), no better than no-trigger (0.69). Confirms
Phase 0b: H1 technicals carry no standalone forward edge. A pin/engulf alone is
not a reason to enter.

**2. The trigger IS a quality filter — but only in combination with the offset.**
Hold entry at offset 0.25: requiring a pin lifts PF 2.20→**3.38**, win% 26.7→36.4,
avgR 0.71→1.25, at the cost of 30→22 fills (−27%). The pin removes ~8 low-quality
fills/6yr and meaningfully raises per-trade payoff. Same direction at offset 0.15
(PF 1.39→1.76).

**3. The offset is still the dominant lever.** Hold trigger=pin: trigger_fill 0.65
→ offset0.15 1.76 → offset0.25 3.38. Monotonic. The earlier funnel finding holds:
filling beyond the zone extreme is what creates the edge; filling at the trigger
bar destroys it.

**4. Engulfing adds nothing over pin.** Engulf alone = fewer fills (16 vs 22),
similar PF (3.06 vs 3.38). `pin_or_engulf` is **identical** to `pin` at offset 0.25
— every engulf fill in this sample was already a pin fill or added no distinct
trade. Keep **pin as the single primary pattern**; do not split engulf out as a
separate scored trigger.

**5. Break-and-retest not modeled.** B&R is a multi-bar pattern; the backtest only
models single-bar pin/engulf. Untested — treat as discretionary at /validate only.

## Decision

- **Keep the H1 trigger gate as-is (pin, in-zone, with outward offset).** Data
  supports it: pin+offset is the highest-quality cell tested.
- **Reject "H1-trigger-only entry"** (the _HOT note after Setup A). trigger_fill =
  PF 0.65, a loser. Setup A missing its fill (offset limit beyond realized high) is
  the *expected cost* of the edge, not a bug to fix by dropping the offset.
- Engulf/B&R may stay as discretionary triggers at /validate but earn no separate
  weight and no code change.

## Caveats

- N small (16–30 trades over 6.35yr). PF gaps are directionally clear but not
  rigorously significant; this is a low-frequency method (~2–4 quality trades/yr).
- offset 0.25 vs 0.15 is a frequency/quality dial: 0.15 ≈ 5.8 tr/yr @ PF 1.76;
  0.25 ≈ 3.5 tr/yr @ PF 3.38. Live uses 0.25 (D014 — quality over frequency).
