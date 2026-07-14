# wl523-wl529 Common-Source Function-Field Squareclass Consolidated

## Scope And Status

This document is the consolidated human reading entry for wl523-wl529. It
follows the [491-522 AA+BB admissibility
history](491-522-aa-bb-admissibility-taxonomy-consolidated.md) and precedes the
[530-585 pure-v_ell M1/M2
history](530-585-pure-v-ell-m1-m2-consolidated-checkpoint.md).

The interval stays at the statement, route-choice, proof-data, and one-family
function-field prototype layers. It records accepted formulas, certificates,
exceptions, provenance, and theorem boundaries. It does not change the
research route and does not delete the seven source worklogs.

The document is human-only and runtime-independent:

~~~text
human_only = true
runtime_input = false
canonical_runtime_reads_this_file = false
ignored_results_are_not_runtime_inputs = true
~~~

The canonical executable destinations are:

~~~text
wl523 -> A2-LEMMA
wl524 -> A2-BOUNDARY
wl525 -> A2-BOUNDARY
wl526 -> A2-BOUNDARY
wl527 -> A0/A2 (tracked inventory input and boundary projection)
wl528 -> B0/B1 (selected wl495 rows and protected prototype evidence)
wl529 -> B1 (protected square-locus evidence)
~~~

## Provenance

The seven source worklog paths are retained as provenance strings:

~~~text
docs/work-logs/523-try-common-source-square-obstruction-lemma-candidate.md
docs/work-logs/524-post-wl523-route-choice-audit.md
docs/work-logs/525-attempt-uniform-cover-family-squareclass-obstruction-lemma.md
docs/work-logs/526-post-wl525-route-choice-audit.md
docs/work-logs/527-function-field-squareclass-proof-data-scope.md
docs/work-logs/528-v5-l1-t5-function-field-prototype.md
docs/work-logs/529-v5-l1-t5-square-locus.md
~~~

Their exact result paths, retained as historical provenance, are:

~~~text
wl523: results/closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.json
wl524: results/closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.json
wl525: results/closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.json
wl526: results/closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.json
wl527: results/closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.json
wl528: results/closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.json
wl529: results/closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json
~~~

The former executable and test paths remain provenance strings, not current
runtime imports:

| WL | Historical script | Historical test |
| --- | --- | --- |
| wl523 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.py | tests/test_closure_quotient_rank_zero_aa_bb_wl523_common_source_obstruction.py |
| wl524 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.py | tests/test_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice.py |
| wl525 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.py | tests/test_closure_quotient_rank_zero_aa_bb_wl525_uniform_cover_family_squareclass_obstruction.py |
| wl526 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.py | tests/test_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice.py |
| wl527 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.py | tests/test_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data.py |
| wl528 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.py | tests/test_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_prototype.py |
| wl529 | scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py | tests/test_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py |

The canonical tracked inputs and projections are:

| Destination | Path and role |
| --- | --- |
| A0 | data/theory/aa_bb/wl500/a0-inventory.v1.json; carries the wl527 named-family inventory |
| A2 | data/theory/aa_bb/wl500/a2-boundary-spec.v1.json; carries wl523-wl527 formulas, route boundaries, and no-claim fields |
| B0 | data/theory/aa_bb/wl500/b0-prototype-rows.v1.json; carries the two selected wl495 rows used by wl528-wl529 |
| B1 | data/theory/aa_bb/wl500/b1-sage-certificate.v1.json; carries the proved Sage rank/torsion/square-X certificate |
| A2 builder | scripts/theory/aa_bb/a2_evidence.py: load_boundary_spec, build_a2, project_a2 |
| B0 loader | scripts/theory/aa_bb/consolidation_inputs.py: B0Document, load_b0, to_wl528_view |
| B1 builder | scripts/theory/aa_bb/b1_prototype.py: load_sage_certificate, build_b1, project_b1, semantic_projection |
| B1 test | tests/theory/aa_bb/test_b1_prototype.py |

The bound source paths for the canonical inputs are:

~~~text
A0 inventory:
  source_work_log = wl527
  source_worklog_path = docs/work-logs/527-function-field-squareclass-proof-data-scope.md
  source_result_path = results/closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.json
  source_script_path = scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.py
  source_test_paths = tests/test_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data.py

B0 prototype rows:
  source_work_log = wl495
  source_worklog_path = docs/work-logs/archive/495-aa-bb-route-refreshed-support-through-ambient-c-d-solubility-then-wl491-filter.md
  source_result_path = results/closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json
  source_script_path = scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py
  source_test_paths = tests/test_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py

B1 Sage certificate:
  source_work_log = wl529
  source_selector = $.genus_one_certificate
  source_result_path = results/closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json
  source_script_path = scripts/theory/aa_bb/b1_prototype.py::_sage_program
~~~

The manifest and loader provenance strings are intentionally not rewritten in
this documentation cutover. In particular, source_work_log,
source_worklog_path, source_result_path, source_script_path, and
source_test_paths continue to identify the original evidence. Canonical
loaders use tracked A0/B0/B1 data and do not load the ignored results paths.

## wl523 Point-Level Lemma

The wl522 input snapshot is:

~~~text
final_candidate_ledger_entry_count = 43
support_family_count = 13
cover_family_count = 22
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
globally_soluble_but_not_aa_bb_admissible_entry_count = 29
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
~~~

The touched object layer is only:

~~~text
complete d-coordinate ambient C_d point
  -> wl491 centered-even pullback
  -> AA+BB common-source admissibility obstruction
~~~

Let A,B > 0. If an ambient global C_d point is on source quotient AA with
L=A, or source quotient BB with L=B, and the certified wl491 centered-even
pullback gives rational N,M, define

~~~text
P_A = (N^2 + A^2)(M^2 + A^2)
P_B = (N^2 + B^2)(M^2 + B^2).
~~~

For an AA source the opposite-side product is P_B. For a BB source it is P_A.
If that opposite-side product is not a rational square, the point is not
AA+BB-admissible and remains in the globally soluble but not AA+BB-admissible
ledger.

The squareclass failure reasons are distinct:

~~~text
AA_common_source_product_not_square
BB_common_source_product_not_square
~~~

The sign and nondegeneracy reasons remain separate:

~~~text
A_not_positive
B_not_positive
N_not_positive
M_not_positive
~~~

In particular, M_not_positive is not a squareclass failure. It can independently
block admissibility, while the squareclass failure alone is sufficient for the
wl491 not_admissible route.

The accepted decision is:

~~~text
point_level_lemma_status = provable_from_existing_wl491_machinery
cover_family_uniform_theorem_status = needs_new_uniform_squareclass_lemma
finite_count_is_not_a_family_theorem = true
~~~

The result artifact is status=ok and records no new point filter, no shell 11,
no new support, no final candidate, no complete Selmer bound, and no rank-zero
or Sha claim.

## wl524 Route Choice

wl524 compares the next route at the cover-family statement layer. The selected
gate is:

~~~text
attempt_uniform_cover_family_squareclass_obstruction_lemma
~~~

It is selected because wl523 closes the point-level statement but leaves the
named question of uniform non-squareness on the globally soluble but
not-AA+BB-admissible families. The selected gate is not entered by wl524.

The route state carried forward is:

~~~text
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
globally_soluble_but_not_aa_bb_admissible_entry_count = 29
opposite_side_squareclass_failure_entry_count = 29
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
active_final_obstruction_candidate_count = 0
selected_next_gate.entered_here = false
selected_route_entered_here = false
~~~

The result artifact is status=ok and records
advance_to_wl525 = false.

Returning to finite shell 11 M_tail diagnostics, naming a theorem-level local
or Hilbert row, and selecting a final obstruction candidate are all deferred
or rejected at this stop. No shell 11, new support, new ambient C_d test, new
wl491 point filter, broad rank/Selmer diagnostic, or package-x/S~ bridge is
entered.

## wl525 Failed Promotion

The attempted uniform target is:

~~~text
For every rational ambient C_d point on each named wl522 globally soluble but
not AA+BB-admissible cover family that has a certified wl491 centered-even
pullback, the opposite-side common-source product is non-square in Q*/Q*2.
~~~

A genuine proof would require, for every named family:

- a cover-family model and rational source-side map;
- N and M as rational functions on the cover-family function field;
- the opposite-side product as a function-field element;
- a function-field nonsquare or divisor-parity certificate that survives the
  required rational specializations;
- uniform control of poles, zeroes, exceptional divisors, positivity, and
  nondegeneracy.

The finite wl522 taxonomy supplies none of these function-field data. The
accepted failure is:

~~~text
finite_taxonomy_has_no_uniform_squareclass_certificate
attempt_decision.failure_point = missing_function_field_squareclass_certificate
attempt_decision.finite_taxonomy_promotion_status = refuted
attempt_decision.mathematical_uniform_lemma_refuted = false
uniform_cover_family_lemma_status = not_proved_from_wl523_wl524_inputs
~~~

Here refuted applies only to the inference from finite taxonomy to a uniform
theorem. It does not refute the mathematical uniform lemma as a possible
future statement.

The result artifact is status=ok and records
stop_after_current_task = true.

## wl526 Route Choice

wl526 compares exactly these four route families:

~~~text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
return_to_finite_shell_m_tail_diagnostics
name_theorem_level_complete_selmer_local_hilbert_row_obligation
abandon_this_obstruction_line_and_select_different_candidate
~~~

The selected later gate is:

~~~text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
selected_next_gate.entered_here = false
function_field_models_built_here = false
function_field_squareclass_certificate_proved_here = false
uniform_cover_family_lemma_proved_here = false
~~~

The finite-shell, theorem-level local/Hilbert, and different-candidate routes
are not entered. No new support, ambient C_d solubility test, wl491 filter,
final candidate, complete Selmer bound, rank-zero claim, or Sha claim is made.

The result artifact is status=ok and records
advance_to_selected_next_gate = false and stop_after_current_task = true.

## wl527 Proof-Data Inventory

wl527 inventories the 15 named globally soluble but not-AA+BB-admissible cover
families:

~~~text
support=u_3|L=3|T=4|d=(?,?,?)
support=u_3+v_13|L=3|T=13|d=(39,3,13)
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)
support=u_3+v_5+w_53|L=9|T=10|d=(15,159,265)
support=u_5|L=10|T=11|d=(5,5,1)
support=u_5|L=10|T=19|d=(5,5,1)
support=u_7|L=7|T=9|d=(7,7,1)
support=u_7+v_13+w_5|L=7|T=13|d=(91,35,65)
support=u_7+v_17+w_5|L=7|T=17|d=(119,35,85)
support=u_7+w_37|L=7|T=10|d=(7,259,37)
support=v_13|L=6|T=13|d=(13,1,13)
support=v_13|L=9|T=13|d=(13,1,13)
support=v_17+w_13|L=10|T=17|d=(17,13,221)
support=v_5|L=1|T=5|d=(5,1,5)
support=v_5|L=2|T=5|d=(5,1,5)
~~~

Fourteen rows have a label plus L,T,d data. The first row has only its family
label and L,T, with d=(?,?,?) absent from the wl522 taxonomy. None of the 15
rows has an explicit cover-family equation, function-field coordinates,
rational source-side map, N,M function-field elements, or a proved
opposite-side squareclass/divisor-parity certificate.

The only available later-proof targets are formulas:

~~~text
AA source target: (N^2 + B^2)(M^2 + B^2)
BB source target: (N^2 + A^2)(M^2 + A^2)
~~~

The readiness decision is:

~~~text
scope_summary.named_cover_family_count = 15
scope_summary.named_entry_count = 29
scope_summary.ready_for_later_uniform_squareclass_proof_attempt = false
scope_summary.ready_cover_family_count = 0
scope_summary.not_ready_cover_family_count = 15
scope_summary.exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
cover_families_missing_explicit_d_vector_count = 1
~~~

This is a proof-data insufficiency statement, not a refutation of a future
uniform lemma.

## wl528 Selected Prototype

The selected family is:

~~~text
support=v_5|L=1|T=5|d=(5,1,5)
AA_A1_B4_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
~~~

The wl495 complete d-coordinate equations are:

~~~text
X - 42 = 5*u_minus_p^2
X - 58 = u_pos_2sqrt_q^2
X + 58 = 5*u_neg_2sqrt_q^2

5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16
u_minus_p^2 - u_neg_2sqrt_q^2 = -20
~~~

With the chart r = u_neg_2sqrt_q + u_minus_p, the prototype function field and
maps are:

~~~text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))

u_minus_p = (r^2 - 20)/(2*r)
u_pos_2sqrt_q = y/(2*r)
u_neg_2sqrt_q = (r^2 + 20)/(2*r)
X = 42 + 5*((r^2 - 20)/(2*r))^2
Y = 5*y*(r^4 - 400)/(8*r^3)
~~~

The chart excludes at least:

~~~text
r = 0
r^2 = 20
X+p = 0
~~~

The centered-even source map and the two source coordinates are:

~~~text
t = Y/(2*(X+p)) = y*(r^2+20)/(4*r*(r^2-20))
z = X/2 - t^2
N = (5+t)/2
M = (5-t)/2
~~~

Both selected entries have source leg L=1, so the source-side product is:

~~~text
(N^2+1)(M^2+1) = (z/4)^2
~~~

The AA/BB symmetry sends the opposite leg to 4 for both rows:

~~~text
AA_A1_B4: opposite product = (N^2+16)(M^2+16)
BB_A4_B1: opposite product = (N^2+16)(M^2+16)

(N^2+16)(M^2+16)
  = ((t^2 + 89)^2 - 100*t^2)/16
~~~

At the checked smooth nonexceptional specialization:

~~~text
r = 10
y = 160
u_minus_p = 4
u_pos_2sqrt_q = 8
u_neg_2sqrt_q = 6
X = 122
Y = 960
t = 6
N = 11/2
M = -1/2
~~~

The point lies on the quartic, is smooth, satisfies the chart/open-denominator
checks, maps to the recorded wl495 cover point and induced E point, and has
regular nonzero opposite product:

~~~text
(N^2+16)(M^2+16) = 12025/16
12025/16 = 5^2*13*37 / 2^4
~~~

Therefore the opposite product is not a square in the prototype function
field: a square function would have square residue at a smooth rational point
where it is regular and nonzero. This is a specialization certificate, not a
divisor-parity certificate.

The checked specialization has M<0. That positivity failure is separate from
the nonsquare certificate and is not used to prove function-field
nonsquareness. The B1 exception ledger retains y=0, t=0, the chart poles, and
all other unclassified zero loci separately; no zero locus is silently merged
into the positive nonexceptional domain.

## wl529 Square-Locus Closure

For P=(N^2+16)(M^2+16), the centered-even parameter gives:

~~~text
16*P = (t^2+39)^2 + 6400
U^2 = t^4 + 78*t^2 + 7921
U = 4*s
~~~

The quartic

~~~text
D: U^2 = t^4 + 78*t^2 + 7921
~~~

is squarefree and smooth of genus one. On the wl528 prototype quartic:

~~~text
y^2 = 5*r^4 - 264*r^2 + 2000

16*r^2*(r^2-20)^2*t^2
  = (r^2+20)^2*(5*r^4-264*r^2+2000)
~~~

The square locus also has the smooth intersection-of-quadrics model:

~~~text
V*Z = T^2 + 39*Z^2
U^2 = V^2 + 6400*Z^2
~~~

It admits the one-way degree-two quotient map:

~~~text
E: Y^2 = X^3 + 78*X^2 + 7921*X
X = t^2
Y = t*U
~~~

The elliptic curve classifies rational points on the quartic through this map.
It is not claimed to be a birational equivalence, and no converse from an
arbitrary rational point on E is claimed.

The tracked Sage proof certificate is:

~~~text
rank(E(Q)) = 0
E(Q)_tors ~= Z/4Z
E(Q) = {O, (0,0), (89,1424), (89,-1424)}
square rational X-values = {0}
~~~

Consequently the affine rational points on D are exactly:

~~~text
(t,U) = (0,89), (0,-89)
~~~

The remaining exceptional branch is t=0. With x=r^2, its prototype preimage
equation is:

~~~text
5*x^2 - 264*x + 2000 = 0
discriminant = 29696 = 2^10*29
~~~

The discriminant is not a rational square, so t=0 has no rational lift to the
wl528 quartic. The certificate also records that t=0 forces y=0. Thus no
rational point on the selected prototype with |t|<5 has a square opposite-side
product.

The exact one-family conclusion is:

~~~text
one_family_positive_square_obstruction_proved_here = true
uniform_cover_family_obstruction_proved_here = false
~~~

The positive source condition used by the square-locus audit is:

~~~text
|t| < 5
N=(5+t)/2 > 0
M=(5-t)/2 > 0
~~~

This closes the selected v_5|L=1|T=5|d=(5,1,5) square locus only. It does not
promote the result to another family or to a uniform theorem.

## Consolidated No-Claim Boundary

The wl523-wl529 interval does not prove:

- a uniform cover-family squareclass obstruction;
- a divisor-parity certificate for the wl528 prototype;
- specialization survival for every rational point in every named family;
- a new local or Hilbert row;
- shell 11, a new M_tail row, or uniform M_tail full rank;
- new ambient C_d solubility or AA+BB admissibility for a new point/support;
- a final obstruction candidate or any family exclusion theorem;
- a complete Selmer upper bound, dim Sel_2(E)=2, rank zero, or Sha[2]=0;
- a package-x/S~ theorem-level bridge;
- M3 or a later roadmap step.

The finite-taxonomy promotion in wl525 is refuted only as an inference from
finite counts. The possible mathematical uniform lemma remains undecided.
The wl528 specialization proves only a function-field nonsquare, and wl529
closes rational square specializations in the required |t|<5 domain for that
single prototype. The Sage rank statement is a certificate about the single
elliptic quotient used in that one-family analysis, not a theorem about the
research elliptic curve or the global AA+BB problem.

## Cutover Reading Route

The current human route is:

~~~text
491-522 -> 491-522-aa-bb-admissibility-taxonomy-consolidated.md
523-529 -> 523-529-common-source-function-field-squareclass-consolidated.md
530-585 -> 530-585-pure-v-ell-m1-m2-consolidated-checkpoint.md
wl586/wl593 -> scripts/theory/aa_bb/d4_factor_twist.py semantic projections
protected appendices -> wl587, wl589, wl590, wl591, wl592 worklogs
downstream context -> wl594 and wl595 worklogs
~~~

The five protected appendices remain separate because their fixed D0/local-image
kernels, formulas, branch tables, survivor ledgers, and no-claim boundaries
are independent evidence. This cutover does not edit those appendices, the D4
module, the manifest, loaders, code, tests, data, results, task anchors, or
wl594+.
