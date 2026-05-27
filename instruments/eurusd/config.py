"""EURUSD instrument config — scaffold. System details TBD.

TODO: define confluence gates, macro drivers, re-forecast triggers
      before running /weekly eurusd.
"""

SYMBOL       = "EUR/USD"
SYM_CLEAN    = "eurusd"
DISPLAY_NAME = "EURUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/eurusd"
PULL_DIR = "data/weekly_pull/eurusd"

# FRED series — USD macro still relevant; expand with EU-specific series TBD
# TODO: add EU macro: ECB rate series, EU inflation, EU PMI (non-FRED sources)
FRED_SERIES = ["DFF", "VIXCLS", "DGS10"]

# COT (CFTC EUR/USD futures) — disabled until system defined
# TODO: verify exact contract name from CFTC deahistfo{year}.zip
COT_ENABLED       = False
COT_CONTRACT_NAME = "EURO FX - CHICAGO MERCANTILE EXCHANGE"  # unverified

# ETF flows — no direct ETF equivalent for EURUSD
ETF_ENABLED      = False
ETF_TICKER       = None
ETF_HOLDINGS_CSV = None

# Volume Profile — EUR/USD futures
VP_TICKER = "6E=F"

# Lot sizing: $2000 / (stop_distance × TICK_MULTIPLIER) = lots
# EURUSD: $0.0001 pip × 100,000 units = $10/pip per standard lot
# stop_distance expressed in price (e.g. 0.0050 = 50 pips)
# $2000 / (0.0050 × 10000) = 40 lots — adjust if using mini/micro
TICK_MULTIPLIER = 10000

# Market hours: same Fri 22:00 UTC close as CME
MARKET_CLOSE_WEEKDAY  = 4
MARKET_CLOSE_HOUR_UTC = 22
MARKET_REOPEN_WEEKDAY  = 6
MARKET_REOPEN_HOUR_UTC = 22
