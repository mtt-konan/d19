from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.c1_pure_v_ell import build_c1
from scripts.theory.aa_bb.c2_character_system import (
    C2_CHARACTER_STAGES,
    build_c2_character_system,
    project_stage,
    semantic_projection,
)
from scripts.theory.aa_bb.c2_global_descent import build_c2_global_descent
from tests.theory.aa_bb.projection_digests import assert_projection_digest


@pytest.fixture(scope="module")
def evidence() -> dict[str, dict[str, object]]:
    c1 = build_c1()
    c2_slice_1 = build_c2_global_descent(c1["wl541"])
    return build_c2_character_system(c2_slice_1["wl552"])


def _valuation(value: int, prime: int) -> int:
    if value == 0:
        return 100
    result = 0
    while value % prime == 0:
        result += 1
        value //= prime
    return result


def _v2(value: int) -> int:
    return _valuation(value, 2)


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def _is_nonzero_square(value: int, prime: int) -> bool:
    return value % prime != 0 and pow(value % prime, (prime - 1) // 2, prime) == 1


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def test_full_stage_semantic_projections_have_frozen_digests(
    evidence: dict[str, dict[str, object]],
) -> None:
    for work_log in C2_CHARACTER_STAGES:
        assert_projection_digest(
            "c2", work_log, semantic_projection(project_stage(evidence, work_log), work_log)
        )


def test_wl553_positivity_identity_and_cone_witnesses(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl553"]
    assert stage["positivity_certificate"] == {
        "identity": "H=(ell-1)*E+ell*F",
        "cone": "C_ell(m,n)=ell*(m^2-n^2)-2*(ell-1)*m*n",
        "ell_eq_5_mod_8": {
            "product_sign": "m*n<0",
            "condition": "C_ell(m,n)>0",
            "uniform_witness": "(m,n)=(5,-8)",
            "witness_value": "41*ell-80",
        },
        "ell_eq_1_mod_8": {
            "product_sign": "m*n>0",
            "condition": "C_ell(m,n)<0",
            "uniform_witness_family": "(m,n)=(1,2^k), k>=1",
        },
    }
    ell, q, d, r, m, n = sp.symbols("ell q d r m n")
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    e = 4 * (ell - 1) * q**2 * d**2
    f = r_form - e
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    cone = ell * (m**2 - n**2) - 2 * (ell - 1) * m * n
    assert sp.expand(h - ((ell - 1) * e + ell * f)) == 0
    assert sp.expand((ell - 1) * (-2 * r * m * n) + ell * r * (m**2 - n**2) - r * cone) == 0
    assert sp.expand((ell - 1) * (8 * r * m * n) - 4 * ell * r * (m**2 - n**2) + 4 * r * cone) == 0
    for ell_value in range(5, 300, 8):
        cone_value = ell_value * (25 - 64) - 2 * (ell_value - 1) * 5 * (-8)
        assert cone_value == 41 * ell_value - 80 and cone_value > 0
    for ell_value in range(5, 300, 8):
        for k in range(1, 12):
            n_value = 2**k
            assert ell_value * (1 - n_value * n_value) - 2 * (ell_value - 1) * n_value < 0


def test_wl554_canonical_gcd_class(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl554"]
    assert stage["gcd_certificate"] == {
        "Gaussian_square_coordinates": ["m^2-n^2", "2*m*n"],
        "odd_common_valuation_parity": "even",
        "candidate_coordinates": ["E=4*(ell-1)*Q^2*D^2", "F=R-E"],
        "canonical_class": "r=sqf_odd(gcd(E,F))=sqf_odd(gcd(ell-1,R))",
        "primewise_formula": "v_p(r)=min(v_p(ell-1),v_p(R)) mod 2",
    }
    for m in range(-30, 31):
        for n in range(-30, 31):
            if m == n == 0:
                continue
            common = math.gcd(m * m - n * n, 2 * m * n)
            assert all(_valuation(common, prime) % 2 == 0 for prime in (3, 5, 7, 11, 13, 17, 19))
    for ell in (5, 13, 17, 29, 37, 41):
        for q in range(1, 15):
            for d in range(1, 15):
                if math.gcd(q, d) != 1:
                    continue
                e = 4 * (ell - 1) * q * q * d * d
                r_value = q**4 + 4 * q * q * d * d - 4 * d**4
                common = math.gcd(e, r_value - e)
                for prime in (3, 5, 7, 11, 13, 17, 19):
                    assert _valuation(common, prime) == min(
                        _valuation(ell - 1, prime), _valuation(r_value, prime)
                    )


def test_wl555_standard_equation_and_delta_rotation(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl555"]
    assert stage["standard_equation"] == {
        "E": "4*(ell-1)*Q^2*D^2",
        "F": "Q^4+(8-4*ell)*Q^2*D^2-4*D^4",
        "Z": "F+i*E",
        "delta_relation": "delta=i*conjugate(Z)",
        "unit_free_square": "Z=r*(a+i*b)^2",
        "coordinate_equations": ["F=r*(a^2-b^2)", "E=2*r*a*b"],
        "uniform_positivity": "ell*(a^2-b^2)+2*(ell-1)*a*b>0",
        "canonical_r": "sqf_odd(gcd(ell-1,R))",
    }
    ell, q, d, r, a, b = sp.symbols("ell q d r a b")
    e = 4 * (ell - 1) * q**2 * d**2
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    f = r_form - e
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    assert sp.expand(f - (q**4 + (8 - 4 * ell) * q**2 * d**2 - 4 * d**4)) == 0
    assert sp.expand(h - ((ell - 1) * e + ell * f)) == 0
    assert (
        sp.expand(
            (ell - 1) * (2 * r * a * b)
            + ell * r * (a**2 - b**2)
            - r * (ell * (a**2 - b**2) + 2 * (ell - 1) * a * b)
        )
        == 0
    )
    e_real, f_real, r_real, a_real, b_real = sp.symbols(
        "e_real f_real r_real a_real b_real", real=True
    )
    z = f_real + sp.I * e_real
    delta = e_real + sp.I * f_real
    assert sp.simplify(delta - sp.I * sp.conjugate(z)) == 0
    gamma = a_real - sp.I * b_real
    substituted_delta = sp.I * r_real * gamma**2
    recovered_z = sp.conjugate(substituted_delta / sp.I)
    assert sp.expand_complex(recovered_z - r_real * (a_real + sp.I * b_real) ** 2) == 0


def test_wl556_orientation_selection_and_parity(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl556"]
    assert stage["orientation_certificate"] == {
        "convention": "a_0 odd and b_0 even",
        "B_pi_parity": "even",
        "R_pi_parity": "odd",
        "ell_eq_5_mod_8": {
            "Q_parity": "odd",
            "selected_orientation": "Q=+/-R_pi(x,y)",
        },
        "ell_eq_1_mod_8": {
            "minimum_v_2_Q": 3,
            "selected_orientation": "Q=+/-B_pi(x,y)",
            "remaining_condition": "v_2(B_pi)>=3",
        },
    }
    for a_0 in range(1, 16, 2):
        for b_0 in range(2, 16, 2):
            for x in range(-10, 11):
                for y in range(-10, 11):
                    if (x - y) % 2 == 0:
                        continue
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    r_pi = a_0 * (x * x - y * y) - 2 * b_0 * x * y
                    assert b_pi % 2 == 0 and r_pi % 2 == 1
    for a_0 in range(1, 100, 2):
        for b_0 in range(2, 100, 2):
            ell = a_0 * a_0 + b_0 * b_0
            if ell % 8 == 5:
                assert b_0 % 4 == 2
            elif ell % 8 == 1:
                assert b_0 % 4 == 0


def test_wl557_exact_valuation_strata(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl557"]
    assert stage["valuation_certificate"] == {
        "ell_eq_5_mod_8": {
            "selected_orientation": "R_pi",
            "valuation": 0,
            "new_condition": "none",
        },
        "ell_eq_1_mod_8": {
            "selected_orientation": "B_pi",
            "c": "v_2(b_0)>=2",
            "k": "v_2(x*y)>=1",
            "formula": {
                "c<k+1": "v_2(B_pi)=c",
                "c>k+1": "v_2(B_pi)=k+1",
                "c=k+1": "v_2(B_pi)>=c+1",
            },
            "minimum_three_condition": "(c=2 and k=1) or (c>=3 and k>=2)",
            "real_descent_match": "v_2(B_pi)=2+v_2(mu*nu)",
        },
    }
    for a_0 in range(1, 16, 2):
        for b_0 in range(4, 65, 4):
            c = _v2(b_0)
            for x in range(1, 32):
                for y in range(1, 32):
                    if (x - y) % 2 == 0:
                        continue
                    k = _v2(x * y)
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    value = _v2(b_pi)
                    if c < k + 1:
                        assert value == c
                    elif c > k + 1:
                        assert value == k + 1
                    else:
                        assert value >= c + 1
    for c in range(2, 8):
        for k in range(1, 8):
            can_reach_three = min(c, k + 1) >= 3 or c == k + 1 == 2
            stated = (c == 2 and k == 1) or (c >= 3 and k >= 2)
            assert can_reach_three == stated


def test_wl558_character_certificate_and_p13_witness(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl558"]
    assert stage["character_certificate"] == {
        "unit_place": "odd p|ell-1 with p not dividing R",
        "inert_p_mod_4_eq_3": "automatic in F_(p^2)",
        "split_p_mod_4_eq_1": "Legendre(F/r,p)=1",
        "generic_q_coordinate": "Legendre((t^2+4*t-4)/r,p)=1",
        "Q_or_D_boundary": "Legendre(r,p)=1",
        "nontrivial_example": {
            "p": 13,
            "t": 10,
            "f_t": 6,
            "source_residues_are_squares": True,
            "f_t_is_nonsquare": True,
        },
    }
    prime = 13
    t = 10
    assert all(_is_square(value, prime) for value in (t, 1 - t, t + 4))
    assert (t * t + 4 * t - 4) % prime == 6
    assert not _is_square(6, prime)
    for prime in (3, 7, 11, 19, 23, 31):
        assert all(pow(value, (prime * prime - 1) // 2, prime) == 1 for value in range(1, prime))


def test_wl559_leading_character_cases(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl559"]
    assert stage["leading_character_certificate"] == {
        "setup": "e=v_p(ell-1), k=v_p(R), d=min(e,k)>0 even",
        "normalized_element": "Z_d=(F+i*E)/p^d",
        "inert_case": "automatic from square norm in F_(p^2)",
        "split_master_condition": "Legendre((F_d+j*E_d)/r,p)=1",
        "e<k": "Legendre(L_e*(-1+j)/r,p)=1",
        "k<e": "Legendre((R/p^k)/r,p)=1",
        "e=k": "Legendre(L_e*(lambda-1+j)/r,p)=1",
    }
    for prime, j in ((5, 2), (13, 5), (17, 4), (29, 12), (37, 6)):
        assert j * j % prime == prime - 1
        for f_value in range(prime):
            for e_value in range(prime):
                first = (f_value + j * e_value) % prime
                second = (f_value - j * e_value) % prime
                if first == 0 or second == 0:
                    continue
                norm = first * second % prime
                if _is_nonzero_square(norm, prime):
                    assert _is_nonzero_square(first, prime) == _is_nonzero_square(second, prime)
    prime = 17
    j = 4
    r = 3
    e_d, r_d = 5, 0
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        e_d * (-1 + j) * pow(r, -1, prime)
    ) % prime
    e_d, r_d = 0, 7
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (r_d * pow(r, -1, prime)) % prime
    e_d, lambda_value = 6, 9
    r_d = lambda_value * e_d % prime
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        e_d * (lambda_value - 1 + j) * pow(r, -1, prime)
    ) % prime


def test_wl560_normalization_and_membership(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl560"]
    assert stage["normalized_character_certificate"] == {
        "d": "min(v_p(ell-1),v_p(R))",
        "epsilon": "d mod 2",
        "canonical_membership": "p|r iff epsilon=1",
        "reduced_class": "r_p=r/p^epsilon",
        "normalized_equation": "(F_d+i*E_d)=r_p*Gamma_p^2",
        "inert_case": "automatic",
        "split_master_condition": "Legendre((F_d+j*E_d)/r_p,p)=1",
        "e<k": "Legendre(L_e*(-1+j)/r_p,p)=1",
        "k<e": "Legendre((R/p^k)/r_p,p)=1",
        "e=k": "Legendre(L_e*(lambda-1+j)/r_p,p)=1",
    }
    for d in range(12):
        epsilon = d % 2
        gamma_exponent = (d - epsilon) // 2
        assert d == epsilon + 2 * gamma_exponent and epsilon in {0, 1}
    for prime in (3, 5, 7, 13):
        for d in range(8):
            epsilon = d % 2
            r = prime**epsilon * 11
            gamma = prime ** ((d - epsilon) // 2) * 7
            assert r * gamma * gamma // prime**d == 11 * 7 * 7


def test_wl561_matrix_and_reciprocity_cancellation(
    evidence: dict[str, dict[str, object]],
) -> None:
    stage = evidence["wl561"]
    assert stage["matrix_certificate"] == {
        "rows": "split p|ell-1",
        "columns": "all odd q|ell-1",
        "membership_vector": "epsilon_q=min(v_q(ell-1),v_q(R)) mod 2",
        "entry": "A_pq=(1-Legendre(q,p))/2",
        "row_equation": "n_p=sum_(q!=p) A_pq*epsilon_q mod 2",
        "reciprocity_product": (
            "prod_(p in S_split) Legendre(C_p,p)=prod_(p in S_split,q in S_inert) Legendre(q,p)"
        ),
        "split_only_corollary": "if S_inert is empty, the product is +1",
    }
    split_primes = [5, 13, 17, 29, 37]
    product = 1
    for index, p in enumerate(split_primes):
        for q in split_primes[index + 1 :]:
            assert _legendre(q, p) == _legendre(p, q)
            product *= _legendre(q, p) * _legendre(p, q)
    assert product == 1
    split = [5, 13, 17]
    inert = [3, 7, 11]
    left_class_product = 1
    for p in split:
        for q in split + inert:
            if q != p:
                left_class_product *= _legendre(q, p)
    inert_cross_product = 1
    for p in split:
        for q in inert:
            inert_cross_product *= _legendre(q, p)
    assert left_class_product == inert_cross_product


def _orientation_value(kind: str, x: int, y: int, prime: int) -> int:
    denominator = (x * x + y * y) % prime
    assert denominator != 0
    numerator = 2 * x * y if kind == "B" else x * x - y * y
    return numerator * pow(denominator, -1, prime) % prime


def test_wl562_exact_p13_witnesses(evidence: dict[str, dict[str, object]]) -> None:
    stage = evidence["wl562"]
    assert stage["witness_certificate"] == {
        "prime": 13,
        "local_ell": 1,
        "class_r": 1,
        "square_character_witness": {
            "t": 0,
            "f_t": 9,
            "row_bit": 0,
            "B_witness": [0, 1],
            "R_witness": [1, 1],
        },
        "nonsquare_character_witness": {
            "t": 10,
            "q": 6,
            "f_t": 6,
            "row_bit": 1,
            "B_witness": [1, 2],
            "R_witness": [1, 4],
        },
        "same_valuation_stratum": "d=0 and epsilon=0",
    }
    prime = 13
    for t, expected_f, expected_square in ((0, 9, True), (10, 6, False)):
        assert all(_is_square(value, prime) for value in (t, 1 - t, t + 4))
        f_t = (t * t + 4 * t - 4) % prime
        assert f_t == expected_f and _is_square(f_t, prime) is expected_square
    witnesses = {
        ("B", 0): (0, 1),
        ("B", 6): (1, 2),
        ("R", 0): (1, 1),
        ("R", 6): (1, 4),
    }
    for (kind, q), (x, y) in witnesses.items():
        assert _orientation_value(kind, x, y, prime) == q


def test_all_stages_are_strict_and_keep_theorem_boundary(
    evidence: dict[str, dict[str, object]],
) -> None:
    assert tuple(evidence) == C2_CHARACTER_STAGES
    for _work_log, stage in evidence.items():
        assert stage["status"] == "ok"
        assert stage["ready"] is True
        assert stage["violations"] == []
        assert stage["advance_to_m3"] is False
        assert stage["complete_selmer_upper_bound_proved"] is False
        assert stage["rank_zero_claimed"] is False
        assert stage["sha2_trivial_claimed"] is False
        assert stage["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False
    assert evidence["wl561"]["theorem_level_selmer_matrix_claimed"] is False


def test_slice_fails_closed_on_unready_wl552(monkeypatch) -> None:
    import scripts.theory.aa_bb.c2_character_system as module

    monkeypatch.setattr(module, "_wl552_ready", lambda _: False)
    c1 = build_c1()
    c2_slice_1 = build_c2_global_descent(c1["wl541"])
    failed = module.build_c2_character_system(c2_slice_1["wl552"])
    assert failed["wl553"]["status"] == "issues"
    assert failed["wl553"]["violations"] == ["wl552_input_not_ready"]
    assert all(stage["status"] == "issues" for stage in failed.values())


def test_projection_rejects_unknown_or_mislabeled_stage(
    evidence: dict[str, dict[str, object]],
) -> None:
    with pytest.raises(KeyError):
        project_stage(evidence, "wl552")
    with pytest.raises(ValueError):
        semantic_projection({"work_log": "wl553"}, "wl554")
    malformed = dict(evidence["wl553"])
    malformed["unexpected"] = True
    with pytest.raises(ValueError):
        semantic_projection(malformed, "wl553")


def test_canonical_runtime_has_no_legacy_or_results_dependency() -> None:
    source = (ROOT / "scripts/theory/aa_bb/c2_character_system.py").read_text(encoding="utf-8")
    for forbidden in (
        "audit_closure_",
        "results/",
        "importlib",
        ".glob(",
        ".rglob(",
        "wl563",
        "wl569",
        "C3",
        "c2_allocation",
    ):
        assert forbidden not in source
