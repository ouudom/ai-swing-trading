---
type: setup
updated: 2026-06-13
confidence: high
tags: [research, backtest, indicators, confluence]
related: [confluence_criteria, calibration, backtest_signals]
---

# Indicator Backtest — 8 New Indicators (2026-06-13)

**Question:** the D025 round made 8 indicators *computed* instead of *eyeballed*. Do they have
edge? Should confluence scoring change?

**Method:** `scripts/backtest_signals.py --instrument all --tf D1 H4 --since 2015-01-01`. Forward
return D1 fwd=5 (1wk), H4 fwd=6 (24h). Edge = win% over directional baseline. t = significance.
N ≈ 600–2300/signal. **Independent forward-return test — NOT the live zone ledger (that's n=1).**

> [!note] This validates *existing* rubric weights — it does not propose new ones. Signals already
> referenced in `confluence_criteria`. Verdict below = keep / cut / flip, per pair.

---

## t-stat matrix — D1 (|t|>2.0 sig, >2.6 strong; sign = edge in stated direction)

| code | signal | dir | xau | eur | gbp | eurg | aud | nzd | ucad | uchf | ujpy | eurj | gbpj |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| A8  | Stoch<20  | LNG | -0.2 | **3.8** | **3.5** | **3.1** | 0.8 | 0.2 | -0.3 | 2.1 | 1.8 | **2.8** | 0.2 |
| A7  | Stoch>80  | SHT | -0.1 | 2.4 | 1.1 | 1.0 | 0.7 | 1.2 | 1.8 | 0.2 | 0.5 | 1.5 | 0.3 |
| A10 | W%R<-80   | LNG | 0.1 | **4.3** | **3.7** | **3.0** | 0.2 | -0.6 | -1.5 | 2.4 | 1.5 | 0.9 | -0.4 |
| A9  | W%R>-20   | SHT | -0.1 | **3.1** | 1.6 | 1.7 | 1.1 | 1.0 | 1.4 | -0.3 | 0.8 | 2.2 | 0.3 |
| A12 | CCI<-100  | LNG | 0.8 | -0.4 | -0.7 | **4.5** | 0.9 | 0.9 | -1.7 | 0.8 | 1.1 | 1.8 | -0.6 |
| A11 | CCI>100   | SHT | 0.1 | 0.7 | -1.8 | **2.9** | 1.6 | 0.3 | 1.2 | -1.2 | 1.7 | -0.4 | 1.3 |
| B9  | Keltner<lo | LNG | 1.3 | 1.4 | 2.5 | **3.9** | 0.7 | 0.5 | 0.9 | **2.6** | 2.3 | **3.2** | 0.0 |
| B10 | Keltner>hi | SHT | -1.6 | 1.4 | **3.6** | 0.5 | 1.7 | -0.6 | 1.0 | 0.3 | 1.7 | **2.7** | 1.5 |
| B11 | TTM squeeze | LNG | **-3.0** | -0.2 | 1.6 | 2.0 | -1.6 | **3.1** | -1.1 | -0.1 | 0.4 | 2.3 | 0.8 |
| C9  | Donchian↑  | LNG | 0.9 | -1.3 | -1.0 | -1.4 | -1.6 | -1.7 | -0.2 | 0.9 | -0.3 | -0.6 | 0.3 |
| C10 | Donchian↓  | SHT | -0.4 | -1.1 | -1.8 | **-3.5** | -1.2 | -0.7 | 1.0 | -1.0 | -1.1 | -1.6 | -0.4 |
| C20 | Supertrend↑ | LNG | 0.0 | **-2.8** | -1.7 | -2.2 | -0.6 | 0.4 | -0.4 | -1.9 | -0.2 | -1.3 | -2.3 |
| C21 | Supertrend↓ | SHT | 0.0 | **-2.8** | -1.6 | -2.2 | -0.6 | 0.3 | -0.5 | -1.7 | -0.5 | -1.4 | -2.5 |
| C22 | PSAR bull  | LNG | 0.8 | 1.4 | 1.7 | -1.8 | -0.5 | -0.7 | 0.6 | -1.1 | 0.2 | -1.7 | -0.1 |
| C23 | PSAR bear  | SHT | 0.9 | 1.3 | 1.7 | -1.5 | -0.5 | -0.6 | 0.5 | -1.0 | 0.2 | -1.7 | -0.1 |

## t-stat matrix — H4

| code | signal | dir | xau | eur | gbp | eurg | aud | nzd | ucad | uchf | ujpy | eurj | gbpj |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| A8  | Stoch<20  | LNG | **3.4** | 1.3 | 1.3 | 0.2 | 2.3 | 2.3 | 2.5 | 1.0 | -0.5 | -0.6 | -0.5 |
| A7  | Stoch>80  | SHT | -0.6 | 2.5 | 1.3 | **4.0** | 1.5 | 0.7 | 0.1 | -0.6 | -0.3 | 2.2 | **4.2** |
| A10 | W%R<-80   | LNG | **3.5** | 0.8 | 1.7 | 2.1 | 2.5 | 2.0 | 1.9 | 0.2 | -1.3 | -0.4 | -1.2 |
| A9  | W%R>-20   | SHT | -2.2 | 2.1 | 1.0 | **3.4** | 1.7 | 1.9 | 0.6 | 0.4 | -0.5 | 1.7 | **3.8** |
| A11 | CCI>100   | SHT | -1.7 | **2.9** | 1.8 | 1.6 | **3.1** | **2.6** | 2.5 | -0.1 | 1.5 | 2.4 | **6.5** |
| A12 | CCI<-100  | LNG | 0.5 | 1.3 | 0.4 | 1.2 | **2.8** | 2.2 | -0.8 | 1.1 | -0.6 | **2.8** | 0.1 |
| B9  | Keltner<lo | LNG | 1.9 | 1.7 | 2.0 | 1.9 | **3.7** | 2.3 | 2.0 | -0.2 | 0.7 | 2.5 | 2.4 |
| B10 | Keltner>hi | SHT | -0.1 | **3.1** | 0.8 | 2.1 | 1.8 | 2.1 | 1.1 | **-2.8** | 1.1 | **3.4** | **6.0** |
| B11 | TTM squeeze | LNG | -0.5 | 2.0 | -1.8 | 0.2 | 0.4 | **2.8** | -1.5 | -0.6 | 1.0 | 2.4 | 1.0 |
| C9  | Donchian↑  | LNG | 0.4 | -1.3 | -1.1 | -1.6 | -1.1 | -1.2 | -1.0 | -0.1 | 0.8 | -0.9 | **-3.5** |
| C10 | Donchian↓  | SHT | -1.1 | -1.6 | -0.3 | -2.8 | -1.3 | -1.5 | -0.6 | 1.8 | 0.5 | -0.4 | -0.4 |
| C20 | Supertrend↑ | LNG | 0.9 | -0.1 | -2.4 | **-3.8** | -1.3 | -1.4 | -0.5 | -0.2 | 0.1 | -1.6 | -2.2 |
| C21 | Supertrend↓ | SHT | 1.0 | -0.0 | -2.4 | -3.6 | -1.3 | -1.3 | -0.7 | -0.3 | 0.4 | -1.6 | -2.5 |
| C22 | PSAR bull  | LNG | 1.1 | -1.2 | 0.3 | -1.1 | -0.9 | -1.5 | -0.6 | 0.1 | -0.2 | -1.0 | -2.1 |
| C23 | PSAR bear  | SHT | 1.2 | -1.0 | 0.5 | -0.9 | -1.0 | -1.5 | -0.6 | 0.1 | -0.2 | -1.1 | -2.2 |

---

## Per-indicator verdict

| Indicator | Verdict | Detail |
|---|---|---|
| **Stochastic** | ✅ KEEP | Oversold-long edge on EUR/GBP/EURGBP/EURJPY D1 (t 2.8–3.8); gold H4 oversold (3.4). Overbought-short weaker. |
| **Williams %R** | ✅ KEEP | Mirrors Stoch, slightly stronger long side (eurusd D1 4.3). Cross-JPY short on H4 (gbpj 3.8). |
| **CCI** | ✅ KEEP (H4) | **Best H4 mean-rev signal** — gbpjpy 6.5, audusd 3.1, eurusd 2.9. D1 only eurgbp. Add weight on H4. |
| **Keltner** | ✅ KEEP | Band-tag fade works broadly H4 (gbpjpy 6.0, eurjpy 3.4, eurusd 3.1). Strong rubric backer. |
| **TTM squeeze** | ⚠️ MARGINAL | Mostly insignificant; nzdusd H4 3.1 the only clean hit. **Anti-edge on gold D1 (-3.0).** Keep as context, low weight. |
| **Donchian** | ❌ CUT/FLIP | Breakout-continuation is **anti-edge on FX** (negative everywhere). FX fades breakouts. Do not score as continuation. |
| **Supertrend** | ❌ CUT (FX) | Trend-follow **anti-edge on FX** (eurusd -2.8, eurgbp -3.8). Neutral on gold. Remove from FX confluence. |
| **PSAR** | ❌ CUT | No edge any pair/TF (|t|<1.8 except wrong-way eurgbp/gbpj). Dead weight. |

## Headline findings

1. **Mean-reversion oscillators confirmed — rubric was right.** Stoch / W%R / CCI / Keltner all
   carry real edge on the mean-reversion FX pairs, exactly where `confluence_criteria` scores
   them. The eyeball-→-computed upgrade hardens a *validated* edge, not a guess.
2. **Trend-follow trio (Donchian / Supertrend / PSAR) is anti-edge on FX — and the rubric already
   knows.** FX mean-reverts at the 1wk/24h horizon → breakout-continuation loses. Cross-check:
   every FX `confluence_criteria.md` *already* lists these as "measured anti-edges that must NEVER
   score" (audusd, eurusd, eurgbp, gbpusd, nzdusd, usdcad, eurjpy, gbpjpy). This backtest
   **re-confirms** that exclusion on fresh 2015+ data — no leak. **One exception:** usdjpy Z5
   scores "PSAR flip toward zone dir" 1.0 (cited PSAR-bear t=2.36) — my run shows usdjpy D1 PSAR
   t≈0.2 (dead). That single weight looks stale → audit.
3. **Gold ≠ FX, confirmed.** xauusd D1 oscillators all dead (momentum); only H4 deep-oversold
   long works (Stoch 3.4 / W%R 3.5). Never score gold D1 overbought as a short.
4. **CCI is the underused winner on H4** — strongest single mean-rev signal on cross-JPY and
   commodity pairs. Worth promoting in H4 Entry Confluence.
5. **USD-base pairs (usdchf/usdjpy) weakest** — thin oscillator edge, matches their "macro-light,
   weakest-edge" character note. usdjpy oscillators near-dead → keep carry-drift model, not fades.

## Recommended actions — verified against live rubrics 2026-06-13

Three candidate fixes proposed; on cross-check against the actual `confluence_criteria.md` files,
**only one was a real gap.** The other two were already handled correctly (good news).

- ✅ **Stoch/W%R/Keltner weights** — validated, no change.
- ⏭️ **CCI "promote"** — **MOOT.** Already a core Z2 engine wherever it has edge: eurusd Z2 (CCI
  +4.0pp t=2.84), audusd/nzdusd/gbpjpy Z2, eurjpy Z4. The "underweight 3×" claim was a stale grep
  miscount. Correctly weighted — no change.
- ⏭️ **Gold oscillator gating** — **MOOT.** xauusd Z1–Z7 + E0–E5 score **zero** oscillators
  (real-yield / DXY / EMA / MTF / VP only). Oscillators are a regime *note*, never confluence
  points. Nothing to gate.
- ✅ **APPLIED — usdjpy Z5 PSAR dropped.** Only real fix. Z5 cited "PSAR bear 2.36"; 2015+ rescan
  shows D1 PSAR t≈0.2 (dead, did not hold out-of-sample). Rewrote Z5 to "engulfing / pin toward
  zone dir", PSAR removed.
- ⏭️ **Donchian/Supertrend/PSAR** — already excluded as measured anti-edges in every FX rubric;
  re-confirmed on fresh data, leave excluded.
- ⏭️ **TTM squeeze** — keep as regime context, do not raise weight.

_Source raw scans: `wiki/research/{pair}/signal-scan-raw.txt` (regenerated 2026-06-13)._
