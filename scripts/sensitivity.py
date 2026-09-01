#!/usr/bin/env python3
"""One-at-a-time sensitivity analysis for contest models.

The model module must define:
    def model_fn(params: dict, **kwargs) -> float | dict[str, float]

Usage:
  python sensitivity.py --model src/model.py --func model_fn \
      --params '{"alpha": 0.5, "beta": 100}' --perturb 0.1 \
      --out tables/sensitivity.md [--plot figures/sensitivity.png]

With --perturb 0.1 each parameter is scanned at -10% / baseline / +10%.
Use --grid '{"alpha": [0.5, 0.9, 5]}' to scan an explicit linear grid
(start, end, n) instead, which gives smoother line plots.

Parameters are varied one at a time (OAT). If model_fn returns a dict,
every output key is reported separately.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path


def load_function(module_path: str, func_name: str):
    path = Path(module_path).resolve()
    spec = importlib.util.spec_from_file_location("user_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, func_name):
        raise RuntimeError(f"function {func_name!r} not found in {path}")
    return getattr(module, func_name)


def flatten_output(output):
    if isinstance(output, dict):
        return list(output.items())
    return [("output", output)]


def build_grids(params: dict, perturb: float, grid: dict) -> dict:
    grids = {}
    for name, base in params.items():
        if name in grid:
            start, end, n = grid[name]
            grids[name] = [start + (end - start) * i / (n - 1) for i in range(n)]
        else:
            grids[name] = [base * (1 - perturb), base, base * (1 + perturb)]
    return grids


def configure_cjk_font() -> None:
    """Pick a CJK-capable font so Chinese labels render correctly."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    available = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in (
        "Microsoft YaHei",
        "SimHei",
        "PingFang SC",
        "Noto Sans CJK SC",
        "WenQuanYi Micro Hei",
    ):
        if candidate in available:
            plt.rcParams["font.family"] = candidate
            plt.rcParams["axes.unicode_minus"] = False
            return


def main() -> None:
    ap = argparse.ArgumentParser(description="OAT sensitivity analysis")
    ap.add_argument("--model", required=True, help="path to model .py module")
    ap.add_argument("--func", default="model_fn", help="function name in module")
    ap.add_argument("--params", required=True, help='JSON dict, e.g. {"a": 1.0}')
    ap.add_argument("--perturb", type=float, default=0.1, help="relative perturbation, default 0.1")
    ap.add_argument("--grid", default=None, help="JSON dict param -> [start, end, n]")
    ap.add_argument("--out", required=True, help="output markdown path")
    ap.add_argument("--plot", default=None, help="optional output figure path (png)")
    args = ap.parse_args()

    params = json.loads(args.params)
    grid = json.loads(args.grid) if args.grid else {}
    model_fn = load_function(args.model, args.func)
    grids = build_grids(params, args.perturb, grid)

    baseline = dict(flatten_output(model_fn(params)))
    rows = []  # (param, value, key, out, rel_change)
    plot_series = {}  # key -> param -> (xs, ys)
    for name, values in grids.items():
        for v in values:
            trial = dict(params)
            trial[name] = v
            for key, out in flatten_output(model_fn(trial)):
                base_val = baseline[key]
                rel = (out - base_val) / base_val if base_val else float("nan")
                rows.append((name, v, key, out, rel))
                series = plot_series.setdefault(key, {}).setdefault(name, ([], []))
                series[0].append(v)
                series[1].append(out)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# 灵敏度分析报告", ""]
    lines.append(f"- 基线参数：`{json.dumps(params, ensure_ascii=False)}`")
    lines.append(f"- 扰动方式：单参数逐项扫描（OAT），±{args.perturb:.0%} 或自定义网格")
    lines.append("")
    lines.append("| 参数 | 取值 | 输出项 | 输出值 | 相对变化 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for name, v, key, val, rel in rows:
        rel_s = f"{rel:.2%}" if not math.isnan(rel) else "-"
        lines.append(f"| {name} | {v:g} | {key} | {val:g} | {rel_s} |")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"sensitivity report written to {out}")

    if args.plot:
        try:
            configure_cjk_font()
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not available; skipping plot", file=sys.stderr)
            return
        fig, axes = plt.subplots(1, len(plot_series), figsize=(5 * len(plot_series), 4), squeeze=False)
        for ax, (key, series) in zip(axes[0], plot_series.items()):
            for name, (xs, ys) in series.items():
                order = sorted(range(len(xs)), key=lambda i: xs[i])
                ax.plot([xs[i] for i in order], [ys[i] for i in order], marker="o", label=name)
            ax.set_xlabel("参数取值")
            ax.set_ylabel("模型输出")
            ax.set_title(key)
            ax.legend()
        fig.tight_layout()
        plot_path = Path(args.plot)
        plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(plot_path, dpi=300)
        print(f"sensitivity figure written to {plot_path}")


if __name__ == "__main__":
    main()
