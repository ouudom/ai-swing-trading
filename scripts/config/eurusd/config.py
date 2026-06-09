"""EURUSD instrument config — euro vs USD. Inherits FX-major defaults from config._fx_base."""

from config._fx_base import *  # noqa: F401,F403  (FX-major shared defaults)

SYMBOL       = "EUR/USD"
SYM_CLEAN    = "eurusd"
DISPLAY_NAME = "EURUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/eurusd"
PULL_DIR = "data/weekly_pull/eurusd"

# Foreign carry leg: ECB Deposit Facility Rate (daily FRED).
RATE_FOREIGN      = "ECBDFR"
RATE_FOREIGN_NAME = "ECB Deposit Rate"
FOREIGN_CCY       = "EZ"

# Direction (DGS2) + US carry (DFF) + risk (VIXCLS) + foreign carry (ECBDFR).
FRED_SERIES = FRED_SERIES_BASE + [RATE_FOREIGN]

# COT — CME EUR FX futures (6E).
COT_CONTRACT_NAME = "EURO FX - CHICAGO MERCANTILE EXCHANGE"

# Volume Profile via CME EUR futures continuous (yfinance).
VP_TICKER = "6E=F"

# Note: DXY is ~58% euro-weighted, so DXY slope is near-circular for EURUSD
# (it's essentially inverse price momentum, not independent macro). Kept in the
# snapshot as context only — confluence weighting handled in P3 backtest.
