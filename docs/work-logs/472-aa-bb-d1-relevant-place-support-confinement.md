# AA+BB D1 Relevant-Place Support Confinement

## Question

After `wl471` defines the complete `d`-coordinate prelocal container, which
places can affect local solubility of the complete `C_d` covers for

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q)?
```

## Result

`D1_relevant_place_support_confinement` is framed as a support lemma, not a
local-row computation.

Let

```text
e_minus = -p
e_pos   =  2*sqrt_q
e_neg   = -2*sqrt_q
```

and keep the complete descent coordinates from `D0`:

```text
d_minus_p       = X-(-p)=X+p
d_pos_2sqrt_q   = X-(2*sqrt_q)
d_neg_2sqrt_q   = X-(-2*sqrt_q)=X+2*sqrt_q
```

with

```text
d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q = 1 in Q*/Q*2.
```

The D1 finite relevant-place set is

```text
S_D1 = {infinity, 2} union { odd ell : ell | L*T*sqrt_q }.
```

Equivalently, before simplifying parameters, the odd support is the odd prime
support of the root differences

```text
(e_minus-e_pos)*(e_minus-e_neg)*(e_pos-e_neg)
  = (p+2*sqrt_q)*(p-2*sqrt_q)*(4*sqrt_q).
```

The AA+BB parameter identities are

```text
p+2*sqrt_q = 16*L^2
p-2*sqrt_q = -4*T^2
4*sqrt_q = 4*(T^2+4*L^2).
```

Thus the odd part is contained in primes dividing `L*T*sqrt_q`.

## Outside-Support Confinement

For any odd prime `ell` outside `S_D1`, the roots are integral and pairwise
distinct modulo `ell`, and all root differences are `ell`-adic units. At such a
good odd prime, the local Kummer image for a full rational 2-torsion model is
unramified. Therefore any locally soluble complete `C_d(Q_ell)` class has even
`ell`-adic valuation in each `d` coordinate.

So global complete `d`-coordinate candidates may be represented by
`S_D1`-supported squareclasses before D2 writes the local rows at the bad
places.

## What This Does Not Do

D1 does not classify the allowed valuation rows at primes in `S_D1`. In
particular, it does not yet say what happens at:

- `ell | L`,
- `ell | T`,
- `ell | sqrt_q`,
- `ell = 2`,
- the real place.

Those are D2 tasks.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_d1_relevant_place_support_confinement.json
```

with:

```text
status = ok
d1_status = framed_and_proved_support_confinement
candidate_support.equivalent_finite_set = {infinity, 2} union {odd ell: ell | L*T*sqrt_q}
local_c_d_rows_built = false
full_c_d_matrix_built = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
```

## Boundary

This work-log stops after D1. It proves only finite support confinement for the
complete `d`-coordinate route. It does not prove:

- local `C_d` rows,
- a complete local-solubility matrix,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

The next scoped lemma is `D2_local_C_d_row_characterization`.
