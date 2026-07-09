# AA+BB Route Refreshed Support Through Ambient C_d Solubility Then Wl491 Filter

## Question

Using `wl494` as input, can the six refreshed active `v_5` `M_tail`
supports be routed through the required sequence:

```text
refreshed M_tail support
  -> instantiate complete d-coordinate C_d cover
  -> prove/refute/defer ambient C_d global solubility
  -> apply wl491 AA+BB admissibility filter only after a global point exists
```

This is a route audit only. It does not prove a new local row, does not run
broad rank or Selmer diagnostics, and does not select a final obstruction
candidate.

## Inputs

The route audit uses:

```text
wl494 active_new_kernel_supports
wl491 classify_ambient_c_d_point_for_aa_bb_admissibility
```

The touched object layers are:

```text
M_tail diagnostic support
complete d-coordinate C_d cover
ambient C_d global solubility
AA+BB admissibility/common-source filter
```

not the old package-`x` / `S~` pseudo-container and not the theorem-level
`Sel_2(E_L/Q)`.

## Route Result

All six active `wl494` entries are kept in order and explicitly classified:

```text
active_refreshed_support_entry_count = 6
ambient_globally_soluble_count = 4
ambient_global_solubility_refuted_count = 0
ambient_global_solubility_deferred_count = 2
wl491_filter_applied_count = 4
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 4
aa_bb_filter_deferred_count = 2
```

For each support, `wl495` instantiates the complete `d`-coordinate cover. For
the current active support family this is:

```text
candidate_support = v_5
d = (5,1,5)
```

The four entries with exact integral ambient `C_d` witnesses are:

```text
AA_A1_B4_v_5_m_tail_refresh_candidate
AA_A2_B3_v_5_m_tail_refresh_candidate
BB_A3_B2_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
```

Each of those four global ambient points is then passed through the `wl491`
filter. All four route to:

```text
output_class = not_admissible
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
```

The two unfinished entries are not silently dropped:

```text
AA_A4_B1_v_5_m_tail_refresh_candidate
BB_A1_B4_v_5_m_tail_refresh_candidate
```

They are routed to:

```text
ambient_c_d_global_solubility_status = global_solubility_deferred
aa_bb_admissibility_status = not_applied_ambient_global_solubility_unproved
ledger_route = ambient_c_d_solubility_deferred_ledger
```

The `wl491` filter is deliberately not applied to these two entries because no
ambient global `C_d` point has been established for them here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json
```

with:

```text
status = ok
work_log = wl495
input_work_logs = wl491, wl494
route_audit_built_here = true
complete_c_d_cover_data_instantiated_here = true
all_refreshed_supports_fully_routed_here = false
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl496 = false
```

## Boundary

This work-log stops after `wl495`. It does not prove:

- ambient solubility or insolubility for the two deferred `v_5` entries;
- an AA+BB-admissible refreshed point;
- a new local/Hilbert row;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining narrow gap, not entered here, is to resolve the two deferred
ambient `C_d` global-solubility ledgers before any final obstruction candidate
can be selected.
