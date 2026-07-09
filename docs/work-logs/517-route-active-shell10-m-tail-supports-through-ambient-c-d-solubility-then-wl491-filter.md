# Route Active Shell-10 M_tail Supports Through Ambient C_d Solubility Then wl491 Filter

## Question

Using `wl516` as input, what happens when exactly the 10 active shell-10
`M_tail` diagnostic supports are routed through ambient `C_d` global solubility
first, with `wl491` applied only after an ambient global point is established?

This is a route audit only. It does not re-open shell-9 ledgers, does not
route duplicate or processed supports, does not execute shell 11, does not
select a final obstruction candidate, does not prove local/Hilbert rows except
for the exact cover checks attached to found points, and does not run broad
rank or Selmer diagnostics.

## Inputs

The inputs are:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl516 finite shell-10 M_tail diagnostic output
```

The touched object layers are:

```text
M_tail diagnostic support queue
complete d-coordinate ambient C_d cover data
wl491 AA+BB admissibility filter for established global ambient points only
```

This is not the old package-`x` / `S~` pseudo-container and not a
theorem-level `Sel_2(E_L/Q)` upper-bound argument.

## Routed Queue

The route audit targets exactly the 10 active shell-10 supports from `wl516`:

```text
AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate
AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
AA_A10_B1_u_5_m_tail_shell10_candidate
AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A1_B10_u_5_m_tail_shell10_candidate
BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate
BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
```

No duplicate or processed support output is re-opened.

## Route Output

Eight entries have exact integral ambient `C_d` points and are then routed
through `wl491` as globally soluble but not AA+BB-admissible:

```text
AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate
AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
AA_A10_B1_u_5_m_tail_shell10_candidate
AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate
BB_A1_B10_u_5_m_tail_shell10_candidate
BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate
BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate
BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
```

Two entries remain genuine ambient-solubility deferred ledgers, so `wl491` is
not applied to them:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

The route summary is:

```text
active_shell10_support_entry_count = 10
processed_exclusions_reopened_count = 0
ambient_globally_soluble_count = 8
ambient_global_solubility_refuted_count = 0
ambient_global_solubility_deferred_count = 2
wl491_filter_applied_count = 8
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 8
aa_bb_filter_deferred_count = 2
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json
```

with:

```text
status = ok
work_log = wl517
input_work_logs = wl491, wl516
route_audit_built_here = true
complete_c_d_cover_data_instantiated_here = true
new_c_d_solubility_tested_here = true
wl491_filter_applied_here = true
all_active_shell10_supports_classified_here = true
all_active_shell10_supports_fully_routed_here = false
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
shell11_executed_here = false
advance_to_wl518 = false
```

## Boundary

This work-log stops after `wl517`. It does not prove:

- a final obstruction candidate;
- a new local/Hilbert row beyond checking exact routed points;
- ambient global non-solubility for the two deferred shell-10 covers;
- AA+BB admissibility for any shell-10 support;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is to decide the two deferred shell-10 ambient `C_d`
global-solubility ledgers if the route continues. That next route is not
entered here.
