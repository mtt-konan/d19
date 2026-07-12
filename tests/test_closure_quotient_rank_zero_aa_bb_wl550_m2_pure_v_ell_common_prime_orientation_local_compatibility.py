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
            "audit_closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility()


def _primes_below(limit: int) -> list[int]:
    return [
        n
        for n in range(3, limit, 2)
        if all(n % divisor for divisor in range(3, int(n**0.5) + 1, 2))
    ]


def _orientation_values(prime: int, a: int, b: int) -> tuple[set[int], set[int]]:
    first: set[int] = set()
    second: set[int] = set()
    for x in range(prime):
        for y in range(prime):
            denominator = (x * x + y * y) % prime
            if denominator == 0:
                continue
            inverse = pow(denominator, -1, prime)
            first.add((b * (x * x - y * y) + 2 * a * x * y) * inverse % prime)
            second.add((a * (x * x - y * y) - 2 * b * x * y) * inverse % prime)
    return first, second


def test_wl550_each_orientation_covers_the_norm_one_coordinate_set() -> None:
    for prime in _primes_below(80):
        target = {
            q
            for q in range(prime)
            if any((a * a + q * q) % prime == 1 for a in range(prime))
        }
        norm_one_factors = [
            (a, b)
            for a in range(prime)
            for b in range(prime)
            if (a * a + b * b) % prime == 1
        ]
        for a, b in norm_one_factors:
            first, second = _orientation_values(prime, a, b)
            assert first == target
            assert second == target


def test_wl550_every_wl549_square_root_is_orientation_compatible() -> None:
    for prime in _primes_below(120):
        roots = [
            t
            for t in range(1, prime)
            if (t * t + 4 * t - 4) % prime == 0
            and pow(t, (prime - 1) // 2, prime) == 1
        ]
        if not roots:
            continue
        a, b = next(
            (a, b)
            for a in range(prime)
            for b in range(prime)
            if (a * a + b * b) % prime == 1
        )
        first, second = _orientation_values(prime, a, b)
        for t in roots:
            q = next(q for q in range(1, prime) if q * q % prime == t)
            assert q in first
            assert q in second


def test_wl550_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["both_wl546_orientations_locally_compatible_here"] is True
    assert audit["proof_status"]["global_odd_class_equation_solved_here"] is False
    assert audit["global_integer_candidate_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl550_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl549_ready", lambda _: False)
    audit = module.build_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl550_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl550.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "both_wl546_orientations_locally_compatible_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
