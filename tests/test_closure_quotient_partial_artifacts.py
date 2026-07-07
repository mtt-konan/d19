from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_partial_artifacts import (
    DEFAULT_REQUIRED_ARTIFACTS,
    Artifact,
    audit_artifacts,
    parse_required_artifact,
    write_json,
)


def test_audit_artifacts_marks_ready_when_required_files_exist(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/example.py"),
        Artifact("test", "tests/test_example.py"),
        Artifact("result", "results/example.json"),
        Artifact("worklog", "docs/work-logs/999-example.md"),
    ]
    for artifact in required:
        path = tmp_path / artifact.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit == {
        "ready": True,
        "required_file_count": 4,
        "category_counts": {
            "result": 1,
            "script": 1,
            "test": 1,
            "worklog": 1,
        },
        "missing_files": [],
        "required_files": [
            {"category": "script", "path": "scripts/theory/example.py"},
            {"category": "test", "path": "tests/test_example.py"},
            {"category": "result", "path": "results/example.json"},
            {"category": "worklog", "path": "docs/work-logs/999-example.md"},
        ],
        "boundary": (
            "This checks artifact presence for the closure-quotient partial-result "
            "package. It does not check mathematical truth."
        ),
    }


def test_audit_artifacts_reports_missing_files(tmp_path: Path) -> None:
    required = [
        Artifact("script", "scripts/theory/present.py"),
        Artifact("result", "results/missing.json"),
    ]
    present = tmp_path / "scripts/theory/present.py"
    present.parent.mkdir(parents=True, exist_ok=True)
    present.write_text("ok\n", encoding="utf-8")

    audit = audit_artifacts(root=tmp_path, required=required)

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {"category": "result", "path": "results/missing.json"}
    ]


def test_default_artifact_manifest_includes_priority_handoff_audit() -> None:
    paths = {artifact.path for artifact in DEFAULT_REQUIRED_ARTIFACTS}

    assert "scripts/theory/audit_mixed_closure_priority_handoffs.py" in paths
    assert "scripts/theory/sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py" in paths
    assert "scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py" in paths
    assert "scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py" in paths
    assert "scripts/theory/audit_mixed_closure_residual_open_frontier.py" in paths
    assert "scripts/theory/summarize_mixed_closure_rank_zero_frontier.py" in paths
    assert "scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py" in paths
    assert "scripts/theory/audit_mixed_closure_residual_frontier_strategy.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_handoffs.py" in paths
    assert "scripts/theory/summarize_mixed_closure_frontier_strictification.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py" in paths
    assert "scripts/theory/sage_probe_mixed_closure_rank_methods.py" in paths
    assert "scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "scripts/theory/audit_mixed_closure_frontier_next_actions.py" in paths
    assert "scripts/theory/sage_probe_mixed_closure_local_witnesses.py" in paths
    assert "scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py" in paths
    assert "tests/test_mixed_closure_priority_handoff_audit.py" in paths
    assert "tests/test_sage_verify_mixed_closure_handoff_maps.py" in paths
    assert "tests/test_sage_verify_mixed_closure_residual_cover_maps.py" in paths
    assert "tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py" in paths
    assert "tests/test_mixed_closure_bsd_conditional_no_point_audit.py" in paths
    assert "tests/test_mixed_closure_residual_open_frontier_audit.py" in paths
    assert "tests/test_mixed_closure_rank_zero_frontier_queue.py" in paths
    assert "tests/test_mixed_closure_non_rankzero_frontier_queue.py" in paths
    assert "tests/test_mixed_closure_residual_frontier_strategy.py" in paths
    assert "tests/test_mixed_closure_frontier_handoff_audit.py" in paths
    assert "tests/test_mixed_closure_frontier_strictification_queue.py" in paths
    assert "tests/test_mixed_closure_frontier_strictification_attempts.py" in paths
    assert "tests/test_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "tests/test_batch_sage_probe_mixed_closure_rank_methods.py" in paths
    assert "tests/test_mixed_closure_frontier_next_action_audit.py" in paths
    assert "tests/test_sage_probe_mixed_closure_local_witnesses.py" in paths
    assert "tests/test_mixed_closure_residual_selmer_gap_ledger.py" in paths
    assert "docs/work-logs/313-priority-handoff-probe-audit.md" in paths
    assert "docs/work-logs/314-sage-cover-map-identity-verification.md" in paths
    assert "docs/work-logs/315-sage-local-witness-probe.md" in paths
    assert "docs/work-logs/316-all-residual-local-witnesses.md" in paths
    assert "docs/work-logs/317-residual-local-witness-paper-claim-gate.md" in paths
    assert "docs/work-logs/318-residual-selmer-gap-ledger.md" in paths
    assert "docs/work-logs/319-all-residual-cover-map-verification.md" in paths
    assert "docs/work-logs/320-residual-selmer-gap-frontier-split.md" in paths
    assert "docs/work-logs/321-rank0-torsion-preimage-audit.md" in paths
    assert "docs/work-logs/322-bsd-conditional-no-point-audit.md" in paths
    assert "docs/work-logs/323-residual-open-frontier-audit.md" in paths
    assert "docs/work-logs/324-rank-zero-frontier-queue.md" in paths
    assert "docs/work-logs/325-non-rankzero-frontier-queue.md" in paths
    assert "docs/work-logs/326-rank1-frontier-recheck.md" in paths
    assert "docs/work-logs/327-even-gap4-frontier-recheck.md" in paths
    assert "docs/work-logs/328-rankzero-frontier-recheck-567-3757.md" in paths
    assert "docs/work-logs/329-rankzero-frontier-recheck-5075-17901.md" in paths
    assert "docs/work-logs/330-rankzero-frontier-long-recheck-1625-5643.md" in paths
    assert "docs/work-logs/331-rankzero-frontier-recheck-8075-8613.md" in paths
    assert "docs/work-logs/332-rankzero-frontier-recheck-391-9009.md" in paths
    assert "docs/work-logs/333-rankzero-frontier-recheck-209-21735.md" in paths
    assert "docs/work-logs/334-rankzero-frontier-recheck-5083-12825.md" in paths
    assert "docs/work-logs/335-rankzero-frontier-recheck-5301-38675.md" in paths
    assert "docs/work-logs/336-residual-frontier-strategy-audit.md" in paths
    assert "docs/work-logs/337-frontier-target-handoff-1625-5643.md" in paths
    assert "docs/work-logs/338-all-rankzero-frontier-handoffs.md" in paths
    assert "docs/work-logs/339-non-rankzero-frontier-handoffs.md" in paths
    assert "docs/work-logs/340-frontier-handoff-audit.md" in paths
    assert "docs/work-logs/341-frontier-strictification-queue.md" in paths
    assert "docs/work-logs/342-frontier-strictification-attempt.md" in paths
    assert "docs/work-logs/343-frontier-rank-method-probe.md" in paths
    assert "docs/work-logs/344-frontier-batch-rank-method-probe.md" in paths
    assert "docs/work-logs/345-frontier-next-action-audit.md" in paths
    assert "docs/work-logs/346-rankzero-frontier-long-recheck-567-3757.md" in paths
    assert "docs/work-logs/347-rankzero-frontier-long-recheck-5075-17901.md" in paths
    assert "docs/work-logs/348-rankzero-frontier-long-recheck-8075-8613.md" in paths
    assert "results/mixed_closure_priority_handoff_audit_top4.json" in paths
    assert "results/mixed_closure_aabb_residual_local_witnesses.json" in paths
    assert "results/mixed_closure_residual_selmer_gap_ledger.json" in paths
    assert "results/mixed_closure_residual_cover_map_verify.json" in paths
    assert "results/mixed_closure_rank0_sha2_torsion_preimage_audit.json" in paths
    assert "results/mixed_closure_bsd_conditional_no_point_audit.json" in paths
    assert "results/mixed_closure_residual_open_frontier_audit.json" in paths
    assert "results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_391_9009_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_209_21735_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5083_12825_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rankzero_frontier_recheck_5301_38675_BB_s13_20_t120.jsonl" in paths
    assert "results/sage_rank1_frontier_recheck_209_5355_BB_s13_20_t120.jsonl" in paths
    assert (
        "results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl"
        in paths
    )
    assert "results/mixed_closure_rank_zero_frontier_queue.json" in paths
    assert "results/mixed_closure_non_rankzero_frontier_queue.json" in paths
    assert "results/mixed_closure_residual_frontier_strategy_audit.json" in paths
    assert "results/mixed_closure_frontier_handoff_audit.json" in paths
    assert "results/mixed_closure_frontier_strictification_queue.json" in paths
    assert "results/mixed_closure_frontier_strictification_attempt_audit.json" in paths
    assert (
        "results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json"
        in paths
    )
    assert (
        "results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json"
        in paths
    )
    assert (
        "results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json"
        in paths
    )
    assert "results/mixed_closure_frontier_next_action_audit.json" in paths
    assert (
        "results/priority_006_567_3757_BB_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_009_5075_17901_AA_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/priority_012_8075_8613_AA_rank_methods_t600_twodescent40.json"
        in paths
    )
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_sage_probe.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_map_verify.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_001_115_297_AA_covers_3_4_local_witnesses.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.sage"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3.magma"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_sage_probe.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_map_verify.json"
    ) in paths
    assert (
        "results/mixed_closure_residual_handoffs/"
        "priority_005_1625_5643_AA_covers_4_3_local_witnesses.json"
    ) in paths
    for name in [
        "priority_006_567_3757_BB_covers_4_3",
        "priority_009_5075_17901_AA_covers_4_3",
        "priority_012_8075_8613_AA_covers_4_3",
        "priority_013_391_9009_BB_covers_4_3",
        "priority_017_209_21735_BB_covers_3_4",
        "priority_024_5083_12825_BB_covers_3_4",
        "priority_025_5301_38675_BB_covers_4_3",
    ]:
        assert f"results/mixed_closure_residual_handoffs/{name}.json" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.sage" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.magma" in paths
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_sage_probe.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_map_verify.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_local_witnesses.json"
            in paths
        )
    for name in [
        "priority_008_209_5355_BB_covers_5_4_3",
        "priority_011_1449_12155_BB_covers_5_6_3_4",
    ]:
        assert f"results/mixed_closure_residual_handoffs/{name}.json" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.sage" in paths
        assert f"results/mixed_closure_residual_handoffs/{name}.magma" in paths
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_sage_probe.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_map_verify.json"
            in paths
        )
        assert (
            f"results/mixed_closure_residual_handoffs/{name}_local_witnesses.json"
            in paths
        )


def test_parse_required_artifact_requires_category_and_path() -> None:
    assert parse_required_artifact("script:scripts/theory/x.py") == Artifact(
        "script", "scripts/theory/x.py"
    )


def test_artifact_cli_strict_exits_nonzero_when_required_file_is_missing(
    tmp_path: Path,
) -> None:
    out = tmp_path / "audit.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_partial_artifacts.py",
            "--root",
            str(tmp_path),
            "--require",
            "script:scripts/theory/missing.py",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "ready=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"] == [
        {"category": "script", "path": "scripts/theory/missing.py"}
    ]


def test_write_json_writes_sorted_artifact_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
