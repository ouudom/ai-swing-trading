---
type: daily_validation
instrument: usdcad
date: 2026-06-12
week: 2026-W24
active_zone: NONE
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto: false
vix_stale: true
reforecast_action: WARN_LOG
reforecast_triggers: []
e0_entry_confirmation: false
e1: false
e2: false
e3: false
e4: false
e5: true
entry_confluence_score: 1.0
zone_confluence_score: 7.0
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0
h4_atr: 0.00234
d1_atr: 0.00546
d1_atr_compressed: false
sl_distance: 0.00254
offset: 0
order_limit: NO_TRADE
limit_price: 0
limit_direction: N/A
limit_expires: 2026-06-12 21:00 UTC
tp1_price: 0
tp2_price: 0
be_trigger_r: 1.5
---

# USDCAD Daily Validation — 2026-06-12 (Fri, W24)

Spot 1.39825. CB calendar clear. No BoC/CAD tier-1 today. US2Y drift 0 (flipped polarity, n/a).

> [!warning] **Weekly abort condition MET (stale data caveat): VIX last close 22.22 > 20**
> (FRED 06-10; 06-11 not yet posted → vix_stale=true). W24 forecast: "Abort long if VIX closes
> >20 (fade-USD flip)." VIX>20 = SHORT-bias regime against the LONG zone. Conservative: NO TRADE
> today; if VIX holds >20 at next print, INVALIDATE the zone at /weekly.

| Zone | Verdict | EC | Why |
|---|---|---|---|
| PRIMARY LONG 1.3885–1.3905 (7.0) | ❌ NO TRADE | ~1.0 | VIX>20 abort (above) + 78 pips OTM + D1 RSI 74.1 overbought + ADX 33.2 (E3 ✗) |

V1/V1b intact (price extended ABOVE zone, not breached against). Zone receding — re-anchor candidate.
