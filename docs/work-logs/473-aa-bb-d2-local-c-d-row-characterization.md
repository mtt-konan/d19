# AA+BB D2 Local C_d Row Characterization

## Question

After `wl471` defines the complete `d`-coordinate prelocal container and
`wl472` confines relevant support to

```text
S_D1 = {infinity, 2} union {odd ell : ell | L*T*sqrt_q}
```

what are the minimal symbolic local `C_d` row obligations for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q)?
```

## Result

`D2_local_C_d_row_characterization` is framed as row-obligation data, not as a
solved local matrix.

The complete `d`-coordinate order remains

```text
d_minus_p       = X-(-p)=X+p
d_pos_2sqrt_q   = X-(2*sqrt_q)
d_neg_2sqrt_q   = X-(-2*sqrt_q)=X+2*sqrt_q
```

with product relation

```text
d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = 1 in Q*/Q*2.
```

The local covering equations are

```text
d_minus_p*u_minus_p^2 = X+p
d_pos_2sqrt_q*u_pos_2sqrt_q^2 = X-2*sqrt_q
d_neg_2sqrt_q*u_neg_2sqrt_q^2 = X+2*sqrt_q
```

and the AA+BB difference equations are

```text
d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2
d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2
d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q
```

No old package `x`-coordinate collapse is used.

## Minimal Row Obligations

For odd `ell | L`, the collision is between

```text
e_minus=-p, e_pos=2*sqrt_q
```

because

```text
e_pos-e_minus = 16*L^2.
```

The row obligation is to characterize the local solubility of

```text
d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2
```

and output the allowed squareclass pairs for
`(d_minus_p,d_pos_2sqrt_q)`, with `d_neg_2sqrt_q` then determined by the
product relation. The row must separately check whether the other two root
differences, `4*T^2` and `4*sqrt_q`, are `ell`-adic units in the active
parameter stratum.

For odd `ell | T`, the collision is between

```text
e_minus=-p, e_neg=-2*sqrt_q
```

because

```text
e_minus-e_neg = 4*T^2.
```

The row obligation is to characterize

```text
d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2
```

and output the allowed squareclass pairs for
`(d_minus_p,d_neg_2sqrt_q)`, with `d_pos_2sqrt_q` then determined by the
product relation.

For odd `ell | sqrt_q`, the collision is between

```text
e_pos=2*sqrt_q, e_neg=-2*sqrt_q
```

because

```text
e_pos-e_neg = 4*sqrt_q.
```

The row obligation is to characterize

```text
d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q
```

and output the allowed squareclass pairs for
`(d_pos_2sqrt_q,d_neg_2sqrt_q)`, with `d_minus_p` then determined by the
product relation.

For `ell=2`, the obligation is a genuinely dyadic complete-`d` row: all three
root differences contain factors `4` or `16`, so the odd collision templates do
not determine the local image. The next row must characterize the complete
`Q_2` squareclass triples directly from the three difference equations,
separated by the necessary parity and residue strata of `L`, `T`, and
`sqrt_q`. Old dyadic rows in package `x`-coordinates are not imported.

At the real place, the ordered roots are

```text
e_neg=-2*sqrt_q < e_minus=-p < e_pos=2*sqrt_q.
```

The complete sign row is

```text
allowed:   (+,+,+), (-,-,+)
forbidden: (+,-,-), (-,+,-)
```

This real row is recorded only as a local row. It is not combined with finite
rows into a Selmer rank bound here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d2_local_c_d_row_characterization.json
```

with:

```text
status = ok
d2_status = row_obligations_framed
row_obligations_framed = true
local_c_d_rows_solved = false
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after D2 row characterization. It does not prove:

- solved local `C_d` rows at the odd bad primes,
- a dyadic complete local image,
- a complete local-solubility matrix,
- a torsion-baseline quotient computation in D3,
- a D4 uniform matrix rank bound,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It also does not proceed to D3 or D4.
