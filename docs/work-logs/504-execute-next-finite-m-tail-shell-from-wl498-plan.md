# Execute Next Finite M_tail Shell From wl498 Plan

## Question

Using `wl503` as input, what does the next declared finite primitive
`M_tail` diagnostic shell produce when executed at exactly:

```text
max(A,B) = 7
side in {AA, BB}
gcd(A,B) = 1
```

This is an `M_tail` diagnostic extension only. It executes the one finite
shell selected by `wl503`, applies the `wl498` duplicate-support guard together
with the closed-ledger exclusions through `wl503`, and records only:

```text
active_new_kernel_supports
excluded_duplicate_or_processed_supports
```

It does not test ambient `C_d` solubility, does not apply `wl491`, does not
select a final obstruction candidate, does not prove local rows, does not run
broad rank/Selmer diagnostics, and does not advance to `wl505`.

## Inputs

The input is:

```text
wl503 post-wl502 empty-shell route choice audit
wl480 D4 M_tail matrix object and row ledger
wl481 existing M_tail explicit matrix builder
wl498 duplicate-support guard and bounded v_5 exclusion keys
wl500 shell-5 u_5 closed ledgers
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
```

## Executed Shell

The declared shell is:

```text
extension_unit = finite_primitive_shell
shell_axis = max(A,B)
shell_bound = 7
side in {AA, BB}
gcd(A,B) = 1
sample order = side, then A ascending, then B ascending
```

This gives:

```text
sample_count = 24
full_rank_sample_count = 12
kernel_sample_count = 12
kernel_support_entry_count = 14
active_new_support_entry_count = 12
excluded_duplicate_or_processed_support_entry_count = 2
unique_active_supports = [u_3, u_7, v_13, v_5, w_17, w_37, w_5]
```

The shell-7 `M_tail` diagnostics therefore produce a non-empty active support
queue under the current row ledger. These entries are still diagnostic
supports only; no ambient `C_d` global point has been proved here.

## Queue Output

The active diagnostic supports are:

```text
AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate
AA_A4_B7_w_5_m_tail_shell7_candidate
AA_A6_B7_v_13_m_tail_shell7_candidate
AA_A7_B2_u_7_m_tail_shell7_candidate
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
AA_A7_B6_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate
BB_A2_B7_u_7_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
BB_A6_B7_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate
BB_A7_B3_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
BB_A7_B6_v_13_m_tail_shell7_candidate
```

The duplicate / processed outputs are:

```text
AA_A6_B7_u_3_m_tail_shell7_candidate
BB_A7_B6_u_3_m_tail_shell7_candidate
```

Both are excluded by the processed `u_3` support-family guard. Compound
supports that include `u_3` are not the same processed support family under
the route-key guard, so they remain diagnostic active supports pending the
later ambient `C_d` solubility route.

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
candidate_id_collision_exclusion_count = 8
```

The active outputs are not final candidates. They must next be routed through:

```text
M_tail support
  -> ambient C_d global solubility
  -> wl491 AA+BB admissibility filter, only where ambient global solubility is proved
  -> admissible / not_admissible / refuted ledger
```

This route is not entered by `wl504`.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl504_execute_next_finite_m_tail_shell_from_wl498_plan.json
```

with:

```text
status = ok
work_log = wl504
input_work_logs = wl480, wl503
m_tail_diagnostics_extended_here = true
new_supports_computed_here = true
active_new_support_entry_count = 12
excluded_duplicate_or_processed_support_entry_count = 2
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
advance_to_wl505 = false
```

## Boundary

This work-log stops after `wl504`. It does not prove:

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

The remaining gap is to route the active shell-7 `M_tail` supports through
ambient `C_d` global solubility, then apply `wl491` only where an ambient
global point is proved. That next gate is not entered here.
