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

# FRED series. Macro driver = US-EU short-rate differential (DGS2 - ESTR), daily + independent
# of EUR price (unlike DXY). German Bund is monthly-only on FRED, so a 10y differential is not
# feasible free; ESTR (euro overnight, daily) supplies the EU side, DGS2 carries the daily move.
#   DGS2  = US 2y (rate-expectations, dominant EURUSD driver)
#   DFII10/DGS10 = US real/nominal 10y (context)
#   ECBESTRVOLWGTTRMDMNRT = ESTR euro short-term rate (daily)
#   DFF, VIXCLS = policy + risk regime
# Differential slope's predictive power on EUR direction must be CONFIRMED in Phase-2 research
# before its weight is locked (edge-first).
FRED_SERIES = ["DGS2", "DGS10", "DFII10", "ECBESTRVOLWGTTRMDMNRT", "DFF", "VIXCLS"]

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

# Lot sizing: lots = $2000 / (stop_distance_price × TICK_MULTIPLIER)
# EURUSD standard lot = 100,000 units → a 1.0 price move = $100,000/lot → TICK_MULTIPLIER = 100000.
# stop_distance in PRICE (e.g. 0.0020 = 20 pips). $2000 / (0.0020 × 100000) = 10 lots
# = 10 lots × $10/pip × 20 pip = $2000 risk. ✓  (was 10000 — 10× over-risk bug, fixed 2026-05-28)
TICK_MULTIPLIER = 100000

# H4 "trading-day" ATR filter: 5 pips (0.0005) is the EUR-scale equivalent of gold's $1.
MIN_BAR_RANGE = 0.0005

# G6 quiet-window gate: EUR's Asia is dead → use London/pre-NY 07:00–13:00 UTC instead.
# Range threshold in price (30 pips = 0.0030).
G6_WINDOW_UTC = (7, 13)
G6_RANGE_MAX = 0.0030

# Market hours: same Fri 22:00 UTC close as CME
MARKET_CLOSE_WEEKDAY  = 4
MARKET_CLOSE_HOUR_UTC = 22
MARKET_REOPEN_WEEKDAY  = 6
MARKET_REOPEN_HOUR_UTC = 22

# Correlation guard: EUR rises when USD falls → inverse → -1.
# usd_position(trade) = trade_dir(+1 long / -1 short) × USD_BETA_SIGN
#   EURUSD short = -1 × -1 = +1 (long USD). EURUSD long = -1 (short USD).
# NOTE: XAUUSD and EURUSD share USD_BETA_SIGN = -1 → a gold-short + EUR-short
# both resolve to +1 (long USD) = stacked dollar bet. Correlation guard applies.
USD_BETA_SIGN = -1
