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
            "audit_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs()


def test_wl575_exact_primitive_gcds() -> None:
    for a in range(1, 50):
        for b in range(1, 50):
            if math.gcd(a, b) != 1:
                continue
            p = a**4 + 4 * b**4
            k_form = a**4 + 4 * a * a * b * b - 4 * b**4
            r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
            r2 = a**4 + 8 * a * a * b * b + 20 * b**4
            expected = 1 if a % 2 else 4
            assert math.gcd(p, k_form) == expected
            assert math.gcd(r1, r2) == expected


def test_wl575_rotation_identities_on_integer_grid() -> None:
    for a, b, m, n in ((1, 1, 2, 3), (2, 1, 3, 5), (3, 2, 5, 8)):
        first = a * a * m + 2 * a * a * n - 2 * b * b * n
        second = a * a * n + 2 * b * b * m - 2 * a * a * m
        third = a * a * m + 4 * b * b * m - 2 * b * b * n
        fourth = a * a * n + 2 * b * b * m + 4 * b * b * n
        p = a**4 + 4 * b**4
        k_form = a**4 + 4 * a * a * b * b - 4 * b**4
        r1 = 5 * a**4 - 8 * a * a * b * b + 4 * b**4
        r2 = a**4 + 8 * a * a * b * b + 20 * b**4
        assert r1 * third == p * first - 2 * k_form * second
        assert r1 * fourth == 2 * k_form * first + p * second
        assert p * p + 4 * k_form * k_form == r1 * r2


def test_wl575_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["exact_scaled_Gaussian_rotation_proved_here"] is True
    assert proof["two_k_allocations_structurally_coupled_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl575_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl574_ready", lambda _: False)
    audit = module.build_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl575_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl575.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "exact_scaled_Gaussian_rotation_proved_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
