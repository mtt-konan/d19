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
            "audit_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return (
        _module().build_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection()
    )


def test_wl584_prime_coupled_source_and_norm_intersection() -> None:
    payload = _audit()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl584"
    assert payload["input_checkpoint"] == {"work_log": "wl583", "ready": True}
    assert all(payload["symbolic_certificate"].values())

    proof = payload["proof_status"]
    assert proof["prime_coupled_torsor_source_identities_proved_here"] is True
    assert proof["fixed_ell_source_curve_genus_one_proved_here"] is True
    assert proof["square_x_source_cover_genus_one_proved_here"] is True
    assert proof["final_norm_discriminant_equivalence_proved_here"] is True
    assert proof["unrestricted_source_elliptic_route_exhausted_here"] is True
    assert proof["final_norm_intersection_solved_here"] is False
    assert proof["uniform_full_wl535_obstruction_proved_here"] is False
    assert proof["advance_to_m3"] is False

    intersection = payload["intersection_certificate"]
    assert intersection["source_curve_genus"] == 1
    assert intersection["square_x_source_cover_genus"] == 1
    assert intersection["norm_discriminant"] == "4*G_ell(X)"
    assert payload["rational_wl535_point_produced_here"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False


def test_wl584_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl583_ready", lambda _: False)
    payload = (
        module.build_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection()
    )
    assert payload["status"] == "issues"
    assert payload["proof_status"] == {}


def test_wl584_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl584.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "work_log=wl584" in result.stdout
    assert out.exists()
