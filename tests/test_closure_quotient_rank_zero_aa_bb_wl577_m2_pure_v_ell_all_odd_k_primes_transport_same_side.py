from __future__ import annotations

import importlib
import json
import math
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
            "audit_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side()


def test_wl577_factor_two_membership_from_primitive_parity() -> None:
    for m in range(1, 40):
        for n in range(1, 40):
            if math.gcd(m, n) != 1:
                continue
            delta = m * m + 2 * m * n - n * n
            exponent = 0
            value = 2 * abs(delta)
            while value and value % 2 == 0:
                exponent += 1
                value //= 2
            in_squarefree_kernel = exponent % 2 == 1
            assert in_squarefree_kernel == ((m - n) % 2 != 0)


def test_wl577_norm_identity_eliminates_singular_case_mod_odd_prime() -> None:
    for a in range(1, 20):
        for b in range(1, 20):
            if math.gcd(a, b) != 1:
                continue
            p_form = a**4 + 4 * b**4
            k_form = a**4 + 4 * a * a * b * b - 4 * b**4
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            for prime in (3, 5, 7, 11, 13, 17, 19):
                if k_form % prime != 0:
                    continue
                assert p_form % prime != 0
                assert r1 % prime != 0
                assert r2 % prime != 0


def test_wl577_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["odd_singular_determinant_cases_eliminated_here"] is True
    assert proof["two_allocations_have_identical_odd_parts_here"] is True
    assert proof["factor_two_is_only_remaining_transport_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl577_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl576_ready", lambda _: False)
    audit = module.build_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl577_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl577.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "two_allocations_have_identical_odd_parts_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
