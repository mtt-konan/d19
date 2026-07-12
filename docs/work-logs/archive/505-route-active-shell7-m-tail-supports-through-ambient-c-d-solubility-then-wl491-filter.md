# Route Active Shell-7 M_tail Supports Through Ambient C_d Solubility Then wl491 Filter

## Question

Using `wl504` as input, how do exactly the 12 active shell-7 `M_tail`
diagnostic supports route after the required ambient `C_d` global-solubility
gate, and where should the `wl491` AA+BB admissibility filter be applied?

This work-log touches only:

```text
wl504 active shell-7 M_tail support entries
complete d-coordinate C_d cover
ambient C_d global solubility
AA+BB admissibility gate routing
```

It does not touch the old package-`x` / `S~` pseudo-container and does not
claim anything about theorem-level `Sel_2(E_L/Q)`.

## Inputs

The input is:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl504 active_new_kernel_supports
```

Only the 12 entries already classified by `wl504` as:

```text
ambient_c_d_global_solubility_status = not_tested_here
aa_bb_admissibility_status = not_applied_here
ledger_route = m_tail_shell_support_pending_ambient_C_d_solubility
```

are eligible. The two pure `u_3` processed exclusions are explicitly retained
as not re-opened:

```text
AA_A6_B7_u_3_m_tail_shell7_candidate
BB_A7_B6_u_3_m_tail_shell7_candidate
```

## Route Result

The audit routes all 12 active shell-7 supports in `wl504` queue order:

```text
active_shell7_support_entry_count = 12
processed_exclusions_reopened_count = 0
ambient_globally_soluble_count = 8
ambient_global_solubility_refuted_count = 0
ambient_global_solubility_deferred_count = 4
wl491_filter_applied_count = 8
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 8
aa_bb_filter_deferred_count = 4
```

The eight globally soluble entries have exact integral ambient `C_d` witnesses
recorded in the result JSON. Each is then passed through `wl491`, and each
routes to:

```text
globally_soluble_but_not_aa_bb_admissible_ledger
```

One representative exact witness is:

```text
AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate
d = (15,51,85)
X = 1088
u_minus_p = 8
u_pos_2sqrt_q = 4
u_neg_2sqrt_q = 4
induced E_L point = (X,Y) = (1088,32640)
wl491 output_class = not_admissible
```

The four unresolved entries are:

```text
AA_A4_B7_w_5_m_tail_shell7_candidate
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
```

They are routed to:

```text
ambient_c_d_global_solubility_status = global_solubility_deferred
aa_bb_admissibility_status = not_applied_ambient_global_solubility_unproved
ledger_route = ambient_c_d_solubility_deferred_ledger
```

The bounded integral probe recorded for those four ledgers is not a global
insolubility proof, so no refutation is claimed.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json
```

with:

```text
status = ok
work_log = wl505
input_work_logs = wl491, wl504
route_audit_built_here = true
all_active_shell7_supports_classified_here = true
all_active_shell7_supports_fully_routed_here = false
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_m_tail_full_rank_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl506 = false
```

## Boundary

This work-log stops after `wl505`. It does not prove:

- a new `M_tail` row;
- a new local/Hilbert row;
- an AA+BB-admissible shell-7 point;
- a global insolubility result for the four deferred shell-7 covers;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero as a family theorem;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is the four deferred shell-7 ambient `C_d` global-solubility
ledgers listed above. No post-`wl505` route choice is entered here.
