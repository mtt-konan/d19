# Next Research Gate

This page is the short handoff for the next agent. It names the current gate,
the closed route state, and the moves that must not be reopened accidentally.

## Current Gate

If `wl529` is present, the current handoff is:

```text
wl529_v5_l1_t5_square_locus_complete_stop
```

`wl529` keeps the same user-selected prototype from `wl528`. It still touches
only:

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented by `AA_A1_B4_v_5_m_tail_refresh_candidate` and
`BB_A4_B1_v_5_m_tail_refresh_candidate` in `wl495`.

`wl528` already reconstructs the function-field chart

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

with

```text
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

and proves the opposite-side product `(N^2+16)(M^2+16)` is nonsquare as a
function-field element.

`wl529` closes the remaining pointwise specialization gap for this one family.
It starts from the exact identity

```text
16*(N^2+16)*(M^2+16) = (t^2+39)^2 + 6400
```

so the square-specialization locus becomes the genus-one quartic

```text
U^2 = t^4 + 78*t^2 + 7921
```

with the smooth intersection-of-quadrics model

```text
V*Z = T^2 + 39*Z^2
U^2 = V^2 + 6400*Z^2
```

and a degree-two map to the elliptic quotient

```text
Y^2 = X^3 + 78*X^2 + 7921*X
```

via `X=t^2`, `Y=tU`. This map is used for rational-point classification; it
is not asserted to be a birational equivalence.

The `wl529` script checks this algebra symbolically, then proves

```text
rank(E(Q)) = 0
E(Q)_tors ~= Z/4Z
E(Q) = {O, (0,0), (89,1424), (89,-1424)}.
```

Any rational square specialization would map to `E(Q)` with `X=t^2` a rational
square. The only square `X`-value among finite rational points is `X=0`, so the
affine square-locus rational points are only

```text
(t,U) = (0,89), (0,-89).
```

`wl529` then checks that `t=0` has no rational lift back to the `wl528`
quartic because writing `x=r^2` gives

```text
5*x^2 - 264*x + 2000 = 0
```

with discriminant `2^10*29`, not a rational square.

Therefore the selected prototype has no rational point in the required
nonexceptional positivity domain `|t|<5` where the opposite-side product is a
rational square. This closes the one-family square-locus question and stops.

Divisor parity remains separate:

```text
Divisor parity can prove generic function-field nonsquareness, but by itself it
cannot rule out every rational specialization landing on a square value.
```

This is still not a uniform cover-family theorem, not a theorem-level Selmer
upper bound, not rank zero, not `Sha[2]=0`, and not family exclusion.

Do not advance to another family from `wl529` without a new explicit user
selection.

If `wl528` is present but `wl529` is not present, the current handoff is:

```text
wl528_v5_l1_t5_function_field_prototype_partial
```

`wl528` is the first user-selected prototype after `wl527`. It proves the
opposite-side product is nonsquare in the prototype function field by a checked
smooth nonexceptional rational specialization, but it does not yet close the
pointwise positivity-domain specialization gap.

If `wl527` is present, the current handoff is:

```text
wl527_completed_function_field_proof_data_scope_not_ready
```

`wl527` uses `wl526` as immediate input and enters only the selected
cover-family function-field proof-data scoping gate. It inventories the 15
`wl522` globally soluble but not AA+BB-admissible cover families and asks
whether the current data is ready for a later uniform squareclass proof
attempt.

The answer is no:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

The missing data classes are explicit cover-family function-field models,
rational source-side maps, `N,M` as function-field elements, an opposite-side
product squareclass or divisor-parity certificate, and exceptional
specialization / positivity separation. One row,
`support=u_3|L=3|T=4|d=(?,?,?)`, also lacks an explicit `d` vector in the
`wl522` taxonomy row.

`wl527` does not prove the uniform lemma, refute the possible mathematical
lemma, build a function-field engine, execute shell 11, compute new `M_tail`
supports, test new ambient `C_d` solubility, apply `wl491` to a new point,
name a theorem-level Selmer row, select a final obstruction candidate, or
claim theorem-level progress. No next roadmap step is entered here.

If `wl526` is present but `wl527` is not present, the current handoff is:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

`wl526` uses `wl525` as immediate input and is only a route-choice audit. It
compares exactly four next-route families:

- gather minimal function-field squareclass proof data for the named cover
  families;
- return to finite shell / `M_tail` diagnostics;
- name a theorem-level complete-Selmer local/Hilbert row obligation;
- abandon this obstruction line and select a different candidate.

The selected later gate is the first route: scope the minimum function-field
proof data needed for the named cover families. That means an inventory of
cover-family models, source-side maps, candidate `N,M` function-field
elements, an opposite-side product squareclass or divisor-parity certificate
target, and exceptional specialization / positivity separation.

This selected gate is not entered in `wl526`. No function-field models are
built, no uniform lemma is proved, no complete-Selmer row obligation is named,
and no candidate is selected or abandoned.

If `wl525` is present but `wl526` is not present, the current handoff is:

```text
wl525_completed_no_next_gate_entered
```

`wl525` entered the `wl524` selected gate:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

It tried to promote the point-level `wl491` opposite-side squareclass
obstruction to a uniform statement over the `wl522` globally soluble but not
AA+BB-admissible cover families. The attempt failed at the statement/proof
input layer:

```text
finite_taxonomy_has_no_uniform_squareclass_certificate
```

The finite 15 cover-family / 29 entry taxonomy records point-level
non-admissibility checks. It does not contain cover-family function-field
models, rational `N,M` maps, divisor parity data, or a specialization argument
showing that the opposite-side product is non-square for every rational point
on each cover family. Therefore the finite taxonomy cannot be promoted to a
uniform theorem from the current inputs.

This does not mathematically refute a possible future uniform lemma. It only
refutes the attempted proof from `wl523` / `wl524` data. No next roadmap step
is entered in `wl525`.

If `wl524` is present but `wl525` is not present, the current handoff is:

```text
attempt_uniform_cover_family_squareclass_obstruction_lemma
```

`wl524` is only a route-choice audit. It uses `wl523` as input, compares the
post-`wl523` options, and selects a later attempt at a new uniform
cover-family squareclass obstruction lemma as the next narrow gate. That gate
is not entered in `wl524`.

The selected later question is whether the opposite-side common-source
product can be proved non-square uniformly on the named globally soluble but
not AA+BB-admissible cover families, without treating finite counts as proof
and without claiming a Selmer upper bound. Returning to finite shell 11
`M_tail` diagnostics is deferred. Proof-level local / Hilbert row work is
deferred until a specific Selmer row obligation is named. Final obstruction
candidate selection is rejected because there is no AA+BB-admissible cover
family, no genuinely deferred cover family, and no active final obstruction
candidate.

If `wl523` is present but `wl524`, `wl525`, `wl526`, and `wl527` are not
present, the current handoff is:

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
- `docs/work-logs/524-post-wl523-route-choice-audit.md`
- `docs/work-logs/525-attempt-uniform-cover-family-squareclass-obstruction-lemma.md`
- `docs/work-logs/526-post-wl525-route-choice-audit.md`
- `docs/work-logs/527-function-field-squareclass-proof-data-scope.md`
- `docs/work-logs/528-v5-l1-t5-function-field-prototype.md`
- `docs/work-logs/529-v5-l1-t5-square-locus.md`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.py`
- `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl523_common_source_obstruction.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl525_uniform_cover_family_squareclass_obstruction.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_prototype.py`
- `tests/test_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`
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
- treat `wl527` proof-data scoping as a uniform cover-family theorem or as a
  ready proof attempt.
- treat `wl528` as more than one checked single-prototype nonsquare
  certificate.
- treat `wl529` as more than one closed one-family positivity-domain
  square-locus audit.

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
  -> post-wl523 route choice selects uniform cover-family lemma attempt (wl524)
  -> uniform cover-family squareclass obstruction attempt fails from finite taxonomy (wl525)
  -> post-wl525 route choice selects minimal function-field proof-data scoping (wl526)
  -> function-field proof-data scoping finds missing model/map/certificate data (wl527)
  -> one selected v_5 L=1 T=5 function-field nonsquare prototype (wl528)
  -> same prototype square-locus closes in the nonexceptional positivity domain (wl529)
```

`wl529` supplies one closed one-family positivity-domain square-locus audit and
stops. It is not another finite shell computation, not a new point-level
filter run, not a divisor-parity theorem, not the uniform lemma itself, and
not a Selmer-family theorem claim unless a rigorous Selmer upper bound is
actually proved.
