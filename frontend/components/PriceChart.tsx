"use client";
import {
  getChart,
  type ChartResponse,
  type ChartTf,
} from "@/lib/api";
import { INSTRUMENTS, pricePrecision } from "@/lib/instruments";
import {
  CandlestickSeries,
  createChart,
  createSeriesMarkers,
  LineStyle,
  type IChartApi,
  type ISeriesApi,
  type ISeriesMarkersPluginApi,
  type IPriceLine,
  type Time,
} from "lightweight-charts";
import { useEffect, useRef, useState } from "react";

const TFS: ChartTf[] = ["D1", "H4", "1H"];

const CHART_OPTS = {
  layout: {
    background: { color: "transparent" },
    textColor: "#a3a3a3",
    fontFamily: "monospace",
  },
  grid: {
    vertLines: { color: "#1a1a1a" },
    horzLines: { color: "#1a1a1a" },
  },
  rightPriceScale: { borderColor: "#303030" },
  timeScale: { borderColor: "#303030", timeVisible: true, secondsVisible: false },
  crosshair: { mode: 0 as const },
};

export default function PriceChart() {
  const wrapRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const markersRef = useRef<ISeriesMarkersPluginApi<Time> | null>(null);
  const priceLinesRef = useRef<IPriceLine[]>([]);

  const [instrument, setInstrument] = useState<string>("xauusd");
  const [tf, setTf] = useState<ChartTf>("D1");
  const [meta, setMeta] = useState<ChartResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // create chart once
  useEffect(() => {
    if (!wrapRef.current) return;
    const chart = createChart(wrapRef.current, {
      ...CHART_OPTS,
      width: wrapRef.current.clientWidth,
      height: 420,
    });
    const series = chart.addSeries(CandlestickSeries, {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });
    chartRef.current = chart;
    seriesRef.current = series;
    markersRef.current = createSeriesMarkers(series, []);

    const onResize = () => {
      if (wrapRef.current) chart.applyOptions({ width: wrapRef.current.clientWidth });
    };
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
      markersRef.current = null;
      priceLinesRef.current = [];
    };
  }, []);

  // load + render data on instrument/tf change
  useEffect(() => {
    let alive = true;
    getChart(instrument, tf)
      .then((d) => {
        if (!alive) return;
        const series = seriesRef.current;
        if (!series) return;
        if (!d.ok) {
          setError(d.error ?? "load failed");
          return;
        }
        setError(null);
        setMeta(d);

        // Per-instrument price precision — without the right minMove, lightweight-charts
        // cannot scale sub-cent FX ranges and keeps a stale (e.g. gold) price scale.
        const { precision, minMove } = pricePrecision(instrument);
        series.applyOptions({
          priceFormat: { type: "price", precision, minMove },
        });

        series.setData(d.candles as { time: Time; open: number; high: number; low: number; close: number }[]);

        // Force the price scale back to autoscale on the new data (a prior instrument
        // with a wildly different range can otherwise leave the scale pinned).
        chartRef.current?.priceScale("right").applyOptions({ autoScale: true });

        // clear old price lines
        priceLinesRef.current.forEach((pl) => series.removePriceLine(pl));
        priceLinesRef.current = [];

        const addLine = (price: number | null | undefined, color: string, title: string, style = LineStyle.Solid) => {
          if (price === null || price === undefined) return;
          priceLinesRef.current.push(
            series.createPriceLine({ price, color, lineWidth: 1, lineStyle: style, axisLabelVisible: true, title }),
          );
        };

        // zone bands → top/bottom lines (color by direction)
        d.overlays?.zones.forEach((z) => {
          const c = z.direction === "LONG" ? "#34d399" : "#f87171";
          addLine(z.top, c, `${z.label} top`, LineStyle.Dashed);
          addLine(z.bottom, c, `${z.label} bot`, LineStyle.Dashed);
          addLine(z.invalidation, "#737373", `${z.label} inval`, LineStyle.Dotted);
        });

        // trade lines
        d.overlays?.trades.forEach((t) => {
          addLine(t.entry ?? t.limit_price, "#60a5fa", `${t.trade_id} entry`);
          addLine(t.sl, "#ef4444", "SL");
          addLine(t.tp, "#10b981", "TP1");
          addLine(t.tp2, "#059669", "TP2");
        });

        // BOS/CHoCH markers
        const markers = (d.overlays?.structure ?? []).map((m) => ({
          time: m.time as Time,
          position: (m.dir === "up" ? "belowBar" : "aboveBar") as "belowBar" | "aboveBar",
          color: m.type === "CHoCH" ? "#f59e0b" : "#737373",
          shape: (m.dir === "up" ? "arrowUp" : "arrowDown") as "arrowUp" | "arrowDown",
          text: m.type,
        }));
        markersRef.current?.setMarkers(markers);

        chartRef.current?.timeScale().fitContent();
      })
      .catch((e) => alive && setError(String(e)));
    return () => {
      alive = false;
    };
  }, [instrument, tf]);

  return (
    <section>
      <h2 className="mb-2 flex flex-wrap items-baseline gap-3 text-xs uppercase tracking-wider text-neutral-500">
        Chart
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
        <span className="flex gap-1">
          {TFS.map((t) => (
            <button
              key={t}
              onClick={() => setTf(t)}
              className={`rounded px-2 py-0.5 text-xs ${
                tf === t
                  ? "bg-neutral-200 text-neutral-900"
                  : "border border-neutral-700 text-neutral-400 hover:bg-neutral-800"
              }`}
            >
              {t}
            </button>
          ))}
        </span>
        {meta?.overlays?.state && (
          <span className="text-neutral-600">structure: {meta.overlays.state}</span>
        )}
        {error && <span className="text-red-400">{error}</span>}
      </h2>
      <div
        ref={wrapRef}
        className="rounded border border-neutral-800 bg-neutral-950/50 p-1"
      />
      <p className="mt-1 text-[10px] text-neutral-600">
        dashed = zone bands · blue = entry/limit · red = SL · green = TP · arrows = BOS (grey) /
        CHoCH (amber). Bars only as fresh as last pipeline run.
      </p>
    </section>
  );
}
