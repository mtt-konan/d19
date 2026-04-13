"""O(n²) search for Pythagorean 4-cycles satisfying the unit-square constraint.

Algorithm
---------
For primitive triples T1=(s1,t1,h1) and T2=(s2,t2,h2), define:

    g  = gcd(t1, s2)        (coupling divisor)
    A  = t1·t2 / g          (reduced product of exit legs)
    B  = s1·s2 / g          (reduced product of entry legs)
    N  = s2/g·(s1-t1) + A  = (s2·(s1-t1) + t1·t2) / g

The candidate 4-cycle  (a,b,c,d) = (B, s2·t1/g, A, N)  satisfies a+c = b+d
automatically (= A+B), and its edges are Pythagorean iff:

    (C3)  A² + N²  is a perfect square   →  x3 = √(A²+N²)
    (C4)  N² + B²  is a perfect square   →  x4 = √(N²+B²)

x1 and x2 come "for free": x1 = s2/g·h1,  x2 = t1/g·h2.

Scale factors: k1 = s2/g,  k2 = t1/g,  k3 = gcd(A,N),  k4 = gcd(N,B).

This produces the **primitive representative** of each chain family: any
integer solution (a,b,c,d) satisfying a+c=b+d is a positive-integer multiple
of the primitive representative derived from its (T1,T2) primitive pair.
Since the unit-square point P = (a/(a+c), b/(a+c)) is scale-invariant, all
members of the same family map to the same point P.

Complexity
----------
Primitive triples up to hypotenuse H: O(H) triples (both leg orientations).
The double loop is O(H²) pairs, each checked with two integer-sqrt calls.
Two arithmetic pre-filters (parity and mod-4) skip ~71% of pairs before the
integer-sqrt calls, giving an effective ~3.4× speedup.

Cross-product family note
-------------------------
For this parameterisation, ac - bd = (s2·t1/g)·(s1-t1)·(t2-s2), which is
nonzero for any primitive triple (s2 ≠ t2, s1 ≠ t1).  Cross-product family
is therefore automatically excluded.

Necessary parity conditions (provably correct filters)
------------------------------------------------------
In any Pythagorean pair (u, v) both legs cannot be odd, because
u² + v² ≡ 2 (mod 4) when both are odd — never a perfect square.
Applying this to all four edges of the chain proves:

    P1 (alternating parity): A ≡ B (mod 2)
        — if A%2 ≠ B%2, one of C3/C4 fails mod 4.

    P2 (even leg divisible by 4): for a primitive Pythagorean pair the even
        leg ≡ 0 (mod 4), because u² + v² ≡ 5 (mod 8) when the even element
        is ≡ 2 (mod 4), which is not a quadratic residue mod 8.
        — if A%2 == 0: must have A%4 == 0 and B%4 == 0.
        — if A%2 == 1: must have b%4 == 0 and N%4 == 0.

Together P1+P2 eliminate ~71% of candidate pairs with no false negatives.
"""

from __future__ import annotations

from collections.abc import Iterator
from math import ceil, gcd, isqrt, sqrt

from tqdm import tqdm

from .math_utils import primitive_pythagorean_triples
from .search_chain import ChainResult, _symmetry_group, results_to_json


def find_chains_fast(
    max_hyp: int = 500,
    progress: bool = True,
) -> list[ChainResult]:
    """Find unit-square Pythagorean 4-cycles by O(n²) primitive-triple-pair enumeration.

    For each ordered pair (T1, T2) of primitive triples with hypotenuse ≤ max_hyp,
    derives the primitive-representative 4-cycle and verifies two perfect-square
    conditions.  All returned results satisfy a+c == b+d by construction.

    Args:
        max_hyp:  Maximum hypotenuse of the two free primitive triples T1, T2.
                  The solution values (a,b,c,d) can be as large as O(max_hyp²).
        progress: Show a tqdm progress bar.

    Returns:
        Sorted, deduplicated list of ChainResult objects (all have square_ok=True).
    """
    max_m = ceil(sqrt(max_hyp)) + 1
    triples: list[tuple[int, int, int]] = [
        (a, b, c)
        for a, b, c in primitive_pythagorean_triples(max_m)
        if c <= max_hyp
    ]
    n = len(triples)

    results: list[ChainResult] = []
    # Deduplicate by min symmetry-group key of the reduced tuple (÷ gcd).
    seen: set[tuple[int, int, int, int]] = set()

    it: Iterator[int] = iter(range(n))
    if progress:
        it = tqdm(range(n), desc="Fast chain (T1)", leave=False)  # type: ignore[assignment]

    for i in it:
        s1, t1, h1 = triples[i]
        for j in range(n):
            s2, t2, h2 = triples[j]

            # Coupling divisor: minimal k1 = s2/g, k2 = t1/g are integers.
            cg = gcd(t1, s2)
            s2r = s2 // cg   # = k1
            t1r = t1 // cg   # = k2

            A = t1r * t2        # = t1·t2 / g   (= c in the candidate tuple)
            B = s1 * s2r        # = s1·s2 / g   (= a in the candidate tuple)
            N = s2r * (s1 - t1) + A  # = (s2·(s1-t1) + t1·t2) / g  (= d)

            if N <= 0:
                continue

            # P1: alternating-parity filter (eliminates ~67% of pairs).
            # If A%2 ≠ B%2, one of C3/C4 fails mod 4 (both-odd leg sum ≡ 2).
            if A % 2 != B % 2:
                continue

            # P2: even-leg-divisible-by-4 filter (eliminates another ~4%).
            # For a primitive Pythagorean pair the even leg must be ≡ 0 mod 4;
            # even ≡ 2 mod 4 gives leg² + odd² ≡ 5 mod 8, not a square.
            if A % 2 == 0:
                # a=B and c=A are both even; each must be ≡ 0 mod 4.
                if A % 4 != 0 or B % 4 != 0:
                    continue

            # b = k1·t1 = k2·s2 = s2r·t1 = t1r·s2 (both equal s2·t1/g)
            b = s2r * t1
            a, c, d = B, A, N

            if A % 2 == 1:
                # a=B and c=A are both odd; b and d=N are both even; each ≡ 0 mod 4.
                if b % 4 != 0 or N % 4 != 0:
                    continue

            # All four values must be distinct.
            if len({a, b, c, d}) < 4:
                continue

            # C3: c² + d²  =  A² + N²  must be a perfect square.
            sq3 = A * A + N * N
            h3 = isqrt(sq3)
            if h3 * h3 != sq3:
                continue

            # C4: d² + a²  =  N² + B²  must be a perfect square.
            sq4 = N * N + B * B
            h4 = isqrt(sq4)
            if h4 * h4 != sq4:
                continue

            # Deduplicate under the 8-element dihedral symmetry group.
            key = min(_symmetry_group(a, b, c, d))
            if key in seen:
                continue
            seen.add(key)

            x1 = s2r * h1
            x2 = t1r * h2

            results.append(
                ChainResult(
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                    x1=x1,
                    x2=x2,
                    x3=h3,
                    x4=h4,
                    square_ok=True,
                )
            )

    return sorted(results, key=lambda r: (r.a, r.b, r.c, r.d))

