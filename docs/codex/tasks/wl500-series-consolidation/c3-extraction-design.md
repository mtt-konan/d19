# C3 Extraction Design: wl569-wl585

## Verdict

```text
worker_outcome = c3_design_ready
design_ready = true
implementation_status = not_started
scope = wl569-wl585 only
claim_boundary = M2 remains open; M3 remains closed
```

This is a read-only extraction design. The audit covers the 17 worklogs, 17
legacy audit scripts, 17 ignored result payloads, and 17 legacy test files for
`wl569` through `wl585`. It proposes a canonical C3 evidence graph and parity
plan without changing a formula, adding mathematics, implementing code, or
materializing a result.

The C3 input is the accepted canonical C2 projection at `wl568`. C3 does not
reopen `wl542`-`wl567`, import a legacy predecessor, read a result file at
runtime, enter `wl586+`, or advance to M3.

## Audit Findings

The inspected legacy scripts have one strict recursive predecessor chain:
`wl569` imports and rebuilds legacy `wl568`, and each later script imports and
rebuilds its immediate predecessor. Each script also writes its own fixed
result path and accepts `--strict`. The inspected tests repeat the same
structure: exact symbolic or arithmetic checks, claim-boundary assertions,
fail-closed predecessor checks, and one strict CLI subprocess per worklog.

The 17 result payloads are present at their exact fixed paths in the current
worktree. They remain ignored, test-only parity oracles. Their `ready` and
`violations` fields are execution metadata and must not become trusted proof
inputs. The canonical runtime must recompute every symbolic identity, finite
witness, converse, branch condition, genus calculation, and route boundary.

The range contains three different kinds of evidence that must not be
collapsed:

- `wl569`-`wl570` select and parameterize one exact positive real branch, but
  do not solve the resulting system.
- `wl571`-`wl580` classify and exhaust several descent, allocation, and
  magnitude rewrites, while leaving the generic arithmetic intersection open.
- `wl581`-`wl585` construct lower-genus quotients and torsors, then explicitly
  show why unrestricted points, ranks, or automatic quadratic lifts do not
  solve the restricted candidate image.

The trivial real-unit branch selected in `wl545`-`wl568` remains a branch
selection. The at-most-two totally positive unit classes from `wl543`-`wl544`
are not merged by C3, and no C3 stage claims that the nontrivial unit class is
empty.

## Protected Boundaries

The following statements are protected semantic boundaries, not implementation
conveniences:

- `wl569` proves `F<0`, chooses the unique positive ordered ratio
  `tau=(C+F)/E` in `(rho_ell,1)`, and leaves the selected orientation/norm
  intersection unsolved. It does not close the reciprocal branch by a new
  global theorem, solve the nontrivial unit branch, or prove `wl535`.
- `wl570` is an exact forward and converse reduction to the two-variable
  factored square system. It is not a solution of that system and does not
  add a second independent parameter or a new square root.
- `wl571` proves the product quartic is genus one, the generic full cover is
  genus five, and `tau=1/2` is the unique genus-one drop. At this stage the
  exceptional branch is still live.
- `wl572` closes only `tau=1/2`: integrality and positivity force `X=4` and
  `ell=8`, so the odd-prime parameter condition fails. The generic
  `tau!=1/2` genus-five cover remains open.
- `wl573`-`wl578` are exact denominator, squareclass, rotation, valuation, and
  allocation-transport identities. They do not prove the generic cover has
  no rational point and do not create a theorem-level Selmer object.
- `wl579` proves a genus-one magnitude curve and a projective Mobius
  reconstruction. It does not prove primitive linear-form reconstruction.
- `wl580` proves unique `tau` reconstruction and the canonical squareclass
  self-consistency relation. Its exact missing lemma, no positive rational
  point on the self-consistent genus-one magnitude torsor in the `wl570`
  interval, remains false as a solved flag.
- `wl581`-`wl582` prove a genus-two character quotient and an elliptic quotient
  over `Q(i)`, then prove that the rational-locus lift reconstructs the
  genus-two point. The automatic `S^2+16` square and unrestricted elliptic
  points, ranks, and torsion are not obstructions.
- `wl583` retains both individual source-square lifts on a genus-one torsor
  and proves that adjoining `q^2=X` is an independent connected lift. It does
  not classify square-`X` torsor points.
- `wl584` is pointwise on the incidence condition `ell=L(X,tau)`. It reduces
  the source equations to a fixed-`ell` genus-one curve and leaves the final
  norm-discriminant intersection unsolved.
- `wl585` proves the fixed-`ell` four-squareclass cover has genus seventeen,
  and the combined source/norm quotient has genus three with an elliptic
  quotient. Its restricted elliptic image is unsolved; unrestricted quotient
  data is not a closure result.

At every stage, C3 preserves the following top-level values:

```text
complete_selmer_upper_bound_proved = false
rank_zero_claimed = false
sha2_trivial_claimed = false
rational_wl535_point_produced_here = false
advance_to_m3 = false
stop_after_current_task = true
```

Every stage also preserves
`proof_status.uniform_full_wl535_obstruction_proved_here = false` and
`proof_status.advance_to_m3 = false`. A derived `ready=true` means only that
the canonical certificates and predecessor checks passed.

## Exact Legacy Assets

The parity test must use an explicit dictionary of the following fixed paths.
It must not use `glob`, `rglob`, filename-prefix matching, directory scans, or
an inferred predecessor path. The worklog, script, test, and result entries
below are the complete owned set.

| WL | Worklog | Legacy script | Legacy test | Legacy result |
| --- | --- | --- | --- | --- |
| `wl569` | `docs/work-logs/569-m2-pure-v-ell-archimedean-selection-of-norm-ratio-branch.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch.py` | `results/closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch.json` |
| `wl570` | `docs/work-logs/570-m2-pure-v-ell-two-variable-norm-ratio-square-system.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system.py` | `results/closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system.json` |
| `wl571` | `docs/work-logs/571-m2-pure-v-ell-source-square-multiquadratic-cover-genus.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus.py` | `results/closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus.json` |
| `wl572` | `docs/work-logs/572-m2-pure-v-ell-exclude-tau-half-by-integrality.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality.py` | `results/closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality.json` |
| `wl573` | `docs/work-logs/573-m2-pure-v-ell-generic-cover-integral-denominator-coupling.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling.py` | `results/closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling.json` |
| `wl574` | `docs/work-logs/574-m2-pure-v-ell-common-delta-squareclass-double-split.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split.py` | `results/closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split.json` |
| `wl575` | `docs/work-logs/575-m2-pure-v-ell-scaled-gaussian-rotation-between-source-pairs.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs.py` | `results/closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs.json` |
| `wl576` | `docs/work-logs/576-m2-pure-v-ell-odd-prime-side-transport-under-rotation.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation.py` | `results/closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation.json` |
| `wl577` | `docs/work-logs/577-m2-pure-v-ell-all-odd-k-primes-transport-same-side.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side.py` | `results/closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side.json` |
| `wl578` | `docs/work-logs/578-m2-pure-v-ell-dyadic-same-side-and-identical-k-allocation.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation.py` | `results/closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation.json` |
| `wl579` | `docs/work-logs/579-m2-pure-v-ell-common-allocation-mobius-magnitude-curve.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve.py` | `results/closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve.json` |
| `wl580` | `docs/work-logs/580-m2-pure-v-ell-primitive-reconstruction-and-descent-exhaustion.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion.py` | `results/closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion.json` |
| `wl581` | `docs/work-logs/581-m2-pure-v-ell-genus-two-character-and-quadratic-elliptic-quotient.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient.py` | `results/closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient.json` |
| `wl582` | `docs/work-logs/582-m2-pure-v-ell-q-i-elliptic-rational-locus-descent-equivalence.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence.py` | `results/closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence.json` |
| `wl583` | `docs/work-logs/583-m2-pure-v-ell-source-square-genus-one-torsor-and-square-x-fiber-product.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product.py` | `results/closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product.json` |
| `wl584` | `docs/work-logs/584-m2-pure-v-ell-prime-coupled-source-elliptic-and-final-norm-intersection.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection.py` | `results/closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection.json` |
| `wl585` | `docs/work-logs/585-m2-pure-v-ell-genus-seventeen-cover-and-combined-source-norm-elliptic-quotient.md` | `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient.py` | `tests/test_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient.py` | `results/closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient.json` |

The parity test must assert that the dictionary keys are exactly
`wl569` through `wl585`, all 17 paths are regular files, and no unowned
`wl586+` or consolidated result is included in this C3 map. Missing fixtures
must fail closed rather than skip a stage.

## Canonical Shape And APIs

The proposed implementation has three mathematical kernels and one
composition boundary:

```text
scripts/theory/aa_bb/c3_real_branch.py
scripts/theory/aa_bb/c3_magnitude_descent.py
scripts/theory/aa_bb/c3_quotient_limits.py
scripts/theory/aa_bb/c3_pure_v_ell.py

tests/theory/aa_bb/test_c3_real_branch.py
tests/theory/aa_bb/test_c3_magnitude_descent.py
tests/theory/aa_bb/test_c3_quotient_limits.py
tests/theory/aa_bb/test_c3_cli.py
```

The public slice APIs accept canonical mappings and return all stages in their
bounded range. They do not expose one public replacement function per old
worklog:

```python
build_c3_real_branch(wl568) -> dict[str, dict[str, Any]]       # wl569-wl574
build_c3_magnitude_descent(wl574) -> dict[str, dict[str, Any]] # wl575-wl580
build_c3_quotient_limits(wl580) -> dict[str, dict[str, Any]]   # wl581-wl585

@dataclass(frozen=True)
class C3Evidence:
    stages: dict[str, dict[str, Any]]

def build_c3(c2=None) -> C3Evidence
def project_stage(evidence, work_log) -> dict[str, Any]
def semantic_projection(payload, work_log) -> dict[str, Any]
```

`build_c3()` calls the public C2 `build_c2()` API exactly once when no C2
argument is supplied, verifies `c2.stages["wl568"]` has
`work_log="wl568"`, `status="ok"`,
`proof_status.allocation_route_independent_obstruction_refuted_here=true`,
`proof_status.uniform_full_wl535_obstruction_proved_here=false`, and
`advance_to_m3=false`, then calls
the three C3 slice builders exactly once and in order. The first slice starts
from `c2.stages["wl568"]`; the second consumes only canonical `wl574`; the
third consumes only canonical `wl580`. The final labels are exactly
`C3_STAGES = tuple(f"wl{number}" for number in range(569, 586))`, in numeric
order.

`project_stage()` rejects `wl568`, `wl586`, unknown labels, missing stages, and
mislabeled payloads. `semantic_projection()` has an exact stage allowlist,
rejects unknown or missing semantic fields, removes only `ready` and
`violations`, and recursively compares every remaining value. It does not
normalize formula strings, signs, list order, proof flags, witnesses, branch
text, or genus text.

## Stage Allowlists

Every C3 stage has this exact common top-level set, plus the row-specific
fields below:

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
rational_wl535_point_produced_here
```

The row-specific top-level additions are:

```text
wl569: branch_certificate, next_exact_lemma, symbolic_certificate
wl570: system_certificate, symbolic_certificate
wl571: cover_certificate, symbolic_certificate
wl572: integrality_certificate, symbolic_certificate
wl573: denominator_certificate, symbolic_certificate
wl574: double_split_certificate, symbolic_certificate
wl575: rotation_certificate, symbolic_certificate
wl576: transport_certificate, symbolic_certificate
wl577: same_side_certificate, symbolic_certificate
wl578: dyadic_certificate, remaining_magnitude_system, symbolic_certificate
wl579: magnitude_curve_certificate, symbolic_certificate
wl580: reconstruction_certificate, exact_missing_lemma, symbolic_certificate
wl581: quotient_certificate, symbolic_certificate
wl582: descent_certificate, symbolic_certificate
wl583: fiber_product_certificate, symbolic_certificate
wl584: intersection_certificate, symbolic_certificate
wl585: cover_certificate, symbolic_certificate
```

`ready` and `violations` are deliberately outside the semantic projection.
They may be emitted as derived execution metadata, but a cached `ready=true`
cannot satisfy a predecessor check.

The exact proof-status allowlist is common keys
`uniform_full_wl535_obstruction_proved_here` and `advance_to_m3`, followed by
the stage-specific keys below. Values marked `T` must be true; values marked
`F` must remain false. The two common keys are `F` for every row.

| WL | Required true proof keys | Required false proof keys |
| --- | --- | --- |
| `wl569` | `source_square_and_positivity_force_0_lt_X_lt_ell_here`; `F_strictly_negative_on_candidate_range_here`; `positive_ordered_norm_ratio_branch_unique_here`; `strict_cone_ratio_interval_proved_here` | `selected_orientation_norm_intersection_solved_here` |
| `wl570` | `quartic_square_root_eliminated_by_unique_tau_here`; `parameter_formula_in_X_tau_proved_here`; `both_source_squares_factored_in_X_tau_here`; `forward_and_converse_wl535_reconstruction_proved_here` | `two_variable_square_system_solved_here` |
| `wl571` | `product_quartic_smooth_genus_one_for_all_admissible_tau_here`; `full_source_square_cover_genus_five_for_tau_ne_half_here`; `tau_half_unique_genus_drop_to_one_here`; `product_plus_one_square_converse_proved_here` | `exceptional_tau_half_branch_solved_here` |
| `wl572` | `integral_parameter_forces_q_denominator_one_here`; `integral_parameter_forces_q_numerator_square_divides_four_here`; `positivity_leaves_only_X_four_here`; `tau_half_excluded_for_odd_prime_parameter_here` | `generic_tau_cover_solved_here` |
| `wl573` | `q_numerator_square_supports_on_four_mn_here`; `q_denominator_square_supports_on_mn_here`; `Delta_coprime_to_mn_here`; `Delta_divides_positive_quartic_form_here` | `generic_genus_five_cover_solved_here` |
| `wl574` | `both_source_pairs_share_canonical_Delta_squareclass_here`; `AB_common_gcd_supported_on_R1_here`; `CD_common_gcd_supported_on_R2_here`; `two_complementary_splits_of_same_k_proved_here` | `generic_genus_five_cover_solved_here` |
| `wl575` | `exact_scaled_Gaussian_rotation_proved_here`; `inverse_rotation_and_norm_identity_proved_here`; `PK_primitive_away_from_two_here`; `R1R2_primitive_away_from_two_here`; `two_k_allocations_structurally_coupled_here` | `generic_genus_five_cover_solved_here` |
| `wl576` | `odd_k_primes_force_two_quadratic_residue_here`; `regular_same_side_transport_by_K_here`; `regular_crossed_side_transport_by_P_here`; `R1_singular_pair_vanishes_together_here`; `R2_singular_pair_vanishes_together_here`; `singular_side_requires_higher_valuation_here` | `generic_genus_five_cover_solved_here` |
| `wl577` | `global_Delta_divisibility_forces_all_odd_k_primes_into_K_here`; `odd_singular_determinant_cases_eliminated_here`; `odd_crossed_transport_eliminated_here`; `two_allocations_have_identical_odd_parts_here`; `factor_two_is_only_remaining_transport_here` | `generic_genus_five_cover_solved_here` |
| `wl578` | `normalized_rotation_is_diagonal_odd_offdiagonal_even_here`; `two_adic_valuation_order_preserved_here`; `factor_two_transports_same_side_here`; `two_complementary_k_allocations_identical_here`; `allocation_analysis_exhausted_here` | `generic_genus_five_cover_solved_here` |
| `wl579` | `biquadratic_genus_one_curve_proved_here`; `common_allocation_magnitude_reduced_to_Mobius_map_here`; `projective_magnitude_converse_proved_here`; `strict_normalized_magnitude_ordering_proved_here` | `primitive_linear_form_reconstruction_proved_here`; `generic_genus_five_cover_solved_here` |
| `wl580` | `allocation_descent_exhausted_here`; `canonical_squareclass_self_consistency_stated_here`; `primitive_m_n_has_no_extra_branch_here`; `source_squares_reconstructed_from_self_consistent_torsor_here`; `tau_uniquely_reconstructed_from_X_z_here` | `self_consistent_genus_one_family_solved_here`; `generic_genus_five_cover_solved_here` |
| `wl581` | `genus_two_character_quotient_proved_here`; `quadratic_elliptic_quotient_over_q_i_proved_here`; `restricted_affine_candidate_image_proved_here` | `restricted_elliptic_image_locus_solved_here` |
| `wl582` | `nonbranch_forward_and_inverse_bijection_proved_here`; `q_i_real_coordinate_locus_split_here`; `quadratic_lift_obstruction_shown_automatic_here`; `rational_genus_two_lift_reconstructed_here`; `wl581_unrestricted_elliptic_route_exhausted_here` | none beyond the two common false keys |
| `wl583` | `exceptional_tau_half_preserved_and_not_reopened_here`; `full_cover_fiber_product_equivalence_proved_here`; `individual_source_squares_retained_on_torsor_here`; `source_square_torsor_genus_one_proved_here`; `square_x_pullback_independent_and_connected_here`; `unramified_degree_two_map_to_product_elliptic_proved_here` | `square_x_torsor_points_solved_here` |
| `wl584` | `final_norm_discriminant_equivalence_proved_here`; `fixed_ell_source_curve_genus_one_proved_here`; `prime_coupled_torsor_source_identities_proved_here`; `square_x_source_cover_genus_one_proved_here`; `unrestricted_source_elliptic_route_exhausted_here` | `final_norm_intersection_solved_here` |
| `wl585` | `combined_rational_elliptic_quotient_proved_here`; `combined_source_norm_genus_three_quotient_proved_here`; `fixed_ell_full_cover_genus_seventeen_proved_here`; `norm_bearing_character_quotients_classified_here`; `selected_tau_interval_equivalent_to_positivity_here` | `restricted_combined_elliptic_image_solved_here` |

The false proof keys in the table are semantic no-claim protections, not
known bugs or invitations to fill the gap. In particular, `wl572` must not
turn its exceptional-branch closure into a generic-cover closure, `wl580`
must not turn self-consistency into a solved family, and `wl581`-`wl585` must
not turn quotient geometry into a restricted-image theorem.

## Obligation And Parity Map

The destination below is a canonical stage projection, not a new narrated
worklog. Each row must retain the listed formulas, witnesses, converses,
exceptional branches, and route boundary exactly. Every `symbolic_certificate`
boolean must be recomputed, not copied from a result payload.

### Slice 1: wl569-wl574

| WL | Canonical destination and semantic section | Required obligation, witness, or converse |
| --- | --- | --- |
| `wl569` | `c3_real_branch.py`, `stages["wl569"]`, `branch_certificate`, `next_exact_lemma`, `symbolic_certificate` | Start with `0<X=q^2<ell`. Keep `F=D^4*(X^2+(8-4*ell)*X-4)`, `F' = 2*X+8-4*ell`, `E>0`, `C^2=F^2+E^2`, and the two roots `(F+C)/E` and `(F-C)/E`. Preserve the unique positive ordered ratio `tau=(C+F)/E`, `rho_ell=(sqrt((ell-1)^2+ell^2)-(ell-1))/ell`, and `rho_ell<tau<1`, with the uniform lower bound `sqrt(2)-1<tau`. Preserve the next lemma coupling `tau` to the selected `R_pi`/`B_pi` orientation. The legacy parameter tests use `ell=5,13,17,29,37,101` for endpoint bounds and `ell=5,13,17,29` for negativity; these are validation witnesses, not new claims. |
| `wl570` | `c3_real_branch.py`, `stages["wl570"]`, `system_certificate`, `symbolic_certificate` | Preserve `delta=tau^2+2*tau-1` and the exact identities `ell=(tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)/(2*X*delta)`, `ell-X=-(X*tau+2*X-2)*(2*X*tau-X-2*tau)/(2*X*delta)`, and `ell*X+4=(X+2*tau+4)*(X*tau+4*tau-2)/(2*delta)`. Retain `sigma_ell<X<ell`, `rho_ell<tau<1`, and `X*(2*tau-1)<2*tau`. Preserve the forward map from a `wl535` candidate and the converse choosing `q^2=X`, `p^2=ell-X`, `c^2=ell*X+4`, `C=E*(1+tau^2)/(2*tau)`, including the proof that `C^2=F^2+E^2` and that no `E=0`, `tau=0`, or `delta=0` branch is lost. |
| `wl571` | `c3_real_branch.py`, `stages["wl571"]`, `cover_certificate`, `symbolic_certificate` | Preserve `a=X*(tau+2)-2`, `b=2*tau-X*(2*tau-1)`, `c=X+2*tau+4`, `d=tau*(X+4)-2`, `Y^2=a*b*c*d`, and the exact pairwise resultants `a_b=2*(tau^2+1)`, `a_c=2*(tau^2+4*tau+5)`, `a_d=4*delta`, `b_c=-4*delta`, `b_d=-2*(5*tau^2-4*tau+1)`, `c_d=-2*(tau^2+1)`. Preserve the full rational 2-torsion genus-one product curve, the degree-eight generic square cover with six branch points and `g=5` by Riemann-Hurwitz, and the `tau=1/2` four-branch-point `g=1` drop. Retain the exact exceptional system `ell=X+5-4/X`, `p^2=5-4/X`, `s^2=X*(X+5)`, `X=q^2`, the product-plus-one-square converse, and the false exceptional solved flag. |
| `wl572` | `c3_real_branch.py`, `stages["wl572"]`, `integrality_certificate`, `symbolic_certificate` | Preserve reduced `q=a/b`, `ell=(a^4+5*a^2*b^2-4*b^4)/(a^2*b^2)`, the reductions `a^2|4*b^4` and `b^2|a^4`, coprimality consequences `a^2|4` and `b=1`, and `X>1` forcing `X=4`, hence `ell=8`. Preserve the exact exceptional closure: at `X=4`, `p^2=4` and `s^2=9` are populated but the odd-prime parameter fails. Do not set `generic_tau_cover_solved_here` true. |
| `wl573` | `c3_real_branch.py`, `stages["wl573"]`, `denominator_certificate`, `symbolic_certificate` | Preserve primitive `X=a^2/b^2`, `tau=m/n`, `gcd(a,b)=gcd(m,n)=1`, `0<m<n`, `Delta=m^2+2*m*n-n^2>0`, and the homogenized numerator `H=a^4*m*n+2*a^2*b^2*m^2+8*a^2*b^2*m*n-2*a^2*b^2*n^2-4*b^4*m*n`. Retain `a^2|4*m*n`, `b^2|m*n`, `gcd(Delta,m*n)=1`, `Delta|K` for `K=a^4+4*a^2*b^2-4*b^4>0`, and `v_2(Delta)=0` for opposite parity or `1` for both odd. The exact test grid and dyadic boundary must remain finite certificate evidence, not a contradiction. |
| `wl574` | `c3_real_branch.py`, `stages["wl574"]`, `double_split_certificate`, `symbolic_certificate` | Preserve `A=a^2*m+2*a^2*n-2*b^2*n`, `B=a^2*n+2*b^2*m-2*a^2*m`, `C=a^2*m+4*b^2*m-2*b^2*n`, `D=a^2*n+2*b^2*m+4*b^2*n`, `p^2=A*B/(2*a^2*b^2*Delta)`, and `s^2=C*D/(2*b^4*Delta)`. Preserve `2*Delta=k*h^2` with positive squarefree `k`, `A*B=k*U^2`, `C*D=k*V^2`, and the converse square roots. Preserve `g1|R1` with `R1=5*a^4-8*a^2*b^2+4*b^4`, `g2|R2` with `R2=a^4+8*a^2*b^2+20*b^4`, and both complementary splits `A/g1=alpha*r1^2`, `B/g1=beta*s1^2`, `alpha*beta=k`, `C/g2=gamma*r2^2`, `D/g2=delta0*s2^2`, `gamma*delta0=k`. |

### Slice 2: wl575-wl580

| WL | Canonical destination and semantic section | Required obligation, witness, or converse |
| --- | --- | --- |
| `wl575` | `c3_magnitude_descent.py`, `stages["wl575"]`, `rotation_certificate`, `symbolic_certificate` | Preserve `P=a^4+4*b^4`, `K=a^4+4*a^2*b^2-4*b^4`, the exact forward relations `R1*C=P*A-2*K*B`, `R1*D=2*K*A+P*B`, inverse relations `R2*A=P*C+2*K*D`, `R2*B=-2*K*C+P*D`, and `P^2+4*K^2=R1*R2`. Preserve `R1*(C^2+D^2)=R2*(A^2+B^2)`, `gcd(P,K)=1 or 4`, `gcd(R1,R2)=1 or 4`, and the exact grid identities including resultants `128*y^4` and `18432*y^4`. |
| `wl576` | `c3_magnitude_descent.py`, `stages["wl576"]`, `transport_certificate`, `symbolic_certificate` | Preserve every odd `p|k` condition `(2/p)=1`, the exact cross-resultants `AC=-2*n*K`, `AD=n*P`, `BC=-n*P`, `BD=-2*n*K`, and `disc_m(Delta)=8*n^2`. Preserve regular `K` same-side transport `A->C`, `B->D`, regular `P` crossed transport `A->D`, `B->C`, and both singular cases: `p|R1` makes `A,B` vanish together while exactly one of `C,D` vanishes, and `p|R2` is inverse. Retain the unresolved larger normalized valuation at a singular pair. |
| `wl577` | `c3_magnitude_descent.py`, `stages["wl577"]`, `same_side_certificate`, `symbolic_certificate` | Use `Delta|K` to force every odd `p|k` into `K` and out of `P*R1*R2`; preserve the norm identity that eliminates singular determinant cases and crossed transport. Preserve identical odd allocations `odd(alpha)=odd(gamma)`, `odd(beta)=odd(delta0)`, and the exact boundary that only the factor `2` remains, with `2|k` iff `m,n` have opposite parity. |
| `wl578` | `c3_magnitude_descent.py`, `stages["wl578"]`, `dyadic_certificate`, `remaining_magnitude_system`, `symbolic_certificate` | Preserve normalization `e=1` for `a` odd and `e=4` for `a` even. The normalized rotation matrix has odd diagonal and even off-diagonal entries over `Z_2`, so the larger coordinate valuation is preserved and the factor `2` transports same-side. Preserve `alpha=gamma`, `beta=delta0`, `allocation_analysis_exhausted_here=true`, and the exact remaining equations `R1*g2*alpha*r2^2=P*g1*alpha*r1^2-2*K*g1*beta*s1^2` and `R1*g2*beta*s2^2=2*K*g1*alpha*r1^2+P*g1*beta*s1^2`. |
| `wl579` | `c3_magnitude_descent.py`, `stages["wl579"]`, `magnitude_curve_certificate`, `symbolic_certificate` | Preserve `lambda=beta/alpha`, `z=lambda*u^2=B/A`, `w=lambda*v^2=D/C`, the Mobius map `w=(2*K+P*z)/(P-2*K*z)`, the curve `lambda*v^2*(P-2*K*lambda*u^2)=2*K+P*lambda*u^2`, domain `0<u^2<P/(2*K*lambda)`, and `v>u`. Recompute the biquadratic genus-one certificate, zero/pole noncollision, and projective magnitude converse. Keep `primitive_linear_form_reconstruction_proved_here=false`. |
| `wl580` | `c3_magnitude_descent.py`, `stages["wl580"]`, `reconstruction_certificate`, `exact_missing_lemma`, `symbolic_certificate` | Preserve `tau=[X+2*z*(1-X)]/[X*(z+2)-2]` with positive denominator for `X>1,z>0`, the two product-ratio identities, `Abar*Dbar-Bbar*Cbar=2*(tau^2+1)*(X^2+4*X-4)`, and the equivalence of `z/lambda` and `w/lambda` squares to the two `wl570` source squares. Preserve `[lambda]=[2*(tau^2+2*tau-1)]`, the no-extra-branch primitive `(m,n)` reconstruction, and the exact missing lemma: no positive rational point on the self-consistent genus-one magnitude torsor in the `wl570` interval. |

### Slice 3: wl581-wl585

| WL | Canonical destination and semantic section | Required obligation, witness, or converse |
| --- | --- | --- |
| `wl581` | `c3_quotient_limits.py`, `stages["wl581"]`, `quotient_certificate`, `symbolic_certificate` | Preserve `C_tau: Z^2=X*a*b*c*d`, the six branch points and genus-two character quotient, involution `X->-4/X`, and lift `(X,Z)->(-4/X,8*i*Z/X^3)`. Preserve the exact factor pairing under the involution: `a(-4/X)=-2*c/X`, `b(-4/X)=2*d/X`, `c(-4/X)=2*a/X`, `d(-4/X)=-2*b/X`. Preserve `S=X-4/X`, `Y=Z*(X-2*i)/X^2`, `E_tau: Y^2=-(S-4*i)*L1*L2`, with `L1=(tau+2)*S+2*tau^2+8*tau+6`, `L2=(2*tau^2-tau)*S+6*tau^2-8*tau+2`, and the exact cubic discriminant `256*(tau-i)^2*(tau+i)^2*((1-2*i)*tau+i)^4*(tau+2+i)^4*(tau^2+2*tau-1)^2`. The elliptic quotient is over `Q(i)`; preserve the restricted image requirements `tau` rational in the exact interval, `S` rational, `S^2+16` a nonzero rational square, positive `X` the original square, `Y!=0`, and `ell=L(X,tau)` the original odd prime. |
| `wl582` | `c3_quotient_limits.py`, `stages["wl582"]`, `descent_certificate`, `symbolic_certificate` | Preserve the split equations for `Y=A+i*B`: `A^2-B^2=-S*L`, `A*B=2*L`, and the nonbranch inverse `X=-2*A/B`, `Z=A*X`, `Y=Z*(X-2*i)/X^2`. Preserve `S^2+16=(X+4/X)^2` as automatic, the exact forward/inverse equivalence, branch exclusion, and the remaining independent conditions: positive square `X`, both individual source products, and prime `ell=L(X,tau)`. The unrestricted `Q(i)` elliptic route is explicitly exhausted, not solved by rank data. |
| `wl583` | `c3_quotient_limits.py`, `stages["wl583"]`, `fiber_product_certificate`, `symbolic_certificate` | Preserve `T_tau: U^2=a*b/(2*delta)`, `V^2=c*d/(2*delta)`, maps `U=q*p`, `V=s`, and converse `p=U/q`. Preserve torsor genus one, product map `Y=2*delta*U*V`, unramified connected degree-two map, generic branch supports `{0,infinity}`, `{root(a),root(b)}`, `{root(c),root(d)}`, and genus-five fiber product with `q^2=X`. Preserve that `X` has an odd divisor on the torsor and the square-X pullback is independent and connected. Keep the excluded exceptional branch recorded but not reopened: `U^2=5*X-4`, `V^2=X*(X+5)`. |
| `wl584` | `c3_quotient_limits.py`, `stages["wl584"]`, `intersection_certificate`, `symbolic_certificate` | Preserve the pointwise incidence `ell=L(X,tau)`, the fixed-`ell` source curve `U^2=X*(ell-X)`, `V^2=ell*X+4`, the identity `V^2-U^2=X^2+4`, its genus-one boundary points `(0,0,2)` and `(0,0,-2)`, and the connected genus-one square-X cover. Preserve `F=X^2+(8-4*ell)*X-4`, `E=4*(ell-1)*X`, `G_ell(X)=X^4+(16-8*ell)*X^3+(32*ell^2-96*ell+72)*X^2+(32*ell-64)*X+16`, `E*tau^2-2*F*tau-E=0`, discriminant `4*G_ell(X)`, the two algebraic roots, the live selected root `tau=(F+C)/E`, and the exact intersection of square-X, `G_ell(X)` square, positive interval, and odd prime `ell=1 mod 4`. Preserve the `E=0` boundary exclusion for `ell>=5`, `X>1`. |
| `wl585` | `c3_quotient_limits.py`, `stages["wl585"]`, `cover_certificate`, `symbolic_certificate` | Preserve the four squareclasses `X`, `ell-X`, `ell*X+4`, and `G_ell(X)`, the quartic discriminant `2^26*(ell-2)^2*(ell-1)^4*((ell-1)^2+1)`, and the exact boundary values `G_ell(0)=16`, `G_ell(ell)=(5*ell^2-8*ell+4)^2`, `G_ell(-4/ell)=16*(5*ell^2-8*ell+4)^2/ell^4`. Preserve degree `16`, eight branch points, and genus `17`. Preserve the norm-bearing quotient genus counts `1` genus-one, `6` genus-two, and `1` genus-three, `J_ell: W^2=X*(ell-X)*(ell*X+4)*G_ell(X)`, `W=q*p*c*C`, the reciprocal identities `G_ell(-4/X)=16*G_ell(X)/X^4` and `X*(ell-X)*(ell*X+4)` at `-4/X` equals `16*X*(ell-X)*(ell*X+4)/X^4`, the reciprocal involution `j(X,W)=(-4/X,16*W/X^4)`, `S=X-4/X`, `Z=W/X^2`, and the elliptic equation `Z^2=(ell^2-ell*S-4)*(S^2+(16-8*ell)*S+32*ell^2-96*ell+80)` with exact cubic discriminant `-64*(ell-1)^2*(5*ell^2-8*ell+4)^4`. Preserve the exact equivalence between the selected `tau` interval and original positivity, and leave the restricted combined elliptic image unsolved. |

## Runtime Dependency Rules

These are hard implementation gates:

1. `c3_real_branch.py` receives only the canonical `wl568` mapping supplied by
   the C3 orchestrator. It may use standard-library and SymPy arithmetic, but
   it may not import any `audit_closure_...wl569+` module, `c2_*` internals,
   C1 modules, a result path, or the `wl530-wl585` consolidated checkpoint.
2. `c3_magnitude_descent.py` receives only the canonical `wl574` stage from
   the first C3 slice. It may not rebuild `wl569`-`wl574`, reopen an old
   allocation script, or read a result payload.
3. `c3_quotient_limits.py` receives only the canonical `wl580` stage from the
   second C3 slice. It may not import `wl581+` legacy builders, call C1/C2
   kernels directly, or use unrestricted elliptic/rank tooling.
4. `c3_pure_v_ell.py` may import the public C2 `build_c2()` once and the three
   public C3 slice builders once. It must not use `importlib` fallback imports,
   `glob`, `Path.rglob`, `results/`, directory enumeration, subprocesses, or
   the consolidated oracle.
5. A predecessor check must inspect exact `work_log`, `status`, required true
   proof keys, common false no-claim fields, and `advance_to_m3`; it must not
   accept `ready=True` alone. A failed predecessor returns an `issues` payload
   with an empty `proof_status`, as in C1/C2.
6. No C3 slice may add a prime, representative, local table, parameter family,
   rank computation, Selmer object, quotient claim beyond the audited
   formulas, or theorem-strength change. `M3` stays closed.

The explicit result map and the legacy builders are test-only parity sources.
They are not part of the canonical import graph or public runtime API.

## One Shared Strict CLI

After the three slice tests pass independently, add only the shared CLI in
`scripts/theory/aa_bb/c3_pure_v_ell.py`:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m \
  scripts.theory.aa_bb.c3_pure_v_ell \
  --out /tmp/c3.json --strict
```

The output contract is exactly:

```text
schema_version = 1
stages = wl569, wl570, wl571, wl572, wl573, wl574, wl575, wl576,
          wl577, wl578, wl579, wl580, wl581, wl582, wl583, wl584, wl585
```

The real payload has exactly the 17 stage labels `wl569` through `wl585`, in
numeric order. The CLI prints one `stage_count=17` line and one aggregate
`status=ok|issues` line. Strict mode exits nonzero if a stage is missing,
unknown, mislabeled, malformed, has an unallowlisted field, has a changed
false no-claim flag, or fails a required proof certificate. It never reads a
legacy result and never launches one subprocess per worklog. The C3 CLI test
has exactly one subprocess invocation.

The parity test may read only the explicit result dictionary above. It must
compare `semantic_projection(project_stage(c3, wl), wl)` with the same
projection of the corresponding legacy JSON for all 17 stages. The test must
also assert stage order, exact allowlist keys, all 17 regular files, failed
predecessor behavior, malformed and unknown-stage rejection, unknown-field
rejection, and every top-level and proof-status no-claim invariant.

## Bounded Implementation Slices

### Slice 1: wl569-wl574

Implement only `c3_real_branch.py` and
`tests/theory/aa_bb/test_c3_real_branch.py`. Start from canonical C2 `wl568`
and compute the unique real ratio, exact two-variable converse, product
quartic and genus-five cover, the `tau=1/2` genus drop, the integrality closure
of that exceptional branch, generic denominator coupling, and the common
Delta squareclass double split.

Focused checks must cover the exact `F` sign and `rho_ell` root, all three
`wl570` formulas and converse reconstruction, the six `wl571` resultants,
generic and exceptional Riemann-Hurwitz counts, the `ell=8` exceptional
witness with populated source squares, the `a^2|4*m*n`, `b^2|m*n`, and
`Delta|K` support grid, and the `wl574` complementary split and gcd supports.
This slice must parity-check only `wl569`-`wl574`, preserve all listed false
flags, and not add any quotient, rank, or `wl575+` dependency.

### Slice 2: wl575-wl580

Implement only `c3_magnitude_descent.py` and
`tests/theory/aa_bb/test_c3_magnitude_descent.py`. Consume canonical `wl574`
once, compute the scaled rotation and exact resultants, classify regular and
singular odd-prime transport, remove all odd allocation freedom, prove the
dyadic same-side identity, and build the genus-one Mobius magnitude system
with the exact `wl580` self-consistency relation.

Focused checks must cover all four rotation identities and both norm/resultant
certificates, the `K`/`P` transport truth table, singular higher-valuation
branches, `Delta|K` same-side reduction, normalized dyadic valuation order,
the two remaining magnitude equations, the Mobius map and ordering, the
primitive `(m,n)` no-extra-branch converse, and the exact self-consistent
missing lemma. This slice must not enter `wl581`, quotient geometry, or M3.

### Slice 3: wl581-wl585

Implement only `c3_quotient_limits.py` and
`tests/theory/aa_bb/test_c3_quotient_limits.py`. Consume canonical `wl580`
once, preserve the genus-two and `Q(i)` quotient maps, prove the rational-locus
equivalence, retain both source squares on the genus-one torsor, impose the
pointwise prime parameter, and compute the fixed-`ell` genus-one, genus-
seventeen, genus-three, and elliptic quotient certificates.

Focused checks must cover the reciprocal involutions and quotient equations,
the real/imaginary reconstruction and automatic `S^2+16` square, torsor
forward/converse maps, branch supports and Riemann-Hurwitz counts, the
independent connected square-X lift, the pointwise `ell=L(X,tau)` identities,
the `4*G_ell(X)` discriminant, the fixed-`ell` boundary points, the genus-17
branch checks, the combined reciprocal elliptic equation, and every restricted
image false flag. This slice must not claim that any unrestricted curve rank,
torsor point, or elliptic quotient solves the active intersection.

### Composition checkpoint

Only after all three bounded slice tests pass independently may the
orchestrator and `test_c3_cli.py` be added. The composition test must verify
that C2 is built once, each C3 slice is built once, and the final evidence has
exactly 17 stages. It must include one explicit legacy-result parity test
parameterized over the fixed dictionary, fail-closed predecessor and
malformed-stage checks, and all no-claim checks. It must not switch consumers,
delete old artifacts, modify C2, or enter `wl586+`.

## Focused Validation

The future implementation slices may run only their focused tests, targeted
Ruff, formatter checks, `py_compile`, explicit dependency/reference scans,
deterministic temporary CLI output, and `git diff --check`. They must not run
the full suite or a consumer cutover. The exact future test commands are:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c3_real_branch.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c3_magnitude_descent.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c3_quotient_limits.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/theory/aa_bb/test_c3_cli.py
```

For this design-only task, validation is limited to the new Markdown file:
ASCII/reference inspection, Markdown structure and link/path inspection, the
new-file `git diff --check`, and inspection of the diff for that file. No code,
tests, result payloads, worklogs, plans, active-task files, consumers, or full
suite may be changed or executed as part of this audit.

## Risks And Gates

| Risk | Required response |
| --- | --- |
| The old scripts hide an obligation in recursive `input_checkpoint` or `ready` metadata. | Recompute exact formulas and inspect `work_log`, required proof keys, and false no-claim values; never treat a cached status as proof. |
| `wl572` exceptional closure is generalized to `tau!=1/2`. | Keep the exceptional `ell=8` witness and the generic false flag in separate fields and tests. |
| `wl580` self-consistency is mistaken for a solved genus-one family. | Preserve `exact_missing_lemma` and `self_consistent_genus_one_family_solved_here=false`. |
| A quotient or torsor point is treated as a `wl535` candidate. | Require positive square `X`, individual source/norm lifts, the selected real interval, and the prime parameter in every restricted-image boundary. |
| `wl581` automatic `S^2+16` square is counted as a new obstruction. | Preserve the explicit nonbranch forward/inverse descent and `wl581_unrestricted_elliptic_route_exhausted_here=true`. |
| `wl583` forgets the independent square-X lift. | Retain the divisor/branch-support certificate and the connected degree-two pullback. |
| `wl584` promotes pointwise prime coupling to an identity of whole torsor families. | Keep the incidence qualifier `ell=L(X,tau)` in the stage payload and parity test. |
| `wl585` treats the genus-three elliptic quotient as the full genus-seventeen problem. | Retain all four squareclasses and the restricted combined elliptic image false flag. |
| A broad C3 rewrite crosses the review boundary. | Require separate parity acceptance for `wl569-wl574`, `wl575-wl580`, and `wl581-wl585` before composition. |

## Acceptance

`design_ready` is justified. The audit identifies all 17 exact legacy asset
paths, maps every independent formula, witness, converse, exceptional branch,
genus calculation, square lift, prime-parameter boundary, and route-exhaustion
certificate to a canonical destination, defines exact semantic allowlists and
no-claim flags, protects the C2 input and M3 boundary, specifies result-free
runtime dependencies and one strict CLI, and divides implementation into
three bounded review slices. No implementation, result materialization,
consumer cutover, deletion, `wl586+` work, or new mathematics is authorized by
this design.
