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
            "audit_closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl566_m2_pure_v_ell_quartic_character_for_split_allocation()


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def _quartic_sign(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 4, prime)
    return -1 if residue == prime - 1 else residue


def test_wl566_alpha_and_beta_side_formulas() -> None:
    for prime in (5, 13, 17, 29, 37, 41):
        for opposite_factor in range(1, prime):
            for square_variable in range(1, prime):
                alpha_side = -(
                    opposite_factor * square_variable * square_variable
                ) ** 2
                expected_alpha = (
                    (-1) ** ((prime - 1) // 4)
                    * _legendre(opposite_factor, prime)
                )
                assert _quartic_sign(alpha_side, prime) == expected_alpha
                beta_side = (
                    opposite_factor * square_variable * square_variable
                ) ** 2
                assert _quartic_sign(beta_side, prime) == _legendre(
                    opposite_factor, prime
                )


def test_wl566_predicted_signs_can_agree_or_differ() -> None:
    seen_equal = False
    seen_different = False
    for prime in (5, 13, 17, 29, 37, 41):
        delta = (-1) ** ((prime - 1) // 4)
        for alpha_0 in range(1, prime):
            for beta_0 in range(1, prime):
                first = delta * _legendre(beta_0, prime)
                second = _legendre(alpha_0, prime)
                seen_equal |= first == second
                seen_different |= first != second
    assert seen_equal
    assert seen_different


def test_wl566_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["quartic_character_strictly_refines_split_allocation_here"] is True
    assert audit["proof_status"]["coupled_split_allocation_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl566_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl565_ready", lambda _: False)
    audit = module.build_wl566_m2_pure_v_ell_quartic_character_for_split_allocation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl566_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl566.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "quartic_character_strictly_refines_split_allocation_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
