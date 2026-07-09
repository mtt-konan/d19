#!/usr/bin/env python3
"""Analyze a persisted historical chain-fast database."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from rational_distance._legacy.chain_analysis import build_chain_analysis_report  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Chain database analysis")
    parser.add_argument("--db", required=True)
    parser.add_argument("--run", default="latest")
    parser.add_argument("--bucket-type", default="all")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--min-after-basic", type=int, default=1000)
    parser.add_argument("--out-json")
    args = parser.parse_args()

    report = build_chain_analysis_report(
        args.db,
        run_selector=args.run,
        bucket_type=args.bucket_type,
        top=args.top,
        min_after_basic=args.min_after_basic,
    )
    print("Chain database analysis")
    print(f"run_id={report['run']['id']}")
    if args.out_json:
        Path(args.out_json).write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
