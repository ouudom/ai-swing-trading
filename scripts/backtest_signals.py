"""
Signal edge backtest — independent forward-return testing, multi-instrument.

Rebuilds the Phase 0b runner (removed in cleanup) and EXTENDS the catalogue with
researched high-quality methods/indicators (Connors RSI2, z-score reversion, Keltner,
TTM squeeze, Aroon, Supertrend, PSAR, ROC, ATR-percentile, round-number proximity,
engulfing/pin price-action, 2s10s curve, carry-diff slope, intermarket DXY beta).

Method (per signal, per direction):
  mask    = condition True for a bar
  fwd_ret = close[t+H]/close[t] - 1
  win     = fwd_ret>0 (long) / fwd_ret<0 (short)
  edge    = win%(signal bars) - baseline%(all bars, same direction)
  t       = (win% - baseline) / sqrt(baseline*(1-baseline)/N)

Usage:
  bash scripts/pyrun.sh scripts/backtest_signals.py --instrument eurusd
  bash scripts/pyrun.sh scripts/backtest_signals.py --instrument all --tf D1 H4
  bash scripts/pyrun.sh scripts/backtest_signals.py --instrument gbpusd --since 2022-01-01

Forward windows (match gold Phase 0b): D1 fwd=5 (1wk), H4 fwd=6 (24h), H1 fwd=4 (4h).
Macro signals are D1-only (FRED is daily).
"""

import os, sys, argparse, importlib
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

REGISTERED = {
    "xauusd": "config.xauusd.config",
    "eurusd": "config.eurusd.config",
    "gbpusd": "config.gbpusd.config",
    "eurgbp": "config.eurgbp.config",
    "audusd": "config.audusd.config",
    "nzdusd": "config.nzdusd.config",
    "usdcad": "config.usdcad.config",
    "usdchf": "config.usdchf.config",
    "usdjpy": "config.usdjpy.config",
    "eurjpy": "config.eurjpy.config",
    "gbpjpy": "config.gbpjpy.config",
}
FWD = {"D1": 5, "H4": 6, "H1": 4}
TF_FILE = {"D1": "1day.csv", "H4": "4h.csv", "H1": "1h.csv"}

# ── indicator helpers (self-contained, vectorized) ────────────────────────────

def ema(s, n):  return s.ewm(span=n, adjust=False).mean()
def sma(s, n):  return s.rolling(n).mean()
def roc(s, n):  return s.pct_change(n)

def rsi(s, n=14):
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100/(1+rs)

def rsi_wilder_simple(s, n=2):
    d = s.diff()
    up = d.clip(lower=0).rolling(n).mean()
    dn = (-d.clip(upper=0)).rolling(n).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100/(1+rs)

def true_range(df):
    pc = df["close"].shift()
    return pd.concat([df["high"]-df["low"], (df["high"]-pc).abs(), (df["low"]-pc).abs()], axis=1).max(axis=1)

def atr(df, n=14): return true_range(df).rolling(n).mean()

def adx(df, n=14):
    up = df["high"].diff(); dn = -df["low"].diff()
    plus  = np.where((up > dn) & (up > 0), up, 0.0)
    minus = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = true_range(df)
    atrn = tr.ewm(alpha=1/n, adjust=False).mean()
    pdi = 100 * pd.Series(plus, index=df.index).ewm(alpha=1/n, adjust=False).mean() / atrn
    mdi = 100 * pd.Series(minus, index=df.index).ewm(alpha=1/n, adjust=False).mean() / atrn
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return dx.ewm(alpha=1/n, adjust=False).mean()

def stoch_k(df, n=14, smooth=3):
    ll = df["low"].rolling(n).min(); hh = df["high"].rolling(n).max()
    k = 100 * (df["close"] - ll) / (hh - ll).replace(0, np.nan)
    return k.rolling(smooth).mean()

def williams_r(df, n=14):
    hh = df["high"].rolling(n).max(); ll = df["low"].rolling(n).min()
    return -100 * (hh - df["close"]) / (hh - ll).replace(0, np.nan)

def cci(df, n=20):
    tp = (df["high"]+df["low"]+df["close"])/3
    ma = tp.rolling(n).mean()
    md = (tp - ma).abs().rolling(n).mean()
    return (tp - ma) / (0.015 * md.replace(0, np.nan))

def macd(s, fast=12, slow=26, sig=9):
    line = ema(s, fast) - ema(s, slow)
    signal = ema(line, sig)
    return line, signal

def bollinger(s, n=20, k=2):
    m = s.rolling(n).mean(); sd = s.rolling(n).std()
    up, lo = m + k*sd, m - k*sd
    pctb = (s - lo) / (up - lo).replace(0, np.nan)
    bw = (up - lo) / m
    return up, lo, pctb, bw

def keltner(df, n=20, k=1.5):
    m = ema(df["close"], n); a = atr(df, n)
    return m + k*a, m - k*a

def aroon(df, n=25):
    up = df["high"].rolling(n+1).apply(lambda x: x.argmax()/n*100, raw=True)
    dn = df["low"].rolling(n+1).apply(lambda x: x.argmin()/n*100, raw=True)
    return up, dn

def supertrend_dir(df, n=10, mult=3.0):
    a = atr(df, n); hl2 = (df["high"]+df["low"])/2
    upper = hl2 + mult*a; lower = hl2 - mult*a
    dirn = pd.Series(1, index=df.index)
    fu, fl = upper.copy(), lower.copy()
    c = df["close"].values
    fu_v, fl_v, d_v = fu.values, fl.values, dirn.values
    for i in range(1, len(df)):
        fl_v[i] = max(fl_v[i], fl_v[i-1]) if c[i-1] > fl_v[i-1] else fl_v[i]
        fu_v[i] = min(fu_v[i], fu_v[i-1]) if c[i-1] < fu_v[i-1] else fu_v[i]
        if c[i] > fu_v[i-1]:   d_v[i] = 1
        elif c[i] < fl_v[i-1]: d_v[i] = -1
        else:                  d_v[i] = d_v[i-1]
    return pd.Series(d_v, index=df.index)

def psar(df, af0=0.02, afmax=0.2):
    h, l = df["high"].values, df["low"].values
    n = len(df); ps = np.zeros(n); bull = True
    af = af0; ep = h[0]; sar = l[0]
    for i in range(1, n):
        sar = sar + af*(ep - sar)
        if bull:
            if l[i] < sar:
                bull = False; sar = ep; ep = l[i]; af = af0
            else:
                if h[i] > ep: ep = h[i]; af = min(af+af0, afmax)
        else:
            if h[i] > sar:
                bull = True; sar = ep; ep = h[i]; af = af0
            else:
                if l[i] < ep: ep = l[i]; af = min(af+af0, afmax)
        ps[i] = 1 if bull else -1
    return pd.Series(ps, index=df.index)

def zscore(s, n=20):
    return (s - s.rolling(n).mean()) / s.rolling(n).std().replace(0, np.nan)

def rolling_slope(s, n=20):
    idx = np.arange(n)
    def f(x):
        if np.isnan(x).any(): return np.nan
        return np.polyfit(idx, x, 1)[0]
    return s.rolling(n).apply(f, raw=True)

def pct_rank(s, n=100):
    return s.rolling(n).apply(lambda x: (x < x.iloc[-1]).mean(), raw=False)

# ── price action ──────────────────────────────────────────────────────────────

def bull_engulf(df):
    o, c, po, pc = df["open"], df["close"], df["open"].shift(), df["close"].shift()
    return (pc < po) & (c > o) & (c >= po) & (o <= pc)

def bear_engulf(df):
    o, c, po, pc = df["open"], df["close"], df["open"].shift(), df["close"].shift()
    return (pc > po) & (c < o) & (c <= po) & (o >= pc)

def pin_bull(df):
    body = (df["close"]-df["open"]).abs()
    tail = df[["open","close"]].min(axis=1) - df["low"]
    return tail >= 2.5*body.replace(0, np.nan)

def pin_bear(df):
    body = (df["close"]-df["open"]).abs()
    wick = df["high"] - df[["open","close"]].max(axis=1)
    return wick >= 2.5*body.replace(0, np.nan)

def inside_bar(df):
    return (df["high"] < df["high"].shift()) & (df["low"] > df["low"].shift())

def nr7(df):
    rng = df["high"]-df["low"]
    return rng == rng.rolling(7).min()

# ── data loading ──────────────────────────────────────────────────────────────

def _db():
    try:
        import db
        return db
    except Exception:
        return None

def load_ohlc(path):
    p = Path(path)
    d = _db()
    df = d.read_ohlc(p.parent.name, p.stem, source=p.parent.parent.name) if d else None
    if df is None or df.empty:
        df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    for c in ("open", "high", "low", "close", "volume"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("datetime").sort_index()
    return df[~df.index.duplicated(keep="last")]

def load_fred(sid):
    d = _db()
    s = d.read_slice("macro_series", {"series_id": sid}, ["date", "value"]) if d else None
    if s is None or s.empty:
        p = ROOT / "data" / "fred" / f"{sid}.csv"
        if not p.exists(): return None
        s = pd.read_csv(p)[["date", "value"]]
    s["date"] = pd.to_datetime(s["date"]); s["value"] = pd.to_numeric(s["value"], errors="coerce")
    return s.set_index("date")["value"].sort_index()

def load_dxy():
    d = _db()
    s = d.read_slice("market_series", {"source": "yahoo", "symbol": "DXY"}, ["date", "value"]) if d else None
    if s is None or s.empty:
        p = ROOT / "data" / "yahoo" / "DXY.csv"
        if not p.exists(): return None
        s = pd.read_csv(p)[["date", "value"]]
    s["date"] = pd.to_datetime(s["date"]); s["value"] = pd.to_numeric(s["value"], errors="coerce")
    return s.set_index("date")["value"].sort_index()

def align_daily(series, idx):
    """Forward-fill a daily macro series onto an OHLC index (date-matched)."""
    if series is None: return None
    s = series.reindex(series.index.union(idx.normalize().unique())).ffill()
    return s.reindex(idx.normalize()).values

# ── scoring ───────────────────────────────────────────────────────────────────

def score(mask, fwd, direction, base_long, base_short):
    m = mask.values if hasattr(mask, "values") else mask
    valid = m & ~np.isnan(fwd)
    n = int(valid.sum())
    if n == 0: return None
    fr = fwd[valid]
    if direction == "LNG":
        win = (fr > 0).mean(); base = base_long; avg = fr.mean()*100
    else:
        win = (fr < 0).mean(); base = base_short; avg = -fr.mean()*100
    edge = (win - base) * 100
    se = np.sqrt(base*(1-base)/n)
    t = (win - base)/se if se > 0 else 0.0
    return {"N": n, "win": win*100, "edge": edge, "avg": avg, "t": t}

# ── signal catalogue ──────────────────────────────────────────────────────────

def build_signals(df, tf, cfg):
    """Return list of (code, label, direction, mask) for the given OHLC frame."""
    c, h, l, o = df["close"], df["high"], df["low"], df["open"]
    sig = []
    A = sig.append

    # ── Oscillator extremes (mean-reversion) ──
    r = rsi(c, 14)
    A(("A1", "RSI>70", "SHT", r > 70)); A(("A2", "RSI<30", "LNG", r < 30))
    A(("A3", "RSI>65", "SHT", r > 65)); A(("A4", "RSI<35", "LNG", r < 35))
    r2 = rsi_wilder_simple(c, 2)
    A(("A5", "RSI2<10 (Connors)", "LNG", r2 < 10)); A(("A6", "RSI2>90 (Connors)", "SHT", r2 > 90))
    k = stoch_k(df)
    A(("A7", "Stoch K>80", "SHT", k > 80)); A(("A8", "Stoch K<20", "LNG", k < 20))
    wr = williams_r(df)
    A(("A9", "Williams%R>-20", "SHT", wr > -20)); A(("A10", "Williams%R<-80", "LNG", wr < -80))
    cc = cci(df)
    A(("A11", "CCI>+100", "SHT", cc > 100)); A(("A12", "CCI<-100", "LNG", cc < -100))

    # ── Bollinger / z-score / volatility bands ──
    bu, bl, pctb, bw = bollinger(c)
    A(("B1", "Close>BB upper", "SHT", c > bu)); A(("B2", "Close<BB lower", "LNG", c < bl))
    A(("B1r","Close>BB upper REV", "LNG", c > bu)); A(("B2r","Close<BB lower REV", "SHT", c < bl))
    A(("B5", "BB squeeze (bw 20-low)", "LNG", bw == bw.rolling(20).min()))
    A(("B6", "BB expanding (>20-med)", "LNG", bw > bw.rolling(20).median()))
    z = zscore(c, 20)
    A(("B7", "z-score<-2 → long", "LNG", z < -2)); A(("B8", "z-score>+2 → short", "SHT", z > 2))
    ku, kl = keltner(df)
    A(("B9", "Close<Keltner low", "LNG", c < kl)); A(("B10","Close>Keltner high", "SHT", c > ku))
    # TTM squeeze: BB inside Keltner (compression) → directional break next
    A(("B11","TTM squeeze on", "LNG", (bu < ku) & (bl > kl)))

    # ── Trend / structure / momentum ──
    A(("C1", "Close>EMA20", "LNG", c > ema(c,20))); A(("C2", "Close<EMA20", "SHT", c < ema(c,20)))
    A(("C3", "Close>EMA50", "LNG", c > ema(c,50))); A(("C4", "Close<EMA50", "SHT", c < ema(c,50)))
    A(("C5", "Close>EMA200", "LNG", c > ema(c,200))); A(("C6", "Close<EMA200", "SHT", c < ema(c,200)))
    A(("C7", "EMA20>EMA50", "LNG", ema(c,20) > ema(c,50))); A(("C8", "EMA20<EMA50", "SHT", ema(c,20) < ema(c,50)))
    hh20, ll20 = h.rolling(20).max(), l.rolling(20).min()
    A(("C9", "Donchian20 breakout UP", "LNG", c >= hh20.shift())); A(("C10","Donchian20 breakdown", "SHT", c <= ll20.shift()))
    near_hi = (hh20 - c)/c < 0.003; near_lo = (c - ll20)/c < 0.003
    A(("C11","Near 20d HIGH", "SHT", near_hi)); A(("C12","Near 20d LOW", "LNG", near_lo))
    A(("C11r","Near 20d HIGH REV", "LNG", near_hi)); A(("C12r","Near 20d LOW REV", "SHT", near_lo))
    ml, sl = macd(c)
    cross_up = (ml > sl) & (ml.shift() <= sl.shift()); cross_dn = (ml < sl) & (ml.shift() >= sl.shift())
    A(("C13","MACD cross up", "LNG", cross_up)); A(("C14","MACD cross down", "SHT", cross_dn))
    aru, ard = aroon(df)
    A(("C18","Aroon up>70 & down<30", "LNG", (aru>70)&(ard<30))); A(("C19","Aroon down>70 & up<30", "SHT", (ard>70)&(aru<30)))
    st = supertrend_dir(df)
    A(("C20","Supertrend bull", "LNG", st > 0)); A(("C21","Supertrend bear", "SHT", st < 0))
    ps = psar(df)
    A(("C22","PSAR bull", "LNG", ps > 0)); A(("C23","PSAR bear", "SHT", ps < 0))
    rc = roc(c, 10)
    A(("C24","ROC10>0", "LNG", rc > 0)); A(("C25","ROC10<0", "SHT", rc < 0))
    # ADX-gated trend (trend signals only count when trending)
    ax = adx(df)
    A(("C26","ADX>25 & EMA20>50", "LNG", (ax>25)&(ema(c,20)>ema(c,50))))
    A(("C27","ADX>25 & EMA20<50", "SHT", (ax>25)&(ema(c,20)<ema(c,50))))
    A(("C28","ADX<20 & RSI<30 (range OS)", "LNG", (ax<20)&(r<30)))
    A(("C29","ADX<20 & RSI>70 (range OB)", "SHT", (ax<20)&(r>70)))

    # ── Volatility regime ──
    a14 = atr(df,14); amed = a14.rolling(20).median()
    A(("D1","ATR<20-med (compressed)", "LNG", a14 < amed)); A(("D1s","ATR<20-med (compressed)", "SHT", a14 < amed))
    A(("D2","ATR>1.5x med (expanding)", "LNG", a14 > 1.5*amed))
    apr = pct_rank(a14, 100)
    A(("D6","ATR pctile<0.2 (calm)", "LNG", apr < 0.2)); A(("D6s","ATR pctile<0.2 (calm)", "SHT", apr < 0.2))
    A(("D4","NR7", "LNG", nr7(df))); A(("D4s","NR7", "SHT", nr7(df)))
    A(("D5","Inside bar", "LNG", inside_bar(df))); A(("D5s","Inside bar", "SHT", inside_bar(df)))

    # ── Price action ──
    A(("P1","Bullish engulfing", "LNG", bull_engulf(df))); A(("P2","Bearish engulfing", "SHT", bear_engulf(df)))
    A(("P3","Bullish pin (tail≥2.5body)", "LNG", pin_bull(df))); A(("P4","Bearish pin", "SHT", pin_bear(df)))

    # ── Round-number proximity (FX big figures: within 15 pips of x.xx00 / x.xx50) ──
    if cfg and getattr(cfg, "MACRO_MODE", "") == "rate_diff":
        # big figure = 100 pips: 0.01 block for 0.0001-pip pairs, 1.00 block for JPY (pip 0.01)
        big_fig = getattr(cfg, "PIP_SIZE", 0.0001) * 100
        figure = (c / big_fig) % 1.0   # distance into the current big-figure (0..1 of a block)
        near_fig = (figure < 0.15) | (figure > 0.85)
        A(("S1","Near big-figure (x.xx00)", "LNG", near_fig)); A(("S1s","Near big-figure", "SHT", near_fig))

    return sig


def macro_signals(df, cfg):
    """D1-only macro signals aligned to the OHLC daily index. Returns list like build_signals."""
    idx = df.index
    sig = []; A = sig.append
    mode = getattr(cfg, "MACRO_MODE", "") if cfg else ""
    rate_diff = mode == "rate_diff"
    cross = mode == "cross_rate_diff"
    # USD-BASE pairs (USDCAD/USDCHF/USDJPY, USD_BETA_SIGN=+1): long pair = LONG USD, so every
    # mechanical USD-direction row (DXY, US-rate M-rows) flips. VIX rows stay unflipped —
    # they are empirical level/regime signals whose polarity is read from the t-stat per pair.
    usd_base = bool(cfg) and getattr(cfg, "USD_BETA_SIGN", -1) > 0
    U = (lambda d: "SHT" if d == "LNG" else "LNG") if usd_base else (lambda d: d)

    if not cross:                       # DXY is a USD index — irrelevant to a non-USD cross
        dxy = align_daily(load_dxy(), idx)
        if dxy is not None:
            dxy_s = pd.Series(dxy, index=idx)
            dsl = rolling_slope(dxy_s, 20)
            A(("E8","DXY 20d slope<0", U("LNG"), dsl < 0)); A(("E9","DXY 20d slope>0", U("SHT"), dsl > 0))
            A(("E10","DXY 1d jump>0.5", U("SHT"), dxy_s.diff() > 0.5))

    vix = align_daily(load_fred("VIXCLS"), idx)
    if vix is not None:
        v = pd.Series(vix, index=idx)
        A(("E13","VIX>20", "LNG", v > 20)); A(("E15","VIX<15", "SHT", v < 15))
        A(("E16","VIX 1d spike>3", "LNG", v.diff() > 3))

    if rate_diff:
        us = align_daily(load_fred(cfg.RATE_US), idx)       # DGS2
        ten = align_daily(load_fred("DGS10"), idx)
        ff = align_daily(load_fred("POLICY_US") if False else load_fred("DFF"), idx)
        fp = align_daily(load_fred(cfg.RATE_FOREIGN), idx)
        if us is not None:
            us_s = pd.Series(us, index=idx); usl = rolling_slope(us_s, 20)
            # USD-quote: falling US 2Y → USD soft → pair UP. USD-base: flipped via U().
            A(("M1","US2Y(DGS2) 20d slope<0", U("LNG"), usl < 0)); A(("M2","US2Y 20d slope>0", U("SHT"), usl > 0))
            A(("M3","US2Y 5d jump>+0.15", U("SHT"), (us_s - us_s.shift(5)) > 0.15))
            A(("M4","US2Y 5d drop>0.15", U("LNG"), (us_s.shift(5) - us_s) > 0.15))
        if us is not None and ten is not None:
            curve = pd.Series(ten - us, index=idx)  # 2s10s
            csl = rolling_slope(curve, 20)
            A(("M5","2s10s steepening", U("LNG"), csl > 0)); A(("M6","2s10s flattening", U("SHT"), csl < 0))
        if ff is not None and fp is not None:
            diff = pd.Series(ff - fp, index=idx)     # US carry premium
            dsl = rolling_slope(diff, 20)
            # widening US carry → USD strength → pair DOWN (USD-quote); flipped for USD-base.
            A(("M7","US-foreign carry widening", U("SHT"), dsl > 0)); A(("M8","US-foreign carry narrowing", U("LNG"), dsl < 0))
            A(("M9","US carry premium falling 1d", U("LNG"), diff.diff() < 0))
        oil_sid = getattr(cfg, "OIL_SERIES", None)
        if oil_sid:
            oil = align_daily(load_fred(oil_sid), idx)
            if oil is not None:
                # 🛢 oil leg (USDCAD): WTI up → CAD strength → pair DOWN (already USD-base aware:
                # directions stated pair-relative, no U() — oil drives the FOREIGN leg).
                o = pd.Series(oil, index=idx); osl = rolling_slope(o, 20)
                A(("W1","WTI 20d slope>0", "SHT", osl > 0)); A(("W2","WTI 20d slope<0", "LNG", osl < 0))
                A(("W3","WTI 1d jump>2%", "SHT", o.pct_change() > 0.02))
                A(("W4","WTI 1d drop>2%", "LNG", o.pct_change() < -0.02))
                A(("W5","WTI 5d move>+5%", "SHT", (o / o.shift(5) - 1) > 0.05))
                A(("W6","WTI 5d move<-5%", "LNG", (o / o.shift(5) - 1) < -0.05))
    elif cross:
        # EURGBP cross macro — EUR (ECB) vs GBP (SONIA). No USD leg. EG2 model.
        eu = align_daily(load_fred(getattr(cfg, "RATE_EUR", "ECBDFR")), idx)
        gb_sid = getattr(cfg, "RATE_GBP", "IUDSOIA")   # None = one-leg cross (EURJPY: no daily BoJ series)
        gb = align_daily(load_fred(gb_sid), idx) if gb_sid else None
        if eu is not None and gb is not None:
            diff = pd.Series(eu - gb, index=idx)      # EUR−GBP rate gap; rising → EURGBP UP
            dsl = rolling_slope(diff, 20)
            A(("X1","EUR-GBP rate diff 20d slope>0", "LNG", dsl > 0)); A(("X2","EUR-GBP diff 20d slope<0", "SHT", dsl < 0))
            A(("X3","EUR-GBP diff 5d widen>+0.05", "LNG", (diff - diff.shift(5)) > 0.05))
            A(("X4","EUR-GBP diff 5d narrow>0.05", "SHT", (diff.shift(5) - diff) > 0.05))
        if gb is not None:
            gb_s = pd.Series(gb, index=idx); gsl = rolling_slope(gb_s, 20)
            # GBP rate rising → GBP strength → EURGBP DOWN
            A(("X5","GBP rate(SONIA) 20d slope>0", "SHT", gsl > 0)); A(("X6","GBP rate 20d slope<0", "LNG", gsl < 0))
            A(("X7","GBP rate 5d jump>+0.05", "SHT", (gb_s - gb_s.shift(5)) > 0.05))
            A(("X8","GBP rate 5d drop>0.05", "LNG", (gb_s.shift(5) - gb_s) > 0.05))
        if eu is not None:
            eu_s = pd.Series(eu, index=idx); esl = rolling_slope(eu_s, 20)
            # Base-leg policy rate rising → base ccy strength → pair UP (RATE_EUR slot =
            # ECBDFR on eur* pairs, IUDSOIA on gbpjpy; sparse step series either way)
            sid = getattr(cfg, "RATE_EUR", "ECBDFR")
            A(("X9", f"base rate({sid}) 20d slope>0", "LNG", esl > 0)); A(("X10", f"base rate({sid}) 20d slope<0", "SHT", esl < 0))
    else:
        # gold real-yield macro (for parity / xauusd runs)
        ry = align_daily(load_fred("DFII10"), idx)
        if ry is not None:
            ry_s = pd.Series(ry, index=idx); rsl = rolling_slope(ry_s, 20)
            A(("E1","DFII10 20d slope<0", "LNG", rsl < 0)); A(("E2","DFII10 20d slope>0", "SHT", rsl > 0))
            A(("E6","DFII10 5d jump>+0.15", "SHT", (ry_s - ry_s.shift(5)) > 0.15))
            A(("E7","DFII10 5d drop>0.15", "LNG", (ry_s.shift(5) - ry_s) > 0.15))
    return sig


def seasonality_signals(df):
    idx = df.index; sig = []; A = sig.append
    dow = idx.dayofweek
    for i, name in enumerate(["Mon","Tue","Wed","Thu","Fri"]):
        A((f"G{i+1}", f"{name} → long", "LNG", pd.Series(dow == i, index=idx)))
        A((f"G{i+1}s", f"{name} → short", "SHT", pd.Series(dow == i, index=idx)))
    mo = idx.month
    A(("G6","January", "LNG", pd.Series(mo == 1, index=idx)))
    A(("G7","September", "SHT", pd.Series(mo == 9, index=idx)))
    A(("G9","Turn of month (day>=26)", "LNG", pd.Series(idx.day >= 26, index=idx)))
    return sig


def session_signals(df, tf):
    if tf not in ("H4","H1"): return []
    idx = df.index; hr = idx.hour; sig = []; A = sig.append
    A(("H2","London open 07-09", "LNG", pd.Series((hr>=7)&(hr<=9), index=idx)))
    A(("H2s","London open 07-09", "SHT", pd.Series((hr>=7)&(hr<=9), index=idx)))
    A(("H3","NY open 13-15", "LNG", pd.Series((hr>=13)&(hr<=15), index=idx)))
    A(("H3s","NY open 13-15", "SHT", pd.Series((hr>=13)&(hr<=15), index=idx)))
    A(("H4o","NY/London overlap 12-16", "LNG", pd.Series((hr>=12)&(hr<=16), index=idx)))
    return sig


def run_tf(inst, cfg, tf, since):
    fpath = ROOT / "data" / "twelvedata" / inst / TF_FILE[tf]
    if not fpath.exists():
        print(f"  [{tf}] no data file {fpath}"); return None
    df = load_ohlc(fpath)
    if since: df = df[df.index >= since]
    H = FWD[tf]
    fwd = (df["close"].shift(-H) / df["close"] - 1).values
    valid_all = ~np.isnan(fwd)
    base_long = float((fwd[valid_all] > 0).mean())
    base_short = float((fwd[valid_all] < 0).mean())

    sigs = build_signals(df, tf, cfg) + session_signals(df, tf)
    if tf == "D1":
        sigs += macro_signals(df, cfg) + seasonality_signals(df)

    rows = []
    for code, label, direction, mask in sigs:
        if not isinstance(mask, pd.Series):
            mask = pd.Series(mask, index=df.index)
        res = score(mask.reindex(df.index).fillna(False), fwd, direction, base_long, base_short)
        if res: rows.append((code, label, direction, res))
    rows.sort(key=lambda x: x[3]["t"], reverse=True)
    return df, base_long, base_short, rows


def fmt_table(inst, tf, base_long, base_short, rows, n_bars):
    out = []
    out.append(f"\n{'='*78}")
    out.append(f"{inst.upper()} Signal Edge Scan — {tf} fwd={FWD[tf]} — "
               f"baseline LNG={base_long*100:.1f}% / SHT={base_short*100:.1f}% — bars={n_bars}")
    out.append(f"{'='*78}")
    out.append(f"{'Code':<6}{'Signal':<32}{'Dir':<5}{'N':>6}{'win%':>7}{'edge':>8}{'avg%':>8}{'t':>7}  ")
    out.append("-"*78)
    for code, label, d, r in rows:
        star = "**" if abs(r["t"]) >= 2.6 else "*" if abs(r["t"]) >= 2.0 else ""
        ins = " INSUFF" if r["N"] < 30 else ""
        out.append(f"{code:<6}{label[:31]:<32}{d:<5}{r['N']:>6}{r['win']:>7.1f}"
                   f"{r['edge']:>+8.1f}{r['avg']:>+8.2f}{r['t']:>7.2f} {star}{ins}")
    out.append("-"*78)
    out.append("* |t|>2.0 (p<.05)   ** |t|>2.6 (p<.01)   N<30 INSUFF")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", default="eurusd")
    ap.add_argument("--tf", nargs="+", default=["D1","H4","H1"], choices=["D1","H4","H1"])
    ap.add_argument("--since", default="2022-01-01")
    ap.add_argument("--out", default=None, help="write markdown to this dir (per instrument)")
    args = ap.parse_args()

    insts = list(REGISTERED) if args.instrument == "all" else [args.instrument]
    since = pd.Timestamp(args.since) if args.since else None

    for inst in insts:
        cfg = importlib.import_module(REGISTERED[inst])
        blocks = []
        for tf in args.tf:
            r = run_tf(inst, cfg, tf, since)
            if r is None: continue
            df, bl, bs, rows = r
            tbl = fmt_table(inst, tf, bl, bs, rows, len(df))
            print(tbl); blocks.append(tbl)
        if args.out:
            d = ROOT / args.out / inst
            d.mkdir(parents=True, exist_ok=True)
            (d / "signal-scan-raw.txt").write_text("\n".join(blocks) + "\n")
            print(f"\n✅ wrote {d/'signal-scan-raw.txt'}")


if __name__ == "__main__":
    main()
