"""Weekly forecast schemas."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import Field, field_validator, model_validator

from .base import (
    AdxRegime,
    Alignment,
    Bias,
    Confidence,
    Direction,
    SchemaBase,
    SetupLetter,
    validate_score,
    validate_week,
    validate_zone,
)


class MacroDriver(SchemaBase):
    """A single macro driver row (e.g. DFII10, DXY)."""

    name: str
    value: float
    delta_1w: float
    signal: str


class Setup(SchemaBase):
    """A single trade setup (A, B, or C) within a weekly forecast."""

    id: int | None = None
    letter: SetupLetter
    label: str
    direction: Direction
    zone_top: float
    zone_bottom: float
    signals: dict[str, bool] = Field(default_factory=dict)
    score: float
    conviction: Confidence
    stop_distance: float
    entry_offset: float
    limit_price: float
    stop_price: float
    tp_price: float
    lots: float
    r_multiple: float
    invalidation_rule: str
    tp_anchor_name: str

    @field_validator("score")
    @classmethod
    def _score(cls, v: float) -> float:
        return validate_score(v)

    @model_validator(mode="after")
    def _zone(self) -> "Setup":
        validate_zone(self.zone_top, self.zone_bottom)
        return self

    @field_validator("signals")
    @classmethod
    def _signals(cls, v: dict[str, bool]) -> dict[str, bool]:
        allowed = {"S1", "S2", "S3", "S4", "S5", "S6", "S7"}
        bad = set(v.keys()) - allowed
        if bad:
            raise ValueError(f"Invalid signal keys: {bad}")
        return v


class WeeklyForecast(SchemaBase):
    """Top-level weekly forecast document."""

    id: int | None = None
    week: str
    generated: date
    instrument: str
    macro_bias: Bias
    macro_confidence: Confidence
    mtf_alignment: Alignment
    best_setup: SetupLetter | None = None
    conviction: Confidence
    baseline_dfii10: float | None = None
    baseline_dxy: float | None = None
    baseline_ratediff: float | None = None
    weekend_gap_pct: float | None = None
    cot_mm_net: int | None = None
    cot_mm_net_chg: int | None = None
    etf_gld_tonnes: float | None = None
    etf_gld_wk_chg: float | None = None
    macro_drivers: list[MacroDriver] = Field(default_factory=list)
    setups: list[Setup] = Field(default_factory=list)
    adx_regime: AdxRegime
    d1_atr: float
    h4_atr: float
    d1_atr_compressed: bool

    @field_validator("week")
    @classmethod
    def _week(cls, v: str) -> str:
        return validate_week(v)

    @model_validator(mode="after")
    def _setups_unique(self) -> "WeeklyForecast":
        letters = [s.letter for s in self.setups]
        if len(letters) != len(set(letters)):
            raise ValueError("Setup letters must be unique within a forecast")
        return self
