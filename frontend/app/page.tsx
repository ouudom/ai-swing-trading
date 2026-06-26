"use client";
import { useState } from "react";
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

const TABS = [
  "Positions",
  "Instruments",
  "Chart",
  "Zones",
  "Edge",
  "Macro",
] as const;
type Tab = (typeof TABS)[number];

export default function Cockpit() {
  const { data, error, updatedAt } = usePoll(getPositions, 60_000);
  const { data: gates, error: gatesError } = usePoll(getGates, 60_000);
  const [tab, setTab] = useState<Tab>("Positions");

  const totalR =
    data?.r_curve && data.r_curve.length
      ? data.r_curve[data.r_curve.length - 1].cum_r
      : 0;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8 font-mono text-sm">
      <header className="mb-6 flex items-baseline justify-between border-b border-neutral-800 pb-3">
        <h1 className="text-lg font-semibold tracking-tight">
          Claude Swing — Cockpit
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

      {/* Tab bar */}
      <nav className="mb-6 flex gap-1 border-b border-neutral-800 text-xs">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`-mb-px border-b-2 px-3 py-2 uppercase tracking-wider transition-colors ${
              tab === t
                ? "border-neutral-300 text-neutral-100"
                : "border-transparent text-neutral-500 hover:text-neutral-300"
            }`}
          >
            {t}
          </button>
        ))}
      </nav>

      {/* ── Positions tab ── */}
      <div className={tab === "Positions" ? "" : "hidden"}>

      {/* System P&L banner — this is the trade_outcome REPLAY, not a real-money book */}
      <div className="mb-4 rounded border border-neutral-800 px-4 py-2 text-[11px] text-neutral-500">
        Entry-mechanics <span className="text-neutral-300">replay</span> (trade_outcome): E0 +
        offset + EC applied to every published zone. No hand-logged trades — this is the system&apos;s
        own would-be P&amp;L.
      </div>

      {/* Filled (replay) + cumulative R */}
      <section className="mb-8">
        <h2 className="mb-2 flex items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
          Replay fills ({data?.filled.length ?? 0})
          <span className={`font-semibold ${rColor(totalR)}`}>cum {fmtR(totalR)}</span>
        </h2>
        {data?.filled.length ? (
          <table className="w-full border-collapse text-xs">
            <thead className="text-neutral-500">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-1 pr-3">instrument</th>
                <th className="pr-3">dir</th>
                <th className="pr-3">EC</th>
                <th className="pr-3">entry</th>
                <th className="pr-3">status</th>
                <th className="pr-3">R</th>
                <th className="pr-3">MFE/MAE</th>
                <th className="pr-3">gate</th>
                <th className="pr-3">verdict</th>
              </tr>
            </thead>
            <tbody>
              {data.filled.map((c) => (
                <tr key={c.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{c.instrument}</td>
                  <td className="pr-3">{c.direction}</td>
                  <td className="pr-3 text-neutral-400">{fmt(c.ec_score, 1)}</td>
                  <td className="pr-3">{fmt(c.entry)}</td>
                  <td className="pr-3">{c.status}</td>
                  <td className={`pr-3 font-semibold ${rColor(c.r_result)}`}>
                    {fmtR(c.r_result)}
                  </td>
                  <td className="pr-3 text-neutral-400">
                    {fmtR(c.mfe_r)} / {fmtR(c.mae_r)}
                  </td>
                  <td className="pr-3 text-amber-300">{c.block_flags || "—"}</td>
                  <td
                    className={`pr-3 ${
                      c.block_verdict === "COSTLY_REFUSED" ? "text-red-400" : "text-neutral-500"
                    }`}
                  >
                    {c.block_verdict ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No replayed fills.</p>
        )}
      </section>

      {/* Pending (live week, limit not yet reached) */}
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
                <th className="pr-3">EC</th>
                <th className="pr-3">anchor</th>
                <th className="pr-3">limit</th>
                <th className="pr-3">E0</th>
              </tr>
            </thead>
            <tbody>
              {data.pending.map((p) => (
                <tr key={p.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{p.instrument}</td>
                  <td className="pr-3">{p.direction}</td>
                  <td className="pr-3 text-neutral-400">{fmt(p.ec_score, 1)}</td>
                  <td className="pr-3">{fmt(p.anchor)}</td>
                  <td className="pr-3 text-amber-300">{fmt(p.limit_px)}</td>
                  <td className="pr-3 text-neutral-500">{p.e0_present ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No pending limits.</p>
        )}
      </section>

      {/* Missed (offset limit never reached = D030 over-wide-offset signal) */}
      <section className="mb-8">
        <h2 className="mb-2 text-xs uppercase tracking-wider text-neutral-500">
          Missed fills · offset never reached ({data?.missed.length ?? 0})
        </h2>
        {data?.missed.length ? (
          <table className="w-full border-collapse text-xs">
            <thead className="text-neutral-500">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-1 pr-3">instrument</th>
                <th className="pr-3">dir</th>
                <th className="pr-3">EC</th>
                <th className="pr-3">anchor</th>
                <th className="pr-3">limit (unreached)</th>
              </tr>
            </thead>
            <tbody>
              {data.missed.map((p) => (
                <tr key={p.trade_id} className="border-b border-neutral-900">
                  <td className="py-1 pr-3 uppercase">{p.instrument}</td>
                  <td className="pr-3">{p.direction}</td>
                  <td className="pr-3 text-neutral-400">{fmt(p.ec_score, 1)}</td>
                  <td className="pr-3">{fmt(p.anchor)}</td>
                  <td className="pr-3 text-neutral-500">{fmt(p.limit_px)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-neutral-600">No missed fills.</p>
        )}
      </section>

      </div>

      {/* ── Instruments tab ── */}
      <div className={tab === "Instruments" ? "" : "hidden"}>

      {/* 10-instrument shell — zone board lands here in Phase 2 */}
      <section>
        <h2 className="mb-2 text-xs uppercase tracking-wider text-neutral-500">
          Instruments
        </h2>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
          {INSTRUMENTS.map((inst) => {
            const hasFilled = data?.filled.some((p) => p.instrument === inst);
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
                    {hasFilled ? (
                      <span className="text-emerald-400">filled</span>
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

      </div>

      {/* ── Chart tab ── */}
      <div className={tab === "Chart" ? "" : "hidden"}>
        <PriceChart />
      </div>

      {/* ── Zones tab ── */}
      <div className={tab === "Zones" ? "" : "hidden"}>
        <ZoneBoard />
      </div>

      {/* ── Edge tab ── */}
      <div className={tab === "Edge" ? "" : "hidden"}>
        <EdgePanel />
      </div>

      {/* ── Macro tab ── */}
      <div className={tab === "Macro" ? "" : "hidden"}>
        <MacroPanel />
      </div>
    </main>
  );
}
