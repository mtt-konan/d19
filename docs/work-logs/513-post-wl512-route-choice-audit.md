# Post-wl512 Route Choice Audit

## Question

Using `wl512` as input, what is the next narrow gate after the two shell-9
`v_13` deferred covers were refuted and exactly two shell-9 `u_7` ambient
`C_d` global-solubility ledgers remain deferred?

This is a route-choice audit only. It observes the `wl512` output, preserves
every closed ledger through `wl512`, chooses the next narrow gate, and stops
before entering that gate.

It does not execute shell 10, does not re-open the two `v_13` ledgers refuted
by `wl512`, does not re-open the four shell-9 globally soluble but not
AA+BB-admissible ledgers from `wl511`, does not prove local/Hilbert rows, does
not run broad rank/Selmer diagnostics, and does not select a final obstruction
candidate.

## Inputs

The input is:

```text
wl512 resolve shell-9 deferred ambient C_d global-solubility ledgers
```

The touched object layer is:

```text
ambient C_d deferred-ledger route choice
```

not the old package-`x` / `S~` pseudo-container, not a new `M_tail` diagnostic
extension, not AA+BB admissibility, and not theorem-level `Sel_2(E_L/Q)`.

The `wl512` state imported here is:

```text
wl512_deferred_entry_count = 4
wl512_explicitly_classified_entry_count = 4
shell9_v13_refuted_count_from_wl512 = 2
shell9_u7_still_deferred_count_after_wl512 = 2
shell9_wl491_filter_applied_count_from_wl512 = 0
aa_bb_admissible_count_after_wl512 = 0
active_candidate_count_after_wl512 = 0
```

The two remaining deferred ledgers are exactly:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They share:

```text
L = 7
T = 16
d = (7, 7, 1)
V^2 = (X + 120)(X - 904)(X + 904)
```

## Closed Ledgers Preserved

The closed-ledger list now carried forward is:

```text
u_3_processed_or_deprioritized_after_wl493_wl491
bounded_v_5_entries_disposed_by_wl495_wl496
shell5_u_5_entries_refuted_by_wl500
shell6_empty_diagnostic_output_from_wl502
shell7_entries_disposed_by_wl505_wl506
shell8_pure_u_3_processed_exclusions_from_wl508
shell9_globally_soluble_not_admissible_ledgers_from_wl511
shell9_v_13_deferred_ledgers_refuted_by_wl512
```

Do not re-open these ledgers in the next gate.

## Route Options

The selected option is:

```text
resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers
```

with:

```text
entered_here = false
candidate_ids = AA_A7_B9_u_7_m_tail_shell9_candidate,
                BB_A9_B7_u_7_m_tail_shell9_candidate
shared_cover = L=7,T=16,d=(7,7,1)
allowed_future_certificates = exact_ambient_C_d_global_point,
                              exhaustive_no_lift_certificate
wl491_filter_allowed_only_after_global_solubility = true
shell10_executed_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
candidate_selected_here = false
```

The rejected or deferred options are:

- executing shell 10, because the current explicit shell-9 ambient `C_d` gap
  remains unresolved;
- re-opening the `wl512` `v_13` refutations or the `wl511` not-admissible
  shell-9 ledgers;
- selecting a final obstruction candidate, because no remaining shell-9 entry
  is AA+BB-admissible and the `u_7` cover is still unresolved;
- proving local/Hilbert rows now, which may be selected only as a future
  explicit gate and is not entered here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice_audit.json
```

with:

```text
status = ok
work_log = wl513
input_work_log = wl512
post_wl512_route_choice_made_here = true
selected_next_gate.gate = resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers
selected_next_gate.entered_here = false
remaining_deferred_candidate_ids = AA_A7_B9_u_7_m_tail_shell9_candidate,
                                   BB_A9_B7_u_7_m_tail_shell9_candidate
remaining_deferred_shared_cover.L = 7
remaining_deferred_shared_cover.T = 16
shell9_not_admissible_ledgers_reopened_count = 0
shell9_v13_refuted_ledgers_reopened_count = 0
closed_ledgers_reopened_count = 0
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
shell10_executed_here = false
candidate_selected_here = false
advance_to_selected_next_gate = false
advance_to_wl514 = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_m_tail_full_rank_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
```

## Boundary

This work-log stops after `wl513`. It does not prove:

- ambient global solubility or non-solubility for the two `u_7` shell-9
  ledgers;
- AA+BB admissibility for any shell-9 support;
- a final obstruction candidate;
- a new local/Hilbert row;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next narrow gate is targeted resolution of the remaining shared shell-9
`u_7` ambient `C_d` cover at `L=7,T=16,d=(7,7,1)`, by either an exact ambient
point or an exhaustive no-lift certificate. That gate is not entered here.
