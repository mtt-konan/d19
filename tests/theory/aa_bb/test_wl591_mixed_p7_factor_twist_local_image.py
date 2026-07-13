from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.wl591_mixed_p7_factor_twist_local_image import (
    build_wl591_mixed_p7_factor_twist_local_image,
)


def test_wl591_exact_image_and_named_mapping() -> None:
    payload = build_wl591_mixed_p7_factor_twist_local_image()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["local_image"] == ["[1]"]
    mapping = payload["named_survivor_mapping"]
    assert mapping["survive"] == [91205]
    assert mapping["deleted"] == [5, 3045, 66045]
    assert [row["Q7_class"] for row in mapping["rows"]] == [
        "[u]",
        "[7]",
        "[7u]",
        "[1]",
    ]


def test_wl591_complete_strata_and_hensel_inclusion() -> None:
    payload = build_wl591_mixed_p7_factor_twist_local_image()
    certificate = payload["proof_certificate"]
    checks = payload["verification"]["local_checks"]

    assert all(checks.values())
    assert checks["source_reduction_matches_frozen_model"] is True
    assert checks["all_nonpole_source_strata_force_class_1"] is True
    assert checks["all_pole_source_strata_force_class_1"] is True
    assert certificate["source_residue_certificate"]["regular_rows_mod_7"] == [
        (0, 2, 4),
        (0, 5, 3),
        (1, 2, 4),
        (1, 5, 3),
        (4, 1, 3),
        (4, 6, 4),
    ]
    assert certificate["infinity_certificate"]["rows_mod_7"] == [(3, 4), (4, 3)]
    assert certificate["pole_and_denominator_certificate"]["A_roots_mod_7"] == []
    assert (
        certificate["pole_and_denominator_certificate"]["checks"]["every_D_row_is_a_simple_t_pole"]
        is True
    )
    inclusion = certificate["inclusion_certificate"]
    assert inclusion["source_residue"]["W_mod_49"] == 16
    assert inclusion["source_residue"]["t_mod_49"] == 4
    assert inclusion["factor_unit_residues"] == {
        "F_plus_over_49_mod_7": 2,
        "F_minus_mod_7": 2,
    }


def test_wl591_retains_fixed_cover_and_aa_bb_lift() -> None:
    payload = build_wl591_mixed_p7_factor_twist_local_image()
    maps = payload["proof_certificate"]["frozen_maps_certificate"]

    assert all(maps["checks"].values())
    assert maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
    assert "source leg L=3, opposite leg=7" in maps["exact_aa_bb_lift"]
    assert "(N^2+9)*(M^2+9)=(Z/4)^2" in maps["exact_aa_bb_lift"]
    assert payload["proof_boundary"]["rational_point_classification"] is False
    assert payload["proof_boundary"]["advance_to_D2"] is False
