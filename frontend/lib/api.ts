// Thin client for the read-only Trading Brain API (api/main.py). Localhost only.
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";

export interface OpenPosition {
  trade_id: string;
  instrument: string;
  direction: string;
  setup: string;
  week: string;
  entry: number | null;
  sl: number | null;
  tp: number | null;
  tp2: number | null;
  lots: number | null;
  r_planned: number | null;
  r_current: number | null;
  sl_status: string;
  outcome: string;
  tp1_touched: boolean;
  tp2_touched: boolean;
  mfe_r: number | null;
  mae_r: number | null;
  last_px: number | null;
  as_of: string | null;
  ambiguous: boolean;
}

export interface PendingOrder {
  trade_id: string;
  instrument: string;
  direction: string;
  setup: string;
  entry: number | null;
  sl: number | null;
  lots: number | null;
  spot: number | null;
  distance_to_fill: number | null;
  expiry: string | null;
  as_of: string | null;
}

export interface ClosedTrade {
  trade_id: string;
  instrument: string;
  direction: string;
  week: string;
  status: string;
  r_actual: number | null;
  exit_reason: string | null;
  exit_time: string | null;
  fill_time: string | null;
}

export interface RCurvePoint {
  exit_time: string | null;
  trade_id: string;
  cum_r: number;
}

export interface PositionsResponse {
  open: OpenPosition[];
  pending: PendingOrder[];
  closed: ClosedTrade[];
  r_curve: RCurvePoint[];
}

export async function getPositions(): Promise<PositionsResponse> {
  const res = await fetch(`${API_BASE}/positions`, { cache: "no-store" });
  if (!res.ok) throw new Error(`/positions ${res.status}`);
  return res.json();
}
