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
            "audit_closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd()


def _valuation(value: int, prime: int) -> int:
    if value == 0:
        return 100
    result = 0
    while value % prime == 0:
        result += 1
        value //= prime
    return result


def test_wl554_gaussian_square_coordinate_gcd_has_even_odd_valuations() -> None:
    for m in range(-30, 31):
        for n in range(-30, 31):
            if m == n == 0:
                continue
            common = math.gcd(m * m - n * n, 2 * m * n)
            for prime in (3, 5, 7, 11, 13, 17, 19):
                assert _valuation(common, prime) % 2 == 0


def test_wl554_candidate_gcd_reduces_to_ell_minus_one_and_r() -> None:
    for ell in (5, 13, 17, 29, 37, 41):
        for q in range(1, 15):
            for d in range(1, 15):
                if math.gcd(q, d) != 1:
                    continue
                e = 4 * (ell - 1) * q * q * d * d
                r_value = q**4 + 4 * q * q * d * d - 4 * d**4
                f = r_value - e
                common = math.gcd(e, f)
                for prime in (3, 5, 7, 11, 13, 17, 19):
                    left = _valuation(common, prime)
                    right = min(_valuation(ell - 1, prime), _valuation(r_value, prime))
                    assert left == right


def test_wl554_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["rational_class_made_candidate_canonical_here"] is True
    assert audit["proof_status"]["canonical_class_equation_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl554_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl553_ready", lambda _: False)
    audit = module.build_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl554_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl554.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "rational_class_made_candidate_canonical_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
