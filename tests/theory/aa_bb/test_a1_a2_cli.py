from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]


def test_shared_a1_cli_smoke() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.a1_certificates",
            "--data-dir",
            "data/theory/aa_bb/wl500",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["status"] == "ok"
    assert payload["certificate_count"] == 12
    assert payload["shell_summaries"]["10"]["active_new_support_entry_count"] == 10
