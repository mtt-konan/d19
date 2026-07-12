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
            "audit_closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation()


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def _orientation_value(kind: str, x: int, y: int, prime: int) -> int:
    denominator = (x * x + y * y) % prime
    assert denominator != 0
    numerator = 2 * x * y if kind == "B" else x * x - y * y
    return numerator * pow(denominator, -1, prime) % prime


def test_wl562_source_squares_and_opposite_row_bits() -> None:
    prime = 13
    for t, expected_f, expected_square in ((0, 9, True), (10, 6, False)):
        assert _is_square(t, prime)
        assert _is_square(1 - t, prime)
        assert _is_square(t + 4, prime)
        f_t = (t * t + 4 * t - 4) % prime
        assert f_t == expected_f
        assert _is_square(f_t, prime) is expected_square
        assert f_t != 0


def test_wl562_both_orientations_realize_both_q_values() -> None:
    prime = 13
    witnesses = {
        ("B", 0): (0, 1),
        ("B", 6): (1, 2),
        ("R", 0): (1, 1),
        ("R", 6): (1, 4),
    }
    for (kind, q), (x, y) in witnesses.items():
        assert _orientation_value(kind, x, y, prime) == q


def test_wl562_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["local_orientation_determinacy_refuted_here"] is True
    assert audit["proof_status"]["global_integer_compatibility_resolved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl562_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl561_ready", lambda _: False)
    audit = module.build_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl562_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl562.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "local_orientation_determinacy_refuted_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
