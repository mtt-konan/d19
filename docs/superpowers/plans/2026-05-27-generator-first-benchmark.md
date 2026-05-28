# Generator-First Candidate Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an experiment-line-B benchmark that compares direct candidate generators over the integer coprime `(A, B) <= H` domain: all coprime pairs, safe-sieve-surviving pairs, and pivot-on-N multi-concordant pairs.

**Architecture:** Keep generation logic in a small reusable module under `src/rational_distance/concordant/`, with a thin CLI script under `scripts/` for benchmark runs. The benchmark deliberately uses the direct integer domain `1 <= A < B <= max_hyp`, not the current triple-pair `proof_status --max-hyp` domain, so results are comparable to the historical multi-N scans.

**Tech Stack:** Python 3.12, standard library `argparse`, `dataclasses`, `json`, `math.gcd`, existing `safe_pair_sieve.allow_reduced_pair`, existing `fast_multi_n.fast_multi_concordant_pairs`, `pytest`, `uv`.

---

## File Structure

- Create: `src/rational_distance/concordant/candidate_generators.py`
  - Owns direct integer-domain generators and benchmark summary helpers.
  - Exports `iter_coprime_pairs`, `iter_safe_coprime_pairs`, `CandidateGeneratorResult`, and `run_generator_benchmark`.

- Create: `scripts/benchmark_candidate_generators.py`
  - CLI entrypoint for experiment-line-B.
  - Prints a compact table and optionally writes JSON.
  - Default `--max-hyp` is `2000` so accidental runs stay short; `10000` is the planned comparison scale.

- Create: `tests/test_candidate_generators.py`
  - Unit tests for pair generation semantics.
  - Small integration test for benchmark row names and counts.

- Create: `docs/work-logs/072-generator-first-candidate-benchmark.md`
  - Records the experiment purpose, domain distinction, and commands to run.
  - Records actual benchmark numbers after running the 2k and 10k commands.

---

### Task 1: Add direct integer-domain candidate generators

**Files:**
- Create: `src/rational_distance/concordant/candidate_generators.py`
- Test: `tests/test_candidate_generators.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_candidate_generators.py` with this full content:

```python
from __future__ import annotations

from math import gcd

from rational_distance.concordant.candidate_generators import (
    iter_coprime_pairs,
    iter_safe_coprime_pairs,
    run_generator_benchmark,
)
from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


def test_iter_coprime_pairs_matches_direct_gcd_definition() -> None:
    max_hyp = 8

    expected = [
        (a, b)
        for a in range(1, max_hyp + 1)
        for b in range(a + 1, max_hyp + 1)
        if gcd(a, b) == 1
    ]

    assert list(iter_coprime_pairs(max_hyp)) == expected


def test_iter_safe_coprime_pairs_applies_safe_sieve_definition() -> None:
    max_hyp = 10

    expected = [
        (a, b)
        for a in range(1, max_hyp + 1)
        for b in range(a + 1, max_hyp + 1)
        if gcd(a, b) == 1 and allow_reduced_pair(a, b)
    ]

    assert list(iter_safe_coprime_pairs(max_hyp)) == expected
    assert list(iter_safe_coprime_pairs(max_hyp)) == [
        (1, 3),
        (1, 7),
        (3, 5),
        (5, 7),
        (7, 9),
    ]


def test_generators_reject_non_positive_max_hyp() -> None:
    for generator in (iter_coprime_pairs, iter_safe_coprime_pairs):
        try:
            list(generator(0))
        except ValueError as exc:
            assert str(exc) == "max_hyp must be positive"
        else:
            raise AssertionError("generator must reject non-positive max_hyp")


def test_run_generator_benchmark_reports_expected_rows() -> None:
    max_hyp = 200

    rows = run_generator_benchmark(max_hyp)
    by_name = {row.name: row for row in rows}

    assert tuple(by_name) == ("all_coprime", "safe_coprime", "multi_n")
    assert by_name["all_coprime"].pair_count == len(list(iter_coprime_pairs(max_hyp)))
    assert by_name["safe_coprime"].pair_count == len(list(iter_safe_coprime_pairs(max_hyp)))
    assert by_name["multi_n"].pair_count == len(fast_multi_concordant_pairs(max_hyp))
    assert by_name["multi_n"].carries_concordant_n is True
    assert by_name["multi_n"].min_n_count is None or by_name["multi_n"].min_n_count >= 2
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
uv run pytest tests/test_candidate_generators.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'rational_distance.concordant.candidate_generators'`.

- [ ] **Step 3: Implement the generator module**

Create `src/rational_distance/concordant/candidate_generators.py` with this full content:

```python
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import asdict, dataclass
from math import gcd
from time import perf_counter
from typing import Any

from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair

Pair = tuple[int, int]


@dataclass(frozen=True)
class CandidateGeneratorResult:
    name: str
    max_hyp: int
    pair_count: int
    elapsed_s: float
    carries_concordant_n: bool
    min_n_count: int | None
    max_n_count: int | None

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_max_hyp(max_hyp: int) -> None:
    if max_hyp <= 0:
        raise ValueError("max_hyp must be positive")


def iter_coprime_pairs(max_hyp: int) -> Iterator[Pair]:
    _validate_max_hyp(max_hyp)
    for a in range(1, max_hyp + 1):
        for b in range(a + 1, max_hyp + 1):
            if gcd(a, b) == 1:
                yield (a, b)


def iter_safe_coprime_pairs(max_hyp: int) -> Iterator[Pair]:
    _validate_max_hyp(max_hyp)
    for a, b in iter_coprime_pairs(max_hyp):
        if allow_reduced_pair(a, b):
            yield (a, b)


def _count_iterator(name: str, max_hyp: int, pairs: Iterator[Pair]) -> CandidateGeneratorResult:
    started = perf_counter()
    count = sum(1 for _ in pairs)
    elapsed = perf_counter() - started
    return CandidateGeneratorResult(
        name=name,
        max_hyp=max_hyp,
        pair_count=count,
        elapsed_s=elapsed,
        carries_concordant_n=False,
        min_n_count=None,
        max_n_count=None,
    )


def _summarize_multi_n(max_hyp: int) -> CandidateGeneratorResult:
    started = perf_counter()
    pairs = fast_multi_concordant_pairs(max_hyp)
    elapsed = perf_counter() - started
    n_counts = [len(ns) for ns in pairs.values()]
    return CandidateGeneratorResult(
        name="multi_n",
        max_hyp=max_hyp,
        pair_count=len(pairs),
        elapsed_s=elapsed,
        carries_concordant_n=True,
        min_n_count=min(n_counts) if n_counts else None,
        max_n_count=max(n_counts) if n_counts else None,
    )


def run_generator_benchmark(max_hyp: int) -> tuple[CandidateGeneratorResult, ...]:
    _validate_max_hyp(max_hyp)
    return (
        _count_iterator("all_coprime", max_hyp, iter_coprime_pairs(max_hyp)),
        _count_iterator("safe_coprime", max_hyp, iter_safe_coprime_pairs(max_hyp)),
        _summarize_multi_n(max_hyp),
    )


__all__ = [
    "CandidateGeneratorResult",
    "iter_coprime_pairs",
    "iter_safe_coprime_pairs",
    "run_generator_benchmark",
]
```

- [ ] **Step 4: Run the focused tests**

Run:

```bash
uv run pytest tests/test_candidate_generators.py -v
```

Expected: PASS, 4 tests.

- [ ] **Step 5: Run formatting and lint checks for touched Python files**

Run:

```bash
uv run ruff format src/rational_distance/concordant/candidate_generators.py tests/test_candidate_generators.py
uv run ruff check src/rational_distance/concordant/candidate_generators.py tests/test_candidate_generators.py
```

Expected: `ruff format` completes; `ruff check` prints `All checks passed!`.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/rational_distance/concordant/candidate_generators.py tests/test_candidate_generators.py
git commit -m "feat: add direct candidate generator benchmark helpers"
```

Expected: commit succeeds.

---

### Task 2: Add the benchmark CLI

**Files:**
- Create: `scripts/benchmark_candidate_generators.py`
- Test: `tests/test_candidate_generators.py`

- [ ] **Step 1: Add CLI smoke-test coverage**

Append this test to `tests/test_candidate_generators.py`:

```python

def test_cli_writes_json_summary(tmp_path) -> None:
    import json
    import subprocess
    import sys

    output_path = tmp_path / "candidate_generators_200.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/benchmark_candidate_generators.py",
            "--max-hyp",
            "200",
            "--json-out",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "all_coprime" in completed.stdout
    assert "safe_coprime" in completed.stdout
    assert "multi_n" in completed.stdout

    rows = json.loads(output_path.read_text(encoding="utf-8"))
    assert [row["name"] for row in rows] == ["all_coprime", "safe_coprime", "multi_n"]
    assert rows[2]["carries_concordant_n"] is True
```

- [ ] **Step 2: Run the CLI test to verify it fails**

Run:

```bash
uv run pytest tests/test_candidate_generators.py::test_cli_writes_json_summary -v
```

Expected: FAIL because `scripts/benchmark_candidate_generators.py` does not exist.

- [ ] **Step 3: Create the CLI script**

Create `scripts/benchmark_candidate_generators.py` with this full content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.candidate_generators import run_generator_benchmark  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark direct integer-domain candidate generators"
    )
    parser.add_argument("--max-hyp", type=int, default=2000)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write benchmark rows as JSON",
    )
    return parser.parse_args()


def _format_table(rows: object) -> str:
    result_rows = list(rows)
    lines = [
        "name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k",
        "------------  -------  ---------  ---------  ---------  -----  -----",
    ]
    for row in result_rows:
        min_k = "-" if row.min_n_count is None else str(row.min_n_count)
        max_k = "-" if row.max_n_count is None else str(row.max_n_count)
        lines.append(
            f"{row.name:<12}  "
            f"{row.max_hyp:>7}  "
            f"{row.pair_count:>9}  "
            f"{row.elapsed_s:>9.3f}  "
            f"{str(row.carries_concordant_n):>9}  "
            f"{min_k:>5}  "
            f"{max_k:>5}"
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    json_out = cast(Path | None, args.json_out)

    rows = run_generator_benchmark(max_hyp)
    print(_format_table(rows))

    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(
            json.dumps([row.to_json_dict() for row in rows], indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"json: {json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the CLI test**

Run:

```bash
uv run pytest tests/test_candidate_generators.py::test_cli_writes_json_summary -v
```

Expected: PASS.

- [ ] **Step 5: Run a small manual benchmark**

Run:

```bash
uv run python scripts/benchmark_candidate_generators.py --max-hyp 200 --json-out results/candidate_generators_max200.json
```

Expected: stdout contains rows for `all_coprime`, `safe_coprime`, and `multi_n`; JSON file is created at `results/candidate_generators_max200.json`.

- [ ] **Step 6: Run formatting and lint checks for touched Python files**

Run:

```bash
uv run ruff format scripts/benchmark_candidate_generators.py tests/test_candidate_generators.py
uv run ruff check scripts/benchmark_candidate_generators.py tests/test_candidate_generators.py
```

Expected: `ruff format` completes; `ruff check` prints `All checks passed!`.

- [ ] **Step 7: Commit**

Run:

```bash
git add scripts/benchmark_candidate_generators.py tests/test_candidate_generators.py results/candidate_generators_max200.json
git commit -m "feat: add candidate generator benchmark cli"
```

Expected: commit succeeds.

---

### Task 3: Run the experiment-line-B benchmark at bounded scales

**Files:**
- Create: `results/candidate_generators_max2000.json`
- Create: `results/candidate_generators_max10000.json`

- [ ] **Step 1: Run the 2k benchmark**

Run:

```bash
uv run python scripts/benchmark_candidate_generators.py --max-hyp 2000 --json-out results/candidate_generators_max2000.json
```

Expected: completes quickly and prints three rows.

- [ ] **Step 2: Inspect the 2k JSON**

Run:

```bash
python -m json.tool results/candidate_generators_max2000.json | head -80
```

Expected: formatted JSON with exactly three row objects named `all_coprime`, `safe_coprime`, and `multi_n`.

- [ ] **Step 3: Run the 10k benchmark**

Run:

```bash
uv run python scripts/benchmark_candidate_generators.py --max-hyp 10000 --json-out results/candidate_generators_max10000.json
```

Expected: completes without running PARI; based on existing worklogs, `multi_n` should be around 854 pairs and near second-level runtime, while all-coprime and safe-coprime counting may take longer because they iterate millions of gcd checks.

- [ ] **Step 4: Inspect the 10k JSON**

Run:

```bash
python -m json.tool results/candidate_generators_max10000.json | head -80
```

Expected: formatted JSON with exactly three row objects named `all_coprime`, `safe_coprime`, and `multi_n`.

- [ ] **Step 5: Verify known 10k multi-N count**

Run:

```bash
python - <<'PY'
import json
from pathlib import Path
rows = json.loads(Path('results/candidate_generators_max10000.json').read_text())
by_name = {row['name']: row for row in rows}
print(by_name['multi_n']['pair_count'])
assert by_name['multi_n']['pair_count'] == 854
PY
```

Expected: prints `854` and exits with status 0.

- [ ] **Step 6: Commit benchmark outputs**

Run:

```bash
git add results/candidate_generators_max2000.json results/candidate_generators_max10000.json
git commit -m "data: record candidate generator benchmark outputs"
```

Expected: commit succeeds.

---

### Task 4: Document the experiment result and domain distinction

**Files:**
- Create: `docs/work-logs/072-generator-first-candidate-benchmark.md`

- [ ] **Step 1: Generate the worklog from benchmark JSON**

Run:

````bash
python - <<'PY'
import json
from pathlib import Path


def table_for(path: Path) -> str:
    rows = json.loads(path.read_text())
    lines = [
        "name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k",
    ]
    for row in rows:
        min_k = "-" if row["min_n_count"] is None else str(row["min_n_count"])
        max_k = "-" if row["max_n_count"] is None else str(row["max_n_count"])
        lines.append(
            f"{row['name']:<12}  "
            f"{row['max_hyp']:>7}  "
            f"{row['pair_count']:>9}  "
            f"{row['elapsed_s']:>9.3f}  "
            f"{str(row['carries_concordant_n']):>9}  "
            f"{min_k:>5}  "
            f"{max_k:>5}"
        )
    return "\n".join(lines)


out = Path("docs/work-logs/072-generator-first-candidate-benchmark.md")
text = f"""# Worklog 072: Generator-first candidate benchmark

## Goal

Compare direct candidate generators over the integer coprime domain:

```text
1 <= A < B <= max_hyp
gcd(A, B) = 1
```

This is experiment line B. It is not the same search domain as the current `proof_status --max-hyp` triple-pair generator, where `max_hyp` bounds primitive Pythagorean triple hypotenuses rather than bounding `A` and `B` directly.

## Generators compared

```text
all_coprime   all reduced integer pairs with A,B <= max_hyp
safe_coprime  all_coprime filtered by safe_pair_sieve.allow_reduced_pair
multi_n       pivot-on-N generator fast_multi_concordant_pairs(max_hyp)
```

`multi_n` carries the concordant-N list by construction, so downstream benchmark variants using it do not need to run `concordant_search` or `multi_n_sieve` again for the generated pairs.

## Commands

```bash
uv run python scripts/benchmark_candidate_generators.py --max-hyp 2000 --json-out results/candidate_generators_max2000.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 10000 --json-out results/candidate_generators_max10000.json
```

## Results: max_hyp=2000

```text
{table_for(Path("results/candidate_generators_max2000.json"))}
```

## Results: max_hyp=10000

```text
{table_for(Path("results/candidate_generators_max10000.json"))}
```

## Interpretation

The direct `multi_n` generator is the strongest candidate generator in this integer-domain comparison because it emits only pairs with at least two concordant N values. At `max_hyp=10000`, existing worklog evidence expects 854 multi-N pairs, matching `results/multi_concordant_N_max10000.jsonl`.

The safe generator is still useful as a cheap front filter, but it does not encode concordant-N existence. It should be benchmarked separately from the current triple-pair `proof_status` domain because direct integer-domain counts and triple-pair-domain counts answer different questions.
"""
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(text, encoding="utf-8")
print(out)
PY
````

Expected: creates `docs/work-logs/072-generator-first-candidate-benchmark.md` from the recorded JSON benchmark outputs.

- [ ] **Step 2: Verify the worklog records the known 10k multi-N count**

Run:

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/work-logs/072-generator-first-candidate-benchmark.md').read_text()
assert 'multi_n         10000        854' in text
assert 'proof_status --max-hyp' in text
print('worklog records 10k multi-N count and domain distinction')
PY
```

Expected: prints `worklog records 10k multi-N count and domain distinction`.

- [ ] **Step 3: Commit the worklog**

Run:

```bash
git add docs/work-logs/072-generator-first-candidate-benchmark.md
git commit -m "docs: document generator-first candidate benchmark"
```

Expected: commit succeeds.

---

### Task 5: Final validation

**Files:**
- Read-only validation across created files.

- [ ] **Step 1: Run the focused Python tests**

Run:

```bash
uv run pytest tests/test_candidate_generators.py tests/test_fast_multi_n.py -v
```

Expected: PASS.

- [ ] **Step 2: Run lint checks for created Python files**

Run:

```bash
uv run ruff check src/rational_distance/concordant/candidate_generators.py scripts/benchmark_candidate_generators.py tests/test_candidate_generators.py
```

Expected: `All checks passed!`.

- [ ] **Step 3: Confirm benchmark outputs exist**

Run:

```bash
python - <<'PY'
from pathlib import Path
for path in [
    Path('results/candidate_generators_max200.json'),
    Path('results/candidate_generators_max2000.json'),
    Path('results/candidate_generators_max10000.json'),
]:
    assert path.exists(), path
    assert path.stat().st_size > 0, path
    print(path)
PY
```

Expected: prints the three result paths.

- [ ] **Step 4: Check git status**

Run:

```bash
git status --short
```

Expected: no uncommitted changes.

---

## Self-Review

- Spec coverage:
  - Direct integer-domain all-coprime generator is covered by Task 1.
  - Direct safe-sieve generator is covered by Task 1.
  - Existing pivot-on-N multi-N direct generator is benchmarked by Task 1 and exposed by Task 2.
  - Bounded 2k and 10k experiment runs are covered by Task 3.
  - Domain distinction from current triple-pair proof_status is documented in Task 4.

- Placeholder scan:
  - No zero-valued result rows are embedded in the plan.
  - No unresolved function names are used.

- Type consistency:
  - `CandidateGeneratorResult` fields match every script, test, and JSON access.
  - Generator names are consistently `all_coprime`, `safe_coprime`, and `multi_n`.
  - `max_hyp` consistently means direct integer bound `1 <= A < B <= max_hyp` for this experiment line.
