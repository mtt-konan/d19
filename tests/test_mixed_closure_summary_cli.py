from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_mixed_closure_summary_cli_reports_rank_certificates_and_uncertain_rows(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "mixed.jsonl"
    out_path = tmp_path / "summary.json"
    _write_jsonl(
        input_path,
        [
            {
                "A": 9,
                "B": 35,
                "curve": "AA",
                "status": "ok",
                "rank_lower": 0,
                "rank_upper": 0,
                "rank0_torsion_certificate": {
                    "status": "certified",
                    "affine_preimage_count": 2,
                    "certifies_no_full_closed_square": True,
                    "all_affine_preimages_are_midpoints": True,
                },
            },
            {
                "A": 9,
                "B": 35,
                "curve": "BB",
                "status": "ok",
                "rank_lower": 0,
                "rank_upper": 2,
                "model": [0, 1, 0, -2, -3],
                "root_number": 1,
                "sha2_lower": 0,
                "torsion_order": 4,
            },
            {
                "A": 9,
                "B": 35,
                "curve": "AB",
                "status": "ok",
                "rank_lower": 1,
                "rank_upper": 1,
            },
            {
                "A": 9,
                "B": 35,
                "curve": "BA",
                "status": "pari-error",
            },
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/summarize_mixed_closure_results.py",
            "--input",
            str(input_path),
            "--out",
            str(out_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    summary = json.loads(out_path.read_text(encoding="utf-8"))
    assert summary["rows"] == 4
    assert summary["status_counts"] == {"ok": 3, "pari-error": 1}
    assert summary["rank_counts"] == {"0/0": 1, "0/2": 1, "1/1": 1}
    assert summary["rank_counts_by_curve"]["AA"] == {"0/0": 1}
    assert summary["rank_counts_by_curve"]["BB"] == {"0/2": 1}
    assert summary["rank0_torsion_certificates"] == 1
    assert summary["certified_no_full_closed_square"] == 1
    assert summary["certified_all_midpoint"] == 1
    assert summary["affine_preimage_counts"] == {"2": 1}
    assert summary["strict_excluded_pair_count"] == 1
    assert summary["strict_excluded_pairs"] == [
        {"A": 9, "B": 35, "certifying_curves": ["AA"]}
    ]
    assert summary["uncertain_rank_rows"] == [
        {
            "A": 9,
            "B": 35,
            "curve": "BB",
            "rank": "0/2",
            "model": [0, 1, 0, -2, -3],
            "root_number": 1,
            "sha2_lower": 0,
            "torsion_order": 4,
        }
    ]
    assert "wrote summary" in result.stdout
