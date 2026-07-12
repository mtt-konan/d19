from __future__ import annotations

import importlib
import json
import math
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
            "audit_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch()


@pytest.mark.parametrize("ell", [5, 13, 17, 29, 37, 101])
def test_wl569_endpoint_bounds_and_cone_root(ell: int) -> None:
    rho = (math.sqrt((ell - 1) ** 2 + ell**2) - (ell - 1)) / ell
    assert math.sqrt(2) - 1 < rho < 0.5
    assert abs(ell * (rho * rho - 1) + 2 * (ell - 1) * rho) < 1e-12
    assert ell * (0.5 * 0.5 - 1) + 2 * (ell - 1) * 0.5 > 0


@pytest.mark.parametrize("ell", [5, 13, 17, 29])
def test_wl569_F_is_negative_through_candidate_interval(ell: int) -> None:
    for numerator in range(1, 100):
        x = ell * numerator / 100
        f = x * x + (8 - 4 * ell) * x - 4
        assert f < 0


def test_wl569_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["F_strictly_negative_on_candidate_range_here"] is True
    assert proof["positive_ordered_norm_ratio_branch_unique_here"] is True
    assert proof["strict_cone_ratio_interval_proved_here"] is True
    assert proof["selected_orientation_norm_intersection_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl569_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl568_ready", lambda _: False)
    audit = module.build_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl569_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl569.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "positive_ordered_norm_ratio_branch_unique_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
