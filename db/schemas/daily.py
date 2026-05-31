"""Daily validation schemas."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import Field, field_validator, model_validator

from .base import (
    AdxRegime,
    Confidence,
    Direction,
    OrderResult,
    SchemaBase,
    SetupLetter,
    validate_score,
    validate_week,
)


class HardBlock(SchemaBase):
    """A hard block (V1, V1b, V3, G4)."""

    name: str
    passed: bool
    note: str = ""


class ValidationGate(SchemaBase):
    """A single validation gate (G1, G3, G2, V2, G5, G6)."""

    code: str
    name: str
    weight: float
    passed: bool
    note: str = ""


class DailyValidation(SchemaBase):
    """Top-level daily validation document."""

    id: int | None = None
    date: date
    week: str
    instrument: str
    active_setup: SetupLetter | None = None
    hard_blocks: list[HardBlock] = Field(default_factory=list)
    validation_gates: list[ValidationGate] = Field(default_factory=list)
    validation_score: float
    floor_used: float = Field(default=6.0, ge=0.0, le=10.0)
    h1_trigger_present: bool
    h1_trigger_description: str | None = None
    weekly_confluence_score: float
    stop_distance: float
    stop_type: str = "structural"
    pivot_price: float | None = None
    structural_dist: float
    entry_offset: float
    order_result: OrderResult
    limit_price: float | None = None
    limit_direction: Direction | None = None
    limit_expires: datetime | None = None
    h4_atr: float
    d1_atr: float
    d1_atr_compressed: bool
    dfii10_slope: float = 0.0
    dfii10_drift: float = 0.0
    vix: float | None = None
    asia_range: float | None = None
    intraday_updates: list[str] = Field(default_factory=list)

    @field_validator("week")
    @classmethod
    def _week(cls, v: str) -> str:
        return validate_week(v)

    @field_validator("validation_score")
    @classmethod
    def _score(cls, v: float) -> float:
        return validate_score(v)

    @model_validator(mode="after")
    def _limit_consistency(self) -> "DailyValidation":
        if self.order_result == OrderResult.PLACED:
            if self.limit_price is None or self.limit_direction is None:
                raise ValueError("PLACED result requires limit_price and limit_direction")
        return self
