---
type: system
updated: 2026-06-11
confidence: high
tags: [usdjpy, confluence, scoring, zones]
related: [usdjpy_profile, signal-results, constitution]
---

# USDJPY — Zone Confluence (R1) + Entry Confluence (R2) — ACTIVE

**Direction-aware system** — first asymmetric pair. LONG zones score drift-continuation
criteria (compression/dip); SHORT zones score D1/H4 oscillator-extreme criteria.
H1-only shorts are PROHIBITED (anti-edge t=−3.3). Evidence: [[signal-results]].
Max 10, floor 5.0, ≤3 zones/wk, ≤1 counter (counter = SHORT here — against D1 drift).

## R1 — Zone Confluence (weekly)
| # | Criterion | Wt | Evidence (t) |
|---|---|---|---|
| Z1 | Structural S/R zone (D1/H4 level, prior reaction) | 2.0 **MAND** | — |
| Z2 | **Side engine** — LONG: D1 TTM squeeze on or H4/H1 ATR pctile<0.2 (calm) · SHORT: ≥2 of D1 RSI>65 / H4 CCI>+100 / H4 Keltner-high | 2.5 | 3.27/4.51/3.22 · 3.11/2.66/2.35 |
| Z3 | DXY 20d slope aligned (up=long zone / down=short zone) | 2.0 | 2.21/1.73 |
| Z4 | LONG only: dip structure — zone at/near 20d low within intact D1 uptrend | 1.0 | H1 3.15, H4 1.85 |
| Z5 | D1 trigger pattern (engulfing / pin toward zone dir) | 1.0 | engulf 1.43. **PSAR dropped** — 2015+ rescan t≈0.2 (dead); prior 2.36 was window-specific, did not hold out-of-sample (see indicator-backtest-2026-06) |
| Z6 | LONG only: big-figure confluence (x.00 within 15 pips) | 1.0 | D1 1.60, H4 1.39 (short = anti) |
| Z7 | Not extended: ADX<25 or zone is a pullback, not extension chase | 0.5 | C26 anti −3.3/−3.4 |

**Vetoes / caps**
- **BoJ decision day or active MoF jawboning → HARD BLOCK** (no zone publishes).
- **LONG zone ≥158 at fresh multi-decade highs → conviction cap MEDIUM** (MoF regime).
- **No H1-only SHORT zones** — shorts require D1/H4 extreme evidence (Z2 short leg).
- Turn-of-month (day ≥26) LONG zones → −0.5 (D1 anti −2.52).
- NO VIX veto, NO VIX score (washout). NO DXY-jump block (anti).

## R2 — Entry Confluence (daily, per zone)
| # | Criterion | Wt |
|---|---|---|
| E0 | 1H close — SHORT (fade): **RSI-reclaim** back through 65 (backtest avgR +0.049, D027 pending) / pin/engulf · LONG (drift): CONTINUATION engulf/pin toward drift, NOT reclaim · 15M CHoCH toward zone dir | 3.0 |
| E1 | Side engine still live — LONG: squeeze/calm still on · SHORT: H4 oscillator still extreme | 2.5 |
| E2 | DXY 20d slope still aligned | 1.5 |
| E3 | LONG only: entry window in NY session 12–16 UTC (H1 drift t=4.71; short = anti −3.97) | 1.0 |
| E4 | Zone structure intact (no D1 close through zone) | 1.0 |
| E5 | Not extended at entry (ADX<25 or pullback entry, not breakout chase) | 1.0 |

Floor 5.0. E0 absent → no order (anchor rules in constitution).

## V1b (intraday invalidation)
2 consecutive H4 closes **>0.04 (4 JPY pips)** past zone extreme → invalidate, cancel limit.
`bash scripts/pyrun.sh scripts/check_v1b.py --instrument usdjpy --direction LONG --zone-top 159.50 --zone-bottom 159.00 --buffer 0.04`
⚠ Intervention days gap through V1b — BoJ/MoF hard block exists precisely for this.
