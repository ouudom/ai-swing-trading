"""Interactive CLI: prompt config, pick strategies, run, report, optional save."""
from datetime import datetime
from pathlib import Path
import pandas as pd
from .engine import Config, metrics
from .data import load, BPY
from .strategies import REGISTRY

REPORT_DIR = Path(__file__).resolve().parent / "reports"


def _df_to_md(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |",
             "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def _ask(prompt, default, cast=float):
    raw = input(f"  {prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return cast(raw)
    except ValueError:
        print(f"  ! invalid, using {default}")
        return default


def prompt_config() -> Config:
    print("\n=== Backtest Configuration ===")
    initial = _ask("Initial balance ($)", 100_000.0)
    risk_pct = _ask("Risk per trade (% of equity)", 1.0) / 100
    rr = _ask("Reward:Risk target (R)", 2.5)
    be_r = _ask("Move stop to BE at +R (0=disable)", 1.5)
    cost = _ask("Cost per oz per side ($)", 0.50)
    return Config(initial=initial, risk_pct=risk_pct, rr=rr, be_r=be_r, cost=cost)


def prompt_strategies():
    print("\n=== Strategies ===")
    for i, (name, _, tfs) in enumerate(REGISTRY, 1):
        print(f"  [{i:2d}] {name:<28s} ({'+'.join(tfs)})")
    print(f"  [ 0] ALL")
    raw = input("Select (comma-separated, e.g. 1,3,5 or 0 for all): ").strip()
    if not raw or raw == "0":
        return list(range(len(REGISTRY)))
    picks = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok: continue
        try:
            idx = int(tok) - 1
            if 0 <= idx < len(REGISTRY): picks.append(idx)
        except ValueError:
            pass
    return picks or list(range(len(REGISTRY)))


def required_tfs(picks):
    needed = set()
    for i in picks:
        needed.update(REGISTRY[i][2])
    return sorted(needed)


def render_report(results, cfg, picks):
    rows = []
    for r, idx in zip(results, picks):
        tfs = REGISTRY[idx][2]
        bpy = BPY[tfs[0]]
        rows.append(metrics(r.name, r.equity, r.trades, bpy=bpy))
    df = pd.DataFrame(rows)
    print("\n" + "=" * 88)
    print(f"  BACKTEST REPORT  ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"  initial=${cfg.initial:,.0f}  risk={cfg.risk_pct*100:.1f}%  RR={cfg.rr}  BE@={cfg.be_r}R  cost=${cfg.cost}/oz")
    print("=" * 88)
    print(df.to_string(index=False))
    print("=" * 88)
    return df


def save_outputs(results, summary_df, cfg, picks):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = REPORT_DIR / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    csv_path = run_dir / "trades.csv"
    md_path = run_dir / "summary.md"

    trade_rows = []
    for r in results:
        for t in r.trades:
            trade_rows.append({
                "strategy": r.name,
                "entry_time": t.entry_time,
                "exit_time": t.exit_time,
                "direction": "LONG" if t.direction > 0 else "SHORT",
                "entry": round(t.entry, 2),
                "exit": round(t.exit, 2),
                "size": round(t.size, 4),
                "risk_dist": round(t.risk_dist, 2),
                "pnl": round(t.pnl, 2),
                "r_mult": round(t.r_mult, 2),
                "reason": t.reason,
            })
    if trade_rows:
        pd.DataFrame(trade_rows).to_csv(csv_path, index=False)
    else:
        csv_path.write_text("(no trades)\n")

    md = []
    md.append("---")
    md.append("type: backtest_report")
    md.append(f"generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md.append(f"initial: {cfg.initial}")
    md.append(f"risk_pct: {cfg.risk_pct}")
    md.append(f"rr: {cfg.rr}")
    md.append(f"be_r: {cfg.be_r}")
    md.append(f"cost: {cfg.cost}")
    md.append(f"strategies: {len(picks)}")
    md.append("---\n")
    md.append(f"# Backtest Summary — {stamp}\n")
    md.append("## Config")
    md.append(f"- Initial balance: ${cfg.initial:,.0f}")
    md.append(f"- Risk per trade: {cfg.risk_pct*100:.2f}%")
    md.append(f"- Reward:Risk: {cfg.rr}R")
    md.append(f"- BE move at: +{cfg.be_r}R")
    md.append(f"- Cost: ${cfg.cost}/oz/side\n")
    md.append("## Results\n")
    md.append(_df_to_md(summary_df))
    md.append("\n## Trade log")
    md.append(f"- CSV: `trades.csv` ({len(trade_rows)} trades)\n")
    md_path.write_text("\n".join(md))

    print(f"\nSaved:")
    print(f"  trades:  {csv_path}")
    print(f"  summary: {md_path}")


def run():
    cfg = prompt_config()
    picks = prompt_strategies()
    tfs = required_tfs(picks)
    print(f"\nLoading data: {', '.join(tfs)}...")
    data = {tf: load(tf) for tf in tfs}
    for tf in tfs:
        print(f"  {tf}: {len(data[tf])} bars  {data[tf].index[0].date()} → {data[tf].index[-1].date()}")

    results = []
    print()
    for idx in picks:
        name, fn, _ = REGISTRY[idx]
        print(f"  running: {name}...")
        results.append(fn(cfg, data))

    summary = render_report(results, cfg, picks)
    ans = input("\nSave report? [y/N]: ").strip().lower()
    if ans in ("y", "yes"):
        save_outputs(results, summary, cfg, picks)
    else:
        print("Not saved.")
