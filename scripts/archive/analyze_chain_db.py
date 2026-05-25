"""Analyze persisted chain-fast bucket statistics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _print_ranked_section(title: str, rows: list[dict]) -> None:
    print(f"\n{title}:")
    if not rows:
        print("  (no rows passed the current filter)")
        return
    for row in rows:
        print(
            f"  key={row['bucket_key']}  "
            f"after_basic={row['n_after_basic']}  "
            f"c3_pass={row['n_c3_pass']}  "
            f"c4_pass={row['n_c4_pass']}  "
            f"near_miss={row['n_near_miss']}  "
            f"c3_rate={row['c3_rate']:.6f}  "
            f"near_miss_rate={row['near_miss_rate']:.6f}  "
            f"best_sq4_deficit={row['best_sq4_deficit']}"
        )
        if row["best_sample"] is not None:
            sample = row["best_sample"]
            print(
                "    sample="
                f"({sample['a']}, {sample['b']}, {sample['c']}, {sample['d']})  "
                f"sq3_deficit={sample['sq3_deficit']}  "
                f"sq4_deficit={sample['sq4_deficit']}"
            )


def _print_summary(report: dict) -> None:
    run = report["run"]
    filters = report["filters"]
    print("=" * 72)
    print(f"Chain database analysis - run {run['id']}")
    print(
        f"  backend={run['backend']}  status={run['status']}  "
        f"bucket_stats={run['bucket_stats']}"
    )
    print(
        f"  elapsed_s={run['elapsed_s']:.3f}  "
        f"bucket_type={filters['bucket_type']}  "
        f"min_after_basic={filters['min_after_basic']}  top={filters['top']}"
    )
    print("=" * 72)

    summaries = report["summary"]["bucket_type_summaries"]
    for bucket_name, summary in summaries.items():
        print(
            f"\n[{bucket_name}] rows={summary['row_count']}  "
            f"n_total={summary['n_total']}  "
            f"n_after_basic={summary['n_after_basic']}  "
            f"n_c3_pass={summary['n_c3_pass']}  "
            f"n_c4_pass={summary['n_c4_pass']}  "
            f"n_near_miss={summary['n_near_miss']}"
        )
        rankings = report["rankings"][bucket_name]
        _print_ranked_section("Top C3 rate", rankings["top_c3_rate"])
        _print_ranked_section("Top near-miss rate", rankings["top_near_miss_rate"])
        _print_ranked_section("Closest sq4 near-miss", rankings["closest_sq4_near_miss"])


def main() -> None:
    from rational_distance.chain_analysis import build_chain_analysis_report

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="SQLite database created by chain-fast runs")
    parser.add_argument(
        "--run",
        default="latest",
        help="Run selector: latest or numeric run id (default: latest)",
    )
    parser.add_argument(
        "--bucket-type",
        choices=["all", "g_bucket", "delta_bucket", "residue_bucket"],
        default="all",
        help="Which bucket family to analyze (default: all)",
    )
    parser.add_argument("--top", type=int, default=20, help="Top rows per ranking (default: 20)")
    parser.add_argument(
        "--min-after-basic",
        type=int,
        default=1000,
        help="Ignore buckets with too little post-basic sample size (default: 1000)",
    )
    parser.add_argument("--out-json", type=str, default=None, help="Write structured analysis JSON")
    args = parser.parse_args()

    run_selector = int(args.run) if str(args.run).isdigit() else args.run
    report = build_chain_analysis_report(
        db_path=args.db,
        run_selector=run_selector,
        bucket_type=args.bucket_type,
        top=args.top,
        min_after_basic=args.min_after_basic,
    )
    _print_summary(report)

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nAnalysis JSON written to {out_json}")


if __name__ == "__main__":
    main()
