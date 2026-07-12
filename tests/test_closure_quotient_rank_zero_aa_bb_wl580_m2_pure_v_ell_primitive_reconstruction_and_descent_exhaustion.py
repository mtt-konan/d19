from __future__ import annotations

import importlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion()


def test_wl580_tau_reconstruction_from_X_z() -> None:
    for x in (Fraction(3, 2), Fraction(2), Fraction(7, 3)):
        for tau in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            first = x * (tau + 2) - 2
            second = 2 * tau - x * (2 * tau - 1)
            if first == 0:
                continue
            z = second / first
            denominator = x * (z + 2) - 2
            if z <= 0:
                continue
            assert denominator > 0
            recovered = (x + 2 * z * (1 - x)) / denominator
            assert recovered == tau


def test_wl580_squareclass_reconstruction_identity() -> None:
    first = Fraction(7, 3)
    z = Fraction(5, 2)
    second = first * z
    assert first * second == first * first * z


def test_wl580_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["tau_uniquely_reconstructed_from_X_z_here"] is True
    assert proof["allocation_descent_exhausted_here"] is True
    assert proof["self_consistent_genus_one_family_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl580_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl579_ready", lambda _: False)
    audit = module.build_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl580_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl580.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "allocation_descent_exhausted_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
