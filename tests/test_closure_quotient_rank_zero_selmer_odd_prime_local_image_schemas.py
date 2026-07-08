from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas import (
    BOUNDARY,
    audit_rank_zero_selmer_odd_prime_local_image_schemas,
    write_json,
)


def _reduction_shapes() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "input_lemma_obligation_count": 2,
        "reduction_shape_count": 2,
        "reduction_shape_proved_count": 2,
        "reduction_shapes_not_local_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "reduction_entries": [
            {
                "lemma_id": "odd-prime-lemma-kernel-minus-p-divides-L",
                "kernel": "kernel_minus_p",
                "case_label": "odd-prime-divides-L",
                "prime_condition": "ell odd and ell | L",
                "mod_relation": "L == 0 mod ell",
                "reduced_a2": "-8*T^2",
                "reduced_a4": "16*T^4",
                "reduced_cubic_factorization": "x*(x - 4*T^2)^2",
                "double_root": "4*T^2",
                "simple_root": "0",
                "tangent_squareclass": "1",
                "double_root_unit": True,
                "simple_root_unit": False,
                "nodal_reduction_shape": (
                    "nodal-cubic-with-nonzero-double-root"
                ),
                "reduction_shape_proved": True,
                "local_condition_proved": False,
                "next_local_gap": (
                    "derive the required isogeny-Selmer local squareclass image "
                    "from this nodal reduction shape"
                ),
            },
            {
                "lemma_id": "odd-prime-lemma-kernel-pos-2sqrt-q-divides-T",
                "kernel": "kernel_pos_2sqrt_q",
                "case_label": "odd-prime-divides-T",
                "prime_condition": "ell odd and ell | T",
                "mod_relation": "T == 0 mod ell",
                "reduced_a2": "-64*L^2",
                "reduced_a4": "0",
                "reduced_cubic_factorization": "x^2*(x - 64*L^2)",
                "double_root": "0",
                "simple_root": "64*L^2",
                "tangent_squareclass": "-1",
                "double_root_unit": False,
                "simple_root_unit": True,
                "nodal_reduction_shape": "nodal-cubic-with-zero-double-root",
                "reduction_shape_proved": True,
                "local_condition_proved": False,
                "next_local_gap": (
                    "derive the required isogeny-Selmer local squareclass image "
                    "from this nodal reduction shape"
                ),
            },
        ],
    }


def test_rank_zero_selmer_odd_prime_local_image_schemas_group_tangent_squareclasses() -> None:
    audit = audit_rank_zero_selmer_odd_prime_local_image_schemas(
        odd_prime_reduction_shapes=_reduction_shapes(),
    )

    assert audit["status"] == "ok"
    assert audit["input_reduction_shape_count"] == 2
    assert audit["local_image_schema_count"] == 2
    assert audit["local_image_schema_proved_count"] == 0
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["local_image_schemas_not_conditions"] is True
    assert audit["boundary"] == BOUNDARY
    assert audit["schemas"][0] == {
        "schema_id": "odd-prime-local-image-nonzero-double-root-tangent-1",
        "nodal_reduction_shape": "nodal-cubic-with-nonzero-double-root",
        "tangent_squareclass": "1",
        "model_shape": "y^2 = x*(x-r)^2 with r a local unit and tangent squareclass 1",
        "unit_hypothesis": "r is nonzero modulo ell and r is a square modulo ell",
        "covered_reduction_shape_count": 1,
        "covered_lemma_ids": ["odd-prime-lemma-kernel-minus-p-divides-L"],
        "required_theorem": (
            "compute the 2-isogeny local squareclass image for the nodal "
            "unit-double-root model with tangent squareclass 1"
        ),
        "proof_status": "open",
        "local_image_schema_proved": False,
        "local_condition_proved": False,
    }
    assert audit["schemas"][1]["schema_id"] == (
        "odd-prime-local-image-zero-double-root-tangent--1"
    )
    assert audit["schemas"][1]["model_shape"] == (
        "y^2 = x^2*(x-s) with s a local unit and tangent squareclass -1"
    )


def test_rank_zero_selmer_odd_prime_local_image_schemas_reports_unready_inputs() -> None:
    reduction_shapes = _reduction_shapes()
    reduction_shapes["ready"] = False
    reduction_shapes["status"] = "issues"

    audit = audit_rank_zero_selmer_odd_prime_local_image_schemas(
        odd_prime_reduction_shapes=reduction_shapes,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["odd_prime_reduction_shapes_not_ready"]


def test_rank_zero_selmer_odd_prime_local_image_schemas_cli_writes_audit(
    tmp_path: Path,
) -> None:
    reduction_shapes = tmp_path / "odd_prime_reduction_shapes.json"
    out = tmp_path / "odd_prime_local_image_schemas.json"
    reduction_shapes.write_text(json.dumps(_reduction_shapes()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py",
            "--odd-prime-reduction-shapes",
            str(reduction_shapes),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "local_image_schema_count=2" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["local_image_schemas_not_conditions"] is True


def test_write_json_writes_sorted_rank_zero_selmer_odd_prime_local_image_schemas(
    tmp_path: Path,
) -> None:
    out = tmp_path / "odd_prime_local_image_schemas.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
