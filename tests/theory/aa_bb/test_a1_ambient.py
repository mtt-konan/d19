from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.a1_ambient import classify_point, verify_cover_certificate
from scripts.theory.aa_bb.a1_certificates import load_certificates

DATA = ROOT / "data/theory/aa_bb/wl500"


def test_all_twelve_certificates_verify_exactly() -> None:
    rows = load_certificates(DATA / "a1-certificates.v1.json")
    assert len(rows) == 12
    assert all(verify_cover_certificate(row).passed for row in rows)
    assert sum(row["status"] == "globally_not_soluble" for row in rows) == 4
    assert sum(row["status"] == "globally_soluble" for row in rows) == 8


def test_special_mordell_weil_certificates_are_retained() -> None:
    rows = load_certificates(DATA / "a1-certificates.v1.json")
    wl506 = next(
        row
        for row in rows
        if row["source_work_log"] == "wl506" and row["status"] == "globally_soluble"
    )
    assert wl506["mordell_weil_point_source"]["point_expression"] == "-49*G + T"
    wl514 = next(row for row in rows if row["source_work_log"] == "wl514")
    assert wl514["no_lift"]["rank"] == 1
    assert wl514["no_lift"]["prime"] == 17
    assert wl514["no_lift"]["rational_image_intersection"] == []


def test_wl519_fraction_point_and_wl491_filter() -> None:
    row = next(
        row
        for row in load_certificates(DATA / "a1-certificates.v1.json")
        if row["source_work_log"] == "wl519"
    )
    assert row["point_on_cover"]["X"] == "1260642/121"
    result = classify_point(
        {
            "candidate_id": row["candidate_ids"][0],
            "A": 10,
            "B": 9,
            "L": 10,
            "quotient": "AA",
            "parameters": row["parameters"],
            "point_on_E_L": row["point_on_E_L"],
            "complete_d_squareclass": row["d_vector"],
        }
    )
    assert result["centered_even_pullback_check"]["passed"]
    assert result["centered_even_pullback_check"]["values"]["t"] == "34858/693"
    assert result["blocking_reasons"] == ["BB_common_source_product_not_square", "M_not_positive"]


def test_wl491_denominator_zero_is_a_distinct_branch() -> None:
    result = classify_point(
        {
            "candidate_id": "boundary",
            "A": 1,
            "B": 1,
            "L": 1,
            "quotient": "AA",
            "parameters": {"p": 2, "q": 1},
            "point_on_E_L": {"X": -2, "Y": 0},
            "complete_d_squareclass": {"d_minus_p": 1, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 1},
        }
    )
    assert result == {
        "output_class": "missing_pullback_data",
        "blocking_reasons": ["centered_even_inverse_denominator_zero"],
    }


def _certificate(source: str, status: str) -> dict[str, object]:
    rows = load_certificates(DATA / "a1-certificates.v1.json")
    return copy.deepcopy(
        next(
            row
            for row in rows
            if row["source_work_log"] == source and row["status"] == status
        )
    )


def test_altered_wl506_group_law_input_fails_closed() -> None:
    row = _certificate("wl506", "globally_soluble")
    row["mordell_weil_point_source"]["curve_generator"] = "G=(-304,5377)"
    assert not verify_cover_certificate(row).passed


def test_altered_wl514_residue_images_fail_closed() -> None:
    row = _certificate("wl514", "globally_not_soluble")
    row["no_lift"]["rational_reduction_image"][1] = "(2,2)"
    assert not verify_cover_certificate(row).passed


def test_altered_torsion_lift_input_fails_closed() -> None:
    row = _certificate("wl500", "globally_not_soluble")
    row["no_lift"]["torsion_points"][1] = "(-327,0)"
    assert not verify_cover_certificate(row).passed
