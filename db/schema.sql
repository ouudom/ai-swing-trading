-- Swing-trading SQLite schema
-- Source of truth for structured forecast, validation, trade, and state data.

PRAGMA foreign_keys = ON;

-- ── Weekly Forecasts ────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS weekly_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week TEXT NOT NULL,
    generated TEXT NOT NULL,  -- ISO date
    instrument TEXT NOT NULL,
    macro_bias TEXT NOT NULL,
    macro_confidence TEXT NOT NULL,
    mtf_alignment TEXT NOT NULL,
    best_setup TEXT,
    conviction TEXT NOT NULL,
    baseline_dfii10 REAL,
    baseline_dxy REAL,
    baseline_ratediff REAL,
    weekend_gap_pct REAL,
    cot_mm_net INTEGER,
    cot_mm_net_chg INTEGER,
    etf_gld_tonnes REAL,
    etf_gld_wk_chg REAL,
    adx_regime TEXT NOT NULL,
    d1_atr REAL NOT NULL,
    h4_atr REAL NOT NULL,
    d1_atr_compressed INTEGER NOT NULL,  -- bool: 0/1
    macro_drivers TEXT NOT NULL DEFAULT '[]',  -- JSON array
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (week, instrument)
);

-- ── Setups (linked to weekly_forecasts) ────────────────────────────────────

CREATE TABLE IF NOT EXISTS setups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weekly_forecast_id INTEGER NOT NULL,
    letter TEXT NOT NULL,
    label TEXT NOT NULL,
    direction TEXT NOT NULL,
    zone_top REAL NOT NULL,
    zone_bottom REAL NOT NULL,
    signals TEXT NOT NULL DEFAULT '{}',  -- JSON object
    score REAL NOT NULL,
    conviction TEXT NOT NULL,
    stop_distance REAL NOT NULL,
    entry_offset REAL NOT NULL,
    limit_price REAL NOT NULL,
    stop_price REAL NOT NULL,
    tp_price REAL NOT NULL,
    lots REAL NOT NULL,
    r_multiple REAL NOT NULL,
    invalidation_rule TEXT NOT NULL,
    tp_anchor_name TEXT NOT NULL,
    FOREIGN KEY (weekly_forecast_id) REFERENCES weekly_forecasts(id) ON DELETE CASCADE,
    UNIQUE (weekly_forecast_id, letter)
);

-- ── Daily Validations ───────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS daily_validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,  -- ISO date
    week TEXT NOT NULL,
    instrument TEXT NOT NULL,
    active_setup TEXT,
    hard_blocks TEXT NOT NULL DEFAULT '[]',  -- JSON array
    validation_gates TEXT NOT NULL DEFAULT '[]',  -- JSON array
    validation_score REAL NOT NULL,
    floor_used REAL NOT NULL DEFAULT 6.0,
    h1_trigger_present INTEGER NOT NULL DEFAULT 0,  -- bool: 0/1
    h1_trigger_description TEXT,
    weekly_confluence_score REAL NOT NULL,
    stop_distance REAL NOT NULL,
    stop_type TEXT NOT NULL DEFAULT 'structural',
    pivot_price REAL,
    structural_dist REAL NOT NULL,
    entry_offset REAL NOT NULL,
    order_result TEXT NOT NULL,
    limit_price REAL,
    limit_direction TEXT,
    limit_expires TEXT,  -- ISO datetime
    h4_atr REAL NOT NULL,
    d1_atr REAL NOT NULL,
    d1_atr_compressed INTEGER NOT NULL DEFAULT 0,  -- bool: 0/1
    dfii10_slope REAL NOT NULL DEFAULT 0.0,
    dfii10_drift REAL NOT NULL DEFAULT 0.0,
    vix REAL,
    asia_range REAL,
    intraday_updates TEXT NOT NULL DEFAULT '[]',  -- JSON array
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (date, instrument)
);

-- ── Trades (filled positions, append-only history) ──────────────────────────

CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,  -- ISO date
    week TEXT NOT NULL,
    instrument TEXT NOT NULL,
    setup TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry REAL NOT NULL,
    sl REAL NOT NULL,
    tp REAL NOT NULL,
    lots REAL NOT NULL,
    stop_dist REAL NOT NULL,
    r_planned REAL NOT NULL,
    fill_time TEXT NOT NULL,  -- ISO datetime
    exit_time TEXT,  -- ISO datetime
    exit_px REAL,
    exit_reason TEXT,
    r_actual REAL,
    mfe REAL,
    mae REAL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Active Setups (current pending/placed setups) ───────────────────────────

CREATE TABLE IF NOT EXISTS active_setups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week TEXT NOT NULL,
    instrument TEXT NOT NULL,
    setup_letter TEXT NOT NULL,
    direction TEXT NOT NULL,
    zone_top REAL NOT NULL,
    zone_bottom REAL NOT NULL,
    score REAL NOT NULL,
    limit_price REAL,
    lifecycle TEXT NOT NULL DEFAULT 'PENDING',
    placed_at TEXT,  -- ISO datetime
    expires_at TEXT,  -- ISO datetime
    invalidation_price REAL,
    weekly_forecast_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (instrument, setup_letter, lifecycle)
);

-- ── Open Positions (currently running trades) ───────────────────────────────

CREATE TABLE IF NOT EXISTS open_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id INTEGER NOT NULL UNIQUE,
    setup_id INTEGER,
    instrument TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry REAL NOT NULL,
    sl REAL NOT NULL,
    tp REAL NOT NULL,
    lots REAL NOT NULL,
    r_planned REAL NOT NULL,
    fill_time TEXT NOT NULL,  -- ISO datetime
    current_mtm REAL,
    highest_r REAL,
    lowest_r REAL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Portfolio Snapshots (daily risk state) ──────────────────────────────────

CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week TEXT NOT NULL,
    total_risk_allocated REAL NOT NULL DEFAULT 0.0,
    total_risk_cap REAL NOT NULL DEFAULT 4000.0,
    weekly_trades_filled INTEGER NOT NULL DEFAULT 0,
    weekly_loss REAL NOT NULL DEFAULT 0.0,
    month_to_date_loss REAL NOT NULL DEFAULT 0.0,
    drawdown_pct REAL NOT NULL DEFAULT 0.0,
    captured_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Data Snapshots (weekly_pull outputs) ────────────────────────────────────

CREATE TABLE IF NOT EXISTS data_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week TEXT NOT NULL,
    instrument TEXT NOT NULL,
    generated TEXT NOT NULL,  -- ISO date
    spot REAL NOT NULL,
    ema_50 REAL,
    ema_200 REAL,
    rsi_14 REAL,
    macd_line REAL,
    macd_signal REAL,
    adx_14 REAL,
    atr_d1 REAL,
    atr_h4 REAL,
    d1_structure TEXT,
    h4_structure TEXT,
    volume_profile_poc REAL,
    volume_profile_vah REAL,
    volume_profile_val REAL,
    cot_mm_net INTEGER,
    cot_mm_net_chg INTEGER,
    etf_gld_tonnes REAL,
    etf_gld_wk_chg REAL,
    weekend_gap_pct REAL,
    dfii10 REAL,
    dgs10 REAL,
    dxy REAL,
    vix REAL,
    pivots TEXT NOT NULL DEFAULT '[]',  -- JSON array
    ohlc_tails TEXT NOT NULL DEFAULT '[]',  -- JSON array
    raw_text TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (week, instrument)
);

-- ── Indexes ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_wf_week_instrument ON weekly_forecasts(week, instrument);
CREATE INDEX IF NOT EXISTS idx_dv_date_instrument ON daily_validations(date, instrument);
CREATE INDEX IF NOT EXISTS idx_trades_week ON trades(week);
CREATE INDEX IF NOT EXISTS idx_trades_instrument ON trades(instrument);
CREATE INDEX IF NOT EXISTS idx_active_instrument ON active_setups(instrument);
CREATE INDEX IF NOT EXISTS idx_active_lifecycle ON active_setups(lifecycle);
CREATE INDEX IF NOT EXISTS idx_positions_instrument ON open_positions(instrument);
