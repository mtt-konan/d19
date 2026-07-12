from __future__ import annotations

import importlib
import json
import math
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
            "audit_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling()


def test_wl573_integral_parameter_implies_support_constraints() -> None:
    for a in range(1, 16):
        for b in range(1, 12):
            if math.gcd(a, b) != 1:
                continue
            for m in range(1, 12):
                for n in range(m + 1, 16):
                    if math.gcd(m, n) != 1:
                        continue
                    delta = m * m + 2 * m * n - n * n
                    if delta <= 0:
                        continue
                    x = Fraction(a * a, b * b)
                    tau = Fraction(m, n)
                    d = tau * tau + 2 * tau - 1
                    ell = (
                        tau * x * x
                        + 2 * x * tau * tau
                        + 8 * x * tau
                        - 2 * x
                        - 4 * tau
                    ) / (2 * x * d)
                    if ell.denominator != 1:
                        continue
                    k = a**4 + 4 * a * a * b * b - 4 * b**4
                    assert (4 * m * n) % (a * a) == 0
                    assert (m * n) % (b * b) == 0
                    assert math.gcd(delta, m * n) == 1
                    assert k % delta == 0


def test_wl573_delta_dyadic_boundary() -> None:
    for m in range(1, 30):
        for n in range(1, 30):
            if math.gcd(m, n) != 1:
                continue
            delta = m * m + 2 * m * n - n * n
            if (m - n) % 2:
                assert delta % 2 == 1
            else:
                assert delta % 4 == 2


def test_wl573_preserves_claim_boundary() -> None:
    audit = _audit()
    proof = audit["proof_status"]
    assert audit["status"] == "ok"
    assert proof["q_numerator_square_supports_on_four_mn_here"] is True
    assert proof["q_denominator_square_supports_on_mn_here"] is True
    assert proof["Delta_divides_positive_quartic_form_here"] is True
    assert proof["generic_genus_five_cover_solved_here"] is False
    assert audit["advance_to_m3"] is False


def test_wl573_fails_closed(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl572_ready", lambda _: False)
    audit = module.build_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling()
    assert audit["status"] == "issues"
    assert audit["proof_status"] == {}


def test_wl573_cli_strict_certificate(tmp_path: Path) -> None:
    out = tmp_path / "wl573.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "Delta_divides_positive_quartic_form_here=True" in result.stdout
    assert payload["advance_to_m3"] is False
