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
            "audit_closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent()


def test_wl546_symbolic_gaussian_certificate() -> None:
    symbolic = _audit()["symbolic_certificate"]
    assert symbolic["Gaussian_norm_identity_verified"] is True
    assert symbolic["conjugate_orientation_reduces_by_y_sign_and_Q_sign"] is True
    assert symbolic["essential_orientation_count"] == 2


def test_wl546_records_two_exact_orientations() -> None:
    descent = _audit()["Gaussian_descent"]
    assert descent == {
        "prime_representation": "ell=a_0^2+b_0^2",
        "factorization": "A+iQ=eta*pi_or_conjugate(pi)*(x+iy)^2",
        "norm": "x^2+y^2=D",
        "orientation_B": "Q=+/-[b_0*(x^2-y^2)+2*a_0*x*y]",
        "orientation_R": "Q=+/-[a_0*(x^2-y^2)-2*b_0*x*y]",
        "essential_orientation_count": 2,
    }


def test_wl546_preserves_remaining_obstruction() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"] == {
        "primitive_Gaussian_factors_proved_coprime_here": True,
        "Gaussian_square_reduced_to_two_orientations_here": True,
        "real_and_Gaussian_descents_coupled_here": True,
        "Gaussian_square_equation_eliminated_exactly_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert "remaining_G_square" in audit["double_descent_system"]
    assert audit["rational_wl535_point_produced_here"] is False


def test_wl546_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl545_ready", lambda _: False)
    audit = module.build_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl546_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl546.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "Gaussian_square_equation_eliminated_exactly_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
