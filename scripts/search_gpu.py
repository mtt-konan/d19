"""GPU-accelerated rational distance search — AMD Ryzen AI Max / RTX 4090 / CPU.

Requires CuPy (preferred) or PyTorch with ROCm/CUDA backend.
Falls back to NumPy (CPU) automatically if no GPU is found.

Install for AMD Ryzen AI Max+ 392 (ROCm)
─────────────────────────────────────────
  # Check your ROCm version first:  rocminfo | grep -i version
  pip install cupy-rocm-6-0       # ROCm 6.x pre-built wheel

  # If ROCm 7.0 (no pre-built CuPy wheel yet — build from source):
  sudo apt install rocm-dev hipcc
  HIP_PATH=/opt/rocm pip install cupy --no-build-isolation

  # PyTorch ROCm fallback (usually simpler to install):
  pip install torch --index-url https://download.pytorch.org/whl/rocm6.2

Install for NVIDIA RTX 4090 (CUDA)
───────────────────────────────────
  pip install cupy-cuda12x

Usage
─────
  uv run python scripts/search_gpu.py --scale 200
  uv run python scripts/search_gpu.py --scale 80 --backend numpy  # CPU test
  uv run python scripts/search_gpu.py --help
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.search import dedup_by_symmetry
from rational_distance.search_gpu import detect_backend, parametric_search_gpu
from rational_distance.square import RationalPoint


# ── Formatting (same as search_3vertex.py) ───────────────────────────────────

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
                        help="Set max_m=N, max_k_den=4N, max_k_num=8N at once")
    parser.add_argument("--max-m",        type=int,  default=80)
    parser.add_argument("--max-k-num",    type=int,  default=640)
    parser.add_argument("--max-k-den",    type=int,  default=320)
    parser.add_argument("--min-rational", type=int,  default=3, choices=[2, 3, 4])
    parser.add_argument("--backend",      type=str,  default="auto",
                        choices=["auto", "cupy", "torch", "numpy"],
                        help="Force a specific compute backend (default: auto)")
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

    # ── Select backend ────────────────────────────────────────────────────
    xp = None
    if args.backend == "numpy":
        import numpy as np
        xp = np
        forced_name = "NumPy (CPU, forced)"
    elif args.backend == "cupy":
        import cupy as cp
        xp = cp
        forced_name = None
    elif args.backend == "torch":
        from rational_distance.search_gpu import _try_torch
        xp = _try_torch()
        if xp is None:
            print("ERROR: PyTorch ROCm/CUDA not available.", file=sys.stderr)
            sys.exit(1)
        forced_name = None

    # ── Banner ────────────────────────────────────────────────────────────
    print("=" * 72)
    print("GPU rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1)")

    if xp is None:
        _, backend_name, is_gpu = detect_backend()
        print(f"  backend  : {backend_name}")
        if not is_gpu:
            print("  [!] No GPU found — running on CPU.  Install CuPy or PyTorch+ROCm.")
    else:
        if args.backend == "numpy":
            backend_name = forced_name
        else:
            backend_name = f"forced:{args.backend}"
        print(f"  backend  : {backend_name}")

    print(f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den},",
          f"min_rational={args.min_rational}")
    est = _size_estimate(args.max_m, args.max_k_num, args.max_k_den)
    print(f"  search space ≈ {est} (triple × k combinations)")
    print("=" * 72)

    dedup_sym = not args.no_dedup_symmetry

    t0 = time.perf_counter()

    results, backend_used = parametric_search_gpu(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        min_rational=args.min_rational,
        progress=True,
        xp=xp,
    )

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
