from __future__ import annotations

import importlib
import itertools
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
            "audit_closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation()


def _bit(value: int) -> int:
    assert value in {-1, 1}
    return (1 - value) // 2


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def test_wl567_branch_formulas_equal_affine_rows() -> None:
    primes = [5, 13, 17]
    alpha_fixed = 2
    beta_fixed = 3
    for assignment in itertools.product((0, 1), repeat=len(primes)):
        for row_index, q in enumerate(primes):
            a_q = _bit(_legendre(alpha_fixed, q))
            b_q = _bit(_legendre(beta_fixed, q))
            d_q = ((q - 1) // 4) % 2
            off_diagonal = {
                index: _bit(_legendre(t, q))
                for index, t in enumerate(primes)
                if index != row_index
            }
            common = sum(
                coefficient * assignment[index]
                for index, coefficient in off_diagonal.items()
            ) % 2
            if assignment[row_index] == 0:
                z_q = (a_q + common) % 2
            else:
                z_q = (
                    d_q
                    + b_q
                    + sum(
                        coefficient * (1 - assignment[index])
                        for index, coefficient in off_diagonal.items()
                    )
                ) % 2
            delta_q = (
                d_q + a_q + b_q + sum(off_diagonal.values())
            ) % 2
            left = (delta_q * assignment[row_index] + common) % 2
            assert left == (z_q + a_q) % 2


def test_wl567_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["quartic_allocation_linearized_over_F2_here"] is True
    assert audit["proof_status"]["affine_system_coupled_to_integer_equations_here"] is False
    assert audit["theorem_level_selmer_matrix_claimed"] is False
    assert audit["advance_to_m3"] is False


def test_wl567_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl566_ready", lambda _: False)
    audit = module.build_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl567_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl567.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "quartic_allocation_linearized_over_F2_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
