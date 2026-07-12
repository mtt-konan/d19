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
            "audit_closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent()


def test_wl544_symbolic_equivalence_certificate() -> None:
    symbolic = _audit()["symbolic_certificate"]
    assert symbolic["automatic_conic_identity_verified"] is True
    assert symbolic["G_homogenization_verified"] is True
    assert symbolic["reconstruction_G_square"] == "V=W/N^4 from W^2=J_ell(F,N)"


def test_wl544_records_explicit_at_most_two_branch_system() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["explicit_system"] == {
        "unit_class_count_upper_bound": 2,
        "nonzero_condition": "N!=0",
        "Gaussian_square": "Z^2=ell*N^2-F^2",
        "G_square": "W^2=J_ell(F,N)",
        "positivity": "ell*F^4+4*F^2*N^2-4*ell*N^4>0",
        "reconstruction": ["q=F/N", "a=Z/N", "c=H/N", "V=W/N^4"],
    }


def test_wl544_trivial_unit_branch_formula() -> None:
    branch = _audit()["trivial_unit_branch"]
    assert branch == {
        "r": 2,
        "s": 0,
        "F": "4*u*v",
        "H": "2*(u^2+ell*v^2)",
        "N": "u^2-ell*v^2",
        "Gaussian_quartic": "Z^2=ell*(u^2-ell*v^2)^2-16*u^2*v^2",
    }


def test_wl544_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["proof_status"] == {
        "abstract_unit_square_descent_expanded_here": True,
        "at_most_two_explicit_integer_quartic_branches_here": True,
        "Gaussian_G_and_positivity_pulled_back_exactly_here": True,
        "forward_and_converse_reconstruction_proved_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    assert audit["rational_wl535_point_produced_here"] is False


def test_wl544_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl543_ready", lambda _: False)
    audit = module.build_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl544_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl544.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "forward_and_converse_reconstruction_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
