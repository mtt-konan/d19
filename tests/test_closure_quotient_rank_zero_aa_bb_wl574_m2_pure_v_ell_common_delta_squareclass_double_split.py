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
            "audit_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl574_m2_pure_v_ell_common_delta_squareclass_double_split()


def _squarefree_kernel(value: int) -> int:
    kernel = 1
    prime = 2
    while prime * prime <= value:
        exponent = 0
        while value % prime == 0:
            exponent += 1
            value //= prime
        if exponent % 2:
            kernel *= prime
        prime += 1
    return kernel * value


def test_wl574_integer_product_squareclass_split() -> None:
    for first in range(1, 80):
        for second in range(1, 80):
            common = math.gcd(first, second)
            left = first // common
            right = second // common
            if math.gcd(left, right) != 1:
                continue
            k = _squarefree_kernel(left * right)
            alpha = _squarefree_kernel(left)
            beta = _squarefree_kernel(right)
            assert alpha * beta == k
            assert math.isqrt(left // alpha) ** 2 == left // alpha
            assert math.isqrt(right // beta) ** 2 == right // beta


def test_wl574_determinant_gcd_support() -> None:
    for a in range(1, 12):
        for b in range(1, 10):
            if math.gcd(a, b) != 1:
                continue
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            for m in range(1, 10):
                for n in range(1, 10):
                    if math.gcd(m, n) != 1:
                        continue
                    first = a * a * m + 2 * a * a * n - 2 * b * b * n
                    second = a * a * n + 2 * b * b * m - 2 * a * a * m
                    third = a * a * m + 4 * b * b * m - 2 * b * b * n
                    fourth = a * a * n + 2 * b * b * m + 4 * b * b * n
                    assert r1 % math.gcd(first, second) == 0
                    assert r2 % math.gcd(third, fourth) == 0


def test_wl574_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["both_source_pairs_share_canonical_Delta_squareclass_here"] is True
    assert proof["two_complementary_splits_of_same_k_proved_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl574_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl573_ready", lambda _: False)
    audit = module.build_wl574_m2_pure_v_ell_common_delta_squareclass_double_split()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl574_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl574.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "two_complementary_splits_of_same_k_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
