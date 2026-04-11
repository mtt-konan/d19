"""Rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1).

Finds points whose distances to 3 (or all 4) vertices of the unit square
are simultaneously rational.  Supports GPU acceleration via CuPy or PyTorch.

Backend selection (--backend):
  auto   — try CuPy → PyTorch → NumPy (default)
  cupy   — force CuPy (NVIDIA/AMD GPU, Linux)
  torch  — force PyTorch ROCm/CUDA (recommended for Windows AMD)
  numpy  — force CPU-only (uses multiprocessing, safe for any scale)

GPU setup — AMD Ryzen AI Max+ 392 Windows (ROCm)
─────────────────────────────────────────────────
  uv python install 3.12 && uv python pin 3.12 && uv sync
  uv pip install torch --index-url https://repo.amd.com/rocm/whl/gfx1151/
  python -c "import torch; print(torch.cuda.is_available())"
  uv run python scripts/search_gpu.py --scale 200 --backend torch

GPU setup — AMD Ryzen AI Max+ 392 Linux (ROCm)
───────────────────────────────────────────────
  pip install torch --index-url https://download.pytorch.org/whl/rocm6.2

GPU setup — NVIDIA RTX 4090 (CUDA)
────────────────────────────────────
  pip install cupy-cuda12x   # or: pip install torch

Usage examples
──────────────
  uv run python scripts/search_gpu.py --scale 200
  uv run python scripts/search_gpu.py --scale 200 --backend torch
  uv run python scripts/search_gpu.py --scale 80  --backend numpy  # CPU, multiprocess
  uv run python scripts/search_gpu.py --scale 400 --inside         # unit square only
  uv run python scripts/search_gpu.py --help
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.search import (
    brute_force_search,
    dedup_by_symmetry,
    merge_results,
    parametric_search_fast,
)
from rational_distance.search_gpu import detect_backend, parametric_search_gpu
from rational_distance.square import RationalPoint


# ── Formatting ────────────────────────────────────────────────────────────────

def _header() -> str:
    return f"{'cnt':>3}  {'den':>7}  {'x':>14}  {'y':>14}  {'d(A)':>10}  {'d(B)':>10}  {'d(C)':>10}  {'d(D)':>10}"


def _row(pt: RationalPoint) -> str:
    def fmt(d):
        return f"{str(d):>10}" if d is not None else f"{'?':>10}"
    dA, dB, dC, dD = pt.distances
    return (
        f"{pt.rational_count:>3}  {pt.denominator:>7}  {str(pt.x):>14}  {str(pt.y):>14}  "
        f"{fmt(dA)}  {fmt(dB)}  {fmt(dC)}  {fmt(dD)}"
    )


def _size_estimate(max_m: int, max_k_num: int, max_k_den: int) -> str:
    from math import gcd
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--scale",        type=int,  default=None,
                        help="Shorthand: sets max_m=N, max_k_den=4N, max_k_num=8N")
    parser.add_argument("--max-m",        type=int,  default=80,
                        help="Max m for Pythagorean triple generation (default 80)")
    parser.add_argument("--max-k-num",    type=int,  default=640,
                        help="Max numerator of scale k (default 640)")
    parser.add_argument("--max-k-den",    type=int,  default=320,
                        help="Max denominator of scale k (default 320)")
    parser.add_argument("--min-rational", type=int,  default=3, choices=[2, 3, 4],
                        help="Minimum rational distances to report (default 3)")
    parser.add_argument("--backend",      type=str,  default="auto",
                        choices=["auto", "cupy", "torch", "numpy"],
                        help="Compute backend: auto|cupy|torch|numpy (default: auto)")
    parser.add_argument("--workers",      type=int,  default=0,
                        help="CPU worker processes — numpy backend only (0=auto)")
    parser.add_argument("--inside",       action="store_true",
                        help="Only return points strictly inside the unit square (0<x<1, 0<y<1)")
    parser.add_argument("--brute-den",    type=int,  default=0,
                        help="Also run brute-force search up to this denominator (0=skip)")
    parser.add_argument("--no-dedup-symmetry", action="store_true",
                        help="Show all symmetric copies (default: one per D4 orbit)")
    parser.add_argument("--out",          type=str,  default=None,
                        help="Write JSON results to this file")
    parser.add_argument("--top",          type=int,  default=50,
                        help="Max rows to print (0=all, default 50)")
    args = parser.parse_args()

    if args.scale is not None:
        args.max_m     = args.scale
        args.max_k_den = 4 * args.scale
        args.max_k_num = 8 * args.scale

    # ── Resolve backend ───────────────────────────────────────────────────
    use_cpu_path = (args.backend == "numpy")
    xp = None
    backend_name = ""

    if use_cpu_path:
        backend_name = "numpy (CPU, multiprocessing)"
    elif args.backend == "cupy":
        import cupy as cp
        xp = cp
        backend_name = "forced:cupy"
    elif args.backend == "torch":
        from rational_distance.search_gpu import _try_torch
        xp = _try_torch()
        if xp is None:
            print("ERROR: PyTorch ROCm/CUDA not available.", file=sys.stderr)
            sys.exit(1)
        backend_name = "forced:torch"
    else:  # auto
        xp, backend_name, _ = detect_backend()

    # ── Banner ────────────────────────────────────────────────────────────
    print("=" * 72)
    print("Rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  backend  : {backend_name}")
    print(f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den},",
          f"min_rational={args.min_rational}")
    est = _size_estimate(args.max_m, args.max_k_num, args.max_k_den)
    print(f"  search space ≈ {est} (triple × k combinations)")
    if args.inside:
        print("  Filter: inside unit square (0<x<1 and 0<y<1)")
    if args.brute_den:
        print(f"  + brute-force denominator ≤ {args.brute_den}")
    print("=" * 72)

    dedup_sym = not args.no_dedup_symmetry

    t0 = time.perf_counter()

    # ── Search ────────────────────────────────────────────────────────────
    if use_cpu_path:
        # numpy backend: use multiprocessing path (int64-safe, supports --workers)
        results = parametric_search_fast(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            workers=args.workers,
            progress=True,
            inside_only=args.inside,
        )
        if args.brute_den:
            bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))
        backend_used = backend_name
    else:
        # GPU path: CuPy / PyTorch / auto-detected numpy
        results, backend_used = parametric_search_gpu(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            progress=True,
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

    # ── Summary ───────────────────────────────────────────────────────────
    count_by_n: dict[int, int] = {}
    for pt in results:
        count_by_n[pt.rational_count] = count_by_n.get(pt.rational_count, 0) + 1

    print(f"\n{'─'*72}")
    if dedup_sym:
        print(f"Found {raw_count} points → {len(results)} orbits after D4 dedup  ({elapsed:.2f}s)")
    else:
        print(f"Found {len(results)} unique points in {elapsed:.2f}s")
    print(f"Sorted by: rational_count DESC, denominator ASC")
    for n in sorted(count_by_n, reverse=True):
        marker = " ◄ 4-VERTEX SOLUTION!" if n == 4 else ""
        print(f"  {count_by_n[n]:6d}  points with {n}/4 rational distances{marker}")
    print(f"{'─'*72}\n")

    # ── Table ─────────────────────────────────────────────────────────────
    display = results if args.top == 0 else results[: args.top]
    print(_header())
    print("─" * 85)
    for pt in display:
        print(_row(pt))
    if args.top and len(results) > args.top:
        print(f"  … {len(results) - args.top} more rows omitted (use --top 0 to see all)")

    # ── 4-vertex highlight ────────────────────────────────────────────────
    four = [pt for pt in results if pt.rational_count == 4]
    if four:
        print(f"\n{'!'*72}")
        print(f"  {len(four)} POINT(S) WITH ALL FOUR RATIONAL DISTANCES:")
        for pt in four:
            print(f"  {pt}")
        print(f"{'!'*72}")
    else:
        if args.min_rational <= 3:
            print("\n(No 4-vertex solutions found in this search range.)")

    # ── JSON output ───────────────────────────────────────────────────────
    if args.out:
        out_path = Path(args.out)
        payload = {
            "backend": backend_used,
            "search_params": vars(args),
            "elapsed_seconds": round(elapsed, 3),
            "total_found": len(results),
            "count_by_rational": {str(k): v for k, v in count_by_n.items()},
            "points": [pt.as_dict() for pt in results],
        }
        out_path.write_text(json.dumps(payload, indent=2))
        print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
