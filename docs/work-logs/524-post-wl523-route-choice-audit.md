# Post-wl523 Route Choice Audit

## Question

Using `wl523` as input, what is the next narrow route after the
common-source square obstruction lemma candidate has been separated into:

```text
point-level obstruction: provable from existing wl491 machinery
uniform cover-family theorem: still unproved
```

This is a route-choice audit only. It compares the viable next moves, chooses
one next gate, and stops before entering it.

It does not prove the uniform cover-family squareclass lemma. It does not
execute shell 11, compute new `M_tail` supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, run broad rank/Selmer diagnostics,
or select a final obstruction candidate.

## Inputs

The immediate input is `wl523`, whose decision is:

```text
point_level_lemma_status = provable_from_existing_wl491_machinery
cover_family_uniform_theorem_status = needs_new_uniform_squareclass_lemma
finite_taxonomy_count_is_proof = false
```

The route state carried forward is:

```text
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
globally_soluble_but_not_aa_bb_admissible_entry_count = 29
opposite_side_squareclass_failure_entry_count = 29
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
active_final_obstruction_candidate_count = 0
```

The touched object layer is only:

```text
post-wl523 route choice at the cover-family statement layer
```

not the old package-`x` / `S~` pseudo-container, not new finite `M_tail`
diagnostics, not new ambient `C_d` solubility, not new point-level
admissibility filtering, and not theorem-level `Sel_2(E_L/Q)`.

## Route Options

The selected option is:

```text
attempt_new_uniform_cover_family_squareclass_obstruction_lemma
```

with next gate:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

and:

```text
entered_here = false
input_work_log_to_use_later = wl523
object_layer = cover_family_statement_layer
not_a_selmer_upper_bound = true
not_a_finite_taxonomy_count_claim = true
uniform_cover_family_lemma_proved_here = false
shell11_executed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
candidate_selected_here = false
```

This is the narrowest next route because `wl523` already closes the
point-level statement but leaves one named theorem-candidate gap: whether the
opposite-side common-source product can be proved non-square uniformly on the
globally soluble but not AA+BB-admissible cover families. A later attempt may
fail; `wl524` does not prejudge it.

The rejected or deferred alternatives are:

- returning to finite shell 11 `M_tail` diagnostics is deferred, because it
  would widen finite diagnostics before testing the named post-`wl523` proof
  gap;
- proof-level local / Hilbert row work is deferred until a specific Selmer row
  obligation is named; `wl523` names a cover-family squareclass gap, not an
  odd-prime, dyadic, or Hilbert-symbol row;
- final obstruction candidate selection is rejected because there is no
  AA+BB-admissible cover family, no genuinely deferred cover family, and no
  active final obstruction candidate.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.json
```

with:

```text
status = ok
work_log = wl524
input_work_log = wl523
post_wl523_route_choice_made_here = true
selected_next_gate.gate = attempt_uniform_cover_family_squareclass_obstruction_lemma
selected_next_gate.entered_here = false
selected_route_entered_here = false
uniform_cover_family_lemma_proved_here = false
shell11_executed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
broad_rank_or_selmer_diagnostics_run = false
advance_to_selected_next_gate = false
advance_to_wl525 = false
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

This work-log stops after `wl524`. It does not prove:

- a uniform cover-family squareclass obstruction;
- a new local/Hilbert row;
- a new `M_tail` row or uniform `M_tail` full rank;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new point or support;
- a final obstruction candidate;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next narrow gate is to attempt a new uniform cover-family squareclass
obstruction lemma, using `wl523` as input. That gate is selected here but not
entered.
