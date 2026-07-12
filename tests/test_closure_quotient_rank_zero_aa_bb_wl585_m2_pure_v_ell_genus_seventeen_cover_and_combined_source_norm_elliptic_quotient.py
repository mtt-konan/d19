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
            "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return (
        _module().build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient()
    )


def test_wl585_genus_seventeen_and_combined_elliptic_quotient() -> None:
    payload = _audit()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl585"
    assert payload["input_checkpoint"] == {"work_log": "wl584", "ready": True}
    assert all(payload["symbolic_certificate"].values())

    proof = payload["proof_status"]
    assert proof["selected_tau_interval_equivalent_to_positivity_here"] is True
    assert proof["fixed_ell_full_cover_genus_seventeen_proved_here"] is True
    assert proof["norm_bearing_character_quotients_classified_here"] is True
    assert proof["combined_source_norm_genus_three_quotient_proved_here"] is True
    assert proof["combined_rational_elliptic_quotient_proved_here"] is True
    assert proof["restricted_combined_elliptic_image_solved_here"] is False
    assert proof["uniform_full_wl535_obstruction_proved_here"] is False
    assert proof["advance_to_m3"] is False

    cover = payload["cover_certificate"]
    assert cover["cover_degree"] == 16
    assert cover["branch_count"] == 8
    assert cover["genus"] == 17
    assert cover["norm_bearing_quotient_genera"] == {
        "genus_1": 1,
        "genus_2": 6,
        "genus_3": 1,
    }
    assert payload["rational_wl535_point_produced_here"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False


def test_wl585_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl584_ready", lambda _: False)
    payload = (
        module.build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient()
    )
    assert payload["status"] == "issues"
    assert payload["proof_status"] == {}


def test_wl585_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl585.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "work_log=wl585" in result.stdout
    assert out.exists()
