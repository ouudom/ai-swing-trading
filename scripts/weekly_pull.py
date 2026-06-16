"""
Multi-instrument data pipeline — orchestrator (fetch + compute + snapshot write).

Usage:
    bash scripts/pyrun.sh scripts/weekly_pull.py                        # xauusd, honors cache
    bash scripts/pyrun.sh scripts/weekly_pull.py --force                # xauusd, re-fetch full
    bash scripts/pyrun.sh scripts/weekly_pull.py --instrument xauusd    # explicit instrument

Split entry points (preferred for granular control):
    scripts/fetch.py    — network IO only (TD 15M + FRED)            → CSVs
    scripts/compute.py  — indicators + snapshot, no TD/FRED network  → pull file
    scripts/weekly_pull.py — this file: cache gate → fetch → compute (back-compat)

Pipeline:
    TD 15M fetch (1 API call) → append 15min.csv → resample → 1h/4h/1day.csv
    FRED fetch                → append data/fred/*.csv
    Compute indicators locally (ATR, ADX, EMA, RSI, MACD, pivots, fibs, swings)
    Fetch VP (yfinance), COT (CFTC, if enabled), ETF flows (if enabled) — no API key required
    Write data/weekly_pull/{instrument}/weekly_pull_{YEAR}_W{WW}.txt

Cache policy: refetch unless (a) snapshot <15min old OR (b) market closed
(CME Globex Fri 22:00 → Sun 22:00 UTC) AND snapshot exists. --force bypasses.

Requirements: pip install requests pandas numpy yfinance python-dotenv
"""

import os, sys, json, argparse, time, importlib
import requests, pandas as pd, numpy as np
import yfinance as yf
from datetime import datetime, timedelta, timezone
from pathlib import Path
from io import StringIO
from dotenv import load_dotenv

# ── INSTRUMENT REGISTRY ───────────────────────────────────────────────────────

REGISTERED_INSTRUMENTS = {
    "xauusd": "config.xauusd.config",
    "eurusd": "config.eurusd.config",
    "gbpusd": "config.gbpusd.config",
    "eurgbp": "config.eurgbp.config",   # cross — EG1 (data); macro placeholder, see D022
    "audusd": "config.audusd.config",   # D024 pair #1 — USD-quote major, no daily RBA series
    "nzdusd": "config.nzdusd.config",   # D024 pair #2 — USD-quote major, no daily RBNZ series
    "usdcad": "config.usdcad.config",   # D024 pair #3 — USD-BASE (inverted), oil leg, COT inverted
    "usdchf": "config.usdchf.config",   # D024 pair #4 — USD-BASE, safe-haven CHF, SNB regime, COT inverted
    "usdjpy": "config.usdjpy.config",   # D024 pair #5 — USD-BASE, first JPY pair (pip 0.01, TICK 650, 3dp)
    "eurjpy": "config.eurjpy.config",   # D024 pair #6 — first cross-JPY (USD_BETA_SIGN=0, JPY pip, one-leg macro)
    "gbpjpy": "config.gbpjpy.config",   # D024 pair #7 — cross-JPY #2 (one-leg macro = SONIA, COT off, high ATR)
}

_instrument_cfg = None  # set by load_instrument()


def load_instrument(name: str):
    """Load instrument config and rebind module globals. Must be called before fetch/compute."""
    global _instrument_cfg, SYMBOL, SYM_CLEAN, TD_DIR, PULL_DIR, FRED_SERIES, GLD_HOLD_CSV, TICK_MULTIPLIER, PRICE_DP

    if name not in REGISTERED_INSTRUMENTS:
        raise ValueError(f"Unknown instrument '{name}'. Registered: {list(REGISTERED_INSTRUMENTS)}")

    # Add project root to sys.path so instruments/ package is importable
    _root = str(Path(__file__).resolve().parents[1])
    if _root not in sys.path:
        sys.path.insert(0, _root)

    cfg = importlib.import_module(REGISTERED_INSTRUMENTS[name])
    _instrument_cfg = cfg

    SYMBOL      = cfg.SYMBOL
    SYM_CLEAN   = cfg.SYM_CLEAN
    TD_DIR      = Path(cfg.TD_DIR)
    PULL_DIR    = Path(cfg.PULL_DIR)
    FRED_SERIES = cfg.FRED_SERIES
    TICK_MULTIPLIER = getattr(cfg, "TICK_MULTIPLIER", 100)
    # Price display/rounding precision: $-scale instruments (gold, TICK<=100) → 2dp;
    # pip-scale FX (TICK>=10000, price ~1.16, ATR ~0.0018) → 5dp or values round to 0.
    # JPY pairs break the TICK heuristic (TICK 650, price ~155, pip 0.01) → config sets PRICE_DP=3.
    PRICE_DP = getattr(cfg, "PRICE_DP", 2 if TICK_MULTIPLIER <= 100 else 5)
    if cfg.ETF_ENABLED and cfg.ETF_HOLDINGS_CSV:
        GLD_HOLD_CSV = Path(cfg.ETF_HOLDINGS_CSV)

    print(f"[instrument] {cfg.DISPLAY_NAME} loaded")

# Cache policy: skip refetch only if file <15min old OR market closed (weekend) with existing data
CACHE_FRESH_SECONDS = 15 * 60   # 15 minutes

def is_market_closed_utc(now=None):
    """CME Globex: closes Fri 22:00 UTC, reopens Sun 22:00 UTC."""
    now = now or datetime.now(timezone.utc)
    wd = now.weekday()  # Mon=0 ... Sun=6
    if wd == 5:                       # Saturday: closed all day
        return True
    if wd == 4 and now.hour >= 22:    # Fri >= 22:00 UTC
        return True
    if wd == 6 and now.hour < 22:     # Sun < 22:00 UTC
        return True
    return False

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from ohlc_store import upsert, last_dt as manifest_last_dt, filter_trading_session
from structure import structure_events, time_at_price

try:                       # DB-live mirror sync (canonical store migration); CSV stays working set
    import db
except Exception:
    db = None


def _db_sync(label, fn):
    """Best-effort sync of a freshly-written slice into data/index.db. Never breaks the
    pull on a DB error — the CSV write already succeeded and is the fallback (STORAGE.md)."""
    if db is None:
        return
    try:
        fn()
    except Exception as e:
        print(f"  ⚠ DB sync {label} failed (CSV OK): {e}")


load_dotenv()

TWELVE_KEY = os.getenv("TWELVE_DATA_KEY")
FRED_KEY   = os.getenv("FRED_KEY")

# All time math in UTC. YEAR must be the ISO year (not calendar year) so the
# weekly_pull filename stays consistent with WEEK_NUM across the Dec/Jan boundary
# (e.g. Jan 1 can belong to ISO week 53 of the PRIOR year).
TODAY    = datetime.now(timezone.utc)
YEAR, WEEK_NUM, _ = TODAY.isocalendar()

# Defaults — overridden by load_instrument(). These match xauusd/config.py
# so legacy callers (compute.py, fetch.py) work without explicit load_instrument().
SYMBOL    = "XAU/USD"
SYM_CLEAN = "xauusd"
TD_DIR    = Path("data/twelvedata/xauusd")
FRED_DIR  = Path("data/fred")
PULL_DIR  = Path("data/weekly_pull/xauusd")
TICK_MULTIPLIER = 100   # $/lot per 1.0 price move (gold). Overridden by load_instrument.
PRICE_DP = 2            # price rounding precision (gold $-scale). FX→5. Overridden by load_instrument.

FRED_SERIES = ["DFII10", "DGS10", "T5YIE", "DFF", "VIXCLS"]
# DXY: ICE 6-currency index via yfinance DX-Y.NYB (not FRED DTWEXBGS which is 26-currency)
DXY_CSV       = Path("data/yahoo/DXY.csv")
GLD_HOLD_CSV  = Path("data/gld_holdings.csv")
COT_CACHE_DIR = Path("data/cftc")
ECON_DIR      = Path("data/econ_calendar")        # economic calendar (#1/#2, Forex Factory free JSON)
ECON_CSV      = ECON_DIR / "calendar.csv"
ECON_COLS     = ["date", "time_utc", "country", "event", "impact", "estimate", "actual", "prev", "unit"]
COMMODITIES_DIR = Path("data/commodities")        # intermarket (#3, yfinance)
NEWS_DIR      = Path("data/news")                  # news store (free RSS feeds, D025)
NEWS_CSV      = NEWS_DIR / "headlines.csv"
NEWS_COLS     = ["datetime_utc", "category", "headline", "source", "url", "summary", "related"]
# Per-pair headline keywords for the pull's NEWS FEED filter (US/Fed terms appended globally).
_NEWS_KEYWORDS = {
    "xauusd": ["gold", "bullion", "xau", "safe haven", "real yield"],
    "eurusd": ["euro", "ecb", "eurozone", "lagarde"],
    "gbpusd": ["pound", "sterling", "boe", "bank of england", "gilt"],
    "eurgbp": ["euro", "pound", "ecb", "boe"],
    "audusd": ["aussie", "australian dollar", "rba", "iron ore", "china", "copper"],
    "nzdusd": ["kiwi", "new zealand dollar", "rbnz", "dairy", "china"],
    "usdcad": ["loonie", "canadian dollar", "boc", "bank of canada", "oil", "crude", "wti"],
    "usdchf": ["franc", "swiss", "snb"],
    "usdjpy": ["yen", "boj", "bank of japan", "mof", "intervention", "ueda"],
    "eurjpy": ["yen", "euro", "boj", "ecb", "intervention"],
    "gbpjpy": ["yen", "pound", "boj", "boe", "intervention"],
}
TF_RESAMPLE = {"1h": "1h", "4h": "4h", "1day": "1D"}

# ── STEP 1: FETCH 15M + RESAMPLE ─────────────────────────────────────────────

MAX_15M_OUTPUTSIZE = 5000  # TD per-call cap; ~52 calendar days of 15M bars


def fetch_15m(force=False):
    last = manifest_last_dt("twelvedata", SYMBOL, "15min")
    if force or last is None:
        outputsize = 800
    else:
        # Size the request from the actual gap since the last stored bar, so a multi-day
        # lapse (vacation, dead sandbox) is backfilled instead of leaving a silent hole
        # that corrupts every resampled H4/D1 bar and ATR downstream.
        gap_secs  = (datetime.now(timezone.utc) - last.tz_localize("UTC")).total_seconds()
        gap_bars  = int(gap_secs / 900) + 50  # +50 margin for weekend/overlap
        if gap_bars > MAX_15M_OUTPUTSIZE:
            raise ValueError(
                f"15M gap since {last} exceeds one API page ({gap_bars} bars > {MAX_15M_OUTPUTSIZE}). "
                f"Run: bash scripts/pyrun.sh scripts/backfill_twelvedata.py --tf 15min --forward-only"
            )
        outputsize = max(200, gap_bars)
    r = requests.get("https://api.twelvedata.com/time_series", params={
        "symbol": SYMBOL, "interval": "15min",
        "outputsize": outputsize, "timezone": "UTC", "apikey": TWELVE_KEY,
    }, timeout=20)
    data = r.json()
    if "code" in data:
        raise ValueError(f"TD 15min: {data.get('message', data)}")
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col])
    df["volume"] = pd.to_numeric(df.get("volume", 0))
    df = df.sort_values("datetime").reset_index(drop=True)
    if not force and last is not None:
        df = df[df["datetime"] > last]
    return df

def resample_all():
    src = db.read_ohlc(SYMBOL, "15min") if db else None   # DB master; CSV fallback for cold start
    if src is None or src.empty:
        src = pd.read_csv(TD_DIR / "15min.csv")
    src = src.copy()
    src["datetime"] = pd.to_datetime(src["datetime"])
    for c in ["open", "high", "low", "close", "volume"]:
        if c in src.columns:
            src[c] = pd.to_numeric(src[c], errors="coerce")
    src = src.sort_values("datetime").set_index("datetime")
    results = []
    for tf, rule in TF_RESAMPLE.items():
        agg = src.resample(rule, label="left", closed="left").agg({
            "open": "first", "high": "max", "low": "min",
            "close": "last", "volume": "sum",
        }).dropna(subset=["open", "close"]).reset_index()
        info = upsert("twelvedata", SYMBOL, tf, agg)
        results.append((tf, len(agg), info["last_dt"]))
    return results

# ── STEP 2: FRED UPDATE ───────────────────────────────────────────────────────

def update_fred(force=False, series=None):
    """Fetch/append FRED series into the `macro_series` table. `series` defaults to the
    instrument's FRED_SERIES; pass an explicit list (e.g. commodity ids) to reuse the path.
    Incremental bookmark = MAX(date) from the DB (no _manifest.json)."""
    series = series if series is not None else FRED_SERIES
    results  = []
    for sid in series:
        csv_path  = FRED_DIR / f"{sid}.csv"
        last_date = db.last_series_date("macro_series", {"series_id": sid}) if db else None
        obs_start = ((datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
                     if (force or not last_date) else last_date)
        try:
            r   = requests.get("https://api.stlouisfed.org/fred/series/observations",
                               params={"series_id": sid, "observation_start": obs_start,
                                       "api_key": FRED_KEY, "file_type": "json"}, timeout=15)
            obs = r.json().get("observations", [])
            new = pd.DataFrame(obs)[["date", "value"]]
            new["value"] = pd.to_numeric(new["value"], errors="coerce")
            new = new.dropna()
            if not force and last_date:
                new = new[new["date"] > last_date]
            if not new.empty:
                prior = db.read_slice("macro_series", {"series_id": sid}, ["date", "value"]) if db else None
                if (prior is None or prior.empty) and csv_path.exists():
                    prior = pd.read_csv(csv_path)[["date", "value"]]
                if prior is not None and not prior.empty:
                    combined = (pd.concat([prior, new], ignore_index=True)
                                .drop_duplicates("date", keep="last")
                                .sort_values("date").reset_index(drop=True))
                else:
                    combined = new
                _db_sync(f"macro_series:{sid}", lambda c=combined, s=sid: db.sync_slice(
                    "macro_series", {"series_id": s},
                    c.assign(series_id=s)[["series_id", "date", "value"]],
                    index_cols=["series_id", "date"]))
            results.append((sid, len(new), db.last_series_date("macro_series", {"series_id": sid}) if db else "?"))
        except Exception as e:
            results.append((sid, f"ERROR: {e}", last_date or "?"))
    return results

# ── STEP 3: LOAD LOCAL DATA ───────────────────────────────────────────────────

def load_ohlc(path):
    # Read from the DB `ohlc` table (kept live by ohlc_store.upsert); CSV fallback on miss.
    p = Path(path)
    df = db.read_ohlc(p.parent.name, p.stem, source=p.parent.parent.name) if db else None
    if df is None or df.empty:
        df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["open", "high", "low", "close"])

def load_fred_local(sid):
    df = db.read_slice("macro_series", {"series_id": sid}, ["date", "value"]) if db else None
    if df is None or df.empty:
        df = pd.read_csv(FRED_DIR / f"{sid}.csv")[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna()

# ── STEP 4: INDICATORS ────────────────────────────────────────────────────────

def _drop_open_bar(df, freq_hours: float) -> pd.DataFrame:
    """Drop last row if its candle period hasn't closed yet (bar still forming).

    Uses UTC now vs (last_bar_open + freq_hours). Safe during weekends: the last
    bar of a closed session is always a completed candle, so nothing is dropped.
    """
    now = pd.Timestamp.now(tz="UTC").tz_localize(None)
    last_ts = df.index[-1] if isinstance(df.index, pd.DatetimeIndex) else pd.Timestamp(df.index[-1])
    if now < last_ts + pd.Timedelta(hours=freq_hours):
        return df.iloc[:-1]
    return df


def calc_atr(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return round(float(tr.rolling(p).mean().iloc[-1]), PRICE_DP)

def calc_atr_series(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(p).mean()

def calc_adx(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    up, down = h.diff(), -l.diff()
    plus  = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    tr_s  = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    tr14  = tr_s.ewm(alpha=1/p, adjust=False).mean()
    dip   = 100 * plus.ewm(alpha=1/p, adjust=False).mean() / tr14
    dim   = 100 * minus.ewm(alpha=1/p, adjust=False).mean() / tr14
    adx   = (100 * (dip-dim).abs() / (dip+dim)).ewm(alpha=1/p, adjust=False).mean()
    return round(float(adx.iloc[-1]), 1)

def calc_ema(series, span):
    return round(float(series.ewm(span=span, adjust=False).mean().iloc[-1]), PRICE_DP)

def calc_bollinger(df, p=20, k=2):
    """20,2 Bollinger bands on D1 close. Context indicator (not scored in v2).
    Returns mid/upper/lower + %B + position vs bands (last close)."""
    c = df["close"]
    mid = c.rolling(p).mean()
    sd  = c.rolling(p).std(ddof=0)
    upper = mid + k * sd
    lower = mid - k * sd
    last = float(c.iloc[-1])
    u, m, lo = float(upper.iloc[-1]), float(mid.iloc[-1]), float(lower.iloc[-1])
    pctb = (last - lo) / (u - lo) if u != lo else 0.5
    pos = "ABOVE upper (over-extended ↑ → fade short)" if last > u else \
          "BELOW lower (over-extended ↓ → fade long)" if last < lo else "inside bands"
    return {"upper": round(u, PRICE_DP), "mid": round(m, PRICE_DP),
            "lower": round(lo, PRICE_DP), "pctb": round(pctb, 2), "pos": pos}

def calc_rsi_series(df, p=14, n=10):
    delta = df["close"].diff()
    avg_g = delta.clip(lower=0).ewm(alpha=1/p, adjust=False).mean()
    avg_l = (-delta).clip(lower=0).ewm(alpha=1/p, adjust=False).mean()
    rsi   = (100 - 100/(1 + avg_g/avg_l)).round(1)
    tail  = rsi.iloc[-n:]
    return list(zip([str(i.date()) for i in tail.index], tail.values))

def calc_macd(df, fast=12, slow=26, sig=9, n=5):
    c    = df["close"]
    line = c.ewm(span=fast, adjust=False).mean() - c.ewm(span=slow, adjust=False).mean()
    sl   = line.ewm(span=sig, adjust=False).mean()
    hist = line - sl
    _md = max(2, PRICE_DP)  # MACD on FX needs more dp or rounds to 0.0
    return [(str(i.date()), round(float(line[i]),_md), round(float(sl[i]),_md), round(float(hist[i]),_md))
            for i in line.iloc[-n:].index]

# ── Oscillators / channels referenced by confluence_criteria (D025 — now COMPUTED,
#    previously eyeballed). All on CLOSED bars; computed for both D1 and H4. ──────

def calc_stochastic(df, k=14, d=3, smooth=3):
    h, l, c = df["high"], df["low"], df["close"]
    ll, hh = l.rolling(k).min(), h.rolling(k).max()
    fast_k = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    sk = fast_k.rolling(smooth).mean()
    sd = sk.rolling(d).mean()
    kv, dv = float(sk.iloc[-1]), float(sd.iloc[-1])
    state = "OVERSOLD" if kv < 20 else "OVERBOUGHT" if kv > 80 else "mid"
    return {"k": round(kv, 1), "d": round(dv, 1), "state": state}

def calc_williams_r(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    hh, ll = h.rolling(p).max(), l.rolling(p).min()
    wr = -100 * (hh - c) / (hh - ll).replace(0, np.nan)
    v = float(wr.iloc[-1])
    state = "OVERSOLD" if v < -80 else "OVERBOUGHT" if v > -20 else "mid"
    return {"wr": round(v, 1), "state": state}

def calc_cci(df, p=20):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    sma = tp.rolling(p).mean()
    mad = (tp - sma).abs().rolling(p).mean()
    cci = (tp - sma) / (0.015 * mad).replace(0, np.nan)
    v = float(cci.iloc[-1])
    state = "OVERBOUGHT (>+100)" if v > 100 else "OVERSOLD (<-100)" if v < -100 else "mid"
    return {"cci": round(v, 1), "state": state}

def calc_keltner(df, ema=20, atr_mult=2.0, atr_p=10):
    mid = df["close"].ewm(span=ema, adjust=False).mean()
    atr = calc_atr_series(df, atr_p)
    up, lo = mid + atr_mult * atr, mid - atr_mult * atr
    c = float(df["close"].iloc[-1]); u, m, d = float(up.iloc[-1]), float(mid.iloc[-1]), float(lo.iloc[-1])
    pos = "ABOVE upper (Keltner-high TAGGED → fade short)" if c >= u else \
          "BELOW lower (Keltner-low TAGGED → fade long)" if c <= d else "inside"
    return {"upper": round(u, PRICE_DP), "mid": round(m, PRICE_DP), "lower": round(d, PRICE_DP), "pos": pos}

def calc_donchian(df, p=20):
    up, lo = df["high"].rolling(p).max(), df["low"].rolling(p).min()
    c = float(df["close"].iloc[-1]); u, d = float(up.iloc[-1]), float(lo.iloc[-1])
    pos = "at/above upper (breakout)" if c >= u else "at/below lower (breakdown)" if c <= d else "mid-channel"
    return {"upper": round(u, PRICE_DP), "lower": round(d, PRICE_DP), "pos": pos}

def calc_ttm_squeeze(df, bb_p=20, bb_k=2.0, kc_p=20, kc_mult=1.5, atr_p=20):
    c = df["close"]
    sd = c.rolling(bb_p).std(ddof=0)
    mid = c.rolling(bb_p).mean()
    bb_u, bb_l = mid + bb_k * sd, mid - bb_k * sd
    atr = calc_atr_series(df, atr_p)
    kc_u, kc_l = mid + kc_mult * atr, mid - kc_mult * atr
    on = (bb_u < kc_u) & (bb_l > kc_l)   # BB inside KC = squeeze ON
    bars = 0
    for v in reversed(on.fillna(False).tolist()):
        if v: bars += 1
        else: break
    return {"on": bool(on.iloc[-1]), "bars": bars}

def calc_psar(df, step=0.02, mx=0.2):
    h, l = df["high"].to_numpy(), df["low"].to_numpy()
    n = len(df)
    if n < 3:
        return {"psar": None, "dir": "n/a", "flip": False}
    psar = np.zeros(n); bull = True; af = step
    ep = h[0]; psar[0] = l[0]
    for i in range(1, n):
        psar[i] = psar[i-1] + af * (ep - psar[i-1])
        if bull:
            if l[i] < psar[i]:
                bull = False; psar[i] = ep; ep = l[i]; af = step
            else:
                if h[i] > ep: ep = h[i]; af = min(af + step, mx)
        else:
            if h[i] > psar[i]:
                bull = True; psar[i] = ep; ep = h[i]; af = step
            else:
                if l[i] < ep: ep = l[i]; af = min(af + step, mx)
    c = float(df["close"].iloc[-1])
    flip = (n >= 2) and ((c > psar[-1]) != (float(df["close"].iloc[-2]) > psar[-2]))
    return {"psar": round(float(psar[-1]), PRICE_DP), "dir": "long" if c > psar[-1] else "short", "flip": bool(flip)}

def calc_supertrend(df, p=10, mult=3.0):
    h, l, c = df["high"], df["low"], df["close"]
    hl2 = (h + l) / 2
    atr = calc_atr_series(df, p)
    upper = hl2 + mult * atr; lower = hl2 - mult * atr
    n = len(df); cl = c.to_numpy()
    fu = upper.to_numpy().copy(); fl = lower.to_numpy().copy()
    dir_up = np.ones(n, dtype=bool)
    for i in range(1, n):
        fu[i] = min(fu[i], fu[i-1]) if cl[i-1] <= fu[i-1] else fu[i]
        fl[i] = max(fl[i], fl[i-1]) if cl[i-1] >= fl[i-1] else fl[i]
        if cl[i] > fu[i-1]: dir_up[i] = True
        elif cl[i] < fl[i-1]: dir_up[i] = False
        else: dir_up[i] = dir_up[i-1]
    line = fl[-1] if dir_up[-1] else fu[-1]
    flip = (n >= 2) and (dir_up[-1] != dir_up[-2])
    return {"dir": "up" if dir_up[-1] else "down", "value": round(float(line), PRICE_DP), "flip": bool(flip)}

def oscillator_block(df, label):
    """Compact oscillator/channel read for one timeframe → (text, extremes_list)."""
    st = calc_stochastic(df); wr = calc_williams_r(df); cci = calc_cci(df)
    kel = calc_keltner(df); don = calc_donchian(df); sq = calc_ttm_squeeze(df)
    ps = calc_psar(df); su = calc_supertrend(df)
    ex = []
    if st["state"] != "mid": ex.append(f"{label} Stoch {st['k']} {st['state']}")
    if wr["state"] != "mid": ex.append(f"{label} W%R {wr['wr']} {wr['state']}")
    if cci["state"] != "mid": ex.append(f"{label} CCI {cci['cci']} {cci['state']}")
    if "TAGGED" in kel["pos"]: ex.append(f"{label} {kel['pos'].split(' (')[0]}")
    if sq["on"]: ex.append(f"{label} TTM squeeze ON {sq['bars']}b")
    txt = (f"  {label}:  Stoch %K {st['k']}/%D {st['d']} ({st['state']}) | W%R {wr['wr']} ({wr['state']}) | "
           f"CCI {cci['cci']} ({cci['state']})\n"
           f"        Keltner u{kel['upper']}/m{kel['mid']}/l{kel['lower']} → {kel['pos']}\n"
           f"        Donchian u{don['upper']}/l{don['lower']} → {don['pos']} | "
           f"TTM squeeze {'ON ('+str(sq['bars'])+' bars)' if sq['on'] else 'OFF'}\n"
           f"        PSAR {ps['psar']} ({ps['dir']}{' FLIP' if ps['flip'] else ''}) | "
           f"Supertrend {su['value']} ({su['dir']}{' FLIP' if su['flip'] else ''})")
    return txt, ex

def entry_triggers_block(df_h1):
    """E0 entry-confirmation triggers on the latest CLOSED 1H bar, both directions (D025-E0).
    Backtest (e0-variants): RSI-reclaim > band-reclaim > pin/engulf for FX fades. This block makes
    them VERIFIABLE at /validate instead of eyeballed. Per-pair primary lives in confluence_criteria.
    """
    d = _drop_open_bar(df_h1, 1)
    if len(d) < 30:
        return "  (insufficient closed 1H bars for E0 triggers)"
    o, h, l, c = d["open"], d["high"], d["low"], d["close"]
    o1, c1, h1, l1 = float(o.iloc[-1]), float(c.iloc[-1]), float(h.iloc[-1]), float(l.iloc[-1])
    po, pc = float(o.iloc[-2]), float(c.iloc[-2])
    body = abs(c1 - o1)
    low_wick, up_wick = min(c1, o1) - l1, h1 - max(c1, o1)
    pin_bull = body > 0 and low_wick >= 2.5 * body
    pin_bear = body > 0 and up_wick >= 2.5 * body
    eng_bull = pc < po and c1 > o1 and c1 >= po and o1 <= pc
    eng_bear = pc > po and c1 < o1 and c1 <= po and o1 >= pc
    # RSI(14) reclaim — cross back THROUGH the 35/65 threshold (the strongest gate in backtest)
    delta = c.diff()
    ag = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    al = (-delta).clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    rsi = 100 - 100/(1 + ag/al)
    rn, rp = float(rsi.iloc[-1]), float(rsi.iloc[-2])
    rsi_rec_bull, rsi_rec_bear = rp < 35 <= rn, rp > 65 >= rn
    # Stochastic %K reclaim through 20/80
    ll, hh = l.rolling(14).min(), h.rolling(14).max()
    k = (100 * (c - ll) / (hh - ll).replace(0, np.nan)).rolling(3).mean()
    kn, kp = float(k.iloc[-1]), float(k.iloc[-2])
    st_rec_bull, st_rec_bear = kp < 20 <= kn, kp > 80 >= kn
    # Keltner(20 EMA, 2×ATR10) band reclaim — close re-enters the band
    mid = c.ewm(span=20, adjust=False).mean(); atr = calc_atr_series(d, 10)
    kl, ku = mid - 2 * atr, mid + 2 * atr
    bnd_bull = float(c.iloc[-2]) < float(kl.iloc[-2]) and c1 >= float(kl.iloc[-1])
    bnd_bear = float(c.iloc[-2]) > float(ku.iloc[-2]) and c1 <= float(ku.iloc[-1])

    def fired(d):
        return " · ".join(d) if d else "none"
    longs, shorts = [], []
    if rsi_rec_bull: longs.append(f"RSI-reclaim✦ ({rp:.0f}→{rn:.0f})")
    if bnd_bull:     longs.append("band-reclaim (Keltner-low re-entry)")
    if st_rec_bull:  longs.append(f"Stoch-reclaim ({kp:.0f}→{kn:.0f})")
    if pin_bull:     longs.append("pin (bull)")
    if eng_bull:     longs.append("engulf (bull)")
    if rsi_rec_bear: shorts.append(f"RSI-reclaim✦ ({rp:.0f}→{rn:.0f})")
    if bnd_bear:     shorts.append("band-reclaim (Keltner-high re-entry)")
    if st_rec_bear:  shorts.append(f"Stoch-reclaim ({kp:.0f}→{kn:.0f})")
    if pin_bear:     shorts.append("pin (bear)")
    if eng_bear:     shorts.append("engulf (bear)")
    bar_t = str(d.index[-1])
    return (f"  latest closed 1H bar: {bar_t}  (RSI {rn:.0f}, Stoch %K {kn:.0f})\n"
            f"  LONG-confirm fired:  {fired(longs)}\n"
            f"  SHORT-confirm fired: {fired(shorts)}\n"
            f"  ✦ = RSI-reclaim is the highest-R E0 gate (backtest); per-pair primary in "
            f"confluence_criteria. Toward zone dir only.")

def calc_pivots(d1_df):
    gw = d1_df.resample("W").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    b  = gw.iloc[-2]
    pp = (b["high"] + b["low"] + b["close"]) / 3
    return {"PP": round(pp,PRICE_DP),
            "R1": round(2*pp-b["low"],PRICE_DP),    "R2": round(pp+b["high"]-b["low"],PRICE_DP),
            "R3": round(b["high"]+2*(pp-b["low"]),PRICE_DP),
            "S1": round(2*pp-b["high"],PRICE_DP),   "S2": round(pp-b["high"]+b["low"],PRICE_DP),
            "S3": round(b["low"]-2*(b["high"]-pp),PRICE_DP)}

def swing_points(df, n=5):
    highs, lows = [], []
    for i in range(n, len(df)-n):
        if df["high"].iloc[i] == df["high"].iloc[i-n:i+n+1].max():
            highs.append((str(df.index[i].date()), round(float(df["high"].iloc[i]),PRICE_DP)))
        if df["low"].iloc[i] == df["low"].iloc[i-n:i+n+1].min():
            lows.append((str(df.index[i].date()), round(float(df["low"].iloc[i]),PRICE_DP)))
    return highs[-5:], lows[-5:]

def fib_levels(lo, hi):
    d = hi - lo
    return {"swing_low": round(lo,PRICE_DP), "swing_high": round(hi,PRICE_DP),
            "78.6%": round(hi-0.786*d,PRICE_DP), "61.8%": round(hi-0.618*d,PRICE_DP),
            "50.0%": round(hi-0.500*d,PRICE_DP), "38.2%": round(hi-0.382*d,PRICE_DP),
            "ext_127.2%": round(lo+1.272*d,PRICE_DP), "ext_161.8%": round(lo+1.618*d,PRICE_DP)}

def weekend_gap(h4_full, h4_trade):
    fri = h4_trade[h4_trade.index.dayofweek == 4]
    if fri.empty:
        return None
    last_fri_ts = fri.index[-1]
    fri_close   = float(fri.iloc[-1]["close"])
    after = h4_full[h4_full.index > last_fri_ts]
    if after.empty:
        return None
    next_ts   = after.index[0]
    next_open = float(after.iloc[0]["open"])
    gap_d   = next_open - fri_close
    gap_pct = (gap_d / fri_close) * 100
    flag    = ("RE-FORECAST" if abs(gap_pct) > 1.00 else
               "WARNING"     if abs(gap_pct) > 0.50 else
               "NOTE"        if abs(gap_pct) > 0.20 else "NOISE")
    return {"fri_date": str(last_fri_ts), "fri_close": round(fri_close,PRICE_DP),
            "next_date": str(next_ts),     "next_open": round(next_open,PRICE_DP),
            "gap_$": round(gap_d,PRICE_DP), "gap_pct": round(gap_pct,3), "flag": flag}

# ── STEP 5: EXTERNAL FETCHES (no API key) ────────────────────────────────────

def volume_profile(ticker="GC=F", period="3mo", bins=50):
    try:
        df = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=True)
        if df.empty:
            return {"error": "empty"}
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        edges = np.linspace(float(df["Low"].min()), float(df["High"].max()), bins+1)
        vols  = np.zeros(bins)
        for _, row in df.iterrows():
            lo, hi, vol = float(row["Low"]), float(row["High"]), float(row["Volume"])
            br = hi - lo
            if br == 0 or vol == 0:
                continue
            for i in range(bins):
                ov = min(hi, edges[i+1]) - max(lo, edges[i])
                if ov > 0:
                    vols[i] += vol * (ov / br)
        poc_idx = int(np.argmax(vols))
        poc = round((edges[poc_idx]+edges[poc_idx+1])/2, PRICE_DP)
        total = vols.sum(); target = total*0.70
        lo_i = hi_i = poc_idx; acc = vols[poc_idx]
        while acc < target and (lo_i > 0 or hi_i < bins-1):
            add_lo = vols[lo_i-1] if lo_i > 0 else 0
            add_hi = vols[hi_i+1] if hi_i < bins-1 else 0
            if add_lo >= add_hi and lo_i > 0: lo_i -= 1; acc += add_lo
            elif hi_i < bins-1:               hi_i += 1; acc += add_hi
            else:                             lo_i -= 1; acc += add_lo
        return {"POC": poc, "VAH": round(edges[hi_i+1],PRICE_DP), "VAL": round(edges[lo_i],PRICE_DP)}
    except Exception as e:
        return {"error": str(e)}

def fetch_cot():
    """CFTC Legacy report (non-commercial long/short). Source: cftc.gov yearly zip.
    Caches deahistfo{YEAR}.zip (combined Futures-Only, all markets) in data/cftc/.
    Returns latest two weekly reports for the instrument's COT contract.
    """
    import zipfile, io
    contract = (_instrument_cfg.COT_CONTRACT_NAME if _instrument_cfg
                else "GOLD - COMMODITY EXCHANGE INC.")
    try:
        COT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        year = datetime.now(timezone.utc).year
        zip_path = COT_CACHE_DIR / f"deahistfo{year}.zip"
        # refetch if older than 24h or missing
        stale = (not zip_path.exists() or
                 (time.time() - zip_path.stat().st_mtime) > 24*3600)
        if stale:
            r = requests.get(f"https://www.cftc.gov/files/dea/history/deahistfo{year}.zip",
                             timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            zip_path.write_bytes(r.content)
        z = zipfile.ZipFile(zip_path)
        df = pd.read_csv(z.open(z.namelist()[0]), low_memory=False)
        # Exact match: main contract only (excludes MICRO variants sharing same date rows)
        mask = df["Market and Exchange Names"].astype(str).str.strip() == contract
        g = df[mask].copy()
        g["date"] = pd.to_datetime(g["As of Date in Form YYYY-MM-DD"], errors="coerce")
        g = g.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
        if g.empty:
            return {"error": f"no rows for contract '{contract}' in zip"}
        long_col  = "Noncommercial Positions-Long (All)"
        short_col = "Noncommercial Positions-Short (All)"
        latest = g.iloc[-1]; prev = g.iloc[-2] if len(g) >= 2 else None
        net_now  = int(latest[long_col]) - int(latest[short_col])
        net_prev = (int(prev[long_col]) - int(prev[short_col])) if prev is not None else None
        return {"date": latest["date"].strftime("%Y-%m-%d"),
                "long": int(latest[long_col]),
                "short": int(latest[short_col]),
                "net": net_now, "net_prev": net_prev,
                "net_chg": (net_now-net_prev) if net_prev is not None else None}
    except Exception as e:
        return {"error": str(e)}

def fetch_gld_flows():
    """GLD ETF holdings via yfinance totalAssets + spot gold → tonnes.
    Stores daily snapshot in data/gld_holdings.csv to compute wk/mo deltas.
    """
    try:
        t = yf.Ticker("GLD")
        total_assets = float(t.info.get("totalAssets") or 0)
        if total_assets <= 0:
            return {"error": "yfinance totalAssets unavailable"}
        # spot gold (use latest D1 close from our pull)
        d1 = load_ohlc(TD_DIR / "1day.csv").sort_index()   # DB-backed (CSV fallback)
        spot = float(d1["close"].iloc[-1])
        oz_per_tonne = 32150.7466
        tonnes = total_assets / (spot * oz_per_tonne)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Append to history CSV (idempotent — keep latest per date)
        GLD_HOLD_CSV.parent.mkdir(parents=True, exist_ok=True)
        hist = db.read_table("gld_holdings") if db else None
        if (hist is None or hist.empty):
            hist = pd.read_csv(GLD_HOLD_CSV) if GLD_HOLD_CSV.exists() \
                else pd.DataFrame(columns=["date", "tonnes", "aum_usd", "spot"])
        hist = pd.concat([hist, pd.DataFrame([{
            "date": today, "tonnes": round(tonnes, 2),
            "aum_usd": total_assets, "spot": spot
        }])], ignore_index=True).drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
        _db_sync("gld_holdings", lambda h=hist: db.sync_table("gld_holdings", h))

        wk_chg = round(tonnes - float(hist.iloc[-6]["tonnes"]), 2) if len(hist) >= 6 else None
        mo_chg = round(tonnes - float(hist.iloc[-21]["tonnes"]), 2) if len(hist) >= 21 else None
        return {"date": today, "tonnes": round(tonnes, 2),
                "wk_chg": wk_chg, "mo_chg": mo_chg,
                "aum_usd": round(total_assets / 1e9, 2)}
    except Exception as e:
        return {"error": str(e)}

def fetch_dxy(force=False):
    """ICE DXY via yfinance DX-Y.NYB. Appends to data/yahoo/DXY.csv (date,value)."""
    try:
        DXY_CSV.parent.mkdir(parents=True, exist_ok=True)
        # always pull last 90d, dedupe + merge
        h = yf.Ticker("DX-Y.NYB").history(period="90d")
        if h.empty:
            return {"error": "yfinance empty"}
        new = pd.DataFrame({
            "date": h.index.strftime("%Y-%m-%d"),
            "value": h["Close"].round(3).values,
        })
        prior = db.read_slice("market_series", {"source": "yahoo", "symbol": "DXY"},
                              ["date", "value"]) if db else None
        if (prior is None or prior.empty) and DXY_CSV.exists():
            prior = pd.read_csv(DXY_CSV)[["date", "value"]]
        if prior is not None and not prior.empty and not force:
            combined = (pd.concat([prior, new], ignore_index=True)
                        .drop_duplicates("date", keep="last")
                        .sort_values("date").reset_index(drop=True))
        else:
            combined = new
        _db_sync("market_series:yahoo:DXY", lambda c=combined: db.sync_slice(
            "market_series", {"source": "yahoo", "symbol": "DXY"},
            c.assign(source="yahoo", symbol="DXY")[["source", "symbol", "date", "value"]],
            index_cols=["source", "symbol", "date"]))
        return {"last_date": str(combined["date"].iloc[-1]), "value": float(combined["value"].iloc[-1]), "rows": len(combined)}
    except Exception as e:
        return {"error": str(e)}

def load_dxy_local():
    """Returns DataFrame indexed by date with 'value' column (matches load_fred_local interface)."""
    df = db.read_slice("market_series", {"source": "yahoo", "symbol": "DXY"},
                       ["date", "value"]) if db else None
    if df is None or df.empty:
        df = pd.read_csv(DXY_CSV)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna()

# ── ECONOMIC CALENDAR (#1/#2 — Forex Factory free JSON) ───────────────────────

# Forex Factory free calendar (faireconomy.media) — NO API KEY. (Prior provider was premium-gated
# → "no access" on its free tier, so we moved to this key-free feed.) Each feed is a
# JSON array of {title, country (currency code), date (ISO+offset), impact, forecast, previous,
# (sometimes) actual}. We map currency→ISO-2 so check_econ_calendar.py reads it unchanged.
FF_CAL_URLS = {
    "lastweek": "https://nfs.faireconomy.media/ff_calendar_lastweek.json",
    "thisweek": "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
    "nextweek": "https://nfs.faireconomy.media/ff_calendar_nextweek.json",
}
FF_CCY_TO_ISO = {"USD": "US", "EUR": "EU", "GBP": "GB", "JPY": "JP", "AUD": "AU",
                 "NZD": "NZ", "CAD": "CA", "CHF": "CH", "CNY": "CN"}


def fetch_econ_calendar(force=False, days_back=10, days_fwd=10):
    """Forex Factory free JSON (faireconomy.media) → data/econ_calendar/calendar.csv.
    NO API key. Pulls last/this/next week (~±10d), maps currency→ISO-2 country, converts each
    event time to UTC, and merges/dedups on date+country+event so a re-pull backfills `actual`
    where the feed provides it (feeds the #2 surprise). days_back/days_fwd kept for signature
    compatibility (the FF feeds are fixed-week). Non-fatal — /weekly web-search fallback covers gaps."""
    headers = {"User-Agent": "Mozilla/5.0 (trading-brain econ-calendar)"}
    recs, errors = [], []
    for tag, url in FF_CAL_URLS.items():
        try:
            r = requests.get(url, headers=headers, timeout=20)
            rows = r.json()
        except Exception as ex:
            errors.append(f"{tag}:{ex}")
            continue
        if not isinstance(rows, list):
            errors.append(f"{tag}:unexpected payload")
            continue
        for e in rows:
            raw_dt = str(e.get("date", "") or "")
            date_s, time_s = "", ""
            if raw_dt:
                try:
                    dt = datetime.fromisoformat(raw_dt).astimezone(timezone.utc)
                    date_s, time_s = dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")
                except ValueError:
                    date_s = raw_dt[:10]
            ccy = str(e.get("country", "") or "").upper().strip()
            recs.append({
                "date": date_s, "time_utc": time_s,
                "country": FF_CCY_TO_ISO.get(ccy, ccy), "event": e.get("title", ""),
                "impact": e.get("impact", ""), "estimate": e.get("forecast", ""),
                "actual": e.get("actual", ""), "prev": e.get("previous", ""),
                "unit": "",
            })
    if not recs:
        return {"error": f"FF calendar fetch failed ({'; '.join(errors) or 'no rows'})"}
    new = pd.DataFrame(recs, columns=ECON_COLS)
    new = new[new["date"].astype(str).str.len() == 10]   # drop unparseable dates
    ECON_DIR.mkdir(parents=True, exist_ok=True)
    if not force:
        old = db.read_table("econ_calendar") if db else None
        if (old is None or old.empty) and ECON_CSV.exists():
            old = pd.read_csv(ECON_CSV, dtype=str).fillna("")
        if old is not None and not old.empty:
            new = pd.concat([old[ECON_COLS], new.astype(str)], ignore_index=True)
    new = (new.astype(str)
           .drop_duplicates(["date", "country", "event"], keep="last")
           .sort_values(["date", "time_utc"]).reset_index(drop=True))
    _db_sync("econ_calendar", lambda n=new: db.sync_table("econ_calendar", n))
    return {"rows": len(new), "this_pull": len(recs), "source": "faireconomy(FF)",
            "last": new["date"].iloc[-1] if len(new) else "?",
            "warn": ("partial: " + "; ".join(errors)) if errors else ""}

# ── NEWS STORE (free RSS feeds — no API key, D025; key-free feed since 2026-06-15) ──

# Key-free forex/markets RSS, matching the key-free Forex Factory calendar feed. Standard RSS 2.0 <item>{title,link,pubDate,description?}. Reachable
# from the scheduled-task sandbox (DailyFX 403s, ForexLive 301s → excluded). check_news.py
# filters on headline text, so the item titles drive relevance.
NEWS_RSS_SOURCES = [
    ("FXStreet",      "forex", "https://www.fxstreet.com/rss/news"),
    ("Investing.com", "forex", "https://www.investing.com/rss/news_1.rss"),
]
# currency tags for the `related` column (schema parity; relevance filtering uses headline text)
_NEWS_REL_KW = {
    "XAU": ["gold", "bullion", "xau"],
    "USD": ["dollar", "fed", "fomc", "powell", "treasury"],
    "EUR": ["euro", "ecb", "eurozone", "lagarde"],
    "GBP": ["pound", "sterling", "boe", "gilt"],
    "JPY": ["yen", "boj", "mof", "ueda", "intervention"],
    "AUD": ["aussie", "australian dollar", "rba", "iron ore"],
    "NZD": ["kiwi", "new zealand", "rbnz", "dairy"],
    "CAD": ["loonie", "canadian dollar", "boc", "crude", "wti", " oil"],
    "CHF": ["franc", "swiss", "snb"],
}


def _parse_rss_date(s):
    """RSS pubDate → 'YYYY-MM-DDTHH:MM:SSZ' (UTC). Handles RFC822 (FXStreet, incl. bare 'Z')
    and ISO-ish 'YYYY-MM-DD HH:MM:SS' (Investing.com). Naive timestamps assumed UTC."""
    from email.utils import parsedate_to_datetime
    s = (s or "").strip()
    for f in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S Z",
              "%a, %d %b %Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(s, f)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ""


def _derive_related(text):
    t = (text or "").lower()
    return ",".join(c for c, kws in _NEWS_REL_KW.items() if any(k in t for k in kws))


def fetch_news(force=False, categories=None):
    """Free RSS forex/markets feeds → data/news/headlines.csv (deduped on url). Accumulates a
    cross-week corpus for Section 2 + the Step 2b retrospective. Key-free since 2026-06-15
    (matches the FF calendar feed). `categories` kept for signature compatibility
    (unused). Non-fatal on failure — /weekly web-search fallback covers gaps."""
    import xml.etree.ElementTree as ET
    headers = {"User-Agent": "Mozilla/5.0 (trading-brain news)"}
    recs, errors = [], []
    for source, cat, url in NEWS_RSS_SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            root = ET.fromstring(r.content)
        except Exception as ex:
            errors.append(f"{source}:{ex}")
            continue
        for it in root.iter("item"):
            def g(tag):
                el = it.find(tag)
                return (el.text or "").strip() if el is not None and el.text else ""
            title, link = g("title"), g("link")
            if not title or not link:
                continue
            summary = g("description")[:400]
            recs.append({"datetime_utc": _parse_rss_date(g("pubDate")), "category": cat,
                         "headline": title, "source": source, "url": link,
                         "summary": summary, "related": _derive_related(title + " " + summary)})
    if not recs:
        return {"error": f"RSS news fetch failed ({'; '.join(errors) or 'no rows'})"}
    new = pd.DataFrame(recs, columns=NEWS_COLS)
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    if not force:
        old = db.read_table("news") if db else None
        if (old is None or old.empty) and NEWS_CSV.exists():
            old = pd.read_csv(NEWS_CSV, dtype=str).fillna("")
        if old is not None and not old.empty:
            new = (pd.concat([old[NEWS_COLS], new.astype(str)], ignore_index=True)
                   .drop_duplicates("url", keep="last")
                   .sort_values("datetime_utc").reset_index(drop=True))
    _db_sync("news", lambda n=new: db.sync_table("news", n))
    return {"rows": len(new), "this_pull": len(recs),
            "source": "rss(" + "+".join(s for s, _, _ in NEWS_RSS_SOURCES) + ")",
            "last": new["datetime_utc"].max() if len(new) else "?",
            "warn": ("partial: " + "; ".join(errors)) if errors else ""}

# ── INTERMARKET COMMODITIES (#3 — yfinance, AUD/NZD only) ─────────────────────

def fetch_commodities_yf(tickers: dict):
    """Daily close for yfinance commodity tickers (e.g. {'copper':'HG=F'}) →
    data/commodities/{name}.csv (date,value). Reuses the yfinance pattern from fetch_dxy."""
    out = {}
    COMMODITIES_DIR.mkdir(parents=True, exist_ok=True)
    for name, tk in tickers.items():
        try:
            h = yf.Ticker(tk).history(period="120d")
            if h.empty:
                out[name] = {"error": "empty"}; continue
            new = pd.DataFrame({"date": h.index.strftime("%Y-%m-%d"),
                                "value": h["Close"].round(4).values})
            p = COMMODITIES_DIR / f"{name}.csv"
            prior = db.read_slice("market_series", {"source": "commodities", "symbol": name},
                                  ["date", "value"]) if db else None
            if (prior is None or prior.empty) and p.exists():
                prior = pd.read_csv(p)[["date", "value"]]
            if prior is not None and not prior.empty:
                new = (pd.concat([prior, new], ignore_index=True)
                       .drop_duplicates("date", keep="last")
                       .sort_values("date").reset_index(drop=True))
            _db_sync(f"market_series:commodities:{name}", lambda n=new, nm=name: db.sync_slice(
                "market_series", {"source": "commodities", "symbol": nm},
                n.assign(source="commodities", symbol=nm)[["source", "symbol", "date", "value"]],
                index_cols=["source", "symbol", "date"]))
            out[name] = {"rows": len(new), "last": new["date"].iloc[-1],
                         "value": float(new["value"].iloc[-1])}
        except Exception as ex:
            out[name] = {"error": str(ex)}
    return out

def load_commodity_local(name: str):
    """Load a commodity series → date-indexed 'value' frame. DB first (market_series then
    macro_series), CSV fallback (commodities/ then fred/)."""
    if db:
        df = db.read_slice("market_series", {"source": "commodities", "symbol": name}, ["date", "value"])
        if df is None or df.empty:
            df = db.read_slice("macro_series", {"series_id": name}, ["date", "value"])
        if df is not None and not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            return df.dropna()
    for d in (COMMODITIES_DIR, FRED_DIR):
        p = d / f"{name}.csv"
        if p.exists():
            df = pd.read_csv(p, parse_dates=["date"]).set_index("date").sort_index()
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            return df.dropna()
    return None

# ── MAIN ──────────────────────────────────────────────────────────────────────

def fetch_and_update(force=False):
    """Fetch 15M bars, resample, update FRED CSVs. Returns brief status lines.
    Called by both run() and --fetch-only mode (used by /validate)."""
    if not TWELVE_KEY or not FRED_KEY:
        print("ERROR: TWELVE_DATA_KEY or FRED_KEY not set in .env"); sys.exit(1)

    print("Fetching 15M bars from Twelve Data (1 API call)...")
    new_15m  = fetch_15m(force=force)
    info_15m = upsert("twelvedata", SYMBOL, "15min", new_15m)
    print(f"  → {len(new_15m)} new 15M bars | last: {info_15m.get('last_dt', 'n/a (already current)')}")
    print("Resampling 15min → 1h / 4h / 1day...")
    resample_results = resample_all()
    for tf, rows, last in resample_results:
        print(f"  → {tf}: {rows} rows | last: {last}")
    print("Updating FRED CSVs...")
    fred_results = update_fred(force=force)
    for sid, n, last in fred_results:
        print(f"  → {sid}: {n} new | last: {last}")
    print("Updating DXY (ICE 6-currency, yfinance DX-Y.NYB)...")
    dxy_res = fetch_dxy(force=force)
    if "error" in dxy_res:
        print(f"  → DXY fetch FAILED: {dxy_res['error']}")
    else:
        print(f"  → DXY: {dxy_res['rows']} rows | last {dxy_res['last_date']} = {dxy_res['value']}")

    # Economic calendar (#1/#2) — shared across instruments, one CSV. Non-fatal on failure.
    print("Updating economic calendar (Forex Factory free JSON)...")
    econ_res = fetch_econ_calendar(force=force)
    if "error" in econ_res:
        print(f"  → econ calendar SKIPPED: {econ_res['error']} (web-search fallback still applies)")
    else:
        print(f"  → econ calendar: {econ_res['rows']} rows ({econ_res['this_pull']} this pull), last {econ_res['last']}")

    # News store (free RSS feeds) — shared across instruments, one CSV. Non-fatal.
    print("Updating news store (RSS)...")
    news_res = fetch_news(force=force)
    if "error" in news_res:
        print(f"  → news SKIPPED: {news_res['error']} (web-search fallback still applies)")
    else:
        print(f"  → news: {news_res['rows']} rows ({news_res['this_pull']} this pull), last {news_res['last']}")

    # Intermarket commodities (#3) — only pairs that declare them (AUD/NZD).
    cfg = _instrument_cfg
    com_fred = list(getattr(cfg, "COMMODITY_FRED", []) or [])
    com_yf   = dict(getattr(cfg, "COMMODITY_YF", {}) or {})
    if com_fred:
        print(f"Updating commodity FRED series {com_fred}...")
        for sid, n, last in update_fred(force=force, series=com_fred):
            print(f"  → {sid}: {n} new | last: {last}")
    if com_yf:
        print(f"Updating commodity yfinance series {list(com_yf)}...")
        for name, info in fetch_commodities_yf(com_yf).items():
            print(f"  → {name}: {info.get('error') or str(info.get('value')) + ' (' + str(info.get('rows')) + ' rows)'}")

    print("✅ CSVs ready.")
    return info_15m


def cache_check(force=False):
    """Returns (out_path, cache_hit_bool). Encapsulates cache-policy gate."""
    out_path = PULL_DIR / f"weekly_pull_{YEAR}_W{WEEK_NUM:02d}.txt"
    if out_path.exists() and not force:
        age_s = time.time() - out_path.stat().st_mtime
        mtime = datetime.fromtimestamp(out_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        size  = out_path.stat().st_size
        if age_s < CACHE_FRESH_SECONDS:
            print(f"✅ Cache hit: {out_path} ({size} bytes, generated {mtime}, age {int(age_s)}s < {CACHE_FRESH_SECONDS}s)")
            print(f"   Skipping fetch (fresh). Use --force to refetch.")
            return out_path, True
        if is_market_closed_utc():
            print(f"✅ Cache hit: {out_path} ({size} bytes, generated {mtime}, age {int(age_s/60)}min)")
            print(f"   Skipping fetch (market closed — weekend). Use --force to refetch.")
            return out_path, True
        print(f"⚠️  Cache stale ({int(age_s/60)}min old, market open) — refetching.")
    return out_path, False


def build_snapshot():
    """Read CSVs (no network), compute indicators, write pull snapshot file. Returns path."""
    out_path = PULL_DIR / f"weekly_pull_{YEAR}_W{WEEK_NUM:02d}.txt"
    return _compute_and_write(out_path)


def run(force=False):
    out_path, hit = cache_check(force=force)
    if hit:
        return str(out_path)

    # 1. Fetch + resample + FRED
    fetch_and_update(force=force)

    # 2. Compute + write
    return _compute_and_write(out_path)


def _compute_and_write(out_path):
    cfg = _instrument_cfg  # may be None if called without load_instrument (legacy mode)

    # Load local data
    print("Computing indicators...")
    price_d       = load_ohlc(TD_DIR / "1day.csv")
    price_h4_full = load_ohlc(TD_DIR / "4h.csv")
    price_h4      = filter_trading_session(price_h4_full.reset_index(), "4h").set_index("datetime")
    price_h1      = load_ohlc(TD_DIR / "1h.csv")   # for time-at-price (USD-base VP substitute)

    # Drop open (still-forming) candle before ATR calcs — fully closed bars only
    price_d_closed  = _drop_open_bar(price_d,  24)   # D1 bar closes 24h after open
    price_h4_closed = _drop_open_bar(price_h4,  4)   # H4 bar closes 4h after open

    # External fetches — conditional on instrument config
    vp_ticker = cfg.VP_TICKER if cfg else "GC=F"
    if vp_ticker:
        print(f"  → Volume Profile (yfinance {vp_ticker})...")
        vp = volume_profile(ticker=vp_ticker)
    else:
        # USD-base pairs: futures chart is the pair upside-down — VP levels unusable.
        vp = {"disabled": f"VP disabled for {SYM_CLEAN} (no usable futures proxy)"}

    if cfg is None or cfg.COT_ENABLED:
        print("  → COT (CFTC)...")
        cot = fetch_cot()
    else:
        cot = {"error": f"COT disabled for {SYM_CLEAN} (system TBD)"}

    if cfg is None or cfg.ETF_ENABLED:
        etf_label = cfg.ETF_TICKER if cfg else "GLD"
        print(f"  → ETF flows ({etf_label})...")
        gld = fetch_gld_flows()
    else:
        gld = {"error": f"ETF flows disabled for {SYM_CLEAN} (no equivalent ETF)"}

    # Alias back to local names used throughout the rest of this function
    gold_d       = price_d
    gold_h4_full = price_h4_full
    gold_h4      = price_h4
    gold_d_closed  = price_d_closed
    gold_h4_closed = price_h4_closed

    # 5. Indicators
    atr_d  = calc_atr(gold_d_closed)
    atr_h4 = calc_atr(gold_h4_closed)

    d1_atr_s   = calc_atr_series(gold_d_closed)
    atr_d_now  = round(float(d1_atr_s.iloc[-1]), PRICE_DP)
    atr_d_med  = round(float(d1_atr_s.iloc[-20:].median()), PRICE_DP)
    compressed = atr_d_now < atr_d_med

    # All indicators on CLOSED bars only (same policy as ATR) — a forming bar would
    # make RSI/ADX/MACD drift intraday and two same-day runs disagree.
    adx_val   = calc_adx(gold_d_closed)
    ema50     = calc_ema(gold_d_closed["close"], 50)
    ema200    = calc_ema(gold_d_closed["close"], 200)
    rsi_vals  = calc_rsi_series(gold_d_closed)
    macd_rows = calc_macd(gold_d_closed)
    boll      = calc_bollinger(gold_d_closed)
    gap       = weekend_gap(gold_h4_full, gold_h4)
    pvt       = calc_pivots(gold_d_closed)
    sh, sl    = swing_points(gold_d_closed)
    sh_h4, sl_h4 = swing_points(gold_h4_closed)

    rec_hi = sh[-1][1] if sh else float(gold_d_closed["high"].tail(30).max())
    rec_lo = sl[-1][1] if sl else float(gold_d_closed["low"].tail(30).min())
    fibs   = fib_levels(rec_lo, rec_hi)

    # FRED derived — shared risk series
    dxy = load_dxy_local(); vix = load_fred_local("VIXCLS")
    ff  = load_fred_local("DFF")
    gc = float(gold_d["close"].iloc[-1]); gp = float(gold_d["close"].iloc[-6])
    dc = float(dxy["value"].iloc[-1]);    dp = float(dxy["value"].iloc[-6])

    # SL per constitution v2: H4 ATR is the FLOOR; half-D1 only lifts it (never shrinks).
    #   if 0.5×D1 < H4 → SL = H4   else → SL = avg(0.5×D1, H4)
    d1_floor = 0.5 * atr_d
    sl_v2 = atr_h4 if d1_floor < atr_h4 else round((d1_floor + atr_h4) / 2, PRICE_DP)
    lots_raw = round(2000 / (sl_v2 * TICK_MULTIPLIER), 3) if sl_v2 > 0 else 0.0
    lots_fl  = max(0.01, int(lots_raw * 100) / 100)  # floor to 0.01-lot step, broker min 0.01

    adx_regime = ("TRENDING (favor continuation/trend setups; floor 6.0)"      if adx_val > 25  else
                  "TRANSITIONAL (chop risk → /validate floor raised to 6.5)"   if adx_val >= 20 else
                  "RANGING (favor reversal/counter at zone edges; floor 6.0)")

    rsi_now = rsi_vals[-1][1]; rsi_old = rsi_vals[0][1]

    # ── MACRO block + baselines — driver depends on instrument MACRO_MODE ──────
    display = _instrument_cfg.DISPLAY_NAME if _instrument_cfg else SYM_CLEAN.upper()
    macro_mode = getattr(cfg, "MACRO_MODE", "real_yield")
    baseline_extra = ""  # optional extra baseline lines (e.g. FX policy diff)

    if macro_mode == "rate_diff":
        # FX vs USD: US 2Y slope = direction (USD rate momentum); DFF − foreign policy = carry regime.
        # USD-base pairs (USDJPY etc., USD_BETA_SIGN=+1): USD strength is BULLISH the pair — flip labels.
        # RATE_FOREIGN=None (AUD/NZD/CAD/CHF — no daily FRED policy series; carry-diff proven DEAD,
        # D021/D024): skip the policy-diff carry lines, keep US2Y direction + VIX.
        us  = load_fred_local(cfg.RATE_US)        # US 2Y (DGS2)
        us_now  = float(us["value"].iloc[-1]); us_prev = float(us["value"].iloc[-6])
        us_20d  = us["value"].iloc[-21:]
        us_slope = float(np.polyfit(range(len(us_20d)), us_20d.values, 1)[0])
        us_drift = us_now - float(us["value"].iloc[-2])
        ffr      = float(ff["value"].iloc[-1])
        usd_base = getattr(cfg, "USD_BETA_SIGN", -1) > 0
        up_lbl   = (f'RISING ✅ (USD strength, bullish {display})' if usd_base
                    else f'RISING ⚠  (USD strength, bearish {display})')
        dn_lbl   = (f'FALLING ⚠  (USD softness, bearish {display})' if usd_base
                    else f'FALLING ✅ (USD softness, bullish {display})')
        macro_block = (
            f"US 2Y (DGS2):     {us_now}% (was {us_prev}% ~1w ago, Δ {round(us_now-us_prev,3):+}%)\n"
            f"  → {up_lbl if us_now > us_prev else dn_lbl}\n"
            f"  20d slope: {us_slope:+.4f} %/day  {'(rising trend)' if us_slope > 0 else '(falling trend)'}\n"
            f"  1d drift:  {us_drift:+.3f}%\n"
            f"Fed Funds:        {ffr:.2f}%\n")
        if getattr(cfg, "RATE_FOREIGN", None):
            fp  = load_fred_local(cfg.RATE_FOREIGN)   # foreign policy rate (ECBDFR / SONIA)
            fpr = float(fp["value"].iloc[-1])
            pol_diff = ffr - fpr
            # Join on date — DFF is a 7-day series, foreign policy rates are business-day;
            # raw iloc[-6] on each would compare different calendar dates.
            joined = ff.join(fp, how="inner", lsuffix="_us", rsuffix="_f").dropna()
            pol_diff_prev = float(joined["value_us"].iloc[-6]) - float(joined["value_f"].iloc[-6])
            pol_dd   = pol_diff - pol_diff_prev
            wide_lbl = (f'WIDENING (USD carry up, bullish {display})' if usd_base
                        else f'WIDENING (USD carry up, bearish {display})')
            narr_lbl = (f'NARROWING (USD carry down, bearish {display})' if usd_base
                        else f'NARROWING (USD carry down, bullish {display})')
            macro_block += (
                f"{cfg.RATE_FOREIGN_NAME + ':':<18}{fpr:.2f}%\n"
                f"Policy diff (US−{cfg.FOREIGN_CCY}): {pol_diff:+.2f}% (was {pol_diff_prev:+.2f}%, Δ {pol_dd:+.2f}%)\n"
                f"  → {wide_lbl if pol_dd > 0 else narr_lbl}\n")
            baseline_extra = f"baseline_policy_diff: {round(pol_diff,3)}\n"
        else:
            macro_block += (f"Foreign policy ({cfg.FOREIGN_CCY}): no daily FRED series — "
                            f"carry leg skipped (dead signal, D021/D024)\n")
        macro_block += f"VIX:              {float(vix['value'].iloc[-1]):.2f}"
        baseline_label = "baseline_dgs2"; baseline_val = us_now
    elif macro_mode == "cross_rate_diff" and getattr(cfg, "RATE_GBP", None) is None:
        # ONE-LEG cross (EURJPY/GBPJPY): second leg has no daily FRED series (BoJ) → no rate diff.
        # Live leg rides the RATE_EUR slot (ECBDFR for eurjpy, IUDSOIA for gbpjpy).
        # Macro = live policy leg only, LOW-weight NON-SCORING tilt. VIX polarity per-pair empirical.
        leg = load_fred_local(cfg.RATE_EUR)
        leg_label = getattr(cfg, "LIVE_LEG_LABEL", f"ECB Deposit ({cfg.RATE_EUR})")
        leg_ccy   = getattr(cfg, "LIVE_LEG_CCY", "EUR")
        leg_now = float(leg["value"].iloc[-1]); leg_20d = float(leg["value"].iloc[-21])
        macro_block = (
            f"⚠ {display} CROSS — one-leg macro (no daily {getattr(cfg,'RATE_FOREIGN_NAME','foreign')} series); "
            f"LOW-weight NON-SCORING tilt.\n"
            f"  {leg_label}: {leg_now:.2f}%  (was {leg_20d:.2f}% 20d ago, Δ {leg_now-leg_20d:+.2f}%)\n"
            f"  → {leg_ccy + ' carry UP (bullish ' + display + ')' if leg_now - leg_20d > 0.005 else leg_ccy + ' carry DOWN (bearish ' + display + ')' if leg_20d - leg_now > 0.005 else 'FLAT (policy step unchanged)'}\n"
            f"VIX:              {float(vix['value'].iloc[-1]):.2f}  (carry barometer — polarity per-pair, see signal-results)")
        baseline_label = getattr(cfg, "BASELINE_LABEL", "baseline_ecb_rate"); baseline_val = round(leg_now, 3)
    elif macro_mode == "cross_rate_diff":
        # EUR/GBP CROSS: no USD leg. Direction tilt = EUR−GBP rate differential (ECBDFR − SONIA).
        # EG2: cross macro is THIN/DEAD on free daily data → LOW-weight, NON-SCORING tilt only.
        # See wiki/research/eurgbp/signal-results.md.
        eur = load_fred_local(cfg.RATE_EUR)   # ECB Deposit Facility Rate (ECBDFR)
        gbp = load_fred_local(cfg.RATE_GBP)   # GBP SONIA (IUDSOIA)
        eur_now = float(eur["value"].iloc[-1]); gbp_now = float(gbp["value"].iloc[-1])
        diff_now  = eur_now - gbp_now
        eur_20d   = float(eur["value"].iloc[-21]); gbp_20d = float(gbp["value"].iloc[-21])
        diff_20d  = eur_20d - gbp_20d
        diff_chg  = diff_now - diff_20d
        # diff rising (EUR rates up rel to GBP) → EURGBP UP.
        macro_block = (
            f"⚠ EUR/GBP CROSS — macro = LOW-weight NON-SCORING tilt (EG2: cross macro thin/dead).\n"
            f"  ECB Deposit (ECBDFR): {eur_now:.2f}%\n"
            f"  GBP SONIA (IUDSOIA):  {gbp_now:.2f}%\n"
            f"  Rate diff (EUR−GBP):  {diff_now:+.2f}%  (was {diff_20d:+.2f}% 20d ago, Δ {diff_chg:+.2f}%)\n"
            f"  → {f'WIDENING (EUR carry up, bullish EURGBP)' if diff_chg > 0 else f'NARROWING (EUR carry down, bearish EURGBP)' if diff_chg < 0 else 'FLAT'}\n"
            f"VIX:              {float(vix['value'].iloc[-1]):.2f}  (EG4: risk-off polarity INVERTED vs USD-majors)")
        baseline_label = "baseline_rate_diff"; baseline_val = round(diff_now, 3)
    else:
        # XAUUSD: real-yield driven (single driver).
        ny  = load_fred_local("DGS10"); be = load_fred_local("T5YIE")
        ry  = load_fred_local("DFII10")
        ry_now  = float(ry["value"].iloc[-1]); ry_prev = float(ry["value"].iloc[-6])
        ry_20d  = ry["value"].iloc[-21:]
        ry_slope = float(np.polyfit(range(len(ry_20d)), ry_20d.values, 1)[0])
        ry_drift = ry_now - float(ry["value"].iloc[-2])
        macro_block = (
            f"Fed Funds:        {float(ff['value'].iloc[-1]):.2f}%\n"
            f"10Y Nominal:      {float(ny['value'].iloc[-1]):.2f}%\n"
            f"10Y Real (TIPS):  {ry_now}% (was {ry_prev}% ~1w ago, Δ {round(ry_now-ry_prev,3):+}%)\n"
            f"  → {'RISING ⚠  (bearish gold)' if ry_now > ry_prev else 'FALLING ✅ (bullish gold)'}\n"
            f"  20d slope: {ry_slope:+.4f} %/day  {'(rising trend)' if ry_slope > 0 else '(falling trend)'}\n"
            f"  1d drift:  {ry_drift:+.3f}%\n"
            f"5Y Breakeven:     {float(be['value'].iloc[-1]):.2f}%\n"
            f"VIX:              {float(vix['value'].iloc[-1]):.2f}")
        baseline_label = "baseline_dfii10"; baseline_val = ry_now

    # Format blocks
    if cot and "error" not in cot:
        net_str = f"{cot['net']:+,}"; chg_str = f"{cot['net_chg']:+,}" if cot["net_chg"] is not None else "N/A"
        cot_label = (_instrument_cfg.COT_CONTRACT_NAME if _instrument_cfg else "GOLD").split(" - ")[0]
        # USD-base pairs: futures quote the FOREIGN ccy → spec net long future = SHORT the pair.
        cot_inv = getattr(_instrument_cfg, "COT_INVERTED", False) if _instrument_cfg else False
        if cot_inv:
            stance = (f"spec long {cot_label} = BEARISH {display}" if cot['net'] > 0
                      else f"spec short {cot_label} = BULLISH {display}")
        else:
            stance = 'BULLISH (spec long)' if cot['net'] > 0 else 'BEARISH (spec short)'
        cot_block = (f"━━━ COT — CFTC {cot_label} FUTURES (non-commercial, as of {cot['date']}) ━━━━━━\n"
                     f"Spec Long:      {cot['long']:,}\nSpec Short:     {cot['short']:,}\n"
                     f"Net Position:   {net_str}  ({stance}){'  ⚠ INVERTED READ (USD-base pair)' if cot_inv else ''}\n"
                     f"W/W Change:     {chg_str}  ({'INCREASING' if (cot['net_chg'] or 0)>0 else 'DECREASING'})\n"
                     f"Note: net-position extremes vs 1y range = crowded = reversal risk (per-instrument threshold)")
    else:
        cot_block = f"━━━ COT — CFTC FUTURES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {(cot or {}).get('error','no data')}"

    if gld and "error" not in gld:
        wk = f"{gld['wk_chg']:+}" if gld["wk_chg"] is not None else "N/A"
        mo = f"{gld['mo_chg']:+}" if gld["mo_chg"] is not None else "N/A"
        bias = "INFLOW (bullish)" if (gld["wk_chg"] or 0) > 0 else "OUTFLOW (bearish)" if (gld["wk_chg"] or 0) < 0 else "FLAT"
        gld_block = (f"━━━ ETF FLOWS — SPDR GLD (tonnes held, as of {gld['date']}) ━━━\n"
                     f"Tonnes:         {gld['tonnes']}\n1w Δ tonnes:    {wk}  ({bias})\n4w Δ tonnes:    {mo}\n"
                     f"Note: persistent outflows during macro BEARISH = confirmation. Inflows against bias = warning.")
    else:
        gld_block = f"━━━ ETF FLOWS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {(gld or {}).get('error','no data')}"

    if gap and "error" not in gap:
        gap_block = (f"━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                     f"Fri close:   ${gap['fri_close']}  ({gap['fri_date']})\n"
                     f"Sun reopen:  ${gap['next_open']}  ({gap['next_date']})\n"
                     f"Gap:         ${gap['gap_$']}  ({gap['gap_pct']:+}%)  → {gap['flag']}\n"
                     f"Thresholds: <0.20% NOISE | 0.20–0.50% NOTE | 0.50–1.00% WARNING | >1.00% RE-FORECAST")
    else:
        gap_block = "━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nNo Sunday reopen bar found"

    vp_block = (f"VAH: ${vp['VAH']}\nPOC: ${vp['POC']}  ← highest volume node\nVAL: ${vp['VAL']}"
                if not (vp.get("error") or vp.get("disabled"))
                else vp.get("disabled") or f"VP fetch failed: {vp['error']}")

    # Intermarket commodity block (#3) — only for pairs declaring COMMODITY_* (AUD/NZD).
    com_names = (list(getattr(cfg, "COMMODITY_FRED", []) or [])
                 + list((getattr(cfg, "COMMODITY_YF", {}) or {}).keys())) if cfg else []
    intermarket_block = ""
    if com_names:
        lines = []
        for nm in com_names:
            s = load_commodity_local(nm)
            if s is None or s.empty:
                lines.append(f"{nm:<10} no data"); continue
            now = float(s["value"].iloc[-1])
            wk  = float(s["value"].iloc[-6]) if len(s) >= 6 else now
            chg = ((now / wk) - 1) * 100 if wk else 0.0
            w20 = s["value"].iloc[-21:]
            slope = float(np.polyfit(range(len(w20)), w20.values, 1)[0]) if len(w20) >= 2 else 0.0
            lines.append(f"{nm:<10} {now:<10.4g} (Δ1w {chg:+.2f}%, 20d slope {slope:+.4g}/day)")
        intermarket_block = (
            "\n━━━ INTERMARKET (commodity proxies — narrative context, NOT scored) ━━\n"
            + "\n".join(lines)
            + "\n  Rising copper/iron ore/dairy = risk-on commodity bid → pair-BULLISH context "
              "(China-demand proxy). Use in Section 1/4 only.\n")

    # ── Oscillators (#C) — computed for D1 + H4, the values Z2 engines read ──
    osc_d_txt,  osc_d_ex  = oscillator_block(gold_d_closed,  "D1")
    osc_h4_txt, osc_h4_ex = oscillator_block(gold_h4_closed, "H4")
    osc_extremes = osc_d_ex + osc_h4_ex
    oscillators_block = (
        f"{osc_d_txt}\n{osc_h4_txt}\n"
        f"  EXTREMES: {' · '.join(osc_extremes) if osc_extremes else 'none (no oscillator at extreme)'}")

    # ── Market structure (#B) — BOS/CHoCH on D1 + H4 (was narrative-only) ──
    def _struct_line(df, tf):
        se = structure_events(df, lookback=60)
        last = se["last"]
        if last is None:
            return f"  {tf}: state {se['state'].upper()} | no BOS/CHoCH in last 60 bars"
        age = len(df.tail(60)) - 1 - last["pos"]
        return (f"  {tf}: state {se['state'].upper()} | last {last['type']} {last['dir'].upper()} "
                f"@ {last['level']} ({last['time']}, {age} bars ago)")
    structure_block = f"{_struct_line(gold_d_closed, 'D1')}\n{_struct_line(gold_h4_closed, 'H4')}"

    # ── Entry triggers (#E0) — RSI/band/Stoch reclaim + pin/engulf on latest closed 1H bar ──
    entry_trig_block = entry_triggers_block(price_h1)

    # ── Time-at-price (#B) — VP substitute for USD-base pairs (tick volume is 0) ──
    tap_block = ""
    if not vp_ticker:  # VP disabled = USD-base pair → acceptance histogram instead
        tap = time_at_price(price_h1, window=480)
        if tap:
            tap_block = (f"\n━━━ TIME-AT-PRICE (H1 acceptance — VP substitute, NOT volume) ━━\n"
                         f"HTN (most-accepted): {round(tap['htn'], PRICE_DP)}\n"
                         f"Value area: {round(tap['va_low'], PRICE_DP)} – {round(tap['va_high'], PRICE_DP)} (70% of time)\n"
                         f"Use as S/R confluence like a POC/VA — acceptance, not traded volume.\n")

    # ── News feed (#A) — recent pair-filtered headlines from the store ──
    news_block = ""
    nf0 = db.read_table("news") if db else None
    if (nf0 is None or nf0.empty) and NEWS_CSV.exists():
        nf0 = pd.read_csv(NEWS_CSV, dtype=str)
    if nf0 is not None and not nf0.empty:
        try:
            nf = nf0.fillna("").sort_values("datetime_utc").tail(40)
            kws = _NEWS_KEYWORDS.get(SYM_CLEAN, []) + ["fed", "fomc", "rate", "inflation", "cpi"]
            hits = nf[nf["headline"].str.lower().apply(lambda h: any(k in h for k in kws))].tail(8)
            if not hits.empty:
                rows = [f"  {r['datetime_utc'][:10]} [{r['source']}] {r['headline']}"
                        for _, r in hits.iterrows()]
                news_block = ("\n━━━ NEWS FEED (recent, pair-filtered — context for Section 2) ━━\n"
                              + "\n".join(rows) + "\n")
        except Exception:
            news_block = ""

    out = f"""
╔══════════════════════════════════════════════════════╗
  {display} WEEKLY DATA — {TODAY.strftime('%Y-%m-%d')} (W{WEEK_NUM})
╚══════════════════════════════════════════════════════╝

━━━ MACRO ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{macro_block}

━━━ PRICE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{display}:{' '*max(1,16-len(display))}${gc:.{PRICE_DP}f} (was ${gp:.{PRICE_DP}f}, {round(((gc/gp)-1)*100,2):+.2f}% ~1w chg)
{'' if macro_mode == 'cross_rate_diff' else f'DXY (ICE 6-cur):  {dc:.3f}  (was {dp:.3f},  {round(((dc/dp)-1)*100,2):+.2f}% ~1w chg)'}

━━━ INDICATORS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATR(14) Daily:    ${atr_d}
ATR(14) H4:       ${atr_h4}  (trading days only)
SL (constitution v2): ${round(sl_v2, PRICE_DP)} = {"H4 ATR (floor — 0.5×D1 " + str(round(d1_floor, PRICE_DP)) + " < H4)" if d1_floor < atr_h4 else "avg(0.5×D1 " + str(round(d1_floor, PRICE_DP)) + ", H4 " + str(atr_h4) + ")"}
D1 ATR now:       ${atr_d_now} | 20d median: ${atr_d_med} → {"COMPRESSED ✅" if compressed else "EXPANDING ⚠"}

Lot sizing ($2000 risk, SL above):
  Raw lots:  {lots_raw}
  Use lots:  {lots_fl}  (floored to 0.01-lot step, min 0.01)

ADX(14) D1:       {adx_val} → {adx_regime}
EMA 50 D1:        ${ema50} | Price {"ABOVE" if gc > ema50 else "BELOW"}
EMA 200 D1:       ${ema200} | Price {"ABOVE" if gc > ema200 else "BELOW"}
RSI(14) D1:       {rsi_now} (was {rsi_old} 10 bars ago, {"rising" if rsi_now > rsi_old else "falling"})
Bollinger(20,2):  upper ${boll['upper']} | mid ${boll['mid']} | lower ${boll['lower']} | %B {boll['pctb']} → {boll['pos']}

RSI D1 (last 10 bars):
{chr(10).join([f"  {v[0]}: {v[1]}" for v in rsi_vals])}

MACD(12,26,9) D1 — last 5 bars:
  {"Date":<12} {"MACD":>8} {"Signal":>8} {"Hist":>8}
{chr(10).join([f"  {r[0]:<12} {r[1]:>8} {r[2]:>8} {r[3]:>8}" for r in macd_rows])}
  Histogram {"POSITIVE (bullish momentum)" if macd_rows[-1][3] > 0 else "NEGATIVE (bearish momentum)"}
  Cross: {"MACD above signal (bullish)" if macd_rows[-1][1] > macd_rows[-1][2] else "MACD below signal (bearish)"}

━━━ OSCILLATORS (D1 / H4 — Z2 engine inputs, were eyeballed pre-D025) ━━
{oscillators_block}

━━━ MARKET STRUCTURE (BOS/CHoCH, fractal N=2) ━━━━━━━━━━━
{structure_block}

━━━ ENTRY TRIGGERS (E0, latest closed 1H — reclaim > pin/engulf, D027) ━━
{entry_trig_block}

━━━ VOLUME PROFILE ({vp_ticker or 'disabled'}, 3mo daily) ━━━━━━━━━━━━
{vp_block}
VP check: zone within ~8 units of POC/VAH/VAL = confluent
{tap_block}

{cot_block}

{gld_block}

{gap_block}
{intermarket_block}{news_block}
━━━ BASELINES (snapshot for forecast frontmatter) ━━━━
{baseline_label}: {baseline_val}
{baseline_extra}baseline_dxy:    {dc:.3f}
weekend_gap_pct: {gap['gap_pct'] if gap and 'gap_pct' in gap else 'N/A'}

━━━ WEEKLY PIVOTS (prior week OHLC) ━━━━━━━━━━━━━━━━━━
R3:{pvt['R3']}  R2:{pvt['R2']}  R1:{pvt['R1']}
PP:{pvt['PP']}
S1:{pvt['S1']}  S2:{pvt['S2']}  S3:{pvt['S3']}

━━━ SWING POINTS (Daily, N=5) ━━━━━━━━━━━━━━━━━━━━━━━━
Highs: {' | '.join([f"${h[1]}({h[0]})" for h in sh])}
Lows:  {' | '.join([f"${l[1]}({l[0]})" for l in sl])}

━━━ SWING POINTS (H4, N=5, trading days) ━━━━━━━━━━━━━
Highs: {' | '.join([f"${h[1]}({h[0]})" for h in sh_h4])}
Lows:  {' | '.join([f"${l[1]}({l[0]})" for l in sl_h4])}

━━━ FIBONACCI (anchored to last D1 swing high/low) ━━━
Swing: ${fibs['swing_low']} → ${fibs['swing_high']}
  78.6%:      ${fibs['78.6%']}
  61.8%:      ${fibs['61.8%']}  ← golden pocket
  50.0%:      ${fibs['50.0%']}
  38.2%:      ${fibs['38.2%']}
  Ext 127.2%: ${fibs['ext_127.2%']}
  Ext 161.8%: ${fibs['ext_161.8%']}  ← TP extension zone

━━━ DAILY OHLCV — last 15 bars ━━━━━━━━━━━━━━━━━━━━━━━
{gold_d[['open','high','low','close']].tail(15).round(PRICE_DP).to_string()}

━━━ H4 OHLCV — last 24 bars (trading days) ━━━━━━━━━━━
{gold_h4[['open','high','low','close']].tail(24).round(PRICE_DP).to_string()}

Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC ({datetime.now().astimezone().strftime('%H:%M %Z')} local)
"""
    PULL_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out)
    print(out)
    print(f"✅ Saved to {out_path}")
    return str(out_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Re-fetch full history")
    ap.add_argument("--instrument", default="xauusd",
                    choices=list(REGISTERED_INSTRUMENTS) + ["all"],
                    help="Instrument to run (default: xauusd). 'all' runs every registered instrument.")
    args = ap.parse_args()

    to_run = list(REGISTERED_INSTRUMENTS) if args.instrument == "all" else [args.instrument]
    for inst in to_run:
        if len(to_run) > 1:
            print(f"\n{'='*54}\n  {inst.upper()}\n{'='*54}")
        load_instrument(inst)
        run(force=args.force)
