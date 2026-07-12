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
            "audit_closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl559_m2_pure_v_ell_even_common_valuation_leading_character()


def _is_square(value: int, prime: int) -> bool:
    return value % prime != 0 and pow(value % prime, (prime - 1) // 2, prime) == 1


def test_wl559_split_components_have_same_character_when_norm_is_square() -> None:
    for prime, j in ((5, 2), (13, 5), (17, 4), (29, 12), (37, 6)):
        assert j * j % prime == prime - 1
        for f_value in range(prime):
            for e_value in range(prime):
                first = (f_value + j * e_value) % prime
                second = (f_value - j * e_value) % prime
                if first == 0 or second == 0:
                    continue
                norm = first * second % prime
                if _is_square(norm, prime):
                    assert _is_square(first, prime) == _is_square(second, prime)


def test_wl559_three_leading_forms_match_master_component() -> None:
    prime = 17
    j = 4
    r = 3
    # e<k: E_d is the only nonzero leading input.
    e_d, r_d = 5, 0
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        e_d * (-1 + j) * pow(r, -1, prime)
    ) % prime
    # k<e: R_d is the only nonzero leading input.
    e_d, r_d = 0, 7
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        r_d * pow(r, -1, prime)
    ) % prime
    # e=k: write R_d=lambda*E_d.
    e_d, lambda_value = 6, 9
    r_d = lambda_value * e_d % prime
    assert (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        e_d * (lambda_value - 1 + j) * pow(r, -1, prime)
    ) % prime


def test_wl559_preserves_claim_boundary() -> None:
    audit = _audit()
    assert audit["status"] == "ok"
    assert audit["proof_status"]["all_odd_places_not_in_r_classified_here"] is True
    assert audit["proof_status"]["global_character_system_solved_here"] is False
    assert audit["rational_wl535_point_produced_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl559_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl558_ready", lambda _: False)
    audit = module.build_wl559_m2_pure_v_ell_even_common_valuation_leading_character()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl559_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl559.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "all_odd_places_not_in_r_classified_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
