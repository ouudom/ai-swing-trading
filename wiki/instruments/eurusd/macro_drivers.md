---
type: system
updated: 2026-05-28
confidence: medium
tags: [eurusd, macro, drivers, fundamental]
related: [profile.md, confluence_criteria.md]
---

# EURUSD Macro / Fundamental Drivers

> Feeds **S5 (weekly) + G4 (daily) as a 0-POINT VETO** — NOT a scored signal (unlike DFII10 for
> gold, which scores). EUR macro is null/regime-unstable as a standalone directional signal
> (research below), so it cannot ADD conviction — it can only BLOCK a fade when fundamentals are
> strongly driving price further into the extreme. Multi-factor + discretionary; never a mechanical
> slope gate. (D016.)

## Primary drivers (ranked)

### 1. US–EU rate differential  [core of S6 / G3]
- Proxy: **DGS2 − ESTR** (US 2y vs euro short-term rate), daily. Also watch DGS10−Bund and Fed/ECB policy spread.
- Direction (textbook): wider US advantage → USD bid → EUR bearish. EUR long wants differential slope < 0; short > 0.
- **Caveat (research 2026-05-28):** as a *lone mechanical slope gate* this had ~0 edge over 22yr and
  flipped sign across regimes (textbook 2010-23, inverted 2023-26). So: use as direction CONTEXT inside
  multi-factor confluence + discretionary forecast, NOT as a standalone trigger. Confidence MEDIUM at best.

### 2. Fed / ECB policy + forward guidance
- DFF vs ECB deposit rate (ECBDFR); meeting outcomes, dot-path / guidance tone. Drives the differential's trend.

### 3. Relative growth & inflation
- EU HICP, German CPI, EU/German PMI vs US CPI/PCE/ISM. Surprise vs consensus matters most
  (consensus feed not yet wired — flagged in research index).

### 4. DXY (inverse) [G3 confirm]
- `data/yahoo/DXY.csv` (ICE). EUR ≈ 57.6% of DXY → strong inverse. DXY 20d trend confirms G3.
  Note: near-mirror of EUR price, so it confirms, doesn't independently lead.

### 5. Risk sentiment / VIX [G5]
- USD safe-haven bid on risk-off. VIXCLS regime table → G5. VIX>35 → shorts blocked.

### 6. COT positioning (context)
- CFTC EURO FX spec net (`data/cftc/eur_cot_net.csv`). Research: no standalone edge (corr +0.01) →
  context/extreme-flag only, not a scored signal.

## News (V3 + T4-X)
ECB decision + presser, EU HICP, German CPI/PMI, plus US NFP/FOMC/CPI/Retail/PCE-GDP. Hard-block
within 2h of London/NY open; structured-shock scan per T4-X. See constitution_addendum.

## Data
DGS2, DGS10, DFII10, ECBESTRVOLWGTTRMDMNRT (ESTR), DFF, ECBDFR, VIXCLS (FRED); DXY (yahoo); EUR COT (cftc).
Full research + nulls: `wiki/research/eurusd/_INDEX.md`.
