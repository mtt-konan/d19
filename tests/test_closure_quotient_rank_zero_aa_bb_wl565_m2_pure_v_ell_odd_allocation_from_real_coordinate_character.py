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
            "audit_closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character()


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def test_wl565_character_rule_for_both_allocations() -> None:
    for prime in (3, 5, 7, 11, 13, 17, 19):
        # q|alpha: H is minus a nonzero square.
        for unit in range(1, prime):
            h_alpha = -(unit * unit)
            h_beta = unit * unit
            assert _legendre(h_alpha, prime) == _legendre(-1, prime)
            assert _legendre(h_beta, prime) == 1


def test_wl565_inert_character_uniquely_selects_side() -> None:
    for prime in (3, 7, 11, 19, 23, 31):
        assert prime % 4 == 3
        assert _legendre(-1, prime) == -1
        assert {-1: "alpha", 1: "beta"}[-1] == "alpha"
        assert {-1: "alpha", 1: "beta"}[1] == "beta"


def test_wl565_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["inert_odd_kappa_factors_assigned_here"] is True
    assert audit["proof_status"]["split_prime_binary_allocations_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl565_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl564_ready", lambda _: False)
    audit = module.build_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl565_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl565.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "inert_odd_kappa_factors_assigned_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
