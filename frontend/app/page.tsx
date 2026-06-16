"use client";
import {
  getGates,
  getPositions,
  worstSeverity,
  type GateSeverity,
} from "@/lib/api";
import { INSTRUMENTS } from "@/lib/instruments";
import { usePoll } from "@/lib/usePoll";
import ZoneBoard from "@/components/ZoneBoard";
import PriceChart from "@/components/PriceChart";
import EdgePanel from "@/components/EdgePanel";
import MacroPanel from "@/components/MacroPanel";

const SEV_STYLE: Record<GateSeverity, string> = {
  HARD_BLOCK: "border-red-700/60 bg-red-950/40 text-red-300",
  CAUTION: "border-amber-700/50 bg-amber-950/30 text-amber-300",
  CLEAR: "border-emerald-800/50 bg-emerald-950/20 text-emerald-300",
};

const SOURCE_TAG: Record<string, string> = {
  cb: "CB",
  econ: "ECON",
  intervention: "MoF",
};

function rColor(r: number | null): string {
  if (r === null) return "text-neutral-400";
  if (r > 0) return "text-emerald-400";
  if (r < 0) return "text-red-400";
  return "text-neutral-300";
}

function fmt(n: number | null, d = 5): string {
  return n === null || n === undefined ? "—" : n.toFixed(d);
}

function fmtR(n: number | null): string {
  return n === null || n === undefined ? "—" : `${n >= 0 ? "+" : ""}${n.toFixed(2)}R`;
}

export default function Cockpit() {
  const { data, error, updatedAt } = usePoll(getPositions, 60_000);
  const { data: gates, error: gatesError } = usePoll(getGates, 60_000);

  const totalR =
    data?.r_curve && data.r_curve.length
      ? data.r_curve[data.r_curve.length - 1].cum_r
      : 0;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8 font-mono text-sm">
      <header className="mb-6 flex items-baseline justify-between border-b border-neutral-800 pb-3">
        <h1 className="text-lg font-semibold tracking-tight">
          Trading Brain — Cockpit
        </h1>
        <span className="text-xs text-neutral-500">
          {error ? (
            <span className="text-red-400">API: {error}</span>
          ) : updatedAt ? (
            `updated ${updatedAt.toLocaleTimeString()} · polls 60s`
          ) : (
            "loading…"
          )}
        </span>
      </header>

      {/* Gate banner — live /gates */}
      <div
        className={`mb-6 rounded border px-4 py-2 text-xs ${
          gates ? SEV_STYLE[gates.severity] : "border-neutral-800 text-neutral-500"
        }`}
      >
        {gatesError ? (
          <span className="text-red-400">gates: {gatesError}</span>
        ) : gates ? (
          <>
            <div className="font-semibold">
              {gates.severity} · {gates.summary}
            </div>
            {gates.warnings.length > 0 && (
              <ul className="mt-1 list-disc pl-4 text-[10px] text-neutral-400">
                {gates.warnings.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            )}
          </>
        ) : (
          "loading gates…"
        )}
      </div>

      {/* Open positions */}
      <section className="mb-8">
        <h2 className="mb-2 text-xs uppercase tracking-wider text-neutral-500">
          Open positions ({data?.open.length ?? 0})
        </h2>
        {data?.open.length ? (
          <table className="w-full border-collapse text-xs">
            <thead className="text-neutral-500">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-1 pr-3">instrument</th>
                <th className="pr-3">dir</th>
                <th className="pr-3">entry</th>
                <th className="pr-3">SL px</th>
                <th className="pr-3">live R</th>
                <th className="pr-3">MFE/MAE</th>
                <th className="pr-3">SL status</th>
                <th className="pr-3">as of</th>
              </tr>
            </thead>
            <tbody>
              {data.open.map((p) => (
                <tr key={p.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{p.instrument}</td>
                  <td className="pr-3">{p.direction}</td>
                  <td className="pr-3">{fmt(p.entry)}</td>
                  <td className="pr-3">{fmt(p.sl)}</td>
                  <td className={`pr-3 font-semibold ${rColor(p.r_current)}`}>
                    {fmtR(p.r_current)}
                  </td>
                  <td className="pr-3 text-neutral-400">
                    {fmtR(p.mfe_r)} / {fmtR(p.mae_r)}
                  </td>
                  <td
                    className={`pr-3 ${
                      p.sl_status === "HIT" ? "text-red-400" : "text-neutral-400"
                    }`}
                  >
                    {p.sl_status}
                    {p.tp1_touched ? " · TP1✓" : ""}
                    {p.ambiguous ? " ⚠" : ""}
                  </td>
                  <td className="pr-3 text-neutral-600">{p.as_of ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No open positions.</p>
        )}
      </section>

      {/* Pending order limits */}
      <section className="mb-8">
        <h2 className="mb-2 text-xs uppercase tracking-wider text-neutral-500">
          Pending limits ({data?.pending.length ?? 0})
        </h2>
        {data?.pending.length ? (
          <table className="w-full border-collapse text-xs">
            <thead className="text-neutral-500">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-1 pr-3">instrument</th>
                <th className="pr-3">dir</th>
                <th className="pr-3">entry</th>
                <th className="pr-3">spot</th>
                <th className="pr-3">dist-to-fill</th>
                <th className="pr-3">expiry</th>
              </tr>
            </thead>
            <tbody>
              {data.pending.map((p) => (
                <tr key={p.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{p.instrument}</td>
                  <td className="pr-3">{p.direction}</td>
                  <td className="pr-3">{fmt(p.entry)}</td>
                  <td className="pr-3">{fmt(p.spot)}</td>
                  <td className="pr-3 text-amber-300">{fmt(p.distance_to_fill, 6)}</td>
                  <td className="pr-3 text-neutral-600">{p.expiry ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No pending limits.</p>
        )}
      </section>

      {/* Closed trades + cumulative R */}
      <section className="mb-8">
        <h2 className="mb-2 flex items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
          Closed ({data?.closed.length ?? 0})
          <span className={`font-semibold ${rColor(totalR)}`}>
            cum {fmtR(totalR)}
          </span>
        </h2>
        {data?.closed.length ? (
          <table className="w-full border-collapse text-xs">
            <thead className="text-neutral-500">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-1 pr-3">instrument</th>
                <th className="pr-3">dir</th>
                <th className="pr-3">week</th>
                <th className="pr-3">status</th>
                <th className="pr-3">R</th>
                <th className="pr-3">reason</th>
                <th className="pr-3">exit</th>
              </tr>
            </thead>
            <tbody>
              {data.closed.map((c) => (
                <tr key={c.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{c.instrument}</td>
                  <td className="pr-3">{c.direction}</td>
                  <td className="pr-3 text-neutral-500">{c.week}</td>
                  <td className="pr-3">{c.status}</td>
                  <td className={`pr-3 font-semibold ${rColor(c.r_actual)}`}>
                    {fmtR(c.r_actual)}
                  </td>
                  <td className="pr-3 text-neutral-500">{c.exit_reason ?? "—"}</td>
                  <td className="pr-3 text-neutral-600">{c.exit_time ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No closed trades.</p>
        )}
      </section>

      {/* 10-instrument shell — zone board lands here in Phase 2 */}
      <section>
        <h2 className="mb-2 text-xs uppercase tracking-wider text-neutral-500">
          Instruments
        </h2>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
          {INSTRUMENTS.map((inst) => {
            const hasOpen = data?.open.some((p) => p.instrument === inst);
            const hasPending = data?.pending.some((p) => p.instrument === inst);
            const blocks = gates?.instruments[inst];
            const sev = worstSeverity(blocks);
            const dot =
              sev === "HARD_BLOCK"
                ? "text-red-500"
                : sev === "CAUTION"
                  ? "text-amber-400"
                  : "text-emerald-600";
            const sources = blocks
              ? [...new Set(blocks.map((b) => SOURCE_TAG[b.source] ?? b.source))]
              : [];
            return (
              <div
                key={inst}
                className="rounded border border-neutral-800 bg-neutral-950/50 px-3 py-2"
              >
                <div className="flex items-center justify-between">
                  <span className="uppercase">
                    <span className={`mr-1 ${dot}`}>●</span>
                    {inst}
                  </span>
                  <span className="text-xs">
                    {hasOpen ? (
                      <span className="text-emerald-400">open</span>
                    ) : hasPending ? (
                      <span className="text-amber-400">pending</span>
                    ) : (
                      <span className="text-neutral-700">flat</span>
                    )}
                  </span>
                </div>
                <div className="mt-1 text-[10px] text-neutral-600">
                  {sources.length ? (
                    <span title={blocks?.map((b) => b.detail).join("\n")}>
                      {sev} · {sources.join(" ")}
                    </span>
                  ) : (
                    "clear"
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Chart — Phase 3 */}
      <div className="mt-8">
        <PriceChart />
      </div>

      {/* Zone board — Phase 2 */}
      <div className="mt-8">
        <ZoneBoard />
      </div>

      {/* Calibration / edge — Phase 4 */}
      <div className="mt-8">
        <EdgePanel />
      </div>

      {/* Macro / news — Phase 5 */}
      <div className="mt-8">
        <MacroPanel />
      </div>
    </main>
  );
}
