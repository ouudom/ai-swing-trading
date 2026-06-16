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
