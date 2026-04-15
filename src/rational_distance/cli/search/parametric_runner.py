"""Parametric CLI runner."""

from __future__ import annotations

import argparse
import sys
import time

from .output import (
    _print_four_vertex,
    _print_summary,
    _print_table,
    _save_json,
    _size_estimate,
)


def _resolve_parametric_limits(args: argparse.Namespace) -> None:
    """Resolve the effective parametric limits for the CLI.

    `--scale` is a shorthand default. Explicit `--max-*` flags keep
    priority so callers can override one field without restating all of them.
    """
    default_max_m = 80
    default_max_k_num = 640
    default_max_k_den = 320

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


def _run_parametric(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance.search import (
        brute_force_search,
        dedup_by_symmetry,
        merge_results,
        parametric_search_fast,
    )
    from rational_distance.search_gpu import parametric_search_gpu

    _resolve_parametric_limits(args)

    use_cpu = args.backend == "numpy"
    xp = None
    backend_name = ""

    if use_cpu:
        backend_name = "numpy (CPU, multiprocessing)"
    elif args.backend == "cupy":
        import cupy as cp

        xp = cp
        backend_name = "forced:cupy"
    elif args.backend == "torch":
        xp = _try_torch()
        if xp is None:
            print("ERROR: PyTorch ROCm/CUDA not available.", file=sys.stderr)
            sys.exit(1)
        backend_name = "forced:torch"
    else:
        xp, backend_name, _ = detect_backend()

    est = _size_estimate(args.max_m, args.max_k_num, args.max_k_den)
    print("=" * 72)
    print("Rational distance search [parametric] — A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  backend  : {backend_name}")
    print(
        f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den}, "
        f"min_rational={args.min_rational}"
    )
    print(f"  search space ≈ {est} (triple x k combinations)")
    if args.inside:
        print("  Filter: inside unit square only (0<x<1, 0<y<1)")
    if args.brute_den:
        print(f"  + brute-force denominator ≤ {args.brute_den}")
    print("=" * 72)

    dedup_sym = not args.no_dedup_symmetry
    t0 = time.perf_counter()

    if use_cpu:
        results = parametric_search_fast(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            workers=args.workers,
            progress=not args.no_progress,
            inside_only=args.inside,
        )
        if args.brute_den:
            bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))
        backend_used = backend_name
    else:
        results, backend_used = parametric_search_gpu(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            progress=not args.no_progress,
            xp=xp,
            inside_only=args.inside,
        )
        if args.brute_den:
            bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))

    raw_count = len(results)
    if dedup_sym:
        results = dedup_by_symmetry(results)

    elapsed = time.perf_counter() - t0
    count_by_n = _print_summary(results, elapsed, deduped_from=raw_count if dedup_sym else None)
    _print_table(results, args.top)
    _print_four_vertex(results)

    if args.out:
        params = {
            "max_m": args.max_m,
            "max_k_num": args.max_k_num,
            "max_k_den": args.max_k_den,
            "min_rational": args.min_rational,
            "backend": args.backend,
            "workers": args.workers,
            "inside": args.inside,
            "brute_den": args.brute_den,
            "no_dedup_symmetry": args.no_dedup_symmetry,
        }
        _save_json(
            args.out, "parametric", params, elapsed, results, count_by_n, backend=backend_used
        )


__all__ = ["_resolve_parametric_limits", "_run_parametric"]
