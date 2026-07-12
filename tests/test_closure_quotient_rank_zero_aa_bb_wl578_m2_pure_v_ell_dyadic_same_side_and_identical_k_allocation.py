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
            "audit_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation()


def _v2(value: int) -> int:
    if value == 0:
        return 99
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def test_wl578_parity_matrix_preserves_unequal_valuation_order() -> None:
    for diagonal in (1, 3, 5, 7):
        for off_diagonal in (2, 4, 6, 10):
            determinant = diagonal * diagonal + off_diagonal * off_diagonal
            assert determinant % 2 == 1
            for first_exp in range(7):
                for second_exp in range(7):
                    if first_exp == second_exp:
                        continue
                    first = 2**first_exp
                    second = 2**second_exp
                    out_first = diagonal * first - off_diagonal * second
                    out_second = off_diagonal * first + diagonal * second
                    assert (_v2(out_first) < _v2(out_second)) == (
                        first_exp < second_exp
                    )


def test_wl578_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["factor_two_transports_same_side_here"] is True
    assert proof["two_complementary_k_allocations_identical_here"] is True
    assert proof["allocation_analysis_exhausted_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl578_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl577_ready", lambda _: False)
    audit = module.build_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl578_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl578.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "two_complementary_k_allocations_identical_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
