"""Trade (filled position) schemas."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import field_validator, model_validator

from .base import Direction, ExitReason, SchemaBase, SetupLetter, validate_week


class Trade(SchemaBase):
    """A single filled trade with optional exit data."""

    id: int | None = None
    date: date
    week: str
    instrument: str
    setup: SetupLetter
    direction: Direction
    entry: float
    sl: float
    tp: float
    lots: float
    stop_dist: float
    r_planned: float
    fill_time: datetime
    exit_time: datetime | None = None
    exit_px: float | None = None
    exit_reason: ExitReason | None = None
    r_actual: float | None = None
    mfe: float | None = None
    mae: float | None = None
    notes: str | None = None

    @field_validator("week")
    @classmethod
    def _week(cls, v: str) -> str:
        return validate_week(v)

    @model_validator(mode="after")
    def _exit_consistency(self) -> "Trade":
        if self.exit_time is not None and self.exit_px is None:
            raise ValueError("exit_px is required when exit_time is set")
        if self.exit_px is not None and self.exit_reason is None:
            raise ValueError("exit_reason is required when exit_px is set")
        return self
