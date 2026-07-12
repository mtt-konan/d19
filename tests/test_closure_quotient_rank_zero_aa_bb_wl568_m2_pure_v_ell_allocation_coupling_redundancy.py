from __future__ import annotations

import importlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl568_m2_pure_v_ell_allocation_coupling_redundancy()


def test_wl568_signed_ratio_branch_implies_norm_square() -> None:
    for a in range(1, 20):
        for b in range(1, 20):
            for e in range(1, 20):
                f = Fraction(e * (a * a - b * b), 2 * a * b)
                c = Fraction(e * (a * a + b * b), 2 * a * b)
                assert c * c == f * f + e * e


def test_wl568_norm_square_alone_does_not_choose_ordered_sign_branch() -> None:
    a, b, e = 3, 2, 5
    f = Fraction(e * (a * a - b * b), 2 * a * b)
    c = Fraction(e * (a * a + b * b), 2 * a * b)
    assert c * c == (-f) * (-f) + e * e
    assert 2 * (-f) * a * b != e * (a * a - b * b)


def test_wl568_records_exact_failure_point() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["scale_is_exact_product_coordinate_rewrite_here"] is True
    assert proof["cone_is_exact_original_positivity_rewrite_here"] is True
    assert proof["affine_rows_automatic_for_actual_factorization_here"] is True
    assert proof["allocation_route_independent_obstruction_refuted_here"] is True
    assert proof["selected_orientation_norm_intersection_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl568_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl567_ready", lambda _: False)
    audit = module.build_wl568_m2_pure_v_ell_allocation_coupling_redundancy()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl568_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl568.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "allocation_route_independent_obstruction_refuted_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
