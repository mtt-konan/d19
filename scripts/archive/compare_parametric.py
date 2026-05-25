"""Compare the CPU baseline and accelerated parametric search paths.

Usage:
    uv run python scripts/compare_parametric.py --max-m 20 --max-k-num 80 --max-k-den 40
    uv run python scripts/compare_parametric.py \
        --max-m 80 --max-k-num 640 --max-k-den 320 --backend torch
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _resolve_backend(name: str):
    from rational_distance.backend import _try_torch, detect_backend

    if name == "numpy":
        return np, "forced:numpy"
    if name == "cupy":
        import cupy as cp

        return cp, "forced:cupy"
    if name == "torch":
        xp = _try_torch()
        if xp is None:
            raise RuntimeError("PyTorch ROCm/CUDA not available.")
        return xp, "forced:torch"
    xp, backend_name, _ = detect_backend()
    return xp, backend_name


def _point_keys(points) -> set[tuple]:
    return {(pt.x, pt.y) for pt in points}


def _resolve_limits(args: argparse.Namespace) -> None:
    """Resolve compare-script limits, keeping `--scale` as the shorthand."""
    default_max_m = 20
    default_max_k_num = 80
    default_max_k_den = 40

    if args.scale is not None:
        if args.max_m is None:
            args.max_m = args.scale
        if args.max_k_den is None:
            args.max_k_den = 4 * args.scale
        if args.max_k_num is None:
            args.max_k_num = 8 * args.scale

    if args.max_m is None:
        args.max_m = default_max_m
    if args.max_k_num is None:
        args.max_k_num = default_max_k_num
    if args.max_k_den is None:
        args.max_k_den = default_max_k_den


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="compare_parametric.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--scale", type=int, default=None)
    parser.add_argument("--max-m", type=int, default=None)
    parser.add_argument("--max-k-num", type=int, default=None)
    parser.add_argument("--max-k-den", type=int, default=None)
    parser.add_argument("--min-rational", type=int, default=3, choices=[3, 4])
    parser.add_argument("--inside", action="store_true")
    parser.add_argument(
        "--backend",
        type=str,
        default="auto",
        choices=["auto", "cupy", "torch", "numpy"],
        help="Accelerated backend to compare against the CPU baseline.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="CPU worker processes for the baseline run (default: 1 for deterministic debug runs).",
    )
    return parser


def main() -> int:
    from rational_distance.search import _parametric_search_fast_run, dedup_by_symmetry
    from rational_distance.search_gpu import _parametric_search_gpu_run

    args = build_parser().parse_args()
    _resolve_limits(args)

    try:
        xp, accel_backend_name = _resolve_backend(args.backend)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("=" * 72)
    print("Parametric CPU vs accelerated compare")
    print(
        f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den}, "
        f"min_rational={args.min_rational}, inside={args.inside}"
    )
    print(f"  accelerated backend: {accel_backend_name}")
    print("=" * 72)

    cpu_t0 = time.perf_counter()
    cpu_points, cpu_stats = _parametric_search_fast_run(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        min_rational=args.min_rational,
        workers=args.workers,
        progress=False,
        inside_only=args.inside,
    )
    cpu_elapsed = time.perf_counter() - cpu_t0

    accel_t0 = time.perf_counter()
    accel_points, accel_backend_used, accel_stats = _parametric_search_gpu_run(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        min_rational=args.min_rational,
        progress=False,
        xp=xp,
        inside_only=args.inside,
    )
    accel_elapsed = time.perf_counter() - accel_t0

    cpu_keys = _point_keys(cpu_points)
    accel_keys = _point_keys(accel_points)
    diff = cpu_keys ^ accel_keys

    cpu_orbits = dedup_by_symmetry(cpu_points)
    accel_orbits = dedup_by_symmetry(accel_points)

    print("\nCPU baseline")
    print(f"  backend: numpy multiprocessing ({args.workers} worker(s))")
    print(f"  elapsed: {cpu_elapsed:.3f}s")
    print(f"  points: {len(cpu_points)}")
    print(f"  D4 orbits: {len(cpu_orbits)}")
    print(
        f"  exact fallback: {'yes' if cpu_stats.fallback_triggered else 'no'} "
        f"({cpu_stats.exact_fallback_triples}/{cpu_stats.total_triples})"
    )

    print("\nAccelerated path")
    print(f"  backend: {accel_backend_used}")
    print(f"  elapsed: {accel_elapsed:.3f}s")
    print(f"  points: {len(accel_points)}")
    print(f"  D4 orbits: {len(accel_orbits)}")
    print(
        f"  exact fallback: {'yes' if accel_stats.fallback_triggered else 'no'} "
        f"({accel_stats.exact_fallback_triples}/{accel_stats.total_triples})"
    )

    print("\nComparison")
    print(f"  symmetric difference: {len(diff)}")
    print(f"  match: {'yes' if not diff else 'no'}")

    return 0 if not diff else 1


if __name__ == "__main__":
    raise SystemExit(main())
