from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c1_pure_v_ell import build_c1
from scripts.theory.aa_bb.c2_allocation import (
    C2_ALLOCATION_STAGES,
    build_c2_allocation,
    project_stage,
    semantic_projection,
)
from scripts.theory.aa_bb.c2_character_system import build_c2_character_system
from scripts.theory.aa_bb.c2_global_descent import build_c2_global_descent
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    c1 = build_c1()
    c2_slice_1 = build_c2_global_descent(c1["wl541"])
    c2_slice_2 = build_c2_character_system(c2_slice_1["wl552"])
    return build_c2_allocation(c2_slice_2["wl562"])


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
    if value > 1:
        kernel *= value
    return kernel


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def _bit(value: int) -> int:
    assert value in {-1, 1}
    return (1 - value) // 2


def _quartic_sign(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 4, prime)
    return -1 if residue == prime - 1 else residue


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: dict[str, dict[str, object]],
) -> None:
    for work_log in C2_ALLOCATION_STAGES:
        assert_projection_digest(
            "c2", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_wl563_complementary_split_and_coordinate_identities(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl563"]
    assert stage["factorization_certificate"] == {
        "product_equation": "a*b=2*(ell-1)/r*(Q*D)^2",
        "squarefree_kernel": "2*(ell-1)/r=kappa*h^2",
        "coprime_split": [
            "a=g*alpha*M^2",
            "b=g*beta*N^2",
            "alpha*beta=kappa",
        ],
        "scale_equation": "g*M*N=h*abs(Q*D)",
        "real_coordinate": "F=r*g^2*(alpha^2*M^4-beta^2*N^4)",
        "positivity": ("ell*(alpha^2*M^4-beta^2*N^4)+2*(ell-1)*kappa*M^2*N^2>0"),
    }
    for first in range(1, 80):
        for second in range(1, 80):
            if math.gcd(first, second) != 1:
                continue
            alpha = _squarefree_kernel(first)
            beta = _squarefree_kernel(second)
            kappa = _squarefree_kernel(first * second)
            assert math.gcd(alpha, beta) == 1
            assert alpha * beta == kappa
            assert math.isqrt(first // alpha) ** 2 == first // alpha
            assert math.isqrt(second // beta) ** 2 == second // beta
    ell, r, g, alpha, beta, m, n = sp.symbols("ell r g alpha beta m n")
    a = g * alpha * m**2
    b = g * beta * n**2
    assert sp.expand(r * (a**2 - b**2) - r * g**2 * (alpha**2 * m**4 - beta**2 * n**4)) == 0
    cone = ell * (a**2 - b**2) + 2 * (ell - 1) * a * b
    reduced = ell * (alpha**2 * m**4 - beta**2 * n**4) + 2 * (ell - 1) * alpha * beta * m**2 * n**2
    assert sp.expand(cone - g**2 * reduced) == 0


def test_wl564_dyadic_allocation_cases(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl564"]
    assert stage["allocation_certificate"] == {
        "r_mod_8": [1, 7],
        "ell_eq_5_mod_8": {
            "kappa_is_even": True,
            "r_eq_1_mod_8": "2|beta",
            "r_eq_7_mod_8": "2|alpha",
        },
        "ell_eq_1_mod_8": {
            "kappa_even_iff": "v_2(ell-1) is even",
            "r_eq_1_mod_8_when_even": "2|alpha",
            "r_eq_7_mod_8_when_even": "2|beta",
        },
    }
    for r_mod_8 in (1, 7):
        inverse = pow(r_mod_8, -1, 8)
        assert inverse % 8 == r_mod_8
        assert 7 * inverse % 8 == (7 if r_mod_8 == 1 else 1)
    for valuation in range(2, 12):
        assert ((valuation + 1) % 2 == 1) == (valuation % 2 == 0)
    assert (2 + 1) % 2 == 1


def test_wl565_inert_and_split_allocation_rules(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl565"]
    assert stage["allocation_certificate"] == {
        "normalized_unit": "U_q=(F/r)/q^v_q(F/r) mod q",
        "valuation_parity": "v_q(F/r)=2*v_q(g)",
        "q_divides_alpha": "Legendre(U_q,q)=Legendre(-1,q)",
        "q_divides_beta": "Legendre(U_q,q)=1",
        "q_eq_3_mod_4": "character uniquely selects alpha or beta",
        "q_eq_1_mod_4": "U_q must be square but side remains unresolved",
    }
    for prime in (3, 5, 7, 11, 13, 17, 19):
        for unit in range(1, prime):
            assert _legendre(-(unit * unit), prime) == _legendre(-1, prime)
            assert _legendre(unit * unit, prime) == 1
    for prime in (3, 7, 11, 19, 23, 31):
        assert prime % 4 == 3
        assert _legendre(-1, prime) == -1
        assert {-1: "alpha", 1: "beta"}[-1] == "alpha"
        assert {-1: "alpha", 1: "beta"}[1] == "beta"


def test_wl566_quartic_sign_and_unresolved_equal_case(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl566"]
    assert stage["quartic_certificate"] == {
        "quartic_sign": "chi_4,q(H)=H^((q-1)/4)",
        "q_divides_alpha": "chi_4,q(H)=(-1)^((q-1)/4)*Legendre(beta,q)",
        "q_divides_beta": "chi_4,q(H)=Legendre(alpha,q)",
        "decision_rule": "different predicted signs uniquely select the side",
        "failure_rule": "equal predicted signs leave the side unresolved",
    }
    for prime in (5, 13, 17, 29, 37, 41):
        for opposite_factor in range(1, prime):
            for square_variable in range(1, prime):
                square = opposite_factor * square_variable * square_variable
                assert _quartic_sign(-(square**2), prime) == (
                    (-1) ** ((prime - 1) // 4) * _legendre(opposite_factor, prime)
                )
                assert _quartic_sign(square**2, prime) == _legendre(opposite_factor, prime)
    seen_equal = False
    seen_different = False
    for prime in (5, 13, 17, 29, 37, 41):
        delta = (-1) ** ((prime - 1) // 4)
        for alpha_0 in range(1, prime):
            for beta_0 in range(1, prime):
                first = delta * _legendre(beta_0, prime)
                second = _legendre(alpha_0, prime)
                seen_equal |= first == second
                seen_different |= first != second
    assert seen_equal and seen_different


def test_wl567_affine_rows_match_exhaustive_branch_assignments(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl567"]
    assert stage["affine_system_certificate"] == {
        "variable": "x_q=1 iff q|alpha",
        "off_diagonal": "A_qt=(1-Legendre(t,q))/2",
        "diagonal": "Delta_q=d_q+a_q+b_q+sum_(t!=q) A_qt",
        "right_hand_side": "z_q+a_q",
        "row": "Delta_q*x_q+sum_(t!=q) A_qt*x_t=z_q+a_q",
        "outcomes": ["inconsistent", "unique", "explicit affine space"],
    }
    primes = [5, 13, 17]
    alpha_fixed = 2
    beta_fixed = 3
    for assignment in itertools.product((0, 1), repeat=len(primes)):
        for row_index, q in enumerate(primes):
            a_q = _bit(_legendre(alpha_fixed, q))
            b_q = _bit(_legendre(beta_fixed, q))
            d_q = ((q - 1) // 4) % 2
            off_diagonal = {
                index: _bit(_legendre(t, q)) for index, t in enumerate(primes) if index != row_index
            }
            common = (
                sum(coefficient * assignment[index] for index, coefficient in off_diagonal.items())
                % 2
            )
            if assignment[row_index] == 0:
                z_q = (a_q + common) % 2
            else:
                z_q = (
                    d_q
                    + b_q
                    + sum(
                        coefficient * (1 - assignment[index])
                        for index, coefficient in off_diagonal.items()
                    )
                ) % 2
            delta_q = (d_q + a_q + b_q + sum(off_diagonal.values())) % 2
            left = (delta_q * assignment[row_index] + common) % 2
            assert left == (z_q + a_q) % 2


def test_wl568_redundancy_identities_and_missing_lemma(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl568"]
    assert stage["redundancy_certificate"] == {
        "scale": "2*r*a*b=E iff g*M*N=h*abs(Q*D)",
        "positivity": "original_strict_expression=ell*F+(ell-1)*E",
        "ratio": "2*F*A*B=E*(A^2-B^2)",
        "norm": (
            "C=E*(A^2+B^2)/(2*A*B); norm square factors into two ordered signed-ratio branches"
        ),
        "affine_rows": "necessary identities when z_q is computed from actual H",
    }
    assert stage["next_exact_lemma"] == (
        "selected B_pi/R_pi orientation intersected with F^2+E^2 square "
        "and the strict positivity condition"
    )
    assert stage["symbolic_certificate"] == {
        "positivity_identity": True,
        "scale_equivalent_after_squareclass_cancellation": True,
        "cone_is_coordinate_substitution": True,
        "norm_square_has_two_signed_ratio_branches": True,
    }
    for a in range(1, 20):
        for b in range(1, 20):
            for e in range(1, 20):
                f = Fraction(e * (a * a - b * b), 2 * a * b)
                c = Fraction(e * (a * a + b * b), 2 * a * b)
                assert c * c == f * f + e * e
    a, b, e = 3, 2, 5
    f = Fraction(e * (a * a - b * b), 2 * a * b)
    c = Fraction(e * (a * a + b * b), 2 * a * b)
    assert c * c == (-f) * (-f) + e * e
    assert 2 * (-f) * a * b != e * (a * a - b * b)


def test_all_stages_are_strict_and_keep_theorem_boundary(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C2_ALLOCATION_STAGES
    for _work_log, stage in evidence.items():
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["advance_to_m3"] is False
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False
    assert evidence["wl567"]["theorem_level_selmer_matrix_claimed"] is False


def test_slice_fails_closed_on_unready_wl562(monkeypatch) -> None:
    import scripts.theory.aa_bb.c2_allocation as module

    monkeypatch.setattr(module, "_wl562_ready", lambda _: False)
    c1 = build_c1()
    c2_slice_1 = build_c2_global_descent(c1["wl541"])
    c2_slice_2 = build_c2_character_system(c2_slice_1["wl552"])
    failed = module.build_c2_allocation(c2_slice_2["wl562"])
    assert failed["wl563"]["status"] == "issues"
    assert failed["wl563"]["violations"] == ["wl562_input_not_ready"]
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_or_mislabeled_stage(
    evidence: dict[str, dict[str, object]],
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl562")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl563"}, "wl564")
    malformed = dict(evidence["wl563"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl563")


def test_canonical_runtime_has_no_legacy_or_results_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c2_allocation.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "wl569",
        "C3",
        "c2_character_system",
    ):
        assert forbidden not in source
