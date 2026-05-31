"""Active setup, open position, and portfolio state schemas."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import Field, field_validator, model_validator

from .base import (
    Direction,
    SchemaBase,
    SetupLetter,
    SetupLifecycle,
    validate_score,
    validate_week,
)


class ActiveSetup(SchemaBase):
    """A forecast setup that is still valid (pending, placed, or watched).

    NOT a filled trade. Multiple ActiveSetups can exist per instrument per week.
    """

    id: int | None = None
    week: str
    instrument: str
    setup_letter: SetupLetter
    direction: Direction
    zone_top: float
    zone_bottom: float
    score: float
    limit_price: float | None = None
    lifecycle: SetupLifecycle
    placed_at: datetime | None = None
    expires_at: datetime | None = None
    invalidation_price: float | None = None
    weekly_forecast_id: int

    @field_validator("week")
    @classmethod
    def _week(cls, v: str) -> str:
        return validate_week(v)

    @field_validator("score")
    @classmethod
    def _score(cls, v: float) -> float:
        return validate_score(v)

    @model_validator(mode="after")
    def _lifecycle_consistency(self) -> "ActiveSetup":
        if self.lifecycle == SetupLifecycle.PLACED and self.placed_at is None:
            raise ValueError("PLACED lifecycle requires placed_at timestamp")
        return self


class OpenPosition(SchemaBase):
    """A filled trade that is currently running."""

    id: int | None = None
    trade_id: int
    setup_id: int
    instrument: str
    direction: Direction
    entry: float
    sl: float
    tp: float
    lots: float
    r_planned: float
    fill_time: datetime
    current_mtm: float | None = None
    highest_r: float | None = None
    lowest_r: float | None = None


class PortfolioState(SchemaBase):
    """Cross-instrument risk snapshot."""

    week: str
    open_positions: list[OpenPosition] = Field(default_factory=list)
    active_setups: list[ActiveSetup] = Field(default_factory=list)
    total_risk_allocated: float = 0.0
    total_risk_cap: float = 4_000.0
    weekly_trades_filled: int = 0
    weekly_loss: float = 0.0
    month_to_date_loss: float = 0.0
    drawdown_pct: float = 0.0

    @field_validator("week")
    @classmethod
    def _week(cls, v: str) -> str:
        return validate_week(v)
