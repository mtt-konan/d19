# AA+BB H2 Coordinate-Equivalence Audit

## Question

For the complete 2-descent curve

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

do the complete-descent `d`-coordinates and the three package `x`-coordinates
define equivalent squareclass data for every Selmer class, including torsion
representatives and exceptional root cases?

## Result

No. `H2_coordinate_equivalence` is refuted as stated.

Work in

```text
V = Q*/Q*2
```

written additively over `F2`. Complete 2-descent uses

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q
```

with relation

```text
d_minus_p + d_pos_2sqrt_q + d_neg_2sqrt_q = 0.
```

The package translation from `wl464` is:

```text
x_minus_p     = d_pos_2sqrt_q*d_neg_2sqrt_q/d_minus_p
x_pos_2sqrt_q = d_minus_p*d_neg_2sqrt_q/d_pos_2sqrt_q
x_neg_2sqrt_q = d_minus_p*d_pos_2sqrt_q/d_neg_2sqrt_q
```

In `Q*/Q*2`, division by a squareclass is the same as multiplication by it.
Therefore each package coordinate is the same row:

```text
d_minus_p + d_pos_2sqrt_q + d_neg_2sqrt_q.
```

On the complete-descent relation plane, that row is zero. Hence every
complete `d`-tuple satisfying the product relation maps to

```text
(x_minus_p, x_pos_2sqrt_q, x_neg_2sqrt_q) = (1,1,1).
```

The induced map has:

```text
rank_on_complete_relation_plane = 0
kernel_dimension_on_complete_relation_plane = 2
injective_on_complete_d_data = false
```

So the package `x`-triple is not equivalent squareclass data for complete
2-descent `d`-coordinates.

## Torsion And Exceptional Roots

The exceptional root cases do not rescue the equivalence. At a root `X=e_i`,
the standard complete-descent Kummer representative replaces the vanishing
coordinate by the product of the two nonzero root differences. For example,
at `T_minus_p=(-p,0)`:

```text
d_minus_p = (-p-2*sqrt_q)*(-p+2*sqrt_q)
d_pos_2sqrt_q = -p-2*sqrt_q
d_neg_2sqrt_q = -p+2*sqrt_q
```

Substituting these into the package formulas gives:

```text
(1,1,1).
```

The same calculation holds for `O`, `T_pos_2sqrt_q`, and
`T_neg_2sqrt_q`. Thus the package `x`-coordinates collapse the torsion
baseline instead of preserving it as complete `d`-data.

## Consequence

`H2_coordinate_equivalence` cannot be used as the theorem bridge. The existing
package rows may still encode point-level/common-source consistency, but they
do not provide a coordinate-equivalent replacement for complete 2-descent.

This audit stops at H2. It does not build the full `C_d` local matrix, does
not enter `H3_uniform_local_containment` or `H4_mixed_rows_upgrade`, and does
not prove a complete Selmer upper bound.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_h2_coordinate_equivalence.json
```

with:

```text
h2_verdict.status = refuted
coordinate_equivalence_proved = false
coordinate_equivalence_refuted = true
complete_selmer_upper_bound_proved = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
```

## Boundary

This work-log proves only the H2 non-equivalence claim above. It does not
prove:

- `dim Sel_2(E)=2`,
- a rank upper bound,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
