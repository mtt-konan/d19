from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c1_local_tables import build_local_stages
from scripts.theory.aa_bb.c1_pure_v_ell import (
    C1Evidence,
    build_c1,
    project_stage,
    semantic_projection,
)
from scripts.theory.aa_bb.c1_wl539 import build_wl539
from scripts.theory.aa_bb.c1_wl540 import build_wl540
from scripts.theory.aa_bb.c1_wl541 import build_wl541
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> C1Evidence:
    return build_c1()


def test_full_stage_projections_have_frozen_digests(evidence: C1Evidence) -> None:
    for number in range(530, 542):
        work_log = f"wl{number}"
        assert_projection_digest(
            "c1", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_stages_are_strict_and_keep_theorem_boundary(evidence: C1Evidence) -> None:
    assert tuple(evidence.stages) == tuple(f"wl{number}" for number in range(530, 542))
    for work_log, stage in evidence.stages.items():
        assert stage["work_log"] == work_log
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage.get("advance_to_m3") is not True
        assert stage.get("complete_selmer_upper_bound_proved") is False
        assert stage.get("rank_zero_claimed") is False
        assert stage.get("sha2_trivial_claimed") is False


def test_wl535_protected_coordinate_kernel(evidence: C1Evidence) -> None:
    stage = evidence["wl535"]
    statement = stage["exact_coordinate_free_reformulation"]["statement"]
    assert "ell-q^2 is a rational square" in statement
    assert "ell*q^2+4 is a rational square" in statement
    assert "ell*q^4+4*q^2-4*ell > 0" in statement
    assert "V^2 = q^8" in statement
    inverse = stage["q_root_coordinate_reduction"]["inverse_and_branch_analysis"]
    assert "u=(q-b)/(p+a)" in inverse["inverse_formula"]
    assert "u=(a-p)/(q+b)" in inverse["inverse_formula"]
    assert inverse["antipode_sign_branch"]["verified"] is True
    assert inverse["all_q_values_covered"] is True


def test_projection_fails_closed_on_unknown_or_mislabeled_stage(evidence: C1Evidence) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl529")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl530"}, "wl531")


def test_wl536_wl538_exact_local_tables(evidence: C1Evidence) -> None:
    expectations = {
        "wl536": (7, 5, 28, 5),
        "wl537": (11, 10, 44, 21),
        "wl538": (19, 15, 76, 53),
    }
    for work_log, (prime, residue, modulus, removed_class) in expectations.items():
        local_obstruction = evidence[work_log]["local_obstruction"]
        table = local_obstruction[f"mod_{prime}_case_table"]
        assert table[f"square_residues_mod_{prime}"] == sorted(
            {value * value % prime for value in range(prime)}
        )
        assert table[f"target_ell_residue_mod_{prime}"] == residue
        assert table[f"surviving_q_square_residues_mod_{prime}"] == []
        assert table["obstruction_proved"] is True
        assert local_obstruction[f"removed_prime_class_mod_{modulus}"] == removed_class


def test_wl539_recomputes_full_good_reduction_exhaustion(evidence: C1Evidence) -> None:
    stage = evidence["wl539"]
    large = stage["large_prime_argument"]
    finite = stage["finite_classification"]
    assert large["factor_degrees"] == [1, 1, 1, 4]
    assert large["total_weil_error_coefficient"] == 41
    assert large["maximum_zero_residue_contribution"] == 7
    assert large["first_relevant_prime_with_strict_bound"] == 1907
    assert finite["checked_auxiliary_prime_count"] == 149
    assert finite["excluding_pairs"] == [(7, 5), (11, 10), (19, 15), (23, 5)]
    assert stage["new_local_obstruction"]["prime_class_mod_92"] == 5


def test_wl540_recomputes_parameter_prime_split(evidence: C1Evidence) -> None:
    stage = evidence["wl540"]
    symbolic = stage["symbolic_certificate"]
    assert symbolic["reduced_discriminant_equals_2_pow_29"] is True
    assert symbolic["gaussian_factorization_verified"] is True
    assert symbolic["root_squareclass_identity_verified"] is True
    assert stage["G_local_split"]["root_branch_only_if_ell_mod_8"] == 1
    assert (
        stage["G_local_split"]["unit_squareclass_after_even_root_distance_still_required"] is True
    )


def test_wl541_recomputes_geometry_witnesses_and_hensel_data(
    evidence: C1Evidence,
) -> None:
    stage = evidence["wl541"]
    curve = stage["finite_field_curve"]
    geometry = curve["geometry_certificate"]
    assert geometry["degree"] == 8
    assert geometry["genus"] == 3
    assert geometry["discriminant_is_power_of_two"] is True
    assert geometry["rational_points_at_infinity"] == 2
    assert geometry["maximum_removed_points"] == 12
    assert geometry["first_claimed_prime_threshold"] == 61
    assert geometry["lower_bound_exceeds_removed_points"] is True
    assert [row["ell"] for row in curve["small_prime_witnesses"]] == [
        5,
        13,
        17,
        29,
        37,
        41,
        53,
    ]
    assert all(row["curve_equation_verified"] for row in curve["small_prime_witnesses"])
    assert stage["hensel_lift"]["unit_derivatives"] == ["2*a", "2*c", "2*V"]
    assert stage["hensel_lift"]["real_positivity_addressed"] is False


def test_computed_consolidated_evidence_keeps_m2_open_and_m3_closed(
    evidence: C1Evidence,
) -> None:
    assert all(stage["status"] == "ok" for stage in evidence.stages.values())
    assert all(
        stage["ready"] is True and stage["violations"] == [] for stage in evidence.stages.values()
    )
    assert evidence["wl530"]["proof_status"]["symbolic_complete_d_family_derived_here"] is True
    assert (
        evidence["wl535"]["proof_status"][
            "remaining_problem_is_direct_q_root_square_quartic_obstruction"
        ]
        is True
    )
    assert evidence["wl539"]["proof_status"]["method_exhausted_outside_four_pairs"] is True
    assert (
        evidence["wl541"]["proof_status"][
            "parameter_prime_standalone_local_obstruction_exhausted_here"
        ]
        is True
    )
    for stage in evidence.stages.values():
        assert stage.get("advance_to_m3", False) is False
        assert stage.get("complete_selmer_upper_bound_proved") is False
        assert stage.get("rank_zero_claimed") is False
        assert stage.get("sha2_trivial_claimed") is False
        assert stage["proof_status"].get("uniform_full_wl535_obstruction_proved_here") is not True


def test_second_half_builders_fail_closed_on_unready_predecessors() -> None:
    local = build_local_stages({})
    assert all(stage["status"] == "issues" for stage in local.values())
    assert local["wl536"]["violations"] == ["wl535_input_not_ready"]

    wl539 = build_wl539({})
    assert wl539["status"] == "issues"
    assert "wl538_input_not_ready" in wl539["violations"]

    wl540 = build_wl540({})
    assert wl540["status"] == "issues"
    assert "wl539_input_not_ready" in wl540["violations"]

    wl541 = build_wl541({})
    assert wl541["status"] == "issues"
    assert "wl540_input_not_ready" in wl541["violations"]
