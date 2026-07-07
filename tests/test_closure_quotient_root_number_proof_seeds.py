from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_closure_quotient_root_number_proof_seeds import (
    BOUNDARY,
    summarize_root_number_proof_seeds,
    write_json,
)


def _triage() -> dict[str, object]:
    return {
        "targets": [
            {
                "class": "3:5",
                "observed_pairs": [[3, 5]],
                "root_number_pattern": "AA:-1|AB:1|BA:1|BB:-1",
                "rank_key_pattern": "AA:1/1|AB:2/2|BA:2/2|BB:1/1",
                "family_exclusion_proved": False,
            },
            {
                "class": "7:11",
                "observed_pairs": [[7, 11], [14, 22]],
                "root_number_pattern": "AA:-1|AB:1|BA:1|BB:-1",
                "rank_key_pattern": "AA:1/1|AB:2/2|BA:2/2|BB:1/1",
                "family_exclusion_proved": False,
            },
            {
                "class": "13:17",
                "observed_pairs": [[13, 17]],
                "root_number_pattern": "AA:1|AB:-1|BA:-1|BB:-1",
                "rank_key_pattern": "AA:2/2|AB:3/3|BA:3/3|BB:1/1",
                "family_exclusion_proved": False,
            },
        ]
    }


def test_root_number_proof_seeds_group_by_combined_root_and_rank_pattern() -> None:
    summary = summarize_root_number_proof_seeds(_triage())

    assert summary == {
        "status": "ok",
        "ready": True,
        "seed_group_count": 2,
        "target_class_count": 3,
        "target_pair_count": 4,
        "family_exclusion_proved_count": 0,
        "groups": [
            {
                "root_number_pattern": "AA:-1|AB:1|BA:1|BB:-1",
                "rank_key_pattern": "AA:1/1|AB:2/2|BA:2/2|BB:1/1",
                "combined_pattern": (
                    "root[AA:-1|AB:1|BA:1|BB:-1] "
                    "rank[AA:1/1|AB:2/2|BA:2/2|BB:1/1]"
                ),
                "target_class_count": 2,
                "target_pair_count": 3,
                "classes": ["3:5", "7:11"],
                "family_exclusion_proved": False,
                "next_action": (
                    "Study this combined root-number/rank pattern as a lambda "
                    "family routing problem; it is not a no-point proof."
                ),
            },
            {
                "root_number_pattern": "AA:1|AB:-1|BA:-1|BB:-1",
                "rank_key_pattern": "AA:2/2|AB:3/3|BA:3/3|BB:1/1",
                "combined_pattern": (
                    "root[AA:1|AB:-1|BA:-1|BB:-1] "
                    "rank[AA:2/2|AB:3/3|BA:3/3|BB:1/1]"
                ),
                "target_class_count": 1,
                "target_pair_count": 1,
                "classes": ["13:17"],
                "family_exclusion_proved": False,
                "next_action": (
                    "Study this combined root-number/rank pattern as a lambda "
                    "family routing problem; it is not a no-point proof."
                ),
            },
        ],
        "boundary": BOUNDARY,
    }


def test_root_number_proof_seeds_cli_writes_summary(tmp_path: Path) -> None:
    triage = tmp_path / "triage.json"
    out = tmp_path / "seeds.json"
    triage.write_text(json.dumps(_triage()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py",
            "--triage",
            str(triage),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "seed_group_count=2" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "family_exclusion_proved_count"
    ] == 0


def test_write_json_writes_sorted_root_number_proof_seeds(tmp_path: Path) -> None:
    out = tmp_path / "seeds.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
