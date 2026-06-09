from __future__ import annotations

import inspect
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _assert_sum_only_boundary(text: str) -> None:
    lowered = text.lower()
    assert "sum-only" in lowered
    assert "inside-square" in lowered
    assert "full-plane" in lowered


def test_dual_closure_sieve_docstring_marks_sum_only_boundary() -> None:
    import rational_distance.concordant.dual_closure_sieve as dual_closure_sieve

    _assert_sum_only_boundary(inspect.getdoc(dual_closure_sieve) or "")


def test_sum_only_cli_entrypoints_warn_in_help() -> None:
    scripts = [
        ROOT / "scripts" / "prove_no_solution_multi_first.py",
        ROOT / "scripts" / "partner" / "full_gm_closure_scan.py",
    ]

    for script in scripts:
        proc = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        _assert_sum_only_boundary(proc.stdout)
