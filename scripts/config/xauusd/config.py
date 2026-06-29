"""XAUUSD instrument config — gold vs USD."""

SYMBOL       = "XAU/USD"
SYM_CLEAN    = "xauusd"
DISPLAY_NAME = "XAUUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/xauusd"
PULL_DIR = "data/weekly_pull/xauusd"

# FRED series to fetch
FRED_SERIES = ["DFII10", "DGS10", "T5YIE", "DFF", "VIXCLS"]

# COT (CFTC gold futures)
COT_ENABLED       = True
COT_CONTRACT_NAME = "GOLD - COMMODITY EXCHANGE INC."

# ETF flows (SPDR GLD)
ETF_ENABLED      = True
ETF_TICKER       = "GLD"
ETF_HOLDINGS_CSV = "data/gld_holdings.csv"

# Volume Profile futures ticker (yfinance)
VP_TICKER = "GC=F"

# TICK_MULTIPLIER: legacy price-scale constant ($1 move in gold = $100 per standard lot).
# No longer used for lot sizing (system is R-multiple only) — retained as a PRICE_DP
# display-precision heuristic in weekly_pull.load_instrument().
TICK_MULTIPLIER = 100

# H4 "trading-day" ATR filter: drop flatline weekend/holiday bars below this price range.
# Gold moves in $ (≥$1 = real bar).
MIN_BAR_RANGE = 1.0

# Market hours: CME Globex closes Fri 22:00 UTC, reopens Sun 22:00 UTC
MARKET_CLOSE_WEEKDAY  = 4   # Friday (0=Mon)
MARKET_CLOSE_HOUR_UTC = 22
MARKET_REOPEN_WEEKDAY  = 6  # Sunday
MARKET_REOPEN_HOUR_UTC = 22

# Correlation guard: sign of instrument-price vs USD-index correlation.
# Gold rises when USD falls → inverse → -1.
# usd_position(trade) = trade_dir(+1 long / -1 short) × USD_BETA_SIGN
#   XAUUSD short = -1 × -1 = +1 (long USD). XAUUSD long = -1 (short USD).
USD_BETA_SIGN = -1
