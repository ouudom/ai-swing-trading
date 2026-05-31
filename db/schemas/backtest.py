"""Backtest engine schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .base import SchemaBase


class BacktestConfig(SchemaBase):
    """Backtest configuration."""

    initial: float = 100_000.0
    risk_pct: float = 0.01
    rr: float = 2.5
    be_r: float = 1.5
    cost: float = 0.50


class BacktestTrade(SchemaBase):
    """A single trade from a backtest run."""

    entry_time: datetime
    exit_time: datetime
    direction: int
    entry: float
    exit: float
    size: float
    risk_dist: float
    pnl: float
    r_mult: float
    reason: str


class BacktestResult(SchemaBase):
    """Full result of a backtest strategy run."""

    name: str
    equity: list[tuple[datetime, float]] = Field(default_factory=list)
    trades: list[BacktestTrade] = Field(default_factory=list)
