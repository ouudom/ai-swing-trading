"""Data snapshot schema for weekly_pull outputs."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from .base import SchemaBase


class OhlcTail(SchemaBase):
    """OHLC tail data for a timeframe."""

    tf: str
    open: float
    high: float
    low: float
    close: float


class PivotLevel(SchemaBase):
    """A pivot or support/resistance level."""

    name: str
    price: float


class DataSnapshot(SchemaBase):
    """Structured representation of a weekly_pull.txt snapshot."""

    id: int | None = None
    week: str
    instrument: str
    generated: date
    spot: float
    ema_50: float | None = None
    ema_200: float | None = None
    rsi_14: float | None = None
    macd_line: float | None = None
    macd_signal: float | None = None
    adx_14: float | None = None
    atr_d1: float | None = None
    atr_h4: float | None = None
    d1_structure: str | None = None
    h4_structure: str | None = None
    volume_profile_poc: float | None = None
    volume_profile_vah: float | None = None
    volume_profile_val: float | None = None
    cot_mm_net: int | None = None
    cot_mm_net_chg: int | None = None
    etf_gld_tonnes: float | None = None
    etf_gld_wk_chg: float | None = None
    weekend_gap_pct: float | None = None
    dfii10: float | None = None
    dgs10: float | None = None
    dxy: float | None = None
    vix: float | None = None
    pivots: list[PivotLevel] = Field(default_factory=list)
    ohlc_tails: list[OhlcTail] = Field(default_factory=list)
    raw_text: str | None = None
