"""NZDUSD instrument config — kiwi vs USD. Inherits FX-major defaults from config._fx_base.

USD-quote major, same class as AUDUSD/EURUSD/GBPUSD (USD_BETA_SIGN=-1, pip=0.0001, TICK 100000).
Onboarded under D024 (7-pair expansion, pair #2). Same data caveats as AUDUSD:
  - No daily FRED policy series for the RBNZ (monthly OECD only) → RATE_FOREIGN=None; the
    rate_diff macro block keeps the US2Y direction leg + VIX and skips the carry diff.
  - NZD is a commodity/China-beta currency (dairy instead of iron ore): RBNZ + China tier-1 +
    GDT dairy auctions are event considerations; no free daily commodity series — narrative only.
  - Antipodean correlation: AUDUSD+NZDUSD same direction ≈ one bet (corr ~0.85) — fx_exposure
    ledger emits an advisory note (D024).
Signal character = decided by the P3 scan, not assumed (AUD scanned mean-reverting H4-centric).
"""

from config._fx_base import *  # noqa: F401,F403  (FX-major shared defaults)

SYMBOL       = "NZD/USD"
SYM_CLEAN    = "nzdusd"
DISPLAY_NAME = "NZDUSD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/nzdusd"
PULL_DIR = "data/weekly_pull/nzdusd"

# Foreign carry leg: RBNZ OCR has NO daily FRED series → carry leg disabled.
RATE_FOREIGN      = None
RATE_FOREIGN_NAME = "RBNZ OCR"
FOREIGN_CCY       = "NZ"

# Direction (DGS2) + US carry (DFF) + risk (VIXCLS) only — no foreign daily series.
FRED_SERIES = FRED_SERIES_BASE

# V1b invalidation buffer: set after ATR calibration (NZD vol ≈ AUD; placeholder 4 pips).
V1B_BUFFER = 0.0004

# COT — CME NZ dollar futures (6N). Exact CFTC name verified in local archive.
COT_CONTRACT_NAME = "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE"

# Volume Profile via CME NZD futures continuous (yfinance).
VP_TICKER = "6N=F"

# Intermarket commodity proxies (#3, D025) — narrative CONTEXT only, NOT scored. Dairy = NZ's
# #1 export (Fonterra/GDT); copper = China-demand proxy. FRED monthly + yfinance daily.
COMMODITY_FRED = ["PDAIRYUSDM"]       # global price of dairy (monthly)
COMMODITY_YF   = {"copper": "HG=F"}   # COMEX copper front-month (daily; shared China proxy)
