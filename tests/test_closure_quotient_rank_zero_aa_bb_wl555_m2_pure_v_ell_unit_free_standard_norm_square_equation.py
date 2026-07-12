from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation()


def test_wl555_standard_element_and_positivity_identities() -> None:
    ell, q, d, r, a, b = sp.symbols("ell q d r a b")
    e = 4 * (ell - 1) * q**2 * d**2
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    f = r_form - e
    assert sp.expand(f - (q**4 + (8 - 4 * ell) * q**2 * d**2 - 4 * d**4)) == 0
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    assert sp.expand(h - ((ell - 1) * e + ell * f)) == 0
    coordinate_h = sp.expand(
        (ell - 1) * (2 * r * a * b) + ell * r * (a**2 - b**2)
    )
    cone = ell * (a**2 - b**2) + 2 * (ell - 1) * a * b
    assert sp.expand(coordinate_h - r * cone) == 0


def test_wl555_delta_rotation_and_unit_cancellation() -> None:
    e, f, r, a, b = sp.symbols("e f r a b", real=True)
    z = f + sp.I * e
    delta = e + sp.I * f
    assert sp.simplify(delta - sp.I * sp.conjugate(z)) == 0
    gamma = a - sp.I * b
    substituted_delta = sp.I * r * gamma**2
    recovered_z = sp.conjugate(substituted_delta / sp.I)
    assert sp.expand_complex(recovered_z - r * (a + sp.I * b) ** 2) == 0


def test_wl555_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["Gaussian_unit_removed_uniformly_here"] is True
    assert audit["proof_status"]["standard_orientation_square_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl555_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl554_ready", lambda _: False)
    audit = module.build_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl555_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl555.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "Gaussian_unit_removed_uniformly_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
