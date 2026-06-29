"""Shared config base for USD-BASE pairs (USD/CAD, USD/CHF, USD/JPY) — D024 wave 2/3.

Inherits the FX defaults from config._fx_base, then flips everything that assumed the pair was
quoted FOREIGN/USD:

  - USD_BETA_SIGN = +1 — long the pair IS long USD. USD strength (DXY up, US rates up) is
    BULLISH the pair, not bearish. weekly_pull macro labels + backtest_signals USD-mechanical
    rows (DXY, M-rows) read this and flip direction.
  - COT_INVERTED = True — CME futures quote the FOREIGN currency (6C/6S/6J): spec net LONG the
    future = long CAD/CHF/JPY = SHORT the pair. Snapshot prints both readings.
  - VP_TICKER = None — the futures chart is the pair UPSIDE-DOWN; volume-profile levels do not
    map onto pair price. Disabled rather than misread.
  - QUOTE_CCY is the foreign currency → pip value is quote-CCY denominated. D024 operator
    ruling (historical; TICK_MULTIPLIER no longer drives lot sizing — system is R-multiple
    only, retained as a PRICE_DP display-precision heuristic): non-JPY pairs keep TICK 100000
    (CHF ~25% over / CAD ~28% under accepted); JPY pairs override TICK_MULTIPLIER=650
    (static ≈100000/154 — the 100000 formula is wrong by ~155×, not a drift).

Per-pair modules set: SYMBOL, SYM_CLEAN, DISPLAY_NAME, TD_DIR, PULL_DIR, FOREIGN_CCY,
RATE_FOREIGN(=None mostly), COT_CONTRACT_NAME, V1B_BUFFER (+ JPY: TICK_MULTIPLIER, PIP_SIZE,
PRICE_DP, MIN_BAR_RANGE).
"""

from config._fx_base import *  # noqa: F401,F403  (FX shared defaults)

# Long pair = LONG USD (base currency). Flips DXY/US-rate row directions + macro labels.
USD_BETA_SIGN = +1

# CME FX futures are FOREIGN/USD → positioning reads inverted for a USD-base pair.
COT_INVERTED = True

# Futures continuous chart is the inverse of the pair — VP levels unusable. Off.
VP_TICKER = None
