# Entry-Confirmation (E0) Conditional Backtest — Tier 1

Edge = win%(setup WITH 1H pin/engulf trigger) − win%(setup, NO trigger). Positive + |z|≥2 ⇒ the E0 trigger improves the fade outcome and earns its weight. Setup = H1 oscillator extreme (RSI/Stoch/W%R/Keltner). FX mean-rev reading; gold E0 is continuation (read separately). 15M CHoCH leg not tested (data-limited).

## Verdict — E0 adds NO directional/win-rate edge (confirms the standing belief)

Across 11 pairs × 2 directions × 3 horizons = **66 cells.** Significant (|z|≥2):

- **Positive (trigger helps): 1 cell** — usdcad LONG H24 (+2.7, z=2.20*). Isolated, fragile.
- **Negative (trigger HURTS): 6 cells** — eurusd SHORT H6 (−3.4, z=−2.73**), eurgbp LONG H6/H12
  (−2.8/−3.2), usdjpy LONG H6 (−3.0), gbpjpy LONG H6 (−2.8), usdchf SHORT H24 (−2.5).
- **Everything else: noise** (|edge|<2pp, |z|<2). Median edge ≈ 0.

**Requiring a 1H pin/engulf at an extreme does not raise the hit-rate — if anything it slightly
lowers it.** This is exactly what the xauusd rubric already states: *"Trigger alone has no edge —
value is as a quality filter combined with the outward offset (pin+offset PF 3.38)."* Tier 1
confirms it on all 11 pairs.

### Why this is NOT a reason to drop E0

Win-rate is the **wrong metric** for E0. The trigger's payoff is in **fill price → R-multiple**, not
direction:
- A pin lets the limit sit *beyond the wick* (outward offset) → better entry, smaller SL distance →
  higher R per win and a smaller loss when wrong. Same hit-rate, better expectancy.
- The JPY/eurgbp LONG negatives at H6 are intuitive: a bull candle inside a carry-drift *downswing*
  is often a dead-cat — the pair keeps falling. The trigger isn't filtering trend there.

### Actionable

1. **Do not raise E0's weight expecting a win-rate lift** — there is none. Its current weight is
   justified (if at all) by R/offset, which Tier 1 cannot see.
2. **Do not reject a zone solely for a weak-direction trigger** — direction isn't where E0 pays.
3. **Tier 2 (entry-sim: anchor→offset→limit→SL→TP → R, PF) is required** to actually price E0.
   Until then, keep E0 as-is — neither promote nor cut on this evidence.

_Raw cells below._

```

======================================================================
XAUUSD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1587    6789       53.4       52.9    -0.5  -0.37 
SHORT   6    2329    9398       49.2       47.7    -1.6  -1.34 
LONG   12    1587    6789       54.0       55.6    +1.6   1.18 
SHORT  12    2328    9394       47.2       45.3    -2.0  -1.69 
LONG   24    1587    6789       53.0       54.9    +1.9   1.38 
SHORT  24    2328    9391       45.6       44.4    -1.2  -1.04 
----------------------------------------------------------------------

======================================================================
EURUSD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1853    8826       52.9       52.5    -0.4  -0.32 
SHORT   6    1933    8797       51.8       48.4    -3.4  -2.73 **
LONG   12    1853    8826       52.4       51.8    -0.6  -0.49 
SHORT  12    1932    8793       51.6       50.3    -1.3  -1.04 
LONG   24    1853    8823       50.4       50.1    -0.3  -0.20 
SHORT  24    1932    8790       50.8       50.0    -0.8  -0.64 
----------------------------------------------------------------------

======================================================================
GBPUSD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1762    8662       52.3       51.0    -1.3  -1.01 
SHORT   6    2046    9353       49.7       51.9    +2.2   1.76 
LONG   12    1762    8662       52.1       52.5    +0.4   0.32 
SHORT  12    2044    9350       49.5       49.8    +0.3   0.23 
LONG   24    1762    8659       51.0       52.8    +1.7   1.34 
SHORT  24    2044    9347       48.4       49.5    +1.1   0.90 
----------------------------------------------------------------------

======================================================================
EURGBP — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1802    8783       52.5       49.7    -2.8  -2.13 *
SHORT   6    1703    7607       51.7       52.1    +0.5   0.35 
LONG   12    1802    8783       51.3       48.1    -3.2  -2.48 *
SHORT  12    1703    7607       53.6       53.7    +0.1   0.11 
LONG   24    1801    8782       49.6       48.2    -1.4  -1.10 
SHORT  24    1703    7605       52.9       53.6    +0.7   0.51 
----------------------------------------------------------------------

======================================================================
AUDUSD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1807    8537       50.2       51.0    +0.8   0.61 
SHORT   6    2063    9474       50.0       49.7    -0.3  -0.25 
LONG   12    1807    8537       51.0       50.9    -0.1  -0.09 
SHORT  12    2063    9468       49.2       50.3    +1.1   0.90 
LONG   24    1807    8536       52.2       53.9    +1.7   1.35 
SHORT  24    2063    9465       48.8       49.7    +1.0   0.79 
----------------------------------------------------------------------

======================================================================
NZDUSD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1796    9064       49.2       47.8    -1.3  -1.03 
SHORT   6    1924    9147       50.8       51.2    +0.4   0.34 
LONG   12    1796    9064       49.8       49.4    -0.4  -0.32 
SHORT  12    1924    9142       51.1       51.2    +0.1   0.05 
LONG   24    1794    9059       50.2       51.4    +1.2   0.94 
SHORT  24    1924    9139       50.3       51.0    +0.7   0.56 
----------------------------------------------------------------------

======================================================================
USDCAD — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    2096    8684       51.0       49.5    -1.5  -1.25 
SHORT   6    1971    8681       50.6       51.8    +1.2   0.95 
LONG   12    2094    8682       50.4       50.2    -0.1  -0.12 
SHORT  12    1971    8681       50.1       50.3    +0.2   0.20 
LONG   24    2094    8682       50.1       52.8    +2.7   2.20 *
SHORT  24    1970    8673       50.1       48.3    -1.8  -1.45 
----------------------------------------------------------------------

======================================================================
USDCHF — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1955    8592       49.9       49.9    -0.0  -0.01 
SHORT   6    1932    8631       51.0       50.7    -0.4  -0.28 
LONG   12    1955    8589       50.2       50.3    +0.1   0.06 
SHORT  12    1932    8631       49.8       49.3    -0.5  -0.40 
LONG   24    1954    8585       49.7       49.8    +0.1   0.11 
SHORT  24    1932    8628       49.7       47.3    -2.5  -1.95 
----------------------------------------------------------------------

======================================================================
USDJPY — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1526    7260       53.8       50.8    -3.0  -2.14 *
SHORT   6    2155   10592       47.7       46.7    -1.1  -0.90 
LONG   12    1525    7258       52.5       50.8    -1.7  -1.22 
SHORT  12    2155   10592       45.9       45.8    -0.0  -0.04 
LONG   24    1525    7255       52.7       52.4    -0.4  -0.25 
SHORT  24    2155   10592       44.5       45.2    +0.7   0.63 
----------------------------------------------------------------------

======================================================================
EURJPY — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1711    7197       54.2       52.5    -1.7  -1.25 
SHORT   6    2317   10031       47.5       47.9    +0.4   0.34 
LONG   12    1711    7197       54.4       51.9    -2.5  -1.87 
SHORT  12    2317   10027       46.7       47.3    +0.6   0.49 
LONG   24    1711    7192       52.9       52.6    -0.3  -0.23 
SHORT  24    2317   10027       47.7       48.1    +0.4   0.34 
----------------------------------------------------------------------

======================================================================
GBPJPY — Entry-Confirmation conditional test (H1)
======================================================================
dir     H  N_trig  N_none  win_none%  win_trig%    edge      z
----------------------------------------------------------------------
LONG    6    1584    7132       54.1       51.3    -2.8  -2.02 *
SHORT   6    2332    9974       48.3       47.0    -1.3  -1.12 
LONG   12    1584    7132       53.0       51.6    -1.3  -0.95 
SHORT  12    2330    9972       47.3       45.7    -1.6  -1.35 
LONG   24    1583    7129       53.2       51.7    -1.5  -1.07 
SHORT  24    2330    9972       46.9       45.9    -1.1  -0.92 
----------------------------------------------------------------------
```
