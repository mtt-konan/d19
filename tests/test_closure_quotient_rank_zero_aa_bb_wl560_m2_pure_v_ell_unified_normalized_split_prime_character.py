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
            "audit_closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl560_m2_pure_v_ell_unified_normalized_split_prime_character()


def test_wl560_squarefree_membership_and_gamma_exponent_for_all_d() -> None:
    for d in range(12):
        epsilon = d % 2
        gamma_exponent = (d - epsilon) // 2
        assert d == epsilon + 2 * gamma_exponent
        assert epsilon in {0, 1}


def test_wl560_normalization_removes_exact_common_power() -> None:
    for prime in (3, 5, 7, 13):
        for d in range(8):
            epsilon = d % 2
            r = prime**epsilon * 11
            gamma = prime ** ((d - epsilon) // 2) * 7
            z_scale = r * gamma * gamma
            normalized = z_scale // (prime**d)
            assert normalized == 11 * 7 * 7


def test_wl560_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["odd_common_leading_character_supplied_here"] is True
    assert audit["proof_status"]["assembled_global_character_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl560_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl559_ready", lambda _: False)
    audit = module.build_wl560_m2_pure_v_ell_unified_normalized_split_prime_character()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl560_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl560.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "odd_common_leading_character_supplied_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
