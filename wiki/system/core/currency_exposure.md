---
type: system
updated: 2026-06-10
confidence: high
tags: [risk, fx, portfolio, netting, correlation, advisory]
related: [constitution, decisions, eurusd_profile, gbpusd_profile, eurgbp_profile]
---

# Currency-Leg Netting — FX Portfolio Exposure (ADVISORY, D024)

## Why this exists
FX pairs are **not independent** — they share currency legs. EURUSD short + GBPUSD short is
not two $2000 trades; it is **one 2× long-USD bet** dressed as two. With the full 10-instrument
FX set the same trap appears on every leg: USDJPY long + EURJPY long = 2× short JPY;
GBPJPY short + GBPUSD short = 2× short GBP. Triangle identities (`EURGBP = EURUSD/GBPUSD`,
`EURJPY = EURUSD × USDJPY`, `GBPJPY = GBPUSD × USDJPY`) mean an explicit cross can silently
stack on a cross already implied by two held majors.

True triangular arbitrage is NOT tradeable retail (HFT latency). This page is the opposite
problem: not capturing the triangle — **not accidentally betting it twice without noticing.**

## D024 — advisory, not enforcement (operator decision 2026-06-10)
> This system **generates trading signals; it is not a risk-management system.** No hard
> per-currency or total-FX $ cap is enforced. The ledger's job is to **flag** shared-leg
> concentration between pairs (e.g. EURUSD vs GBPUSD) and **suggest the single cleaner trade**
> (highest Entry Confluence). The operator decides what to actually hold.

This supersedes the D022 hard gate (keep-best-**drop**-weaker with forced ❌ SKIP) and the
Architecture-B per-axis $2000 cap. The leg algebra survives; the enforcement does not.

## Leg decomposition — all 10 FX instruments
Every pair = `+base −quote` for a LONG; a SHORT flips signs. 8 currencies.

| Instrument | Long = legs | Class |
|---|---|---|
| EURUSD | `+EUR −USD` | USD-quote major |
| GBPUSD | `+GBP −USD` | USD-quote major |
| AUDUSD | `+AUD −USD` | USD-quote major |
| NZDUSD | `+NZD −USD` | USD-quote major |
| USDCAD | `+USD −CAD` | USD-base |
| USDCHF | `+USD −CHF` | USD-base |
| USDJPY | `+USD −JPY` | USD-base |
| EURGBP | `+EUR −GBP` | cross |
| EURJPY | `+EUR −JPY` | cross |
| GBPJPY | `+GBP −JPY` | cross |

Note the USD-base sign flip: **long USDJPY is LONG USD** — it stacks with a SHORT EURUSD,
not a long one. The ledger handles this; intuition often doesn't.

## The concentration signal
For each currency, sum signed legs across all live + candidate FX orders
(units = risk$/2000). **Flag = ≥2 orders contributing the SAME sign on the same currency.**
Net-zero is not safety: EURUSD long + GBPUSD short nets USD to 0 but is exactly a long-EURGBP
cross bet — which the ledger still surfaces the moment an explicit cross order joins it
(the EUR and GBP legs double).

Soft advisory (not a leg): **AUDUSD + NZDUSD same direction** ≈ one bet (corr ~0.85) even
though AUD and NZD are distinct currencies — emitted as a note.

## Workflow — runs inside /validate at order-finalization
```bash
bash scripts/pyrun.sh scripts/fx_exposure.py --live "<other live FX orders>" \
     --candidate "<this inst:dir:risk>" --new-ec <EC> --live-ecs "<inst:ec,...>"
```
- `INDEPENDENT` → place normally.
- `CONCENTRATED` → place if it passed Entry Confluence, **but** emit
  `> [!warning] Concentration: <orders> share <side> <CCY> leg — one factor, not independent.
  Ledger suggests keeping <best> (EC x.x).` in the daily file + mirror to `_HOT.md`.
  Operator chooses whether to drop the weaker order. Nothing is auto-skipped/auto-cancelled.

Audit view of any portfolio: `fx_exposure.py --orders "inst:dir:risk,..."`.
Selftest: `fx_exposure.py --selftest` (12 cases incl. USD-base flips, JPY stacks, cross-on-implied).

## Scope boundaries
- **Gold excluded.** XAUUSD is USD-priced but real-yield driven — not a clean USD leg.
  Surface gold/USD co-movement as context only.
- **Within-instrument stacking** (PRIMARY + SECONDARY same pair) is the constitution's
  Multi-Zone rule, not the ledger's — literal scale-in, allowed.

## History
- **D022 (2026-06-09):** original 3-instrument / 2-axis (USD, EURGBP-cross) hard gate,
  $2000/axis cap, forced keep-best-drop-weaker. Architecture A/B framing.
- **D024 (2026-06-10):** generalized to 10 instruments / 8 currency legs; enforcement dropped
  → advisory + suggestion. Architecture B's ledger built, its caps deliberately not adopted.

Cross-links: [[constitution]] (Portfolio Currency-Leg Netting), [[decisions]] D022/D024.
