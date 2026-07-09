# AA+BB Complete d-Container Definition

## Question

After `wl470` pivoted away from the failed package `x`-coordinate bridge, what
is the replacement D0 object before any local `C_d` rows are built?

## Result

`D0_complete_d_container_definition` is framed directly in complete
`d`-coordinates.

Work in the squareclass quotient

```text
V = Q*/Q*2.
```

The pre-local replacement container is

```text
D0_complete_d_prelocal_container =
  { (d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q) in V^3 :
    d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = 1 }.
```

The coordinate order is fixed as

```text
d_minus_p       = X-(-p)=X+p
d_pos_2sqrt_q   = X-(2*sqrt_q)
d_neg_2sqrt_q   = X-(-2*sqrt_q)=X+2*sqrt_q
```

This object is a complete `d`-coordinate pre-local container for symbolic
`C_d` covers. It is not the old `S_tilde` container, and it does not use the
collapsed package `x`-coordinates from `wl469`.

## Product Relation

For a non-root point on

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

the product of the three complete `d`-coordinates is

```text
(X+p)*(X-2*sqrt_q)*(X+2*sqrt_q) = Y^2.
```

Therefore in `Q*/Q*2`,

```text
d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = 1.
```

This is the only row imposed at D0. No local solubility row for `C_d` is built
here.

## Torsion Kummer Baseline

The rational 2-torsion baseline is recorded in the same quotient `V^3` with the
same product relation:

```text
O:
  (1, 1, 1)

T_minus_p=(-p,0):
  ((-p-2*sqrt_q)*(-p+2*sqrt_q),
   -p-2*sqrt_q,
   -p+2*sqrt_q)

T_pos_2sqrt_q=(2*sqrt_q,0):
  (2*sqrt_q+p,
   (2*sqrt_q+p)*(4*sqrt_q),
   4*sqrt_q)

T_neg_2sqrt_q=(-2*sqrt_q,0):
  (-2*sqrt_q+p,
   -4*sqrt_q,
   (-2*sqrt_q+p)*(-4*sqrt_q))
```

These four representatives form the rational `E_L[2](Q)` Kummer baseline
inside the D0 container. The baseline has dimension 2, generated for example by
`T_minus_p` and `T_pos_2sqrt_q`, with

```text
T_minus_p*T_pos_2sqrt_q = T_neg_2sqrt_q
```

in `V^3`. The baseline is recorded, not quotiented out.

## Exceptional Roots

At a root `X=e_i`, the standard complete-descent representative replaces the
vanishing coordinate by the product of the two nonzero root differences. Thus
the root cases are included as complete `d`-data, not rescued through the
package `x`-coordinate collapse:

```text
e_minus = -p
e_pos   =  2*sqrt_q
e_neg   = -2*sqrt_q
```

with representatives listed above for `T_minus_p`, `T_pos_2sqrt_q`, and
`T_neg_2sqrt_q`.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_complete_d_container_definition.json
```

with:

```text
status = ok
d0_status = framed_definition
complete_d_container.local_c_d_rows_built = false
complete_d_container.package_x_coordinates_used = false
torsion_kummer_baseline.same_quotient_as_container = true
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
```

## Boundary

This work-log stops after D0. It does not prove:

- local `C_d` row support confinement,
- a complete local-solubility matrix,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It also does not proceed to D1-D4.
