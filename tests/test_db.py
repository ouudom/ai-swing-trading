"""Tests for SQLite CRUD operations."""

from __future__ import annotations

import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest

from db import get_conn, init_db, set_db_path
from db.crud import (
    create_daily_validation,
    create_trade,
    create_weekly_forecast,
    delete_active_setup,
    get_active_setups,
    get_daily_validation,
    get_latest_daily_validation,
    get_open_positions,
    get_open_trades,
    get_trade_by_id,
    get_weekly_forecast,
    update_trade_exit,
    upsert_active_setup,
)
from schemas import (
    ActiveSetup,
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


@pytest.fixture(autouse=True)
def temp_db():
    """Use a fresh temporary database for every test."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    set_db_path(db_path)
    init_db()
    yield db_path
    # cleanup
    set_db_path(None)
    Path(db_path).unlink(missing_ok=True)


class TestWeeklyForecastCRUD:
    def _sample_forecast(self, week: str = "2026-W22") -> WeeklyForecast:
        return WeeklyForecast(
            week=week,
            generated=date(2026, 5, 25),
            instrument="xauusd",
            macro_bias=Bias.BEARISH,
            macro_confidence=Confidence.MEDIUM_HIGH,
            mtf_alignment="ALIGNED",
            conviction=Confidence.MEDIUM_HIGH,
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

    def test_create_and_read(self):
        wf = self._sample_forecast()
        created = create_weekly_forecast(wf)
        assert created.id is not None

        fetched = get_weekly_forecast("2026-W22", "xauusd")
        assert fetched is not None
        assert fetched.week == "2026-W22"
        assert fetched.instrument == "xauusd"
        assert fetched.macro_bias == Bias.BEARISH
        assert len(fetched.setups) == 1
        assert fetched.setups[0].letter == SetupLetter.A
        assert fetched.setups[0].signals["S1"] is True

    def test_unique_week_instrument(self):
        wf = self._sample_forecast()
        create_weekly_forecast(wf)
        with pytest.raises(Exception):
            create_weekly_forecast(wf)


class TestDailyValidationCRUD:
    def _sample_validation(self) -> DailyValidation:
        return DailyValidation(
            date=date(2026, 5, 26),
            week="2026-W22",
            instrument="xauusd",
            active_setup=SetupLetter.A,
            hard_blocks=[
                HardBlock(name="V1", passed=True),
                HardBlock(name="V3", passed=True),
            ],
            validation_gates=[
                ValidationGate(code="G1", name="structure", weight=4.0, passed=True),
                ValidationGate(code="G3", name="slope", weight=3.5, passed=True),
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

    def test_create_and_read(self):
        dv = self._sample_validation()
        created = create_daily_validation(dv)
        assert created.id is not None

        fetched = get_daily_validation(date(2026, 5, 26), "xauusd")
        assert fetched is not None
        assert fetched.validation_score == 10.0
        assert fetched.order_result == OrderResult.PLACED
        assert fetched.limit_price == 4590.24

    def test_upsert_same_date(self):
        dv = self._sample_validation()
        create_daily_validation(dv)
        dv.validation_score = 9.5
        dv.order_result = OrderResult.WATCH
        updated = create_daily_validation(dv)
        assert updated.validation_score == 9.5
        assert updated.order_result == OrderResult.WATCH

        # Should still be only one row
        with get_conn() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM daily_validations WHERE date = ? AND instrument = ?",
                ("2026-05-26", "xauusd"),
            ).fetchone()[0]
        assert count == 1

    def test_latest(self):
        create_daily_validation(self._sample_validation())
        fetched = get_latest_daily_validation("xauusd")
        assert fetched is not None
        assert fetched.date == date(2026, 5, 26)


class TestTradeCRUD:
    def _sample_trade(self, exit_time: datetime | None = None) -> Trade:
        return Trade(
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
            exit_time=exit_time,
            exit_px=4501.11 if exit_time else None,
            exit_reason=ExitReason.TP if exit_time else None,
            r_actual=3.51 if exit_time else None,
        )

    def test_create_and_read(self):
        t = self._sample_trade()
        created = create_trade(t)
        assert created.id is not None

        fetched = get_trade_by_id(created.id)
        assert fetched is not None
        assert fetched.entry == 4590.24
        assert fetched.exit_time is None

    def test_open_trades(self):
        create_trade(self._sample_trade())
        create_trade(self._sample_trade())
        open_trades = get_open_trades("xauusd")
        assert len(open_trades) == 2

    def test_update_exit(self):
        created = create_trade(self._sample_trade())
        updated = update_trade_exit(
            trade_id=created.id,
            exit_time=datetime(2026, 5, 27, 9, 15),
            exit_px=4501.11,
            exit_reason="TP",
            r_actual=3.51,
        )
        assert updated is not None
        assert updated.exit_reason == ExitReason.TP
        assert updated.exit_px == 4501.11

        open_trades = get_open_trades("xauusd")
        assert len(open_trades) == 0


class TestActiveSetupLifecycle:
    def _sample_active(self, lifecycle: SetupLifecycle = SetupLifecycle.PENDING) -> ActiveSetup:
        return ActiveSetup(
            week="2026-W22",
            instrument="xauusd",
            setup_letter=SetupLetter.A,
            direction=Direction.SHORT,
            zone_top=4575.0,
            zone_bottom=4530.0,
            score=8.0,
            lifecycle=lifecycle,
            weekly_forecast_id=1,
            placed_at=datetime(2026, 5, 26, 7, 30) if lifecycle == SetupLifecycle.PLACED else None,
        )

    def test_upsert_and_read(self):
        s = self._sample_active()
        upsert_active_setup(s)
        active = get_active_setups("xauusd")
        assert len(active) == 1
        assert active[0].setup_letter == SetupLetter.A

    def test_delete(self):
        s = self._sample_active()
        created = upsert_active_setup(s)
        delete_active_setup(created.id)
        assert len(get_active_setups("xauusd")) == 0

    def test_closed_filtered(self):
        upsert_active_setup(self._sample_active(SetupLifecycle.PENDING))
        upsert_active_setup(self._sample_active(SetupLifecycle.CLOSED))
        active = get_active_setups("xauusd")
        assert len(active) == 1
