# AA+BB D2a Odd L-Collision Row

## Question

In the complete `d`-coordinate route for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

what is the local `C_d` row at an odd prime `ell | L` in the pure
`L`-collision stratum, where the other two root differences are `ell`-adic
units?

## Result

`D2a_odd_L_collision_row` is solved only in the pure stratum

```text
ell odd, ell | L, ell does not divide T*sqrt_q.
```

The complete `d`-coordinate order remains

```text
d_minus_p       = X-(-p)=X+p
d_pos_2sqrt_q   = X-(2*sqrt_q)
d_neg_2sqrt_q   = X-(-2*sqrt_q)=X+2*sqrt_q
```

with product relation

```text
d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = 1 in Q_ell*/Q_ell*2.
```

At such an `ell`, the colliding difference is

```text
e_pos-e_minus = p+2*sqrt_q = 16*L^2,
```

which has positive even `ell`-adic valuation and squareclass `1`. The two
differences to the third root are square units:

```text
e_minus-e_neg = -p+2*sqrt_q = 4*T^2,
e_pos-e_neg   = 4*sqrt_q = (2*T)^2*(1+4*L^2/T^2).
```

Since `ell` is odd and `ell | L` but `ell` does not divide `T`, the factor
`1+4*L^2/T^2` is a square in `Q_ell`.

Therefore the pure `ell | L` local row is

```text
(d_minus_p, d_pos_2sqrt_q) = (lambda, lambda)
for lambda in Q_ell*/Q_ell*2,
```

equivalently

```text
v_ell(d_minus_p) == v_ell(d_pos_2sqrt_q) mod 2
unit(d_minus_p)  == unit(d_pos_2sqrt_q) in F_ell*/F_ell*2.
```

With a fixed nonsquare unit `nu`, the row is

```text
(1,1), (nu,nu), (ell,ell), (nu*ell,nu*ell).
```

The product relation then forces

```text
d_neg_2sqrt_q = 1 in Q_ell*/Q_ell*2.
```

## Proof Sketch

Translate by `e_neg` and scale by the square unit `e_minus-e_neg`. In the pure
stratum, both non-colliding differences to `e_neg` are square units, while the
`e_minus/e_pos` separation is a square of positive valuation. The reduction is
the split nodal model

```text
y^2 = x*(x-1)^2.
```

Away from the node, solubility forces `x` to be a square, so the two colliding
`d`-coordinates have the same squareclass and the third coordinate is square.
Smooth points on the split nodal reduction realize both unit squareclasses,
and choosing `v_ell(X-e_minus)=1` realizes the ramified classes. Hence all and
only the diagonal pairs occur.

## Multi-Collision Boundaries

The following overlaps are not solved here:

- `ell | L` and `ell | T`: then `e_minus-e_neg=4*T^2` is not an `ell`-adic
  unit.
- `ell | L` and `ell | sqrt_q`: then `e_pos-e_neg=4*sqrt_q` is not an
  `ell`-adic unit.

These remain multi-collision obligations for a later D2 row-solving step.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d2a_odd_l_collision_row.json
```

with:

```text
status = ok
d2a_status = pure_L_collision_row_solved
solved_local_row.allowed_pair_rule = (d_minus_p,d_pos_2sqrt_q)=(lambda,lambda)
solved_local_row.d_neg_2sqrt_q_from_product_relation = 1 in Q_ell*/Q_ell*2
local_c_d_rows_partially_solved = true
local_c_d_rows_solved = false
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
```

## Boundary

This work-log stops after the pure odd `ell | L` row. It does not solve:

- the `ell | T` row,
- the `ell | sqrt_q` row,
- the dyadic complete row,
- the multi-collision overlaps,
- a complete local-solubility matrix,
- a D4 uniform matrix rank bound,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It also does not proceed to D4.
