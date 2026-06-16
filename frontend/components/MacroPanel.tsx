"use client";
import { getMacro, getNews, type Headline, type MacroSeries } from "@/lib/api";
import { INSTRUMENTS } from "@/lib/instruments";
import { usePoll } from "@/lib/usePoll";
import { useEffect, useState } from "react";

function chgStyle(v: number | null): string {
  if (v === null) return "text-neutral-600";
  return v > 0 ? "text-emerald-400" : v < 0 ? "text-red-400" : "text-neutral-400";
}

function fmtChg(v: number | null): string {
  if (v === null) return "—";
  return `${v >= 0 ? "+" : ""}${v.toFixed(2)}`;
}

function MacroRow({ s }: { s: MacroSeries }) {
  return (
    <tr className="border-b border-neutral-900">
      <td className="py-0.5 pr-2 text-neutral-300">{s.label}</td>
      <td className="pr-2 text-right tabular-nums text-neutral-200">
        {s.latest !== null ? s.latest : "—"}
      </td>
      <td className={`pr-2 text-right tabular-nums ${chgStyle(s.chg_1)}`}>{fmtChg(s.chg_1)}</td>
      <td className={`text-right tabular-nums ${chgStyle(s.chg_5)}`}>{fmtChg(s.chg_5)}</td>
    </tr>
  );
}

function NewsItem({ h }: { h: Headline }) {
  const title = (
    <span className="text-neutral-200">{h.headline}</span>
  );
  return (
    <li className="border-b border-neutral-900 py-1">
      <div className="flex items-baseline gap-2 text-[11px]">
        <span className="shrink-0 text-neutral-600">{h.datetime_utc.slice(5, 16).replace("T", " ")}</span>
        <span className="shrink-0 text-neutral-500">[{h.source}]</span>
        {h.url ? (
          <a href={h.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
            {title}
          </a>
        ) : (
          title
        )}
      </div>
      {h.summary && <p className="mt-0.5 pl-1 text-[10px] text-neutral-500">{h.summary}</p>}
    </li>
  );
}

export default function MacroPanel() {
  const { data: macro, error: macroErr } = usePoll(getMacro, 60_000);
  const [instrument, setInstrument] = useState<string>("xauusd");
  const [news, setNews] = useState<Headline[] | null>(null);
  const [newsNote, setNewsNote] = useState<string | null>(null);
  const [newsErr, setNewsErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    const load = () =>
      getNews(instrument)
        .then((d) => {
          if (!alive) return;
          setNews(d.headlines);
          setNewsNote(d.note ?? null);
          setNewsErr(null);
        })
        .catch((e) => alive && setNewsErr(String(e)));
    load();
    const id = setInterval(load, 60_000);
    return () => {
      alive = false;
      clearInterval(id);
    };
  }, [instrument]);

  return (
    <section>
      <h2 className="mb-2 flex flex-wrap items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
        Macro / news
        <span className="text-neutral-600">
          {macro?.as_of ? `as of ${macro.as_of}` : ""}
          {macroErr ? <span className="text-red-400"> · {macroErr}</span> : ""}
        </span>
      </h2>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* macro snapshot */}
        <div>
          <table className="w-full border-collapse text-[11px]">
            <thead className="text-neutral-600">
              <tr className="border-b border-neutral-800 text-left">
                <th className="py-0.5 pr-2">series</th>
                <th className="pr-2 text-right">latest</th>
                <th className="pr-2 text-right">Δ1</th>
                <th className="text-right">Δ5</th>
              </tr>
            </thead>
            <tbody>
              {macro?.series.map((s) => <MacroRow key={s.series_id} s={s} />) ?? (
                <tr>
                  <td colSpan={4} className="py-1 text-neutral-700">
                    loading…
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          <p className="mt-1 text-[10px] text-neutral-600">
            Δ1 = vs prior obs · Δ5 = vs 5 obs ago (macro drift vs week-ago baseline).
          </p>
        </div>

        {/* pair-filtered news */}
        <div>
          <div className="mb-1 flex items-center gap-2">
            <select
              value={instrument}
              onChange={(e) => setInstrument(e.target.value)}
              className="rounded border border-neutral-700 bg-neutral-900 px-2 py-0.5 text-xs uppercase text-neutral-200"
            >
              {INSTRUMENTS.map((i) => (
                <option key={i} value={i}>
                  {i}
                </option>
              ))}
            </select>
            {newsErr && <span className="text-[11px] text-red-400">{newsErr}</span>}
          </div>
          {newsNote ? (
            <p className="text-[11px] text-amber-400/80">{newsNote}</p>
          ) : news && news.length ? (
            <ul className="max-h-72 overflow-y-auto">
              {news.map((h, i) => (
                <NewsItem key={`${h.datetime_utc}-${i}`} h={h} />
              ))}
            </ul>
          ) : (
            <p className="text-[11px] text-neutral-700">no matching headlines</p>
          )}
        </div>
      </div>
    </section>
  );
}
