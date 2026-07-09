# Execute Next Finite M_tail Shell From wl498 Plan

## Question

Using `wl509` as input, what does the next declared finite primitive
`M_tail` diagnostic shell produce when executed at exactly:

```text
max(A,B) = 9
side in {AA, BB}
gcd(A,B) = 1
```

This is an `M_tail` diagnostic extension only. It executes the one finite
shell selected by `wl509`, applies the `wl498` duplicate-support guard together
with all closed-ledger exclusions through `wl509`, and records only:

```text
active_new_kernel_supports
excluded_duplicate_or_processed_supports
```

It does not test ambient `C_d` solubility, does not apply `wl491`, does not
select a final obstruction candidate, does not prove local rows, does not run
broad rank/Selmer diagnostics, and does not advance to the next route.

## Inputs

The input is:

```text
wl509 post-wl508 empty-shell route choice audit
wl480 D4 M_tail matrix object and row ledger
wl481 existing M_tail explicit matrix builder
wl498 duplicate-support guard and bounded v_5 exclusion keys
wl500 shell-5 u_5 closed ledgers
wl502 shell-6 empty diagnostic output
wl505 shell-7 globally soluble but not-admissible ledgers
wl506 shell-7 deferred ledger resolutions
wl508 shell-8 processed u_3 exclusions
```

The touched object layer is:

```text
M_tail
```

not the old package-`x` / `S~` pseudo-container, not ambient `C_d`
solubility, not AA+BB admissibility, and not theorem-level `Sel_2(E_L/Q)`.

The closed ledgers applied here are:

```text
u_3_processed_or_deprioritized_after_wl493_wl491
bounded_v_5_entries_disposed_by_wl495_wl496
shell5_u_5_entries_refuted_by_wl500
shell6_empty_diagnostic_output_from_wl502
shell7_active_not_admissible_ledgers_from_wl505
shell7_processed_u3_exclusions_from_wl505
shell7_w5_deferred_ledgers_refuted_by_wl506
shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506
shell8_empty_active_diagnostic_output_from_wl508
shell8_processed_u3_exclusions_from_wl508
```

## Executed Shell

The declared shell is:

```text
extension_unit = finite_primitive_shell
shell_axis = max(A,B)
shell_bound = 9
side in {AA, BB}
gcd(A,B) = 1
sample order = side, then A ascending, then B ascending
```

This gives:

```text
sample_count = 24
full_rank_sample_count = 16
kernel_sample_count = 8
kernel_support_entry_count = 8
active_new_support_entry_count = 8
excluded_duplicate_or_processed_support_entry_count = 0
unique_active_supports = u_3, u_7, v_13, v_5, w_53
```

These are finite diagnostic outputs only. They are not ambient global `C_d`
points, not AA+BB-admissible points, and not final obstruction candidates.

## Queue Output

The active diagnostic support queue is:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
AA_A9_B1_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
AA_A9_B4_v_13_m_tail_shell9_candidate
BB_A1_B9_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
BB_A4_B9_v_13_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

The duplicate / processed queue is empty:

```text
excluded_duplicate_or_processed_supports = []
```

No ambient `C_d` cover is instantiated or tested for any of these entries
here.

## Duplicate Guard Outcome

The guard is applied with route-key fields:

```text
source_quotient, A, B, L, T, candidate_support
```

The processed/exclusion ledger used by the guard has:

```text
processed_support_family_exclusion_count = 1
bounded_route_key_exclusion_count = 6
shell5_closed_route_key_exclusion_count = 2
shell6_closed_route_key_exclusion_count = 0
shell7_closed_route_key_exclusion_count = 14
shell8_closed_route_key_exclusion_count = 2
candidate_id_collision_exclusion_count = 24
```

This is only a finite-shell diagnostic result. It is not a uniform full-rank
theorem for `M_tail`.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan.json
```

with:

```text
status = ok
work_log = wl510
input_work_logs = wl480, wl509
m_tail_diagnostics_extended_here = true
new_supports_computed_here = true
active_new_support_entry_count = 8
excluded_duplicate_or_processed_support_entry_count = 0
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
aa_bb_admissibility_proved_for_new_candidate_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_m_tail_full_rank_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl511 = false
```

## Boundary

This work-log stops after `wl510`. It does not prove:

- a new local/Hilbert row;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new support;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is to route these active shell-9 `M_tail` diagnostic
supports through ambient `C_d` global solubility first, and only then apply
`wl491` where a global point is proved. That later route is not entered here.
