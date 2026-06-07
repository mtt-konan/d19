# Proof Leads

## Lead 1: Explain The `D_g=1` Layer

Observation:

```text
D_g = guaranteed divisor of every concordant N.
D_g=1 when gcd(A,B) is divisible by 12.
```

In this layer, the gcd-aware divisibility sieve has no force. The near-miss data says this is where most survivors live.

Possible lemma shape:

```text
Assume 12 | gcd(A,B), A < B, and A,B share at least two concordant N values.
Then the four full-plane closure values miss by a nonzero residue modulo some
quantity depending on A/12, B/12, or the shared Pythagorean factorization.
```

This is the best theorem target because it attacks the largest remaining hard core.

## Lead 2: Delta-1 Local Model

Model pair:

```text
(A,B) = (15960,61776)
gcd = 24
D_g = 1
N = [4950, 10368, 20007, 49280, 95095]
|95095 - 49280| = 45815
|A - B| = 45816
```

The miss is exactly `1`.

Suggested next work:

- Factor `A`, `B`, both witness `N` values, and the two hypotenuses.
- Ask whether the delta-1 miss is forced by parity, square classes, or a hidden congruence.
- Search for scaled or related pairs with the same pattern.

## Lead 3: Construct First, Then Test Squares

Instead of generating concordant `N` first, force a closure relation first:

```text
N2 = A + B - N1
N2 = |A - B| - N1
N2 = N1 + A + B
N2 = N1 + |A - B|
```

Then test whether both `N1` and `N2` satisfy:

```text
N_i^2 + A^2 = square
N_i^2 + B^2 = square
```

This route is attractive because the blind scan shows near misses are common, but exact equality is elusive.

The first constructive probe already found gap-1 rows with all four square checks true:

```text
(A,B,N1,N2) = (60,84,63,80)
N1 + N2 = 143
A + B = 144
```

This should be treated as a Diophantine template, not just a one-off sample.

## Lead 4: High-k Is Not Enough, But It Is Still A Lens

High `k` examples give many `N_i,N_j` pairs, yet the observed high-k rows still miss closure or are killed by modular obstruction.

Possible lemma shape:

```text
For high-k pairs in the dominant gcd strata, the concordant N values occupy
residue classes whose pairwise sums/differences avoid A+B and |A-B|.
```

This should be tested by collecting residue vectors for top high-k rows modulo small prime squares and modulo `g/12`.

## Lead 5: Full-Plane Relation Split

The closest-relation distribution among survivors is not dominated by a single relation. Both sum and difference forms appear.

This suggests proof attempts should keep all four relations until the last possible step. Any proof that only handles `N1+N2=A+B` is proving an inside-square statement, not the full target.

## Lead 6: Upgrade Partner Graph Delta

Old partner graph scans should be rerun with a full-plane delta helper:

```text
min over N_i,N_j and all four relations:
  |N_i+N_j-(A+B)|
  |N_i+N_j-|A-B||
  ||N_i-N_j|-(A+B)|
  ||N_i-N_j|-|A-B||
```

The first bounded recheck found no hit but did find delta-1 examples in all four relation families. That means the partner graph may still be a good near-miss generator after the old sum-only wording is fixed.

Follow-up status: completed for stored `G_M @ max_value=1M`.

```text
338,225 vertices
5,071,562 full-plane relation rows
0 full-plane hits
global min delta = 1
```

See `docs/explorations/2026-06-07-next-step-hard-layer/partner-full-plane-scan.md`.
