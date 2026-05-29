"""CRUD operations: Pydantic models ↔ SQLite rows."""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from schemas import (
    ActiveSetup,
    BacktestConfig,
    BacktestResult,
    BacktestTrade,
    DailyValidation,
    DataSnapshot,
    HardBlock,
    MacroDriver,
    OpenPosition,
    PortfolioState,
    Setup,
    Trade,
    ValidationGate,
    WeeklyForecast,
)

from .connection import get_conn


# ── JSON helpers ─────────────────────────────────────────────────────────────

def _to_json(value: Any) -> str:
    return json.dumps(value, default=str)


def _from_json(value: str | None, default: Any = None) -> Any:
    if value is None:
        return default
    return json.loads(value)


def _iso(dt: datetime | date | None) -> str | None:
    if dt is None:
        return None
    return dt.isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    if value is None:
        return None
    # sqlite3 PARSE_DECLTYPES handles datetime for declared columns,
    # but for text fields we parse manually.
    if "T" in value:
        return datetime.fromisoformat(value)
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def _bool_int(value: bool) -> int:
    return 1 if value else 0


def _int_bool(value: int) -> bool:
    return bool(value)


# ── Weekly Forecasts ─────────────────────────────────────────────────────────

def create_weekly_forecast(wf: WeeklyForecast) -> WeeklyForecast:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO weekly_forecasts
            (week, generated, instrument, macro_bias, macro_confidence,
             mtf_alignment, best_setup, conviction, baseline_dfii10,
             baseline_dxy, baseline_ratediff, weekend_gap_pct, cot_mm_net,
             cot_mm_net_chg, etf_gld_tonnes, etf_gld_wk_chg, adx_regime,
             d1_atr, h4_atr, d1_atr_compressed, macro_drivers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                wf.week,
                wf.generated.isoformat(),
                wf.instrument,
                wf.macro_bias.value,
                wf.macro_confidence.value,
                wf.mtf_alignment.value,
                wf.best_setup.value if wf.best_setup else None,
                wf.conviction.value,
                wf.baseline_dfii10,
                wf.baseline_dxy,
                wf.baseline_ratediff,
                wf.weekend_gap_pct,
                wf.cot_mm_net,
                wf.cot_mm_net_chg,
                wf.etf_gld_tonnes,
                wf.etf_gld_wk_chg,
                wf.adx_regime.value,
                wf.d1_atr,
                wf.h4_atr,
                _bool_int(wf.d1_atr_compressed),
                _to_json([m.model_dump() for m in wf.macro_drivers]),
            ),
        )
        wf_id = cur.lastrowid
        conn.commit()

    # insert child setups
    for s in wf.setups:
        create_setup(wf_id, s)

    return get_weekly_forecast(wf.week, wf.instrument)


def get_weekly_forecast(week: str, instrument: str) -> WeeklyForecast | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM weekly_forecasts WHERE week = ? AND instrument = ?",
            (week, instrument),
        ).fetchone()
        if row is None:
            return None

        setups = get_setups_by_forecast_id(row["id"])
        return WeeklyForecast(
            id=row["id"],
            week=row["week"],
            generated=date.fromisoformat(row["generated"]),
            instrument=row["instrument"],
            macro_bias=row["macro_bias"],
            macro_confidence=row["macro_confidence"],
            mtf_alignment=row["mtf_alignment"],
            best_setup=row["best_setup"],
            conviction=row["conviction"],
            baseline_dfii10=row["baseline_dfii10"],
            baseline_dxy=row["baseline_dxy"],
            baseline_ratediff=row["baseline_ratediff"],
            weekend_gap_pct=row["weekend_gap_pct"],
            cot_mm_net=row["cot_mm_net"],
            cot_mm_net_chg=row["cot_mm_net_chg"],
            etf_gld_tonnes=row["etf_gld_tonnes"],
            etf_gld_wk_chg=row["etf_gld_wk_chg"],
            adx_regime=row["adx_regime"],
            d1_atr=row["d1_atr"],
            h4_atr=row["h4_atr"],
            d1_atr_compressed=_int_bool(row["d1_atr_compressed"]),
            macro_drivers=[MacroDriver(**m) for m in _from_json(row["macro_drivers"], [])],
            setups=setups,
        )


def list_weekly_forecasts(instrument: str | None = None) -> list[WeeklyForecast]:
    with get_conn() as conn:
        if instrument:
            rows = conn.execute(
                "SELECT week, instrument FROM weekly_forecasts WHERE instrument = ? ORDER BY week",
                (instrument,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT week, instrument FROM weekly_forecasts ORDER BY week"
            ).fetchall()
    return [get_weekly_forecast(r["week"], r["instrument"]) for r in rows if r]


# ── Setups ───────────────────────────────────────────────────────────────────

def create_setup(weekly_forecast_id: int, s: Setup) -> Setup:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO setups
            (weekly_forecast_id, letter, label, direction, zone_top, zone_bottom,
             signals, score, conviction, stop_distance, entry_offset, limit_price,
             stop_price, tp_price, lots, r_multiple, invalidation_rule, tp_anchor_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                weekly_forecast_id,
                s.letter.value,
                s.label,
                s.direction.value,
                s.zone_top,
                s.zone_bottom,
                _to_json(s.signals),
                s.score,
                s.conviction.value,
                s.stop_distance,
                s.entry_offset,
                s.limit_price,
                s.stop_price,
                s.tp_price,
                s.lots,
                s.r_multiple,
                s.invalidation_rule,
                s.tp_anchor_name,
            ),
        )
        conn.commit()
    return s


def get_setups_by_forecast_id(forecast_id: int) -> list[Setup]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM setups WHERE weekly_forecast_id = ? ORDER BY letter",
            (forecast_id,),
        ).fetchall()
    return [
        Setup(
            id=r["id"],
            letter=r["letter"],
            label=r["label"],
            direction=r["direction"],
            zone_top=r["zone_top"],
            zone_bottom=r["zone_bottom"],
            signals=_from_json(r["signals"], {}),
            score=r["score"],
            conviction=r["conviction"],
            stop_distance=r["stop_distance"],
            entry_offset=r["entry_offset"],
            limit_price=r["limit_price"],
            stop_price=r["stop_price"],
            tp_price=r["tp_price"],
            lots=r["lots"],
            r_multiple=r["r_multiple"],
            invalidation_rule=r["invalidation_rule"],
            tp_anchor_name=r["tp_anchor_name"],
        )
        for r in rows
    ]


# ── Daily Validations ────────────────────────────────────────────────────────

def create_daily_validation(dv: DailyValidation) -> DailyValidation:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO daily_validations
            (date, week, instrument, active_setup, hard_blocks, validation_gates,
             validation_score, floor_used, h1_trigger_present, h1_trigger_description,
             weekly_confluence_score, stop_distance, stop_type, pivot_price,
             structural_dist, entry_offset, order_result, limit_price, limit_direction,
             limit_expires, h4_atr, d1_atr, d1_atr_compressed, dfii10_slope,
             dfii10_drift, vix, asia_range, intraday_updates)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date, instrument) DO UPDATE SET
                week=excluded.week,
                active_setup=excluded.active_setup,
                hard_blocks=excluded.hard_blocks,
                validation_gates=excluded.validation_gates,
                validation_score=excluded.validation_score,
                floor_used=excluded.floor_used,
                h1_trigger_present=excluded.h1_trigger_present,
                h1_trigger_description=excluded.h1_trigger_description,
                weekly_confluence_score=excluded.weekly_confluence_score,
                stop_distance=excluded.stop_distance,
                stop_type=excluded.stop_type,
                pivot_price=excluded.pivot_price,
                structural_dist=excluded.structural_dist,
                entry_offset=excluded.entry_offset,
                order_result=excluded.order_result,
                limit_price=excluded.limit_price,
                limit_direction=excluded.limit_direction,
                limit_expires=excluded.limit_expires,
                h4_atr=excluded.h4_atr,
                d1_atr=excluded.d1_atr,
                d1_atr_compressed=excluded.d1_atr_compressed,
                dfii10_slope=excluded.dfii10_slope,
                dfii10_drift=excluded.dfii10_drift,
                vix=excluded.vix,
                asia_range=excluded.asia_range,
                intraday_updates=excluded.intraday_updates
            """,
            (
                dv.date.isoformat(),
                dv.week,
                dv.instrument,
                dv.active_setup.value if dv.active_setup else None,
                _to_json([hb.model_dump() for hb in dv.hard_blocks]),
                _to_json([vg.model_dump() for vg in dv.validation_gates]),
                dv.validation_score,
                dv.floor_used,
                _bool_int(dv.h1_trigger_present),
                dv.h1_trigger_description,
                dv.weekly_confluence_score,
                dv.stop_distance,
                dv.stop_type,
                dv.pivot_price,
                dv.structural_dist,
                dv.entry_offset,
                dv.order_result.value,
                dv.limit_price,
                dv.limit_direction.value if dv.limit_direction else None,
                _iso(dv.limit_expires),
                dv.h4_atr,
                dv.d1_atr,
                _bool_int(dv.d1_atr_compressed),
                dv.dfii10_slope,
                dv.dfii10_drift,
                dv.vix,
                dv.asia_range,
                _to_json(dv.intraday_updates),
            ),
        )
        conn.commit()
    return get_daily_validation(dv.date, dv.instrument)


def get_daily_validation_by_id(dv_id: int) -> DailyValidation | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM daily_validations WHERE id = ?", (dv_id,)
        ).fetchone()
    if row is None:
        return None
    return _row_to_daily_validation(row)


def get_daily_validation(date: date, instrument: str) -> DailyValidation | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM daily_validations WHERE date = ? AND instrument = ?",
            (date.isoformat(), instrument),
        ).fetchone()
    if row is None:
        return None
    return _row_to_daily_validation(row)


def get_latest_daily_validation(instrument: str) -> DailyValidation | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM daily_validations WHERE instrument = ? ORDER BY date DESC LIMIT 1",
            (instrument,),
        ).fetchone()
    if row is None:
        return None
    return _row_to_daily_validation(row)


def list_daily_validations(instrument: str, limit: int = 30) -> list[DailyValidation]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM daily_validations WHERE instrument = ? ORDER BY date DESC LIMIT ?",
            (instrument, limit),
        ).fetchall()
    return [_row_to_daily_validation(r) for r in rows]


def _row_to_daily_validation(row: Any) -> DailyValidation:
    return DailyValidation(
        id=row["id"],
        date=date.fromisoformat(row["date"]),
        week=row["week"],
        instrument=row["instrument"],
        active_setup=row["active_setup"],
        hard_blocks=[HardBlock(**hb) for hb in _from_json(row["hard_blocks"], [])],
        validation_gates=[ValidationGate(**vg) for vg in _from_json(row["validation_gates"], [])],
        validation_score=row["validation_score"],
        floor_used=row["floor_used"],
        h1_trigger_present=_int_bool(row["h1_trigger_present"]),
        h1_trigger_description=row["h1_trigger_description"],
        weekly_confluence_score=row["weekly_confluence_score"],
        stop_distance=row["stop_distance"],
        stop_type=row["stop_type"],
        pivot_price=row["pivot_price"],
        structural_dist=row["structural_dist"],
        entry_offset=row["entry_offset"],
        order_result=row["order_result"],
        limit_price=row["limit_price"],
        limit_direction=row["limit_direction"],
        limit_expires=_parse_iso(row["limit_expires"]),
        h4_atr=row["h4_atr"],
        d1_atr=row["d1_atr"],
        d1_atr_compressed=_int_bool(row["d1_atr_compressed"]),
        dfii10_slope=row["dfii10_slope"],
        dfii10_drift=row["dfii10_drift"],
        vix=row["vix"],
        asia_range=row["asia_range"],
        intraday_updates=_from_json(row["intraday_updates"], []),
    )


# ── Trades ───────────────────────────────────────────────────────────────────

def create_trade(t: Trade) -> Trade:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO trades
            (date, week, instrument, setup, direction, entry, sl, tp, lots,
             stop_dist, r_planned, fill_time, exit_time, exit_px, exit_reason,
             r_actual, mfe, mae, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                t.date.isoformat(),
                t.week,
                t.instrument,
                t.setup.value,
                t.direction.value,
                t.entry,
                t.sl,
                t.tp,
                t.lots,
                t.stop_dist,
                t.r_planned,
                t.fill_time.isoformat(),
                t.exit_time.isoformat() if t.exit_time else None,
                t.exit_px,
                t.exit_reason.value if t.exit_reason else None,
                t.r_actual,
                t.mfe,
                t.mae,
                t.notes,
            ),
        )
        t_id = cur.lastrowid
        conn.commit()
    return get_trade_by_id(t_id)


def update_trade_exit(
    trade_id: int,
    exit_time: datetime,
    exit_px: float,
    exit_reason: str,
    r_actual: float | None = None,
    mfe: float | None = None,
    mae: float | None = None,
    notes: str | None = None,
) -> Trade | None:
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE trades
            SET exit_time = ?, exit_px = ?, exit_reason = ?,
                r_actual = ?, mfe = ?, mae = ?, notes = ?
            WHERE id = ?
            """,
            (
                exit_time.isoformat(),
                exit_px,
                exit_reason,
                r_actual,
                mfe,
                mae,
                notes,
                trade_id,
            ),
        )
        conn.commit()
    return get_trade_by_id(trade_id)


def get_trade_by_id(trade_id: int) -> Trade | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()
    if row is None:
        return None
    return _row_to_trade(row)


def get_open_trades(instrument: str | None = None) -> list[Trade]:
    sql = "SELECT * FROM trades WHERE exit_time IS NULL"
    params: tuple = ()
    if instrument:
        sql += " AND instrument = ?"
        params = (instrument,)
    sql += " ORDER BY fill_time DESC"
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_trade(r) for r in rows]


def get_all_trades(instrument: str | None = None, limit: int = 1000) -> list[Trade]:
    sql = "SELECT * FROM trades"
    params: tuple = ()
    if instrument:
        sql += " WHERE instrument = ?"
        params = (instrument,)
    sql += " ORDER BY fill_time DESC LIMIT ?"
    params += (limit,)
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_trade(r) for r in rows]


def _row_to_trade(row: Any) -> Trade:
    return Trade(
        id=row["id"],
        date=date.fromisoformat(row["date"]),
        week=row["week"],
        instrument=row["instrument"],
        setup=row["setup"],
        direction=row["direction"],
        entry=row["entry"],
        sl=row["sl"],
        tp=row["tp"],
        lots=row["lots"],
        stop_dist=row["stop_dist"],
        r_planned=row["r_planned"],
        fill_time=datetime.fromisoformat(row["fill_time"]),
        exit_time=datetime.fromisoformat(row["exit_time"]) if row["exit_time"] else None,
        exit_px=row["exit_px"],
        exit_reason=row["exit_reason"],
        r_actual=row["r_actual"],
        mfe=row["mfe"],
        mae=row["mae"],
        notes=row["notes"],
    )


# ── Active Setups ────────────────────────────────────────────────────────────

def upsert_active_setup(s: ActiveSetup) -> ActiveSetup:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO active_setups
            (week, instrument, setup_letter, direction, zone_top, zone_bottom,
             score, limit_price, lifecycle, placed_at, expires_at,
             invalidation_price, weekly_forecast_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(instrument, setup_letter, lifecycle) DO UPDATE SET
                week=excluded.week,
                direction=excluded.direction,
                zone_top=excluded.zone_top,
                zone_bottom=excluded.zone_bottom,
                score=excluded.score,
                limit_price=excluded.limit_price,
                lifecycle=excluded.lifecycle,
                placed_at=excluded.placed_at,
                expires_at=excluded.expires_at,
                invalidation_price=excluded.invalidation_price,
                weekly_forecast_id=excluded.weekly_forecast_id,
                updated_at=datetime('now')
            """,
            (
                s.week,
                s.instrument,
                s.setup_letter.value,
                s.direction.value,
                s.zone_top,
                s.zone_bottom,
                s.score,
                s.limit_price,
                s.lifecycle.value,
                _iso(s.placed_at),
                _iso(s.expires_at),
                s.invalidation_price,
                s.weekly_forecast_id,
            ),
        )
        conn.commit()
    return get_active_setup(s.instrument, s.setup_letter)


def get_active_setup(instrument: str, setup_letter: str) -> ActiveSetup | None:
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT * FROM active_setups
            WHERE instrument = ? AND setup_letter = ?
            ORDER BY updated_at DESC LIMIT 1
            """,
            (instrument, setup_letter),
        ).fetchone()
    if row is None:
        return None
    return _row_to_active_setup(row)


def get_active_setups(instrument: str | None = None) -> list[ActiveSetup]:
    sql = "SELECT * FROM active_setups WHERE lifecycle NOT IN ('CLOSED', 'INVALIDATED')"
    params: tuple = ()
    if instrument:
        sql += " AND instrument = ?"
        params = (instrument,)
    sql += " ORDER BY updated_at DESC"
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_active_setup(r) for r in rows]


def delete_active_setup(setup_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM active_setups WHERE id = ?", (setup_id,))
        conn.commit()


def _row_to_active_setup(row: Any) -> ActiveSetup:
    return ActiveSetup(
        id=row["id"],
        week=row["week"],
        instrument=row["instrument"],
        setup_letter=row["setup_letter"],
        direction=row["direction"],
        zone_top=row["zone_top"],
        zone_bottom=row["zone_bottom"],
        score=row["score"],
        limit_price=row["limit_price"],
        lifecycle=row["lifecycle"],
        placed_at=_parse_iso(row["placed_at"]),
        expires_at=_parse_iso(row["expires_at"]),
        invalidation_price=row["invalidation_price"],
        weekly_forecast_id=row["weekly_forecast_id"],
    )


# ── Open Positions ───────────────────────────────────────────────────────────

def create_open_position(pos: OpenPosition) -> OpenPosition:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO open_positions
            (trade_id, setup_id, instrument, direction, entry, sl, tp, lots,
             r_planned, fill_time, current_mtm, highest_r, lowest_r)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pos.trade_id,
                pos.setup_id,
                pos.instrument,
                pos.direction.value,
                pos.entry,
                pos.sl,
                pos.tp,
                pos.lots,
                pos.r_planned,
                pos.fill_time.isoformat(),
                pos.current_mtm,
                pos.highest_r,
                pos.lowest_r,
            ),
        )
        conn.commit()
    return get_open_position_by_trade_id(pos.trade_id)


def get_open_position_by_trade_id(trade_id: int) -> OpenPosition | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM open_positions WHERE trade_id = ?", (trade_id,)
        ).fetchone()
    if row is None:
        return None
    return _row_to_open_position(row)


def get_open_positions(instrument: str | None = None) -> list[OpenPosition]:
    sql = "SELECT * FROM open_positions"
    params: tuple = ()
    if instrument:
        sql += " WHERE instrument = ?"
        params = (instrument,)
    sql += " ORDER BY fill_time DESC"
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_open_position(r) for r in rows]


def delete_open_position(trade_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM open_positions WHERE trade_id = ?", (trade_id,))
        conn.commit()


def _row_to_open_position(row: Any) -> OpenPosition:
    return OpenPosition(
        id=row["id"],
        trade_id=row["trade_id"],
        setup_id=row["setup_id"],
        instrument=row["instrument"],
        direction=row["direction"],
        entry=row["entry"],
        sl=row["sl"],
        tp=row["tp"],
        lots=row["lots"],
        r_planned=row["r_planned"],
        fill_time=datetime.fromisoformat(row["fill_time"]),
        current_mtm=row["current_mtm"],
        highest_r=row["highest_r"],
        lowest_r=row["lowest_r"],
    )


# ── Portfolio Snapshots ──────────────────────────────────────────────────────

def create_portfolio_snapshot(ps: PortfolioState) -> PortfolioState:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO portfolio_snapshots
            (week, total_risk_allocated, total_risk_cap, weekly_trades_filled,
             weekly_loss, month_to_date_loss, drawdown_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ps.week,
                ps.total_risk_allocated,
                ps.total_risk_cap,
                ps.weekly_trades_filled,
                ps.weekly_loss,
                ps.month_to_date_loss,
                ps.drawdown_pct,
            ),
        )
        conn.commit()
    return ps


def get_latest_portfolio_snapshot() -> PortfolioState | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM portfolio_snapshots ORDER BY captured_at DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    return PortfolioState(
        week=row["week"],
        total_risk_allocated=row["total_risk_allocated"],
        total_risk_cap=row["total_risk_cap"],
        weekly_trades_filled=row["weekly_trades_filled"],
        weekly_loss=row["weekly_loss"],
        month_to_date_loss=row["month_to_date_loss"],
        drawdown_pct=row["drawdown_pct"],
    )


# ── Data Snapshots ───────────────────────────────────────────────────────────

def create_data_snapshot(ds: DataSnapshot) -> DataSnapshot:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO data_snapshots
            (week, instrument, generated, spot, ema_50, ema_200, rsi_14,
             macd_line, macd_signal, adx_14, atr_d1, atr_h4, d1_structure,
             h4_structure, volume_profile_poc, volume_profile_vah, volume_profile_val,
             cot_mm_net, cot_mm_net_chg, etf_gld_tonnes, etf_gld_wk_chg,
             weekend_gap_pct, dfii10, dgs10, dxy, vix, pivots, ohlc_tails, raw_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(week, instrument) DO UPDATE SET
                generated=excluded.generated,
                spot=excluded.spot,
                ema_50=excluded.ema_50,
                ema_200=excluded.ema_200,
                rsi_14=excluded.rsi_14,
                macd_line=excluded.macd_line,
                macd_signal=excluded.macd_signal,
                adx_14=excluded.adx_14,
                atr_d1=excluded.atr_d1,
                atr_h4=excluded.atr_h4,
                d1_structure=excluded.d1_structure,
                h4_structure=excluded.h4_structure,
                volume_profile_poc=excluded.volume_profile_poc,
                volume_profile_vah=excluded.volume_profile_vah,
                volume_profile_val=excluded.volume_profile_val,
                cot_mm_net=excluded.cot_mm_net,
                cot_mm_net_chg=excluded.cot_mm_net_chg,
                etf_gld_tonnes=excluded.etf_gld_tonnes,
                etf_gld_wk_chg=excluded.etf_gld_wk_chg,
                weekend_gap_pct=excluded.weekend_gap_pct,
                dfii10=excluded.dfii10,
                dgs10=excluded.dgs10,
                dxy=excluded.dxy,
                vix=excluded.vix,
                pivots=excluded.pivots,
                ohlc_tails=excluded.ohlc_tails,
                raw_text=excluded.raw_text
            """,
            (
                ds.week,
                ds.instrument,
                ds.generated.isoformat(),
                ds.spot,
                ds.ema_50,
                ds.ema_200,
                ds.rsi_14,
                ds.macd_line,
                ds.macd_signal,
                ds.adx_14,
                ds.atr_d1,
                ds.atr_h4,
                ds.d1_structure,
                ds.h4_structure,
                ds.volume_profile_poc,
                ds.volume_profile_vah,
                ds.volume_profile_val,
                ds.cot_mm_net,
                ds.cot_mm_net_chg,
                ds.etf_gld_tonnes,
                ds.etf_gld_wk_chg,
                ds.weekend_gap_pct,
                ds.dfii10,
                ds.dgs10,
                ds.dxy,
                ds.vix,
                _to_json([p.model_dump() for p in ds.pivots]),
                _to_json([t.model_dump() for t in ds.ohlc_tails]),
                ds.raw_text,
            ),
        )
        ds_id = cur.lastrowid
        conn.commit()
    return get_data_snapshot_by_id(ds_id)


def get_data_snapshot_by_id(ds_id: int) -> DataSnapshot | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM data_snapshots WHERE id = ?", (ds_id,)).fetchone()
    if row is None:
        return None
    return _row_to_data_snapshot(row)


def get_data_snapshot(week: str, instrument: str) -> DataSnapshot | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM data_snapshots WHERE week = ? AND instrument = ?",
            (week, instrument),
        ).fetchone()
    if row is None:
        return None
    return _row_to_data_snapshot(row)


def _row_to_data_snapshot(row: Any) -> DataSnapshot:
    from schemas import OhlcTail, PivotLevel

    return DataSnapshot(
        id=row["id"],
        week=row["week"],
        instrument=row["instrument"],
        generated=date.fromisoformat(row["generated"]),
        spot=row["spot"],
        ema_50=row["ema_50"],
        ema_200=row["ema_200"],
        rsi_14=row["rsi_14"],
        macd_line=row["macd_line"],
        macd_signal=row["macd_signal"],
        adx_14=row["adx_14"],
        atr_d1=row["atr_d1"],
        atr_h4=row["atr_h4"],
        d1_structure=row["d1_structure"],
        h4_structure=row["h4_structure"],
        volume_profile_poc=row["volume_profile_poc"],
        volume_profile_vah=row["volume_profile_vah"],
        volume_profile_val=row["volume_profile_val"],
        cot_mm_net=row["cot_mm_net"],
        cot_mm_net_chg=row["cot_mm_net_chg"],
        etf_gld_tonnes=row["etf_gld_tonnes"],
        etf_gld_wk_chg=row["etf_gld_wk_chg"],
        weekend_gap_pct=row["weekend_gap_pct"],
        dfii10=row["dfii10"],
        dgs10=row["dgs10"],
        dxy=row["dxy"],
        vix=row["vix"],
        pivots=[PivotLevel(**p) for p in _from_json(row["pivots"], [])],
        ohlc_tails=[OhlcTail(**t) for t in _from_json(row["ohlc_tails"], [])],
        raw_text=row["raw_text"],
    )
