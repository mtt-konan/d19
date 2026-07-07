# Frontier Handoff Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a rerunnable audit proving that the 10 residual frontier handoff packages are internally consistent and are still marked as non-proofs.

**Architecture:** Add one focused Python audit that reads the rank-zero queue, non-rankzero queue, priority ledger, and handoff directory. The audit verifies JSON/Sage/Magma file presence plus map verification, local witness, and bounded Sage probe contents without promoting any residual cover to a theorem.

**Tech Stack:** Python standard library, `pytest`, existing `uv run` test workflow.

---

### Task 1: Frontier Audit Tests

**Files:**
- Create: `tests/test_mixed_closure_frontier_handoff_audit.py`

- [ ] **Step 1: Write the failing test**

Create synthetic queues, priorities, and handoff files for one rank-zero group, one rank-one group, and one even-gap4 group. Assert that the audit returns `status="ok"`, `handoff_group_count=3`, `target_cover_count=7`, all map/local/probe counts are `3`, `strict_promotion_count=0`, and `candidate_not_proof=True`.

- [ ] **Step 2: Run test to verify it fails**

Run: `UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest tests/test_mixed_closure_frontier_handoff_audit.py -q`

Expected: FAIL because `scripts.theory.audit_mixed_closure_frontier_handoffs` does not exist.

### Task 2: Frontier Audit Script

**Files:**
- Create: `scripts/theory/audit_mixed_closure_frontier_handoffs.py`

- [ ] **Step 1: Implement minimal audit logic**

Read queues and priorities, derive expected handoff names from priority rows, check required files and JSON content, and return a structured audit with `violations` and `missing_files`.

- [ ] **Step 2: Run test to verify it passes**

Run: `UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest tests/test_mixed_closure_frontier_handoff_audit.py -q`

Expected: PASS.

### Task 3: Integrate Gates And Docs

**Files:**
- Modify: `scripts/theory/audit_closure_quotient_partial_artifacts.py`
- Modify: `scripts/theory/summarize_closure_quotient_partial_result.py`
- Modify: `tests/test_closure_quotient_partial_artifacts.py`
- Modify: `tests/test_summarize_closure_quotient_partial_result.py`
- Modify: `docs/CLOSURE_QUOTIENT_MAINLINE.md`
- Modify: `docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md`
- Create: `docs/work-logs/340-frontier-handoff-audit.md`

- [ ] **Step 1: Add the audit to artifact and summary gates**

The summary gate must fail if the frontier handoff audit is not `status="ok"`, has violations, has missing files, has `strict_promotion_count != 0`, or lacks `candidate_not_proof=True`.

- [ ] **Step 2: Run gates**

Run the new audit on real `results/`, rerun language, paper-claim, artifact, and partial-result summaries, then run focused pytest and ruff.

Expected: all checks pass; real audit reports 10 groups, 23 covers, no strict promotions.
