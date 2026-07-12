from __future__ import annotations

import importlib
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
            "audit_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence()


def test_wl582_rational_locus_descent_equivalence() -> None:
    payload = _audit()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl582"
    assert payload["input_checkpoint"] == {"work_log": "wl581", "ready": True}
    assert all(payload["symbolic_certificate"].values())

    proof = payload["proof_status"]
    assert proof["rational_genus_two_lift_reconstructed_here"] is True
    assert proof["nonbranch_forward_and_inverse_bijection_proved_here"] is True
    assert proof["quadratic_lift_obstruction_shown_automatic_here"] is True
    assert proof["wl581_unrestricted_elliptic_route_exhausted_here"] is True
    assert proof["uniform_full_wl535_obstruction_proved_here"] is False
    assert proof["advance_to_m3"] is False

    descent = payload["descent_certificate"]
    assert descent["inverse"] == ["X=-2*A/B", "Z=A*X"]
    assert descent["automatic_square"] == "S^2+16=(X+4/X)^2"
    assert payload["rational_wl535_point_produced_here"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False


def test_wl582_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl581_ready", lambda _: False)
    payload = module.build_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence()
    assert payload["status"] == "issues"
    assert payload["proof_status"] == {}


def test_wl582_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl582.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "work_log=wl582" in result.stdout
    assert out.exists()
