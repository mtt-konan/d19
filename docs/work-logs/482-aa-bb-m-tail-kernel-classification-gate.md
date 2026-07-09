# AA+BB M_tail Kernel Classification Gate

## Question

Using `wl481` as input, what is the status of the finite AA sample

```text
A=3, B=1
```

kernel support

```text
u_3
```

in the complete `d`-coordinate tail matrix `M_tail`?

The gate is narrow: decide whether this support is an artifact of the sampled
row builder / omitted visible torsion pivot, is killed by a known missing local
character row, or should be recorded as a genuine parameter-specialized tail
obstruction candidate.

## Result

`WL482_M_tail_kernel_classification_gate` classifies the `AA, A=3, B=1`
support `u_3` as:

```text
genuine_parameter_specialized_tail_obstruction_candidate
```

within the `wl481` finite-sample `M_tail` row contract.

This means:

- it is not an omitted `tau_sqrt_q` pivot artifact,
- no known `wl475`-`wl478` / `wl481` local row omitted by the sample builder
  kills it,
- killing it would require a newly justified local/Hilbert condition outside
  the current solved-row ledger.

## Pivot Check

For the target sample,

```text
L=3
T=4
sqrt_q=52=4*13
```

the raw pre-quotient columns are:

```text
u_3, w_13
```

The visible torsion quotient omits:

```text
w_13
```

as the `tau_sqrt_q` pivot. The target kernel support is `u_3`, so it is not
the omitted pivot and is not equal to the visible `tau_sqrt_q` support.
Restoring the raw pivot leaves the known row pairings with `u_3` equal to:

```text
0, 0, 0
```

Thus the `u_3` support is not created by the quotient convention.

## Local Row Coverage

The relevant places recorded for this finite sample are:

```text
infinity, 2, 3, 13
```

The instantiated `wl481` rows are:

```text
odd_L_3_equal_d_minus_p_d_pos_2sqrt_q
odd_sqrt_q_13_equal_d_pos_2sqrt_q_d_neg_2sqrt_q
dyadic_ordinary_d_neg_2sqrt_q_sign_character
```

All have zero entry on `u_3`.

The other known row types are inactive or already accounted for:

- odd `T` rows are vacuous because `T=4` has no odd prime divisor,
- balanced dyadic rows are inactive because `epsilon_balanced_2=0`,
- the real sign row is already quotiented as `tau_minus`, and `u_3` is
  positive.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl482_m_tail_kernel_classification_gate.json
```

with:

```text
status = ok
work_log = wl482
input_work_log = wl481
classification.final_classification = genuine_parameter_specialized_tail_obstruction_candidate
omitted_torsion_pivot_check.decision = not_an_omitted_torsion_pivot_artifact
known_local_row_coverage_check.decision = no_known_wl475_wl478_or_wl481_row_missing_that_kills_u_3
symbolic_rank_status = uniform_full_rank_not_proved
computed_rank_status = finite_sample_kernel_classified_only
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after classifying the finite `AA, A=3, B=1` `u_3`
kernel from `wl481`. It does not prove:

- a uniform full-rank theorem for `M_tail`,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
