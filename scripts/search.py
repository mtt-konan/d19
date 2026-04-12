"""Rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1).

Single entry point supporting two complementary search methods:

  parametric   Parametric brute-force search (GPU / CPU multiprocessing)
  ec           Elliptic-curve guided search (chord-tangent orbit expansion)

──────────────────────────────────────────────────────────────────────────
PARAMETRIC METHOD
──────────────────────────────────────────────────────────────────────────
Iterates over primitive Pythagorean triples (p,q,r) and rational scale
factors k=a/b to generate candidate points P=(kp/r, kq/r).  Checks each
candidate's distances to all four vertices using integer arithmetic and
numpy/GPU vectorisation.

  uv run python scripts/search.py parametric --scale 200
  uv run python scripts/search.py parametric --scale 200 --backend torch
  uv run python scripts/search.py parametric --scale 80  --backend numpy
  uv run python scripts/search.py parametric --scale 400 --inside
  uv run python scripts/search.py parametric --max-m 50 --max-k-num 400 --max-k-den 200

Backend options (--backend):
  auto   try CuPy → PyTorch → NumPy  (default)
  numpy  CPU multiprocessing, int64-safe, any scale
  cupy   NVIDIA/AMD GPU via CuPy (Linux)
  torch  AMD/NVIDIA GPU via PyTorch (recommended for Windows AMD)

──────────────────────────────────────────────────────────────────────────
EC METHOD
──────────────────────────────────────────────────────────────────────────
Finds seeds (k values where dA, dB, dD are simultaneously rational) then
expands each seed's rational orbit along the associated quartic elliptic
curve using chord-tangent arithmetic (exact Fraction arithmetic, no GPU).

  uv run python scripts/search.py ec --max-m 30
  uv run python scripts/search.py ec --max-m 50 --max-k-num 400 --max-k-den 800
  uv run python scripts/search.py ec --min-rational 4 --inside

──────────────────────────────────────────────────────────────────────────
GPU SETUP — AMD Ryzen AI Max+ 392 (Windows, ROCm)
──────────────────────────────────────────────────────────────────────────
  uv python install 3.12 && uv python pin 3.12 && uv sync
  uv pip install torch --index-url https://repo.amd.com/rocm/whl/gfx1151/
  python -c "import torch; print(torch.cuda.is_available())"
  uv run python scripts/search.py parametric --scale 200 --backend torch

GPU SETUP — NVIDIA RTX 4090 (CUDA)
  pip install cupy-cuda12x
  uv run python scripts/search.py parametric --scale 200 --backend cupy
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# ── Shared formatting ─────────────────────────────────────────────────────────

def _header() -> str:
    return (f"{'cnt':>3}  {'den':>7}  {'x':>14}  {'y':>14}  "
            f"{'d(A)':>10}  {'d(B)':>10}  {'d(C)':>10}  {'d(D)':>10}")


def _row(pt) -> str:
    def fmt(d):
        return f"{str(d):>10}" if d is not None else f"{'?':>10}"
    dA, dB, dC, dD = pt.distances
    return (f"{pt.rational_count:>3}  {pt.denominator:>7}  "
            f"{str(pt.x):>14}  {str(pt.y):>14}  "
            f"{fmt(dA)}  {fmt(dB)}  {fmt(dC)}  {fmt(dD)}")


def _size_estimate(max_m: int, max_k_num: int, max_k_den: int) -> str:
    n_triples = sum(
        1 for m in range(2, max_m + 1) for n in range(1, m)
        if (m - n) % 2 == 1 and gcd(m, n) == 1
    ) * 2
    n_pairs = sum(
        1 for b in range(1, max_k_den + 1)
        for a in range(1, max_k_num + 1)
        if gcd(a, b) == 1
    )
    total = n_triples * n_pairs
    if total >= 1_000_000_000:
        return f"{total/1e9:.1f}B"
    if total >= 1_000_000:
        return f"{total/1e6:.1f}M"
    return f"{total:,}"


def _print_summary(results, elapsed, deduped_from=None):
    count_by_n: dict[int, int] = {}
    for pt in results:
        count_by_n[pt.rational_count] = count_by_n.get(pt.rational_count, 0) + 1

    print(f"\n{'─'*72}")
    if deduped_from is not None and deduped_from != len(results):
        print(f"Found {deduped_from} points → {len(results)} orbits after D4 dedup  ({elapsed:.2f}s)")
    else:
        print(f"Found {len(results)} unique points in {elapsed:.2f}s")
    for n in sorted(count_by_n, reverse=True):
        marker = " ◄ 4-VERTEX SOLUTION!" if n == 4 else ""
        print(f"  {count_by_n[n]:6d}  points with {n}/4 rational distances{marker}")
    print(f"{'─'*72}\n")
    return count_by_n


def _print_table(results, top):
    display = results if top == 0 else results[:top]
    print(_header())
    print("─" * 85)
    for pt in display:
        print(_row(pt))
    if top and len(results) > top:
        print(f"  … {len(results) - top} more rows omitted (use --top 0 to see all)")


def _print_four_vertex(results):
    four = [pt for pt in results if pt.rational_count == 4]
    if four:
        print(f"\n{'!'*72}")
        print(f"  {len(four)} POINT(S) WITH ALL FOUR RATIONAL DISTANCES:")
        for pt in four:
            print(f"  {pt}")
        print(f"{'!'*72}")
    else:
        print("\n(No 4-vertex solutions found in this search range.)")


def _save_json(path: str, method: str, params: dict, elapsed: float,
               results, count_by_n: dict, backend: str = "") -> None:
    payload = {
        "method": method,
        "backend": backend,
        "search_params": params,
        "elapsed_seconds": round(elapsed, 3),
        "total_found": len(results),
        "count_by_rational": {str(k): v for k, v in count_by_n.items()},
        "points": [pt.as_dict() for pt in results],
    }
    Path(path).write_text(json.dumps(payload, indent=2))
    print(f"\nResults written to {path}")


# ── Subcommand: parametric ────────────────────────────────────────────────────

def _add_common_args(p: argparse.ArgumentParser) -> None:
    """Add arguments shared by both subcommands."""
    p.add_argument("--min-rational", type=int, default=3, choices=[3, 4],
                   help="Minimum rational distances to report (default: 3)")
    p.add_argument("--inside", action="store_true",
                   help="Only return points strictly inside the unit square (0<x<1, 0<y<1)")
    p.add_argument("--out", type=str, default=None,
                   help="Write JSON results to this file")
    p.add_argument("--top", type=int, default=50,
                   help="Max rows to print (0=all, default: 50)")
    p.add_argument("--no-progress", action="store_true",
                   help="Suppress the progress bar")


def _run_parametric(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance.search import (
        brute_force_search,
        dedup_by_symmetry,
        merge_results,
        parametric_search_fast,
    )
    from rational_distance.search_gpu import parametric_search_gpu

    if args.scale is not None:
        args.max_m     = args.scale
        args.max_k_den = 4 * args.scale
        args.max_k_num = 8 * args.scale

    # Resolve backend
    use_cpu = (args.backend == "numpy")
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
    print(f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den}, "
          f"min_rational={args.min_rational}")
    print(f"  search space ≈ {est} (triple × k combinations)")
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
            bf = list(brute_force_search(max_den=args.brute_den,
                                         min_rational=args.min_rational))
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
            bf = list(brute_force_search(max_den=args.brute_den,
                                         min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))

    raw_count = len(results)
    if dedup_sym:
        results = dedup_by_symmetry(results)

    elapsed = time.perf_counter() - t0
    count_by_n = _print_summary(results, elapsed,
                                deduped_from=raw_count if dedup_sym else None)
    _print_table(results, args.top)
    _print_four_vertex(results)

    if args.out:
        params = {
            "max_m": args.max_m, "max_k_num": args.max_k_num,
            "max_k_den": args.max_k_den, "min_rational": args.min_rational,
            "backend": args.backend, "workers": args.workers,
            "inside": args.inside, "brute_den": args.brute_den,
            "no_dedup_symmetry": args.no_dedup_symmetry,
        }
        _save_json(args.out, "parametric", params, elapsed,
                   results, count_by_n, backend=backend_used)


# ── Subcommand: ec ────────────────────────────────────────────────────────────

def _run_ec(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance.search_ec import ec_search

    # Resolve backend for the seed-finding step
    xp = None
    backend_name = "numpy (CPU)"
    if args.backend == "numpy":
        pass  # xp stays None → numpy path
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
    elif args.backend == "auto":
        xp_auto, backend_name, _ = detect_backend()
        import numpy as _np
        xp = None if xp_auto is _np else xp_auto
        backend_name = backend_name if xp is not None else "numpy (CPU)"

    print("=" * 72)
    print("Rational distance search [ec] — A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  backend  : {backend_name}")
    print(f"  max_m={args.max_m}, seed range k_num≤{args.max_k_num}, "
          f"k_den≤{args.max_k_den}")
    print(f"  max_steps={args.max_steps}, min_rational={args.min_rational}, "
          f"inside={args.inside}")
    print("=" * 72)

    t0 = time.perf_counter()
    results = ec_search(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        max_steps=args.max_steps,
        min_rational=args.min_rational,
        inside_only=args.inside,
        progress=not args.no_progress,
        xp=xp,
    )
    elapsed = time.perf_counter() - t0

    count_by_n = _print_summary(results, elapsed)
    _print_table(results, args.top)
    _print_four_vertex(results)

    if args.out:
        params = {
            "max_m": args.max_m, "max_k_num": args.max_k_num,
            "max_k_den": args.max_k_den, "max_steps": args.max_steps,
            "min_rational": args.min_rational, "inside": args.inside,
        }
        _save_json(args.out, "ec", params, elapsed, results, count_by_n)


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="search.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="method", metavar="METHOD")
    sub.required = True

    # ── parametric ──────────────────────────────────────────────────────────
    p = sub.add_parser(
        "parametric",
        help="Parametric brute-force search (GPU / CPU multiprocessing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Parametric brute-force search over Pythagorean triples and scale factors.",
    )
    p.add_argument("--scale", type=int, default=None,
                   help="Shorthand: sets max_m=N, max_k_den=4N, max_k_num=8N")
    p.add_argument("--max-m",     type=int, default=80,
                   help="Max m for Pythagorean triple generation (default: 80)")
    p.add_argument("--max-k-num", type=int, default=640,
                   help="Max numerator of scale k=a/b (default: 640)")
    p.add_argument("--max-k-den", type=int, default=320,
                   help="Max denominator of scale k=a/b (default: 320)")
    p.add_argument("--backend", type=str, default="auto",
                   choices=["auto", "cupy", "torch", "numpy"],
                   help="Compute backend: auto|cupy|torch|numpy (default: auto)")
    p.add_argument("--workers", type=int, default=0,
                   help="CPU worker processes for numpy backend (0=auto)")
    p.add_argument("--brute-den", type=int, default=0,
                   help="Also run brute-force search up to this denominator (0=skip)")
    p.add_argument("--no-dedup-symmetry", action="store_true",
                   help="Show all D4 symmetric copies (default: one per orbit)")
    _add_common_args(p)

    # ── ec ──────────────────────────────────────────────────────────────────
    e = sub.add_parser(
        "ec",
        help="Elliptic-curve guided search (chord-tangent orbit expansion)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "EC-guided search: find seeds by brute force, then expand rational\n"
            "orbits on the associated quartic elliptic curve to reach points\n"
            "outside the brute-force range."
        ),
    )
    e.add_argument("--max-m",     type=int, default=30,
                   help="Max m for Pythagorean triple generation (default: 30)")
    e.add_argument("--max-k-num", type=int, default=400,
                   help="Max numerator for seed search k=a/b (default: 400)")
    e.add_argument("--max-k-den", type=int, default=800,
                   help="Max denominator for seed search k=a/b (default: 800)")
    e.add_argument("--max-steps", type=int, default=20,
                   help="Max chord-tangent expansion steps per orbit (default: 20)")
    e.add_argument("--backend", type=str, default="auto",
                   choices=["auto", "cupy", "torch", "numpy"],
                   help="Backend for seed finding: auto|cupy|torch|numpy (default: auto)")
    _add_common_args(e)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.method == "parametric":
        _run_parametric(args)
    elif args.method == "ec":
        _run_ec(args)


if __name__ == "__main__":
    main()
