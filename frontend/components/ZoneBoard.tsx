"use client";
import { getForecast, getZones, type Zone } from "@/lib/api";
import { INSTRUMENTS } from "@/lib/instruments";
import { usePoll } from "@/lib/usePoll";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

function statusStyle(s: string): string {
  if (s.startsWith("WIN")) return "bg-emerald-900/50 text-emerald-300";
  if (s.startsWith("LOSS")) return "bg-red-900/50 text-red-300";
  if (s === "ARMED") return "bg-sky-900/50 text-sky-300";
  if (s === "INVALIDATED" || s === "NO_TRADE") return "bg-neutral-800 text-neutral-500 line-through";
  if (s === "TOUCHED") return "bg-amber-900/40 text-amber-300";
  return "bg-neutral-800 text-neutral-400"; // PENDING / FLAT / RESOLVED
}

function dirStyle(dir: string): string {
  return dir === "LONG" ? "text-emerald-400" : dir === "SHORT" ? "text-red-400" : "text-neutral-400";
}

function fmtBand(z: Zone): string {
  if (z.zone_bottom === null || z.zone_top === null) return "—";
  const d = z.zone_bottom < 10 ? 4 : 1;
  return `${z.zone_bottom.toFixed(d)}–${z.zone_top.toFixed(d)}`;
}

function ZoneRow({ z, onOpen }: { z: Zone; onOpen: (z: Zone) => void }) {
  return (
    <button
      onClick={() => onOpen(z)}
      className="flex w-full items-center gap-2 rounded px-2 py-1 text-left text-[11px] hover:bg-neutral-800/60"
      title={z.notes ?? z.source_file}
    >
      <span className="w-16 shrink-0 text-neutral-500">{z.label}</span>
      <span className={`w-12 shrink-0 ${dirStyle(z.direction)}`}>{z.direction}</span>
      <span className="w-28 shrink-0 tabular-nums">{fmtBand(z)}</span>
      <span className="w-16 shrink-0 text-neutral-400">
        R1 {z.zone_confluence?.toFixed(1) ?? "—"}
      </span>
      <span className="w-16 shrink-0 text-neutral-500">{z.conviction}</span>
      <span className={`ml-auto rounded px-1.5 py-0.5 ${statusStyle(z.board_status)}`}>
        {z.board_status}
      </span>
    </button>
  );
}

function ForecastModal({ zone, onClose }: { zone: Zone; onClose: () => void }) {
  const [md, setMd] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    getForecast(zone.source_file)
      .then((r) => {
        if (!alive) return;
        if (r.ok) setMd(r.markdown);
        else setErr(r.error ?? "load failed");
      })
      .catch((e) => alive && setErr(String(e)));
    return () => {
      alive = false;
    };
  }, [zone.source_file]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/70 p-6"
      onClick={onClose}
    >
      <div
        className="my-8 w-full max-w-3xl rounded-lg border border-neutral-700 bg-neutral-950 p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-3 flex items-baseline justify-between border-b border-neutral-800 pb-2">
          <h3 className="font-mono text-sm">
            {zone.zone_id}{" "}
            <span className="text-neutral-500">· {zone.source_file}</span>
          </h3>
          <button onClick={onClose} className="text-neutral-400 hover:text-neutral-200">
            ✕ close
          </button>
        </div>
        {err ? (
          <p className="font-mono text-xs text-red-400">{err}</p>
        ) : md === null ? (
          <p className="font-mono text-xs text-neutral-500">loading forecast…</p>
        ) : (
          <article className="prose-trading max-w-none text-sm leading-relaxed">
            <Markdown remarkPlugins={[remarkGfm]}>{md}</Markdown>
          </article>
        )}
      </div>
    </div>
  );
}

export default function ZoneBoard() {
  const { data, error, updatedAt } = usePoll(getZones, 60_000);
  const [open, setOpen] = useState<Zone | null>(null);

  return (
    <section>
      <h2 className="mb-2 flex items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
        Zone board
        <span className="text-neutral-600">
          {data ? `${data.week} · ${data.count} zones` : ""}
          {error ? <span className="text-red-400"> · {error}</span> : ""}
          {updatedAt ? ` · ${updatedAt.toLocaleTimeString()}` : ""}
        </span>
      </h2>
      <div className="grid grid-cols-1 gap-2 lg:grid-cols-2">
        {INSTRUMENTS.map((inst) => {
          const zones = data?.instruments[inst] ?? [];
          return (
            <div
              key={inst}
              className="rounded border border-neutral-800 bg-neutral-950/50 px-3 py-2"
            >
              <div className="mb-1 text-xs uppercase text-neutral-300">{inst}</div>
              {zones.length ? (
                zones.map((z) => <ZoneRow key={z.zone_id} z={z} onOpen={setOpen} />)
              ) : (
                <div className="px-2 py-1 text-[11px] text-neutral-700">
                  no zones this week
                </div>
              )}
            </div>
          );
        })}
      </div>
      {open && <ForecastModal zone={open} onClose={() => setOpen(null)} />}
    </section>
  );
}
