from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c3_quotient_limits import (
    C3_QUOTIENT_ALLOWLISTS,
    C3_QUOTIENT_STAGES,
    build_c3_quotient_limits,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


def _canonical_wl580() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl580",
        "object_layer": "m2_primitive_reconstruction_and_descent_exhaustion",
        "input_checkpoint": {"work_log": "wl579", "ready": True},
        "reconstruction_certificate": {
            "tau": "[X+2*z*(1-X)]/[X*(z+2)-2]",
            "denominator": "X*(z+2)-2>0 for X>1,z>0",
            "canonical_class": "[lambda]=[2*(tau^2+2*tau-1)]",
            "source_square_equivalence": [
                "z/lambda square reconstructs first source square",
                "w/lambda square reconstructs second source square",
            ],
            "strict_identity": "Abar*Dbar-Bbar*Cbar=2*(tau^2+1)*(X^2+4*X-4)",
        },
        "exact_missing_lemma": (
            "no positive rational point on the self-consistent genus-one magnitude "
            "torsor in the wl570 interval"
        ),
        "symbolic_certificate": {
            "tau_reconstruction": True,
            "strict_cross_identity": True,
            "first_product_ratio_identity": True,
            "second_product_ratio_identity": True,
        },
        "proof_status": {
            "tau_uniquely_reconstructed_from_X_z_here": True,
            "primitive_m_n_has_no_extra_branch_here": True,
            "canonical_squareclass_self_consistency_stated_here": True,
            "source_squares_reconstructed_from_self_consistent_torsor_here": True,
            "allocation_descent_exhausted_here": True,
            "self_consistent_genus_one_family_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        },
        "violations": [],
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
        "rational_wl535_point_produced_here": False,
    }


def _g_ell(ell_value: Fraction, x: Fraction) -> Fraction:
    return (
        x**4
        + (16 - 8 * ell_value) * x**3
        + (32 * ell_value**2 - 96 * ell_value + 72) * x**2
        + (32 * ell_value - 64) * x
        + 16
    )


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    return build_c3_quotient_limits(_canonical_wl580())


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(C3_QUOTIENT_ALLOWLISTS) == C3_QUOTIENT_STAGES
    for work_log in C3_QUOTIENT_STAGES:
        assert_projection_digest(
            "c3", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_stages_keep_exact_allowlists_and_no_claims(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C3_QUOTIENT_STAGES
    for work_log, stage in evidence.items():
        assert set(stage) == C3_QUOTIENT_ALLOWLISTS[work_log] | {"ready", "violations"}
        assert set(semantic_projection(stage, work_log)) == C3_QUOTIENT_ALLOWLISTS[work_log]
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["rational_wl535_point_produced_here"] is False
        assert stage["advance_to_m3"] is False
        assert stage["stop_after_current_task"] is True
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False
        assert stage["proof_status"]["advance_to_m3"] is False


def test_wl581_reciprocal_involution_and_restricted_image(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl581"]
    assert all(stage["symbolic_certificate"].values())
    quotient = stage["quotient_certificate"]
    assert quotient["genus_two_curve"] == "Z^2=X*a*b*c*d"
    assert quotient["genus_two_branch_count"] == 6
    assert quotient["base_involution"] == "X->-4/X"
    assert quotient["quadratic_lift"] == "(X,Z)->(-4/X,8*i*Z/X^3)"
    assert quotient["elliptic_coordinates"] == ["S=X-4/X", "Y=Z*(X-2*i)/X^2"]
    assert "Y nonzero" in quotient["candidate_image_restrictions"]

    for x in (Fraction(3, 2), Fraction(2), Fraction(7, 3)):
        transform = -Fraction(4, 1) / x
        assert transform - Fraction(4, 1) / transform == x - Fraction(4, 1) / x
        assert (8 * sp.I / sp.Rational(transform.numerator, transform.denominator) ** 3) * (
            8 * sp.I / sp.Rational(x.numerator, x.denominator) ** 3
        ) == 1


def test_wl582_real_imaginary_reconstruction_and_automatic_square(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl582"]
    assert all(stage["symbolic_certificate"].values())
    descent = stage["descent_certificate"]
    assert descent["elliptic_split"] == ["A^2-B^2=-S*L", "A*B=2*L"]
    assert descent["inverse"] == ["X=-2*A/B", "Z=A*X"]
    assert descent["automatic_square"] == "S^2+16=(X+4/X)^2"

    a_part = Fraction(3, 2)
    b_part = Fraction(2)
    x = -2 * a_part / b_part
    s = x - 4 / x
    ell_value = a_part * b_part / 2
    assert a_part * a_part - b_part * b_part == -s * ell_value
    assert a_part * b_part == 2 * ell_value
    assert s * s + 16 == (x + 4 / x) ** 2

    source_x = Fraction(7, 3)
    source_z = Fraction(5, 2)
    forward_a = source_z / source_x
    forward_b = -2 * source_z / source_x**2
    assert -2 * forward_a / forward_b == source_x
    assert forward_a * source_x == source_z


def test_wl583_torsor_maps_branch_supports_and_exception(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl583"]
    assert all(stage["symbolic_certificate"].values())
    fiber = stage["fiber_product_certificate"]
    assert fiber["torsor"] == ["U^2=a*b/(2*delta)", "V^2=c*d/(2*delta)"]
    assert fiber["product_elliptic_map"] == "Y=2*delta*U*V"
    assert fiber["generic_branch_supports"] == [
        "{0,infinity}",
        "{root(a),root(b)}",
        "{root(c),root(d)}",
    ]
    assert fiber["generic_genera"] == {"torsor": 1, "full_cover": 5}
    assert stage["proof_status"]["square_x_pullback_independent_and_connected_here"] is True
    assert stage["proof_status"]["square_x_torsor_points_solved_here"] is False

    x = Fraction(3)
    tau = Fraction(1, 2)
    delta = tau * tau + 2 * tau - 1
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    u_square = first * second / (2 * delta)
    v_square = third * fourth / (2 * delta)
    q = Fraction(2)
    p_square = u_square / q**2
    assert q**2 * p_square == u_square
    assert (2 * delta) ** 2 * u_square * v_square == first * second * third * fourth

    assert [-2, 2 * tau, 2 * tau + 4, 4 * tau - 2] == [-2, 1, 5, 0]
    assert [tau + 2, 1 - 2 * tau, 1, tau] == [Fraction(5, 2), 0, 1, Fraction(1, 2)]
    assert stage["symbolic_certificate"]["zero_fiber_factor_values"] is True
    assert stage["symbolic_certificate"]["infinity_leading_factor_values"] is True

    half_delta = Fraction(1, 2) ** 2 + 2 * Fraction(1, 2) - 1
    half_first = x * (Fraction(1, 2) + 2) - 2
    half_second = 2 * Fraction(1, 2) - x * (2 * Fraction(1, 2) - 1)
    half_third = x + 2 * Fraction(1, 2) + 4
    half_fourth = Fraction(1, 2) * (x + 4) - 2
    assert half_first * half_second / (2 * half_delta) == 5 * x - 4
    assert half_third * half_fourth / (2 * half_delta) == x * (x + 5)


def test_wl584_pointwise_prime_coupling_and_norm_discriminant(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl584"]
    assert all(stage["symbolic_certificate"].values())
    intersection = stage["intersection_certificate"]
    assert intersection["source_curve"] == ["U^2=X*(ell-X)", "V^2=ell*X+4"]
    assert intersection["source_boundary_points"] == ["(0,0,2)", "(0,0,-2)"]
    assert intersection["norm_discriminant"] == "4*G_ell(X)"
    assert intersection["source_curve_genus"] == 1
    assert intersection["square_x_source_cover_genus"] == 1

    x = Fraction(3)
    tau = Fraction(1, 2)
    delta = tau * tau + 2 * tau - 1
    ell_value = (tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau) / (2 * x * delta)
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    assert first * second / (2 * delta) == x * (ell_value - x)
    assert third * fourth / (2 * delta) == ell_value * x + 4
    f = x**2 + (8 - 4 * ell_value) * x - 4
    e = 4 * (ell_value - 1) * x
    g = f**2 + e**2
    assert e * tau**2 - 2 * f * tau - e == 0
    assert 4 * g == (-2 * f) ** 2 - 4 * e * (-e)
    assert ell_value >= 5 and x > 1 and e != 0
    positivity = ell_value * x**2 + 4 * x - 4 * ell_value
    cone = ell_value * (2 * tau * f / e) + 2 * (ell_value - 1) * tau
    assert cone == tau * positivity / (2 * (ell_value - 1) * x)
    assert Fraction(0) ** 2 == Fraction(0) * (ell_value - Fraction(0))
    assert Fraction(2) ** 2 == ell_value * Fraction(0) + 4


def test_wl585_genus_seventeen_cover_and_reciprocal_elliptic_quotient(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl585"]
    assert all(stage["symbolic_certificate"].values())
    cover = stage["cover_certificate"]
    assert cover["squareclasses"] == ["X", "ell-X", "ell*X+4", "G_ell(X)"]
    assert cover["cover_degree"] == 16
    assert cover["branch_count"] == 8
    assert cover["genus"] == 17
    assert cover["norm_bearing_quotient_genera"] == {
        "genus_1": 1,
        "genus_2": 6,
        "genus_3": 1,
    }
    assert cover["elliptic_coordinates"] == ["S=X-4/X", "Z=W/X^2"]
    assert stage["proof_status"]["restricted_combined_elliptic_image_solved_here"] is False

    for ell_value in (Fraction(5), Fraction(13)):
        boundary = 5 * ell_value**2 - 8 * ell_value + 4
        assert _g_ell(ell_value, Fraction(0)) == 16
        assert _g_ell(ell_value, ell_value) == boundary**2
        assert _g_ell(ell_value, -4 / ell_value) == 16 * boundary**2 / ell_value**4
        for x in (Fraction(3, 2), Fraction(2)):
            source_product = x * (ell_value - x) * (ell_value * x + 4)
            assert _g_ell(ell_value, -4 / x) == 16 * _g_ell(ell_value, x) / x**4
            assert (-4 / x) * (ell_value + 4 / x) * (
                ell_value * (-4 / x) + 4
            ) == 16 * source_product / x**4
            s = x - 4 / x
            quotient = (ell_value**2 - ell_value * s - 4) * (
                s**2 + (16 - 8 * ell_value) * s + 32 * ell_value**2 - 96 * ell_value + 80
            )
            assert quotient == source_product * _g_ell(ell_value, x) / x**4


def test_invalid_canonical_wl580_fails_closed() -> None:
    invalid = _canonical_wl580()
    invalid["proof_status"] = dict(invalid["proof_status"])
    invalid["proof_status"]["allocation_descent_exhausted_here"] = False
    failed = build_c3_quotient_limits(invalid)
    assert failed["wl581"]["status"] == "issues"
    assert failed["wl581"]["violations"] == ["wl580_input_not_ready"]
    assert failed["wl581"]["proof_status"] == {}
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_missing_and_mislabeled_stages(
    evidence: dict[str, dict[str, object]],
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl580")
    with pytest.raises(KeyError):
        project_stage(evidence, "wl586")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl582"}, "wl581")
    malformed = dict(evidence["wl581"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl581")
    missing = dict(evidence["wl582"])
    del missing["descent_certificate"]
    with pytest.raises(ValueError):
        semantic_projection(missing, "wl582")
    mutated = dict(evidence["wl585"])
    mutated["proof_status"] = dict(mutated["proof_status"])
    mutated["proof_status"]["restricted_combined_elliptic_image_solved_here"] = True
    with pytest.raises(ValueError):
        semantic_projection(mutated, "wl585")


def test_canonical_runtime_has_no_legacy_or_future_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c3_quotient_limits.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "subprocess",
        "wl586",
        "c2_",
        "ellrank",
        "rank(",
    ):
        assert forbidden not in source
