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
            "audit_closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification()


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def _primes_below(limit: int) -> list[int]:
    return [
        n
        for n in range(3, limit, 2)
        if all(n % divisor for divisor in range(3, int(n**0.5) + 1, 2))
    ]


def test_wl549_root_identities_are_exact() -> None:
    for prime in _primes_below(400):
        for t in range(1, prime):
            if (t * t + 4 * t - 4) % prime == 0:
                assert (1 - t - t * t * pow(4, -1, prime)) % prime == 0
                assert (t + 4 - 4 * pow(t, -1, prime)) % prime == 0


def test_wl549_mod_8_root_square_classification() -> None:
    for prime in _primes_below(400):
        roots = [t for t in range(1, prime) if (t * t + 4 * t - 4) % prime == 0]
        square_roots = [t for t in roots if _is_square(t, prime)]
        if prime % 8 == 7:
            assert len(roots) == 2
            assert len(square_roots) == 1
        elif prime % 8 == 1:
            assert len(roots) == 2
            assert len(square_roots) in {0, 2}
        else:
            assert roots == []


def test_wl549_square_root_makes_source_residues_square() -> None:
    for prime in _primes_below(400):
        for t in range(1, prime):
            if (t * t + 4 * t - 4) % prime == 0 and _is_square(t, prime):
                assert _is_square(1 - t, prime)
                assert _is_square(t + 4, prime)


def test_wl549_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["root_square_condition_classified_here"] is True
    assert audit["proof_status"]["odd_Gaussian_class_equations_solved_here"] is False
    assert audit["proof_status"]["uniform_full_wl535_obstruction_proved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl549_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl548_ready", lambda _: False)
    audit = module.build_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl549_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl549.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "root_square_condition_classified_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
