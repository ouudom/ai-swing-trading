"""Swing-trading structured schemas (Pydantic v2)."""

from .base import (
    AdxRegime,
    Alignment,
    Bias,
    Confidence,
    Direction,
    ExitReason,
    GateStatus,
    OrderResult,
    SchemaBase,
    SetupLetter,
    SetupLifecycle,
)
from .daily import DailyValidation, HardBlock, ValidationGate
from .hot import ActiveSetup, OpenPosition, PortfolioState
from .snapshot import DataSnapshot, OhlcTail, PivotLevel
from .trade import Trade
from .weekly import MacroDriver, Setup, WeeklyForecast
from .backtest import BacktestConfig, BacktestTrade, BacktestResult

__all__ = [
    # base
    "AdxRegime",
    "Alignment",
    "Bias",
    "Confidence",
    "Direction",
    "ExitReason",
    "GateStatus",
    "OrderResult",
    "SchemaBase",
    "SetupLetter",
    "SetupLifecycle",
    # weekly
    "MacroDriver",
    "Setup",
    "WeeklyForecast",
    # daily
    "DailyValidation",
    "HardBlock",
    "ValidationGate",
    # trade
    "Trade",
    # hot
    "ActiveSetup",
    "OpenPosition",
    "PortfolioState",
    # snapshot
    "DataSnapshot",
    "OhlcTail",
    "PivotLevel",
    # backtest
    "BacktestConfig",
    "BacktestTrade",
    "BacktestResult",
]
