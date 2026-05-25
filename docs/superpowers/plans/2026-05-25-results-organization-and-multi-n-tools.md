# Results Organization and Multi-N Tools Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organize `results/` into an authoritative, searchable home for the `max_hyp=10000` multi-concordant scan, then add reusable tools to query ground-truth pairs and inspect half-points / squarefree 2-descent classes.

**Architecture:** Keep `results/multi_concordant_N_max10000.jsonl` as the authoritative raw dataset instead of immediately migrating to SQLite. Add a lightweight results catalog (`results/README.md` + generated `results/catalog.json`) so humans and scripts can find important artifacts, then add a small Python results library under `src/rational_distance/results/` plus two focused scripts: one for ground-truth lookup and one for half-point analysis. This keeps the expensive scan output immutable while making downstream comparison and future “fast algorithm” experiments easy to verify.

**Tech Stack:** Python 3.11+, argparse, JSON/JSONL, pytest, existing `src/` import pattern, existing `uv` workflow.

---

## File Structure

### New files
- `results/README.md` — human-readable index of important result artifacts, grouped by topic, with “authoritative” notes.
- `results/catalog.json` — machine-readable catalog of curated result files.
- `src/rational_distance/results/__init__.py` — package marker + public exports for results helpers.
- `src/rational_distance/results/catalog.py` — curated metadata definitions and catalog writer.
- `src/rational_distance/results/multi_concordant.py` — loaders and lookup helpers for `multi_concordant_N_max10000.jsonl`.
- `src/rational_distance/concordant/half_points.py` — reusable half-point enumeration and squarefree 2-descent signature helpers.
- `scripts/build_results_catalog.py` — regenerate `results/catalog.json` from curated metadata.
- `scripts/lookup_multi_n.py` — query a pair `(A,B)` against the ground-truth JSONL.
- `scripts/analyze_multi_n_half_points.py` — print concordant `N`, corresponding `P_N`, all half-points, and squarefree signatures.
- `tests/test_results_catalog.py` — verifies catalog generation.
- `tests/test_multi_concordant_results.py` — verifies results lookup helpers.
- `tests/test_half_points.py` — verifies half-point enumeration and signatures on known examples.

### Existing files to modify
- `docs/MULTI_CONCORDANT_N_STRATEGY.md` — add one short note pointing to the new `results/README.md` and lookup/analyze commands.
- `docs/work-logs/046-multi-concordant-n-scan-10k.md` — add one short “authoritative storage” section pointing to the catalog.

---

### Task 1: Create an authoritative catalog for `results/`

**Files:**
- Create: `results/README.md`
- Create: `src/rational_distance/results/__init__.py`
- Create: `src/rational_distance/results/catalog.py`
- Create: `scripts/build_results_catalog.py`
- Create: `tests/test_results_catalog.py`

- [ ] **Step 1: Write the failing catalog test**

```python
from __future__ import annotations

import json
from pathlib import Path

from rational_distance.results.catalog import build_results_catalog


def test_build_results_catalog_records_curated_artifacts(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    dataset = results_dir / "multi_concordant_N_max10000.jsonl"
    dataset.write_text('{"A": 27, "B": 160}\n', encoding="utf-8")

    catalog = build_results_catalog(results_dir)

    assert catalog["artifacts"][0]["path"] == "multi_concordant_N_max10000.jsonl"
    assert catalog["artifacts"][0]["exists"] is True
    assert catalog["artifacts"][0]["category"] == "multi-concordant"
    assert catalog["artifacts"][0]["authoritative"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_results_catalog.py::test_build_results_catalog_records_curated_artifacts -v
```

Expected: FAIL with `ModuleNotFoundError` or `cannot import name 'build_results_catalog'`.

- [ ] **Step 3: Write minimal catalog implementation**

Create `src/rational_distance/results/__init__.py`:

```python
"""Helpers for curated result artifacts."""

from .catalog import build_results_catalog
from .multi_concordant import MultiConcordantPair, load_multi_concordant_index, lookup_multi_concordant_pair

__all__ = [
    "MultiConcordantPair",
    "build_results_catalog",
    "load_multi_concordant_index",
    "lookup_multi_concordant_pair",
]
```

Create `src/rational_distance/results/catalog.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class CuratedArtifact:
    path: str
    category: str
    description: str
    authoritative: bool = False


CURATED_ARTIFACTS: tuple[CuratedArtifact, ...] = (
    CuratedArtifact(
        path="multi_concordant_N_max10000.jsonl",
        category="multi-concordant",
        description="Ground-truth reduced pairs with >= 2 concordant N for max_hyp=10000.",
        authoritative=True,
    ),
    CuratedArtifact(
        path="proof_status.db",
        category="proof-status",
        description="SQLite database for proof workflow state.",
        authoritative=True,
    ),
)


def build_results_catalog(results_dir: Path) -> dict[str, object]:
    artifacts: list[dict[str, object]] = []
    for item in CURATED_ARTIFACTS:
        file_path = results_dir / item.path
        artifacts.append(
            {
                "path": item.path,
                "category": item.category,
                "description": item.description,
                "authoritative": item.authoritative,
                "exists": file_path.exists(),
                "size_bytes": file_path.stat().st_size if file_path.exists() else None,
            }
        )
    return {"results_dir": str(results_dir), "artifacts": artifacts}


def write_results_catalog(results_dir: Path, output_path: Path | None = None) -> Path:
    target = output_path if output_path is not None else results_dir / "catalog.json"
    payload = build_results_catalog(results_dir)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
```

Create `scripts/build_results_catalog.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.results.catalog import write_results_catalog

    output_path = write_results_catalog(ROOT / "results")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `results/README.md` with curated sections like:

```markdown
# Results Directory

This directory contains generated artifacts. Not every file is equally important.

## Authoritative artifacts

### Multi-concordant ground truth
- `multi_concordant_N_max10000.jsonl`
- Coverage: all reduced coprime pairs `1 <= A < B <= 10000`
- Meaning: one JSON line per pair with `n_concordant >= 2`
- Record count: 854
- Use this file as the ground-truth comparison set for any future “fast multi-N” heuristic.

### Proof workflow state
- `proof_status.db`
- Meaning: SQLite state for proof-status workflow

## Regenerate curated catalog

```bash
uv run python scripts/build_results_catalog.py
```
```

- [ ] **Step 4: Run targeted test to verify it passes**

Run:

```bash
uv run pytest tests/test_results_catalog.py::test_build_results_catalog_records_curated_artifacts -v
```

Expected: PASS.

- [ ] **Step 5: Generate the real catalog file**

Run:

```bash
uv run python scripts/build_results_catalog.py
```

Expected: `wrote /Users/konan/Desktop/d19/results/catalog.json`

- [ ] **Step 6: Commit**

```bash
git add results/README.md results/catalog.json src/rational_distance/results/__init__.py src/rational_distance/results/catalog.py scripts/build_results_catalog.py tests/test_results_catalog.py
git commit -m "feat: catalog curated result artifacts"
```

---

### Task 2: Add reusable ground-truth lookup for multi-N pairs

**Files:**
- Create: `src/rational_distance/results/multi_concordant.py`
- Create: `scripts/lookup_multi_n.py`
- Create: `tests/test_multi_concordant_results.py`
- Modify: `src/rational_distance/results/__init__.py`

- [ ] **Step 1: Write the failing lookup test**

```python
from __future__ import annotations

from pathlib import Path

from rational_distance.results.multi_concordant import lookup_multi_concordant_pair


def test_lookup_multi_concordant_pair_matches_pair_ignoring_order(tmp_path: Path) -> None:
    dataset = tmp_path / "multi.jsonl"
    dataset.write_text(
        "\n".join(
            [
                '{"A": 27, "B": 160, "n_concordant": 2, "concordant_N": [36, 120], "A_plus_B": 187, "closure_pairs": []}',
                '{"A": 153, "B": 560, "n_concordant": 3, "concordant_N": [204, 420, 3900], "A_plus_B": 713, "closure_pairs": []}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    row = lookup_multi_concordant_pair(560, 153, dataset_path=dataset)

    assert row is not None
    assert row.A == 153
    assert row.B == 560
    assert row.n_concordant == 3
    assert row.concordant_N == [204, 420, 3900]
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_multi_concordant_results.py::test_lookup_multi_concordant_pair_matches_pair_ignoring_order -v
```

Expected: FAIL with missing module or function.

- [ ] **Step 3: Write minimal lookup implementation**

Create `src/rational_distance/results/multi_concordant.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MULTI_CONCORDANT_PATH = ROOT / "results" / "multi_concordant_N_max10000.jsonl"


@dataclass(frozen=True)
class MultiConcordantPair:
    A: int
    B: int
    n_concordant: int
    concordant_N: list[int]
    A_plus_B: int
    closure_pairs: list[list[int]]


def iter_multi_concordant_pairs(dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH):
    with dataset_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            yield MultiConcordantPair(**row)


def load_multi_concordant_index(dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH) -> dict[tuple[int, int], MultiConcordantPair]:
    index: dict[tuple[int, int], MultiConcordantPair] = {}
    for row in iter_multi_concordant_pairs(dataset_path):
        index[(row.A, row.B)] = row
    return index


def lookup_multi_concordant_pair(A: int, B: int, dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH) -> MultiConcordantPair | None:
    a, b = sorted((A, B))
    return load_multi_concordant_index(dataset_path).get((a, b))
```

Create `scripts/lookup_multi_n.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lookup a pair in multi_concordant_N_max10000.jsonl")
    _ = parser.add_argument("A", type=int)
    _ = parser.add_argument("B", type=int)
    _ = parser.add_argument("--dataset", type=Path, default=ROOT / "results" / "multi_concordant_N_max10000.jsonl")
    return parser.parse_args()


def main() -> int:
    from rational_distance.results.multi_concordant import lookup_multi_concordant_pair

    args = parse_args()
    row = lookup_multi_concordant_pair(args.A, args.B, dataset_path=args.dataset)
    if row is None:
        print("not found")
        return 1
    print(json.dumps(row.__dict__, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run targeted test to verify it passes**

Run:

```bash
uv run pytest tests/test_multi_concordant_results.py::test_lookup_multi_concordant_pair_matches_pair_ignoring_order -v
```

Expected: PASS.

- [ ] **Step 5: Smoke-test the real dataset lookup**

Run:

```bash
uv run python scripts/lookup_multi_n.py 153 560
```

Expected: JSON output containing `"n_concordant": 3` and `"concordant_N": [204, 420, 3900]`.

- [ ] **Step 6: Commit**

```bash
git add src/rational_distance/results/multi_concordant.py src/rational_distance/results/__init__.py scripts/lookup_multi_n.py tests/test_multi_concordant_results.py
git commit -m "feat: add multi-N ground-truth lookup"
```

---

### Task 3: Add a reusable half-point and squarefree 2-descent analysis tool

**Files:**
- Create: `src/rational_distance/concordant/half_points.py`
- Create: `scripts/analyze_multi_n_half_points.py`
- Create: `tests/test_half_points.py`

- [ ] **Step 1: Write the failing half-point test**

```python
from __future__ import annotations

from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N


def test_enumerate_half_points_for_known_multi_n_pair() -> None:
    halves = enumerate_half_points_for_concordant_N(153, 560, 204)

    assert len(halves) == 8
    assert (19992, -17013192) in [(point.x, point.y) for point in halves]
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_half_points.py::test_enumerate_half_points_for_known_multi_n_pair -v
```

Expected: FAIL with missing module or function.

- [ ] **Step 3: Write minimal half-point implementation**

Create `src/rational_distance/concordant/half_points.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isqrt
from fractions import Fraction


@dataclass(frozen=True)
class RationalPoint:
    x: int
    y: int


@dataclass(frozen=True)
class HalfPointAnalysis:
    x: int
    y: int
    signature: tuple[int, int, int]


def _square_root_or_raise(value: int) -> int:
    root = isqrt(value)
    if root * root != value:
        raise ValueError(f"{value} is not a square")
    return root


def squarefree_part(n: int) -> int:
    sign = -1 if n < 0 else 1
    n = abs(n)
    factor = 2
    out = 1
    while factor * factor <= n:
        exponent = 0
        while n % factor == 0:
            n //= factor
            exponent += 1
        if exponent % 2 == 1:
            out *= factor
        factor += 1 if factor == 2 else 2
    if n > 1:
        out *= n
    return sign * out


def _double_point(A: int, B: int, point: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    x, y = point
    a2 = A * A + B * B
    a4 = A * A * B * B
    slope = Fraction(3 * x * x + 2 * a2 * x + a4, 2 * y)
    x2 = slope * slope - a2 - 2 * x
    y2 = -y + slope * (x - x2)
    return x2, y2


def enumerate_half_points_for_concordant_N(A: int, B: int, N: int) -> list[HalfPointAnalysis]:
    r1 = N
    r2 = _square_root_or_raise(N * N + A * A)
    r3 = _square_root_or_raise(N * N + B * B)
    target = (Fraction(N * N), Fraction(N * r2 * r3))

    halves: dict[tuple[int, int], HalfPointAnalysis] = {}
    for s1, s2, s3 in product((1, -1), repeat=3):
        u1, u2, u3 = s1 * r1, s2 * r2, s3 * r3
        x = u1 * u2 + u1 * u3 + u2 * u3
        y = (u1 + u2) * (u1 + u3) * (u2 + u3)
        doubled = _double_point(A, B, (Fraction(x), Fraction(y)))
        if doubled == target or doubled == (target[0], -target[1]):
            halves[(x, y)] = HalfPointAnalysis(
                x=x,
                y=y,
                signature=(
                    squarefree_part(x),
                    squarefree_part(x + A * A),
                    squarefree_part(x + B * B),
                ),
            )
    return sorted(halves.values(), key=lambda item: (abs(item.x), abs(item.y), item.x, item.y))
```

Create `scripts/analyze_multi_n_half_points.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze half-points for all concordant N of a pair")
    _ = parser.add_argument("A", type=int)
    _ = parser.add_argument("B", type=int)
    return parser.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N

    args = parse_args()
    concordant = sorted(find_concordant_by_factorization(args.A, args.B))
    payload: dict[str, object] = {"A": args.A, "B": args.B, "concordant_N": concordant, "half_points": {}}
    for N in concordant:
        payload["half_points"][str(N)] = [
            {"x": point.x, "y": point.y, "signature": list(point.signature)}
            for point in enumerate_half_points_for_concordant_N(args.A, args.B, N)
        ]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run targeted test to verify it passes**

Run:

```bash
uv run pytest tests/test_half_points.py::test_enumerate_half_points_for_known_multi_n_pair -v
```

Expected: PASS.

- [ ] **Step 5: Smoke-test the real pair analysis**

Run:

```bash
uv run python scripts/analyze_multi_n_half_points.py 153 560
```

Expected: JSON output containing `"concordant_N": [204, 420, 3900]` and the known half-point `(19992, -17013192)` under `204`.

- [ ] **Step 6: Commit**

```bash
git add src/rational_distance/concordant/half_points.py scripts/analyze_multi_n_half_points.py tests/test_half_points.py
git commit -m "feat: add half-point analysis for multi-N pairs"
```

---

### Task 4: Link the new catalog and tools from existing docs

**Files:**
- Modify: `docs/MULTI_CONCORDANT_N_STRATEGY.md`
- Modify: `docs/work-logs/046-multi-concordant-n-scan-10k.md`

- [ ] **Step 1: Add a short “authoritative storage” note to the strategy doc**

Insert a small block like:

```markdown
### Ground-truth storage

The authoritative `max_hyp=10000` multi-N dataset lives at:

```text
results/multi_concordant_N_max10000.jsonl
```

Supporting index and helper commands:

```bash
uv run python scripts/build_results_catalog.py
uv run python scripts/lookup_multi_n.py 153 560
uv run python scripts/analyze_multi_n_half_points.py 153 560
```
```

- [ ] **Step 2: Add the same pointer to worklog 046**

Append a short section like:

```markdown
## Authoritative storage

The raw scan output remains:
- `results/multi_concordant_N_max10000.jsonl`

Use these helpers for follow-up work:
- `results/README.md`
- `results/catalog.json`
- `uv run python scripts/lookup_multi_n.py A B`
- `uv run python scripts/analyze_multi_n_half_points.py A B`
```

- [ ] **Step 3: Run focused tests and lints**

Run:

```bash
uv run pytest tests/test_results_catalog.py tests/test_multi_concordant_results.py tests/test_half_points.py -q
uv run ruff check src/rational_distance/results src/rational_distance/concordant/half_points.py scripts/build_results_catalog.py scripts/lookup_multi_n.py scripts/analyze_multi_n_half_points.py tests/test_results_catalog.py tests/test_multi_concordant_results.py tests/test_half_points.py
```

Expected: all tests pass; `ruff check` reports `All checks passed!`.

- [ ] **Step 4: Commit**

```bash
git add docs/MULTI_CONCORDANT_N_STRATEGY.md docs/work-logs/046-multi-concordant-n-scan-10k.md

git commit -m "docs: index multi-N results and helper tools"
```

---

## Self-Review

### Spec coverage
- Organize and record results under noisy `results/`: covered by Task 1 (`results/README.md` + `results/catalog.json`).
- Make the expensive `max_hyp=10000` run easy to query later: covered by Task 2 (`lookup_multi_n.py` + reusable loader).
- Prepare the short reusable half-point script before fast algorithm work: covered by Task 3 (`analyze_multi_n_half_points.py` + reusable library).
- Make future “fast algorithm” outputs comparable with current ground truth: covered by Task 2 and Task 4.

### Placeholder scan
- No `TODO` / `TBD` placeholders remain.
- Every test, command, and target path is explicit.

### Type consistency
- `MultiConcordantPair` is reused consistently between package exports and lookup script.
- Half-point tool uses a single `HalfPointAnalysis` type and one public function `enumerate_half_points_for_concordant_N`.

---

Plan complete and saved to `docs/superpowers/plans/2026-05-25-results-organization-and-multi-n-tools.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
