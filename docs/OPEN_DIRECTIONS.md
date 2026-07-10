# Open Directions

This document keeps only directions that are still worth considering. Detailed
history belongs in the worklogs, not here.

## P0: Missing Function-Field Proof Data After wl527

Current handoff:

```text
wl527_completed_function_field_proof_data_scope_not_ready
```

Input state:

- `wl522` compressed the `wl491`-`wl521` AA+BB admissibility ledgers.
- The taxonomy has no genuinely deferred cover family.
- The taxonomy has no AA+BB-admissible cover family.
- `wl523` tried the named theorem-candidate:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

`wl523` records that the point-level obstruction is already provable from
`wl491`: once the centered-even pullback gives rational `N,M`, a non-square
opposite-side common-source product blocks AA+BB admissibility. It also records
that this is not a uniform cover-family theorem.

`wl524` decided the route choice and selected a later attempt at a new uniform
squareclass lemma for those cover families. `wl524` did not enter that proof
attempt. The attempt must not use the 15 cover-family count as proof, and it
must not claim a theorem-level Selmer upper bound unless one is actually
proved.

`wl525` entered the selected attempt and found the precise failure point:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

The finite taxonomy does not provide cover-family function-field models,
rational `N,M` maps, divisor parity data, or a specialization argument for the
opposite-side product. The uniform lemma is therefore not proved from
`wl523` / `wl524`. This does not refute the possible lemma; it refutes only
the finite-taxonomy promotion.

`wl526` made that route choice. It compared exactly four route families and
selected only a later minimal function-field proof-data scoping gate for the
named cover families. The selected gate should inventory cover-family models,
source-side maps, candidate `N,M` function-field elements, the opposite-side
product squareclass/divisor-parity certificate target, and exceptional
specialization / positivity separation. `wl526` did not enter that gate, build
function-field models, prove the uniform lemma, name a theorem-level
complete-Selmer row, abandon the obstruction line, or select a different
candidate.

`wl527` entered only that proof-data scoping gate. It found that the current
data is not ready for a later uniform squareclass proof attempt:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

The exact missing data classes are explicit cover-family function-field
models, rational source-side maps on each family, `N,M` as function-field
elements, an opposite-side product squareclass/divisor-parity certificate, and
exceptional specialization / positivity separation. One named row also lacks
an explicit `d` vector in the `wl522` taxonomy label. `wl527` does not build
those objects, prove the uniform lemma, refute the possible mathematical
lemma, or advance to another roadmap step.

## P1: Return To Selmer Family Proof Only With A Named Gap

The high-level rank-zero/Selmer route still needs:

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

Enter this direction only when the next proof obligation is named precisely.
More finite samples, packages, or route counts do not by themselves advance a
theorem-level Selmer upper bound.

## P2: Finite Shell Extension

The previous finite-shell machinery selected a later shell extension at:

```text
max(A,B) = 11
```

This is lower priority than the explicit post-`wl527` missing function-field
proof-data gap. Execute shell 11 only if the user explicitly chooses this
route, and keep it classified as finite `M_tail` diagnostic work rather than
Selmer theorem progress.

## Closed Or Paused Directions

- The old package-`x` / `S~` bridge is deprecated as a theorem bridge.
- `M_tail` diagnostics are parameter-dependent; do not claim uniform full rank
  from finite shell counts.
- Ambient `C_d` global points must pass the `wl491` AA+BB common-source
  admissibility filter before entering any admissible-point ledger.
- Globally soluble but not AA+BB-admissible ledgers are diagnostic failures,
  not obstruction candidates.

Older long direction lists are archived under `docs/archive/` and the
consolidated worklogs.
