"""A.9 closure-necessity — what linear relation must two concordant N satisfy?

Background
----------
The pipeline's chain-closure test
(`analysis.check_chain_compatibility`, `chain_closure_sieve.killed_at_modulus`)
asks only whether two concordant values satisfy the **sum** relation

    N1 + N2 = A + B          (partner  b = A + B - N  is also concordant).

This worklog (wl093) shows that the sum relation is the *inside-the-unit-square*
case of a more general necessary condition, and that a Harborth counterexample
located **outside** the square satisfies one of three other linear relations
that the current sieve never checks.

Geometry (see derivation in wl093 / MATH.md §3, §7)
---------------------------------------------------
A Harborth counterexample is a rational point P = (x, y) at rational distance to
all four corners of the unit square.  Write x = u/n, y = v/n with integers
u, v, n (n > 0, n = common denominator).  The four squared corner distances,
cleared of denominators, are

    u^2     + v^2     = []      (corner (0,0))
    (u-n)^2 + v^2     = []      (corner (1,0))
    (u-n)^2 + (v-n)^2 = []      (corner (1,1))
    u^2     + (v-n)^2 = []      (corner (0,1))

Set the two *horizontal* legs (A, B) := (|u|, |u-n|) and the two *vertical* legs
(N1, N2) := (|v|, |v-n|).  Then **both** N1 and N2 are concordant for (A, B)
(each combination above is a perfect square), and a short case analysis on the
sign of u (resp. v) gives

    |u| + |u-n| = n   if 0 <= u <= n,   else   | |u| - |u-n| | = n,

i.e. exactly one of {A+B, |A-B|} equals n, and likewise exactly one of
{N1+N2, |N1-N2|} equals n.  Hence the common scale n lies in

    {A + B, |A - B|}  ∩  {N1 + N2, |N1 - N2|}  != empty.        (GEN-CLOSURE)

* P inside the square (0<=x<=1, 0<=y<=1)  <=>  A+B = n = N1+N2  (the SUM
  relation the pipeline already checks).
* P outside the square  =>  one of the three relations
      |N1 - N2| = A + B,   N1 + N2 = |A - B|,   |N1 - N2| = |A - B|
  holds instead — none of which the current sieve tests.

Consequence
-----------
"all concordant N fail N1+N2=A+B" only rules out *inside-square* counterexamples.
The complete, all-ranks, Magma-free necessary-and-sufficient closure test for a
reduced pair (A, B) is GEN-CLOSURE over the (finite, exhaustively enumerated)
concordant set.  This script verifies:
  (1) the region/leg algebra on sampled rational points (sanity);
  (2) GEN-CLOSURE finds **zero** counterexamples over all safe-pass pairs up to
      a small max_hyp — strengthening the no-counterexample evidence from
      "inside square" to the whole plane;
  (3) the residual hard_cases tabulated against all four relations.

Run:
    PYTHONPATH=src uv run python scripts/theory/closure_necessity_relations.py --max-hyp 500
"""

from __future__ import annotations

import argparse
import time

from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


# --------------------------------------------------------------------------
# (1) region / leg algebra sanity check
# --------------------------------------------------------------------------
def region_label(u: int, n: int) -> str:
    if 0 <= u <= n:
        return "in"
    return "out"


def axis_relation(u: int, n: int) -> tuple[str, int]:
    """Which of {sum, diff} of the two legs (|u|, |u-n|) equals n."""
    h0, h1 = abs(u), abs(u - n)
    if h0 + h1 == n:
        return "sum", n
    assert abs(h0 - h1) == n
    return "diff", n


def check_region_algebra() -> bool:
    """For sampled (u, v, n), confirm exactly one of {sum,diff}=n per axis and
    that the matching relation type matches inside/outside the strip."""
    ok = True
    samples = [
        (3, 4, 10),  # both inside
        (13, 4, 10),  # u outside (right), v inside
        (3, 14, 10),  # u inside, v outside (above)
        (-2, 14, 10),  # both outside
        (5, 5, 10),  # vertical center line (v = n/2)
    ]
    for u, v, n in samples:
        rh, _ = axis_relation(u, n)
        rv, _ = axis_relation(v, n)
        exp_h = "sum" if region_label(u, n) == "in" else "diff"
        exp_v = "sum" if region_label(v, n) == "in" else "diff"
        match = rh == exp_h and rv == exp_v
        ok = ok and match
        print(
            f"  u={u:>4} v={v:>4} n={n}: "
            f"horiz={rh:<4}({region_label(u,n)}) vert={rv:<4}({region_label(v,n)})  "
            f"{'ok' if match else 'MISMATCH'}"
        )
    return ok


# --------------------------------------------------------------------------
# (2) generalized closure decider
# --------------------------------------------------------------------------
def generalized_closure(A: int, B: int, ns: list[int]) -> list[tuple[int, int, str]]:
    """Return all (Ni, Nj, relation) where {Ni+Nj,|Ni-Nj|} meets {A+B,|A-B|}.

    Allows i == j (the center-line case 2N = target).  The four relations:
        N1 + N2 == A + B   (SUM=SUM, inside square — current pipeline test)
        |N1 - N2| == A + B (DIFF=SUM)
        N1 + N2 == |A - B| (SUM=DIFF)
        |N1 - N2| == |A - B| (DIFF=DIFF)
    """
    targets = {A + B, abs(A - B)}
    hits: list[tuple[int, int, str]] = []
    m = len(ns)
    for i in range(m):
        for j in range(i, m):
            s = ns[i] + ns[j]
            d = abs(ns[i] - ns[j])
            if s in targets:
                rel = "sum=A+B" if s == A + B else "sum=|A-B|"
                hits.append((ns[i], ns[j], rel))
            if i != j and d in targets and d > 0:
                rel = "diff=A+B" if d == A + B else "diff=|A-B|"
                hits.append((ns[i], ns[j], rel))
    return hits


def sum_closure_only(A: int, B: int, ns: list[int]) -> bool:
    """The pipeline's current test: exists Ni, Nj (i<=j) with Ni+Nj == A+B."""
    s = A + B
    sset = set(ns)
    return any((s - n) in sset and (s - n) > 0 for n in ns)


def scan(max_hyp: int) -> dict:
    t0 = time.perf_counter()
    n_pairs = 0
    n_multi = 0
    sum_hits: list[tuple[int, int]] = []
    gen_hits: list[tuple[int, int, list[tuple[int, int, str]]]] = []
    rel_counts: dict[str, int] = {}
    for a, b in generate_ab_pairs(max_hyp):
        if not allow_reduced_pair(a, b):
            continue
        n_pairs += 1
        ns = find_concordant_by_factorization(a, b)
        if len(ns) >= 2:
            n_multi += 1
        if sum_closure_only(a, b, ns):
            sum_hits.append((a, b))
        hits = generalized_closure(a, b, ns)
        # exclude the trivial sum=A+B that equals the pipeline test? keep all,
        # but tally relation types that are NEW (not sum=A+B).
        new_hits = [h for h in hits if h[2] != "sum=A+B"]
        for _, _, rel in hits:
            rel_counts[rel] = rel_counts.get(rel, 0) + 1
        if new_hits:
            gen_hits.append((a, b, new_hits))
    return {
        "elapsed_ms": (time.perf_counter() - t0) * 1000.0,
        "n_pairs": n_pairs,
        "n_multi": n_multi,
        "sum_closure_pairs": sum_hits,
        "new_relation_pairs": gen_hits,
        "relation_counts": rel_counts,
    }


def residual_hard_cases(max_hyp: int) -> list[tuple[int, int, list[int]]]:
    out = []
    for a, b in generate_ab_pairs(max_hyp):
        if not allow_reduced_pair(a, b):
            continue
        ns = find_concordant_by_factorization(a, b)
        if len(ns) >= 2 and not sum_closure_only(a, b, ns):
            out.append((a, b, ns))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-hyp", type=int, default=500)
    args = ap.parse_args()

    print("== (1) region / leg-relation algebra sanity ==")
    ok = check_region_algebra()
    print(f"  all samples consistent: {ok}\n")

    print(f"== (2) generalized closure scan, max_hyp={args.max_hyp} ==")
    res = scan(args.max_hyp)
    print(f"  safe-pass pairs: {res['n_pairs']}  (multi-N: {res['n_multi']})")
    print(f"  elapsed: {res['elapsed_ms']:.1f} ms")
    print(f"  pairs with SUM closure (N1+N2=A+B, pipeline test): {len(res['sum_closure_pairs'])}")
    print(f"  relation hit counts (incl. i==j): {res['relation_counts']}")
    print(
        "  pairs hitting a NON-sum relation "
        f"(would be a counterexample outside the square): {len(res['new_relation_pairs'])}"
    )
    for a, b, hits in res["new_relation_pairs"]:
        print(f"    ({a},{b}): {hits}")

    print("\n== (3) residual hard_cases (>=2 concordant N, sum-closure fails) ==")
    print("   tabulated against all four linear relations:")
    hard = residual_hard_cases(args.max_hyp)
    print(f"   {'(A,B)':>16} {'A+B':>7} {'|A-B|':>7}  concordant_N -> sums / |diffs|")
    for a, b, ns in hard:
        m = len(ns)
        sums = sorted({ns[i] + ns[j] for i in range(m) for j in range(i, m)})
        diffs = sorted({abs(ns[i] - ns[j]) for i in range(m) for j in range(m) if i != j})
        flag = "  CLOSES!" if generalized_closure(a, b, ns) else ""
        label = f"({a},{b})"
        print(f"   {label:>16} {a+b:>7} {abs(a-b):>7}  N={ns} sums={sums} diffs={diffs}{flag}")
    print(f"\n   total residual hard_cases: {len(hard)} ; any closing under GEN-CLOSURE: "
          f"{any(generalized_closure(a, b, ns) for a, b, ns in hard)}")


if __name__ == "__main__":
    main()
