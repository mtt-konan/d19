# Next Research Gate

This page is the short handoff for the next agent. It names the current gate,
the closed route state, and the moves that must not be reopened accidentally.

## Current Gate

If `wl523` is present, the current handoff is:

```text
post_wl523_route_choice_not_entered_here
```

`wl523` tried the named common-source square obstruction lemma candidate at the
proof/statement layer. The point-level obstruction is already provable from
the existing `wl491` machinery: after a certified centered-even pullback gives
rational `N,M`, the opposite-side product

```text
AA source: (N^2+B^2)(M^2+B^2)
BB source: (N^2+A^2)(M^2+A^2)
```

being a non-square in `Q*/Q*2` is sufficient to route the point as
`not_admissible`. Sign/positivity failures such as `M_not_positive` are
separate admissibility failures, not squareclass failures.

The stronger cover-family theorem is not proved. The 15 globally soluble but
not AA+BB-admissible cover families from `wl522` are finite taxonomy data; a
uniform claim that every rational point on those cover families fails the
opposite-side squareclass condition would need a new lemma. The next gate, if
chosen, is only a route choice between attempting that new uniform
cover-family squareclass lemma and later returning to the finite-shell route.

If `wl522` is present but `wl523` is not present, the current handoff is:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

The next narrow question is whether the recorded opposite-side AA/BB
common-source product-not-square failures can be stated and proved as a
reusable admissibility obstruction lemma:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

This lemma candidate has not been proved. No proof-level work was entered in
`wl522`.

## Evidence Snapshot

`wl522` uses `wl521` as the latest state and compresses the `wl491`-`wl521`
ledgers into a stable support/cover taxonomy by classification and failure
mode:

- 43 final candidate-ledger entries.
- 13 support families.
- 22 cover families.
- 5 ambient-globally-not-soluble cover families.
- 15 globally soluble but not AA+BB-admissible cover families.
- 2 processed / duplicate cover families.
- No genuinely deferred cover families.
- No AA+BB-admissible cover families.

The important current classification is:

```text
ambient globally soluble but not AA+BB-admissible
```

For the original `u_3` diagnostic point, the ambient `C_d` point pulls back to
the `AA` quotient with:

```text
N = 4
M = 0
```

but it fails the `BB` common-source closure condition because:

```text
(N^2+B^2)(M^2+B^2) = 17
```

which is not a rational square. This point is therefore neither an obstruction
candidate nor an AA+BB-admissible point.

For the full route history, read:

- `docs/work-logs/522-support-cover-taxonomy-to-lemma-candidate-checkpoint.md`
- `docs/work-logs/523-try-common-source-square-obstruction-lemma-candidate.md`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl523_common_source_obstruction.py`
- `docs/work-logs/README.md`

## Do Not Reopen

Unless the user explicitly asks for one of these, do not:

- execute shell 11;
- compute new supports;
- test new ambient `C_d` solubility;
- apply `wl491` to a new point;
- select a final obstruction candidate;
- run broad rank/Selmer diagnostics;
- claim rank zero, a Selmer upper bound, uniform `M_tail` full rank, family
  exclusion, or Harborth global theorem;
- treat the finite count of 15 not-admissible cover families as theorem
  progress.

Do not go back to the old package-`x` / `S~` bridge as if it were a complete
Selmer object. `S~` was a pseudo-container; it is not the theorem-level
`Sel_2(E_L/Q)`.

## Current Route Line

The corrected line is the complete `d`-coordinate route:

```text
complete d-container
  -> local C_d rows
  -> torsion baseline
  -> parameter-dependent M_tail diagnostics
  -> ambient C_d global points
  -> AA+BB common-source admissibility filter (wl491)
  -> support/cover taxonomy (wl522)
  -> point-level common-source square obstruction statement (wl523)
  -> post-wl523 route choice not entered
```

The next task, if chosen, is route-choice work only. It is not another finite
shell computation and not a Selmer-family theorem claim.
