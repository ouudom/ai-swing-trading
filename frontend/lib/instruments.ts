// The 10 active instruments, in constitution order. Used by the cockpit + zone-board grid.
export const INSTRUMENTS = [
  "xauusd",
  "eurusd",
  "gbpusd",
  "eurgbp",
  "audusd",
  "nzdusd",
  "usdcad",
  "usdchf",
  "usdjpy",
  "eurjpy",
  "gbpjpy",
] as const;

export type Instrument = (typeof INSTRUMENTS)[number];

// Price precision per instrument. lightweight-charts needs the right `minMove`
// or it can't build a price scale for sub-cent FX ranges (the chart then keeps a
// stale scale and the candles flatten into an invisible sliver). JPY-quoted pairs
// carry pip 0.01 → 3dp; other FX 5dp; gold 2dp.
const JPY_QUOTED = new Set(["usdjpy", "eurjpy", "gbpjpy"]);

export function pricePrecision(instrument: string): { precision: number; minMove: number } {
  const i = instrument.toLowerCase();
  if (i === "xauusd") return { precision: 2, minMove: 0.01 };
  if (JPY_QUOTED.has(i)) return { precision: 3, minMove: 0.001 };
  return { precision: 5, minMove: 0.00001 };
}
