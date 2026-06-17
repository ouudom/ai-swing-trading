// Thin client for the read-only Claude Swing API (api/main.py). Localhost only.
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8008";

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

export type GateSeverity = "HARD_BLOCK" | "CAUTION" | "CLEAR";

export interface GateBlock {
  source: "cb" | "econ" | "intervention";
  severity: "HARD_BLOCK" | "CAUTION";
  detail: string;
  when: string | null;
}

export interface GatesResponse {
  date: string;
  week: string;
  summary: string;
  severity: GateSeverity;
  instruments: Record<string, GateBlock[]>;
  warnings: string[];
}

export async function getGates(): Promise<GatesResponse> {
  const res = await fetch(`${API_BASE}/gates`, { cache: "no-store" });
  if (!res.ok) throw new Error(`/gates ${res.status}`);
  return res.json();
}

// Worst severity among an instrument's blocks (for the grid dots).
export function worstSeverity(blocks: GateBlock[] | undefined): GateSeverity {
  if (!blocks || blocks.length === 0) return "CLEAR";
  return blocks.some((b) => b.severity === "HARD_BLOCK") ? "HARD_BLOCK" : "CAUTION";
}

export interface Zone {
  zone_id: string;
  label: string;
  direction: string;
  zone_bottom: number | null;
  zone_top: number | null;
  zone_confluence: number | null;
  conviction: string;
  invalidation_level: number | null;
  tp_anchor: number | null;
  status: string;
  daily_verdict: string | null;
  limit_price: number | null;
  entry_confluence: number | null;
  validated_date: string | null;
  source_file: string;
  notes: string | null;
  board_status: string;
  touched: boolean;
  r_result: number | null;
  mfe_r: number | null;
  mae_r: number | null;
}

export interface ZonesResponse {
  week: string;
  count: number;
  instruments: Record<string, Zone[]>;
}

export async function getZones(week?: string): Promise<ZonesResponse> {
  const url = week
    ? `${API_BASE}/zones?week=${encodeURIComponent(week)}`
    : `${API_BASE}/zones`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`/zones ${res.status}`);
  return res.json();
}

export interface ForecastResponse {
  ok: boolean;
  source_file?: string;
  error?: string;
  markdown: string | null;
}

export async function getForecast(sourceFile: string): Promise<ForecastResponse> {
  const res = await fetch(
    `${API_BASE}/forecast?source_file=${encodeURIComponent(sourceFile)}`,
    { cache: "no-store" },
  );
  if (!res.ok) throw new Error(`/forecast ${res.status}`);
  return res.json();
}

export type ChartTf = "D1" | "H4" | "1H" | "15M";

// lightweight-charts time: string 'YYYY-MM-DD' (daily) or UTC epoch seconds (intraday).
export interface Candle {
  time: string | number;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface ZoneBand {
  label: string;
  direction: string;
  bottom: number;
  top: number;
  status: string;
  invalidation: number | null;
  tp_anchor: number | null;
}

export interface TradeLine {
  trade_id: string;
  status: string;
  direction: string;
  entry: number | null;
  sl: number | null;
  tp: number | null;
  tp2: number | null;
  limit_price: number | null;
}

export interface StructureMarker {
  time: string | number;
  type: "BOS" | "CHoCH";
  dir: "up" | "down";
  level: number;
}

export interface ChartResponse {
  ok: boolean;
  error?: string;
  instrument: string;
  tf: ChartTf;
  candles: Candle[];
  overlays?: {
    zones: ZoneBand[];
    trades: TradeLine[];
    structure: StructureMarker[];
    state: string | null;
  };
  as_of?: string | number | null;
  warnings?: string[];
}

export async function getChart(
  instrument: string,
  tf: ChartTf = "D1",
): Promise<ChartResponse> {
  const res = await fetch(
    `${API_BASE}/chart/${encodeURIComponent(instrument)}?tf=${tf}`,
    { cache: "no-store" },
  );
  if (!res.ok) throw new Error(`/chart ${res.status}`);
  return res.json();
}

export interface StatRow {
  n: number;
  wins?: number;
  win_pct?: number;
  total_r?: number;
  avg_r?: number;
  verdict?: string;
}

export type StatGroup = Record<string, StatRow>;

export interface EdgeSummary {
  generated_utc: string;
  min_n: number;
  total_zones: number;
  completed_n: number;
  invalidated_n: number;
  overall: StatRow;
  by_r1: StatGroup;
  by_instrument: StatGroup;
  by_direction: StatGroup;
  by_conviction: StatGroup;
  by_session: StatGroup;
  by_instrument_direction: StatGroup;
}

export interface ScatterPoint {
  instrument: string;
  direction: string;
  conviction: string;
  zone_confluence: number;
  r_result: number;
}

export interface ShadowVsRealRow {
  instrument: string;
  shadow_zones: number;
  real_trades: number;
  real_total_r: number;
}

export interface EdgeResponse {
  ok: boolean;
  min_n: number;
  empty: boolean;
  note?: string;
  summary: Partial<EdgeSummary>;
  scatter: ScatterPoint[];
  shadow_vs_real: {
    by_instrument: ShadowVsRealRow[];
    real_trades_total: number;
    real_total_r: number;
  };
}

export async function getEdge(): Promise<EdgeResponse> {
  const res = await fetch(`${API_BASE}/edge`, { cache: "no-store" });
  if (!res.ok) throw new Error(`/edge ${res.status}`);
  return res.json();
}

export interface MacroSeries {
  series_id: string;
  label: string;
  group: string;
  latest: number | null;
  date: string | null;
  chg_1: number | null;
  chg_5: number | null;
}

export interface MacroResponse {
  series: MacroSeries[];
  as_of: string | null;
}

export async function getMacro(): Promise<MacroResponse> {
  const res = await fetch(`${API_BASE}/macro`, { cache: "no-store" });
  if (!res.ok) throw new Error(`/macro ${res.status}`);
  return res.json();
}

export interface Headline {
  datetime_utc: string;
  headline: string;
  source: string;
  summary: string | null;
  url: string | null;
  category: string | null;
}

export interface NewsResponse {
  ok: boolean;
  instrument?: string;
  days?: number;
  count?: number;
  note?: string;
  error?: string;
  headlines: Headline[];
}

export async function getNews(instrument: string, days = 7): Promise<NewsResponse> {
  const res = await fetch(
    `${API_BASE}/news/${encodeURIComponent(instrument)}?days=${days}`,
    { cache: "no-store" },
  );
  if (!res.ok) throw new Error(`/news ${res.status}`);
  return res.json();
}
