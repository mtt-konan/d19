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
            "audit_closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata()


def _v2(value: int) -> int:
    if value == 0:
        return 100
    result = 0
    while value % 2 == 0:
        result += 1
        value //= 2
    return result


def test_wl557_exact_unequal_valuation_formula_and_equal_lower_bound() -> None:
    for a_0 in range(1, 16, 2):
        for b_0 in range(4, 65, 4):
            c = _v2(b_0)
            for x in range(1, 32):
                for y in range(1, 32):
                    if (x - y) % 2 == 0:
                        continue
                    k = _v2(x * y)
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    value = _v2(b_pi)
                    if c < k + 1:
                        assert value == c
                    elif c > k + 1:
                        assert value == k + 1
                    else:
                        assert value >= c + 1


def test_wl557_minimum_three_condition_is_exact() -> None:
    for c in range(2, 8):
        for k in range(1, 8):
            can_reach_three = min(c, k + 1) >= 3 or c == k + 1 == 2
            stated = (c == 2 and k == 1) or (c >= 3 and k >= 2)
            assert can_reach_three == stated


def test_wl557_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["real_and_Gaussian_descent_valuations_coupled_here"] is True
    assert audit["proof_status"]["surviving_valuation_strata_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl557_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl556_ready", lambda _: False)
    audit = module.build_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl557_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl557.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "surviving_orientations_stratified_2_adically_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
