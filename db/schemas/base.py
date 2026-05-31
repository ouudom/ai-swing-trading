"""Shared enums, validators, and base mixins for swing-trading schemas."""

from __future__ import annotations

import re
from datetime import date
try:
    from enum import StrEnum
except ImportError:  # Python < 3.11
    from enum import Enum

    class StrEnum(str, Enum):
        pass
from typing import Any

from pydantic import BaseModel, field_validator, model_validator


# ── Enums ────────────────────────────────────────────────────────────────────

class Direction(StrEnum):
    LONG = "LONG"
    SHORT = "SHORT"


class Bias(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class Confidence(StrEnum):
    HIGH = "HIGH"
    MEDIUM_HIGH = "MEDIUM-HIGH"
    MEDIUM = "MEDIUM"
    MEDIUM_LOW = "MEDIUM-LOW"
    LOW = "LOW"


class Alignment(StrEnum):
    ALIGNED = "ALIGNED"
    MIXED = "MIXED"
    OPPOSING = "OPPOSING"


class AdxRegime(StrEnum):
    TRENDING = "TRENDING"
    TRANSITIONAL = "TRANSITIONAL"
    RANGING = "RANGING"


class OrderResult(StrEnum):
    PLACED = "PLACED"
    WATCH = "WATCH"
    NO_TRADE = "NO_TRADE"
    INVALIDATED = "INVALIDATED"
    EXPIRED_UNFILLED = "EXPIRED_UNFILLED"


class SetupLetter(StrEnum):
    A = "A"
    B = "B"
    C = "C"


class ExitReason(StrEnum):
    TP = "TP"
    SL = "SL"
    TIME_STOP = "TIME_STOP"
    MANUAL = "MANUAL"


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"


class SetupLifecycle(StrEnum):
    PENDING = "PENDING"
    PLACED = "PLACED"
    EXPIRED_UNFILLED = "EXPIRED_UNFILLED"
    FILLED = "FILLED"
    CLOSED = "CLOSED"
    INVALIDATED = "INVALIDATED"


# ── Validators ───────────────────────────────────────────────────────────────

_WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")


def validate_week(v: str) -> str:
    if not _WEEK_RE.match(v):
        raise ValueError(f"Invalid week format: {v!r}. Expected YYYY-WNN.")
    return v


def validate_score(v: float) -> float:
    if not 0.0 <= v <= 10.0:
        raise ValueError(f"Score must be 0.0–10.0, got {v}")
    return v


def validate_zone(top: float, bottom: float) -> None:
    if top <= bottom:
        raise ValueError(f"Zone top ({top}) must be > bottom ({bottom})")


# ── Base Model ───────────────────────────────────────────────────────────────

class SchemaBase(BaseModel):
    """Base model with common config."""

    model_config = {"extra": "forbid", "validate_assignment": True}
