# Support/Cover Taxonomy To Lemma Candidate Checkpoint

## Question

Using `wl521` as the latest state, can the `wl491`-`wl521` AA+BB ledgers be
compressed into a stable support-family / cover-family taxonomy that separates
ambient global failure from AA+BB common-source admissibility failure, and does
that taxonomy isolate one proof-level lemma candidate to try next?

This enters only the taxonomy checkpoint requested after `wl521`. It does not
execute shell 11, compute new `M_tail` supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, run broad rank/Selmer diagnostics,
or select a final obstruction candidate.

## Inputs

The input ledger interval is:

```text
wl491, wl492, wl493, wl494, wl495, wl496, wl497, wl498, wl499,
wl500, wl501, wl502, wl503, wl504, wl505, wl506, wl507, wl508,
wl509, wl510, wl511, wl512, wl513, wl514, wl515, wl516, wl517,
wl518, wl519, wl520, wl521
```

The latest state is `wl521`, which already re-aggregated the final candidate
ledger and recorded:

```text
final_candidate_ledger_entry_count = 43
support_family_count = 13
cover_family_count = 22
genuinely_deferred_entry_count = 0
aa_bb_admissible_entry_count = 0
```

This checkpoint is still in the complete `d`-coordinate / `M_tail` /
ambient-`C_d` / `wl491` route. It is not the old package-`x` / `S~` bridge and
not a theorem-level `Sel_2(E_L/Q)` upper-bound argument.

## Taxonomy

The stable cover-family taxonomy has:

```text
taxonomy_row_count = 22
ambient_globally_not_soluble_cover_family_count = 5
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
processed_or_duplicate_cover_family_count = 2
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
```

The key separation is:

- `ambient_globally_not_soluble`: the ambient `C_d` cover is already refuted,
  so `wl491` is not applicable.
- `common_source_aa_bb_admissibility_failure`: the ambient `C_d` cover is
  globally soluble, but the AA+BB common-source square check fails.
- `processed_or_duplicate_m_tail_support`: finite `M_tail` bookkeeping only.

Thus the 10 refuted entries and 5 refuted cover families are dead ends for the
AA+BB admissibility filter, while the 29 globally soluble but not-admissible
entries across 15 cover families are the reusable signal.

## Lemma Candidates

The extracted patterns are:

```text
common_source_square_obstruction_across_not_admissible_cover_families
  status = theorem-candidate
  cover_family_count = 15
  entry_count = 29

mixed_refuted_not_admissible_same_support_families
  status = data-only
  support_families = u_5, u_7, v_13, v_5

ambient_globally_not_soluble_cover_families
  status = dead end

processed_or_duplicate_m_tail_supports
  status = data-only
```

The one named proof-level lemma candidate isolated here is:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

It is only a theorem-candidate. No proof-level work is entered here, and it is
not a final obstruction candidate. The candidate says exactly what to try next:
turn the recorded opposite-side AA/BB common-source product-not-square
failures into a reusable admissibility obstruction lemma, without treating the
finite cover count as Selmer progress.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.json
```

with:

```text
status = ok
work_log = wl522
input_work_log = wl521
support_cover_taxonomy_built_here = true
selected_next_proof_level_lemma_candidate.status = named_lemma_candidate_isolated
selected_next_gate.gate = try_common_source_square_obstruction_lemma_candidate
selected_next_gate.entered_here = false
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
rank_zero_claimed = false
complete_selmer_upper_bound_proved = false
advance_to_wl523 = false
```

## Boundary

This work-log stops after `wl522`. It does not prove:

- the common-source square obstruction lemma;
- a new local/Hilbert row;
- a new `M_tail` row or uniform `M_tail` full rank;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new support;
- a final obstruction candidate;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next narrow gate is:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

Shell 11 remains unexecuted.
