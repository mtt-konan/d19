from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c1_pure_v_ell import build_c1
from scripts.theory.aa_bb.c2_global_descent import (
    C2_GLOBAL_STAGES,
    build_c2_global_descent,
    project_stage,
    semantic_projection,
)
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    c1 = build_c1()
    return build_c2_global_descent(c1["wl541"])


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def _primes_below(limit: int) -> list[int]:
    return [
        n
        for n in range(3, limit, 2)
        if all(n % divisor for divisor in range(3, math.isqrt(n) + 1, 2))
    ]


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: dict[str, dict[str, object]],
) -> None:
    for work_log in C2_GLOBAL_STAGES:
        assert_projection_digest(
            "c2", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_wl542_denominator_support_and_local_converse(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl542"]
    assert stage["denominator_support"] == {
        "primitive_equations": [
            "A^2+Q^2=ell*D^2",
            "C^2=ell*Q^2+4*D^2",
        ],
        "D_is_odd": True,
        "gcd_D_ell": 1,
        "prime_conditions": [
            "r is congruent to 1 mod 4",
            "Legendre(ell/r)=1",
            "Legendre(r/ell)=1",
        ],
        "splitting_field": "Q(i,sqrt(ell))",
        "D_mod_ell_is_nonzero_square": True,
    }
    assert stage["local_converse"]["all_three_square_conditions_locally_compatible"] is True
    assert stage["local_converse"]["symbolic_factorization"] == {
        "G_leading_term_factorization_verified": True,
        "first_square_factorization_verified": True,
        "second_square_factorization_verified": True,
        "smallest_principal_unit_valuation_for_v_r_q_minus_k": "2*k",
    }


def test_wl543_real_quadratic_descent(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl543"]
    assert stage["descent"]["square_ideal_equation"] == "(alpha)=a^2"
    assert stage["descent"]["element_equation"] == "alpha=epsilon*beta^2"
    assert stage["unit_squareclass_split"]["norm_minus_one_unit_exists"] == {
        "class_count": 1,
        "epsilon_is_square": True,
    }
    assert stage["unit_squareclass_split"]["no_norm_minus_one_unit"]["class_count"] == 2


def test_wl544_explicit_quartic_reformulation(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl544"]
    assert stage["symbolic_certificate"]["automatic_conic_identity_verified"] is True
    assert stage["symbolic_certificate"]["G_homogenization_verified"] is True
    assert stage["explicit_system"]["reconstruction"] == [
        "q=F/N",
        "a=Z/N",
        "c=H/N",
        "V=W/N^4",
    ]
    assert stage["trivial_unit_branch"]["Gaussian_quartic"] == (
        "Z^2=ell*(u^2-ell*v^2)^2-16*u^2*v^2"
    )


def test_wl545_two_adic_dichotomy(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl545"]
    assert stage["q_valuation_dichotomy"] == {
        "ell_eq_5_mod_8": "v_2(q)=0",
        "ell_eq_1_mod_8": "v_2(q)>=3",
        "excluded_valuations": [1, 2],
    }
    assert stage["descent_variable_parity"]["primitive_normalization"] == "v_2(N)=2"
    assert stage["residue_certificate"]["G_unit_branch_residue_mod_8"] == 1


def test_wl546_gaussian_orientations(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl546"]
    assert stage["symbolic_certificate"]["Gaussian_norm_identity_verified"] is True
    assert stage["symbolic_certificate"]["essential_orientation_count"] == 2
    assert stage["Gaussian_descent"]["orientation_B"] == ("Q=+/-[b_0*(x^2-y^2)+2*a_0*x*y]")
    assert stage["Gaussian_descent"]["orientation_R"] == ("Q=+/-[a_0*(x^2-y^2)-2*b_0*x*y]")


def test_wl547_finite_gaussian_support(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl547"]
    assert stage["symbolic_certificate"]["P_plus_R_identity_verified"] is True
    assert stage["symbolic_certificate"]["root_polynomial"] == "t^2+4*t-4"
    assert stage["symbolic_certificate"]["root_discriminant"] == 32
    assert stage["finite_support"]["outside_support_Gaussian_valuations_are_even"] is True
    assert stage["proof_status"]["theorem_level_Selmer_object_claimed_here"] is False


def test_wl548_dyadic_squareclass_elimination(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl548"]
    assert stage["valuation_certificate"]["ell_eq_5_mod_8"]["v_1_plus_i_delta"] == 0
    assert stage["valuation_certificate"]["ell_eq_1_mod_8"]["v_1_plus_i_delta"] == 4
    assert stage["refined_support"]["contains_one_plus_i"] is False


def test_wl549_root_square_classification(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl549"]
    assert stage["identities_at_a_root"] == {
        "polynomial": "t^2+4*t-4",
        "one_minus_t": "t^2/4",
        "t_plus_four": "4/t",
        "root_is_nonzero": True,
    }
    for prime in _primes_below(200):
        roots = [t for t in range(1, prime) if (t * t + 4 * t - 4) % prime == 0]
        squares = [t for t in roots if _is_square(t, prime)]
        if prime % 8 == 7:
            assert len(roots) == 2 and len(squares) == 1
        elif prime % 8 == 1:
            assert len(roots) == 2 and len(squares) in {0, 2}
        else:
            assert roots == []


def _orientation_values(prime: int, a: int, b: int) -> tuple[set[int], set[int]]:
    first: set[int] = set()
    second: set[int] = set()
    for x in range(prime):
        for y in range(prime):
            denominator = (x * x + y * y) % prime
            if denominator == 0:
                continue
            inverse = pow(denominator, -1, prime)
            first.add((b * (x * x - y * y) + 2 * a * x * y) * inverse % prime)
            second.add((a * (x * x - y * y) - 2 * b * x * y) * inverse % prime)
    return first, second


def test_wl550_both_orientations_are_locally_compatible(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl550"]
    assert stage["proof_status"]["both_wl546_orientations_locally_compatible_here"] is True
    assert stage["proof_status"]["quadratic_etale_hilbert_90_witness_given_here"] is True
    for prime in _primes_below(50):
        norm_one = [
            (a, b) for a in range(prime) for b in range(prime) if (a * a + b * b) % prime == 1
        ]
        if not norm_one:
            continue
        a, b = norm_one[0]
        target = {
            q for q in range(prime) if any((x * x + q * q) % prime == 1 for x in range(prime))
        }
        first, second = _orientation_values(prime, a, b)
        assert first == target
        assert second == target


def test_wl551_norm_pairing(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl551"]
    assert stage["norm_certificate"]["conclusion"] == "Norm(d) is an integer square"
    assert stage["norm_certificate"]["reduced_factor"] == (
        "d=r up to a unit, with rational squarefree r|rad(ell-1)"
    )
    split_primes = [5, 13, 17]
    inert_primes = [3, 7, 11]
    for split_bits in itertools.product((0, 1), repeat=2 * len(split_primes)):
        for inert_bits in itertools.product((0, 1), repeat=len(inert_primes)):
            norm_exponents = {
                prime: split_bits[2 * index] + split_bits[2 * index + 1]
                for index, prime in enumerate(split_primes)
            }
            norm_exponents.update(
                {prime: 2 * inert_bits[index] for index, prime in enumerate(inert_primes)}
            )
            assert all(value % 2 == 0 for value in norm_exponents.values()) == all(
                split_bits[2 * index] == split_bits[2 * index + 1]
                for index in range(len(split_primes))
            )


def test_wl552_forced_unit_class_and_parities(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl552"]
    assert stage["parity_certificate"]["ell_eq_5_mod_8"]["forced_unit_class"] == "i"
    assert stage["parity_certificate"]["ell_eq_1_mod_8"]["gamma_factorization"] == (
        "gamma=(1+i)^2*gamma_0"
    )
    for m in range(-9, 10):
        for n in range(-9, 10):
            if (m - n) % 2 == 0:
                continue
            real = m * m - n * n
            imaginary = 2 * m * n
            assert real % 2 == 1
            assert imaginary % 2 == 0
            assert (-imaginary) % 2 == 0
            assert real % 2 == 1


def test_all_stages_are_strict_and_keep_theorem_boundary(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C2_GLOBAL_STAGES
    for _work_log, stage in evidence.items():
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["advance_to_m3"] is False
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False


def test_slice_fails_closed_on_unready_c1(monkeypatch, evidence) -> None:
    import scripts.theory.aa_bb.c2_global_descent as module

    monkeypatch.setattr(module, "_c1_wl541_ready", lambda _: False)
    c1 = build_c1()
    failed = module.build_c2_global_descent(c1["wl541"])
    assert failed["wl542"]["status"] == "issues"
    assert failed["wl542"]["violations"] == ["wl541_input_not_ready"]
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_or_mislabeled_stage(evidence) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl553")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl542"}, "wl543")
    malformed = dict(evidence["wl542"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl542")


def test_canonical_runtime_has_no_legacy_or_results_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c2_global_descent.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "wl553",
    ):
        assert forbidden not in source
