# Post-wl525 Route-Choice Audit

## Question

Using `wl525` as immediate input, what is the next narrow route after the
attempted promotion of the finite taxonomy to a uniform cover-family
squareclass theorem failed?

This is a route-choice audit only. It compares exactly the four next-route
families requested here, chooses one later gate, and stops before entering it.
It does not execute shell 11, compute new `M_tail` supports, test new ambient
`C_d` solubility, apply `wl491` to a new point, build function-field models,
prove the uniform lemma, run broad rank/Selmer diagnostics, use the old
package-`x` / `S~` bridge, select a final obstruction candidate, or claim
theorem-level progress.

## Input

`wl525` entered the `wl524` selected gate:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

and found the precise failure point:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

The finite 15 cover-family / 29 entry taxonomy has point-level
non-admissibility data, but it does not provide cover-family function-field
models, rational `N,M` maps, divisor parity data, or a specialization argument.
Therefore the finite taxonomy cannot be promoted to a uniform theorem from the
current inputs. This does not mathematically refute a possible future uniform
lemma.

## Route Families Compared

The audit compares exactly:

- `gather_minimal_function_field_squareclass_proof_data_for_named_cover_families`
- `return_to_finite_shell_m_tail_diagnostics`
- `name_theorem_level_complete_selmer_local_hilbert_row_obligation`
- `abandon_this_obstruction_line_and_select_different_candidate`

## Decision

The selected next narrow gate is:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

It is selected because it is the smallest route that directly addresses the
`wl525` failure point. Before another proof attempt, the route needs only to
scope whether the named cover families have:

- a cover-family model inventory;
- rational source-side map inventory;
- candidate `N` and `M` function-field elements;
- an opposite-side product squareclass or divisor-parity certificate target;
- an exceptional specialization and positivity-separation checklist.

This gate is not entered here. In particular, `wl526` does not build those
models, compute the function-field squareclasses, prove the uniform lemma, or
claim that the uniform lemma is true.

The other route families are not selected:

- finite shell / `M_tail` diagnostics are deferred because more finite support
  data would not by itself supply the missing function-field certificate;
- theorem-level complete-Selmer local / Hilbert row work is deferred because
  `wl525` names a cover-family squareclass proof-data gap, not a specific
  Selmer row obligation;
- abandoning the obstruction line and selecting a different candidate is
  rejected for now because `wl525` refutes only the finite-taxonomy promotion,
  not the possible mathematical lemma.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.json
```

with:

```text
status = ok
work_log = wl526
input_work_log = wl525
routing_audit_only = true
post_wl525_route_choice_made_here = true
selected_next_gate.gate =
  gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
selected_next_gate.entered_here = false
selected_next_gate.object_layer = cover_family_function_field_proof_data_scoping
function_field_models_built_here = false
function_field_squareclass_certificate_proved_here = false
uniform_cover_family_lemma_proved_here = false
complete_selmer_local_hilbert_row_obligation_named_here = false
abandoned_obstruction_line_here = false
different_candidate_selected_here = false
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
rank_zero_claimed = false
complete_selmer_upper_bound_proved = false
advance_to_selected_next_gate = false
advance_to_wl527 = false
stop_after_current_task = true
```

## Boundary

This work-log stops after `wl526`. It does not prove:

- a uniform cover-family squareclass obstruction;
- function-field nonsquareness of any opposite-side product;
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

No next roadmap step is entered here. The next explicit gate, if chosen later,
is only the proof-data scoping step named above.
