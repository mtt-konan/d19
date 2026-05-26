#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


class BenchmarkArgs(argparse.Namespace):
    max_hyp: int = 0
    limit: int = 0
    batch_size: int = 0
    json_out: Path = Path()
    full_permutations: bool = False
    workers: int = 1
    chunksize: int = 50
    serial: bool = False


def parse_args(argv: list[str] | None = None) -> BenchmarkArgs:
    from rational_distance.parallel import add_parallel_args

    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--max-hyp", type=int, default=500)
    _ = parser.add_argument("--limit", type=int, default=0)
    _ = parser.add_argument("--batch-size", type=int, default=64)
    _ = parser.add_argument(
        "--json-out",
        type=Path,
        default=ROOT / "results" / "ab_sieve_benchmark.json",
    )
    _ = parser.add_argument("--full-permutations", action="store_true")
    add_parallel_args(parser)
    return parser.parse_args(argv, namespace=BenchmarkArgs())


def main(argv: list[str] | None = None) -> int:
    from rational_distance.concordant.pairs import generate_ab_pairs
    from rational_distance.parallel import get_parallel_config_from_args
    from rational_distance.proof_status.ab_sieve_benchmark import (
        benchmark_specs,
        build_core_order_specs,
        build_full_order_specs,
        build_incremental_specs,
        build_legacy_baseline_spec,
        build_tail_order_specs,
    )

    args = parse_args(argv)
    pairs = generate_ab_pairs(args.max_hyp)
    if args.limit > 0:
        pairs = pairs[: args.limit]
    cfg = get_parallel_config_from_args(args)
    best_core_names: list[str]

    if args.full_permutations:
        core_specs = build_full_order_specs()
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pairs,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        extra_specs = [build_legacy_baseline_spec()]
        best_core_names = list(
            min(
                core_summaries,
                key=lambda summary: summary.total_elapsed_s,
            ).spec.method_names
        )
    else:
        core_specs = build_core_order_specs()
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pairs,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        best_core = min(core_summaries, key=lambda summary: summary.total_elapsed_s)
        extra_specs = build_tail_order_specs(best_core.spec.method_names)
        extra_specs.extend(build_incremental_specs(best_core.spec.method_names))
        extra_specs.append(build_legacy_baseline_spec())
        best_core_names = list(best_core.spec.method_names)

    extra_summaries = benchmark_specs(
        specs=extra_specs,
        pairs=pairs,
        parallel=cfg,
        batch_size=args.batch_size,
    )

    payload = {
        "max_hyp": args.max_hyp,
        "pair_count": len(pairs),
        "core_order_count": len(core_specs),
        "extra_order_count": len(extra_specs),
        "best_core_order": best_core_names,
        "core": [summary.to_dict() for summary in core_summaries],
        "extra": [summary.to_dict() for summary in extra_summaries],
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    _ = args.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"pairs={len(pairs)} core_orders={len(core_specs)} extra_orders={len(extra_specs)}")
    print(f"best_core={' -> '.join(best_core_names)}")
    print(f"json={args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
