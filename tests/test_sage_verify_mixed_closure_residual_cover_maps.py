from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_verify_mixed_closure_handoff_maps import MARKER
from scripts.theory.sage_verify_mixed_closure_residual_cover_maps import (
    build_residual_map_handoffs,
    verify_residual_cover_maps,
    write_json,
)


def test_build_residual_map_handoffs_selects_no_point_covers() -> None:
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "covers": [
                {"index": 1, "quartic": "x^4+1", "covering_map_to_elliptic": "[x,y]"},
                {"index": 3, "quartic": "x^4+3", "covering_map_to_elliptic": "[x^2,x*y]"},
                {"index": 4, "quartic": "x^4+4", "covering_map_to_elliptic": "[x^3,y]"},
            ],
        }
    ]
    cover_summary = {
        "no_point_cover_rows": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "no_point_cover_indices": [3, 4],
            }
        ]
    }

    handoffs = build_residual_map_handoffs(
        cover_rows=cover_rows,
        cover_summary=cover_summary,
    )

    assert handoffs == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
            "target_cover_indices": [3, 4],
            "target_covers": [
                {
                    "index": 3,
                    "quartic": "x^4+3",
                    "covering_map_to_elliptic": "[x^2,x*y]",
                },
                {
                    "index": 4,
                    "quartic": "x^4+4",
                    "covering_map_to_elliptic": "[x^3,y]",
                },
            ],
        }
    ]


def test_verify_residual_cover_maps_summarizes_group_results(tmp_path: Path) -> None:
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "model": [0, 196194, 0, -699602500, -137257812885000],
            "covers": [
                {"index": 3, "quartic": "x^4+3", "covering_map_to_elliptic": "[x,y]"},
                {"index": 4, "quartic": "x^4+4", "covering_map_to_elliptic": "[x,y]"},
            ],
        },
        {
            "A": 575,
            "B": 4641,
            "curve": "AA",
            "model": [0, 123, 0, -456, 789],
            "covers": [
                {"index": 3, "quartic": "x^4+5", "covering_map_to_elliptic": "[x,y]"},
            ],
        },
    ]
    cover_summary = {
        "no_point_cover_rows": [
            {"A": 115, "B": 297, "curve": "AA", "no_point_cover_indices": [3, 4]},
            {"A": 575, "B": 4641, "curve": "AA", "no_point_cover_indices": [3]},
        ]
    }

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        marker_payload = {
            "all_verified": True,
            "covers": [
                {"index": 3, "map_parse_status": "ok", "identity_verified": True}
            ],
        }
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout=MARKER + json.dumps(marker_payload) + "\n",
            stderr="",
        )

    result = verify_residual_cover_maps(
        cover_rows=cover_rows,
        cover_summary=cover_summary,
        sage_executable="sage",
        timeout_seconds=30,
        dot_sage=tmp_path / "dot_sage",
        run=fake_run,
    )

    assert result == {
        "status": "ok",
        "all_verified": True,
        "group_count": 2,
        "target_cover_count": 3,
        "verified_cover_count": 2,
        "failed_cover_count": 0,
        "status_counts": {"ok": 2},
        "groups": [
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "target_cover_indices": [3, 4],
                "status": "ok",
                "all_verified": True,
                "verified_cover_count": 1,
                "failed_cover_count": 0,
            },
            {
                "A": 575,
                "B": 4641,
                "curve": "AA",
                "target_cover_indices": [3],
                "status": "ok",
                "all_verified": True,
                "verified_cover_count": 1,
                "failed_cover_count": 0,
            },
        ],
        "boundary": (
            "This verifies stored rational maps for residual no-point covers. "
            "It does not prove that any residual cover has no rational point."
        ),
    }


def test_residual_cover_map_cli_writes_audit(tmp_path: Path) -> None:
    covers = tmp_path / "covers.jsonl"
    summary = tmp_path / "summary.json"
    out = tmp_path / "out.json"
    covers.write_text(
        json.dumps(
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "model": [0, 196194, 0, -699602500, -137257812885000],
                "covers": [
                    {
                        "index": 3,
                        "quartic": "x^4+3",
                        "covering_map_to_elliptic": "[x,y]",
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    summary.write_text(
        json.dumps(
            {
                "no_point_cover_rows": [
                    {
                        "A": 115,
                        "B": 297,
                        "curve": "AA",
                        "no_point_cover_indices": [3],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py",
            "--covers",
            str(covers),
            "--cover-summary",
            str(summary),
            "--out",
            str(out),
            "--sage",
            sys.executable,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "target_cover_count=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["all_verified"] is False


def test_write_json_writes_sorted_residual_cover_map_audit(tmp_path: Path) -> None:
    out = tmp_path / "maps.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
