# AA+BB D2c Odd sqrt_q-Collision Row

## Question

In the complete `d`-coordinate route for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

what is the local `C_d` row at an odd prime `ell | sqrt_q` in the pure
`sqrt_q`-collision stratum, where

```text
ell does not divide L*T,
```

so the other two root differences `16*L^2` and `4*T^2` are `ell`-adic square
units?

## Result

`D2c_odd_sqrt_q_collision_row` is solved only in the pure stratum

```text
ell odd, ell | sqrt_q, ell does not divide L*T.
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

At such an `ell`, the colliding root separation is

```text
e_pos-e_neg = 4*sqrt_q,
```

with positive valuation

```text
m = v_ell(sqrt_q) > 0.
```

Unlike the pure `L` and `T` rows, `m` is not assumed even. The two differences
to the third root are square units:

```text
e_pos-e_minus = 16*L^2,
e_minus-e_neg = 4*T^2.
```

The pure stratum also gives a residue constraint:

```text
sqrt_q = T^2 + 4*L^2 == 0 mod ell,
ell does not divide L*T,
```

so `-1` is a square modulo `ell`.

Therefore the pure `ell | sqrt_q` local row is still diagonal:

```text
(d_pos_2sqrt_q, d_neg_2sqrt_q) = (lambda, lambda)
for lambda in Q_ell*/Q_ell*2.
```

Equivalently,

```text
v_ell(d_pos_2sqrt_q) == v_ell(d_neg_2sqrt_q) mod 2
unit(d_pos_2sqrt_q)  == unit(d_neg_2sqrt_q) in F_ell*/F_ell*2.
```

With a fixed nonsquare unit `nu`, the row is

```text
(1,1), (nu,nu), (ell,ell), (nu*ell,nu*ell).
```

The product relation then forces

```text
d_minus_p = 1 in Q_ell*/Q_ell*2.
```

The final allowed row does not depend on the parity of `v_ell(sqrt_q)` or on
the unit squareclass of `sqrt_q`, after imposing the pure-stratum residue
constraint above. The proof does, however, need a separate valuation-case
argument.

## Proof Sketch

Translate by `e_minus` and scale by one of the square-unit differences to the
third root. The third root becomes `0`, and the two colliding roots become

```text
1 and 1 + epsilon, with v_ell(epsilon)=m>0.
```

The reduction is the split nodal model

```text
y^2 = x*(x-1)^2.
```

Away from the node, solubility forces the third-root coordinate to be a square.
Near the node, write the local node parameter as `z`. The two colliding
coordinates are represented by

```text
z and z-epsilon,
```

and local solubility forces

```text
z*(z-epsilon) in Q_ell*2.
```

Thus the two colliding `d`-coordinates have the same squareclass, and the
product relation gives `d_minus_p=1`.

Conversely, every diagonal squareclass is realized:

- Unit squareclasses: choose `v_ell(z)=0`; then `z` and `z-epsilon` have the
  same prescribed unit squareclass.
- Ramified squareclasses with `m >= 2`: choose `v_ell(z)=1<m`; then `z` and
  `z-epsilon` have the same prescribed ramified squareclass.
- Ramified squareclasses with `m = 1`: the class of `epsilon` is realized by
  `v_ell(z)>1`, since `z-epsilon` has class `epsilon` because `-1` is a square.
  The opposite ramified class is realized by taking `z=epsilon*b`, where
  `b` and `b-1` are both nonsquares modulo `ell`. Such a `b` exists because
  `chi(-1)=1`; indeed the number of residues with
  `chi(b)=chi(b-1)=-1` is `(ell-1)/4`.

Hence all and only the four diagonal pairs occur.

## Multi-Collision Boundaries

The following overlaps are not solved here:

- `ell | sqrt_q` and `ell | L`: then `e_pos-e_minus=16*L^2` is not an
  `ell`-adic unit.
- `ell | sqrt_q` and `ell | T`: then `e_minus-e_neg=4*T^2` is not an
  `ell`-adic unit.

These remain multi-collision obligations for a later D2 row-solving step.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row.json
```

with:

```text
status = ok
d2c_status = pure_sqrt_q_collision_row_solved
solved_local_row.allowed_pair_rule = (d_pos_2sqrt_q,d_neg_2sqrt_q)=(lambda,lambda)
solved_local_row.d_minus_p_from_product_relation = 1 in Q_ell*/Q_ell*2
row_depends_on_v_ell_sqrt_q_parity = false
row_depends_on_sqrt_q_unit_residue = false
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

This work-log stops after the pure odd `ell | sqrt_q` row. It references
`wl475` and `wl476` only as the prior solved pure odd rows and does not solve:

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
