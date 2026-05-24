"""Trade execution + metrics."""
from dataclasses import dataclass, field, asdict
from typing import List
import numpy as np
import pandas as pd


@dataclass
class Config:
    initial: float = 100_000.0
    risk_pct: float = 0.01
    rr: float = 2.5
    be_r: float = 1.5  # move stop to BE at +be_r R; 0 disables
    cost: float = 0.50  # per oz per side


@dataclass
class Trade:
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: int
    entry: float
    exit: float
    size: float
    risk_dist: float
    pnl: float
    r_mult: float
    reason: str


@dataclass
class Result:
    name: str
    equity: pd.Series
    trades: List[Trade] = field(default_factory=list)


def open_trade(cfg: Config, direction, entry_px, risk_dist, equity):
    size = (equity * cfg.risk_pct) / risk_dist
    equity -= cfg.cost * size
    stop = entry_px - risk_dist if direction > 0 else entry_px + risk_dist
    tp = entry_px + cfg.rr * risk_dist if direction > 0 else entry_px - cfg.rr * risk_dist
    be_trigger = entry_px + cfg.be_r * risk_dist if direction > 0 else entry_px - cfg.be_r * risk_dist
    return size, stop, tp, be_trigger, equity


def close_pnl(cfg, direction, entry, exit_px, size, risk_dist):
    raw = (exit_px - entry) * direction * size
    pnl = raw - cfg.cost * size
    r = (exit_px - entry) * direction / risk_dist if risk_dist > 0 else 0
    return pnl, r


def manage(cfg: Config, pos, entry, stop, tp, be_trig, size, row, be_armed, risk_dist):
    """Returns (exit_px, reason, new_stop, be_armed). exit_px None if still open."""
    h, l = row.high, row.low
    if cfg.be_r > 0 and not be_armed:
        if pos > 0 and h >= be_trig:
            stop = entry; be_armed = True
        elif pos < 0 and l <= be_trig:
            stop = entry; be_armed = True
    if pos > 0:
        if l <= stop:
            return stop, "stop", stop, be_armed
        if h >= tp:
            return tp, "tp", stop, be_armed
    else:
        if h >= stop:
            return stop, "stop", stop, be_armed
        if l <= tp:
            return tp, "tp", stop, be_armed
    return None, None, stop, be_armed


def metrics(name, equity: pd.Series, trades: List[Trade], bpy=252):
    rets = equity.pct_change().dropna()
    years = max((equity.index[-1] - equity.index[0]).days / 365.25, 0.01)
    final = float(equity.iloc[-1])
    cagr = (final / equity.iloc[0]) ** (1 / years) - 1 if final > 0 else -1
    sharpe = rets.mean() / rets.std() * np.sqrt(bpy) if rets.std() > 0 else 0
    dd = (equity / equity.cummax() - 1).min()
    pnls = [t.pnl for t in trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    pf = (sum(wins) / -sum(losses)) if losses and sum(losses) < 0 else (float("inf") if wins else 0)
    wr = len(wins) / len(trades) if trades else 0
    avg_r = float(np.mean([t.r_mult for t in trades])) if trades else 0
    return {
        "strategy": name,
        "final": round(final),
        "PnL$": round(final - equity.iloc[0]),
        "CAGR": round(cagr * 100, 1),
        "Sharpe": round(sharpe, 2),
        "MaxDD%": round(dd * 100, 1),
        "trades": len(trades),
        "win%": round(wr * 100),
        "PF": round(pf, 2) if pf != float("inf") else "inf",
        "avgR": round(avg_r, 2),
    }
