# Ponytail Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove repo complexity found by the ponytail audit without touching active proof work accidentally.

**Architecture:** Do the cleanup in small, independently testable slices. Start with low-risk code surface reductions, then optional dependency trimming, then larger artifact/script deletions only after an explicit checkpoint because the worktree already has active uncommitted proof files.

**Tech Stack:** Python 3.12, uv, pytest, ruff, git.

---

## File Structure

- `scripts/search.py`: keep as a script-only compatibility entrypoint; no private re-export surface.
- `pyproject.toml`: move literature-only dependencies out of core runtime if tests can remain green.
- `src/rational_distance/proof_status/methods.py`: remove always-skipped placeholder methods only after updating pipeline expectations.
- `tests/`: adjust tests beside each behavior change.
- `results/`: defer tracked result-corpus pruning until the user confirms destructive deletion, because several `results/` files are currently modified.

### Task 1: Thin Search Script Wrapper

**Files:**
- Modify: `scripts/search.py`
- Test: `tests/test_cli.py`

- [x] **Step 1: Replace broad private re-export wrapper with a minimal compatibility surface**

```python
"""Compatibility entrypoint for the split search CLI.

Tests still import `build_parser` and `_resolve_parametric_limits` from this
historical script module, so keep only that small compatibility surface.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.cli.search import build_parser, main
from rational_distance.cli.search.parametric_runner import _resolve_parametric_limits

__all__ = ["_resolve_parametric_limits", "build_parser", "main"]


if __name__ == "__main__":
    main()
```

- [x] **Step 2: Run CLI parser tests**

Run: `uv run pytest tests/test_cli.py -q`
Expected: PASS.

- [x] **Step 3: Run import smoke**

Run: `uv run python scripts/search.py --help >/tmp/d19-search-help.txt`
Expected: exit 0.

### Task 2: Move PDF Extraction Dependency Out Of Core Runtime

**Files:**
- Modify: `pyproject.toml`
- Modify: `src/rational_distance/literature/pdf_text.py`
- Modify: `tests/test_pdf_text.py`
- Modify: `docs/literature/README.md`
- Modify: `docs/literature/pdfs/README.md`

- [x] **Step 1: Make `pypdf` optional**

Move `pypdf>=6.12.1` from `[project].dependencies` into a `literature` dependency group.

- [x] **Step 2: Make PDF tests skip when the optional group is not installed**

Add `pytest.importorskip("pypdf")` before importing `rational_distance.literature.pdf_text`.

- [x] **Step 3: Update commands**

Change PDF extraction docs to use `uv run --group literature python scripts/utility/extract_pdf_text.py ...`.

- [x] **Step 4: Verify**

Run: `uv run pytest tests/test_pdf_text.py -q`
Expected: PASS or SKIP only when `pypdf` is absent.

### Task 3: Remove Always-Skipped Future Method Placeholders

**Files:**
- Modify: `src/rational_distance/proof_status/methods.py`
- Modify: `tests/test_proof_status.py`
- Modify: `docs/IMPLEMENTATION.md`

- [x] **Step 1: Remove `run_chabauty_stub` and `run_brauer_manin_stub` from the default pipeline**

Keep future directions in docs, not as runtime method rows.

- [x] **Step 2: Update pipeline-name tests**

Expected default pipeline names become:

```python
(
    "safe_sieve",
    "chain_closure_mod_sieve",
    "factor_concordant",
    "multi_n_sieve",
    "f2_rank",
    "rank_zero",
    "heegner",
)
```

- [x] **Step 3: Verify proof-status tests**

Run: `uv run pytest tests/test_proof_status.py -q`
Expected: PASS.

### Task 4: Consolidate Repeated JSON Helpers

**Files:**
- Create: `scripts/theory/json_io.py`
- Modify: a first batch of AA+BB audit scripts and matching tests.

- [x] **Step 1: Add shared helper**

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
```

- [x] **Step 2: Convert one coherent batch**

Start with `scripts/theory/audit_closure_quotient_rank_zero_aa_bb_*.py`.

- [x] **Step 3: Verify converted tests**

Run: `uv run pytest tests/test_closure_quotient_rank_zero_aa_bb_*.py -q`
Expected: PASS.

### Task 5: Prune Tracked Result Corpus

**Files:**
- Delete: tracked generated files under `results/`, except `results/README.md` and any compact canonical fixtures still imported by tests.
- Modify: `.gitignore`
- Modify: docs that point at deleted raw files.

- [x] **Step 1: Check destructive boundary**

Do not run `git rm` until the user confirms this specific deletion batch, because the current worktree has modified and untracked proof result files.

- [x] **Step 2: Identify test-used fixtures**

Run: `rg -n "results/" tests src scripts docs/PROJECT_STATUS.md docs/OPEN_DIRECTIONS.md`.

- [x] **Step 3: Delete only unused generated outputs**

Use `git rm` for tracked generated outputs and leave active modified proof files alone unless explicitly confirmed.

- [x] **Step 4: Verify**

Run: `uv run pytest -q`
Expected: PASS.

## Self-Review

- Spec coverage: covers every ponytail-audit item except the 8,868-line `rational_ratio.py` split, which is intentionally deferred because it is high-blast-radius math tooling.
- Placeholder scan: no `TBD` or unspecified code-only steps.
- Type consistency: helper functions use `Path` and `dict[str, Any]` consistently across planned scripts.
