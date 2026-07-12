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
            "audit_closure_quotient_rank_zero_aa_bb_wl539_m2_pure_v_ell_direct_residue_method_classification"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl539_m2_pure_v_ell_direct_residue_method_classification()


def test_wl539_large_prime_bound_is_strict() -> None:
    audit = _audit()
    large = audit["large_prime_argument"]
    assert large["factor_degrees"] == [1, 1, 1, 4]
    assert large["total_weil_error_coefficient"] == 41
    assert large["maximum_zero_residue_contribution"] == 7
    assert large["first_relevant_prime_with_strict_bound"] == 1907
    assert large["weighted_lower_bound_at_threshold"] > 7
    assert large["strictly_greater_than_zero_contribution_bound"] is True
    assert large["degenerate_square_cases"] == {
        1: "(R^2+4*R-4)^2",
        2: "(R^2+4)^2",
    }


def test_wl539_finite_classification_is_exact() -> None:
    audit = _audit()
    finite = audit["finite_classification"]
    assert finite["bound_exclusive"] == 1907
    assert finite["excluding_pairs"] == [(7, 5), (11, 10), (19, 15), (23, 5)]
    assert finite["rows_with_exclusions"] == [
        {"auxiliary_prime": 7, "excluding_parameter_residues": [5]},
        {"auxiliary_prime": 11, "excluding_parameter_residues": [10]},
        {"auxiliary_prime": 19, "excluding_parameter_residues": [15]},
        {"auxiliary_prime": 23, "excluding_parameter_residues": [5]},
    ]
    assert finite["matches_expected_complete_list"] is True


def test_wl539_records_method_boundary_without_overclaim() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "direct_single_prime_good_reduction_method_classified_here": True,
        "only_auxiliary_primes_7_11_19_23_exclude_residues": True,
        "new_prime_class_ell_eq_5_mod_92_excluded_here": True,
        "method_exhausted_outside_four_pairs": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["new_local_obstruction"]["prime_class_mod_92"] == 5
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["advance_to_m3"] is False


def test_wl539_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl538_ready", lambda _: False)
    audit = module.build_wl539_m2_pure_v_ell_direct_residue_method_classification()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl539_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl539.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl539_m2_pure_v_ell_direct_residue_method_classification.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "method_exhausted_outside_four_pairs=True" in result.stdout
    assert payload["advance_to_m3"] is False
