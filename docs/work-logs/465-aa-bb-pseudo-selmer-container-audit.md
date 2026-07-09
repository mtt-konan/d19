# AA+BB Pseudo-Selmer Container Audit

## Question

After `wl464`, can we avoid building the full complete 2-cover local matrix
until a cheaper upper-bound audit says it is necessary?

## Result

Yes. Define a pseudo-Selmer container

```text
S~ = S_tilde_AA_BB
```

in the complete 2-descent coordinates

```text
(d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q)
```

with product relation

```text
d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1.
```

The current evidence gives only:

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign.
```

So `S~` does **not** force `dim Sel_2(E)=2`.

## Quantifier Audit

The rows split as follows:

```text
wl457  mixed
       AA+BB kernel_neg_2sqrt_q has no odd-prime valuation support.
       Uses local image rows plus AA/BB primitive common-source intersection.

wl458  mixed
       AA+BB kernel_minus_p has no odd-prime valuation support.
       Uses local image rows plus disjointness of D_A and D_B.

wl459  mixed
       AA+BB kernel_pos_2sqrt_q has odd support only at ell | T, ell == 1 mod 4.
       Uses local image rows and leaves the shared T tail.

wl460  local-point
       Opposite-mod-4 dyadic branch forces x_minus_p in {1}.

wl461  local-point
       Same-mod-4 dyadic branch has local x_minus_p class 2.

wl462  local-common-source
       Same-mod-4 x_minus_p=2 is incompatible with the other two local kernel
       coordinates.

wl463  global-point-summary
       Genuine AA+BB rational points collapse to (1,1,1).
```

Only the local-point and local-common-source rows transfer directly to the
complete 2-descent Selmer membership row. The mixed odd-prime rows are still
usable in `S~`, but only as support bounds in an upper-bound container, not as
a proved exact local matrix.

## Container Definition

The container keeps:

```text
1. product relation,
2. kernel_minus_p odd-prime support trivial,
3. kernel_neg_2sqrt_q odd-prime support trivial,
4. kernel_pos_2sqrt_q odd-prime support inside ell | T, ell == 1 mod 4,
5. dyadic wl460-wl463 collapse of the 2-primary local common-source branch,
6. archimedean sign row as a possible one-dimensional tail.
```

By definition, `S~` is an upper-bound container for AA+BB common-source
Selmer-candidates: unresolved tails are retained, not cut away. Therefore

```text
AA+BB common-source Selmer candidates subset S~
```

is safe for the audit, while `S~ = Sel_2(E_row)` for the full single diagnostic
curve is not claimed.

## Diagnostics

Existing `sage_mixed_closure_aabb_selmer_diagnostics.jsonl` rows give:

```text
measured_object = single_curve_full_2_selmer
source_tool = Sage EllipticCurve(model).selmer_rank on the row's AA or BB curve
diagnostic_row_count = 12
ok_row_count = 12
selmer_dim_eq_torsion_count = 0
selmer_dim_gt_torsion_count = 12
proved_rank_zero_and_selmer_gt_torsion_count = 0
rank_zero_frontier_selmer_gt_torsion_count = 11
max_selmer_rank_minus_torsion = 4
t_tail_histogram = {0: 7, 1: 5}
```

These diagnostics measure the full 2-Selmer group of the individual elliptic
curve in that row (`AA` or `BB`). They do **not** measure the AA side alone,
the BB side alone, the AA+BB common-source pseudo-container `S~`, or the full
complete-cover local matrix for `S~`.

This resolves the apparent mismatch: rows with

```text
omega_{1 mod 4}(T) = 0
selmer_rank_minus_torsion = 2
```

are full single-curve Selmer diagnostics, so they are not counterexamples to
the symbolic AA+BB common-source container bound

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign.
```

For bookkeeping, 7 diagnostic rows have `omega_{1 mod 4}(T)=0` and extra
full-curve Selmer dimension, and 8 full-curve rows exceed the symbolic tail
capacity one would get by incorrectly comparing them to `S~`. Those counts are
recorded only to prevent future object-confusion; they are not violations of
the `S~` bound.

Plain meaning: every available full-curve diagnostic has `Sel_2` dimension
larger than the two-torsion baseline, but none is a proved rank-zero plus
extra-`Sel_2` row. So this is not yet enough to declare `Sha[2]` the true
obstruction.

## Route Decision

Current route:

```text
joint_local_condition_at_T_tail
```

Reason:

```text
S~ does not force dimension 2; full-curve diagnostics show extra Selmer
dimension but no proved rank-zero Sha[2] witness.
```

Next action:

```text
kill or account for the ell | T, ell == 1 mod 4 tail and the archimedean sign bit.
```

If a later diagnostic proves rank zero while `dim Sel_2(E)>2`, then the route
should switch to `Sha[2]` separation by Cassels-Tate pairing, second descent,
or an L-value route.

## Boundary

This audit does not prove:

- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion.

It only proves that the current cheap upper-bound container still has symbolic
tail terms, so a rank-zero theorem cannot yet be promoted.
