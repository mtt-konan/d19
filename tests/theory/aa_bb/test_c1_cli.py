from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]


def test_c1_strict_cli_is_the_only_subprocess_entrypoint(tmp_path: Path) -> None:
    out = tmp_path / "c1.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.theory.aa_bb.c1_pure_v_ell",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "stage_count=12" in result.stdout
    assert "status=ok" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert tuple(payload["stages"]) == tuple(f"wl{number}" for number in range(530, 542))
    assert all(stage["status"] == "ok" for stage in payload["stages"].values())
