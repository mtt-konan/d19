from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

import scripts.theory.aa_bb.wl590_p5_factor_twist_local_image_comparison as wl590
from scripts.theory.aa_bb.wl590_p5_factor_twist_local_image_comparison import (
    build_wl590_from_d0,
    build_wl590_p5_factor_twist_local_image_comparison,
)


def test_wl590_proves_the_exact_p5_local_images() -> None:
    audit = build_wl590_p5_factor_twist_local_image_comparison()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl590"
    assert audit["verification"]["violations"] == []
    assert audit["local_images"] == {
        "pure_u7": [],
        "mixed_u3_v5_w17": ["[5]"],
    }


def test_wl590_keeps_the_named_survivor_mapping_exact() -> None:
    audit = build_wl590_p5_factor_twist_local_image_comparison()
    named = audit["named_survivor_mapping"]

    assert named["pure_u7"]["survive"] == []
    assert named["pure_u7"]["deleted"] == [
        1,
        97,
        105,
        265,
        1113,
        1385,
        5817,
        10185,
        14681,
        25705,
        107961,
        134345,
        564249,
        1424057,
        1541505,
        149525985,
    ]
    assert named["mixed_u3_v5_w17"]["survive"] == [5, 3045, 66045, 91205]
    assert named["mixed_u3_v5_w17"]["deleted"] == [
        21,
        29,
        37,
        85,
        357,
        493,
        629,
        3885,
        5365,
        22533,
        51765,
        383061,
    ]


def test_wl590_covers_all_p5_exceptional_strata_and_exact_lifts() -> None:
    audit = build_wl590_p5_factor_twist_local_image_comparison()

    assert all(audit["proof_certificate"]["pure_u7"]["checks"].values())
    assert all(audit["proof_certificate"]["mixed_u3_v5_w17"]["checks"].values())
    assert (
        audit["proof_certificate"]["pure_u7"]["factor_zero_certificate"]["checks"][
            "pure_factor_zero_branch_is_Q5_empty"
        ]
        is True
    )
    assert (
        audit["proof_certificate"]["mixed_u3_v5_w17"]["factor_zero_certificate"]["checks"][
            "factor_zero_branch_exists_by_Hensel"
        ]
        is True
    )
    assert (
        audit["proof_certificate"]["mixed_u3_v5_w17"]["zero_chart_certificate"]["checks"][
            "all_zero_chart_F5_rows_are_listed"
        ]
        is True
    )
    factor_zero = audit["proof_certificate"]["mixed_u3_v5_w17"]["factor_zero_certificate"]
    assert factor_zero["hensel_root_value_mod_5"] == 0
    assert factor_zero["hensel_root_derivative_mod_5"] == 1
    assert factor_zero["plus_zero_nonzero_factor_unit_mod_5"] in {1, 4}
    assert factor_zero["minus_zero_nonzero_factor_unit_mod_5"] in {1, 4}
    assert audit["fixed_cover_and_lift"]["pure_u7"]["source_leg"] == 7
    assert audit["fixed_cover_and_lift"]["pure_u7"]["opposite_leg"] == 2
    assert audit["fixed_cover_and_lift"]["mixed_u3_v5_w17"]["source_leg"] == 3
    assert audit["fixed_cover_and_lift"]["mixed_u3_v5_w17"]["opposite_leg"] == 7


def test_wl590_adapter_matches_default_rejects_invalid_d0_and_does_not_rebuild(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pure_payload = wl590.pure.build_wl587_pure_u7_d0_relative_2_descent()
    mixed_payload = wl590.mixed.build_wl589_mixed_d0_relative_2_descent()
    assert build_wl590_from_d0(pure_payload, mixed_payload) == (
        build_wl590_p5_factor_twist_local_image_comparison()
    )

    invalid = deepcopy(mixed_payload)
    invalid["verification"] = dict(invalid["verification"])
    invalid["verification"]["checks"] = dict(invalid["verification"]["checks"])
    first_check = next(iter(invalid["verification"]["checks"]))
    invalid["verification"]["checks"][first_check] = False
    with pytest.raises(ValueError):
        build_wl590_from_d0(pure_payload, invalid)
    invalid = deepcopy(mixed_payload)
    invalid["source_cover"] = {"bogus": True}
    with pytest.raises(ValueError):
        build_wl590_from_d0(pure_payload, invalid)
    with pytest.raises(ValueError):
        build_wl590_from_d0({"ready": True}, mixed_payload)

    calls = {"pure": 0, "mixed": 0}

    def counted_pure() -> dict[str, object]:
        calls["pure"] += 1
        return pure_payload

    def counted_mixed() -> dict[str, object]:
        calls["mixed"] += 1
        return mixed_payload

    monkeypatch.setattr(wl590.pure, "build_wl587_pure_u7_d0_relative_2_descent", counted_pure)
    monkeypatch.setattr(wl590.mixed, "build_wl589_mixed_d0_relative_2_descent", counted_mixed)
    build_wl590_from_d0(pure_payload, mixed_payload)
    assert calls == {"pure": 0, "mixed": 0}
