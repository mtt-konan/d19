# AA+BB Extend Or Refresh M_tail Diagnostics

## Question

After `wl493` finds no active unprocessed support in the existing `wl481`
queue, does a narrow deterministic refresh of the `M_tail` diagnostics expose
new unprocessed kernel supports beyond the already processed `u_3` support?

This is a diagnostic refresh only. It does not prove a new local row, does not
test ambient `C_d` solubility for a new support, does not apply or prove
AA+BB admissibility for a new candidate, and does not select a final
obstruction candidate.

## Inputs

The refresh uses:

```text
wl480 D4 M_tail matrix object and row ledger
wl493 empty active queue / processed u_3 routing state
wl481 existing M_tail explicit matrix builder
```

The touched object layer is:

```text
M_tail
```

not the old package-`x` / `S~` pseudo-container, not an ambient `C_d`
solubility proof, and not the theorem-level `Sel_2(E_L/Q)`.

## Refresh Scope

`wl494` reruns the existing `wl481` matrix builder on the bounded primitive
grid:

```text
side in {AA, BB}
1 <= A <= 4
1 <= B <= 4
gcd(A,B) = 1
sample order = side, then A ascending, then B ascending
```

This gives:

```text
sample_count = 22
full_rank_sample_count = 14
kernel_sample_count = 8
kernel_support_entry_count = 8
active_new_support_entry_count = 6
processed_or_excluded_u3_entry_count = 2
unique_active_supports = v_5
```

The active refreshed entries are `v_5` supports in six sampled rows. They are
only diagnostic queue entries. Their ambient `C_d` solubility and AA+BB
admissibility are both recorded as:

```text
not_tested_here
```

The refreshed `u_3` entries are kept out of the active queue using the `wl493`
processed / not-admissible routing state:

```text
ambient C_d status = globally_soluble
AA+BB admissibility status = not_admissible
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl494_extend_or_refresh_m_tail_diagnostics.json
```

with:

```text
status = ok
work_log = wl494
input_work_logs = wl480, wl493
diagnostic_refresh_built_here = true
candidate_selected_here = false
new_m_tail_row_proved_here = false
ambient_c_d_solubility_proved_for_new_candidate_here = false
aa_bb_admissibility_proved_for_new_candidate_here = false
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl495 = false
```

## Boundary

This work-log stops after `wl494`. It does not prove:

- a new local/Hilbert row;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new point;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next narrow action, not entered here, is to take any active refreshed
support through the normal route:

```text
refreshed M_tail support
  -> ambient C_d solubility
  -> wl491 AA+BB admissibility filter
  -> only then admissible / not_admissible ledger routing
```
