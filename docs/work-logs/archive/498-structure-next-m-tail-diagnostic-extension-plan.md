# Structure Next M_tail Diagnostic Extension Plan

## Question

Using `wl497` as input, what exact structure must the next `M_tail`
diagnostic extension have before any new grid is refreshed or any new support
is routed?

This is a planning audit only. It defines the allowed parameter axes,
exclusion ledger, duplicate-support guard, expected output schema, stop
conditions, and future routing contract. It does not refresh a new grid, does
not compute new supports, does not test ambient `C_d` solubility, does not
apply `wl491` to a new point, does not select a final obstruction candidate,
and does not advance to `wl499`.

## Inputs

The input is:

```text
wl497 post-wl496 route choice audit
```

The touched object layer is the route structure around the parameter-dependent
`M_tail` diagnostic layer. This is not the old package-`x` / `S~`
pseudo-container and not theorem-level `Sel_2(E_L/Q)`.

The required `wl497` state is:

```text
u3_active_unprocessed_candidate_count_after_wl493 = 0
u3_processed_or_deprioritized_count_after_wl493 = 1
bounded_v5_active_support_entry_count_from_wl494 = 6
bounded_v5_routed_not_admissible_count_from_wl495 = 4
bounded_v5_refuted_ambient_count_from_wl496 = 2
bounded_v5_still_deferred_count_after_wl496 = 0
aa_bb_admissible_count_after_wl496 = 0
active_candidate_count_after_wl496 = 0
```

## Allowed Parameter Axes

The next extension must be a finite, declared primitive shell:

```text
extension_unit = finite_primitive_shell
side in {AA, BB}
A, B positive integers
gcd(A,B) = 1
shell_axis = max(A,B)
prior_completed_shell_bound = 4
allowed_future_shells = finite shells with max(A,B) > 4
sample_order = shell_bound ascending, side, then A ascending, then B ascending
```

Derived fields such as `L`, `T`, `sqrt_q`, `M_tail` rows, kernel supports, and
complete `d`-coordinate cover input are future execution outputs only. They are
not computed here.

## Exclusion Ledger

The family-level exclusion is:

```text
support = u_3
scope = support_family
future_action = exclude_or_deprioritize_without_reentering
```

The bounded `v_5` entries from `wl494` through `wl496` are route-key
exclusions:

```text
AA_A1_B4_v_5_m_tail_refresh_candidate
AA_A2_B3_v_5_m_tail_refresh_candidate
AA_A4_B1_v_5_m_tail_refresh_candidate
BB_A1_B4_v_5_m_tail_refresh_candidate
BB_A3_B2_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
```

The four `wl495` globally soluble entries stay in:

```text
globally_soluble_but_not_aa_bb_admissible_ledger
```

The two `wl496` refuted entries stay in:

```text
ambient_c_d_global_solubility_refuted_ledger
```

None of these disposed entries may be selected as a final obstruction or
retested for ambient `C_d` solubility inside `wl498`.

## Duplicate-Support Guard

The future extension must key every support by:

```text
source_quotient, A, B, L, T, candidate_support
```

The guard rules are:

- the same route key as the exclusion ledger is not genuinely new;
- a candidate id collision with the exclusion ledger routes to
  `excluded_duplicate_or_processed_supports`;
- `u_3` is always excluded as already processed;
- bounded `wl494`-`wl496` `v_5` route keys are excluded, but a `v_5` support on
  a different future shell is labeled `existing_support_family_new_sample`
  rather than silently treated as the old bounded entry;
- any other support is eligible only if its route key is absent from the
  exclusion ledger.

## Future Output Schema

A later executable extension should emit, at minimum:

```text
status
ready
work_log
input_work_log
declared_extension_scope
sample_summary
rank_kernel_summary_by_sample
active_new_kernel_supports
excluded_duplicate_or_processed_supports
duplicate_support_guard_summary
next_gate_after_extension
```

Each candidate entry should include:

```text
candidate_id
candidate_support
sample
route_key
rank_and_row_status
duplicate_guard_result
routing_state
required_next_gate
```

The required false claim flags remain:

```text
candidate_selected_here = false
new_local_row_proved_here = false
new_c_d_solubility_tested_here = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
```

## Future Routing Contract

Any genuinely new support must follow:

```text
M_tail support
  -> ambient C_d global solubility
  -> wl491 AA+BB admissibility filter
  -> admissible / not_admissible / refuted ledger
```

The future `M_tail` extension should stop after the finite declared shell is
audited, stop if only duplicate or processed supports remain, and stop
immediately after recording any genuinely new support queue. It should not
test ambient `C_d` solubility inside the `M_tail` extension and should not
apply `wl491` until ambient `C_d` global solubility is proved.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan.json
```

with:

```text
status = ok
work_log = wl498
input_work_log = wl497
extension_plan_built_here = true
new_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
candidate_selected_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl499 = false
```

## Boundary

This work-log stops after `wl498`. It does not prove:

- a new `M_tail` row;
- a new local/Hilbert row;
- a new support;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new point;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is to execute a finite `M_tail` diagnostic extension in a
later work-log using this axis/exclusion/duplicate-guard plan as input. That
later extension must still stop before ambient `C_d` routing unless it is
explicitly scoped as a separate route audit.
