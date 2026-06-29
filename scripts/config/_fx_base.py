"""Shared FX-major config base (USD pairs: EUR/USD, GBP/USD).

Per-pair modules `from config._fx_base import *` then override the pair-specific
fields (SYMBOL, SYM_CLEAN, DISPLAY_NAME, TD_DIR, PULL_DIR, VP_TICKER, RATE_FOREIGN*,
COT_CONTRACT_NAME). Everything common to FX majors lives here.

Contrast with gold (config/xauusd/config.py): gold is a single-driver real-yield
instrument; FX majors are a two-country rate story (MACRO_MODE="rate_diff").
"""

# ── Macro: FX = US-vs-foreign rate story, NOT gold's single real-yield driver ──
# Direction leg  = US 2Y (DGS2) slope — USD rate momentum (rising US 2Y → USD up → pair down).
# Carry/regime   = policy differential DFF − foreign policy rate (per pair).
MACRO_MODE        = "rate_diff"
RATE_US           = "DGS2"      # US 2Y nominal — rate-momentum leg (drives pair direction)
POLICY_US         = "DFF"       # Fed funds effective — US carry leg
# RATE_FOREIGN, RATE_FOREIGN_NAME, FOREIGN_CCY → set per pair.

# FRED series to fetch. DGS2 (direction) + DGS10 (2s10s curve) + DFF (US carry)
# + VIXCLS (risk gate); the foreign policy rate is appended per pair.
FRED_SERIES_BASE  = ["DGS2", "DGS10", "DFF", "VIXCLS"]

# ── COT — CME currency futures exist (EUR=6E, GBP=6B). Contract name per pair. ──
COT_ENABLED       = True
# COT_CONTRACT_NAME → set per pair.

# ── No bullion-style ETF flow proxy for FX majors. ──
ETF_ENABLED       = False
ETF_TICKER        = None
ETF_HOLDINGS_CSV  = None

# ── TICK_MULTIPLIER: legacy price-scale constant (standard FX lot = 100,000 units).
#    No longer used for lot sizing (system is R-multiple only) — retained as a heuristic
#    input to PRICE_DP (display decimal precision) in weekly_pull.load_instrument(). ──
TICK_MULTIPLIER   = 100000

# ── H4 trading-day ATR filter: FX bars move in pips, not $. Drop flatline bars below this range. ──
MIN_BAR_RANGE     = 0.0003

# ── Market hours: spot FX = same Globex window (Sun 22:00 → Fri 22:00 UTC) as gold. ──
MARKET_CLOSE_WEEKDAY   = 4   # Friday
MARKET_CLOSE_HOUR_UTC  = 22
MARKET_REOPEN_WEEKDAY  = 6   # Sunday
MARKET_REOPEN_HOUR_UTC = 22

# ── Correlation guard: pair rises when USD falls → inverse → -1 (same polarity as gold).
#    usd_position(trade) = trade_dir(+1 long / -1 short) × USD_BETA_SIGN. ──
USD_BETA_SIGN = -1

# ── Pip size: smallest quoted increment block (1 pip). 0.0001 for standard pairs;
#    JPY-quoted pairs override to 0.01. Drives big-figure math (100 pips = 1 figure). ──
PIP_SIZE = 0.0001
