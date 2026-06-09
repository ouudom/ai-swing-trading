"""GBPUSD instrument config — sterling vs USD. Inherits FX-major defaults from config._fx_base."""

from config._fx_base import *  # noqa: F401,F403  (FX-major shared defaults)

SYMBOL       = "GBP/USD"
SYM_CLEAN    = "gbpusd"
DISPLAY_NAME = "GBPUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/gbpusd"
PULL_DIR = "data/weekly_pull/gbpusd"

# Foreign carry leg: SONIA (Sterling Overnight Index Average, daily FRED) as BoE-rate proxy.
RATE_FOREIGN      = "IUDSOIA"
RATE_FOREIGN_NAME = "UK SONIA"
FOREIGN_CCY       = "UK"

# Direction (DGS2) + US carry (DFF) + risk (VIXCLS) + foreign carry (SONIA).
FRED_SERIES = FRED_SERIES_BASE + [RATE_FOREIGN]

# COT — CME GBP FX futures (6B).
COT_CONTRACT_NAME = "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"

# Volume Profile via CME GBP futures continuous (yfinance).
VP_TICKER = "6B=F"

# Note: GBP is only ~12% of DXY, so DXY slope is a cleaner (less circular) macro
# signal for GBPUSD than for EURUSD. Confluence weighting handled in P3 backtest.
