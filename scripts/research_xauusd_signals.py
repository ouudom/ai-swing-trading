"""Phase 0b — XAUUSD independent signal research.

Tests each signal/indicator in isolation to measure true forward-return edge.
NO combined scoring. Each condition tested alone vs ~54% gold upward baseline.

Methodology: signal fires → forward close return at fixed horizon →
             compare win% vs baseline → N | win% | edge (pp) | avg% | t_stat

Data:
  D1/H4/H1: data/twelvedata/xauusd/{1day,4h,1h}.csv  (6.3yr 2020-2026)
  Macro:    data/fred/{DFII10,T5YIE,VIXCLS,DFF,DCOILWTICO}.csv
  DXY:      data/yahoo/DXY.csv
  COT:      data/cftc/deahistfo{year}.zip (2019-2026)
  Long D1:  data/yahoo/XAUUSD_long.csv (yfinance GC=F, auto-fetched if missing)

Forward windows:
  D1 → fwd=5 (1 trading week)
  H4 → fwd=6 (24h)
  H1 → fwd=4 (4h)

Run:
  .venv/bin/python -m scripts.research_xauusd_signals           # D1 only
  .venv/bin/python -m scripts.research_xauusd_signals --tf h4   # H4 only
  .venv/bin/python -m scripts.research_xauusd_signals --tf h1   # H1 only
  .venv/bin/python -m scripts.research_xauusd_signals --tf all  # all three
  .venv/bin/python -m scripts.research_xauusd_signals --long    # incl 22yr yfinance (seasonality)
"""

import argparse
import zipfile
import warnings
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ─── Paths ────────────────────────────────────────────────────────────────────
TD_DIR   = Path("data/twelvedata/xauusd")
FRED_DIR = Path("data/fred")
YAHOO_DIR = Path("data/yahoo")
CFTC_DIR = Path("data/cftc")

XAUUSD_LONG_CSV = YAHOO_DIR / "XAUUSD_long.csv"

# ─── Indicators ───────────────────────────────────────────────────────────────

def rsi(s, p=14):
    dlt = s.diff()
    up  = dlt.clip(lower=0).rolling(p).mean()
    dn  = (-dlt.clip(upper=0)).rolling(p).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def atr(df, p=14):
    tr = pd.concat([
        (df.high - df.low),
        (df.high - df.close.shift()).abs(),
        (df.low  - df.close.shift()).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(p).mean()


def stoch(df, k=14, d=3):
    lo = df.low.rolling(k).min()
    hi = df.high.rolling(k).max()
    pct_k = 100 * (df.close - lo) / (hi - lo).replace(0, np.nan)
    pct_d = pct_k.rolling(d).mean()
    return pct_k, pct_d


def williams_r(df, p=14):
    hi = df.high.rolling(p).max()
    lo = df.low.rolling(p).min()
    return -100 * (hi - df.close) / (hi - lo).replace(0, np.nan)


def cci(df, p=20):
    tp  = (df.high + df.low + df.close) / 3
    sma = tp.rolling(p).mean()
    mad = tp.rolling(p).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    return (tp - sma) / (0.015 * mad.replace(0, np.nan))


def macd(s, fast=12, slow=26, sig=9):
    ema_f  = s.ewm(span=fast, adjust=False).mean()
    ema_s  = s.ewm(span=slow, adjust=False).mean()
    line   = ema_f - ema_s
    signal = line.ewm(span=sig, adjust=False).mean()
    return line, signal


def bb(s, p=20, k=2):
    sma = s.rolling(p).mean()
    std = s.rolling(p).std()
    return sma + k * std, sma - k * std, std * 2  # upper, lower, width


def adx(df, p=14):
    hi, lo, cl = df.high, df.low, df.close
    up_move = hi.diff()
    dn_move = -lo.diff()
    plus_dm  = np.where((up_move > dn_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((dn_move > up_move) & (dn_move > 0), dn_move, 0.0)
    tr_s = atr(df, p) * p
    plus_di  = 100 * pd.Series(plus_dm,  index=df.index).rolling(p).sum() / tr_s.replace(0, np.nan)
    minus_di = 100 * pd.Series(minus_dm, index=df.index).rolling(p).sum() / tr_s.replace(0, np.nan)
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.rolling(p).mean(), plus_di, minus_di


# ─── Statistics ───────────────────────────────────────────────────────────────

def edge_stat(df, mask, direction, fwd_col, baseline):
    """Compute edge stats for a signal mask.
    direction: +1 = expect price UP, -1 = expect price DOWN.
    Returns formatted string.
    """
    sub = df[mask].dropna(subset=[fwd_col])
    n   = len(sub)
    if n < 15:
        return f"N={n:>4}  INSUFFICIENT"
    ret = sub[fwd_col]  # forward return (positive = price went up)
    if direction > 0:
        wins = (ret > 0).sum()
    else:
        wins = (ret < 0).sum()
    win_pct = wins / n * 100
    edge    = win_pct - baseline
    avg_ret = ret.mean() * direction * 100  # in %, signed to signal direction
    t_stat  = edge / (100 * np.sqrt(baseline / 100 * (1 - baseline / 100) / n))
    stars   = " **" if abs(t_stat) > 2.6 else (" *" if abs(t_stat) > 2.0 else "")
    insuf   = " [n<50]" if n < 50 else ""
    return (f"N={n:>4}  win%={win_pct:>5.1f}  edge={edge:>+5.1f}pp"
            f"  avg={avg_ret:>+.3f}%  t={t_stat:>+.2f}{stars}{insuf}")


def section(title):
    print(f"\n{'─'*68}")
    print(f"  {title}")
    print(f"{'─'*68}")


def row(label, direction, stat):
    dir_label = "LNG" if direction > 0 else "SHT"
    print(f"  {label:<38} {dir_label}  {stat}")


# ─── Data Loaders ─────────────────────────────────────────────────────────────

def load_td(tf="1day"):
    df = pd.read_csv(TD_DIR / f"{tf}.csv", parse_dates=["datetime"]).sort_values("datetime")
    df = df[df.datetime.dt.dayofweek < 5].reset_index(drop=True)
    return df


def load_long_d1():
    """Fetch 22yr gold daily from yfinance GC=F. Cache to XAUUSD_long.csv."""
    if XAUUSD_LONG_CSV.exists():
        df = pd.read_csv(XAUUSD_LONG_CSV, parse_dates=["datetime"]).sort_values("datetime")
        # refresh if older than 7 days
        age_days = (pd.Timestamp.now() - df.datetime.iloc[-1]).days
        if age_days < 7:
            print(f"  [long D1] loaded from cache: {len(df)} rows "
                  f"({df.datetime.iloc[0].date()} → {df.datetime.iloc[-1].date()})")
            return df
    try:
        import yfinance as yf
        print("  [long D1] fetching GC=F from yfinance (22yr)...")
        raw = yf.download("GC=F", start="2004-01-01", progress=False, auto_adjust=True)
        if raw.empty:
            raise ValueError("yfinance returned empty frame")
        raw = raw.reset_index()
        # Handle MultiIndex columns from newer yfinance versions
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = [c[0].lower() for c in raw.columns]
        else:
            raw.columns = [c.lower() for c in raw.columns]
        raw = raw.rename(columns={"date": "datetime", "adj close": "close"})
        for col in ["open", "high", "low", "close"]:
            if col not in raw.columns:
                raise ValueError(f"Missing column: {col}")
        df = raw[["datetime", "open", "high", "low", "close"]].copy()
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df[df.datetime.dt.dayofweek < 5].reset_index(drop=True)
        YAHOO_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(XAUUSD_LONG_CSV, index=False)
        print(f"  [long D1] cached {len(df)} rows "
              f"({df.datetime.iloc[0].date()} → {df.datetime.iloc[-1].date()})")
        return df
    except Exception as e:
        print(f"  [long D1] yfinance failed: {e} — seasonality tests skipped")
        return None


def load_fred_aligned(d1_index):
    """Load FRED series, forward-fill onto D1 trading-day index."""
    series = {}
    specs = {
        "dfii10": ("DFII10.csv",     "value"),
        "t5yie":  ("T5YIE.csv",      "value"),
        "vix":    ("VIXCLS.csv",     "value"),
        "dff":    ("DFF.csv",        "value"),
        "oil":    ("DCOILWTICO.csv", "value"),
    }
    for key, (fname, col) in specs.items():
        path = FRED_DIR / fname
        if not path.exists():
            continue
        fr = pd.read_csv(path, parse_dates=["date"]).dropna()
        fr = fr.rename(columns={"date": "datetime", col: key})
        series[key] = fr.set_index("datetime")[key]

    dxy_path = YAHOO_DIR / "DXY.csv"
    if dxy_path.exists():
        dxy = pd.read_csv(dxy_path, parse_dates=["date"]).dropna()
        dxy = dxy.rename(columns={"date": "datetime", "value": "dxy"})
        series["dxy"] = dxy.set_index("datetime")["dxy"]

    idx = pd.DatetimeIndex(d1_index)
    out = pd.DataFrame(index=idx)
    for key, s in series.items():
        out[key] = s.reindex(idx, method="ffill")
    return out.reset_index().rename(columns={"index": "datetime"})


def load_cot_history():
    """Parse CFTC zips (2019-2026) → full gold spec net weekly series."""
    records = []
    for year in range(2019, 2027):
        zpath = CFTC_DIR / f"deahistfo{year}.zip"
        if not zpath.exists():
            continue
        try:
            z  = zipfile.ZipFile(zpath)
            df = pd.read_csv(z.open(z.namelist()[0]), low_memory=False)
            mask = (df["Market and Exchange Names"].astype(str).str.strip()
                    == "GOLD - COMMODITY EXCHANGE INC.")
            g = df[mask].copy()
            g["date"] = pd.to_datetime(g["As of Date in Form YYYY-MM-DD"], errors="coerce")
            g = g.dropna(subset=["date"])
            long_col  = "Noncommercial Positions-Long (All)"
            short_col = "Noncommercial Positions-Short (All)"
            g["net"] = g[long_col].astype(int) - g[short_col].astype(int)
            records.append(g[["date", "net"]])
        except Exception:
            continue
    if not records:
        return None
    cot = pd.concat(records).sort_values("date").drop_duplicates("date").reset_index(drop=True)
    cot["net_chg"] = cot.net.diff()
    return cot


# ─── Build indicators on a dataframe ──────────────────────────────────────────

def build_indicators(df):
    """Add all technical indicators to df (in-place)."""
    c = df.close

    df["rsi"]     = rsi(c)
    df["stoch_k"], df["stoch_d"] = stoch(df)
    df["wr"]      = williams_r(df)
    df["cci"]     = cci(df)
    df["macd_l"], df["macd_s"] = macd(c)
    df["macd_hist"] = df.macd_l - df.macd_s
    df["bb_hi"], df["bb_lo"], df["bb_w"] = bb(c, 20, 2)
    df["bb_hi15"], df["bb_lo15"], _       = bb(c, 20, 1.5)
    df["ema20"]   = c.ewm(span=20,  adjust=False).mean()
    df["ema50"]   = c.ewm(span=50,  adjust=False).mean()
    df["ema200"]  = c.ewm(span=200, adjust=False).mean()
    df["don_hi20"] = df.high.rolling(20).max().shift(1)
    df["don_lo20"] = df.low.rolling(20).min().shift(1)
    df["hi20"]    = df.high.rolling(20).max()
    df["lo20"]    = df.low.rolling(20).min()
    df["atr14"]   = atr(df)
    df["atr_med"] = df.atr14.rolling(20).median()
    df["adx14"], df["pdi"], df["mdi"] = adx(df)
    df["bb_w_med"] = df.bb_w.rolling(20).median()

    # Candlestick patterns
    body  = (df.close - df.open).abs()
    rng   = df.high - df.low
    df["body_ratio"] = body / rng.replace(0, np.nan)
    df["inside_bar"] = (rng < (df.high - df.low).shift(1)).astype(int)
    df["nr7"]        = (rng == rng.rolling(7).min()).astype(int)

    # MACD cross
    df["macd_cross_up"]  = ((df.macd_l > df.macd_s) & (df.macd_l.shift() <= df.macd_s.shift())).astype(int)
    df["macd_cross_dn"]  = ((df.macd_l < df.macd_s) & (df.macd_l.shift() >= df.macd_s.shift())).astype(int)
    df["rsi_cross_dn70"] = ((df.rsi < 70) & (df.rsi.shift() >= 70)).astype(int)  # exit OB
    df["rsi_cross_up30"] = ((df.rsi > 30) & (df.rsi.shift() <= 30)).astype(int)  # exit OS

    return df


# ─── D1 Tests ─────────────────────────────────────────────────────────────────

def run_d1(use_long=False):
    print("\n" + "═"*68)
    print("  XAUUSD — D1 SIGNAL SCAN  (fwd=5 bars, ~1 trading week)")
    print("═"*68)

    # Load data
    df = load_td("1day")
    build_indicators(df)

    FWD  = 5
    BASE = 54.0  # gold D1 secular baseline

    df["fwd"] = df.close.shift(-FWD) / df.close - 1

    print(f"\n  Sample: {df.datetime.iloc[0].date()} → {df.datetime.iloc[-1].date()}"
          f"  N={len(df)}  baseline={BASE}%  fwd={FWD}d")

    # Load macro
    macro = load_fred_aligned(df.datetime)
    df = df.merge(macro, on="datetime", how="left")

    # COT (weekly, forward-fill)
    cot = load_cot_history()
    if cot is not None:
        cot_s = cot.set_index("date")["net"].reindex(pd.DatetimeIndex(df.datetime), method="ffill")
        cot_c = cot.set_index("date")["net_chg"].reindex(pd.DatetimeIndex(df.datetime), method="ffill")
        df["cot_net"] = cot_s.values
        df["cot_chg"] = cot_c.values
        df["cot_pct"] = df.cot_net.rank(pct=True) * 100
        print(f"  COT: {cot.date.iloc[0].date()} → {cot.date.iloc[-1].date()}  N={len(cot)} weekly")
    else:
        df["cot_net"] = np.nan
        df["cot_chg"] = np.nan
        df["cot_pct"] = np.nan
        print("  COT: not available")

    # DFII10 derived
    df["dfii_sl20"] = df.dfii10.diff(20)
    df["dfii_sl5"]  = df.dfii10.diff(5)
    df["dxy_sl20"]  = df.dxy.diff(20)
    df["dxy_sl1"]   = df.dxy.diff(1)
    df["t5_sl20"]   = df.t5yie.diff(20)
    df["oil_sl20"]  = df.oil.diff(20)
    df["vix_sl1"]   = df.vix.diff(1)

    E = lambda mask, d: edge_stat(df, mask, d, "fwd", BASE)

    # ── Category A: Oscillator Extremes ──────────────────────────────────────
    section("A — Oscillator Extremes (mean-reversion candidates)")
    row("A1  RSI(14)>70 → short",          -1, E(df.rsi > 70, -1))
    row("A2  RSI(14)<30 → long",            +1, E(df.rsi < 30, +1))
    row("A3  RSI(14)>65 → short (soft)",   -1, E(df.rsi > 65, -1))
    row("A4  RSI(14)<35 → long (soft)",    +1, E(df.rsi < 35, +1))
    row("A5  RSI cross below 70 → short",  -1, E(df.rsi_cross_dn70 == 1, -1))
    row("A6  RSI cross above 30 → long",   +1, E(df.rsi_cross_up30 == 1, +1))
    row("A7  Stoch K>80 → short",          -1, E(df.stoch_k > 80, -1))
    row("A8  Stoch K<20 → long",           +1, E(df.stoch_k < 20, +1))
    row("A9  Williams %R > -20 → short",   -1, E(df.wr > -20, -1))
    row("A10 Williams %R < -80 → long",    +1, E(df.wr < -80, +1))
    row("A11 CCI(20) > +100 → short",      -1, E(df.cci > 100, -1))
    row("A12 CCI(20) < -100 → long",       +1, E(df.cci < -100, +1))

    # ── Category B: Bollinger ─────────────────────────────────────────────────
    section("B — Bollinger / Volatility Bands")
    row("B1  Close > BB(20,2) upper → short",   -1, E(df.close > df.bb_hi, -1))
    row("B2  Close < BB(20,2) lower → long",    +1, E(df.close < df.bb_lo, +1))
    row("B3  Close > BB(20,1.5) upper → short", -1, E(df.close > df.bb_hi15, -1))
    row("B4  Close < BB(20,1.5) lower → long",  +1, E(df.close < df.bb_lo15, +1))
    row("B5  BB squeeze (width < 20-bar med) → long",  +1, E(df.bb_w < df.bb_w_med, +1))
    row("B5s BB squeeze (width < 20-bar med) → short", -1, E(df.bb_w < df.bb_w_med, -1))
    row("B6  BB expand (width > 20-bar med) → long",   +1, E(df.bb_w > df.bb_w_med, +1))

    # ── Category C: Trend / Structure / Momentum ─────────────────────────────
    section("C — Trend / Structure / Momentum")
    row("C1  Close > EMA(20) → long",         +1, E(df.close > df.ema20, +1))
    row("C2  Close < EMA(20) → short",        -1, E(df.close < df.ema20, -1))
    row("C3  Close > EMA(50) → long",         +1, E(df.close > df.ema50, +1))
    row("C4  Close < EMA(50) → short",        -1, E(df.close < df.ema50, -1))
    row("C5  Close > EMA(200) → long",        +1, E(df.close > df.ema200, +1))
    row("C6  Close < EMA(200) → short",       -1, E(df.close < df.ema200, -1))
    row("C7  EMA20 > EMA50 → long (regime)",  +1, E(df.ema20 > df.ema50, +1))
    row("C8  EMA20 < EMA50 → short (regime)", -1, E(df.ema20 < df.ema50, -1))
    row("C9  Donchian20 break UP → long",     +1, E(df.close > df.don_hi20, +1))
    row("C10 Donchian20 break DOWN → short",  -1, E(df.close < df.don_lo20, -1))
    row("C11 Near 20d HIGH (within 0.3%) → short", -1,
        E((df.high >= df.hi20 * 0.997) & (df.high <= df.hi20 * 1.003), -1))
    row("C12 Near 20d LOW (within 0.3%) → long",   +1,
        E((df.low <= df.lo20 * 1.003) & (df.low >= df.lo20 * 0.997), +1))
    row("C13 MACD cross UP → long",           +1, E(df.macd_cross_up == 1, +1))
    row("C14 MACD cross DOWN → short",        -1, E(df.macd_cross_dn == 1, -1))
    row("C15 ADX < 20 (ranging) → long",      +1, E(df.adx14 < 20, +1))
    row("C15 ADX < 20 (ranging) → short",     -1, E(df.adx14 < 20, -1))
    row("C16 ADX 20-25 (transition) → long",  +1, E((df.adx14 >= 20) & (df.adx14 <= 25), +1))
    row("C17 ADX > 25 (trending) → long",     +1, E(df.adx14 > 25, +1))
    row("C17 ADX > 25 (trending) → short",    -1, E(df.adx14 > 25, -1))

    # ── Category D: Volatility Regime ─────────────────────────────────────────
    section("D — Volatility Regime")
    row("D1  ATR compressed (<20-bar med) → long",    +1, E(df.atr14 < df.atr_med, +1))
    row("D1s ATR compressed (<20-bar med) → short",   -1, E(df.atr14 < df.atr_med, -1))
    row("D2  ATR expanded (>1.5× med) → long",        +1, E(df.atr14 > 1.5 * df.atr_med, +1))
    row("D2s ATR expanded (>1.5× med) → short",       -1, E(df.atr14 > 1.5 * df.atr_med, -1))
    row("D3  ATR compressed + RSI>70 → short",        -1,
        E((df.atr14 < df.atr_med) & (df.rsi > 70), -1))
    row("D3l ATR compressed + RSI<30 → long",         +1,
        E((df.atr14 < df.atr_med) & (df.rsi < 30), +1))
    row("D4  NR7 (narrowest range 7 bars) → long",    +1, E(df.nr7 == 1, +1))
    row("D4s NR7 → short",                            -1, E(df.nr7 == 1, -1))
    row("D5  Inside bar → long",                      +1, E(df.inside_bar == 1, +1))
    row("D5s Inside bar → short",                     -1, E(df.inside_bar == 1, -1))

    # ── Category E: Macro ─────────────────────────────────────────────────────
    section("E — Macro (DFII10 / DXY / VIX / T5YIE / Oil)")
    row("E1  DFII10 20d slope < 0 → long",    +1, E(df.dfii_sl20 < 0, +1))
    row("E2  DFII10 20d slope > 0 → short",   -1, E(df.dfii_sl20 > 0, -1))
    row("E3  DFII10 level < 0 → long",        +1, E(df.dfii10 < 0, +1))
    row("E4  DFII10 level > 2.0 → short",     -1, E(df.dfii10 > 2.0, -1))
    row("E5  DFII10 level 0-1 → long",        +1, E((df.dfii10 >= 0) & (df.dfii10 <= 1), +1))
    row("E6  DFII10 5d jump > +0.15 → short", -1, E(df.dfii_sl5 > 0.15, -1))
    row("E7  DFII10 5d drop > 0.15 → long",   +1, E(df.dfii_sl5 < -0.15, +1))
    row("E8  DXY 20d slope < 0 → long",       +1, E(df.dxy_sl20 < 0, +1))
    row("E9  DXY 20d slope > 0 → short",      -1, E(df.dxy_sl20 > 0, -1))
    row("E10 DXY 1d jump > 0.75 → short",     -1, E(df.dxy_sl1 > 0.75, -1))
    row("E11 T5YIE 20d slope > 0 → long",     +1, E(df.t5_sl20 > 0, +1))
    row("E12 T5YIE 20d slope < 0 → short",    -1, E(df.t5_sl20 < 0, -1))
    row("E13 VIX > 20 → long",                +1, E(df.vix > 20, +1))
    row("E14 VIX > 30 → long",                +1, E(df.vix > 30, +1))
    row("E15 VIX < 15 → short",               -1, E(df.vix < 15, -1))
    row("E16 VIX 1d spike > +3 → long",       +1, E(df.vix_sl1 > 3, +1))
    row("E17 DFF > 4% → short",               -1, E(df.dff > 4, -1))
    row("E18 DFF < 1% → long",                +1, E(df.dff < 1, +1))
    row("E19 Oil 20d slope > 0 → long",       +1, E(df.oil_sl20 > 0, +1))
    row("E20 Oil 20d slope < 0 → short",      -1, E(df.oil_sl20 < 0, -1))

    # ── Category F: COT ───────────────────────────────────────────────────────
    if df.cot_net.notna().sum() > 30:
        section("F — COT Positioning (CFTC gold spec net, weekly forward-filled)")
        row("F1  Spec net > 200k → short",           -1, E(df.cot_net > 200_000, -1))
        row("F2  Spec net < 75k → long",             +1, E(df.cot_net < 75_000, +1))
        row("F3  Spec net >80th pctile → short",     -1, E(df.cot_pct > 80, -1))
        row("F4  Spec net <20th pctile → long",      +1, E(df.cot_pct < 20, +1))
        row("F5  W/W change < -15k → short",         -1, E(df.cot_chg < -15_000, -1))
        row("F6  W/W change > +15k → long",          +1, E(df.cot_chg > 15_000, +1))
    else:
        print("\n  [F — COT] Insufficient data")

    # ── Category G: Seasonality (needs long history) ──────────────────────────
    if use_long:
        dlong = load_long_d1()
        if dlong is not None:
            build_indicators(dlong)
            dlong["fwd"] = dlong.close.shift(-FWD) / dlong.close - 1
            BASE_L = float((dlong.close.pct_change(FWD).shift(-FWD) > 0).mean() * 100)
            n_yrs  = (dlong.datetime.iloc[-1] - dlong.datetime.iloc[0]).days / 365.25
            EL = lambda mask, d: edge_stat(dlong, mask, d, "fwd", BASE_L)
            section(f"G — Seasonality  ({dlong.datetime.iloc[0].year}→{dlong.datetime.iloc[-1].year}"
                    f"  ~{n_yrs:.0f}yr  baseline={BASE_L:.1f}%)")
            for dow, name in [(0,"Mon"),(1,"Tue"),(2,"Wed"),(3,"Thu"),(4,"Fri")]:
                m = dlong.datetime.dt.dayofweek == dow
                row(f"G-{name} → long",  +1, EL(m, +1))
                row(f"G-{name} → short", -1, EL(m, -1))
            for mon, name in [(1,"Jan"),(2,"Feb"),(3,"Mar"),(4,"Apr"),(5,"May"),(6,"Jun"),
                               (7,"Jul"),(8,"Aug"),(9,"Sep"),(10,"Oct"),(11,"Nov"),(12,"Dec")]:
                m = dlong.datetime.dt.month == mon
                row(f"G-{name:>3} → long",  +1, EL(m, +1))
                row(f"G-{name:>3} → short", -1, EL(m, -1))
            # Turn of month
            eom = dlong.datetime.dt.is_month_end | (
                (dlong.datetime + pd.Timedelta(days=1)).dt.is_month_end) | (
                (dlong.datetime + pd.Timedelta(days=2)).dt.is_month_end)
            bom = dlong.datetime.dt.is_month_start | (
                (dlong.datetime - pd.Timedelta(days=1)).dt.is_month_start) | (
                (dlong.datetime - pd.Timedelta(days=2)).dt.is_month_start)
            row("G-TOM last 3 days → long",   +1, EL(eom, +1))
            row("G-TOM first 3 days → long",  +1, EL(bom, +1))

    # ── Combinations ─────────────────────────────────────────────────────────
    section("COMBINATIONS (macro × technical)")
    row("E1+A2  DFII10 fall + RSI<30 → long",  +1,
        E((df.dfii_sl20 < 0) & (df.rsi < 30), +1))
    row("E2+A1  DFII10 rise + RSI>70 → short", -1,
        E((df.dfii_sl20 > 0) & (df.rsi > 70), -1))
    row("E1+D1  DFII10 fall + ATR comp → long", +1,
        E((df.dfii_sl20 < 0) & (df.atr14 < df.atr_med), +1))
    row("E13+E1 VIX>20 + DFII10 fall → long",  +1,
        E((df.vix > 20) & (df.dfii_sl20 < 0), +1))
    row("A1+C11 RSI>70 + near 20d high → short", -1,
        E((df.rsi > 70) & (df.high >= df.hi20 * 0.997), -1))
    row("A2+C12 RSI<30 + near 20d low → long",   +1,
        E((df.rsi < 30) & (df.low <= df.lo20 * 1.003), +1))
    row("B1+A1  BB upper + RSI>70 → short",      -1,
        E((df.close > df.bb_hi) & (df.rsi > 70), -1))
    row("B2+A2  BB lower + RSI<30 → long",       +1,
        E((df.close < df.bb_lo) & (df.rsi < 30), +1))

    print(f"\n  Legend: * t>2.0  ** t>2.6  [n<50] small sample")
    print(f"  Baseline: {BASE}% of fwd-5d bars up  (2020-2026 secular uptrend)")


# ─── H4 Tests ─────────────────────────────────────────────────────────────────

def run_h4():
    print("\n" + "═"*68)
    print("  XAUUSD — H4 SIGNAL SCAN  (fwd=6 bars = ~24h)")
    print("═"*68)

    df = load_td("4h")
    # Filter weekend/holiday flatline (range < $1)
    df = df[(df.high - df.low) >= 1.0].reset_index(drop=True)
    build_indicators(df)

    FWD  = 6
    BASE = float((df.close.pct_change(FWD).shift(-FWD) > 0).mean() * 100)
    df["fwd"] = df.close.shift(-FWD) / df.close - 1

    print(f"\n  Sample: {df.datetime.iloc[0].date()} → {df.datetime.iloc[-1].date()}"
          f"  N={len(df)}  baseline={BASE:.1f}%  fwd={FWD} bars (24h)")

    E = lambda mask, d: edge_stat(df, mask, d, "fwd", BASE)

    section("H4-A — Oscillator Extremes")
    row("A1  RSI(14)>70 → short",     -1, E(df.rsi > 70, -1))
    row("A2  RSI(14)<30 → long",       +1, E(df.rsi < 30, +1))
    row("A3  RSI(14)>65 → short",     -1, E(df.rsi > 65, -1))
    row("A4  RSI(14)<35 → long",       +1, E(df.rsi < 35, +1))
    row("A7  Stoch K>80 → short",     -1, E(df.stoch_k > 80, -1))
    row("A8  Stoch K<20 → long",       +1, E(df.stoch_k < 20, +1))
    row("A9  Williams %R > -20 → short", -1, E(df.wr > -20, -1))
    row("A10 Williams %R < -80 → long",  +1, E(df.wr < -80, +1))
    row("A11 CCI(20) > +100 → short",  -1, E(df.cci > 100, -1))
    row("A12 CCI(20) < -100 → long",   +1, E(df.cci < -100, +1))

    section("H4-B — Bollinger")
    row("B1  Close > BB(20,2) → short",   -1, E(df.close > df.bb_hi, -1))
    row("B2  Close < BB(20,2) → long",    +1, E(df.close < df.bb_lo, +1))
    row("B5  BB squeeze → long",          +1, E(df.bb_w < df.bb_w_med, +1))
    row("B5s BB squeeze → short",         -1, E(df.bb_w < df.bb_w_med, -1))

    section("H4-C — Trend / Momentum")
    row("C1  Close > EMA(20) → long",     +1, E(df.close > df.ema20, +1))
    row("C2  Close < EMA(20) → short",    -1, E(df.close < df.ema20, -1))
    row("C3  Close > EMA(50) → long",     +1, E(df.close > df.ema50, +1))
    row("C4  Close < EMA(50) → short",    -1, E(df.close < df.ema50, -1))
    row("C5  Close > EMA(200) → long",    +1, E(df.close > df.ema200, +1))
    row("C9  Donchian20 break UP → long", +1, E(df.close > df.don_hi20, +1))
    row("C10 Donchian20 break DN → short",-1, E(df.close < df.don_lo20, -1))
    row("C13 MACD cross UP → long",       +1, E(df.macd_cross_up == 1, +1))
    row("C14 MACD cross DN → short",      -1, E(df.macd_cross_dn == 1, -1))
    row("C17 ADX > 25 → long",            +1, E(df.adx14 > 25, +1))
    row("C17 ADX > 25 → short",           -1, E(df.adx14 > 25, -1))

    section("H4-D — Volatility")
    row("D1  ATR compressed → long",      +1, E(df.atr14 < df.atr_med, +1))
    row("D1s ATR compressed → short",     -1, E(df.atr14 < df.atr_med, -1))
    row("D4  NR7 → long",                 +1, E(df.nr7 == 1, +1))
    row("D4s NR7 → short",                -1, E(df.nr7 == 1, -1))
    row("D5  Inside bar → long",          +1, E(df.inside_bar == 1, +1))
    row("D5s Inside bar → short",         -1, E(df.inside_bar == 1, -1))

    section("H4-H — Session (UTC hour of bar open)")
    df["hour"] = df.datetime.dt.hour
    row("H1  Asia bar (22-06 UTC) → long",     +1, E((df.hour >= 22) | (df.hour < 6), +1))
    row("H1s Asia bar (22-06 UTC) → short",    -1, E((df.hour >= 22) | (df.hour < 6), -1))
    row("H2  London open (07-09) → long",      +1, E((df.hour >= 7) & (df.hour < 9), +1))
    row("H2s London open (07-09) → short",     -1, E((df.hour >= 7) & (df.hour < 9), -1))
    row("H3  NY open (13-15) → long",          +1, E((df.hour >= 13) & (df.hour < 15), +1))
    row("H3s NY open (13-15) → short",         -1, E((df.hour >= 13) & (df.hour < 15), -1))
    row("H4  NY/Lon overlap (12-16) → long",   +1, E((df.hour >= 12) & (df.hour < 16), +1))
    row("H4s NY/Lon overlap (12-16) → short",  -1, E((df.hour >= 12) & (df.hour < 16), -1))
    row("H5  London close (16-17) → short",    -1, E((df.hour >= 16) & (df.hour < 17), -1))
    row("H6  Asia dead zone (00-04) → long",   +1, E((df.hour >= 0) & (df.hour < 4), +1))

    print(f"\n  Legend: * t>2.0  ** t>2.6  [n<50] small sample")
    print(f"  Baseline: {BASE:.1f}% of fwd-{FWD} H4 bars up (2020-2026)")


# ─── H1 Tests ─────────────────────────────────────────────────────────────────

def run_h1():
    print("\n" + "═"*68)
    print("  XAUUSD — H1 SIGNAL SCAN  (fwd=4 bars = ~4h)")
    print("═"*68)

    df = load_td("1h")
    # Filter non-trading hours (very thin bars)
    df = df[(df.high - df.low) >= 0.5].reset_index(drop=True)
    build_indicators(df)

    FWD  = 4
    BASE = float((df.close.pct_change(FWD).shift(-FWD) > 0).mean() * 100)
    df["fwd"] = df.close.shift(-FWD) / df.close - 1

    print(f"\n  Sample: {df.datetime.iloc[0].date()} → {df.datetime.iloc[-1].date()}"
          f"  N={len(df)}  baseline={BASE:.1f}%  fwd={FWD} bars (4h)")

    E = lambda mask, d: edge_stat(df, mask, d, "fwd", BASE)

    section("H1-A — Oscillator Extremes")
    row("A1  RSI(14)>70 → short",     -1, E(df.rsi > 70, -1))
    row("A2  RSI(14)<30 → long",       +1, E(df.rsi < 30, +1))
    row("A7  Stoch K>80 → short",     -1, E(df.stoch_k > 80, -1))
    row("A8  Stoch K<20 → long",       +1, E(df.stoch_k < 20, +1))
    row("A9  Williams %R > -20 → short", -1, E(df.wr > -20, -1))
    row("A10 Williams %R < -80 → long",  +1, E(df.wr < -80, +1))
    row("A11 CCI(20) > +100 → short",  -1, E(df.cci > 100, -1))
    row("A12 CCI(20) < -100 → long",   +1, E(df.cci < -100, +1))

    section("H1-B — Bollinger")
    row("B1  Close > BB(20,2) → short",  -1, E(df.close > df.bb_hi, -1))
    row("B2  Close < BB(20,2) → long",   +1, E(df.close < df.bb_lo, +1))
    row("B5  BB squeeze → long",         +1, E(df.bb_w < df.bb_w_med, +1))

    section("H1-C — Trend / Momentum")
    row("C1  Close > EMA(20) → long",    +1, E(df.close > df.ema20, +1))
    row("C2  Close < EMA(20) → short",   -1, E(df.close < df.ema20, -1))
    row("C3  Close > EMA(50) → long",    +1, E(df.close > df.ema50, +1))
    row("C4  Close < EMA(50) → short",   -1, E(df.close < df.ema50, -1))
    row("C9  Donchian20 break UP → long",+1, E(df.close > df.don_hi20, +1))
    row("C10 Donchian20 break DN → short",-1, E(df.close < df.don_lo20, -1))
    row("C13 MACD cross UP → long",      +1, E(df.macd_cross_up == 1, +1))
    row("C14 MACD cross DN → short",     -1, E(df.macd_cross_dn == 1, -1))

    section("H1-D — Volatility")
    row("D1  ATR compressed → long",     +1, E(df.atr14 < df.atr_med, +1))
    row("D5  Inside bar → long",         +1, E(df.inside_bar == 1, +1))
    row("D4  NR7 → long",                +1, E(df.nr7 == 1, +1))

    section("H1-H — Session (UTC hour)")
    df["hour"] = df.datetime.dt.hour
    for h in range(0, 24):
        m = df.hour == h
        stat_l = edge_stat(df, m, +1, "fwd", BASE)
        stat_s = edge_stat(df, m, -1, "fwd", BASE)
        print(f"  H{h:02d}:00 UTC  LNG  {stat_l}")
        print(f"  H{h:02d}:00 UTC  SHT  {stat_s}")

    print(f"\n  Legend: * t>2.0  ** t>2.6  [n<50] small sample")
    print(f"  Baseline: {BASE:.1f}% of fwd-{FWD} H1 bars up (2020-2026)")


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="XAUUSD Phase 0b — independent signal scan")
    p.add_argument("--tf",   default="d1",
                   choices=["d1", "h4", "h1", "all"],
                   help="Timeframe to scan (default: d1)")
    p.add_argument("--long", action="store_true",
                   help="Include 22yr yfinance seasonality section (fetches GC=F if needed)")
    args = p.parse_args()

    tf = args.tf.lower()

    if tf in ("d1", "all"):
        run_d1(use_long=args.long)
    if tf in ("h4", "all"):
        run_h4()
    if tf in ("h1", "all"):
        run_h1()

    print("\n" + "═"*68)
    print("  DONE. Results above.")
    print("  Action thresholds: edge>5pp + t>2.6 = keep/promote")
    print("                     edge<2pp or t<1.5 = cut/demote")
    print("                     negative edge = remove from system")
    print("═"*68 + "\n")


if __name__ == "__main__":
    main()
