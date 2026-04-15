"""Rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1).

Single entry point supporting five complementary search methods:

  parametric   Parametric brute-force search (GPU / CPU multiprocessing)
  ec           Elliptic-curve guided search (chord-tangent orbit expansion)
  chain        Pythagorean 4-cycle search (generalised rectangle problem)
  chain-fast   O(n²) primitive-triple-pair 4-cycle search (unit-square only)
  concordant   EC concordant-form analysis of chain (A,B) pairs

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
CHAIN METHOD
──────────────────────────────────────────────────────────────────────────
Searches for integer 4-tuples (a,b,c,d) where each consecutive pair forms
a Pythagorean triple (a²+b², b²+c², c²+d², d²+a² are all perfect squares).
This is the generalised rectangle problem.  When a+c == b+d == k the point
(a/k, b/k) has rational distances to all four corners of the unit square.

  uv run python scripts/search.py chain --max-val 200
  uv run python scripts/search.py chain --max-val 500 --require-square
  uv run python scripts/search.py chain --max-val 1000 --out chain.json

──────────────────────────────────────────────────────────────────────────
CHAIN-FAST METHOD
──────────────────────────────────────────────────────────────────────────
O(n²) search over primitive-triple pairs.  For each ordered pair (T1, T2)
of primitive triples with hypotenuse ≤ max_hyp, derives the unique 4-cycle
candidate satisfying a+c=b+d and verifies two perfect-square conditions.
All results satisfy the unit-square constraint by construction.

  uv run python scripts/search.py chain-fast --max-hyp 200
  uv run python scripts/search.py chain-fast --max-hyp 1000 --out fast.json

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


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments shared by both subcommands."""
    parser.add_argument(
        "--min-rational",
        type=int,
        default=3,
        choices=[3, 4],
        help="Minimum rational distances to report (default: 3)",
    )
    parser.add_argument(
        "--inside",
        action="store_true",
        help="Only return points strictly inside the unit square (0<x<1, 0<y<1)",
    )
    parser.add_argument("--out", type=str, default=None, help="Write JSON results to this file")
    parser.add_argument(
        "--top", type=int, default=50, help="Max rows to print (0=all, default: 50)"
    )
    parser.add_argument("--no-progress", action="store_true", help="Suppress the progress bar")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="search.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="method", metavar="METHOD")
    sub.required = True

    p = sub.add_parser(
        "parametric",
        help="Parametric brute-force search (GPU / CPU multiprocessing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Parametric brute-force search over Pythagorean triples and scale factors.",
    )
    p.add_argument(
        "--scale",
        type=int,
        default=None,
        help="Shorthand default: max_m=N, max_k_den=4N, max_k_num=8N",
    )
    p.add_argument(
        "--max-m",
        type=int,
        default=None,
        help="Max m for Pythagorean triple generation (default: 80; overrides --scale)",
    )
    p.add_argument(
        "--max-k-num",
        type=int,
        default=None,
        help="Max numerator of scale k=a/b (default: 640; overrides --scale)",
    )
    p.add_argument(
        "--max-k-den",
        type=int,
        default=None,
        help="Max denominator of scale k=a/b (default: 320; overrides --scale)",
    )
    p.add_argument(
        "--backend",
        type=str,
        default="auto",
        choices=["auto", "cupy", "torch", "numpy"],
        help="Compute backend: auto|cupy|torch|numpy (default: auto)",
    )
    p.add_argument(
        "--workers", type=int, default=0, help="CPU worker processes for numpy backend (0=auto)"
    )
    p.add_argument(
        "--brute-den",
        type=int,
        default=0,
        help="Also run brute-force search up to this denominator (0=skip)",
    )
    p.add_argument(
        "--no-dedup-symmetry",
        action="store_true",
        help="Show all D4 symmetric copies (default: one per orbit)",
    )
    _add_common_args(p)

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
    e.add_argument(
        "--max-m",
        type=int,
        default=30,
        help="Max m for Pythagorean triple generation (default: 30)",
    )
    e.add_argument(
        "--max-k-num",
        type=int,
        default=400,
        help="Max numerator for seed search k=a/b (default: 400)",
    )
    e.add_argument(
        "--max-k-den",
        type=int,
        default=800,
        help="Max denominator for seed search k=a/b (default: 800)",
    )
    e.add_argument(
        "--max-steps",
        type=int,
        default=20,
        help="Max chord-tangent expansion steps per orbit (default: 20)",
    )
    e.add_argument(
        "--backend",
        type=str,
        default="auto",
        choices=["auto", "cupy", "torch", "numpy"],
        help="Backend for seed finding: auto|cupy|torch|numpy (default: auto)",
    )
    e.add_argument("--db", type=str, default=None, help="Persist this EC run to a SQLite database")
    e.add_argument(
        "--resume",
        action="store_true",
        help="Resume the latest EC database run with the same search parameters",
    )
    _add_common_args(e)

    c = sub.add_parser(
        "chain",
        help="Pythagorean 4-cycle search (generalised rectangle / unit-square problem)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Find integer 4-tuples (a,b,c,d) where a²+b², b²+c², c²+d², d²+a²\n"
            "are all perfect squares (each consecutive pair is a Pythagorean triple).\n"
            "Without --require-square these are generalised rectangle solutions;\n"
            "with --require-square (a+c == b+d) only unit-square candidates are shown.\n\n"
            "Examples:\n"
            "  uv run python scripts/search.py chain\n"
            "  uv run python scripts/search.py chain --max-val 1000\n"
            "  uv run python scripts/search.py chain --max-val 2000 --out chain.json\n"
            "  uv run python scripts/search.py chain --max-val 5000 --require-square"
        ),
    )
    c.add_argument(
        "--max-val",
        type=int,
        default=500,
        help="Upper bound for all four integers a,b,c,d (default: 500)",
    )
    c.add_argument(
        "--require-square",
        action="store_true",
        help="Only report solutions where a+c == b+d (unit-square constraint)",
    )
    c.add_argument("--out", type=str, default=None, help="Write JSON results to this file")
    c.add_argument("--top", type=int, default=50, help="Max rows to print (0=all, default: 50)")
    c.add_argument("--no-progress", action="store_true", help="Suppress the progress bar")

    cf = sub.add_parser(
        "chain-fast",
        help="O(n²) primitive-triple-pair 4-cycle search (unit-square only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "O(n²) search over all ordered pairs of primitive Pythagorean triples\n"
            "(T1, T2) with hypotenuse ≤ max_hyp.  For each pair, derives the unique\n"
            "4-cycle candidate satisfying a+c=b+d and checks two perfect-square\n"
            "conditions.  All results satisfy the unit-square constraint by construction.\n\n"
            "Solution values (a,b,c,d) can be as large as O(max_hyp²).\n\n"
            "Examples:\n"
            "  uv run python scripts/search.py chain-fast --max-hyp 200\n"
            "  uv run python scripts/search.py chain-fast --max-hyp 1000 --profile\n"
            "  uv run python scripts/search.py chain-fast --max-hyp 1000 --out fast.json"
        ),
    )
    cf.add_argument(
        "--max-hyp",
        type=int,
        default=500,
        help="Max hypotenuse of primitive triples T1, T2 (default: 500)",
    )
    cf.add_argument("--out", type=str, default=None, help="Write JSON results to this file")
    cf.add_argument("--top", type=int, default=50, help="Max rows to print (0=all, default: 50)")
    cf.add_argument("--no-progress", action="store_true", help="Suppress the progress bar")
    cf.add_argument(
        "--backend",
        choices=["auto", "numpy", "python"],
        default="auto",
        help="Computation backend (default: auto — uses numpy if available)",
    )
    cf.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Worker processes for chain-fast (0=auto, default: 0)",
    )
    cf.add_argument(
        "--db",
        type=str,
        default=None,
        metavar="PATH",
        help="SQLite database path for persistence (enables resume + near-miss logging)",
    )
    cf.add_argument(
        "--resume",
        action="store_true",
        help="Resume the last incomplete run in --db (requires --db)",
    )
    cf.add_argument(
        "--near-miss",
        action="store_true",
        dest="near_miss",
        help="Log C3-pass/C4-fail pairs to --db for proximity analysis (requires --db)",
    )
    cf.add_argument(
        "--near-miss-limit",
        type=int,
        default=100000,
        help="Max near-miss rows kept per run when --near-miss is enabled (default: 100000)",
    )
    cf.add_argument(
        "--profile",
        action="store_true",
        help="Collect and print chain-fast timing/count profile; also persist it when --db is set",
    )
    cf.add_argument(
        "--bucket-stats",
        action="store_true",
        help="Collect aggregated structural bucket stats and persist them to --db",
    )
    cf.add_argument(
        "--mod-sieve",
        action="store_true",
        help="Experimental C3 pre-sieve using fixed small moduli (16,3,5,7)",
    )
    cf.add_argument(
        "--safe-pair-sieve",
        action="store_true",
        help="Experimental proved-safe pair sieve (python backend only)",
    )

    co = sub.add_parser(
        "concordant",
        help="Elliptic curve concordant-form analysis of chain (A,B) pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Analyse (A,B) pairs from the chain parameterisation using elliptic\n"
            "curves.  For each pair, searches for concordant integers N where\n"
            "N²+A²=□ and N²+B²=□, then checks chain compatibility.\n\n"
            "Examples:\n"
            "  uv run python scripts/search.py concordant --max-hyp 100\n"
            "  uv run python scripts/search.py concordant --max-hyp 500 --ec-bound 500000\n"
            "  uv run python scripts/search.py concordant --pair 264,420\n"
            "  uv run python scripts/search.py concordant --pair 264,420 --deep 10"
        ),
    )
    co.add_argument(
        "--max-hyp",
        type=int,
        default=100,
        help="Max hypotenuse for triple-pair generation (default: 100)",
    )
    co.add_argument(
        "--ec-bound",
        type=int,
        default=100000,
        help="Bound for ellratpoints search (default: 100000)",
    )
    co.add_argument(
        "--pair",
        type=str,
        default=None,
        help="Analyse a single A,B pair (e.g. --pair 264,420)",
    )
    co.add_argument(
        "--deep",
        type=int,
        default=0,
        help="Generator multiple depth for deep search (0=off, default: 0)",
    )
    co.add_argument(
        "--profile",
        action="store_true",
        help="Collect and print concordant timing/count profile",
    )
    co.add_argument("--out", type=str, default=None, help="Write JSON report to this file")
    co.add_argument("--top", type=int, default=20, help="Max rows to print (0=all, default: 20)")
    co.add_argument("--no-progress", action="store_true", help="Suppress the progress bar")

    return parser


__all__ = ["build_parser"]
