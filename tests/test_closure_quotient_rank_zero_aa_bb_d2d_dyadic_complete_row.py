from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d2d_dyadic_complete_row import (
    BOUNDARY,
    audit_rank_zero_aa_bb_d2d_dyadic_complete_row,
)


def _v2_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        raise ValueError("zero has no finite v2 in this test helper")
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def _q2_squareclass(x: Fraction) -> str:
    if x == 0:
        raise ValueError("zero has no squareclass in this test helper")
    v = _v2_int(x.numerator) - _v2_int(x.denominator)
    num = x.numerator
    den = x.denominator
    if v >= 0:
        num //= 2**v
    else:
        den //= 2 ** (-v)
    unit = (num % 8) * (den % 8) % 8
    if v % 2 == 0:
        return {1: "1", 7: "-1", 5: "5", 3: "-5"}[unit]
    return {1: "2", 7: "-2", 5: "10", 3: "-10"}[unit]


def _sample_complete_d_triples(L: int, T: int) -> set[tuple[str, str, str]]:
    sqrt_q = T * T + 4 * L * L
    p = 8 * L * L - 2 * T * T
    roots = [-p, 2 * sqrt_q, -2 * sqrt_q]
    triples: set[tuple[str, str, str]] = set()

    root_representatives = [
        (
            (roots[0] - roots[1]) * (roots[0] - roots[2]),
            roots[0] - roots[1],
            roots[0] - roots[2],
        ),
        (
            roots[1] - roots[0],
            (roots[1] - roots[0]) * (roots[1] - roots[2]),
            roots[1] - roots[2],
        ),
        (
            roots[2] - roots[0],
            roots[2] - roots[1],
            (roots[2] - roots[0]) * (roots[2] - roots[1]),
        ),
    ]
    for representative in root_representatives:
        triples.add(tuple(_q2_squareclass(Fraction(x)) for x in representative))

    modulus = 2**10
    for valuation in range(-6, 14):
        scale = Fraction(2**valuation) if valuation >= 0 else Fraction(1, 2 ** (-valuation))
        for odd_part in range(1, modulus, 2):
            x = odd_part * scale
            values = [x - root for root in roots]
            if any(value == 0 for value in values):
                continue
            if _q2_squareclass(values[0] * values[1] * values[2]) == "1":
                triples.add(tuple(_q2_squareclass(value) for value in values))
    return triples


def _d0_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D0_complete_d_container_definition",
        "d0_status": "framed_definition",
        "complete_d_container": {
            "name": "D0_complete_d_prelocal_container",
            "coordinate_tuple_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "defining_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
            "local_c_d_rows_built": False,
            "package_x_coordinates_used": False,
        },
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d1_support() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D1_relevant_place_support_confinement",
        "d1_status": "framed_and_proved_support_confinement",
        "candidate_support": {
            "equivalent_finite_set": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
        },
        "support_only_not_row_classification": True,
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2_rows() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2_local_C_d_row_characterization",
        "d2_status": "row_obligations_framed",
        "complete_d_coordinate_frame": {
            "coordinate_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "product_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
            "package_x_coordinates_used": False,
        },
        "local_row_obligations": [
            {"id": "D2a_odd_L_collision_row", "place_type": "ell|L"},
            {"id": "D2b_odd_T_collision_row", "place_type": "ell|T"},
            {"id": "D2c_odd_sqrt_q_collision_row", "place_type": "ell|sqrt_q"},
            {"id": "D2d_dyadic_complete_row", "place_type": "ell=2"},
            {"id": "D2e_real_sign_row", "place_type": "infinity"},
        ],
        "row_obligations_framed": True,
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d3_baseline() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D3_torsion_baseline_in_d_coordinates",
        "d3_status": "torsion_baseline_recorded_in_complete_d_coordinates",
        "baseline_comparison_contract": {
            "comparison_status": "pending_until_local_c_d_rows_are_solved",
            "quotient_baseline_here": False,
        },
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2a_row() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2a_odd_L_collision_row",
        "d2a_status": "pure_L_collision_row_solved",
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": ["D2a_odd_L_collision_row"],
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2b_row() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2b_odd_T_collision_row",
        "d2b_status": "pure_T_collision_row_solved",
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
        ],
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2c_row() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2c_odd_sqrt_q_collision_row",
        "d2c_status": "pure_sqrt_q_collision_row_solved",
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
            "D2c_odd_sqrt_q_collision_row",
        ],
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _audit() -> dict[str, object]:
    return audit_rank_zero_aa_bb_d2d_dyadic_complete_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
        d2c_row=_d2c_row(),
    )


def test_d2d_solves_dyadic_complete_row_by_two_valuation_strata() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D2d_dyadic_complete_row"
    assert audit["d2d_status"] == "dyadic_complete_row_solved"
    assert audit["complete_d_coordinate_order"] == [
        "d_minus_p",
        "d_pos_2sqrt_q",
        "d_neg_2sqrt_q",
    ]
    assert audit["dyadic_strata"] == [
        {
            "id": "ordinary_even_sqrt_q_stratum",
            "condition": "v2(T) != v2(L)+1, equivalently v2(sqrt_q) is even",
            "subcases": [
                "v2(T) < v2(L)+1 gives v2(sqrt_q)=2*v2(T)",
                "v2(T) > v2(L)+1 gives v2(sqrt_q)=2*v2(L)+2",
            ],
            "odd_unit_residue_dependence": False,
        },
        {
            "id": "balanced_odd_sqrt_q_stratum",
            "condition": "v2(T) == v2(L)+1, equivalently v2(sqrt_q)=2*v2(T)+1",
            "subcases": [
                "write L=2^a*l and T=2^(a+1)*t with l,t odd",
                "then sqrt_q=2^(2*a+2)*(l^2+t^2) has odd valuation 2*a+3",
            ],
            "odd_unit_residue_dependence": False,
        },
    ]


def test_d2d_records_allowed_q2_triples_in_complete_coordinate_order() -> None:
    audit = _audit()

    assert audit["solved_local_rows"] == [
        {
            "stratum_id": "ordinary_even_sqrt_q_stratum",
            "allowed_triple_rule": (
                "d_minus_p in {1,-1,5,-5}, d_neg_2sqrt_q in {1,5}, "
                "and d_pos_2sqrt_q=d_minus_p*d_neg_2sqrt_q"
            ),
            "allowed_triples": [
                ["1", "1", "1"],
                ["1", "5", "5"],
                ["-1", "-1", "1"],
                ["-1", "-5", "5"],
                ["5", "5", "1"],
                ["5", "1", "5"],
                ["-5", "-5", "1"],
                ["-5", "-1", "5"],
            ],
            "row_dimension_over_F2_local_only": 3,
        },
        {
            "stratum_id": "balanced_odd_sqrt_q_stratum",
            "allowed_triple_rule": (
                "d_minus_p in {1,-1}, d_neg_2sqrt_q in {1,2,5,10}, "
                "and d_pos_2sqrt_q=d_minus_p*d_neg_2sqrt_q"
            ),
            "allowed_triples": [
                ["1", "1", "1"],
                ["1", "2", "2"],
                ["1", "5", "5"],
                ["1", "10", "10"],
                ["-1", "-1", "1"],
                ["-1", "-2", "2"],
                ["-1", "-5", "5"],
                ["-1", "-10", "10"],
            ],
            "row_dimension_over_F2_local_only": 3,
        },
    ]
    assert audit["row_obstruction_remaining"] is False
    assert audit["row_depends_on_odd_unit_residues_of_L_or_T"] is False


def test_d2d_rows_match_finite_q2_sample_evidence_in_both_strata() -> None:
    audit = _audit()
    ordinary = {tuple(row) for row in audit["solved_local_rows"][0]["allowed_triples"]}
    balanced = {tuple(row) for row in audit["solved_local_rows"][1]["allowed_triples"]}

    assert _sample_complete_d_triples(1, 1) == ordinary
    assert _sample_complete_d_triples(1, 4) == ordinary
    assert _sample_complete_d_triples(4, 2) == ordinary
    assert _sample_complete_d_triples(1, 2) == balanced
    assert _sample_complete_d_triples(1, 6) == balanced
    assert _sample_complete_d_triples(2, 4) == balanced


def test_d2d_keeps_scope_below_full_matrix_and_leaves_overlaps() -> None:
    audit = _audit()

    assert audit["wl475_referenced_only"] is True
    assert audit["wl476_referenced_only"] is True
    assert audit["wl477_referenced_only"] is True
    assert audit["local_c_d_rows_partially_solved"] is True
    assert audit["local_c_d_rows_solved"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["remaining_d2_obligations"] == ["D2_multi_collision_overlaps"]
    assert audit["multi_collision_overlaps_solved_here"] is False
    assert audit["boundary"] == BOUNDARY


def test_d2d_rejects_missing_obligation_or_overadvanced_prior_row() -> None:
    d2 = _d2_rows()
    d2["local_row_obligations"] = [
        {"id": "D2a_odd_L_collision_row", "place_type": "ell|L"},
        {"id": "D2b_odd_T_collision_row", "place_type": "ell|T"},
        {"id": "D2c_odd_sqrt_q_collision_row", "place_type": "ell|sqrt_q"},
    ]
    d2c = _d2c_row()
    d2c["complete_selmer_upper_bound_proved"] = True

    audit = audit_rank_zero_aa_bb_d2d_dyadic_complete_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=d2,
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
        d2c_row=d2c,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d2d_obligation_missing",
        "d2c_already_claims_selmer_bound",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d2d_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    d2 = tmp_path / "d2.json"
    d3 = tmp_path / "d3.json"
    d2a = tmp_path / "d2a.json"
    d2b = tmp_path / "d2b.json"
    d2c = tmp_path / "d2c.json"
    out = tmp_path / "d2d.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")
    d2.write_text(json.dumps(_d2_rows()), encoding="utf-8")
    d3.write_text(json.dumps(_d3_baseline()), encoding="utf-8")
    d2a.write_text(json.dumps(_d2a_row()), encoding="utf-8")
    d2b.write_text(json.dumps(_d2b_row()), encoding="utf-8")
    d2c.write_text(json.dumps(_d2c_row()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d2d_dyadic_complete_row.py",
            "--d0-container",
            str(d0),
            "--d1-support",
            str(d1),
            "--d2-rows",
            str(d2),
            "--d3-baseline",
            str(d3),
            "--d2a-row",
            str(d2a),
            "--d2b-row",
            str(d2b),
            "--d2c-row",
            str(d2c),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d2d_status=dyadic_complete_row_solved" in result.stdout
    assert "full_c_d_matrix_built=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["solved_local_rows"][1]["stratum_id"] == "balanced_odd_sqrt_q_stratum"
    assert payload["remaining_d2_obligations"] == ["D2_multi_collision_overlaps"]
    assert payload["complete_selmer_upper_bound_proved"] is False
