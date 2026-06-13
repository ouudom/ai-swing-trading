"""Shared market-structure primitives — fractal pivots, trend state, structural distance.

Single source of truth for MTF structure alignment (Z4/E1) and structural_dist (stop
sizing), used by live /validate. All functions operate on CLOSED bars only — the caller
must drop any forming/open bar before passing a frame in.

Pivot definition: N=2 fractal. A bar is a pivot high if its `high` is strictly greater
than the highs of the N bars on each side; pivot low symmetric on `low`. N=2 needs 2
confirming bars to the right, so the most recent pivot lags ~2 bars — intended (a pivot
is only real once price turns away from it).
"""
import numpy as np
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


def structure_events(df, n=PIVOT_N, lookback=60):
    """Label market-structure breaks over the last `lookback` bars (D025).

    Walks confirmed fractal pivots; a close beyond the most-recent confirmed pivot extreme is:
      BOS   (break of structure) when it extends the prevailing trend (continuation), or
      CHoCH (change of character) when it breaks AGAINST it (first reversal tell — the FX
            mean-reversion fade's signal).
    A pivot at position p is only 'confirmed' n bars later (find_pivots' right-confirmation lag).
    Returns {state, events[], last}. Each event: {type, dir, level, time, pos}.
    """
    sub = df.tail(lookback).reset_index()
    times = sub["datetime"] if "datetime" in sub.columns else sub.index
    highs, lows, closes = sub["high"].to_numpy(), sub["low"].to_numpy(), sub["close"].to_numpy()
    L = len(sub)
    ph, pl = find_pivots(sub, n)
    conf_h_at = {p + n: highs[p] for p in ph if p + n < L}   # bar where pivot becomes confirmed
    conf_l_at = {p + n: lows[p] for p in pl if p + n < L}

    events = []
    trend = "mixed"
    last_h = last_l = None
    for i in range(L):
        if i in conf_h_at: last_h = conf_h_at[i]
        if i in conf_l_at: last_l = conf_l_at[i]
        c = closes[i]
        if last_h is not None and c > last_h:
            typ = "CHoCH" if trend == "down" else "BOS"
            events.append({"type": typ, "dir": "up", "level": round(float(last_h), 6),
                           "time": str(times.iloc[i])[:16] if hasattr(times, "iloc") else str(times[i])[:16],
                           "pos": i})
            trend = "up"; last_h = None
        elif last_l is not None and c < last_l:
            typ = "CHoCH" if trend == "up" else "BOS"
            events.append({"type": typ, "dir": "down", "level": round(float(last_l), 6),
                           "time": str(times.iloc[i])[:16] if hasattr(times, "iloc") else str(times[i])[:16],
                           "pos": i})
            trend = "down"; last_l = None
    return {"state": structure_state(df, n), "events": events, "last": events[-1] if events else None}


def time_at_price(df, bins=50, window=480):
    """Price-acceptance histogram = VP substitute when tick volume is 0 (USD-base pairs).

    Counts bars whose range covers each price bin over the last `window` bars (≈H1, ~20 trading
    days). High-time node (HTN) = most-accepted price; value area = 70% of time around it.
    This is TIME at price, not VOLUME — label it as such. Returns {htn, va_high, va_low} or None.
    """
    sub = df.tail(window)
    lo_all, hi_all = float(sub["low"].min()), float(sub["high"].max())
    if hi_all <= lo_all:
        return None
    edges = np.linspace(lo_all, hi_all, bins + 1)
    counts = np.zeros(bins)
    for lo, hi in zip(sub["low"].to_numpy(), sub["high"].to_numpy()):
        for b in range(bins):
            if min(hi, edges[b + 1]) > max(lo, edges[b]):
                counts[b] += 1
    htn_i = int(np.argmax(counts))
    mid = lambda i: (edges[i] + edges[i + 1]) / 2
    total, target = counts.sum(), counts.sum() * 0.70
    lo_i = hi_i = htn_i; acc = counts[htn_i]
    while acc < target and (lo_i > 0 or hi_i < bins - 1):
        add_lo = counts[lo_i - 1] if lo_i > 0 else -1
        add_hi = counts[hi_i + 1] if hi_i < bins - 1 else -1
        if add_lo >= add_hi and lo_i > 0: lo_i -= 1; acc += add_lo
        elif hi_i < bins - 1:             hi_i += 1; acc += add_hi
        else:                             lo_i -= 1; acc += add_lo
    return {"htn": mid(htn_i), "va_high": edges[hi_i + 1], "va_low": edges[lo_i]}
