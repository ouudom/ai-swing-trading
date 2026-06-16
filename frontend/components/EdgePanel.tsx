"use client";
import { getEdge, type ScatterPoint, type StatGroup, type StatRow } from "@/lib/api";
import { usePoll } from "@/lib/usePoll";

function verdictStyle(v: string | undefined): string {
  if (!v) return "text-neutral-500";
  if (v === "WORKING") return "text-emerald-400";
  if (v === "DEAD") return "text-red-400";
  return "text-neutral-500"; // INSUFFICIENT / no data
}

function rStyle(r: number | undefined): string {
  if (r === undefined) return "text-neutral-500";
  return r > 0 ? "text-emerald-400" : r < 0 ? "text-red-400" : "text-neutral-400";
}

function StatTable({ title, group }: { title: string; group: StatGroup | undefined }) {
  const keys = group ? Object.keys(group) : [];
  return (
    <div>
      <h3 className="mb-1 text-[11px] uppercase tracking-wider text-neutral-500">{title}</h3>
      <table className="w-full border-collapse text-[11px]">
        <thead className="text-neutral-600">
          <tr className="border-b border-neutral-800 text-left">
            <th className="py-0.5 pr-2">slice</th>
            <th className="pr-2">n</th>
            <th className="pr-2">win%</th>
            <th className="pr-2">tot R</th>
            <th className="pr-2">avg R</th>
            <th>verdict</th>
          </tr>
        </thead>
        <tbody>
          {keys.length === 0 ? (
            <tr>
              <td colSpan={6} className="py-1 text-neutral-700">
                no completed trades
              </td>
            </tr>
          ) : (
            keys.map((k) => {
              const s: StatRow = group![k];
              return (
                <tr key={k} className="border-b border-neutral-900">
                  <td className="py-0.5 pr-2 text-neutral-300">{k}</td>
                  <td className="pr-2">{s.n}</td>
                  <td className="pr-2">{s.win_pct !== undefined ? `${(s.win_pct * 100).toFixed(0)}%` : "—"}</td>
                  <td className={`pr-2 ${rStyle(s.total_r)}`}>
                    {s.total_r !== undefined ? `${s.total_r >= 0 ? "+" : ""}${s.total_r.toFixed(1)}` : "—"}
                  </td>
                  <td className={`pr-2 ${rStyle(s.avg_r)}`}>
                    {s.avg_r !== undefined ? `${s.avg_r >= 0 ? "+" : ""}${s.avg_r.toFixed(2)}` : "—"}
                  </td>
                  <td className={verdictStyle(s.verdict)}>{s.verdict ?? "—"}</td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

function Scatter({ pts }: { pts: ScatterPoint[] }) {
  const W = 460;
  const H = 200;
  const P = 28;
  // x = zone_confluence (floor 5 → 10), y = r_result (clamp -2..+4)
  const xMin = 5;
  const xMax = 10;
  const yMin = -2;
  const yMax = 4;
  const sx = (x: number) => P + ((x - xMin) / (xMax - xMin)) * (W - 2 * P);
  const sy = (y: number) => H - P - ((Math.min(yMax, Math.max(yMin, y)) - yMin) / (yMax - yMin)) * (H - 2 * P);
  const yZero = sy(0);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="confluence vs R scatter">
      <line x1={P} y1={H - P} x2={W - P} y2={H - P} stroke="#303030" />
      <line x1={P} y1={P} x2={P} y2={H - P} stroke="#303030" />
      <line x1={P} y1={yZero} x2={W - P} y2={yZero} stroke="#525252" strokeDasharray="3 3" />
      <text x={P} y={H - 8} fill="#737373" fontSize="9">R1 5</text>
      <text x={W - P - 14} y={H - 8} fill="#737373" fontSize="9">10</text>
      <text x={4} y={sy(yMax) + 4} fill="#737373" fontSize="9">+{yMax}R</text>
      <text x={4} y={yZero + 3} fill="#737373" fontSize="9">0</text>
      <text x={4} y={sy(yMin)} fill="#737373" fontSize="9">{yMin}R</text>
      {pts.map((p, i) => (
        <circle
          key={i}
          cx={sx(p.zone_confluence)}
          cy={sy(p.r_result)}
          r={3.5}
          fill={p.r_result > 0 ? "#10b981" : p.r_result < 0 ? "#ef4444" : "#a3a3a3"}
          opacity={0.8}
        >
          <title>{`${p.instrument} ${p.direction} · R1 ${p.zone_confluence} → ${p.r_result >= 0 ? "+" : ""}${p.r_result}R`}</title>
        </circle>
      ))}
    </svg>
  );
}

export default function EdgePanel() {
  const { data, error, updatedAt } = usePoll(getEdge, 60_000);
  const s = data?.summary;

  return (
    <section>
      <h2 className="mb-2 flex flex-wrap items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
        Calibration / edge
        <span className="text-neutral-600">
          {s
            ? `${s.completed_n ?? 0} completed · ${s.total_zones ?? 0} zones · min-n ${data?.min_n}`
            : ""}
          {error ? <span className="text-red-400"> · {error}</span> : ""}
          {updatedAt ? ` · ${updatedAt.toLocaleTimeString()}` : ""}
        </span>
      </h2>

      {data?.empty && (
        <p className="mb-3 text-[11px] text-amber-400/80">
          {data.note ?? "few completed shadow trades — verdicts INSUFFICIENT until n grows."}
        </p>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <StatTable title="overall" group={s ? { overall: s.overall! } : undefined} />
          <StatTable title="by instrument" group={s?.by_instrument} />
          <StatTable title="by direction" group={s?.by_direction} />
          <StatTable title="by R1 bucket" group={s?.by_r1} />
        </div>
        <div className="space-y-4">
          <StatTable title="by conviction" group={s?.by_conviction} />
          <StatTable title="by session" group={s?.by_session} />
          <StatTable title="by instrument × direction" group={s?.by_instrument_direction} />
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div>
          <h3 className="mb-1 text-[11px] uppercase tracking-wider text-neutral-500">
            Confluence → R (does score predict outcome?)
          </h3>
          {data && data.scatter.length ? (
            <Scatter pts={data.scatter} />
          ) : (
            <p className="text-[11px] text-neutral-700">no completed shadow trades yet</p>
          )}
        </div>
        <div>
          <h3 className="mb-1 text-[11px] uppercase tracking-wider text-neutral-500">
            Shadow vs real
            {data && (
              <span className={`ml-2 ${rStyle(data.shadow_vs_real.real_total_r)}`}>
                real {data.shadow_vs_real.real_trades_total} trades ·{" "}
                {data.shadow_vs_real.real_total_r >= 0 ? "+" : ""}
                {data.shadow_vs_real.real_total_r.toFixed(1)}R
              </span>
            )}
          </h3>
          <table className="w-full border-collapse text-[11px]">
            <thead className="text-neutral-600">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-0.5 pr-2">instrument</th>
                <th className="pr-2">shadow zones</th>
                <th className="pr-2">real trades</th>
                <th>real R</th>
              </tr>
            </thead>
            <tbody>
              {data?.shadow_vs_real.by_instrument.map((r) => (
                <tr key={r.instrument} className="border-b border-neutral-900">
                  <td className="py-0.5 pr-2 uppercase text-neutral-300">{r.instrument}</td>
                  <td className="pr-2">{r.shadow_zones}</td>
                  <td className="pr-2">{r.real_trades}</td>
                  <td className={rStyle(r.real_total_r)}>
                    {r.real_trades ? `${r.real_total_r >= 0 ? "+" : ""}${r.real_total_r.toFixed(1)}` : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
