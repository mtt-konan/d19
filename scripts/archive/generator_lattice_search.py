#!/usr/bin/env python3
"""X1: Generator lattice search on rank>=1 hard_case (wl043 direction).

For each (A, B) hard_case with rank >= 1, take PARI's generator(s) and
enumerate lattice combinations kP (rank=1) or aP + bQ (rank=2) up to
some cap. For each combination, check whether the X-coordinate is a
rational square X = N^2 with integer N, then test full chain closure.

Three outcome classes per lattice point:
  - X not rational square            (skip)
  - X = N^2 rational but N not integer  (record, partial-concordant pattern)
  - X = N^2 integer:
      - N^2+A^2 / N^2+B^2 both squares -> concordant pair (rare and interesting)
      - chain closure (b=N-A>0 and b^2+A^2 / b^2+B^2 both squares) -> COUNTEREXAMPLE

Output: JSONL with one row per hard_case, listing all lattice points
that hit X-rational-square plus their chain-closure status.

This is the first construction-side search in d19 (all previous methods
were obstruction-side).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import cypari2

ROOT = Path(__file__).parent.parent.parent


def is_perfect_square(n: int) -> tuple[bool, int]:
    if n < 0:
        return False, -1
    r = math.isqrt(n)
    return r * r == n, r


def check_chain_closure(N: int, A: int, B: int) -> dict[str, Any]:
    """Check whether N gives a valid chain closure for (A, B)."""
    out: dict[str, Any] = {"N": N}
    n2_pa2 = N * N + A * A
    n2_pb2 = N * N + B * B
    ok1, h3 = is_perfect_square(n2_pa2)
    ok2, h4 = is_perfect_square(n2_pb2)
    out["concordant"] = ok1 and ok2
    if ok1:
        out["h3"] = h3
    if ok2:
        out["h4"] = h4
    if not (ok1 and ok2):
        return out

    b = N - A
    out["b"] = b
    if b <= 0:
        out["chain_closes"] = False
        out["chain_reason"] = "b<=0"
        return out

    b2_pa2 = b * b + A * A
    b2_pb2 = b * b + B * B
    ok3, h5 = is_perfect_square(b2_pa2)
    ok4, h6 = is_perfect_square(b2_pb2)
    out["chain_closes"] = ok3 and ok4
    if ok3:
        out["h5"] = h5
    if ok4:
        out["h6"] = h6
    if not ok3:
        out["chain_reason"] = "b^2+A^2 not square"
    elif not ok4:
        out["chain_reason"] = "b^2+B^2 not square"
    else:
        out["chain_reason"] = "FULL CHAIN CLOSES"
    return out


def check_point_X(pari: Any, kP: Any, A: int, B: int, k_label: str,
                  max_N: int) -> dict[str, Any] | None:
    """Inspect X-coord of an EC point. Return finding dict iff X is a rational square."""
    if kP == 0 or str(kP) == "[0]":
        return None
    X = kP[0]
    try:
        num = int(pari.numerator(X))
        den = int(pari.denominator(X))
    except Exception:
        return None
    if num <= 0 or den <= 0:
        return None
    ok_num, n_num = is_perfect_square(num)
    ok_den, n_den = is_perfect_square(den)
    if not (ok_num and ok_den) or n_den == 0:
        return None

    if n_num % n_den != 0:
        return {"k": k_label,
                "X_is_square": True,
                "N_numerator": n_num, "N_denominator": n_den,
                "comment": "N rational, not integer"}
    N = n_num // n_den
    if N <= 0 or N > max_N * 100:  # allow some slack beyond max_hyp
        return None
    chain = check_chain_closure(N, A, B)
    chain["k"] = k_label
    return chain


def lattice_search(pari: Any, A: int, B: int,
                   K1_max: int, K2_max: int, effort: int = 2) -> dict[str, Any]:
    """Run lattice search on E_{A,B}; auto-handle rank 1 / 2 / >=3."""
    t0 = time.perf_counter()
    E = pari(f"ellinit([0, {A*A + B*B}, 0, {A*A * B*B}, 0])")
    try:
        rank_info = pari.ellrank(E, effort)
    except Exception as exc:
        return {"A": A, "B": B, "error": f"ellrank failed: {exc}",
                "time_s": round(time.perf_counter() - t0, 3)}

    rank_lo = int(rank_info[0])
    rank_hi = int(rank_info[1])
    gens = rank_info[3]
    n_gens = len(gens)
    max_N = max(A + B, 20000)  # search slightly beyond max_hyp

    out: dict[str, Any] = {
        "A": A, "B": B, "rank_lower": rank_lo, "rank_upper": rank_hi,
        "n_gens_returned": n_gens,
        "K1_max": K1_max if n_gens >= 1 else 0,
        "K2_max": K2_max if n_gens >= 2 else 0,
    }

    if n_gens == 0 or rank_lo == 0:
        out["error"] = "no generator from PARI"
        out["time_s"] = round(time.perf_counter() - t0, 3)
        return out

    findings: list[dict[str, Any]] = []

    if n_gens == 1:
        P = gens[0]
        for k in range(1, K1_max + 1):
            kP = pari.ellmul(E, P, k)
            f = check_point_X(pari, kP, A, B, str(k), max_N)
            if f is not None:
                findings.append(f)
    else:
        # rank >= 2: enumerate aP + bQ for |a|, |b| <= K2_max
        P, Q = gens[0], gens[1]
        for a in range(-K2_max, K2_max + 1):
            for b in range(-K2_max, K2_max + 1):
                if a == 0 and b == 0:
                    continue
                try:
                    aP = pari.ellmul(E, P, a) if a != 0 else None
                    bQ = pari.ellmul(E, Q, b) if b != 0 else None
                    if aP is None:
                        R = bQ
                    elif bQ is None:
                        R = aP
                    else:
                        R = pari.elladd(E, aP, bQ)
                except Exception:
                    continue
                f = check_point_X(pari, R, A, B, f"({a},{b})", max_N)
                if f is not None:
                    findings.append(f)

    out["findings"] = findings
    out["n_findings"] = len(findings)
    out["n_concordant"] = sum(1 for f in findings if f.get("concordant"))
    out["n_chain_closes"] = sum(1 for f in findings if f.get("chain_closes"))
    out["time_s"] = round(time.perf_counter() - t0, 3)
    return out


def load_hard_cases(jsonl_path: Path,
                    min_rank: int = 1) -> list[tuple[int, int, int]]:
    rows: list[tuple[int, int, int]] = []
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rank_lo = r.get("rank_lower")
            if isinstance(rank_lo, int) and rank_lo >= min_rank:
                rows.append((int(r["A"]), int(r["B"]), rank_lo))
    rows.sort()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path",
                    default="results/ell2cover_10k.jsonl",
                    help="hard_case JSONL (default: %(default)s)")
    ap.add_argument("--out", default="results/generator_lattice_10k.jsonl")
    ap.add_argument("--K1-max", type=int, default=50,
                    help="rank=1: enumerate kP for k in [1, K1_max]")
    ap.add_argument("--K2-max", type=int, default=5,
                    help="rank>=2: enumerate aP+bQ for |a|,|b| <= K2_max")
    ap.add_argument("--effort", type=int, default=2,
                    help="PARI ellrank effort (need stable generator)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--progress-every", type=int, default=20)
    args = ap.parse_args()

    in_path = ROOT / args.in_path if not Path(args.in_path).is_absolute() \
        else Path(args.in_path)
    out_path = ROOT / args.out if not Path(args.out).is_absolute() \
        else Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = load_hard_cases(in_path, min_rank=1)
    if args.limit:
        rows = rows[: args.limit]

    pari = cypari2.Pari()
    pari.allocatemem(512 * 1024 * 1024)

    print(f"input:  {in_path}")
    print(f"output: {out_path}")
    print(f"rank>=1 cases: {len(rows)}  "
          f"K1_max={args.K1_max}  K2_max={args.K2_max}  effort={args.effort}")
    print()

    t_start = time.perf_counter()
    n_concordant_hits = 0
    n_chain_closes = 0
    n_with_X_square = 0

    with open(out_path, "w", encoding="utf-8") as fh:
        for idx, (A, B, rank_lo) in enumerate(rows, 1):
            result = lattice_search(pari, A, B, args.K1_max, args.K2_max,
                                    effort=args.effort)
            fh.write(json.dumps(result) + "\n")
            fh.flush()

            n_f = result.get("n_findings", 0)
            n_c = result.get("n_concordant", 0)
            n_cl = result.get("n_chain_closes", 0)
            if n_f > 0:
                n_with_X_square += 1
            n_concordant_hits += n_c
            n_chain_closes += n_cl

            if n_cl > 0:
                print(f"*** COUNTEREXAMPLE: A={A}, B={B} ***")
                print(f"  {result}")

            if idx % args.progress_every == 0 or idx == len(rows):
                elapsed = time.perf_counter() - t_start
                rate = idx / elapsed if elapsed > 0 else 0
                eta = (len(rows) - idx) / rate if rate > 0 else float("inf")
                print(
                    f"[{idx:>4}/{len(rows)}] {elapsed:>5.0f}s  "
                    f"{rate:>5.2f}/s  ETA {eta:>5.0f}s  "
                    f"with_X_sq:{n_with_X_square}  "
                    f"concordant:{n_concordant_hits}  "
                    f"chain:{n_chain_closes}",
                    flush=True,
                )

    elapsed = time.perf_counter() - t_start
    print()
    print("=" * 60)
    print(f"Done. {len(rows)} cases in {elapsed:.0f}s.")
    print(f"  cases with >=1 X-rational-square point: {n_with_X_square}")
    print(f"  total concordant hits (N integer + 2 squares): {n_concordant_hits}")
    print(f"  total CHAIN CLOSES: {n_chain_closes}")
    print(f"  output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
