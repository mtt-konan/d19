# Attempt Uniform Cover-Family Squareclass Obstruction Lemma

## Question

Using `wl523` and `wl524` as inputs, can the point-level opposite-side
common-source square obstruction be promoted to a uniform cover-family lemma
for the `wl522` globally soluble but not AA+BB-admissible cover families?

This enters only the cover-family statement layer selected by `wl524`. It does
not execute shell 11, compute new `M_tail` supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, run broad rank/Selmer diagnostics,
use the old package-`x` / `S~` bridge, or select a final obstruction
candidate.

## Inputs

`wl523` supplies the point-level statement:

```text
After a certified wl491 centered-even pullback gives rational N,M,
the opposite-side product

  AA source: (N^2+B^2)(M^2+B^2)
  BB source: (N^2+A^2)(M^2+A^2)

being a non-square in Q*/Q*2 blocks AA+BB admissibility.
```

`wl524` selected the later gate:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

and stopped before entering it.

The finite snapshot carried through `wl523` remains:

```text
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
globally_soluble_but_not_aa_bb_admissible_entry_count = 29
opposite_side_squareclass_failure_entry_count = 29
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
```

These are audit counts, not a theorem proof.

## Uniform Lemma Target

The attempted uniform statement would be:

```text
For every rational ambient C_d point on each named wl522 globally soluble but
not AA+BB-admissible cover family that has a certified wl491 centered-even
pullback, the opposite-side common-source product is non-square in Q*/Q*2.
```

Even if proved, this would only be a cover-family AA+BB non-admissibility
obstruction. It would not prove a theorem-level Selmer upper bound, rank zero,
`Sha[2]=0`, uniform `M_tail` full rank, or family exclusion.

## Required Proof Obligations

A genuine uniform proof would need at least:

- a cover-family model and rational source-side map for each named cover family;
- `N` and `M` as rational functions on the cover-family function field;
- the opposite-side product as a rational function on that function field;
- a proof that this function is not a square in the relevant function field,
  or an equivalent squareclass obstruction that survives specialization to
  every rational point under consideration;
- separate control of exceptional divisors, poles, zeroes, and positivity /
  nondegeneracy failures;
- a uniform argument for all rational points on the family, not just the finite
  `wl522` ledger entries.

## Decision

The uniform lemma is not proved from the `wl523` / `wl524` inputs.

The precise failure point is:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

`wl523` gives a point-level `wl491` obstruction, and `wl524` chooses this proof
attempt. Neither input gives cover-family function-field squareclass data,
divisor parity data, or a specialization argument. Therefore the 15
cover-family / 29 entry taxonomy cannot be promoted to a uniform theorem.

This does not mathematically refute the possible uniform lemma. It refutes
only the attempted promotion from the available finite taxonomy to that
uniform statement.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.json
```

with:

```text
status = ok
work_log = wl525
input_work_logs = [wl523, wl524]
object_layer = cover_family_statement_layer
selected_gate_entered_here = true
attempted_uniform_cover_family_lemma_here = true
attempt_decision.uniform_cover_family_lemma_status =
  not_proved_from_wl523_wl524_inputs
attempt_decision.finite_taxonomy_promotion_status = refuted
attempt_decision.mathematical_uniform_lemma_refuted = false
attempt_decision.failure_point = missing_function_field_squareclass_certificate
finite_taxonomy_is_theorem_proof = false
uniform_cover_family_lemma_proved_here = false
precise_failure_point = finite_taxonomy_has_no_uniform_squareclass_certificate
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
rank_zero_claimed = false
complete_selmer_upper_bound_proved = false
advance_to_next_roadmap_step = false
stop_after_current_task = true
```

## Boundary

This work-log stops after `wl525`. It does not prove:

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

No next roadmap step is entered here. A later route choice would have to decide
whether to gather new function-field squareclass proof data, return to a finite
diagnostic route, or name a different theorem-level Selmer obligation.
