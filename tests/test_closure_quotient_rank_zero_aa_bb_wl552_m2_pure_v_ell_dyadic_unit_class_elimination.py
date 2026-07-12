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
            "audit_closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl552_m2_pure_v_ell_dyadic_unit_class_elimination()


def test_wl552_square_and_i_square_parity_patterns() -> None:
    for m in range(-9, 10):
        for n in range(-9, 10):
            if (m - n) % 2 == 0:
                continue
            square_real = m * m - n * n
            square_imaginary = 2 * m * n
            assert square_real % 2 == 1
            assert square_imaginary % 2 == 0
            i_square_real = -square_imaginary
            i_square_imaginary = square_real
            assert i_square_real % 2 == 0
            assert i_square_imaginary % 2 == 1


def test_wl552_branch_valuations_give_normalized_parities() -> None:
    for ell in range(5, 64, 8):
        for q in range(1, 10, 2):
            for d in range(1, 10, 2):
                e = 4 * (ell - 1) * q * q * d * d
                r_value = q**4 + 4 * q * q * d * d - 4 * d**4
                f = r_value - e
                assert e % 2 == 0
                assert f % 2 == 1
    for ell in range(1, 64, 8):
        for q in range(8, 33, 8):
            for d in range(1, 10, 2):
                e = 4 * (ell - 1) * q * q * d * d
                r_value = q**4 + 4 * q * q * d * d - 4 * d**4
                f = r_value - e
                assert (e // 4) % 2 == 0
                assert (f // 4) % 2 == 1


def test_wl552_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["Gaussian_unit_class_forced_to_i_here"] is True
    assert audit["proof_status"]["remaining_eta_i_coordinate_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl552_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl551_ready", lambda _: False)
    audit = module.build_wl552_m2_pure_v_ell_dyadic_unit_class_elimination()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl552_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl552.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "Gaussian_unit_class_forced_to_i_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
