"""Analyze persisted EC search runs and optionally render HTML."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _print_summary(report: dict) -> None:
    run = report["run"]
    summary = report["summary"]

    print("=" * 72)
    print(f"EC database analysis — run {run['id']}")
    print(f"  backend={run['backend']}, status={run['status']}")
    print(
        f"  points={summary['point_count']}, triples={summary['triple_count']}, "
        f"seeds={summary['seed_count']}"
    )
    print(
        "  point denominator stats:",
        summary["point_denominators"],
    )
    print(
        "  seed k denominator stats:",
        summary["seed_k_denominators"],
    )
    print("  missing vertex counts:", summary["missing_vertex_counts"])
    print("  source counts:", summary["source_counts"])
    print("=" * 72)

    if report["top_triples_by_points"]:
        print("\nTop triples by points:")
        for item in report["top_triples_by_points"][:5]:
            triple = tuple(item["triple"])
            print(
                f"  {triple}: points={item['point_count']}, seeds={item['seed_count']}, "
                f"slope={item['slope']}, inside={item['inside_points']}, "
                f"outside={item['outside_points']}"
            )

    if report["outside_only_triples"]:
        print("\nOutside-only triples:")
        for item in report["outside_only_triples"][:5]:
            triple = tuple(item["triple"])
            print(f"  {triple}: points={item['point_count']}, seeds={item['seed_count']}")


def main() -> None:
    from rational_distance.ec_analysis import build_analysis_report, parse_triple_arg
    from scripts.visualize import build_html

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        required=True,
        help="SQLite database created by scripts/search.py ec",
    )
    parser.add_argument(
        "--run",
        default="latest",
        help="Run selector: latest or a numeric run id (default: latest)",
    )
    parser.add_argument("--triple", type=parse_triple_arg, help="Optional triple filter: p,q,r")
    parser.add_argument("--seed-id", type=int, default=None, help="Optional seed id filter")
    parser.add_argument(
        "--region",
        choices=["all", "inside", "outside"],
        default="all",
        help="Filter final points by region (default: all)",
    )
    parser.add_argument("--out-json", type=str, default=None, help="Write structured analysis JSON")
    parser.add_argument("--html", type=str, default=None, help="Write an HTML report")
    args = parser.parse_args()

    run_selector = int(args.run) if str(args.run).isdigit() else args.run
    report = build_analysis_report(
        db_path=args.db,
        run_selector=run_selector,
        triple=args.triple,
        seed_id=args.seed_id,
        region=args.region,
    )
    _print_summary(report)

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nAnalysis JSON written to {out_json}")

    if args.html:
        payload = report["visualize_payload"]
        html = build_html(payload, Path(args.html).name, inside_only=False)
        out_html = Path(args.html)
        out_html.write_text(html, encoding="utf-8")
        print(f"HTML report written to {out_html}")


if __name__ == "__main__":
    main()
