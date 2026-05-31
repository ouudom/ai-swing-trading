import { useEffect, useState } from "react";
import CandleChart, { Candle } from "./CandleChart";

const TFS = ["15m", "1h", "4h", "1d"] as const;
type TF = (typeof TFS)[number];

const LIMITS: Record<TF, number> = { "15m": 500, "1h": 500, "4h": 400, "1d": 300 };
const POLL_MS = 60_000;

export default function App() {
  const [tf, setTf] = useState<TF>("4h");
  const [candles, setCandles] = useState<Candle[]>([]);
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const r = await fetch(`/api/candles?tf=${tf}&limit=${LIMITS[tf]}`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const j = await r.json();
        if (cancelled) return;
        setCandles(j.candles);
        setStatus(`${j.count} bars · ${new Date().toLocaleTimeString()}`);
      } catch (e) {
        if (!cancelled) setStatus(`error: ${(e as Error).message}`);
      }
    };

    load();
    const id = setInterval(load, POLL_MS);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [tf]);

  return (
    <div className="app">
      <div className="toolbar">
        <h1>XAUUSD</h1>
        <div className="tf-group">
          {TFS.map((t) => (
            <button
              key={t}
              className={`tf-btn ${t === tf ? "active" : ""}`}
              onClick={() => setTf(t)}
            >
              {t.toUpperCase()}
            </button>
          ))}
        </div>
        <div className="status">{status}</div>
      </div>
      <div className="chart-wrap">
        <CandleChart candles={candles} />
      </div>
    </div>
  );
}
