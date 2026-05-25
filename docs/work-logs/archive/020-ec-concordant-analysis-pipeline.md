# Work Log 020 — EC Concordant-Form Analysis Pipeline

## Summary

Completed the Weierstrass derivation for the concordant form problem that was
left incomplete in a prior conversation, discovered that the proposed rank filter
is empirically useless, and implemented an EC analysis pipeline as a research
tool (not a replacement for chain-fast search).

## Completed Weierstrass Derivation

The prior session attempted to transform Y²=(X²+A²)(X²+B²) to Weierstrass form
via a complicated substitution.  The correct approach is simpler:

**Setting X = N², Y = N·S·T** directly gives:

    Y² = N²(N²+A²)(N²+B²) = X(X+A²)(X+B²)

This is already Weierstrass form:

    E: Y² = X³ + (A²+B²)X² + A²B²X

No further transformation is needed.  The torsion subgroup is Z/2Z × Z/4Z:
- 2-torsion: (0,0), (-A²,0), (-B²,0)
- 4-torsion: (AB, ±AB(A+B))

## Critical Finding: Rank Filter Provides 0% Filtering

The proposed Module 2 (rank filter: discard pairs where rank=0) was tested on
ALL 2800 unique primitive (A,B) pairs from chain-fast with max_hyp=500:

    rank=0 count: 0  (zero!)
    filter rate:  0.0%

Every chain-generated (A,B) pair has rank ≥ 1.  Concordant N values exist
abundantly, but none satisfy the chain constraint C1+C2 simultaneously.

Example: (A=264, B=420), rank=2.  concordant N = {77, 315, 352}:
- N=77  → b=607: B²+b² not square, b²+A² not square
- N=315 → b=369: B²+b² not square, b²+A² not square
- N=352 → b=332: B²+b² not square, b²+A² not square

## cubic vs. concordant Distinction (rubber-duck finding)

X = N² on the Weierstrass curve does NOT guarantee concordant.
The curve only ensures (N²+A²)(N²+B²) is a square, not each factor separately.

Counterexample: A=1, B=4, N=2 → product=100=10², but 5 and 20 aren't squares.

Fix: after finding X=N², always verify isqrt(N²+A²) and isqrt(N²+B²).

## Architecture: EC as Analysis Tool, Not Search Accelerator

User's original 4-module architecture revised:

| Module | Original | Revised |
|--------|---------|---------|
| Data Generator | Euclid formula + hash map | Already exists (chain-fast) |
| Rank Filter | rank=0 → discard | USELESS (0% filter rate) |
| Deep Point Search | 100×P₁ expansion | Limited (heights grow as n²·ĥ(P)) |
| Distributed | BOINC | Local multiprocessing sufficient |

Practical generator-search depth: n ≤ 10 (not 100 as proposed).
Heights grow as ĥ(nP) = n²·ĥ(P), so X-coords have ~10,000 digits at n=100.

## Files Changed

- `src/rational_distance/concordant_ec.py` (new, 335 lines):
  `analyze_pair()`, `compute_rank()`, `find_concordant_integers()`,
  `check_chain_compatibility()`, `enumerate_multiples()`
- `src/rational_distance/pair_generator.py` (new, 49 lines):
  `generate_ab_pairs()` — deduplicated primitive (A,B) pairs from triple-pairs
- `scripts/search.py`: new `concordant` subcommand
- `tests/test_all.py`: 22 new tests (90 total)
- `docs/MATH.md`: Section 8 — EC concordant-form analysis
- `pyproject.toml`: `cypari2>=2.2.0` added

## Bugs Found and Fixed

1. `ellratpoints` returns `[X,Y]` point pairs, not alternating X,Y values.
2. `analyze_pair` was incorrectly normalizing (A,B) by gcd before concordant
   search — concordant N values are pair-specific, so normalization must be
   opt-in (normalize=False by default).
3. A=B case: curve E is singular (node at X=-A²) — special-cased with fallback.

## Commit

    f31673d  feat: add EC concordant-form analysis pipeline
