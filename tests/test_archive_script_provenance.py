from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


ARCHIVE_SCRIPTS_WITH_STALE_PROOF_STATUS_DEFAULTS = [
    "batch_ell2cover_hard_cases.py",
    "batch_sha2_scan_v2.py",
    "finite_descent_hard_cases.py",
    "finite_descent_layer2.py",
    "pattern_hunt_hard_cases.py",
    "probe_chain_closure_mod_sieve.py",
]


def test_archive_scripts_warn_when_defaulting_to_stale_proof_status_db() -> None:
    for script_name in ARCHIVE_SCRIPTS_WITH_STALE_PROOF_STATUS_DEFAULTS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "archive" / script_name), "--help"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        help_text = proc.stdout.lower()

        assert "results/proof_status.db" in help_text
        assert "stale" in help_text, script_name
        assert "historical" in help_text, script_name
