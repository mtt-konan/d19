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
            "audit_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return (
        _module().build_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product()
    )


def test_wl583_torsor_and_fiber_product_certificate() -> None:
    payload = _audit()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl583"
    assert payload["input_checkpoint"] == {"work_log": "wl582", "ready": True}
    assert all(payload["symbolic_certificate"].values())

    proof = payload["proof_status"]
    assert proof["individual_source_squares_retained_on_torsor_here"] is True
    assert proof["source_square_torsor_genus_one_proved_here"] is True
    assert proof["full_cover_fiber_product_equivalence_proved_here"] is True
    assert proof["square_x_pullback_independent_and_connected_here"] is True
    assert proof["square_x_torsor_points_solved_here"] is False
    assert proof["uniform_full_wl535_obstruction_proved_here"] is False
    assert proof["advance_to_m3"] is False

    fiber = payload["fiber_product_certificate"]
    assert fiber["generic_genera"] == {"torsor": 1, "full_cover": 5}
    assert fiber["full_cover"] == "T_tau fiber product with q^2=X"
    assert payload["rational_wl535_point_produced_here"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False


def test_wl583_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl582_ready", lambda _: False)
    payload = (
        module.build_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product()
    )
    assert payload["status"] == "issues"
    assert payload["proof_status"] == {}


def test_wl583_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl583.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "work_log=wl583" in result.stdout
    assert out.exists()
