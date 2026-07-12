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
            "audit_closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation()


def test_wl556_orientation_parities_for_opposite_parity_x_y() -> None:
    for a_0 in range(1, 16, 2):
        for b_0 in range(2, 16, 2):
            for x in range(-10, 11):
                for y in range(-10, 11):
                    if (x - y) % 2 == 0:
                        continue
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    r_pi = a_0 * (x * x - y * y) - 2 * b_0 * x * y
                    assert b_pi % 2 == 0
                    assert r_pi % 2 == 1


def test_wl556_sum_of_two_squares_even_coordinate_valuation() -> None:
    for a_0 in range(1, 100, 2):
        for b_0 in range(2, 100, 2):
            ell = a_0 * a_0 + b_0 * b_0
            if ell % 8 == 5:
                assert b_0 % 4 == 2
            elif ell % 8 == 1:
                assert b_0 % 4 == 0


def test_wl556_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["one_complete_orientation_eliminated_per_branch_here"] is True
    assert audit["proof_status"]["surviving_orientation_systems_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl556_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl555_ready", lambda _: False)
    audit = module.build_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl556_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl556.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "one_complete_orientation_eliminated_per_branch_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
