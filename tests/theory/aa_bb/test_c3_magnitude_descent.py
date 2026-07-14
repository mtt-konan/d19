from __future__ import annotations

import math
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c3_magnitude_descent import (
    C3_MAGNITUDE_ALLOWLISTS,
    C3_MAGNITUDE_STAGES,
    build_c3_magnitude_descent,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


def _canonical_wl574() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl574",
        "object_layer": "m2_common_Delta_squareclass_double_split",
        "input_checkpoint": {"work_log": "wl573", "ready": True},
        "double_split_certificate": {
            "canonical_class": "2*Delta=k*h^2 with k positive squarefree",
            "source_products": ["A*B=k*U^2", "C*D=k*V^2"],
            "first_gcd_support": "gcd(A,B) divides 5*a^4-8*a^2*b^2+4*b^4",
            "second_gcd_support": "gcd(C,D) divides a^4+8*a^2*b^2+20*b^4",
            "first_split": "A/g1=alpha*r1^2, B/g1=beta*s1^2, alpha*beta=k",
            "second_split": "C/g2=gamma*r2^2, D/g2=delta0*s2^2, gamma*delta0=k",
        },
        "symbolic_certificate": {
            "AB_determinant_in_m": True,
            "AB_determinant_in_n": True,
            "CD_determinant_in_m": True,
            "CD_determinant_in_n": True,
            "R1_positive_completion": True,
        },
        "proof_status": {
            "both_source_pairs_share_canonical_Delta_squareclass_here": True,
            "AB_common_gcd_supported_on_R1_here": True,
            "CD_common_gcd_supported_on_R2_here": True,
            "two_complementary_splits_of_same_k_proved_here": True,
            "generic_genus_five_cover_solved_here": False,
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


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    return build_c3_magnitude_descent(_canonical_wl574())


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
    assert tuple(C3_MAGNITUDE_ALLOWLISTS) == C3_MAGNITUDE_STAGES
    for work_log in C3_MAGNITUDE_STAGES:
        assert_projection_digest(
            "c3", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_all_stages_keep_exact_allowlists_and_no_claims(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C3_MAGNITUDE_STAGES
    for work_log, stage in evidence.items():
        assert set(stage) == C3_MAGNITUDE_ALLOWLISTS[work_log] | {"ready", "violations"}
        assert set(semantic_projection(stage, work_log)) == C3_MAGNITUDE_ALLOWLISTS[work_log]
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


def test_wl575_rotation_and_primitive_gcd_certificates() -> None:
    for a in range(1, 40):
        for b in range(1, 40):
            if gcd(a, b) != 1:
                continue
            p = a**4 + 4 * b**4
            k_form = a**4 + 4 * a * a * b * b - 4 * b**4
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            expected = 1 if a % 2 else 4
            assert math.gcd(p, k_form) == expected
            assert math.gcd(r1, r2) == expected
    for a, b, m, n in ((1, 1, 2, 3), (2, 1, 3, 5), (3, 2, 5, 8)):
        first = a * a * m + 2 * a * a * n - 2 * b * b * n
        second = a * a * n + 2 * b * b * m - 2 * a * a * m
        third = a * a * m + 4 * b * b * m - 2 * b * b * n
        fourth = a * a * n + 2 * b * b * m + 4 * b * b * n
        p = a**4 + 4 * b**4
        k_form = a**4 + 4 * a * a * b * b - 4 * b**4
        r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
        r2 = a**4 + 8 * a * a * b * b + 20 * b**4
        assert r1 * third == p * first - 2 * k_form * second
        assert r1 * fourth == 2 * k_form * first + p * second
        assert p * p + 4 * k_form * k_form == r1 * r2


def test_wl576_wl577_transport_boundaries() -> None:
    for prime in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41):
        roots = [t for t in range(prime) if (t * t + 2 * t - 1) % prime == 0]
        legendre = pow(2, (prime - 1) // 2, prime)
        assert bool(roots) == (legendre == 1)
    for a in range(1, 20):
        for b in range(1, 20):
            if gcd(a, b) != 1:
                continue
            p_form = a**4 + 4 * b**4
            k_form = a**4 + 4 * a * a * b * b - 4 * b**4
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            for prime in (3, 5, 7, 11, 13, 17, 19):
                if k_form % prime == 0:
                    assert p_form % prime != 0
                    assert r1 % prime != 0
                    assert r2 % prime != 0


def test_wl578_dyadic_order_and_wl579_mobius() -> None:
    def v2(value: int) -> int:
        if value == 0:
            return 99
        exponent = 0
        while value % 2 == 0:
            exponent += 1
            value //= 2
        return exponent

    for diagonal in (1, 3, 5, 7):
        for off_diagonal in (2, 4, 6, 10):
            for first_exp in range(7):
                for second_exp in range(7):
                    if first_exp == second_exp:
                        continue
                    first = 2**first_exp
                    second = 2**second_exp
                    out_first = diagonal * first - off_diagonal * second
                    out_second = off_diagonal * first + diagonal * second
                    assert (v2(out_first) < v2(out_second)) == (first_exp < second_exp)
    for p, k_form in ((5, 1), (13, 2), (29, 3)):
        for z in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)):
            if 2 * k_form * z >= p:
                continue
            w = (2 * k_form + p * z) / (p - 2 * k_form * z)
            assert w > z
            assert w - z == 2 * k_form * (1 + z * z) / (p - 2 * k_form * z)


def test_wl580_reconstruction_identity() -> None:
    for x in (Fraction(3, 2), Fraction(2), Fraction(7, 3)):
        for tau in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            first = x * (tau + 2) - 2
            second = 2 * tau - x * (2 * tau - 1)
            if first == 0:
                continue
            z = second / first
            denominator = x * (z + 2) - 2
            if z <= 0:
                continue
            assert denominator > 0
            recovered = (x + 2 * z * (1 - x)) / denominator
            assert recovered == tau
    first = Fraction(7, 3)
    z = Fraction(5, 2)
    second = first * z
    assert first * second == first * first * z


def test_invalid_canonical_wl574_fails_closed() -> None:
    invalid = _canonical_wl574()
    invalid["proof_status"] = dict(invalid["proof_status"])
    invalid["proof_status"]["two_complementary_splits_of_same_k_proved_here"] = False
    failed = build_c3_magnitude_descent(invalid)
    assert failed["wl575"]["status"] == "issues"
    assert failed["wl575"]["violations"] == ["wl574_input_not_ready"]
    assert failed["wl575"]["proof_status"] == {}
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_missing_and_mislabeled_stages(
    evidence: dict[str, dict[str, object]],
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl574")
    with pytest.raises(KeyError):
        project_stage(evidence, "wl581")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl576"}, "wl575")
    malformed = dict(evidence["wl575"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl575")
    mutated = dict(evidence["wl580"])
    mutated["proof_status"] = dict(mutated["proof_status"])
    mutated["proof_status"]["self_consistent_genus_one_family_solved_here"] = True
    with pytest.raises(ValueError):
        semantic_projection(mutated, "wl580")


def test_canonical_runtime_has_no_legacy_or_future_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c3_magnitude_descent.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "subprocess",
        "wl581",
        "wl586",
        "c3_quotient_limits",
    ):
        assert forbidden not in source
