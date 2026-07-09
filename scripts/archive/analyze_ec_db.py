#!/usr/bin/env python3
"""Analyze a persisted historical EC search database."""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from rational_distance._legacy.ec_analysis import build_analysis_report  # noqa: E402


def _write_html(path: str | Path, report: dict) -> None:
    payload = json.dumps(report)
    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>EC analysis</title></head>
<body>
<h1>EC analysis</h1>
<h2>Pattern Insights</h2>
<pre id="payload">{escape(json.dumps(report, indent=2))}</pre>
<script>
const report = {payload};
Plotly.newPlot;
</script>
</body>
</html>
"""
    Path(path).write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="EC database analysis")
    parser.add_argument("--db", required=True)
    parser.add_argument("--run", default="latest")
    parser.add_argument("--region", default="all")
    parser.add_argument("--out-json")
    parser.add_argument("--html")
    args = parser.parse_args()

    report = build_analysis_report(args.db, run_selector=args.run, region=args.region)
    if args.out_json:
        Path(args.out_json).write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.html:
        _write_html(args.html, report)


if __name__ == "__main__":
    main()
