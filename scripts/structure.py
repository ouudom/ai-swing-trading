"""Shared market-structure primitives — fractal pivots, trend state, structural distance.

Single source of truth for MTF structure alignment (Z4/E1) and structural_dist (stop
sizing), used by live /validate. All functions operate on CLOSED bars only — the caller
must drop any forming/open bar before passing a frame in.

Pivot definition: N=2 fractal. A bar is a pivot high if its `high` is strictly greater
than the highs of the N bars on each side; pivot low symmetric on `low`. N=2 needs 2
confirming bars to the right, so the most recent pivot lags ~2 bars — intended (a pivot
is only real once price turns away from it).
"""
import pandas as pd

PIVOT_N = 2          # fractal half-width
STRUCT_LOOKBACK = 30  # H4 bars (~5 trading days) for structural_dist search


def find_pivots(df, n=PIVOT_N):
    """Return (pivot_high_positions, pivot_low_positions) as integer row positions."""
    highs = df["high"].to_numpy()
    lows = df["low"].to_numpy()
    L = len(df)
    ph, pl = [], []
    for i in range(n, L - n):
        hi = highs[i]
        if all(hi > highs[i - k] for k in range(1, n + 1)) and \
           all(hi > highs[i + k] for k in range(1, n + 1)):
            ph.append(i)
        lo = lows[i]
        if all(lo < lows[i - k] for k in range(1, n + 1)) and \
           all(lo < lows[i + k] for k in range(1, n + 1)):
            pl.append(i)
    return ph, pl


def structure_state(df, n=PIVOT_N):
    """'up' (HH+HL), 'down' (LH+LL), or 'mixed'. Reads last two pivot highs + lows."""
    ph, pl = find_pivots(df, n)
    if len(ph) < 2 or len(pl) < 2:
        return "mixed"
    highs = df["high"].to_numpy()
    lows = df["low"].to_numpy()
    hh = highs[ph[-1]] > highs[ph[-2]]
    hl = lows[pl[-1]] > lows[pl[-2]]
    lh = highs[ph[-1]] < highs[ph[-2]]
    ll = lows[pl[-1]] < lows[pl[-2]]
    if hh and hl:
        return "up"
    if lh and ll:
        return "down"
    return "mixed"


def mtf_aligned(h4, h1, direction, n=PIVOT_N):
    """MTF structure (Z4/E1): both H4 and H1 align with `direction` (+1 long / -1 short)."""
    want = "up" if direction > 0 else "down"
    return structure_state(h4, n) == want and structure_state(h1, n) == want


def nearest_pivot_dist(df, ref_price, direction, lookback_bars=STRUCT_LOOKBACK, n=PIVOT_N):
    """structural_dist from a zone extreme to the nearest qualifying fractal pivot.

    Long (+1): nearest pivot LOW below ref_price → ref_price - highest_such_low.
    Short (-1): nearest pivot HIGH above ref_price → lowest_such_high - ref_price.
    Returns float distance, or None if no qualifying pivot in the lookback window.
    """
    sub = df.tail(lookback_bars).reset_index(drop=True)
    ph, pl = find_pivots(sub, n)
    lows = sub["low"].to_numpy()
    highs = sub["high"].to_numpy()
    if direction > 0:
        cands = [lows[i] for i in pl if lows[i] < ref_price]
        if not cands:
            return None
        return ref_price - max(cands)
    cands = [highs[i] for i in ph if highs[i] > ref_price]
    if not cands:
        return None
    return min(cands) - ref_price
