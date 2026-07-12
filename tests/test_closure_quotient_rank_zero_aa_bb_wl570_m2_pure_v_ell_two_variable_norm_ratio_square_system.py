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
            "audit_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system()


def test_wl570_exact_rational_reconstruction_identity() -> None:
    for x in (Fraction(3, 2), Fraction(2), Fraction(7, 3)):
        for tau in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            delta = tau * tau + 2 * tau - 1
            ell = (
                tau * x * x
                + 2 * x * tau * tau
                + 8 * x * tau
                - 2 * x
                - 4 * tau
            ) / (2 * x * delta)
            f = x * x + (8 - 4 * ell) * x - 4
            e = 4 * (ell - 1) * x
            c = e * (1 + tau * tau) / (2 * tau)
            assert 2 * tau * f == e * (tau * tau - 1)
            assert c * c == f * f + e * e


def test_wl570_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["quartic_square_root_eliminated_by_unique_tau_here"] is True
    assert proof["both_source_squares_factored_in_X_tau_here"] is True
    assert proof["forward_and_converse_wl535_reconstruction_proved_here"] is True
    assert proof["two_variable_square_system_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl570_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl569_ready", lambda _: False)
    audit = module.build_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl570_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl570.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "forward_and_converse_wl535_reconstruction_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
