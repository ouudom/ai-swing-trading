---
type: daily_validation
instrument: usdchf
date: 2026-06-12
week: 2026-W24
active_zone: PRIMARY
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto: false
vix_stale: true
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: true
e1: false
e2: true
e3: false
e4: true
e5: true
entry_confluence_score: 6.5
zone_confluence_score: 7.5
e0_pattern: 1H_pin
anchor_type: confirmation_close
anchor_price: 0.79647
h4_atr: 0.00221
d1_atr: 0.0053
d1_atr_compressed: false
sl_distance: 0.00243
offset: 0.0017
order_limit: PLACED
limit_price: 0.79477
limit_direction: BUY
limit_expires: 2026-06-12 21:00 UTC
tp1_price: 0.80085
tp2_price: 0.80206
be_trigger_r: 1.5
---

# USDCHF Daily Validation — 2026-06-12 (Fri, W24)

Spot 0.79672. CB calendar clear — **SNB 06-18 is NEXT week** (outside 2d window; zones expire
tonight anyway). UMich 14:00 caution. No VIX gate/score (washout). DXY 99.811, 20d slope +0.93
RISING = live macro WITH the long. US2Y drift 0.

**Zone action:** price dipped into PRIMARY LONG 0.79450–0.79600 yesterday (D1 close 0.79516
INSIDE zone) and bounced. E0 = bullish 1H pin 06:00 UTC (low 0.79598 tagged zone top, tail
4.9p ≥ 2.5× body 1.5p), confirmed on close 0.79647. London 07–09 UTC = best long-fade window.

| Zone | Verdict | EC | Detail |
|---|---|---|---|
| PRIMARY LONG 0.7945–0.7960 (7.5) | ✅ ORDER LIMIT | **6.5/10** | E0 ✓3.0 (1H pin) · E1 ✗ (H1 W%R −69, RSI2 64 — washout resolved) · E2 ✓1.5 (DXY slope rising) · E3 ✗ (no squeeze, H1 ATR pctile 0.94) · E4 ✓1.0 (ADX 22.6) · E5 ✓1.0. Floor 6.5 (ADX transitional) — **marginal pass at floor** |
| COUNTER SHORT 0.8005–0.8030 (5.5) | ❌ NO TRADE | ~2.0 | 38 pips OTM, no H1 OB cluster, no E0; SNB-band MEDIUM cap |

```
USDCHF ORDER LIMIT: BUY 0.79477 | SL 0.79234 | TP1 2.5R 0.80085 (manual) | TP2 3.0R 0.80206 (limit) | BE @1.5R | expires 2026-06-12 21:00 UTC
Entry Confluence: 6.5/10 (E0:✅ E1:❌ E2:✅ E3:❌ E4:✅ E5:✅)
Anchor: confirmation close 0.79647 | SL 0.00243 = avg(0.5×D1 0.00265, H4 0.00221) | offset 0.00170 = (10−6.5)×0.2×SL | limit inside zone ✓
"If price reaches 0.79477, order triggers. Cancel if not hit by 21:00 UTC."
```

> [!note] Structural TP anchor = 20d high **0.80063 = 2.41R** from limit — sits just BELOW TP1
> (2.5R). Operator option: take full exit at the structural anchor instead of TP1/TP2 ladder.

> [!note] FX netting ledger: INDEPENDENT (no other live FX orders). Risk $2000. Friday order —
> expires 21:00 UTC, no weekend carry of the unfilled limit.
