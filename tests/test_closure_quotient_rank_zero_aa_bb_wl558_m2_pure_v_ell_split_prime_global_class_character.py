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
            "audit_closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl558_m2_pure_v_ell_split_prime_global_class_character()


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def test_wl558_nontrivial_mod_13_source_square_example() -> None:
    prime = 13
    t = 10
    assert _is_square(t, prime)
    assert _is_square(1 - t, prime)
    assert _is_square(t + 4, prime)
    f_t = (t * t + 4 * t - 4) % prime
    assert f_t == 6
    assert not _is_square(f_t, prime)


def test_wl558_rational_units_are_squares_over_inert_quadratic_field() -> None:
    for prime in (3, 7, 11, 19, 23, 31):
        assert prime % 4 == 3
        for value in range(1, prime):
            assert pow(value, (prime * prime - 1) // 2, prime) == 1


def test_wl558_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["split_prime_character_condition_proved_here"] is True
    assert audit["proof_status"]["global_character_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl558_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl557_ready", lambda _: False)
    audit = module.build_wl558_m2_pure_v_ell_split_prime_global_class_character()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl558_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl558.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "split_prime_character_condition_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
