from __future__ import annotations

import importlib
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl563_m2_pure_v_ell_global_product_squareclass_split()


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
    if value > 1:
        kernel *= value
    return kernel


def test_wl563_coprime_product_has_complementary_squarefree_split() -> None:
    for first in range(1, 80):
        for second in range(1, 80):
            if math.gcd(first, second) != 1:
                continue
            alpha = _squarefree_kernel(first)
            beta = _squarefree_kernel(second)
            kappa = _squarefree_kernel(first * second)
            assert math.gcd(alpha, beta) == 1
            assert alpha * beta == kappa
            assert math.isqrt(first // alpha) ** 2 == first // alpha
            assert math.isqrt(second // beta) ** 2 == second // beta


def test_wl563_coordinate_and_cone_substitution_identities() -> None:
    ell, r, g, alpha, beta, m, n = sp.symbols("ell r g alpha beta m n")
    a = g * alpha * m**2
    b = g * beta * n**2
    f_coordinate = r * (a**2 - b**2)
    assert sp.expand(
        f_coordinate - r * g**2 * (alpha**2 * m**4 - beta**2 * n**4)
    ) == 0
    cone = ell * (a**2 - b**2) + 2 * (ell - 1) * a * b
    reduced = (
        ell * (alpha**2 * m**4 - beta**2 * n**4)
        + 2 * (ell - 1) * alpha * beta * m**2 * n**2
    )
    assert sp.expand(cone - g**2 * reduced) == 0


def test_wl563_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["coprime_squareclass_split_proved_here"] is True
    assert audit["proof_status"]["complementary_divisor_split_systems_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl563_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl562_ready", lambda _: False)
    audit = module.build_wl563_m2_pure_v_ell_global_product_squareclass_split()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl563_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl563.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "coprime_squareclass_split_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
