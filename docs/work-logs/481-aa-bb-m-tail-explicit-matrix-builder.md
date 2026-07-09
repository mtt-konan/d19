# AA+BB M_tail Explicit Matrix Builder

## Question

After `wl480` reduced the complete `d`-coordinate D4 obstruction to the
parameter-dependent matrix

```text
M_tail,
```

can we build that matrix explicitly, while staying after the `wl469`/`wl470`
pivot and avoiding the old package-`x` / `S~` bridge?

## Result

`WL481_M_tail_explicit_matrix_builder` builds finite, parameter-specialized
`F2` matrices for primitive AA+BB samples directly in the complete coordinates

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q
```

for

```text
E_L: Y^2=(X+p)*(X^2-4*q).
```

The object is precisely the tail matrix from `wl480`: the residual local
character matrix after the D0 product relation, solved rows `wl475`-`wl479`,
and quotienting the D3 visible torsion baseline. It is not the old
package-`x` pseudo-container.

## Column Definition

Before quotienting by the second visible torsion generator, the row-ledger
generators are

```text
u_ell = (ell,ell,1)      for odd ell | L
v_ell = (ell,1,ell)      for odd ell | T
w_ell = (1,ell,ell)      for odd ell | sqrt_q
w_2   = (1,2,2)          in the balanced dyadic stratum
```

The tail columns remove `tau_minus` and then quotient by

```text
tau_sqrt_q = product_{ell|sqrt_q} w_ell
             times w_2 when v2(sqrt_q) is odd.
```

The implementation chooses a deterministic omitted pivot column: `w_2` if it
is present, otherwise the last odd `w_ell` column if available.

## Row Definition

The odd rows are computable finite-prime character rows:

```text
ell | L:
  chi_ell(d_minus_p/d_pos_2sqrt_q)

ell | T:
  chi_ell(d_minus_p/d_neg_2sqrt_q)

ell | sqrt_q:
  chi_ell(d_pos_2sqrt_q/d_neg_2sqrt_q)
```

where `chi_ell` is the Legendre character. The dyadic rows are computable
`Q_2` squareclass character rows from the two `wl478` strata.

For the ordinary stratum, the builder records the residual sign character of
`d_neg_2sqrt_q`. For the balanced stratum, it records the residual
5-character of `d_minus_p` and sign character of `d_neg_2sqrt_q`.

## Sample Diagnostics

The result JSON contains deterministic primitive AA+BB samples with:

```text
columns
rows
matrix
rank_needed
computed_rank
computed_rank_status
symbolic_rank_status
kernel_diagnostics
```

The samples include both outcomes:

```text
full_for_this_finite_sample
kernel_found_for_this_finite_sample
```

The kernel diagnostics are finite-sample diagnostics only. A kernel in one
sample is a concrete obstruction to treating the solved rows as a uniform
full-rank theorem; a full-rank sample is not promoted to a theorem.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder.json
```

with:

```text
status = ok
work_log = wl481
input_work_log = wl480
matrix_object.id = M_tail
symbolic_rank_status = uniform_full_rank_not_proved
computed_rank_status = finite_samples_computed_only
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after building explicit sampled `M_tail` matrices. It does
not prove:

- a uniform full-rank theorem for `M_tail`,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
