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
            "audit_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient()


def test_wl581_genus_two_and_elliptic_quotient_certificate() -> None:
    payload = _audit()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl581"
    assert payload["input_checkpoint"] == {"work_log": "wl580", "ready": True}
    assert all(payload["symbolic_certificate"].values())

    proof = payload["proof_status"]
    assert proof["genus_two_character_quotient_proved_here"] is True
    assert proof["quadratic_elliptic_quotient_over_q_i_proved_here"] is True
    assert proof["restricted_affine_candidate_image_proved_here"] is True
    assert proof["restricted_elliptic_image_locus_solved_here"] is False
    assert proof["uniform_full_wl535_obstruction_proved_here"] is False
    assert proof["advance_to_m3"] is False

    quotient = payload["quotient_certificate"]
    assert quotient["genus_two_branch_count"] == 6
    assert "Y nonzero" in quotient["candidate_image_restrictions"]
    assert payload["rational_wl535_point_produced_here"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False
    assert payload["stop_after_current_task"] is True


def test_wl581_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl580_ready", lambda _: False)
    payload = module.build_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient()
    assert payload["status"] == "issues"
    assert payload["proof_status"] == {}


def test_wl581_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl581.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "work_log=wl581" in result.stdout
    assert out.exists()
