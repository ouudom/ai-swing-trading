"""
entry_confluence.py — programmatic Entry Confluence (R2) scorer for the replay.

Live `/validate` has Claude assemble the R2 score in prose from each
`wiki/system/{inst}/confluence_criteria.md`. `trade_outcome.py` needs that score
computed deterministically at a historical fill bar, for two reasons:
  1. the entry offset is EC-dependent — offset = max(SL/3, (10 − EC) × 0.2 × SL);
  2. R2 calibration needs an EC per replayed fill (the real `trade` table has n≈2).

Design
  - Pure functions, no I/O beyond the shared macro loaders. All indicator math is
    REUSED from `backtest_signals.py` (rsi/atr/adx/stoch_k/williams_r/cci/keltner/
    bollinger/rolling_slope + pin/engulf detectors). No re-implementation.
  - Per-instrument component table lives in `config/ec_spec.py` (EC_SPEC), sourced
    from each pair's confluence_criteria.md R2 rows. score() walks it, sums the
    weight of every passing predicate, and returns (score, breakdown).
  - Every signal is read on CLOSED bars at/before `fill_time` — no lookahead.

FIDELITY CAVEAT (see plan / decisions D031): the per-pair R2 prose carries bespoke
oscillator/threshold/session choices picked off t-stats. This scorer applies the
GENERIC fade thresholds (RSI 35/65, Stoch 20/80, W%R −80/−20, CCI ±100) and the
dominant predicate per row; fine per-pair tuning is approximated. Macro/session
predicates degrade to False + a 'na' flag when their series can't be loaded at the
bar. Treat R2 numbers as provisional until ec_spec is reviewed against the markdown.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from backtest_signals import (  # noqa: E402
    rsi, atr, adx, stoch_k, williams_r, cci, keltner, bollinger, rolling_slope,
    pin_bull, pin_bear, bull_engulf, bear_engulf,
    load_fred, load_dxy, align_daily,
)
from config.ec_spec import EC_SPEC, DEFAULT_SPEC  # noqa: E402
import structure as struct  # noqa: E402

# Does the zone need USD STRONGER to work? (drives DXY/real-yield slope polarity.)
# XXXUSD long ⇒ USD weaker; USDXXX long ⇒ USD stronger; xauusd long ⇒ USD weaker.
_USD_QUOTE = {"eurusd", "gbpusd", "audusd", "nzdusd", "xauusd"}   # USD is the quote / pro-USD-weak on long
_USD_BASE = {"usdcad", "usdchf", "usdjpy"}                         # USD is the base
_NO_USD = {"eurgbp", "eurjpy", "gbpjpy"}                           # crosses — no USD leg


def usd_strength_needed(inst: str, is_long: bool) -> bool | None:
    if inst in _NO_USD:
        return None
    if inst in _USD_BASE:
        return is_long          # long USDXXX ⇒ USD up
    return not is_long          # long XXXUSD / gold ⇒ USD down


# ── context ───────────────────────────────────────────────────────────────────

class Ctx:
    """Everything a predicate needs, with frames pre-sliced to ≤ fill_time."""

    def __init__(self, inst, is_long, fill_time, zone_top, zone_bottom,
                 h1, h4, d1, e0_present, structure_intact):
        self.inst = inst
        self.is_long = is_long
        self.sign = 1 if is_long else -1
        self.t = pd.Timestamp(fill_time)
        self.zone_top, self.zone_bottom = zone_top, zone_bottom
        self.e0_present = bool(e0_present)
        self.structure_intact = bool(structure_intact)
        self.flags = []
        # closed bars only
        self.h1 = self._cut(h1)
        self.h4 = self._cut(h4)
        self.d1 = self._cut(d1)

    def _cut(self, df):
        if df is None or df.empty:
            return df
        return df[df["datetime"] <= self.t].reset_index(drop=True)


# ── oscillator / band helpers ───────────────────────────────────────────────────

def _last(series):
    if series is None or len(series) == 0:
        return np.nan
    v = series.iloc[-1] if hasattr(series, "iloc") else series[-1]
    return float(v) if pd.notna(v) else np.nan


def osc_extreme(df, is_long, min_bars=20) -> bool:
    """Any of RSI/Stoch/W%R/CCI beyond the fade threshold on the last closed bar.
    LONG fades oversold; SHORT fades overbought."""
    if df is None or len(df) < min_bars:
        return False
    r = _last(rsi(df["close"], 14))
    k = _last(stoch_k(df))
    w = _last(williams_r(df))
    c = _last(cci(df))
    if is_long:
        return any(v < t for v, t in [(r, 35), (k, 20), (w, -80), (c, -100)] if not np.isnan(v))
    return any(v > t for v, t in [(r, 65), (k, 80), (w, -20), (c, 100)] if not np.isnan(v))


def band_touch(df, is_long, min_bars=20) -> bool:
    """Last bar tagged the Keltner band on the fade side."""
    if df is None or len(df) < min_bars:
        return False
    ku, kl = keltner(df)
    if is_long:
        return float(df["low"].iloc[-1]) <= _last(kl)
    return float(df["high"].iloc[-1]) >= _last(ku)


def squeeze_on(df, min_bars=25) -> bool:
    """TTM-style squeeze: Keltner channel inside the Bollinger band on the last bar."""
    if df is None or len(df) < min_bars:
        return False
    bu, bl, _, _ = bollinger(df["close"], 20, 2)
    ku, kl = keltner(df, 20, 1.5)
    return _last(bu) < _last(ku) and _last(bl) > _last(kl)


def atr_compressed(df, min_bars=35) -> bool:
    if df is None or len(df) < min_bars:
        return False
    a = atr(df, 14)
    med = a.rolling(20).median()
    return _last(a) < _last(med)


def adx_below(df, thr, min_bars=30) -> bool:
    if df is None or len(df) < min_bars:
        return False
    return _last(adx(df, 14)) < thr


# ── macro helpers (degrade to None when series absent) ──────────────────────────

def _daily_slope_at(series, d1, cutoff, n=20):
    """20d slope of a daily macro series, aligned to the D1 frame, at `cutoff`."""
    if series is None or d1 is None or d1.empty:
        return None
    idx = pd.to_datetime(d1["datetime"])
    vals = align_daily(series, pd.DatetimeIndex(idx))
    if vals is None:
        return None
    s = pd.Series(vals)
    sl = rolling_slope(s, n)
    v = _last(sl)
    return None if np.isnan(v) else v


def dxy_slope_aligned(ctx) -> bool:
    need_strong = usd_strength_needed(ctx.inst, ctx.is_long)
    if need_strong is None:
        return False
    sl = _daily_slope_at(load_dxy(), ctx.d1, ctx.t)
    if sl is None:
        ctx.flags.append("dxy_na")
        return False
    return sl > 0 if need_strong else sl < 0


def realyield_slope_aligned(ctx) -> bool:
    # gold: long wants real yields DOWN (DFII10 slope < 0); short wants up.
    sl = _daily_slope_at(load_fred("DFII10"), ctx.d1, ctx.t)
    if sl is None:
        ctx.flags.append("dfii10_na")
        return False
    return sl < 0 if ctx.is_long else sl > 0


def macro_drift_ok(ctx, band=0.10) -> bool:
    """xauusd E3: |DFII10 now − ~week-ago| < band against direction.
    Baseline proxy = value ~5 business days before the fill (no stored baseline in replay)."""
    s = load_fred("DFII10")
    if s is None:
        ctx.flags.append("dfii10_na")
        return False
    s = s[s.index <= ctx.t]
    if len(s) < 6:
        return False
    now, base = float(s.iloc[-1]), float(s.iloc[-6])
    drift = now - base
    # "against direction" for gold = real yields RISING (drift>0) when long, falling when short
    against = drift if ctx.is_long else -drift
    return against < band


def macro_regime_aligned(ctx) -> bool:
    """aud/cad E4: VIX level toward the zone. LONG risk-pair / short-USD wants low VIX; mirror short."""
    s = load_fred("VIXCLS")
    if s is None:
        ctx.flags.append("vix_na")
        return False
    s = s[s.index <= ctx.t]
    if s.empty:
        return False
    vix = float(s.iloc[-1])
    # audusd long = risk-on (low VIX); usdcad long = USD-up which VIX>20 fuels (fade-USD logic),
    # so usdcad long wants HIGH vix. Encode via usd_strength_needed inversion for cad.
    if ctx.inst == "usdcad":
        return vix > 20 if ctx.is_long else vix < 20
    return vix < 20 if ctx.is_long else vix > 20


def session_window(ctx, params) -> bool:
    """jpy session legs. params: {'long': (lo,hi), 'short': (lo,hi)} in UTC hours; missing side ⇒ pass-through False."""
    win = params.get("long" if ctx.is_long else "short")
    if not win:
        return False
    lo, hi = win
    return lo <= ctx.t.hour < hi


# ── predicate registry ──────────────────────────────────────────────────────────

def _pred(key, ctx, params):
    p = params or {}
    if key == "e0":
        return ctx.e0_present
    if key == "structure_intact":
        return ctx.structure_intact
    if key == "h4_osc_extreme":
        return osc_extreme(ctx.h4, ctx.is_long)
    if key == "h1_osc_extreme":
        return osc_extreme(ctx.h1, ctx.is_long)
    if key == "d1_osc_extreme":
        return osc_extreme(ctx.d1, ctx.is_long)
    if key == "band_touch_h4":
        return band_touch(ctx.h4, ctx.is_long)
    if key == "band_touch_h1":
        return band_touch(ctx.h1, ctx.is_long)
    if key == "h1osc_or_h4band":          # aud/nzd E2: short=H1 osc extreme, long=H4 band tag
        return osc_extreme(ctx.h1, ctx.is_long) or band_touch(ctx.h4, ctx.is_long)
    if key == "squeeze_or_h4osc":         # usdjpy E1: long=squeeze/calm, short=H4 osc extreme
        return squeeze_on(ctx.h4) if ctx.is_long else osc_extreme(ctx.h4, ctx.is_long)
    if key == "adx_below":
        return adx_below(ctx.d1, p.get("thr", 25))
    if key == "atr_compression":
        return atr_compressed(ctx.d1)
    if key == "squeeze":
        return squeeze_on(ctx.h4) or squeeze_on(ctx.d1)
    if key == "h4_structure_aligned":
        return struct.structure_state(ctx.h4) == ("up" if ctx.is_long else "down")
    if key == "dxy_slope":
        return dxy_slope_aligned(ctx)
    if key == "realyield_slope":
        return realyield_slope_aligned(ctx)
    if key == "macro_drift_ok":
        return macro_drift_ok(ctx)
    if key == "macro_regime":
        return macro_regime_aligned(ctx)
    if key == "session_window":
        return session_window(ctx, p)
    ctx.flags.append(f"unknown_pred:{key}")
    return False


def score(inst, is_long, fill_time, zone_top, zone_bottom,
          h1, h4, d1, e0_present, structure_intact) -> tuple[float, dict]:
    """Return (ec_score 0–10, breakdown dict). breakdown carries per-component
    pass/weight + a 'flags' list of degraded macro/session legs."""
    ctx = Ctx(inst, is_long, fill_time, zone_top, zone_bottom,
              h1, h4, d1, e0_present, structure_intact)
    spec = EC_SPEC.get(inst, DEFAULT_SPEC)
    total = 0.0
    comp = {}
    for code, weight, key, params in spec:
        ok = bool(_pred(key, ctx, params))
        comp[code] = {"weight": weight, "pass": ok, "pred": key}
        if ok:
            total += weight
    return round(total, 2), {"components": comp, "flags": sorted(set(ctx.flags)), "spec": inst in EC_SPEC}
