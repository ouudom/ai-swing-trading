"""Tests for markdown/CSV rendering."""

from __future__ import annotations

import csv
import tempfile
from datetime import date, datetime
from pathlib import Path

import yaml

from render import render_daily_validation, render_weekly_forecast, export_trades_to_csv
from schemas import (
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
    Trade,
    ValidationGate,
    WeeklyForecast,
)


class TestWeeklyMdRender:
    def test_frontmatter_keys_present(self):
        wf = WeeklyForecast(
            week="2026-W22",
            generated=date(2026, 5, 25),
            instrument="xauusd",
            macro_bias=Bias.BEARISH,
            macro_confidence=Confidence.MEDIUM_HIGH,
            mtf_alignment="ALIGNED",
            best_setup=SetupLetter.A,
            conviction=Confidence.MEDIUM_HIGH,
            baseline_dfii10=2.18,
            baseline_dxy=99.239,
            weekend_gap_pct=1.46,
            cot_mm_net=148660,
            cot_mm_net_chg=-16514,
            etf_gld_tonnes=1052.56,
            adx_regime="TRENDING",
            d1_atr=70.49,
            h4_atr=31.21,
            d1_atr_compressed=True,
            macro_drivers=[
                MacroDriver(name="DFII10", value=2.18, delta_1w=0.18, signal="rising"),
            ],
            setups=[
                Setup(
                    letter=SetupLetter.A,
                    label="POC Retest Short",
                    direction=Direction.SHORT,
                    zone_top=4575.0,
                    zone_bottom=4530.0,
                    score=8.0,
                    conviction=Confidence.MEDIUM_HIGH,
                    stop_distance=28.30,
                    entry_offset=16.98,
                    limit_price=4591.98,
                    stop_price=4620.28,
                    tp_price=4501.11,
                    lots=0.70,
                    r_multiple=3.21,
                    invalidation_rule="D1 close above 4575",
                    tp_anchor_name="D1 swing low",
                    signals={"S1": True, "S6": True, "S7": True},
                ),
            ],
        )
        md = render_weekly_forecast(wf)
        assert md.startswith("---")

        # Parse frontmatter
        fm_text = md.split("---\n")[1]
        fm = yaml.safe_load(fm_text)
        assert fm["type"] == "weekly_forecast"
        assert fm["week"] == "2026-W22"
        assert fm["macro_bias"] == "BEARISH"
        assert fm["baseline_dfii10"] == 2.18

    def test_body_contains_setup(self):
        wf = WeeklyForecast(
            week="2026-W22",
            generated=date(2026, 5, 25),
            instrument="xauusd",
            macro_bias=Bias.BEARISH,
            macro_confidence=Confidence.MEDIUM,
            mtf_alignment="ALIGNED",
            conviction=Confidence.MEDIUM,
            adx_regime="TRENDING",
            d1_atr=70.0,
            h4_atr=30.0,
            d1_atr_compressed=True,
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
            ],
        )
        md = render_weekly_forecast(wf)
        assert "Setup A — Test [8.0/10] HIGH" in md
        assert "Direction | SHORT" in md


class TestDailyMdRender:
    def test_frontmatter_and_body(self):
        dv = DailyValidation(
            date=date(2026, 5, 26),
            week="2026-W22",
            instrument="xauusd",
            active_setup=SetupLetter.A,
            hard_blocks=[HardBlock(name="V1", passed=True), HardBlock(name="V3", passed=True)],
            validation_gates=[
                ValidationGate(code="G1", name="structure", weight=4.0, passed=True),
            ],
            validation_score=10.0,
            h1_trigger_present=True,
            weekly_confluence_score=8.0,
            stop_distance=25.40,
            structural_dist=5.94,
            entry_offset=15.24,
            order_result=OrderResult.PLACED,
            limit_price=4590.24,
            limit_direction=Direction.SHORT,
            limit_expires=datetime(2026, 5, 26, 21, 0),
            h4_atr=25.87,
            d1_atr=88.77,
            d1_atr_compressed=True,
            dfii10_slope=0.29,
            dfii10_drift=0.0,
        )
        md = render_daily_validation(dv)
        assert md.startswith("---")

        fm_text = md.split("---\n")[1]
        fm = yaml.safe_load(fm_text)
        assert fm["type"] == "daily_validation"
        assert fm["validation_score"] == 10.0
        assert fm["order_limit"] == "PLACED"

        assert "✅ ORDER LIMIT" in md
        assert "Validation Score (max 10.0)" in md


class TestTradeCsvRender:
    def test_round_trip(self):
        trades = [
            Trade(
                date=date(2026, 5, 26),
                week="2026-W22",
                instrument="xauusd",
                setup=SetupLetter.A,
                direction=Direction.SHORT,
                entry=4590.24,
                sl=4615.64,
                tp=4501.11,
                lots=0.78,
                stop_dist=25.40,
                r_planned=3.51,
                fill_time=datetime(2026, 5, 26, 14, 30),
            ),
            Trade(
                date=date(2026, 5, 27),
                week="2026-W22",
                instrument="xauusd",
                setup=SetupLetter.B,
                direction=Direction.LONG,
                entry=4500.0,
                sl=4480.0,
                tp=4600.0,
                lots=1.0,
                stop_dist=20.0,
                r_planned=5.0,
                fill_time=datetime(2026, 5, 27, 10, 0),
                exit_time=datetime(2026, 5, 27, 16, 0),
                exit_px=4600.0,
                exit_reason=ExitReason.TP,
                r_actual=5.0,
            ),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        export_trades_to_csv(path, trades)

        with open(path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["setup"] == "A"
        assert rows[0]["direction"] == "SHORT"
        assert rows[1]["exit_reason"] == "TP"
        assert rows[1]["r_actual"] == "5.0"

        Path(path).unlink()
