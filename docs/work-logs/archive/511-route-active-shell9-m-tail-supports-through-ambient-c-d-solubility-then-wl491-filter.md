# Route Active Shell-9 M_tail Supports Through Ambient C_d Solubility Then wl491 Filter

## Question

Using `wl510` as input, what happens to exactly the eight active shell-9
`M_tail` diagnostic supports when they are routed through ambient `C_d` global
solubility first, with the `wl491` AA+BB admissibility filter applied only
after an ambient global point is established?

This is a route audit only. It does not execute shell 10, does not re-open any
closed ledger through `wl510`, does not re-open duplicate / processed supports,
does not select a final obstruction candidate, does not prove local rows, does
not run broad rank/Selmer diagnostics, and does not advance to the next route.

## Inputs

The input is:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl510 finite shell-9 M_tail diagnostic extension
```

The touched object layers are:

```text
M_tail diagnostic support queue
ambient complete d-coordinate C_d solubility
AA+BB admissibility filter after ambient solubility is established
```

not the old package-`x` / `S~` pseudo-container and not theorem-level
`Sel_2(E_L/Q)`.

The closed ledgers through `wl510` are preserved. In particular, the shell-7
resolved ledgers, shell-8 processed pure `u_3` exclusions, bounded `v_5`
ledgers, shell-5 `u_5` ledgers, and old `u_3` ambient ledger are not re-opened.

## Routed Shell-9 Supports

The routed active diagnostic supports are exactly:

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

The duplicate / processed queue remains empty:

```text
processed_exclusions_not_reopened = []
```

## Route Output

Four entries have exact integral ambient `C_d` witnesses and are globally
soluble:

```text
AA_A9_B1_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
AA_A9_B4_v_13_m_tail_shell9_candidate
BB_A1_B9_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
BB_A4_B9_v_13_m_tail_shell9_candidate
```

The `wl491` filter is applied to exactly those four entries. All four route to:

```text
globally soluble but not AA+BB-admissible
```

The remaining four entries are genuinely deferred because this audit records no
ambient global `C_d` point for them and the bounded integral probe is not a
global insolubility proof:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

No entry is AA+BB-admissible here, and no entry is proved ambient globally not
soluble here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl511_route_active_shell9_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json
```

with:

```text
status = ok
work_log = wl511
input_work_logs = wl491, wl510
active_shell9_support_entry_count = 8
ambient_globally_soluble_count = 4
ambient_global_solubility_refuted_count = 0
ambient_global_solubility_deferred_count = 4
wl491_filter_applied_count = 4
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 4
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
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
shell10_executed_here = false
advance_to_wl512 = false
```

## Boundary

This work-log stops after `wl511`. It does not prove:

- a new local/Hilbert row;
- ambient global non-solubility for the four deferred shell-9 covers;
- AA+BB admissibility for any shell-9 support;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is the four shell-9 ambient `C_d` global-solubility deferred
ledgers. That later route is not entered here.
