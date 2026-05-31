---
type: research
updated: 2026-05-24
confidence: medium
tags: [session, timing, London, NY, Asia, DOW]
related: [confluence_criteria]
---

# Session Timing — Findings

**Data**: H1 UTC, 2020-01-24→2026-05-24. N=39,220 H1 bars.

## Session Volatility (H1 candle range by UTC hour)

- **London open 08:00–10:00 UTC**: highest H1 range — peak volatility window
- **NY open 13:00–15:00 UTC**: second volatility peak
- **Asia session 00:00–07:00 UTC**: lowest range, minimal movement
- **Directional return by hour**: near-zero across all hours — session edge is VOLATILITY, not direction

Implication: limits placed for London or NY execution benefit from higher volatility → better chance of reaching zone, triggering, and following through.

## Day-of-Week Bias (D1 returns)

| Day | Mean daily return | N |
|---|---|---|
| Monday | +0.068% | 330 |
| Tuesday | +0.075% | 329 |
| **Wednesday** | **+0.087%** | 329 |
| Thursday | +0.058% | 330 |
| **Friday** | **+0.035%** | 322 |

- Wednesday strongest, Friday weakest
- Weak effect — not tradeable alone, no statistical significance
- **Friday risk**: new position on Friday carries weekend gap risk. Prefer not placing new limits Friday afternoon.

## Key Conclusions

1. **Session edge = volatility, not direction** — London/NY open best execution windows
2. **G4 gate (08:00–17:00 UTC)** validated: restricts to high-volatility sessions
3. Asia-session limits get triggered on thin moves that can reverse on London open — avoid
4. Friday new entries carry weekend gap risk — note in weekly forecast no-trade events if applicable

## Open Questions

- Does filter G4 combined with actual entry zone proximity improve TP% at 3R?
- NFP day (1st Friday) — specific day-of-week patterns? (NFP analysis pending)
- Does trading on days with high previous-day ATR improve or hurt outcomes?
