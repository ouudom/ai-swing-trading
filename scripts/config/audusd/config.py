"""AUDUSD instrument config — aussie vs USD. Inherits FX-major defaults from config._fx_base.

USD-quote major, same class as EURUSD/GBPUSD (USD_BETA_SIGN=-1, pip=0.0001, TICK 100000).
Onboarded under D024 (7-pair expansion, pair #1). Differences vs EUR/GBP:
  - No daily FRED policy series for the RBA (monthly OECD only) → RATE_FOREIGN=None; the
    rate_diff macro block keeps the US2Y direction leg + VIX and skips the carry diff
    (carry-diff was DEAD for EUR/GBP anyway — D021).
  - AUD is a commodity/China-beta currency: RBA + China tier-1 data (CPI/PMI/trade) are
    event blocks; iron-ore/copper context has no free daily series — narrative only.
  - Antipodean correlation: AUDUSD+NZDUSD same direction ≈ one bet (corr ~0.85) — the
    fx_exposure ledger emits an advisory note (D024).
Signal character (mean-reversion vs momentum) = decided by the P3 scan, not assumed.
"""

from config._fx_base import *  # noqa: F401,F403  (FX-major shared defaults)

SYMBOL       = "AUD/USD"
SYM_CLEAN    = "audusd"
DISPLAY_NAME = "AUDUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/audusd"
PULL_DIR = "data/weekly_pull/audusd"

# Foreign carry leg: RBA cash rate has NO daily FRED series → carry leg disabled.
RATE_FOREIGN      = None
RATE_FOREIGN_NAME = "RBA cash rate"
FOREIGN_CCY       = "AU"

# Direction (DGS2) + US carry (DFF) + risk (VIXCLS) only — no foreign daily series.
FRED_SERIES = FRED_SERIES_BASE

# V1b invalidation buffer: 4 pips past zone, 2 consecutive H4 closes (ATR ≈ 80% of EURUSD's 5-pip).
V1B_BUFFER = 0.0004

# COT — CME Australian dollar futures (6A).
COT_CONTRACT_NAME = "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"

# Volume Profile via CME AUD futures continuous (yfinance).
VP_TICKER = "6A=F"

# Intermarket commodity proxies (#3, D025) — narrative CONTEXT only, NOT scored (needs a
# research scan before any confluence weight). Copper = China-demand proxy (no clean free
# China PMI series); iron ore = AU's #1 export. FRED monthly + yfinance daily.
COMMODITY_FRED = ["PIORECRUSDM"]      # global price of iron ore (monthly)
COMMODITY_YF   = {"copper": "HG=F"}   # COMEX copper front-month (daily)
