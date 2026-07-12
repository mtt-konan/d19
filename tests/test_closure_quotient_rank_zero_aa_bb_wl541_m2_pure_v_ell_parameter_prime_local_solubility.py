from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl541_m2_pure_v_ell_parameter_prime_local_solubility"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl541_m2_pure_v_ell_parameter_prime_local_solubility()


def test_wl541_geometry_bound_is_strict() -> None:
    audit = _audit()
    geometry = audit["finite_field_curve"]["geometry_certificate"]
    assert geometry["degree"] == 8
    assert geometry["genus"] == 3
    assert geometry["discriminant_is_power_of_two"] is True
    assert geometry["rational_points_at_infinity"] == 2
    assert geometry["maximum_removed_points"] == 12
    assert geometry["first_claimed_prime_threshold"] == 61
    assert geometry["hasse_weil_lower_bound_at_61"] > 12


def test_wl541_small_prime_witnesses_are_complete() -> None:
    audit = _audit()
    rows = audit["finite_field_curve"]["small_prime_witnesses"]
    assert [row["ell"] for row in rows] == [5, 13, 17, 29, 37, 41, 53]
    assert all(row["x_nonzero"] for row in rows)
    assert all(row["y_nonzero"] for row in rows)
    assert all(row["curve_equation_verified"] for row in rows)


def test_wl541_records_local_failure_proposition_only() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "unit_finite_field_point_exists_for_every_ell_eq_1_mod_4_here": True,
        "simultaneous_parameter_prime_hensel_lift_proved_here": True,
        "parameter_prime_standalone_local_obstruction_exhausted_here": True,
        "rational_wl535_point_produced_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["hensel_lift"]["simultaneous_lift_for_same_q"] is True
    assert audit["hensel_lift"]["real_positivity_addressed"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_wl541_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl540_ready", lambda _: False)
    audit = module.build_wl541_m2_pure_v_ell_parameter_prime_local_solubility()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl541_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl541.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl541_m2_pure_v_ell_parameter_prime_local_solubility.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "parameter_prime_standalone_local_obstruction_exhausted_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
