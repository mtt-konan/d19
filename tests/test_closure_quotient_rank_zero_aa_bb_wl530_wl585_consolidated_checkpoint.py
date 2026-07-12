from __future__ import annotations

import importlib
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
            "audit_closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl530_wl585_consolidated_checkpoint()


def test_consolidated_checkpoint_rechecks_algebra_and_exhausts_route() -> None:
    payload = _audit()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["checkpoint"] == "wl530-wl585"
    assert payload["input_checkpoints"] == {"wl530": True, "wl585": True}
    assert all(payload["independent_symbolic_review"].values())

    review = payload["review_status"]
    assert review["key_algebra_independently_rechecked"] is True
    assert review["forward_converse_and_exceptions_reviewed"] is True
    assert review["correctness_defect_found"] is False
    assert review["wl535_proved"] is False
    assert review["strict_counterexample_found"] is False
    assert review["strictly_smaller_arithmetic_proposition_found"] is False
    assert review["wl585_uniform_arithmetic_tool_available"] is False
    assert review["elliptic_quotient_route_exhausted"] is True
    assert review["m2_closed"] is False
    assert review["advance_to_m3"] is False
    assert review["allow_equivalent_model_as_future_progress"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["rank_zero_claimed"] is False
    assert payload["sha2_trivial_claimed"] is False
    assert payload["advance_to_m3"] is False


def test_consolidated_checkpoint_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl585_ready", lambda _: False)
    payload = module.build_wl530_wl585_consolidated_checkpoint()
    assert payload["status"] == "issues"
    assert payload["review_status"] == {}


def test_consolidated_checkpoint_cli_strict(tmp_path: Path) -> None:
    out = tmp_path / "consolidated.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "checkpoint=wl530-wl585" in result.stdout
    assert out.exists()
