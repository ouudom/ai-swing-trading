import os
DATE="2026-06-18"; WK="2026-W25"
os.makedirs("forecasts/daily",exist_ok=True)

# (instrument, active_zone, v3_clear, body) ; zones list of (label,dir,verdict,reason)
DATA = {
"xauusd": dict(active="NONE", snap="Spot $4263.82 | DFII10 2.14% (base 2.16, drift -0.020) | H4 ATR $37.99 | D1 ATR $123.05 (med 101.71, not compressed) | VIX 16.41 | ADX(14) D1 43.9 (trending)",
  zones=[("PRIMARY","SHORT","NO_TRADE","Spot 4263.82 sits ~96 below the 4360-4390 short zone — no approach to resistance, no E0 bear confirmation. Zone intact, remains PENDING."),
         ("SECONDARY","SHORT","NO_TRADE","Spot ~186 below the 4450-4485 zone. Not in play, no E0. PENDING.")],
  hardblock=None),
"eurusd": dict(active="NONE", snap="Spot 1.14629 | DGS2 4.05% (flat vs base) | DXY 1d jump +0.617 | H4 ATR 0.00257 | D1 ATR 0.00623 (med 0.00555, not compressed) | VIX 16.41 | ADX(14) D1 22.5 (calm)",
  zones=[("PRIMARY","LONG","NO_TRADE","DXY 1d jump +0.617 (>0.5) AGAINST the long = macro-flip block; spot 1.14629 also dipped below the 1.150-1.152 support with no E0 bull turn. V1b intact (threshold 1.14950, only one H4 close below). PENDING — not invalidated."),
         ("SECONDARY","SHORT","NO_TRADE","Spot ~0.0155 below the 1.1618-1.164 short zone — far from resistance, no E0 bear. PENDING.")],
  hardblock=None),
"gbpusd": dict(active="NONE", snap="Hard-block day — confluence not scored (BoE decision).",
  zones=[("PRIMARY","SHORT","NO_TRADE","BoE MPC decision today (own central bank) = V3 HARD BLOCK all day; D028 forward-carry carve-out does NOT relax own-CB-today. PENDING."),
         ("COUNTER","LONG","NO_TRADE","BoE own-CB-today V3 HARD BLOCK. PENDING.")],
  hardblock="BoE MPC 2026-06-18 (own central bank)"),
"eurgbp": dict(active="NONE", snap="Hard-block day — confluence not scored (BoE / GBP leg).",
  zones=[("PRIMARY","LONG","NO_TRADE","BoE MPC decision today hits the GBP leg = V3 HARD BLOCK for the cross. PENDING."),
         ("SECONDARY","SHORT","NO_TRADE","BoE own-CB (GBP leg) V3 HARD BLOCK. PENDING.")],
  hardblock="BoE MPC 2026-06-18 (GBP leg)"),
"audusd": dict(active="NONE", snap="Spot 0.70119 | DGS2 4.05% (flat) | H4 ATR 0.00193 | D1 ATR 0.00544 (med 0.00562, compressed) | VIX 16.41 | ADX(14) D1 30.5 (trending)",
  zones=[("PRIMARY","SHORT","NO_TRADE","Spot 0.70119 sits ~0.0053 below the 0.7065-0.711 short zone — no approach to resistance, no E0 bear. PENDING."),
         ("COUNTER","LONG","NO_TRADE","Spot 0.70119 just above the 0.698-0.700 zone top, no E0 bull turn; D1 ADX 30.5 (>30) flags trend risk against a counter-fade. PENDING.")],
  hardblock=None),
"nzdusd": dict(active="COUNTER", snap="Spot 0.57638 | DGS2 4.05% (flat) | H4 ATR 0.00205 | D1 ATR 0.00561 (med 0.00551, not compressed) | VIX 16.41 | ADX(14) D1 21.3 (calm)",
  zones=[("PRIMARY","SHORT","NO_TRADE","Spot ~0.0091 below the 0.5855-0.589 short zone — far from resistance, no E0 bear. PENDING."),
         ("COUNTER","LONG","NO_TRADE","Spot 0.57638 is INSIDE the 0.575-0.579 zone and V1b is intact (thr 0.57460), but the entry trigger is absent: last closed 1H (09:00) is a doji at the lows (body -0.00004) after a -0.00166 down bar — no bullish reversal. H4 -DI 29.8 >> +DI 16.7 = momentum still falling INTO the zone. EC well below 5.0 (E0 absent; only E2 band-touch + E3 ADX<25 score). NO TRADE — wait for a confirmed bullish turn. PENDING.")],
  hardblock=None),
"usdcad": dict(active="NONE", snap="Spot 1.41236 | DGS2 4.05% (flat) | H4 ATR 0.00242 | D1 ATR 0.00589 (med 0.00488, not compressed) | VIX 16.41 | ADX(14) D1 39.3 (strong trend)",
  zones=[("PRIMARY","LONG","NO_TRADE","Spot 1.41236 has run ~0.0249 ABOVE the 1.383-1.3875 buy-dip zone (strong uptrend, D1 ADX 39.3) and never pulled back — no entry available at the zone. PENDING (zone intact but stale vs price).")],
  hardblock=None),
"usdchf": dict(active="NONE", snap="Hard-block day — confluence not scored (SNB assessment).",
  zones=[("PRIMARY","SHORT","NO_TRADE","SNB quarterly assessment today (own central bank) = V3 HARD BLOCK all day. PENDING.")],
  hardblock="SNB quarterly assessment 2026-06-18 (own central bank)"),
"usdjpy": dict(active="NONE", snap="JPY trio NO ZONES all week (standing W25 rule) — not validated.",
  zones=[], hardblock="JPY trio NO ZONES — BoJ 06-16 + active MoF intervention regime (W25)"),
"eurjpy": dict(active="NONE", snap="JPY trio NO ZONES all week (standing W25 rule) — not validated.",
  zones=[], hardblock="JPY trio NO ZONES — BoJ 06-16 + active MoF intervention regime (W25)"),
"gbpjpy": dict(active="NONE", snap="JPY trio NO ZONES all week; also BoE decision today.",
  zones=[], hardblock="JPY trio NO ZONES (W25) + BoE MPC 06-18 (GBP leg)"),
}

for inst,d in DATA.items():
    os.makedirs(f"forecasts/daily/{inst}",exist_ok=True)
    v3_clear = "false" if d["hardblock"] else "true"
    fm = f"""---
type: daily_validation
instrument: {inst}
date: {DATE}
week: {WK}
active_zone: {d['active']}
v1_structure_intact: true
v1b_intact: true
v3_news_clear: {v3_clear}
vix_veto: false
vix_stale: false
reforecast_action: NONE
reforecast_triggers: []
entry_confluence_score: 0.0
order_limit: NO_TRADE
limit_direction: N/A
vix_now: 16.41
---

# Validation — {DATE} ({inst}, {WK})

Automated hourly run (10:1x UTC). **Verdict: NO TRADE — 0 order limits.**

## Market Snapshot
{d['snap']}
"""
    if d["hardblock"]:
        fm += f"\n## Hard Block\n{d['hardblock']} → all zones NO TRADE regardless of confluence (D028 own-CB-today / standing-rule carve-out does not relax).\n"
    fm += "\n## Per-Zone Verdicts\n"
    if not d["zones"]:
        fm += "No PENDING zones this week.\n"
    else:
        for lab,dirn,verdict,reason in d["zones"]:
            fm += f"\n### {lab} {dirn} — ❌ {verdict}\n{reason}\n"
    fm += f"\n## Result\nNO TRADE on all zones. No invalidations — every zone remains PENDING/intact. Next D1 close {DATE} 24:00 UTC.\n"
    with open(f"forecasts/daily/{inst}/{DATE}.md","w") as f: f.write(fm)
    print("wrote", f"forecasts/daily/{inst}/{DATE}.md")
