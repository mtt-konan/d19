from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

import scripts.theory.aa_bb.wl592_mixed_p17_factor_twist_local_image as wl592
from scripts.theory.aa_bb.wl592_mixed_p17_factor_twist_local_image import (
    build_wl592_from_mixed_d0,
    build_wl592_mixed_p17_factor_twist_local_image,
)


def test_wl592_exact_image_excludes_91205() -> None:
    payload = build_wl592_mixed_p17_factor_twist_local_image()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["local_image"] == ["[u]"]
    assert payload["target_twist"] == 91205
    assert payload["target_twist_class"] == "[17u]"
    assert payload["target_twist_in_image"] is False


def test_wl592_covers_integral_infinity_and_exceptional_strata() -> None:
    payload = build_wl592_mixed_p17_factor_twist_local_image()
    certificate = payload["proof_certificate"]
    checks = payload["verification"]["local_checks"]

    assert all(checks.values())
    assert all(certificate["chart_identity_certificate"]["checks"].values())
    assert checks["integral_tau_identity_is_exact"] is True
    assert checks["infinity_source_equation_is_exact"] is True
    assert checks["infinity_tau_identity_is_exact"] is True
    assert certificate["integral_source_certificate"]["source_rows_mod_17"] == [
        (0, 5),
        (0, 12),
        (1, 3),
        (1, 14),
        (4, 6),
        (4, 11),
        (5, 6),
        (5, 11),
        (8, 3),
        (8, 14),
        (9, 5),
        (9, 12),
        (11, 1),
        (11, 16),
        (15, 1),
        (15, 16),
    ]
    assert certificate["infinity_source_certificate"]["source_rows_mod_17"] == [
        (0, 1),
        (0, 16),
        (1, 8),
        (1, 9),
        (3, 7),
        (3, 10),
        (5, 4),
        (5, 13),
        (7, 4),
        (7, 13),
        (9, 7),
        (9, 10),
        (11, 8),
        (11, 9),
        (12, 1),
        (12, 16),
    ]
    assert certificate["denominator_pole_certificate"]["Q17_pole_branches"] == []
    assert certificate["factor_and_zero_certificate"]["factor_zero_source_points"] == []


def test_wl592_retains_fixed_cover_and_exact_aa_bb_lift() -> None:
    payload = build_wl592_mixed_p17_factor_twist_local_image()
    maps = payload["proof_certificate"]["frozen_maps_certificate"]

    assert all(maps["checks"].values())
    assert maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
    assert "source leg L=3, opposite leg=7" in maps["exact_aa_bb_lift"]
    assert "(N^2+9)*(M^2+9)=(Z/4)^2" in maps["exact_aa_bb_lift"]
    assert "-10<t<10 is retained as global positivity" in maps["exact_aa_bb_lift"]
    assert payload["proof_boundary"]["rational_point_classification"] is False
    assert payload["proof_boundary"]["advance_to_D2"] is False


def test_wl592_adapter_matches_default_rejects_invalid_d0_and_does_not_rebuild(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mixed_payload = wl592.mixed.build_wl589_mixed_d0_relative_2_descent()
    assert build_wl592_from_mixed_d0(mixed_payload) == (
        build_wl592_mixed_p17_factor_twist_local_image()
    )

    invalid = deepcopy(mixed_payload)
    invalid["verification"] = dict(invalid["verification"])
    invalid["verification"]["checks"] = dict(invalid["verification"]["checks"])
    first_check = next(iter(invalid["verification"]["checks"]))
    invalid["verification"]["checks"][first_check] = False
    with pytest.raises(ValueError):
        build_wl592_from_mixed_d0(invalid)
    invalid = deepcopy(mixed_payload)
    invalid["source_cover"] = {"bogus": True}
    with pytest.raises(ValueError):
        build_wl592_from_mixed_d0(invalid)
    with pytest.raises(ValueError):
        build_wl592_from_mixed_d0({"ready": True})

    calls = 0

    def counted_mixed() -> dict[str, object]:
        nonlocal calls
        calls += 1
        return mixed_payload

    monkeypatch.setattr(wl592.mixed, "build_wl589_mixed_d0_relative_2_descent", counted_mixed)
    build_wl592_from_mixed_d0(mixed_payload)
    assert calls == 0
