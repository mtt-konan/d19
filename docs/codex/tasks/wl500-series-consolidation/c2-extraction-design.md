# C2 Extraction Design: wl542-wl568

## Verdict

```text
worker_outcome = c2_extraction_design_ready
design_ready = true
implementation_status = not_started
scope = wl542-wl568 only
claim_boundary = M2 remains open; M3 remains closed
```

The read-only audit is complete. All 27 worklogs, 27 legacy audit scripts,
and 27 legacy test files are present. The legacy scripts form one recursive
predecessor chain and each legacy test starts its own strict CLI subprocess.
Only seven of the 27 ignored result payloads are present in the current
worktree: `wl542-wl547` and `wl568`. The other 20 expected result paths are
recorded below explicitly. This is a parity-fixture readiness risk, not a
design ambiguity: the new runtime must never depend on those files, and the
parity test must fail closed until every explicit source is available.

This document proposes only structural extraction. It does not add a
mathematical claim, repair a legacy formula, enter `wl569+`, run shell 11,
perform Selmer/rank work, cut over a consumer, delete a legacy file, or run
the full suite.

## Audit Findings

The legacy chain has these properties:

- `wl542` imports and builds the legacy `wl541` payload; `wl543-wl568` each
  import and rebuild their immediate legacy predecessor.
- The scripts write one result path each, accept `--strict`, print all
  `proof_status` flags, and make strict mode fail only when the payload
  status is not `ok`.
- The tests repeat the same pattern: in-process algebra or finite witnesses,
  a predecessor fail-closed test, exact claim-boundary assertions, and one
  subprocess test per worklog.
- The scripts use only the existing Python/SymPy stack for executable
  certificates. No legacy script reads a result payload as runtime input;
  result files are test evidence only.
- The old payloads contain execution fields (`ready`, `violations`) alongside
  mathematical fields. The former must not become trusted proof inputs.
- `wl545-wl568` continue the trivial real-unit branch selected in `wl544`.
  The at-most-two-unit-class statement in `wl543-wl544` remains a union of
  branches; the later trivial-unit descent is not a closure of the
  nontrivial unit branch.

The new C2 implementation therefore replaces repeated recursive execution,
not mathematical evidence. It recomputes the exact identities, finite
certificates, witnesses, flags, and final boundary from direct canonical
kernels.

## Protected Kernels

Every row in the following table is protected evidence. A canonical kernel
may change representation and helper names, but it may not change the
displayed formulas, quantifiers, exceptional branches, witness coordinates,
or theorem strength.

| Kernel | Protected content | Final boundary |
| --- | --- | --- |
| `D-SUPPORT` (`wl542`) | Primitive `A^2+Q^2=ell*D^2`, `C^2=ell*Q^2+4*D^2`; odd `D`, `gcd(D,ell)=1`; complete splitting of every denominator prime in `Q(i,sqrt(ell))`; `D mod ell` a nonzero square; all three negative-valuation square conditions locally compatible. | Denominator places add no obstruction; no point or uniform exclusion. |
| `D-RQ` (`wl543-wl544`) | Totally positive integral `alpha=(C+Q*sqrt(ell))/2`, square ideal, prime-discriminant ordinary class-group 2-torsion elimination, at most two totally positive unit squareclasses, explicit `F,H,N` forms, exact `Z` and `W` squares, converse reconstruction, and the trivial-unit branch. | Exact branch reduction only; no theorem-level Selmer or family claim. |
| `D-2ADIC` (`wl545`) | `ell=5 mod 8` forces `v_2(q)=0` and odd `u,v`; `ell=1 mod 8` forces `v_2(q)>=3` and even `u,v` with opposite-parity halves; `G_ell` adds no standalone 2-adic obstruction. | Both allowed trivial-unit branches remain open. |
| `D-GAUSS` (`wl546-wl548`) | Gaussian UFD factorization into exactly the `B_pi` and `R_pi` orientations; finite Gaussian support for `G`; root polynomial `t^2+4*t-4`; exact `v_(1+i)(delta)=0` or `4`; `1+i` removed from the squarefree factor. | Finite Gaussian squareclasses remain; they are not Selmer classes. |
| `D-LOCAL` (`wl549-wl552`) | Root-square classification, automatic `1-t=t^2/4` and `t+4=4/t`, Hilbert-90 compatibility of both orientations, norm pairing to rational `r`, and parity forcing `eta=i` with both mod-8 coordinate systems. | Same-prime local analysis is exhausted; the coordinate system remains unsolved. |
| `D-CONE` (`wl553-wl557`) | Exact positivity transfer to `C_ell(m,n)`, uniform cone witnesses, `r=sqf_odd(gcd(ell-1,R))`, unit-free `Z=r*(a+i*b)^2`, one selected orientation per mod-8 branch, and exact `v_2(B_pi)` strata. | Positivity and standalone dyadic analysis do not close the selected branch. |
| `D-CHAR` (`wl558-wl562`) | Split/inert character cases at every odd `p|ell-1`, normalized leading character, the `F_2` matrix and reciprocity cancellation, and the exact `p=13` witnesses showing both row bits survive either orientation. | No uniform character contradiction; local orientation does not determine the global row. |
| `D-ALLOC` (`wl563-wl568`) | Product squareclass split `a=g*alpha*M^2`, `b=g*beta*N^2`, `alpha*beta=kappa`; dyadic/inert/split allocation rules; quartic signs; affine rows; exact scale/cone rewrites; automatic rows on an actual factorization; and the ordered signed-ratio warning. | Allocation adds no independent obstruction. The remaining exact lemma is the selected `B_pi`/`R_pi` orientation intersected with `F^2+E^2` square and strict positivity. |

The following no-claim fields are protected at every stage, whether they
occur at the top level or inside `proof_status` in the old payload:

```text
complete_selmer_upper_bound_proved = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_full_wl535_obstruction_proved_here = false
advance_to_m3 = false
```

The canonical output also preserves `rational_wl535_point_produced_here =
false` wherever the legacy payload has that top-level field; `wl542` carries
it only inside `proof_status`. The output also preserves the legacy
stage-specific false fields such as
`global_character_system_solved_here`,
`selected_orientation_norm_intersection_solved_here`, and
`theorem_level_selmer_matrix_claimed`.

## Canonical Shape And APIs

No new tracked data file is needed. All C2 evidence is symbolic, finite, or
an exact witness already present in the legacy scripts and tests.

Proposed files:

```text
scripts/theory/aa_bb/c2_global_descent.py
scripts/theory/aa_bb/c2_character_system.py
scripts/theory/aa_bb/c2_allocation.py
scripts/theory/aa_bb/c2_pure_v_ell.py
tests/theory/aa_bb/test_c2_global_descent.py
tests/theory/aa_bb/test_c2_character_system.py
tests/theory/aa_bb/test_c2_allocation.py
tests/theory/aa_bb/test_c2_cli.py
```

The three slice modules are mathematical kernels. The fourth module is only
the orchestrator, projection boundary, and CLI:

```python
build_c2_global_descent(c1_wl541) -> dict[str, dict[str, Any]]
build_c2_character_system(wl552) -> dict[str, dict[str, Any]]
build_c2_allocation(wl562) -> dict[str, dict[str, Any]]

@dataclass(frozen=True)
class C2Evidence:
    stages: dict[str, dict[str, Any]]

def build_c2(c1=None) -> C2Evidence
def project_stage(evidence, work_log) -> dict[str, Any]
def semantic_projection(payload, work_log) -> dict[str, Any]
```

`build_c2()` obtains `wl541` through the public canonical C1 API when no C1
argument is supplied, then runs the three slices once in order. It must not
expose or call 27 replacement functions that mirror the old recursive API.
The stage labels in `C2Evidence.stages` are exactly
`wl542`, ..., `wl568`, in numeric order.

`project_stage()` rejects unknown or mislabeled stages. `semantic_projection()`
rejects unlisted top-level fields, removes only `ready` and `violations`, and
compares all remaining allowlisted values recursively. It does not normalize
formula strings, signs, list order, proof flags, witnesses, or boundary text.
JSON object key order and CLI formatting are the only ignored differences.

## Obligation And Parity Map

The destination column names the canonical stage projection, not a new
mathematical worklog. The allowlist column names the exact semantic sections
that must survive old/new parity. Each row also retains the exact
stage-specific `proof_status` keys listed below.

### Slice 1: wl542-wl552

| WL | Canonical destination | Semantic allowlist | Required obligation and parity witness |
| --- | --- | --- | --- |
| `wl542` | `c2_global_descent.py`, `stages["wl542"]` | `denominator_support`, `local_converse` | Preserve all primitive equations, three prime conditions, complete splitting, `D mod ell`, the two principal-unit factorizations, the `q` negative-valuation scope, and the exact claim flags. |
| `wl543` | `c2_global_descent.py`, `stages["wl543"]` | `descent`, `unit_squareclass_split`, `symbolic_certificate` | Preserve total positivity/integrality, coprime square ideals, genus-theory class-group elimination, negative Pell condition, and one-versus-two unit classes. |
| `wl544` | `c2_global_descent.py`, `stages["wl544"]` | `coordinate_forms`, `explicit_system`, `trivial_unit_branch`, `symbolic_certificate` | Preserve `N,F,H`, `H^2-ell*F^2=4*N^2`, `Z`, `W`, positivity, all four reconstructions, and the exact trivial-unit quartic. |
| `wl545` | `c2_global_descent.py`, `stages["wl545"]` | `q_valuation_dichotomy`, `descent_variable_parity`, `residue_certificate` | Preserve excluded valuations `1,2`, both mod-8 branches, the `G` unit precision, and `v_2(N)=2`. |
| `wl546` | `c2_global_descent.py`, `stages["wl546"]` | `Gaussian_descent`, `double_descent_system`, `primitive_conditions`, `symbolic_certificate` | Preserve coprime Gaussian factors, `ell=a_0^2+b_0^2`, both `B_pi/R_pi` orientations, `x^2+y^2=D`, coupled real/Gaussian equations, and primitive parity. |
| `wl547` | `c2_global_descent.py`, `stages["wl547"]` | `Gaussian_norm`, `finite_support`, `squareclass_equation`, `symbolic_certificate` | Preserve `delta=(P+iR)/(1+i)`, `Norm(delta)=W^2`, `P+R`, support `p|ell-1` with `(2/p)=1`, the root condition, and the finite `eta*d*gamma^2` statement. |
| `wl548` | `c2_global_descent.py`, `stages["wl548"]` | `valuation_certificate`, `refined_support` | Preserve exact dyadic values `0` and `4`, the `P,R` congruences, post-division parity, and removal of `1+i`. |
| `wl549` | `c2_global_descent.py`, `stages["wl549"]` | `identities_at_a_root`, `classification` | Preserve the nonzero root, `1-t`, `t+4`, the `p=7 mod 8` one-root rule, the `p=1 mod 8` zero-or-two rule, and refined support. |
| `wl550` | `c2_global_descent.py`, `stages["wl550"]` | `certificate` | Preserve the quadratic-etale/Hilbert-90 witnesses `z=1+h` and `z=i`, both orientation targets, and the `A=+/-t/2` root lift. |
| `wl551` | `c2_global_descent.py`, `stages["wl551"]` | `norm_certificate` | Preserve norm-square parity, split conjugate pairing, inert-prime treatment, rational squarefree `r`, and the remaining unit classes. |
| `wl552` | `c2_global_descent.py`, `stages["wl552"]` | `parity_certificate` | Preserve both mod-8 parity derivations, the `gamma` factorization in the `ell=1 mod 8` branch, forced `eta=i`, and both normalized coordinate equations. |

### Slice 2: wl553-wl562

| WL | Canonical destination | Semantic allowlist | Required obligation and parity witness |
| --- | --- | --- | --- |
| `wl553` | `c2_character_system.py`, `stages["wl553"]` | `positivity_certificate` | Preserve `H=(ell-1)*E+ell*F`, both cone signs, exact uniform witnesses `(5,-8)` and `(1,2^k)`, and the statement that positivity alone is exhausted. |
| `wl554` | `c2_character_system.py`, `stages["wl554"]` | `gcd_certificate` | Preserve even odd valuations of Gaussian-square coordinates and the canonical identity `r=sqf_odd(gcd(E,F))=sqf_odd(gcd(ell-1,R))`. |
| `wl555` | `c2_character_system.py`, `stages["wl555"]` | `standard_equation` | Preserve `E,F,Z`, `delta=i*conjugate(Z)`, `Z=r*(a+i*b)^2`, the two coordinate equations, the uniform cone, and canonical `r`. |
| `wl556` | `c2_character_system.py`, `stages["wl556"]` | `orientation_certificate` | Preserve `B_pi` even, `R_pi` odd, the `ell=5 mod 8` `R_pi` selection, the `ell=1 mod 8` `B_pi` selection, and `v_2(B_pi)>=3`. |
| `wl557` | `c2_character_system.py`, `stages["wl557"]` | `valuation_certificate` | Preserve the `R_pi` no-new-condition branch and the exact `c,k` cases, minimum-three condition, and match `v_2(B_pi)=2+v_2(mu*nu)`. |
| `wl558` | `c2_character_system.py`, `stages["wl558"]` | `character_certificate` | Preserve inert automaticity, split `Legendre(F/r,p)=1`, `Q/D` boundary cases, and the exact `p=13,t=10,f(t)=6` nontrivial example. |
| `wl559` | `c2_character_system.py`, `stages["wl559"]` | `leading_character_certificate` | Preserve normalization by `d=min(e,k)`, inert automaticity, split master component, and all `e<k`, `k<e`, `e=k` formulas. |
| `wl560` | `c2_character_system.py`, `stages["wl560"]` | `normalized_character_certificate` | Preserve `epsilon=d mod 2`, `r_p=r/p^epsilon`, normalized equation, all valuation-order formulas, and complete odd-place classification. |
| `wl561` | `c2_character_system.py`, `stages["wl561"]` | `matrix_certificate` | Preserve split rows, all odd columns, `epsilon_q`, `A_pq`, row equation, reciprocity product, split-split cancellation, and the no-contradiction boundary. |
| `wl562` | `c2_character_system.py`, `stages["wl562"]` | `witness_certificate` | Preserve the exact `p=13`, `t=0`/`t=10` values, row bits `0/1`, same `d=0,epsilon=0` stratum, and `B/R` witnesses `(0,1),(1,2),(1,1),(1,4)`. |

### Slice 3: wl563-wl568

| WL | Canonical destination | Semantic allowlist | Required obligation and parity witness |
| --- | --- | --- | --- |
| `wl563` | `c2_allocation.py`, `stages["wl563"]` | `factorization_certificate` | Preserve product equation, `2*(ell-1)/r=kappa*h^2`, coprime complementary split, scale equation, real coordinate, and cone. |
| `wl564` | `c2_allocation.py`, `stages["wl564"]` | `allocation_certificate` | Preserve all `r mod 8` allocations, `kappa` even criterion, and the fact that only odd allocation remains. |
| `wl565` | `c2_allocation.py`, `stages["wl565"]` | `allocation_certificate` | Preserve normalized `U_q`, both side character rules, unique inert assignment, and unresolved split-prime side choice. |
| `wl566` | `c2_allocation.py`, `stages["wl566"]` | `quartic_certificate` | Preserve the quartic sign, alpha-side and beta-side formulas, different/equal predicted-sign cases, and unresolved coupled allocation. |
| `wl567` | `c2_allocation.py`, `stages["wl567"]` | `affine_system_certificate` | Preserve `x_q`, fixed factors, `A_qt`, `Delta_q`, right-hand side, exact affine row, and inconsistent/unique/affine-space outcomes. |
| `wl568` | `c2_allocation.py`, `stages["wl568"]` | `redundancy_certificate`, `next_exact_lemma`, `symbolic_certificate` | Preserve exact scale and cone substitutions, automatic actual-factorization rows, the two signed-ratio branches, all four SymPy identities, and the selected-orientation norm-square missing lemma. |

## Stage Allowlist Contract

The implementation must define an explicit `C2_ALLOWLISTS` map for exactly
the 27 labels. Each entry is the union of the following common keys and its
row-specific sections; no wildcard or prefix matching is allowed.

```text
status
work_log
object_layer
input_checkpoint
proof_status
complete_selmer_upper_bound_proved
rank_zero_claimed
sha2_trivial_claimed
advance_to_m3
stop_after_current_task
```

The row-specific top-level additions are:

```text
wl542: denominator_support, local_converse
wl543: descent, unit_squareclass_split, symbolic_certificate,
       rational_wl535_point_produced_here
wl544: coordinate_forms, explicit_system, trivial_unit_branch, symbolic_certificate,
       rational_wl535_point_produced_here
wl545: q_valuation_dichotomy, descent_variable_parity, residue_certificate,
       rational_wl535_point_produced_here
wl546: Gaussian_descent, double_descent_system, primitive_conditions, symbolic_certificate,
       rational_wl535_point_produced_here
wl547: Gaussian_norm, finite_support, squareclass_equation, symbolic_certificate,
       rational_wl535_point_produced_here
wl548: valuation_certificate, refined_support, rational_wl535_point_produced_here
wl549: identities_at_a_root, classification, rational_wl535_point_produced_here
wl550: certificate, global_integer_candidate_produced_here,
       rational_wl535_point_produced_here
wl551: norm_certificate, rational_wl535_point_produced_here
wl552: parity_certificate, rational_wl535_point_produced_here
wl553: positivity_certificate, full_coordinate_solution_produced_here,
       rational_wl535_point_produced_here
wl554: gcd_certificate, rational_wl535_point_produced_here
wl555: standard_equation, rational_wl535_point_produced_here
wl556: orientation_certificate, rational_wl535_point_produced_here
wl557: valuation_certificate, rational_wl535_point_produced_here
wl558: character_certificate, rational_wl535_point_produced_here
wl559: leading_character_certificate, rational_wl535_point_produced_here
wl560: normalized_character_certificate, rational_wl535_point_produced_here
wl561: matrix_certificate, theorem_level_selmer_matrix_claimed,
       rational_wl535_point_produced_here
wl562: witness_certificate, rational_wl535_point_produced_here
wl563: factorization_certificate, rational_wl535_point_produced_here
wl564: allocation_certificate, rational_wl535_point_produced_here
wl565: allocation_certificate, rational_wl535_point_produced_here
wl566: quartic_certificate, rational_wl535_point_produced_here
wl567: affine_system_certificate, theorem_level_selmer_matrix_claimed,
       rational_wl535_point_produced_here
wl568: redundancy_certificate, next_exact_lemma, symbolic_certificate,
       rational_wl535_point_produced_here
```

The exact `proof_status` allowlist is also stage-specific. The common keys
`uniform_full_wl535_obstruction_proved_here` and `advance_to_m3` are present
in every stage. The additional keys are:

```text
wl542: global_denominator_is_odd_and_coprime_to_ell_here,
       every_denominator_prime_splits_completely_here,
       D_mod_ell_is_nonzero_square_here,
       allowed_denominator_places_add_no_G_local_obstruction_here,
       rational_wl535_point_produced_here
wl543: real_quadratic_alpha_is_totally_positive_integral_here,
       principal_ideal_of_alpha_is_square_ideal_here,
       ordinary_class_group_2_torsion_eliminated_by_genus_theory_here,
       alpha_reduced_to_unit_times_element_square_here,
       remaining_totally_positive_unit_squareclasses_at_most_two
wl544: abstract_unit_square_descent_expanded_here,
       at_most_two_explicit_integer_quartic_branches_here,
       Gaussian_G_and_positivity_pulled_back_exactly_here,
       forward_and_converse_reconstruction_proved_here
wl545: trivial_unit_2_adic_q_valuation_classified_here,
       ell_eq_5_mod_8_forces_u_v_odd_here,
       ell_eq_1_mod_8_forces_even_halves_opposite_parity_here,
       G_condition_adds_no_2_adic_obstruction_here
wl546: primitive_Gaussian_factors_proved_coprime_here,
       Gaussian_square_reduced_to_two_orientations_here,
       real_and_Gaussian_descents_coupled_here,
       Gaussian_square_equation_eliminated_exactly_here
wl547: G_square_rewritten_as_Gaussian_norm_square_here,
       common_odd_prime_support_bounded_by_ell_minus_1_here,
       common_odd_primes_require_Legendre_2_eq_1_here,
       G_square_reduced_to_finite_S_squareclasses_here,
       theorem_level_Selmer_object_claimed_here
wl548: dyadic_delta_valuation_computed_exactly_here,
       one_plus_i_squareclass_eliminated_here,
       finite_support_reduced_to_odd_primes_here
wl549: root_square_condition_classified_here,
       source_square_residues_automatic_at_square_root_here,
       p_eq_7_mod_8_root_test_exhausted_here,
       odd_Gaussian_class_equations_solved_here
wl550: both_wl546_orientations_locally_compatible_here,
       quadratic_etale_hilbert_90_witness_given_here,
       same_prime_orientation_route_exhausted_here,
       global_odd_class_equation_solved_here
wl551: global_norm_square_parity_used_here,
       split_Gaussian_primes_paired_here,
       squarefree_factor_reduced_to_rational_integer_here,
       global_rational_class_equations_solved_here
wl552: dyadic_parity_applied_to_global_class_equation_here,
       Gaussian_unit_class_forced_to_i_here,
       two_unit_classes_reduced_to_one_here,
       remaining_eta_i_coordinate_system_solved_here
wl553: positivity_transferred_to_class_coordinates_here,
       rational_squareclass_cancels_from_sign_here,
       positivity_alone_exhausted_on_both_mod8_branches_here,
       simultaneous_orientation_class_cone_system_solved_here
wl554: odd_coordinate_gcd_parity_of_Gaussian_square_proved_here,
       rational_class_made_candidate_canonical_here,
       independent_r_divisor_choice_eliminated_here,
       canonical_class_equation_solved_here
wl555: standard_norm_element_identified_here,
       Gaussian_unit_removed_uniformly_here,
       branch_dependent_cone_signs_unified_here,
       standard_orientation_square_system_solved_here
wl556: wl546_orientations_coupled_to_dyadic_branches_here,
       one_complete_orientation_eliminated_per_branch_here,
       ell_eq_5_mod_8_R_orientation_selected_here,
       ell_eq_1_mod_8_B_orientation_selected_here,
       surviving_orientation_systems_solved_here
wl557: surviving_orientations_stratified_2_adically_here,
       real_and_Gaussian_descent_valuations_coupled_here,
       ell_eq_5_mod_8_standalone_dyadic_route_exhausted_here,
       ell_eq_1_mod_8_mixed_valuation_cases_eliminated_here,
       surviving_valuation_strata_solved_here
wl558: global_class_equation_applied_at_odd_unit_places_here,
       split_prime_character_condition_proved_here,
       inert_prime_unit_condition_exhausted_here,
       distinct_place_r_coupling_produced_here,
       global_character_system_solved_here
wl559: positive_even_common_valuation_normalized_here,
       split_prime_leading_character_classified_here,
       inert_even_common_valuation_exhausted_here,
       all_odd_places_not_in_r_classified_here,
       global_character_system_solved_here
wl560: odd_common_leading_character_supplied_here,
       all_valuation_parities_unified_here,
       every_odd_ell_minus_one_place_fully_classified_here,
       assembled_global_character_system_solved_here
wl561: split_prime_characters_assembled_as_F2_system_here,
       reciprocity_product_over_odd_common_split_primes_proved_here,
       split_split_pairwise_characters_cancelled_here,
       reciprocity_matrix_uniform_contradiction_proved_here
wl562: opposite_leading_bits_with_same_local_stratum_proved_here,
       both_Gaussian_orientations_locally_compatible_here,
       local_orientation_determinacy_refuted_here,
       global_integer_compatibility_resolved_here
wl563: global_product_coordinate_used_here,
       coprime_squareclass_split_proved_here,
       Gaussian_square_coordinates_reduced_to_fourth_powers_here,
       orientation_product_scale_coupled_here,
       complementary_divisor_split_systems_solved_here
wl564: dyadic_factor_in_complementary_split_allocated_here,
       canonical_r_mod8_coupled_to_global_split_here,
       binary_choice_at_2_removed_when_present_here,
       odd_complementary_divisor_allocation_solved_here
wl565: real_coordinate_leading_unit_defined_here,
       inert_odd_kappa_factors_assigned_here,
       split_odd_kappa_square_unit_test_proved_here,
       split_prime_binary_allocations_solved_here
wl566: quartic_sign_for_split_factor_defined_here,
       alpha_side_quartic_character_proved_here,
       beta_side_quartic_character_proved_here,
       quartic_character_strictly_refines_split_allocation_here,
       coupled_split_allocation_system_solved_here
wl567: quartic_allocation_linearized_over_F2_here,
       affine_row_formula_proved_here,
       exponential_case_split_removed_here,
       affine_system_coupled_to_integer_equations_here
wl568: scale_is_exact_product_coordinate_rewrite_here,
       cone_is_exact_original_positivity_rewrite_here,
       affine_rows_automatic_for_actual_factorization_here,
       allocation_route_independent_obstruction_refuted_here,
       selected_orientation_norm_intersection_solved_here
```

The old payload's remaining top-level flags are parity targets, not inputs to
the kernels. Their values must remain exactly as audited: all Selmer/rank/Sha
flags false, `stop_after_current_task` true, and the stage-specific
unsolved/route-exhaustion flags false or true exactly where shown above.

## Exact Legacy Result Map

This map belongs in the parity test module only. It is explicit by label and
path; it must not use `glob`, `rglob`, filename prefix matching, or directory
scanning.

```python
LEGACY_RESULTS = {
    "wl542": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl542_m2_pure_v_ell_denominator_splitting_support.json",
    "wl543": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent.json",
    "wl544": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent.json",
    "wl545": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy.json",
    "wl546": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent.json",
    "wl547": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent.json",
    "wl548": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination.json",
    "wl549": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification.json",
    "wl550": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility.json",
    "wl551": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing.json",
    "wl552": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination.json",
    "wl553": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone.json",
    "wl554": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd.json",
    "wl555": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation.json",
    "wl556": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation.json",
    "wl557": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata.json",
    "wl558": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character.json",
    "wl559": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character.json",
    "wl560": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character.json",
    "wl561": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product.json",
    "wl562": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation.json",
    "wl563": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split.json",
    "wl564": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split.json",
    "wl565": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character.json",
    "wl566": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation.json",
    "wl567": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation.json",
    "wl568": ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy.json",
}
```

The parity test must assert that the map keys are exactly
`wl542` through `wl568`, that every mapped path is a regular file, and that
the map excludes all unowned result names. At audit time the explicit map has
seven present files (`wl542-wl547`, `wl568`) and 20 absent files
(`wl548-wl567`). The implementation task may materialize those legacy
payloads through the old scripts as a one-time test fixture step, but the
canonical runtime must never read them and the current audit does not create
or modify them.

## Runtime Dependency Rules

The following rules are hard gates for each slice:

1. `c2_global_descent.py` may consume only the canonical C1 `wl541` stage and
   standard-library/SymPy arithmetic. It must not import the legacy `wl541`
   builder, any `audit_closure_...wl542+` module, or any result path.
2. `c2_character_system.py` may consume only the canonical `wl552` output
   from `c2_global_descent.py`. It must not import `wl569+`, the consolidated
   `wl530-wl585` checkpoint, B0/B1, A0/A1/A2, or ignored results.
3. `c2_allocation.py` may consume only the canonical `wl562` output from
   `c2_character_system.py`. It must not reopen local tables, import C3, or
   call any legacy predecessor.
4. `c2_pure_v_ell.py` may call the public C1 `build_c1()` API once and the
   three canonical slice APIs once. It must not use `importlib` fallback
   imports, `glob`, `Path.rglob`, `results/`, or the consolidated oracle.
5. A `ready` value may be emitted as derived execution status but may never be
   accepted as mathematical proof. Predecessor checks must inspect exact
   worklog labels, required proof flags, and false no-claim fields.
6. No slice may add a new prime, representative, local table, parameter
   family, quotient, rank computation, Selmer object, or theorem claim.

The old result map and old builders are test-only parity sources. They are not
part of the import graph or the public runtime API.

## One Shared Strict CLI

The only new subprocess entrypoint is:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m \
  scripts.theory.aa_bb.c2_pure_v_ell \
  --out /tmp/c2.json --strict
```

The output shape follows C1:

```text
{"schema_version": 1, "stages": {"wl542": ..., ..., "wl568": ...}}
```

The CLI prints `stage_count=27` and one aggregate `status=ok|issues` line.
`--strict` exits nonzero if any stage is not `ok`, any required stage is
missing, any stage label is wrong, or a protected no-claim invariant fails.
The CLI does not load legacy result files and does not run a subprocess per
stage. The four new test files use in-process builders; only
`test_c2_cli.py` invokes this command once.

## Bounded Implementation Slices

### Slice 1: wl542-wl552

Implement `c2_global_descent.py` and its focused test. Start from the
canonical C1 `wl541` projection and build the denominator support, real
quadratic descent, explicit unit branches, trivial-unit 2-adic split,
Gaussian orientations, finite Gaussian support, dyadic `1+i` elimination,
root-square classification, Hilbert-90 compatibility, norm pairing, and
forced `eta=i` stages.

The focused checks must cover:

- the `wl542` principal-unit factorizations and denominator support;
- `wl543-wl544` total positivity, ideal-square, genus-theory, conic,
  homogenized `G`, and all converse reconstruction formulas;
- the `wl545` valuation exclusions and both mod-8 branches;
- the `wl546` norm identity and exactly two orientations;
- `wl547-wl549` support identities, exact dyadic valuations, and root tests;
- `wl550` finite-field orientation coverage and Hilbert-90 witness branches;
- `wl551-wl552` conjugate-prime pairing and both parity normalizations;
- old/new semantic parity against the explicit `wl542-wl552` result map,
  predecessor fail-closed behavior, and all no-claim flags.

No character or allocation module is added in this slice. No consumer is
switched and no old file is removed.

### Slice 2: wl553-wl562

Implement `c2_character_system.py` against the canonical `wl552` output.
Preserve the exact positivity identity and cone witnesses, the canonical
squareclass, the unit-free standard element, dyadic orientation selection and
valuation strata, all split/inert/valuation-order character formulas, the
reciprocity matrix, and the `p=13` local witnesses.

The focused checks must cover:

- symbolic positivity and coordinate substitutions plus both uniform cone
  witness families;
- even odd-valuations in a Gaussian square and the exact `r` gcd formula;
- `Z=r*(a+i*b)^2`, `a*b>0`, and the uniform cone;
- parity selection of `R_pi` versus `B_pi`, including the exact `c,k`
  valuation cases;
- inert automaticity, split master components, `e<k`, `k<e`, and `e=k`;
- exact `F_2` row construction and reciprocity cancellation;
- the four `p=13` orientation witnesses with opposite leading bits;
- old/new semantic parity against the explicit `wl553-wl562` result map and
  all no-claim flags.

This slice must not import or reconstruct the allocation system. The
`wl562` result remains a local-determinacy counterexample, not a rational
candidate or a global obstruction.

### Slice 3: wl563-wl568

Implement `c2_allocation.py` against the canonical `wl562` output. Preserve
the complementary squarefree split, exact dyadic allocation, inert and split
odd allocation rules, quartic signs, the affine `F_2` system, and the exact
redundancy proof in `wl568`.

The focused checks must cover:

- coprime squarefree splitting and coordinate/cone substitutions;
- all `r mod 8` and `kappa` parity allocation cases;
- the `q|alpha` and `q|beta` character rules for inert and split primes;
- quartic-sign formulas with both equal and different predicted signs;
- affine-row equivalence by exhaustive small assignments;
- the scale identity, cone identity, and two signed-ratio branches;
- the exact `wl568` final missing lemma and its false solved flag;
- old/new semantic parity against the explicit `wl563-wl568` result map and
  all no-claim flags.

After the three slice tests pass independently, add only the one shared C2
CLI smoke and the full 27-stage parity test. Keep the legacy result map and
the `wl530-wl585` consolidated checkpoint as read-only oracles. Do not enter
`wl569`, M3, deletion, or consumer cutover.

## Focused Validation

Per slice, the allowed validation is:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c2_global_descent.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c2_character_system.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c2_allocation.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c2_cli.py
```

The implementation slice may additionally run targeted Ruff, formatter,
`py_compile`, explicit reference scans for `results`, `glob`, `wl569+`, and
`C3`, deterministic CLI materialization into a temporary directory, and
`git diff --check`. It must not run the full suite.

Parity acceptance requires:

- exactly 27 canonical stages and exactly 27 explicit legacy paths;
- every allowlisted semantic field equal after projection;
- every exact witness and finite table recomputed, not copied as a cached
  boolean;
- fail-closed predecessor, malformed-stage, unknown-field, and no-claim tests;
- no canonical runtime import or filesystem access to legacy results;
- one new strict CLI subprocess, not 27;
- no change to any old file, result, worklog, plan, active-task, C1, or
  consumer during these slices.

The full-suite and final runtime comparison belong to the later C4 gate in the
plan, not to this design audit.

## Risks And Gates

| Risk | Required response |
| --- | --- |
| 20 expected result files are absent now. | Keep the exact map; materialize or otherwise provide the explicit legacy parity sources before implementation acceptance. Never silently skip missing paths or fall back to a glob. |
| A direct rewrite accidentally closes the nontrivial real-unit branch. | Keep `wl543-wl544` as the at-most-two-class union and label `wl545+` as the trivial-unit branch only. Add a parity assertion for this boundary. |
| The `wl547` support is mistaken for a Selmer object. | Preserve `theorem_level_Selmer_object_claimed_here = false` and test it explicitly. |
| The `wl561` and `wl567` matrices are treated as contradictions merely because they are linear. | Preserve their unsolved flags and exact `wl562`/`wl568` failure witnesses. |
| The `wl568` factorization is treated as a converse without ordering. | Retain both signed-ratio factors and require the selected orientation branch before any future reconstruction. |
| Recursive predecessor checks are copied into C2. | Canonical slices accept only canonical predecessor projections and run each kernel once. |
| Cached `ready=True` or a result payload becomes proof. | Derive readiness from exact formulas/proof flags and make runtime result-free. |
| A broad implementation crosses the bounded slice boundary. | Require separate review and focused parity for each of the three slices before composing `build_c2()`. |

## Acceptance

`design_ready` is justified. The exact mathematical obligations, semantic
destinations, stage allowlists, runtime boundaries, result paths, three
bounded slices, and focused validation are all specified. The known missing
ignored result artifacts and the unresolved `wl568` orientation/norm lemma
are explicit implementation gates, not hidden assumptions. No implementation,
cutover, deletion, new mathematics, or theorem-strength change is authorized
by this design.
