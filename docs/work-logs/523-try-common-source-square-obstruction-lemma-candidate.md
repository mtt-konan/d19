# Try Common-Source Square Obstruction Lemma Candidate

## Question

Using `wl522` as input, can the selected theorem-candidate

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

be stated as a precise reusable AA+BB admissibility obstruction lemma?

This enters only the proof/statement layer. It does not execute shell 11,
compute new `M_tail` supports, test new ambient `C_d` solubility, apply `wl491`
to a new point, run broad rank/Selmer diagnostics, or select a final
obstruction candidate.

## Inputs

The immediate input is `wl522`, whose taxonomy records:

```text
final_candidate_ledger_entry_count = 43
support_family_count = 13
cover_family_count = 22
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
globally_soluble_but_not_aa_bb_admissible_entry_count = 29
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
```

The touched object layer is only:

```text
complete d-coordinate ambient C_d point
  -> wl491 centered-even pullback
  -> AA+BB common-source admissibility obstruction statement
```

This is not the old package-`x` / `S~` pseudo-container and not a
theorem-level `Sel_2(E_L/Q)` upper-bound argument.

## Lemma Statement

The reusable point-level lemma is:

```text
Let A,B > 0. Let an ambient global C_d point in the complete d-coordinate route
be on source quotient AA with L=A, or source quotient BB with L=B. Suppose the
wl491 centered-even pullback is certified and gives rational N,M.

Define
  P_A = (N^2 + A^2)(M^2 + A^2)
  P_B = (N^2 + B^2)(M^2 + B^2).

If the opposite-side product is not a rational square, then the ambient C_d
point is not AA+BB-admissible and must remain in the globally soluble but not
AA+BB-admissible ledger.
```

For an `AA` source the opposite-side product is `P_B`; for a `BB` source it is
`P_A`.

## Failure Separation

The squareclass obstruction reasons are:

```text
AA_common_source_product_not_square
BB_common_source_product_not_square
```

The sign / positivity / nondegeneracy reasons are separate:

```text
A_not_positive
B_not_positive
N_not_positive
M_not_positive
```

In particular, `M_not_positive` is not a squareclass failure. It can block
AA+BB admissibility, but it is not the common-source square obstruction lemma.
The squareclass failure alone is sufficient to route a point as
`not_admissible` under `wl491`.

## Decision

The point-level lemma is already provable from the existing `wl491` machinery.
No new point-level lemma is needed: `wl491` defines the centered-even pullback,
the two common-source square checks, and the ledger route.

The stronger cover-family reading is not proved. The `wl522` count of 15
globally soluble but not-admissible cover families is finite taxonomy data; it
does not prove that every rational point on those cover families must fail the
opposite-side squareclass condition. A uniform cover-family theorem would need
a new squareclass lemma.

Thus the candidate is:

```text
point-level obstruction: proved by existing wl491 contract
uniform cover-family obstruction: not proved here; needs a new lemma
finite-count theorem reading: too finite
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.json
```

with:

```text
status = ok
work_log = wl523
input_work_log = wl522
proof_statement_layer_only = true
proof_decision.point_level_lemma_status =
  provable_from_existing_wl491_machinery
proof_decision.cover_family_uniform_theorem_status =
  needs_new_uniform_squareclass_lemma
wl522_taxonomy_application.opposite_side_squareclass_failure_entry_count = 29
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
rank_zero_claimed = false
complete_selmer_upper_bound_proved = false
advance_to_wl524 = false
```

## Boundary

This work-log stops after `wl523`. It does not prove:

- a uniform cover-family squareclass obstruction;
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
post_wl523_route_choice_not_entered_here
```

That later gate should decide whether to attempt a new uniform cover-family
squareclass obstruction lemma, or return to the finite-shell route. Shell 11
remains unexecuted.
