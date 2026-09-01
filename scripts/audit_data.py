#!/usr/bin/env python3
"""Data audit for mathematical modeling contest attachments.

Usage:
  python audit_data.py --data <folder-or-file> --out <report.md>

Scans CSV/TSV/XLSX files (folder or single file) and produces a markdown
audit report: rows, columns, dtypes, missing values, unique counts,
min/max/mean, and IQR-based outlier counts. Uses pandas when available and
falls back to stdlib csv otherwise.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import pandas as pd

    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False


def audit_csv_stdlib(path: Path) -> dict:
    import csv

    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return {"file": str(path), "rows": 0, "columns": [], "note": "empty"}
    cols = list(rows[0].keys())
    report: dict = {"file": str(path), "rows": len(rows), "columns": cols}
    for c in cols:
        values = [r.get(c) for r in rows]
        non_null = [v for v in values if v not in (None, "")]
        report[c] = {
            "non_null": len(non_null),
            "unique": len(set(non_null)),
            "sample": non_null[:3],
        }
    return report


def audit_pandas(path: Path) -> dict:
    if path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    report: dict = {
        "file": str(path),
        "rows": int(len(df)),
        "columns": list(df.columns),
    }
    for c in df.columns:
        s = df[c]
        num = pd.to_numeric(s, errors="coerce")
        info = {
            "dtype": str(s.dtype),
            "non_null": int(s.notna().sum()),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique()),
        }
        if num.notna().sum() > 0:
            q1 = num.quantile(0.25)
            q3 = num.quantile(0.75)
            iqr = q3 - q1
            lo = q1 - 1.5 * iqr
            hi = q3 + 1.5 * iqr
            info.update(
                {
                    "min": float(num.min()),
                    "max": float(num.max()),
                    "mean": float(num.mean()),
                    "iqr_outliers": int(((num < lo) | (num > hi)).sum()),
                }
            )
        report[c] = info
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit contest data files")
    ap.add_argument("--data", required=True, help="data folder or a single file")
    ap.add_argument("--out", required=True, help="output markdown report path")
    args = ap.parse_args()

    target = Path(args.data)
    files: list[Path] = []
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(
            f
            for f in target.iterdir()
            if f.suffix.lower() in (".csv", ".tsv", ".xlsx", ".xls")
        )

    reports = []
    for f in files:
        try:
            reports.append(audit_pandas(f) if HAVE_PANDAS else audit_csv_stdlib(f))
        except Exception as exc:  # report per-file failures
            reports.append({"file": str(f), "error": str(exc)})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# 数据审计报告", ""]
    for r in reports:
        lines.append(f"## {r.get('file')}")
        if "error" in r:
            lines.append(f"错误：{r['error']}")
            continue
        lines.append(f"- 行数：{r.get('rows')}，列：{len(r.get('columns', []))}")
        for c in r.get("columns", []):
            lines.append(f"- `{c}`：{json.dumps(r.get(c, {}), ensure_ascii=False)}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"audit report written to {out}")


if __name__ == "__main__":
    main()

