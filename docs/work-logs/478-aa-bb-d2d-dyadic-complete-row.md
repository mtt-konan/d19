# AA+BB D2d Dyadic Complete Row

## Question

In the complete `d`-coordinate route for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

what is the `Q_2` local `C_d` row from the three complete difference
equations

```text
d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2
d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2
d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q
```

without importing old package `x`-coordinate dyadic rows?

## Result

`D2d_dyadic_complete_row` is solved as a local `Q_2` row in the complete
coordinate order

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q.
```

Write

```text
L = 2^a*l,  T = 2^b*t,  l,t odd,
sqrt_q = T^2 + 4*L^2.
```

There are two necessary dyadic valuation strata.

### Ordinary Even-sqrt_q Stratum

If

```text
v2(T) != v2(L)+1,
```

equivalently `v2(sqrt_q)` is even, then the allowed triples are

```text
( 1,  1, 1)
( 1,  5, 5)
(-1, -1, 1)
(-1, -5, 5)
( 5,  5, 1)
( 5,  1, 5)
(-5, -5, 1)
(-5, -1, 5)
```

Equivalently,

```text
d_minus_p in {1,-1,5,-5},
d_neg_2sqrt_q in {1,5},
d_pos_2sqrt_q = d_minus_p*d_neg_2sqrt_q.
```

This covers the two subcases

```text
v2(T) < v2(L)+1,  so v2(sqrt_q)=2*v2(T),
v2(T) > v2(L)+1,  so v2(sqrt_q)=2*v2(L)+2.
```

The row does not depend on the odd unit residues of `l` or `t`.

### Balanced Odd-sqrt_q Stratum

If

```text
v2(T) = v2(L)+1,
```

equivalently

```text
v2(sqrt_q)=2*v2(T)+1,
```

then the allowed triples are

```text
( 1,   1,  1)
( 1,   2,  2)
( 1,   5,  5)
( 1,  10, 10)
(-1,  -1,  1)
(-1,  -2,  2)
(-1,  -5,  5)
(-1, -10, 10)
```

Equivalently,

```text
d_minus_p in {1,-1},
d_neg_2sqrt_q in {1,2,5,10},
d_pos_2sqrt_q = d_minus_p*d_neg_2sqrt_q.
```

The row again does not depend on the odd unit residues of `l` or `t`.

## Proof Sketch

Use only the complete `d`-coordinates. Put

```text
A = X+p.
```

Then the represented quantities are

```text
A,  A-16*L^2,  A+4*T^2.
```

If `b != a+1`, the constants `16*L^2` and `4*T^2` have distinct even
2-adic valuations. A valuation partition for `A` rules out ramified
coordinates and leaves exactly the ordinary row above. The root representatives
from the complete-descent convention fall into the same list.

If `b=a+1`, divide the three equations by the square `2^(2*a+4)`. The
normalized quantities are

```text
z,  z-l^2,  z+t^2,
```

with `l,t` odd. The finite roots are congruent to `1` and `-1` modulo `8`,
and their separation has odd valuation because `l^2+t^2` has valuation `1`.
This is exactly the stratum where ramified classes occur, giving the balanced
row above. Hensel lifting of the listed residue classes gives the converse
realization for every listed triple.

## Remaining Overlaps

This work-log does not solve odd multi-collision overlaps. The remaining D2
obligation is

```text
D2_multi_collision_overlaps.
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d2d_dyadic_complete_row.json
```

with:

```text
status = ok
d2d_status = dyadic_complete_row_solved
local_c_d_rows_partially_solved = true
local_c_d_rows_solved = false
remaining_d2_obligations = ["D2_multi_collision_overlaps"]
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after the dyadic complete `Q_2` row. It references
`wl475`, `wl476`, and `wl477` only as the prior solved pure odd rows and does
not solve:

- odd multi-collision overlaps,
- a complete local-solubility matrix,
- a D4 uniform matrix rank bound,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It also does not proceed to D4.
