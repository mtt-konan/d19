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
            "audit_closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone()


def test_wl553_positivity_identity_and_substitutions() -> None:
    ell, q, d, r, m, n = sp.symbols("ell q d r m n")
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    e = 4 * (ell - 1) * q**2 * d**2
    f = r_form - e
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    assert sp.expand(h - ((ell - 1) * e + ell * f)) == 0
    cone = ell * (m**2 - n**2) - 2 * (ell - 1) * m * n
    branch_5 = sp.expand((ell - 1) * (-2 * r * m * n) + ell * r * (m**2 - n**2))
    assert sp.expand(branch_5 - r * cone) == 0
    branch_1 = sp.expand((ell - 1) * (8 * r * m * n) - 4 * ell * r * (m**2 - n**2))
    assert sp.expand(branch_1 + 4 * r * cone) == 0


def test_wl553_uniform_cone_witnesses() -> None:
    for ell in range(5, 300, 8):
        cone = ell * (5 * 5 - 8 * 8) - 2 * (ell - 1) * 5 * (-8)
        assert cone == 41 * ell - 80
        assert cone > 0
    for ell in range(1, 300, 8):
        if ell < 5:
            continue
        for k in range(1, 12):
            n = 2**k
            cone = ell * (1 - n * n) - 2 * (ell - 1) * n
            assert cone < 0


def test_wl553_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["positivity_transferred_to_class_coordinates_here"] is True
    assert audit["proof_status"]["simultaneous_orientation_class_cone_system_solved_here"] is False
    assert audit["full_coordinate_solution_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl553_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl552_ready", lambda _: False)
    audit = module.build_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl553_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl553.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "positivity_transferred_to_class_coordinates_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
