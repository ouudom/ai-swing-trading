"""All strategies. Each takes (cfg, data_dict) where data_dict has D1/H4/H1 frames.
Returns Result(name, equity, trades). Required timeframes declared in REGISTRY.
"""
import numpy as np
import pandas as pd
from .engine import Config, Trade, Result, open_trade, close_pnl, manage
from .data import atr, rsi
from scripts.structure import g1_pass, nearest_pivot_dist


def _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_time, exit_time, reason):
    pnl, r = close_pnl(cfg, pos, entry, exit_px, size, risk_dist)
    trades.append(Trade(entry_time, exit_time, pos, entry, exit_px, size, risk_dist, pnl, r, reason))
    return pnl


# ===== 1. Vol-target SMA 50/200 (D1, no stop/TP — pure regime exposure) =====
def s_voltrend(cfg: Config, data):
    df = data["D1"].copy()
    df["sma50"] = df.close.rolling(50).mean()
    df["sma200"] = df.close.rolling(200).mean()
    df["sigma"] = df.close.pct_change().rolling(20).std()
    target_vol = 0.15
    df["lev"] = (target_vol / (df.sigma * np.sqrt(252))).clip(0, 3)
    sig = (df.sma50 > df.sma200).astype(int).shift(1).fillna(0)
    rets = df.close.pct_change().fillna(0) * sig * df.lev.shift(1).fillna(0)
    eq = cfg.initial * (1 + rets).cumprod()
    trades = []
    in_pos = 0; entry_eq = eq.iloc[0]; entry_t = eq.index[0]
    for t, s, e in zip(eq.index, sig, eq):
        if in_pos == 0 and s == 1:
            entry_eq = e; in_pos = 1; entry_t = t
        elif in_pos == 1 and s == 0:
            trades.append(Trade(entry_t, t, 1, 0, 0, 0, 1, e - entry_eq, 0, "regime_flip"))
            in_pos = 0
    return Result("Vol-target SMA 50/200", eq, trades)


# ===== 2. London breakout (H1) =====
def s_london(cfg, data):
    df = data["H1"].copy()
    df["date"] = df.index.date
    df["hour"] = df.index.hour
    equity = cfg.initial; trades = []; eq_curve = []
    for date, day in df.groupby("date"):
        asia = day[(day.hour >= 0) & (day.hour < 7)]
        london = day[(day.hour >= 8) & (day.hour < 12)]
        ny_close = day[day.hour >= 20]
        if len(asia) < 3 or len(london) < 2 or len(ny_close) < 1:
            eq_curve.extend([equity] * len(day)); continue
        a_hi, a_lo = asia.high.max(), asia.low.min()
        rng = a_hi - a_lo
        if rng <= 0:
            eq_curve.extend([equity] * len(day)); continue
        pos = 0; entry = stop = tp = be_trig = size = 0
        be_armed = False; entry_t = None; risk_dist = rng
        in_session = day[day.hour >= 8]
        for ts, row in in_session.iterrows():
            if pos == 0 and ts.hour < 12:
                if row.high > a_hi:
                    size, stop, tp, be_trig, equity = open_trade(cfg, 1, a_hi, rng, equity)
                    entry = a_hi; pos = 1; entry_t = ts; be_armed = False
                elif row.low < a_lo:
                    size, stop, tp, be_trig, equity = open_trade(cfg, -1, a_lo, rng, equity)
                    entry = a_lo; pos = -1; entry_t = ts; be_armed = False
            if pos != 0:
                exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, risk_dist)
                if exit_px is not None:
                    pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                    equity += pnl; pos = 0
        if pos != 0:
            exit_px = ny_close.close.iloc[-1]; ts = ny_close.index[-1]
            pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, "eod")
            equity += pnl; pos = 0
        eq_curve.extend([equity] * len(day))
    eq = pd.Series(eq_curve[:len(df)], index=df.index[:len(eq_curve)])
    return Result("London breakout", eq, trades)


# ===== 3. NY momentum (H1) =====
def s_ny_mom(cfg, data):
    df = data["H1"].copy()
    df["date"] = df.index.date
    df["hour"] = df.index.hour
    equity = cfg.initial; trades = []; eq_curve = []
    for date, day in df.groupby("date"):
        early = day[(day.hour >= 13) & (day.hour < 17)]
        late = day[(day.hour >= 17) & (day.hour < 21)]
        if len(early) < 2 or len(late) < 2:
            eq_curve.extend([equity] * len(day)); continue
        mom = early.close.iloc[-1] - early.open.iloc[0]
        rng = early.high.max() - early.low.min()
        if abs(mom) < 0.1 or rng <= 0:
            eq_curve.extend([equity] * len(day)); continue
        direction = 1 if mom > 0 else -1
        entry = late.open.iloc[0]; entry_t = late.index[0]
        size, stop, tp, be_trig, equity = open_trade(cfg, direction, entry, rng, equity)
        pos = direction; be_armed = False
        for ts, row in late.iterrows():
            if pos == 0: break
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, rng)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, rng, entry_t, ts, reason)
                equity += pnl; pos = 0
        if pos != 0:
            ts = late.index[-1]; exit_px = late.close.iloc[-1]
            pnl = _close_position(cfg, trades, pos, entry, exit_px, size, rng, entry_t, ts, "eod")
            equity += pnl; pos = 0
        eq_curve.extend([equity] * len(day))
    eq = pd.Series(eq_curve[:len(df)], index=df.index[:len(eq_curve)])
    return Result("NY momentum", eq, trades)


# ===== 4. NFP momentum (H1, first Friday) =====
def s_nfp(cfg, data):
    df = data["H1"].copy()
    df["date"] = df.index.date
    dates = pd.to_datetime(df.date.unique())
    nfp_dates = set()
    for ym, grp in pd.DataFrame({"d": dates}).groupby([dates.year, dates.month]):
        fridays = grp.d[grp.d.dt.weekday == 4]
        if len(fridays) > 0:
            nfp_dates.add(fridays.iloc[0].date())
    equity = cfg.initial; trades = []; eq_curve = []
    for date, day in df.groupby("date"):
        if date not in nfp_dates:
            eq_curve.extend([equity] * len(day)); continue
        rel = day[day.index.hour == 13]
        post = day[(day.index.hour >= 14) & (day.index.hour < 20)]
        if len(rel) < 1 or len(post) < 2:
            eq_curve.extend([equity] * len(day)); continue
        rel_bar = rel.iloc[0]
        mom = rel_bar.close - rel_bar.open
        rng = rel_bar.high - rel_bar.low
        if abs(mom) < 0.1 or rng <= 0:
            eq_curve.extend([equity] * len(day)); continue
        direction = 1 if mom > 0 else -1
        entry = post.open.iloc[0]; entry_t = post.index[0]
        size, stop, tp, be_trig, equity = open_trade(cfg, direction, entry, rng, equity)
        pos = direction; be_armed = False
        for ts, row in post.iterrows():
            if pos == 0: break
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, rng)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, rng, entry_t, ts, reason)
                equity += pnl; pos = 0
        if pos != 0:
            ts = post.index[-1]; exit_px = post.close.iloc[-1]
            pnl = _close_position(cfg, trades, pos, entry, exit_px, size, rng, entry_t, ts, "eod")
            equity += pnl; pos = 0
        eq_curve.extend([equity] * len(day))
    eq = pd.Series(eq_curve[:len(df)], index=df.index[:len(eq_curve)])
    return Result("NFP momentum", eq, trades)


# ===== 5. Multi-TF confluence D1+H4+H1 =====
def s_confluence(cfg, data):
    d1, h4, h1 = data["D1"].copy(), data["H4"].copy(), data["H1"].copy()
    d1["sma50"] = d1.close.rolling(50).mean()
    d1["uptrend"] = (d1.close > d1.sma50).astype(int)
    d1_state = d1.uptrend.reindex(h1.index, method="ffill").fillna(0)
    h4["rsi"] = rsi(h4.close, 14)
    h4["pullback"] = (h4.rsi < 40).astype(int)
    h4_state = h4.pullback.reindex(h1.index, method="ffill").fillna(0)
    h1["prev_hi"] = h1.high.shift(1)
    h1["a"] = atr(h1, 14)
    equity = cfg.initial; trades = []; eq_curve = []
    pos = 0; entry = stop = tp = be_trig = size = 0
    be_armed = False; entry_t = None; risk_dist = 0
    for i, (ts, row) in enumerate(h1.iterrows()):
        if pos != 0:
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, risk_dist)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                equity += pnl; pos = 0
        a = row.a
        if pos == 0 and d1_state.iloc[i] == 1 and h4_state.iloc[i] == 1 \
                and not np.isnan(row.prev_hi) and row.high > row.prev_hi and not np.isnan(a):
            entry = max(row.open, row.prev_hi)
            risk_dist = 1.5 * a
            if risk_dist > 0:
                size, stop, tp, be_trig, equity = open_trade(cfg, 1, entry, risk_dist, equity)
                pos = 1; be_armed = False; entry_t = ts
        eq_curve.append(equity + ((row.close - entry) * size if pos else 0))
    eq = pd.Series(eq_curve, index=h1.index)
    return Result("Multi-TF confluence", eq, trades)


# ===== 6. Vol-regime switch (D1) =====
def s_vol_regime(cfg, data):
    df = data["D1"].copy()
    df["atr"] = atr(df, 14)
    df["atr_pct"] = df.atr.rolling(252).rank(pct=True)
    df["sma200"] = df.close.rolling(200).mean()
    df["rsi2"] = rsi(df.close, 2)
    df["dc_hi"] = df.high.rolling(20).max().shift(1)
    df["dc_lo"] = df.low.rolling(20).min().shift(1)
    equity = cfg.initial; trades = []; eq_curve = []
    pos = 0; entry = stop = tp = be_trig = size = 0
    be_armed = False; entry_t = None; risk_dist = 0
    for row in df.itertuples():
        a = row.atr; ts = row.Index
        if pos != 0:
            class R: pass
            r = R(); r.open = row.open; r.high = row.high; r.low = row.low; r.close = row.close
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, r, be_armed, risk_dist)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                equity += pnl; pos = 0
        if pos == 0 and not np.isnan(row.atr_pct) and not np.isnan(a):
            if row.atr_pct > 0.7 and not np.isnan(row.dc_hi) and row.close > row.dc_hi:
                entry = row.close; risk_dist = 2 * a
                size, stop, tp, be_trig, equity = open_trade(cfg, 1, entry, risk_dist, equity)
                pos = 1; be_armed = False; entry_t = ts
            elif row.atr_pct < 0.3 and row.close > row.sma200 and row.rsi2 < 10:
                entry = row.close; risk_dist = 3 * a
                size, stop, tp, be_trig, equity = open_trade(cfg, 1, entry, risk_dist, equity)
                pos = 1; be_armed = False; entry_t = ts
        eq_curve.append(equity + ((row.close - entry) * size if pos else 0))
    eq = pd.Series(eq_curve, index=df.index)
    return Result("Vol-regime switch", eq, trades)


# ===== 7. Inside-day breakout (D1 setup, H4 execution) =====
def s_inside_day(cfg, data):
    d1 = data["D1"].copy()
    d1["prev_hi"] = d1.high.shift(1)
    d1["prev_lo"] = d1.low.shift(1)
    d1["inside"] = (d1.high < d1.prev_hi) & (d1.low > d1.prev_lo)
    d1["a"] = atr(d1, 14)
    inside_days = d1[d1.inside].copy()
    h4 = data["H4"].copy()
    equity = cfg.initial; trades = []; eq_curve = []
    pos = 0; entry = stop = tp = be_trig = size = 0
    be_armed = False; entry_t = None; risk_dist = 0
    setup_active = False; upper = lower = a = None; setup_expiry = None
    for ts, row in h4.iterrows():
        day = ts.date()
        prev_day = pd.Timestamp(day) - pd.Timedelta(days=1)
        if prev_day in inside_days.index and not setup_active and pos == 0:
            rec = inside_days.loc[prev_day]
            upper, lower, a = rec.high, rec.low, rec.a
            setup_expiry = pd.Timestamp(day) + pd.Timedelta(days=1)
            setup_active = True
        if setup_active and pos == 0 and setup_expiry and ts > setup_expiry:
            setup_active = False; upper = lower = a = None
        if pos != 0:
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, risk_dist)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                equity += pnl; pos = 0
                setup_active = False; upper = lower = a = None
        if pos == 0 and setup_active and a is not None and not np.isnan(a):
            if row.high > upper:
                entry = upper; risk_dist = 1.5 * a
                size, stop, tp, be_trig, equity = open_trade(cfg, 1, entry, risk_dist, equity)
                pos = 1; be_armed = False; entry_t = ts; setup_active = False
            elif row.low < lower:
                entry = lower; risk_dist = 1.5 * a
                size, stop, tp, be_trig, equity = open_trade(cfg, -1, entry, risk_dist, equity)
                pos = -1; be_armed = False; entry_t = ts; setup_active = False
        eq_curve.append(equity + (((row.close - entry) * size if pos > 0 else (entry - row.close) * size) if pos else 0))
    eq = pd.Series(eq_curve, index=h4.index)
    return Result("Inside-day breakout", eq, trades)


# ----- signal-based runners (research strategies) -----
def _run_signal(cfg, df, signal, name, stop_atr=2.5, bpy_key="D1"):
    df = df.copy()
    df["atr"] = atr(df, 14)
    sig = signal.shift(1).fillna(0)
    equity = cfg.initial
    pos = 0; entry = 0.0; stop = 0.0; tp = 0.0; size = 0.0; risk_dist = 0; be_trig = 0
    be_armed = False; entry_t = None
    eq_curve = []; trades = []
    for i, (ts, row) in enumerate(df.iterrows()):
        o, h, l, c, a = row.open, row.high, row.low, row.close, row.atr
        if pos != 0:
            class R: pass
            r = R(); r.open = o; r.high = h; r.low = l; r.close = c
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, r, be_armed, risk_dist)
            if exit_px is None:
                s = sig.iloc[i]
                if s != pos:
                    exit_px = o; reason = "flip"
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                equity += pnl; pos = 0
        if pos == 0:
            s = sig.iloc[i]
            if s != 0 and not np.isnan(a):
                risk_dist = stop_atr * a
                if risk_dist > 0:
                    size, stop, tp, be_trig, equity = open_trade(cfg, int(np.sign(s)), o, risk_dist, equity)
                    entry = o; pos = int(np.sign(s)); be_armed = False; entry_t = ts
        mtm = equity + (((c - entry) if pos > 0 else (entry - c)) * size if pos != 0 else 0)
        eq_curve.append(mtm)
    eq = pd.Series(eq_curve, index=df.index)
    return Result(name, eq, trades)


def _sig_sma_cross(df, fast, slow, long_only=False):
    f = df.close.rolling(fast).mean()
    s = df.close.rolling(slow).mean()
    sig = pd.Series(0, index=df.index)
    sig[f > s] = 1
    sig[f < s] = 0 if long_only else -1
    return sig


def _sig_donchian(df, n=20, long_only=False):
    hh = df.high.rolling(n).max().shift(1)
    ll = df.low.rolling(n).min().shift(1)
    sig = pd.Series(np.nan, index=df.index)
    sig[df.close > hh] = 1
    sig[df.close < ll] = 0 if long_only else -1
    return sig.ffill().fillna(0)


def _sig_rsi2(df, lo=10, hi=70):
    r = rsi(df.close, 2)
    sma200 = df.close.rolling(200).mean()
    state = 0; out = []
    for rv, c, m in zip(r.values, df.close.values, sma200.values):
        if np.isnan(m): out.append(0); continue
        if state == 0 and c > m and rv < lo: state = 1
        elif state == 1 and rv > hi: state = 0
        out.append(state)
    return pd.Series(out, index=df.index)


def _sig_trend_pullback(df):
    r = rsi(df.close, 14)
    m = df.close.rolling(200).mean()
    state = 0; out = []
    for rv, c, mv in zip(r.values, df.close.values, m.values):
        if np.isnan(mv): out.append(0); continue
        if state == 0 and c > mv and rv < 35: state = 1
        elif state == 1 and (rv > 65 or c < mv): state = 0
        out.append(state)
    return pd.Series(out, index=df.index)


def s_sma_cross_long(cfg, data):
    df = data["D1"]
    return _run_signal(cfg, df, _sig_sma_cross(df, 50, 200, True), "SMA 50/200 long", stop_atr=3.0)


def s_sma_cross_ls(cfg, data):
    df = data["D1"]
    return _run_signal(cfg, df, _sig_sma_cross(df, 20, 50, False), "SMA 20/50 L/S", stop_atr=2.5)


def s_donchian(cfg, data):
    df = data["D1"]
    return _run_signal(cfg, df, _sig_donchian(df, 20, True), "Donchian-20 long", stop_atr=2.0)


def s_rsi2(cfg, data):
    df = data["D1"]
    return _run_signal(cfg, df, _sig_rsi2(df), "RSI2 + 200SMA (MR)", stop_atr=3.0)


def s_trend_pullback(cfg, data):
    df = data["D1"]
    return _run_signal(cfg, df, _sig_trend_pullback(df), "Trend pullback (RSI14<35)", stop_atr=2.5)


def s_buyhold(cfg, data):
    df = data["D1"]
    eq = cfg.initial * df.close / df.close.iloc[0]
    return Result("Buy & Hold", eq, [])


# ===== 13. Weekly swing v1 — mirrors live /validate formula =====
# Stop = avg(0.5*D1_ATR14, H4_ATR14_trading, structural_dist)
# OUTWARD offset = (10 - score) * 0.3 * stop_distance
# Score: G1 (MTF align) 3.5 + G2 (ATR compressed) 2.0 + G3 (D1 EMA50 trend) 3.5 = 9.0 max
# (V2 macro drift excluded — no FRED data in backtest loader)
def s_weekly_swing_v1(cfg, data):
    d1 = data["D1"].copy()
    h4_full = data["H4"].copy()
    h1 = data["H1"].copy()

    # H4 trading-day filter (drop weekend/holiday flatline bars)
    h4 = h4_full[(h4_full.high - h4_full.low) >= 1.0].copy()

    d1["atr14"]  = atr(d1, 14)
    d1["atr_med20"] = d1["atr14"].rolling(20).median()
    d1["ema50"] = d1.close.ewm(span=50, adjust=False).mean()
    h4["atr14"] = atr(h4, 14)
    h1["ema20"] = h1.close.ewm(span=20, adjust=False).mean()

    equity = cfg.initial
    trades = []
    eq_curve = []

    pos = 0
    entry = stop = tp = be_trig = size = 0.0
    risk_dist = 0.0
    entry_t = None
    be_armed = False

    # State: per-week setup zone built on Sunday's data
    current_week = None
    zone_top = zone_bot = None
    bias = 0  # 1 long, -1 short
    score = 0.0
    limit_armed_until = None
    trigger_bar_idx = -999

    for i, (ts, row) in enumerate(h1.iterrows()):
        # === Active trade management ===
        if pos != 0:
            exit_px, reason, stop, be_armed = manage(cfg, pos, entry, stop, tp, be_trig, size, row, be_armed, risk_dist)
            if exit_px is not None:
                pnl = _close_position(cfg, trades, pos, entry, exit_px, size, risk_dist, entry_t, ts, reason)
                equity += pnl
                pos = 0
                limit_armed_until = None

        # === Weekly setup re-build (Monday 00:00) ===
        iso_year, iso_week, iso_wd = ts.isocalendar()
        wkey = (iso_year, iso_week)
        if wkey != current_week and iso_wd == 1 and ts.hour == 0:
            current_week = wkey
            # Need recent D1 close + EMA50 + ATR
            d1_hist = d1[d1.index < ts]
            if len(d1_hist) < 50:
                zone_top = zone_bot = None
                eq_curve.append(equity)
                continue
            last_d = d1_hist.iloc[-1]
            d1_atr = last_d.atr14
            d1_atr_med = last_d.atr_med20
            if pd.isna(d1_atr) or pd.isna(d1_atr_med):
                zone_top = zone_bot = None; eq_curve.append(equity); continue

            # Bias from EMA50
            bias = 1 if last_d.close > last_d.ema50 else -1

            # Zone = prior 5 trading-day extreme ± 0.5*D1_ATR
            recent_d = d1_hist.tail(5)
            if bias > 0:
                # long: zone = recent low support
                z_lo = recent_d.low.min()
                z_hi = z_lo + 0.5 * d1_atr
            else:
                z_hi = recent_d.high.max()
                z_lo = z_hi - 0.5 * d1_atr
            zone_top, zone_bot = z_hi, z_lo

            # Score components — G1 now a real fractal structure check (shared module)
            h4_hist = h4[h4.index < ts].tail(60)
            h1_hist = h1[h1.index < ts].tail(60)
            g1 = 3.5 if g1_pass(h4_hist, h1_hist, bias) else 0.0
            g2 = 2.0 if d1_atr < d1_atr_med else 0.0
            g3 = 3.5  # bias passes if direction matches D1 EMA trend (already true by construction)
            score = g1 + g2 + g3  # max 9.0

            limit_armed_until = ts + pd.Timedelta(days=4, hours=17)  # Mon → Fri 17:00
            trigger_bar_idx = -999

        # === No active zone or trade ===
        if pos != 0 or zone_top is None:
            eq_curve.append(equity); continue
        if limit_armed_until is None or ts > limit_armed_until:
            eq_curve.append(equity); continue
        # Only check entries during London/NY session
        if ts.hour < 8 or ts.hour >= 17:
            eq_curve.append(equity); continue
        if score < 5.5:
            eq_curve.append(equity); continue

        # === H1 trigger detection (pin or engulfing inside zone) ===
        in_zone = (row.low <= zone_top) and (row.high >= zone_bot)
        if not in_zone:
            eq_curve.append(equity); continue

        body = abs(row.close - row.open)
        upper_wick = row.high - max(row.close, row.open)
        lower_wick = min(row.close, row.open) - row.low
        is_pin_bull = lower_wick >= 2 * body and row.close > row.open and bias > 0
        is_pin_bear = upper_wick >= 2 * body and row.close < row.open and bias < 0
        trigger = is_pin_bull or is_pin_bear

        if trigger:
            trigger_bar_idx = i

        # Recency cap: trigger ≤ 8 bars ago
        if (i - trigger_bar_idx) > 8:
            eq_curve.append(equity); continue
        if trigger_bar_idx < 0:
            eq_curve.append(equity); continue

        # === Compute stop using live formula ===
        d1_atr = d1[d1.index < ts].iloc[-1].atr14
        h4_atr_now = h4[h4.index < ts].iloc[-1].atr14 if len(h4[h4.index < ts]) else d1_atr * 0.4
        # structural_dist: distance from zone extreme to nearest fractal pivot (shared module)
        h4_hist = h4[h4.index < ts]
        ref_px = zone_bot if bias > 0 else zone_top
        struct = nearest_pivot_dist(h4_hist, ref_px, bias)
        if struct is None or struct <= 0:
            stop_distance = (0.5 * d1_atr + h4_atr_now) / 2.0
            struct = 0.0
        else:
            stop_distance = (0.5 * d1_atr + h4_atr_now + struct) / 3.0
        if stop_distance <= 0 or stop_distance != stop_distance:
            eq_curve.append(equity); continue
        # cap
        if struct > 3 * h4_atr_now:
            eq_curve.append(equity); continue

        # Outward offset
        recent_d = d1[d1.index < ts].tail(5)
        entry_offset = (10 - score) * 0.3 * stop_distance
        if bias > 0:
            limit_px = zone_bot - entry_offset
            tp_px = recent_d.high.max()  # opposite-direction structural anchor
        else:
            limit_px = zone_top + entry_offset
            tp_px = recent_d.low.min()

        # Did this bar reach limit_px?
        filled = (row.low <= limit_px <= row.high)
        if not filled:
            eq_curve.append(equity); continue

        # R:R floor — mirrors live /validate (1.8R)
        r_planned = abs(tp_px - limit_px) / stop_distance
        if r_planned < 1.8:
            eq_curve.append(equity); continue

        risk_dist = stop_distance
        size, stop, _tp_engine, be_trig, equity = open_trade(cfg, bias, limit_px, risk_dist, equity)
        # Override engine TP with our structural anchor
        tp = tp_px
        entry = limit_px
        pos = bias
        entry_t = ts
        be_armed = False
        limit_armed_until = None  # one trade per week per setup
        trigger_bar_idx = -999

        eq_curve.append(equity)

    eq = pd.Series(eq_curve, index=h1.index)
    return Result("Weekly swing v1 (live formula)", eq, trades)


REGISTRY = [
    ("Vol-target SMA 50/200",   s_voltrend,       ["D1"]),
    ("London breakout",         s_london,         ["H1"]),
    ("NY momentum",             s_ny_mom,         ["H1"]),
    ("NFP momentum",            s_nfp,            ["H1"]),
    ("Multi-TF confluence",     s_confluence,     ["D1", "H4", "H1"]),
    ("Vol-regime switch",       s_vol_regime,     ["D1"]),
    ("Inside-day breakout",     s_inside_day,     ["D1", "H4"]),
    ("SMA 50/200 long",         s_sma_cross_long, ["D1"]),
    ("SMA 20/50 L/S",           s_sma_cross_ls,   ["D1"]),
    ("Donchian-20 long",        s_donchian,       ["D1"]),
    ("RSI2 + 200SMA (MR)",      s_rsi2,           ["D1"]),
    ("Trend pullback",          s_trend_pullback, ["D1"]),
    ("Buy & Hold",              s_buyhold,        ["D1"]),
    ("Weekly swing v1 (live)",  s_weekly_swing_v1,["D1", "H4", "H1"]),
]
