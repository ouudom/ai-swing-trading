# E0 Trigger Bake-Off — is there a better entry confirmation?

Identical Tier-2 sim (oscillator-extreme universe, s/3 offset limit, SL=ATR, 2.5R); only the GATE changes. Compare avgR / PF / fill% per trigger vs the current pin/engulf E0 and the un-gated LIMIT_all. Higher avgR at usable fill% = better E0. FX mean-rev reading; xauusd & usdjpy excluded from POOLED.

## Verdict — YES: oscillator RECLAIM beats pin/engulf. Current E0 is one of the weaker gates.

Pooled FX mean-rev avgR / PF (confirm-then-enter, trigger within 6 bars of the extreme):

| gate | fill% | avgR | PF | vs current |
|---|--:|--:|--:|---|
| **rsi_reclaim** (RSI back through 35/65) | 26% | **+0.104** | **1.15** | **+0.066 R, best** |
| band_reclaim (close re-enters Keltner) | 34% | +0.068 | 1.10 | +0.030 R |
| stoch_reclaim (Stoch back through 20/80) | 40% | +0.055 | 1.08 | +0.017 R |
| micro_bos (close > prior bar high) | 62% | +0.053 | 1.08 | +0.015 R |
| **pin_engulf — CURRENT E0** | 69% | +0.038 | 1.05 | baseline |
| close_strong (close top-third) | 82% | +0.034 | 1.05 | −0.004 R |
| LIMIT_all (no trigger gate) | 87% | +0.036 | 1.05 | — |

**Per-pair best trigger:** rsi_reclaim wins **7 of 11** (eurusd, audusd, nzdusd, usdchf, usdjpy,
eurjpy, gbpjpy); band_reclaim wins 2 (xauusd, usdcad); pin_engulf wins **only gbpusd**.

**Findings:**
1. **The current pin/engulf E0 barely beats placing a raw limit** (+0.038 vs LIMIT_all +0.036). It
   fires on 69% of setups — too loose, mostly noise. It is near the *bottom* of the trigger ranking.
2. **An oscillator RECLAIM is a much stronger confirmation.** RSI crossing back up through 35
   (down through 65) nearly **3× the per-trade R** (+0.104 vs +0.038) and PF 1.15 vs 1.05 — because
   it requires the momentum to actually turn, not just a single candle shape. Costs frequency
   (26% fill) but that's the right trade: E0 is a *quality* gate.
3. **band_reclaim** (price closing back inside the Keltner band) is the best complement — wins the
   two pairs RSI-reclaim doesn't, including gold (the one continuation-model pair here).
4. close_strong / micro_bos / any_combo ≈ pin/engulf — loose, low selectivity, little lift.

## Recommendation (research-grade — do NOT rewrite the rubric yet)

**Strong candidate E0 redefinition:** primary trigger = **oscillator reclaim** (RSI back through the
35/65 threshold, and/or Stoch back through 20/80, and/or close re-entering the Keltner band on the
fade side), confirmed on the 1H close; keep **pin/engulf as a secondary** trigger (still positive,
and the best gate on gbpusd). This matches the system's mean-reversion thesis better than a raw
candle shape — you enter when momentum has demonstrably turned, not on the first wick.

**Caveats before any change:** forward-return sim, in-sample (2015+), unfiltered universe (every
extreme, not the confluence-gated zones the system trades); R magnitudes small. The *ranking* is
robust and mechanistically sensible, but validate on (a) the confluence-gated subset and (b) the
live zone ledger before editing E0 in `constitution.md` / `confluence_criteria.md`. gold keeps its
continuation E0 — this fade-reading does not apply to xauusd.

## 15M test — reclaim edge does NOT replicate; keep E0 on 1H

Ran `--tf 15M` (windows ×4 to hold wall-clock equal). Only 5 pairs have usable 15M depth
(xauusd 2020+, usdchf/usdjpy/eurjpy/gbpjpy 2024+); the 6 USD majors keep ~11 days only → skipped.

Pooled (usdchf/eurjpy/gbpjpy) avgR: band_reclaim +0.058, rsi_reclaim +0.049, pin/engulf +0.039,
LIMIT_all +0.036 — the triggers **compress**; reclaim's big 1H edge (+0.104) mostly collapses. Per
pair it even flips: **usdchf rsi_reclaim → −0.002** (was +0.105 on 1H), **eurjpy pin/engulf +0.058
wins** (1H: rsi won). Only **gbpjpy** keeps a strong reclaim edge on both TF (15M band +0.139).

Why: 15M is noisier (smaller ATR, micro-wiggle triggers). **Caveat:** 15M sample is only 2024+
(~2.4yr) vs 1H 2015+ (~11yr) — shorter/recent period, not apples-to-apples. Either way: no reason to
move E0 to 15M, clear reason to keep it on **1H close**. 15M useful as a fast-fill leg on gbpjpy only.

## Per-pair suggested E0 (1H close; from per-pair avgR, best marked in bake-off)

Timeframe = **1H close** for every pair (what was tested). 15M CHoCH leg untested (thin data) —
leave as-is. avgR shown for the top candidates per pair.

| pair | character | **E0 primary** | E0 secondary | avoid | note |
|---|---|---|---|---|---|
| eurusd | mean-rev | **RSI-reclaim** (35/65) +0.143 | band-reclaim +0.071 | — | reclaim dominates |
| audusd | mean-rev | **RSI-reclaim** +0.118 | band-reclaim +0.089 | — | |
| nzdusd | mean-rev | **RSI-reclaim** +0.127 | stoch-reclaim +0.081 | close-strong | |
| eurjpy | mean-rev | **RSI-reclaim** +0.101 | close-strong +0.043 | — | |
| gbpjpy | extension-fade | **RSI-reclaim** +0.091 | band-reclaim +0.062 | **pin/engulf (−0.024)** | drop pin here |
| usdchf | mean-rev | **RSI-reclaim** +0.105 | pin/engulf +0.087 | **band (−0.003)** | no band on chf |
| usdcad | mean-rev | **band-reclaim** +0.107 | micro-BOS +0.090 / RSI +0.076 | — | band wins here |
| gbpusd | mean-rev | **pin/engulf** +0.143 | band-reclaim +0.106 | — | only pair pin wins |
| usdjpy | asymmetric | SHORT: **RSI-reclaim** +0.049 · LONG: keep drift-continuation (engulf toward drift) | — | stoch-reclaim (−0.029) | fade reading = SHORT leg only |
| xauusd | momentum | **keep continuation E0** (pin/engulf TOWARD zone) | — | fade triggers | bake-off is fade-reading; N/A to gold — needs own continuation study |

**Default rule of thumb:** RSI-reclaim primary everywhere **except** gbpusd (pin/engulf) and usdcad
(band-reclaim); gold/usdjpy-long keep continuation. Secondary trigger = the pair's 2nd-best column
(diversifies when the primary doesn't fire). All 1H close.

_Still research-grade — validate on gated subset + live ledger before editing the rubric._

_Script: `scripts/backtest_e0_variants.py`. Raw per-pair tables below._

```
================================================================
POOLED — FX mean-rev (excl xauusd, usdjpy)
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET          40638   100%    29.1   +0.013    1.02
LIMIT_all       35520    87%    29.7   +0.036    1.05
pin_engulf      28010    69%    29.8   +0.038    1.05  ← current
rsi_reclaim     10455    26%    31.7   +0.104    1.15
stoch_reclaim   16159    40%    30.2   +0.055    1.08
band_reclaim    13969    34%    30.7   +0.068    1.10
micro_bos       25342    62%    30.2   +0.053    1.08
close_strong    33403    82%    29.7   +0.034    1.05
any_combo       35345    87%    29.8   +0.037    1.05
----------------------------------------------------------------

================================================================
XAUUSD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4202   100%    29.2   +0.018    1.02
LIMIT_all        3625    86%    28.9   +0.009    1.01
pin_engulf       3011    72%    29.0   +0.011    1.02  ← current
rsi_reclaim      1093    26%    28.6   -0.001    1.00
stoch_reclaim    1644    39%    26.6   -0.068    0.91
band_reclaim     1432    34%    29.9   +0.045    1.06
micro_bos        2721    65%    29.1   +0.014    1.02
close_strong     3472    83%    28.8   +0.004    1.01
any_combo        3658    87%    28.2   -0.018    0.97
----------------------------------------------------------------

================================================================
EURUSD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4571   100%    29.3   +0.021    1.03
LIMIT_all        3989    87%    29.3   +0.024    1.03
pin_engulf       3098    68%    29.2   +0.021    1.03  ← current
rsi_reclaim      1159    25%    32.8   +0.143    1.21
stoch_reclaim    1778    39%    30.3   +0.060    1.09
band_reclaim     1627    36%    30.7   +0.071    1.10
micro_bos        2851    62%    29.9   +0.045    1.06
close_strong     3726    82%    29.3   +0.025    1.04
any_combo        3942    86%    29.1   +0.019    1.03
----------------------------------------------------------------

================================================================
GBPUSD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4537   100%    28.0   -0.025    0.96
LIMIT_all        3984    88%    28.5   -0.004    1.00
pin_engulf       3055    67%    29.4   +0.028    1.04  ← current
rsi_reclaim      1173    26%    32.2   +0.125    1.19
stoch_reclaim    1725    38%    28.8   +0.007    1.01
band_reclaim     1661    37%    30.8   +0.075    1.11
micro_bos        2905    64%    29.4   +0.025    1.03
close_strong     3695    81%    28.1   -0.018    0.98
any_combo        3913    86%    27.9   -0.029    0.96
----------------------------------------------------------------

================================================================
EURGBP
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4553   100%    30.3   +0.055    1.08
LIMIT_all        3952    87%    31.5   +0.098    1.14
pin_engulf       3242    71%    32.8   +0.143    1.21  ← current
rsi_reclaim      1300    29%    30.3   +0.053    1.08
stoch_reclaim    1821    40%    31.3   +0.088    1.13
band_reclaim     1536    34%    31.8   +0.106    1.15
micro_bos        2739    60%    31.4   +0.091    1.13
close_strong     3805    84%    31.8   +0.106    1.16
any_combo        4042    89%    32.2   +0.118    1.17
----------------------------------------------------------------

================================================================
AUDUSD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4424   100%    28.1   -0.022    0.97
LIMIT_all        3888    88%    28.4   -0.007    0.99
pin_engulf       2966    67%    29.2   +0.018    1.03  ← current
rsi_reclaim      1136    26%    32.0   +0.118    1.17
stoch_reclaim    1826    41%    30.7   +0.073    1.11
band_reclaim     1574    36%    31.2   +0.089    1.13
micro_bos        2792    63%    30.9   +0.074    1.11
close_strong     3640    82%    29.2   +0.020    1.03
any_combo        3817    86%    29.1   +0.016    1.02
----------------------------------------------------------------

================================================================
NZDUSD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4509   100%    30.4   +0.061    1.09
LIMIT_all        3934    87%    29.7   +0.036    1.05
pin_engulf       3031    67%    29.0   +0.012    1.02  ← current
rsi_reclaim      1061    24%    32.3   +0.127    1.19
stoch_reclaim    1771    39%    30.9   +0.081    1.12
band_reclaim     1511    34%    31.0   +0.083    1.12
micro_bos        2862    63%    30.1   +0.051    1.07
close_strong     3715    82%    28.8   +0.003    1.00
any_combo        3915    87%    29.2   +0.017    1.02
----------------------------------------------------------------

================================================================
USDCAD
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4555   100%    28.2   -0.018    0.97
LIMIT_all        4014    88%    30.0   +0.045    1.06
pin_engulf       3209    70%    29.4   +0.020    1.03  ← current
rsi_reclaim      1134    25%    30.9   +0.076    1.11
stoch_reclaim    1834    40%    31.0   +0.079    1.11
band_reclaim     1517    33%    31.8   +0.107    1.16
micro_bos        2832    62%    31.2   +0.090    1.13
close_strong     3744    82%    30.2   +0.051    1.07
any_combo        3988    88%    29.9   +0.040    1.06
----------------------------------------------------------------

================================================================
USDCHF
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4586   100%    29.2   +0.019    1.03
LIMIT_all        4023    88%    30.4   +0.060    1.09
pin_engulf       3171    69%    31.1   +0.087    1.13  ← current
rsi_reclaim      1188    26%    31.7   +0.105    1.15
stoch_reclaim    1814    40%    29.1   +0.018    1.02
band_reclaim     1479    32%    28.7   -0.003    1.00
micro_bos        2837    62%    29.8   +0.041    1.06
close_strong     3765    82%    29.3   +0.025    1.04
any_combo        3987    87%    30.2   +0.056    1.08
----------------------------------------------------------------

================================================================
USDJPY
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4264   100%    26.6   -0.076    0.90
LIMIT_all        3763    88%    28.2   -0.018    0.97
pin_engulf       2898    68%    29.6   +0.031    1.04  ← current
rsi_reclaim      1142    27%    30.1   +0.049    1.07
stoch_reclaim    1705    40%    28.0   -0.029    0.96
band_reclaim     1475    35%    30.2   +0.046    1.07
micro_bos        2675    63%    28.7   -0.001    1.00
close_strong     3458    81%    28.0   -0.025    0.97
any_combo        3717    87%    27.9   -0.029    0.96
----------------------------------------------------------------

================================================================
EURJPY
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4505   100%    29.1   +0.012    1.02
LIMIT_all        3928    87%    29.9   +0.037    1.05
pin_engulf       3166    70%    29.5   +0.025    1.04  ← current
rsi_reclaim      1175    26%    31.7   +0.101    1.15
stoch_reclaim    1868    41%    29.8   +0.035    1.05
band_reclaim     1574    35%    29.3   +0.021    1.03
micro_bos        2798    62%    29.3   +0.019    1.03
close_strong     3713    82%    29.9   +0.043    1.06
any_combo        3945    88%    30.2   +0.052    1.07
----------------------------------------------------------------

================================================================
GBPJPY
================================================================
gate                N  fill%    win%     avgR      PF
----------------------------------------------------------------
MARKET           4398   100%    29.1   +0.010    1.01
LIMIT_all        3808    87%    29.5   +0.030    1.04
pin_engulf       3072    70%    28.1   -0.024    0.97  ← current
rsi_reclaim      1129    26%    31.4   +0.091    1.13
stoch_reclaim    1722    39%    30.2   +0.051    1.07
band_reclaim     1490    34%    30.7   +0.062    1.09
micro_bos        2726    62%    30.0   +0.045    1.06
close_strong     3600    82%    30.2   +0.048    1.07
any_combo        3796    86%    30.0   +0.041    1.06
----------------------------------------------------------------
```
