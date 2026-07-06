from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.export_mixed_closure_residual_handoff import (
    build_handoff,
    render_magma_handoff,
    render_sage_handoff,
    write_handoff_files,
)


def _cover_row() -> dict[str, object]:
    return {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "input_rank": "0/2",
        "model": [0, 196194, 0, -699602500, -137257812885000],
        "status": "ok",
        "ellrank": {"lower": 0, "upper": 2, "sha2_lower": 0},
        "covers": [
            {
                "index": 3,
                "quartic": "41*x^4 + 1025",
                "covering_map_to_elliptic": "[map3x, map3y]",
                "point_count": 0,
                "points": [],
            },
            {
                "index": 4,
                "quartic": "-19*x^4 - 5",
                "covering_map_to_elliptic": "[map4x, map4y]",
                "point_count": 0,
                "points": [],
            },
        ],
    }


def test_build_handoff_keeps_strict_proof_boundary() -> None:
    handoff = build_handoff(
        cover_row=_cover_row(),
        bsd_row={
            "status": "ok",
            "analytic_rank": 0,
            "analytic_leading_value": "4.72955644264359",
            "bsd_factor": "0.295597277665225",
            "evidence_level": "bsd-conditional-diagnostic",
        },
        target_indices=[3, 4],
    )

    assert handoff == {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "weierstrass_model": [0, 196194, 0, -699602500, -137257812885000],
        "input_rank": "0/2",
        "ellrank": {"lower": 0, "upper": 2, "sha2_lower": 0},
        "target_cover_indices": [3, 4],
        "target_covers": [
            {
                "index": 3,
                "quartic": "41*x^4 + 1025",
                "covering_map_to_elliptic": "[map3x, map3y]",
                "point_count": 0,
                "points": [],
            },
            {
                "index": 4,
                "quartic": "-19*x^4 - 5",
                "covering_map_to_elliptic": "[map4x, map4y]",
                "point_count": 0,
                "points": [],
            },
        ],
        "local_solubility_source": "PARI ell2cover returns everywhere locally soluble 2-covers",
        "bounded_search_evidence": (
            "hyperellratpoints found no points on target covers in the input row"
        ),
        "bsd_conditional_diagnostic": {
            "status": "ok",
            "analytic_rank": 0,
            "analytic_leading_value": "4.72955644264359",
            "bsd_factor": "0.295597277665225",
            "evidence_level": "bsd-conditional-diagnostic",
        },
        "strict_proof_status": "open",
        "proof_boundary": (
            "This handoff packages evidence and external-tool inputs. It does not "
            "prove that any cover has no rational point."
        ),
        "next_strict_tasks": [
            (
                "Prove each target cover has no rational point, or replace this "
                "with a strict rank/L-value certificate."
            ),
            (
                "If using Magma or a Mordell-Weil sieve, record a reproducible "
                "transcript before promoting the result."
            ),
        ],
    }


def test_render_handoff_files_include_target_equations() -> None:
    handoff = build_handoff(
        cover_row=_cover_row(),
        bsd_row=None,
        target_indices=[3],
    )

    magma = render_magma_handoff(handoff)
    sage = render_sage_handoff(handoff)

    assert "f3 := 41*x^4 + 1025;" in magma
    assert "C3 := HyperellipticCurve(f3);" in magma
    assert "This Magma file is a handoff, not a certified transcript." in magma
    assert "f3 = 41*x**4 + 1025" in sage
    assert "C3 = HyperellipticCurve(f3, R(0))" in sage
    assert "bounded search is not a proof" in sage


def test_write_handoff_files(tmp_path: Path) -> None:
    handoff = build_handoff(
        cover_row=_cover_row(),
        bsd_row=None,
        target_indices=[3],
    )

    write_handoff_files(tmp_path, "target", handoff)

    assert json.loads((tmp_path / "target.json").read_text(encoding="utf-8"))["A"] == 115
    assert "f3 :=" in (tmp_path / "target.magma").read_text(encoding="utf-8")
    assert "f3 =" in (tmp_path / "target.sage").read_text(encoding="utf-8")


def test_handoff_cli_writes_target_files(tmp_path: Path) -> None:
    covers = tmp_path / "covers.jsonl"
    bsd = tmp_path / "bsd.jsonl"
    out_dir = tmp_path / "handoff"
    covers.write_text(json.dumps(_cover_row()) + "\n", encoding="utf-8")
    bsd.write_text(
        json.dumps({"A": 115, "B": 297, "curve": "AA", "status": "ok"}) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/export_mixed_closure_residual_handoff.py",
            "--covers",
            str(covers),
            "--bsd",
            str(bsd),
            "--target",
            "115,297,AA",
            "--cover-index",
            "3",
            "--cover-index",
            "4",
            "--out-dir",
            str(out_dir),
            "--name",
            "target",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "wrote handoff" in result.stdout
    assert (out_dir / "target.json").exists()
    assert (out_dir / "target.magma").exists()
    assert (out_dir / "target.sage").exists()
