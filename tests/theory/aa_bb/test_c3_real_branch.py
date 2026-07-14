from __future__ import annotations

import math
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c3_real_branch import (
    C3_REAL_BRANCH_ALLOWLISTS,
    C3_REAL_BRANCH_STAGES,
    build_c3_real_branch,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


def _canonical_wl568() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl568",
        "object_layer": "m2_trivial_unit_selected_orientation_norm_intersection",
        "input_checkpoint": {"work_log": "wl567", "ready": True},
        "next_exact_lemma": (
            "selected B_pi/R_pi orientation intersected with F^2+E^2 square and "
            "the strict positivity condition"
        ),
        "redundancy_certificate": {
            "affine_rows": "necessary identities when z_q is computed from actual H",
            "norm": (
                "C=E*(A^2+B^2)/(2*A*B); norm square factors into two ordered signed-ratio branches"
            ),
            "positivity": "original_strict_expression=ell*F+(ell-1)*E",
            "ratio": "2*F*A*B=E*(A^2-B^2)",
            "scale": "2*r*a*b=E iff g*M*N=h*abs(Q*D)",
        },
        "symbolic_certificate": {
            "cone_is_coordinate_substitution": True,
            "norm_square_has_two_signed_ratio_branches": True,
            "positivity_identity": True,
            "scale_equivalent_after_squareclass_cancellation": True,
        },
        "proof_status": {
            "advance_to_m3": False,
            "affine_rows_automatic_for_actual_factorization_here": True,
            "allocation_route_independent_obstruction_refuted_here": True,
            "cone_is_exact_original_positivity_rewrite_here": True,
            "scale_is_exact_product_coordinate_rewrite_here": True,
            "selected_orientation_norm_intersection_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
        },
        "violations": [],
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
        "rational_wl535_point_produced_here": False,
    }


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    return build_c3_real_branch(_canonical_wl568())


def _squarefree_kernel(value: int) -> int:
    kernel = 1
    prime = 2
    while prime * prime <= value:
        exponent = 0
        while value % prime == 0:
            exponent += 1
            value //= prime
        if exponent % 2:
            kernel *= prime
        prime += 1
    return kernel * value


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(C3_REAL_BRANCH_ALLOWLISTS) == C3_REAL_BRANCH_STAGES
    for work_log in C3_REAL_BRANCH_STAGES:
        assert_projection_digest(
            "c3", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_stages_keep_exact_allowlists_and_no_claims(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C3_REAL_BRANCH_STAGES
    for work_log, stage in evidence.items():
        assert set(stage) == C3_REAL_BRANCH_ALLOWLISTS[work_log] | {"ready", "violations"}
        assert set(semantic_projection(stage, work_log)) == C3_REAL_BRANCH_ALLOWLISTS[work_log]
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


@pytest.mark.parametrize("ell", [5, 13, 17, 29, 37, 101])
def test_wl569_endpoint_bounds_and_cone_root(ell: int) -> None:
    rho = (math.sqrt((ell - 1) ** 2 + ell**2) - (ell - 1)) / ell
    assert math.sqrt(2) - 1 < rho < 0.5
    assert abs(ell * (rho * rho - 1) + 2 * (ell - 1) * rho) < 1e-12
    assert ell * (0.5 * 0.5 - 1) + 2 * (ell - 1) * 0.5 > 0


@pytest.mark.parametrize("ell", [5, 13, 17, 29])
def test_wl569_F_is_negative_through_candidate_interval(ell: int) -> None:
    for numerator in range(1, 100):
        x = ell * numerator / 100
        f = x * x + (8 - 4 * ell) * x - 4
        assert f < 0


def test_wl570_formula_and_converse_reconstruction() -> None:
    for x in (Fraction(3, 2), Fraction(2), Fraction(7, 3)):
        for tau in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            delta = tau * tau + 2 * tau - 1
            ell = (tau * x * x + 2 * x * tau * tau + 8 * x * tau - 2 * x - 4 * tau) / (
                2 * x * delta
            )
            f = x * x + (8 - 4 * ell) * x - 4
            e = 4 * (ell - 1) * x
            c = e * (1 + tau * tau) / (2 * tau)
            first_square = -((x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)) / (2 * x * delta)
            second_square = (x + 2 * tau + 4) * (x * tau + 4 * tau - 2) / (2 * delta)
            assert 2 * tau * f == e * (tau * tau - 1)
            assert ell - x == first_square
            assert ell * x + 4 == second_square
            assert c * c == f * f + e * e


def test_wl571_genus_resultants_and_tau_half_exception(evidence) -> None:
    stage = evidence["wl571"]
    symbolic = stage["symbolic_certificate"]
    assert symbolic["pairwise_resultants_verified"] is True
    assert symbolic["tau_half_has_infinity_and_zero_roots"] is True
    assert symbolic["tau_half_parameter_formula_verified"] is True
    assert stage["cover_certificate"]["product_curve_genus"] == 1
    assert stage["cover_certificate"]["generic_full_cover_branch_points"] == 6
    assert stage["cover_certificate"]["generic_full_cover_genus"] == 5
    assert stage["cover_certificate"]["tau_half_full_cover_branch_points"] == 4
    assert stage["cover_certificate"]["tau_half_full_cover_genus"] == 1
    tau = Fraction(1, 2)
    for x in (Fraction(3, 2), Fraction(2), Fraction(9, 4)):
        delta = tau * tau + 2 * tau - 1
        ell = (tau * x * x + 2 * x * tau * tau + 8 * x * tau - 2 * x - 4 * tau) / (2 * x * delta)
        p_square = -((x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)) / (2 * x * delta)
        s_square = (x + 2 * tau + 4) * (x * tau + 4 * tau - 2) / (2 * delta)
        assert ell == x + 5 - 4 / x
        assert p_square == 5 - 4 / x
        assert s_square == x * (x + 5)


def test_wl572_exceptional_integrality_closure(evidence) -> None:
    for b in range(1, 30):
        for a in range(-60, 61):
            if a == 0 or gcd(a, b) != 1:
                continue
            x = Fraction(a * a, b * b)
            ell = x + 5 - 4 / x
            if ell.denominator == 1:
                assert b == 1
                assert a * a in {1, 4}
    stage = evidence["wl572"]
    assert stage["integrality_certificate"]["positivity"] == "X=q^2>1, hence X=4"
    assert Fraction(4) + 5 - Fraction(4, 4) == 8
    assert 5 - Fraction(4, 4) == 4
    assert Fraction(4) + 5 == 9
    assert stage["proof_status"]["generic_tau_cover_solved_here"] is False


def test_wl573_denominator_support_and_dyadic_boundary() -> None:
    for a in range(1, 16):
        for b in range(1, 12):
            if gcd(a, b) != 1:
                continue
            for m in range(1, 12):
                for n in range(m + 1, 16):
                    if gcd(m, n) != 1:
                        continue
                    delta = m * m + 2 * m * n - n * n
                    if delta <= 0:
                        continue
                    x = Fraction(a * a, b * b)
                    tau = Fraction(m, n)
                    d = tau * tau + 2 * tau - 1
                    ell = (tau * x * x + 2 * x * tau * tau + 8 * x * tau - 2 * x - 4 * tau) / (
                        2 * x * d
                    )
                    if ell.denominator != 1:
                        continue
                    k = a**4 + 4 * a * a * b * b - 4 * b**4
                    assert (4 * m * n) % (a * a) == 0
                    assert (m * n) % (b * b) == 0
                    assert gcd(delta, m * n) == 1
                    assert k % delta == 0
    for m in range(1, 30):
        for n in range(1, 30):
            if gcd(m, n) != 1:
                continue
            delta = m * m + 2 * m * n - n * n
            if (m - n) % 2:
                assert delta % 2 == 1
            else:
                assert delta % 4 == 2


def test_wl574_complementary_split_and_gcd_support() -> None:
    for first in range(1, 80):
        for second in range(1, 80):
            common = gcd(first, second)
            left = first // common
            right = second // common
            if gcd(left, right) != 1:
                continue
            k = _squarefree_kernel(left * right)
            alpha = _squarefree_kernel(left)
            beta = _squarefree_kernel(right)
            assert alpha * beta == k
            assert math.isqrt(left // alpha) ** 2 == left // alpha
            assert math.isqrt(right // beta) ** 2 == right // beta
    for a in range(1, 12):
        for b in range(1, 10):
            if gcd(a, b) != 1:
                continue
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            for m in range(1, 10):
                for n in range(1, 10):
                    if gcd(m, n) != 1:
                        continue
                    first = a * a * m + 2 * a * a * n - 2 * b * b * n
                    second = a * a * n + 2 * b * b * m - 2 * a * a * m
                    third = a * a * m + 4 * b * b * m - 2 * b * b * n
                    fourth = a * a * n + 2 * b * b * m + 4 * b * b * n
                    assert r1 % gcd(first, second) == 0
                    assert r2 % gcd(third, fourth) == 0


def test_invalid_canonical_wl568_fails_closed() -> None:
    invalid = _canonical_wl568()
    invalid["proof_status"] = dict(invalid["proof_status"])
    invalid["proof_status"]["allocation_route_independent_obstruction_refuted_here"] = False
    failed = build_c3_real_branch(invalid)
    assert failed["wl569"]["status"] == "issues"
    assert failed["wl569"]["violations"] == ["wl568_input_not_ready"]
    assert failed["wl569"]["proof_status"] == {}
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_missing_and_mislabeled_stages(evidence) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl568")
    with pytest.raises(KeyError):
        project_stage(evidence, "wl575")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl570"}, "wl569")
    malformed = dict(evidence["wl569"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl569")
    missing = dict(evidence["wl570"])
    del missing["system_certificate"]
    with pytest.raises(ValueError):
        semantic_projection(missing, "wl570")
    mutated = dict(evidence["wl572"])
    mutated["proof_status"] = dict(mutated["proof_status"])
    mutated["proof_status"]["generic_tau_cover_solved_here"] = True
    with pytest.raises(ValueError):
        semantic_projection(mutated, "wl572")


def test_canonical_runtime_has_no_legacy_or_future_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c3_real_branch.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "subprocess",
        "wl575",
        "wl586",
        "c3_magnitude_descent",
    ):
        assert forbidden not in source
