"""Tests for Pydantic schema validation and round-trips."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas import (
    ActiveSetup,
    Alignment,
    Bias,
    Confidence,
    DailyValidation,
    Direction,
    ExitReason,
    HardBlock,
    MacroDriver,
    OrderResult,
    Setup,
    SetupLetter,
    SetupLifecycle,
    Trade,
    ValidationGate,
    WeeklyForecast,
)


class TestWeeklyForecast:
    def test_minimal_valid(self):
        wf = WeeklyForecast(
            week="2026-W22",
            generated="2026-05-25",
            instrument="xauusd",
            macro_bias=Bias.BEARISH,
            macro_confidence=Confidence.MEDIUM_HIGH,
            mtf_alignment=Alignment.ALIGNED,
            conviction=Confidence.MEDIUM_HIGH,
            adx_regime="TRENDING",
            d1_atr=70.49,
            h4_atr=31.21,
            d1_atr_compressed=True,
        )
        assert wf.week == "2026-W22"
        assert wf.generated.isoformat() == "2026-05-25"

    def test_invalid_week_format(self):
        with pytest.raises(ValidationError):
            WeeklyForecast(
                week="2026-22",  # missing W
                generated="2026-05-25",
                instrument="xauusd",
                macro_bias=Bias.BEARISH,
                macro_confidence=Confidence.MEDIUM,
                mtf_alignment=Alignment.ALIGNED,
                conviction=Confidence.MEDIUM,
                adx_regime="TRENDING",
                d1_atr=1.0,
                h4_atr=1.0,
                d1_atr_compressed=False,
            )

    def test_duplicate_setup_letters(self):
        with pytest.raises(ValidationError):
            WeeklyForecast(
                week="2026-W22",
                generated="2026-05-25",
                instrument="xauusd",
                macro_bias=Bias.BEARISH,
                macro_confidence=Confidence.MEDIUM,
                mtf_alignment=Alignment.ALIGNED,
                conviction=Confidence.MEDIUM,
                adx_regime="TRENDING",
                d1_atr=1.0,
                h4_atr=1.0,
                d1_atr_compressed=False,
                setups=[
                    Setup(
                        letter=SetupLetter.A,
                        label="Test",
                        direction=Direction.SHORT,
                        zone_top=100.0,
                        zone_bottom=90.0,
                        score=8.0,
                        conviction=Confidence.HIGH,
                        stop_distance=5.0,
                        entry_offset=2.0,
                        limit_price=98.0,
                        stop_price=103.0,
                        tp_price=85.0,
                        lots=0.5,
                        r_multiple=2.6,
                        invalidation_rule="D1 close above 100",
                        tp_anchor_name="swing low",
                    ),
                    Setup(
                        letter=SetupLetter.A,  # duplicate!
                        label="Test 2",
                        direction=Direction.SHORT,
                        zone_top=110.0,
                        zone_bottom=100.0,
                        score=7.0,
                        conviction=Confidence.MEDIUM,
                        stop_distance=5.0,
                        entry_offset=2.0,
                        limit_price=108.0,
                        stop_price=113.0,
                        tp_price=95.0,
                        lots=0.5,
                        r_multiple=2.6,
                        invalidation_rule="D1 close above 110",
                        tp_anchor_name="swing low",
                    ),
                ],
            )

    def test_zone_top_must_exceed_bottom(self):
        with pytest.raises(ValidationError):
            Setup(
                letter=SetupLetter.A,
                label="Bad zone",
                direction=Direction.LONG,
                zone_top=90.0,
                zone_bottom=100.0,
                score=5.0,
                conviction=Confidence.MEDIUM,
                stop_distance=5.0,
                entry_offset=2.0,
                limit_price=85.0,
                stop_price=80.0,
                tp_price=100.0,
                lots=0.5,
                r_multiple=3.0,
                invalidation_rule="D1 close below 80",
                tp_anchor_name="swing high",
            )

    def test_score_out_of_range(self):
        with pytest.raises(ValidationError):
            WeeklyForecast(
                week="2026-W22",
                generated="2026-05-25",
                instrument="xauusd",
                macro_bias=Bias.BEARISH,
                macro_confidence=Confidence.MEDIUM,
                mtf_alignment=Alignment.ALIGNED,
                conviction=Confidence.MEDIUM,
                adx_regime="TRENDING",
                d1_atr=1.0,
                h4_atr=1.0,
                d1_atr_compressed=False,
                setups=[
                    Setup(
                        letter=SetupLetter.A,
                        label="Bad score",
                        direction=Direction.SHORT,
                        zone_top=100.0,
                        zone_bottom=90.0,
                        score=11.0,
                        conviction=Confidence.HIGH,
                        stop_distance=5.0,
                        entry_offset=2.0,
                        limit_price=98.0,
                        stop_price=103.0,
                        tp_price=85.0,
                        lots=0.5,
                        r_multiple=2.6,
                        invalidation_rule="D1 close above 100",
                        tp_anchor_name="swing low",
                    ),
                ],
            )

    def test_macro_drivers_round_trip(self):
        wf = WeeklyForecast(
            week="2026-W22",
            generated="2026-05-25",
            instrument="xauusd",
            macro_bias=Bias.BULLISH,
            macro_confidence=Confidence.HIGH,
            mtf_alignment=Alignment.ALIGNED,
            conviction=Confidence.HIGH,
            adx_regime="TRENDING",
            d1_atr=50.0,
            h4_atr=20.0,
            d1_atr_compressed=True,
            macro_drivers=[
                MacroDriver(name="DFII10", value=2.18, delta_1w=0.18, signal="rising"),
                MacroDriver(name="DXY", value=99.2, delta_1w=-0.5, signal="falling"),
            ],
        )
        assert len(wf.macro_drivers) == 2
        assert wf.macro_drivers[0].value == 2.18


class TestDailyValidation:
    def test_placed_requires_limit(self):
        with pytest.raises(ValidationError):
            DailyValidation(
                date="2026-05-26",
                week="2026-W22",
                instrument="xauusd",
                validation_score=8.0,
                h1_trigger_present=True,
                weekly_confluence_score=8.0,
                stop_distance=25.0,
                structural_dist=10.0,
                entry_offset=5.0,
                order_result=OrderResult.PLACED,
                h4_atr=25.0,
                d1_atr=70.0,
                d1_atr_compressed=True,
                dfii10_slope=0.29,
                dfii10_drift=0.0,
            )

    def test_valid_placed(self):
        dv = DailyValidation(
            date="2026-05-26",
            week="2026-W22",
            instrument="xauusd",
            active_setup=SetupLetter.A,
            hard_blocks=[HardBlock(name="V1", passed=True), HardBlock(name="V3", passed=True)],
            validation_gates=[
                ValidationGate(code="G1", name="structure", weight=4.0, passed=True),
            ],
            validation_score=8.0,
            h1_trigger_present=True,
            weekly_confluence_score=8.0,
            stop_distance=25.0,
            structural_dist=10.0,
            entry_offset=5.0,
            order_result=OrderResult.PLACED,
            limit_price=4590.24,
            limit_direction=Direction.SHORT,
            h4_atr=25.0,
            d1_atr=70.0,
            d1_atr_compressed=True,
            dfii10_slope=0.29,
            dfii10_drift=0.0,
        )
        assert dv.limit_price == 4590.24


class TestTrade:
    def test_exit_without_px_fails(self):
        with pytest.raises(ValidationError):
            Trade(
                date="2026-05-26",
                week="2026-W22",
                instrument="xauusd",
                setup=SetupLetter.A,
                direction=Direction.SHORT,
                entry=4590.24,
                sl=4615.64,
                tp=4501.11,
                lots=0.78,
                stop_dist=25.4,
                r_planned=3.51,
                fill_time="2026-05-26T14:30:00",
                exit_time="2026-05-27T09:15:00",
            )

    def test_valid_exit(self):
        t = Trade(
            date="2026-05-26",
            week="2026-W22",
            instrument="xauusd",
            setup=SetupLetter.A,
            direction=Direction.SHORT,
            entry=4590.24,
            sl=4615.64,
            tp=4501.11,
            lots=0.78,
            stop_dist=25.4,
            r_planned=3.51,
            fill_time="2026-05-26T14:30:00",
            exit_time="2026-05-27T09:15:00",
            exit_px=4501.11,
            exit_reason=ExitReason.TP,
            r_actual=3.51,
        )
        assert t.exit_reason == ExitReason.TP


class TestActiveSetup:
    def test_placed_requires_timestamp(self):
        with pytest.raises(ValidationError):
            ActiveSetup(
                week="2026-W22",
                instrument="xauusd",
                setup_letter=SetupLetter.A,
                direction=Direction.SHORT,
                zone_top=100.0,
                zone_bottom=90.0,
                score=8.0,
                lifecycle=SetupLifecycle.PLACED,
                weekly_forecast_id=1,
            )

    def test_valid_pending(self):
        s = ActiveSetup(
            week="2026-W22",
            instrument="xauusd",
            setup_letter=SetupLetter.A,
            direction=Direction.SHORT,
            zone_top=100.0,
            zone_bottom=90.0,
            score=8.0,
            lifecycle=SetupLifecycle.PENDING,
            weekly_forecast_id=1,
        )
        assert s.lifecycle == SetupLifecycle.PENDING
