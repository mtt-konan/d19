#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from itertools import islice
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


class BenchmarkArgs(argparse.Namespace):
    max_hyp: int = 0
    limit: int = 0
    batch_size: int = 0
    json_out: Path = Path()
    full_permutations: bool = False
    head_only: bool = False
    safe_top2_only: bool = False
    safe_first_only: bool = False
    skip_extra: bool = False
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
    _ = parser.add_argument("--head-only", action="store_true")
    _ = parser.add_argument("--safe-top2-only", action="store_true")
    _ = parser.add_argument("--safe-first-only", action="store_true")
    _ = parser.add_argument("--skip-extra", action="store_true")
    add_parallel_args(parser)
    return parser.parse_args(argv, namespace=BenchmarkArgs())


def main(argv: list[str] | None = None) -> int:
    from rational_distance.concordant.pairs import iter_ab_pairs
    from rational_distance.parallel import get_parallel_config_from_args
    from rational_distance.proof_status.ab_sieve_benchmark import (
        CORE_METHOD_NAMES,
        OrderSpec,
        benchmark_specs,
        build_core_order_specs,
        build_full_order_specs,
        build_head_validation_specs,
        build_incremental_specs,
        build_legacy_baseline_spec,
        build_safe_top2_specs,
        build_tail_order_specs,
    )

    args = parse_args(argv)

    def pair_source():
        pairs = iter_ab_pairs(args.max_hyp)
        if args.limit > 0:
            return islice(pairs, args.limit)
        return pairs

    cfg = get_parallel_config_from_args(args)
    best_core_names: list[str]
    extra_specs: list[OrderSpec]

    if args.head_only:
        core_specs = build_head_validation_specs()
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pair_source,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        extra_specs = []
        best_core_names = list(
            min(
                core_summaries,
                key=lambda summary: summary.total_elapsed_s,
            ).spec.method_names
        )
    elif args.safe_top2_only:
        core_specs = build_safe_top2_specs()
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pair_source,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        extra_specs = []
        best_core_names = list(
            min(
                core_summaries,
                key=lambda summary: summary.total_elapsed_s,
            ).spec.method_names
        )
    elif args.full_permutations:
        core_specs = build_full_order_specs()
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pair_source,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        extra_specs = [] if args.skip_extra else [build_legacy_baseline_spec()]
        best_core_names = list(
            min(
                core_summaries,
                key=lambda summary: summary.total_elapsed_s,
            ).spec.method_names
        )
    else:
        core_prefix = (CORE_METHOD_NAMES[0],) if args.safe_first_only else ()
        core_specs = build_core_order_specs(prefix=core_prefix)
        core_summaries = benchmark_specs(
            specs=core_specs,
            pairs=pair_source,
            parallel=cfg,
            batch_size=args.batch_size,
        )
        best_core = min(core_summaries, key=lambda summary: summary.total_elapsed_s)
        best_core_names = list(best_core.spec.method_names)
        if args.skip_extra:
            extra_specs = []
        else:
            extra_specs = build_tail_order_specs(best_core.spec.method_names)
            extra_specs.extend(build_incremental_specs(best_core.spec.method_names))
            extra_specs.append(build_legacy_baseline_spec())

    if args.head_only or args.safe_top2_only or args.skip_extra:
        extra_summaries = []
    else:
        extra_summaries = benchmark_specs(
            specs=extra_specs,
            pairs=pair_source,
            parallel=cfg,
            batch_size=args.batch_size,
        )

    pair_count = core_summaries[0].n_pairs if core_summaries else 0

    payload = {
        "max_hyp": args.max_hyp,
        "pair_count": pair_count,
        "core_order_count": len(core_specs),
        "extra_order_count": len(extra_specs),
        "best_core_order": best_core_names,
        "head_only": args.head_only,
        "safe_top2_only": args.safe_top2_only,
        "safe_first_only": args.safe_first_only,
        "skip_extra": args.skip_extra,
        "core": [summary.to_dict() for summary in core_summaries],
        "extra": [summary.to_dict() for summary in extra_summaries],
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    _ = args.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"pairs={pair_count} core_orders={len(core_specs)} extra_orders={len(extra_specs)}")
    print(f"best_core={' -> '.join(best_core_names)}")
    print(f"json={args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
