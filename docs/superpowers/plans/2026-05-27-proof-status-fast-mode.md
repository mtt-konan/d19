# Proof Status Fast Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fast, observable `proof_status` route that prioritizes wall-clock speed for 20k/50k runs while reusing one DB path safely instead of creating throwaway databases.

**Architecture:** Keep the current full-audit SQLite workflow as the correctness-preserving path. Add a separate CPU-first `fast-core` pipeline that runs cheap/core sieves in parallel by chunk, returns only aggregate counts plus survivor pairs, and writes only the final survivor audit to SQLite. Add explicit DB reset handling that deletes the main DB plus SQLite sidecar files before a fresh run.

**Tech Stack:** Python 3.12, `multiprocessing` spawn pools through `rational_distance.parallel`, SQLite, pytest, existing `rational_distance.proof_status` methods.

---

## Context and Constraints

- Current `process_pairs_parallel()` is audit-first: every pair returns a full `PairComputeResult`, then the main process writes `pair_method_attempts` and `pair_proof_status` row-by-row.
- At `max_hyp=20000`, this means about 10,090,806 pair-level results and 20M+ SQLite operations.
- `commit_every` reduces commit frequency but does not reduce per-row `execute`, JSON serialization, inter-process result traffic, or SQLite index maintenance.
- `--progress-every` in the current path adds work to the main-process hot loop and can slow runs.
- Historical core-only benchmark at `max_hyp=20000` established the target shape: core sieve can finish much faster than full audit and leaves 1,361 survivors under the standard core order.
- Preserve the existing default full-audit behavior unless a new explicit mode is selected.
- Avoid requiring new DB filenames for every benchmark. `--force` should reset the chosen DB path in place.

---

## File Structure

### Create

- `src/rational_distance/proof_status/fast_core.py`
  - Owns the CPU-first chunk worker and result dataclasses.
  - Has no SQLite dependency.
  - Provides a narrow API that accepts pairs and returns aggregate counts plus survivors.

- `tests/test_proof_status_fast_core.py`
  - Unit tests for fast-core behavior, chunk aggregation, and survivor selection.

- `tests/test_prove_no_solution_reset_db.py`
  - CLI-level tests for `--force` / reset DB behavior, including `-wal` and `-shm` sidecars.

- `tests/test_prove_no_solution_fast_mode.py`
  - CLI-level tests for `--fast-core`, proving it avoids full per-pair audit writes and then audits only survivors.

### Modify

- `scripts/prove_no_solution.py`
  - Add `--fast-core` CLI flag.
  - Strengthen `--force` to delete `db`, `db-wal`, and `db-shm` before connecting.
  - Print phase-level progress that is not tied to every pair.
  - Route `--fast-core --max-hyp` to `fast_core` first, then audit only survivors.

- `src/rational_distance/proof_status/workflow.py`
  - Keep current full-audit functions.
  - Add a small `process_pairs_parallel_summary()` helper only if needed by CLI tests; do not mix fast-core logic into this file.

- `src/rational_distance/proof_status/methods.py`
  - Keep `set_moduli_preset()` environment-variable implementation so spawn workers can read the selected preset.
  - Optionally add a focused test proving worker-visible moduli preset; do not use module globals for cross-process state.

---

## Public CLI Design

### Full-audit mode, existing behavior

```bash
uv run python scripts/prove_no_solution.py \
  --db results/proof_status.sqlite3 \
  --max-hyp 20000 \
  --workers 6 \
  --force
```

Behavior:

- Deletes `results/proof_status.sqlite3`, `results/proof_status.sqlite3-wal`, `results/proof_status.sqlite3-shm` if present.
- Creates the DB at the same path.
- Runs the existing full-audit workflow.

### Fast-core mode, new speed path

```bash
uv run python scripts/prove_no_solution.py \
  --db results/proof_status.sqlite3 \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --force
```

Behavior:

1. Deletes existing DB and sidecars if `--force` is set.
2. Materializes pairs for max-hyp parallel runs only if this is still faster on Mac.
3. Runs `fast_core` in chunks.
4. Prints phase-level progress per chunk, not per pair.
5. Writes full audit only for survivors.
6. Prints both core summary and final DB report.

Expected fast-core output shape:

```text
========================================================================
Proof-status workflow — DB: results/proof_status.sqlite3
  mode:             fast-core
  pairs to process: 10090806 (materialized from max_hyp=20000)
  workers:          6
  moduli:           standard (14 个)
========================================================================
[phase] fast-core start pairs=10090806 workers=6 chunk_size=50000
[phase] fast-core done checked=10090806 no_solution=10089445 survivors=1361 elapsed=...
[phase] survivor audit start pairs=1361
[phase] survivor audit done hard_case=1361 elapsed=...
```

---

## Task 1: Make `--force` Reset the Same DB Path Correctly

**Files:**
- Modify: `scripts/prove_no_solution.py`
- Test: `tests/test_prove_no_solution_reset_db.py`

- [ ] **Step 1: Write failing test for DB sidecar reset**

Create `tests/test_prove_no_solution_reset_db.py`:

```python
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_force_removes_db_and_sqlite_sidecars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    db.write_text("old db")
    db.with_name(db.name + "-wal").write_text("old wal")
    db.with_name(db.name + "-shm").write_text("old shm")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--pair",
            "1,5",
            "--serial",
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    assert db.exists()
    assert not db.with_name(db.name + "-wal").exists()
    assert not db.with_name(db.name + "-shm").exists()

    conn = sqlite3.connect(db)
    total = conn.execute("SELECT COUNT(*) FROM pair_proof_status").fetchone()[0]
    assert total == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_prove_no_solution_reset_db.py -q
```

Expected: fail if sidecars are not removed or stale DB content causes schema/open errors.

- [ ] **Step 3: Implement reset helper**

In `scripts/prove_no_solution.py`, add this helper near `_parse_pair()`:

```python
def _reset_sqlite_db(db_path: Path) -> None:
    for path in (
        db_path,
        db_path.with_name(db_path.name + "-wal"),
        db_path.with_name(db_path.name + "-shm"),
    ):
        if path.exists():
            path.unlink()
```

Replace current force block:

```python
# --force: 删除旧库重建
if args.force and db_path.exists():
    db_path.unlink()
```

with:

```python
if args.force:
    _reset_sqlite_db(db_path)
```

- [ ] **Step 4: Run reset test**

Run:

```bash
uv run pytest tests/test_prove_no_solution_reset_db.py -q
```

Expected: pass.

- [ ] **Step 5: Run existing CLI-related tests**

Run:

```bash
uv run pytest tests/test_prove_no_solution_batches.py tests/test_proof_status_executor_prescan.py -q
```

Expected: pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/prove_no_solution.py tests/test_prove_no_solution_reset_db.py
git commit -m "fix: reset proof status sqlite database in place"
```

---

## Task 2: Add Pure Fast-Core Worker API

**Files:**
- Create: `src/rational_distance/proof_status/fast_core.py`
- Test: `tests/test_proof_status_fast_core.py`

- [ ] **Step 1: Write failing tests for fast-core chunk behavior**

Create `tests/test_proof_status_fast_core.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_evaluate_core_chunk_returns_only_survivors(monkeypatch) -> None:
    from rational_distance.proof_status import fast_core
    from rational_distance.proof_status.types import MethodResult

    def fake_safe(A: int, B: int) -> MethodResult:
        if A == 1:
            return MethodResult("safe_sieve", "no_solution")
        return MethodResult("safe_sieve", "pass")

    def fake_chain(A: int, B: int) -> MethodResult:
        if A == 2:
            return MethodResult("chain_closure_mod_sieve", "no_solution")
        return MethodResult("chain_closure_mod_sieve", "pass")

    def fake_factor(A: int, B: int) -> MethodResult:
        if A == 3:
            return MethodResult("factor_concordant", "no_solution")
        return MethodResult(
            "factor_concordant",
            "inconclusive",
            details={"concordant_n_count": 1, "chain_compatible_count": 0},
        )

    monkeypatch.setattr(fast_core.proof_methods, "run_safe_sieve", fake_safe)
    monkeypatch.setattr(fast_core.proof_methods, "run_chain_closure_mod_sieve", fake_chain)
    monkeypatch.setattr(fast_core.proof_methods, "run_factor_concordant", fake_factor)

    result = fast_core.evaluate_core_chunk(((1, 5), (2, 7), (3, 11), (4, 13)))

    assert result.checked == 4
    assert result.no_solution == 3
    assert result.survivors == ((4, 13),)


def test_merge_core_results_combines_counts_and_survivors() -> None:
    from rational_distance.proof_status.fast_core import CoreChunkResult, merge_core_results

    merged = merge_core_results(
        [
            CoreChunkResult(checked=2, no_solution=1, survivors=((1, 5),)),
            CoreChunkResult(checked=3, no_solution=2, survivors=((7, 45),)),
        ]
    )

    assert merged.checked == 5
    assert merged.no_solution == 3
    assert merged.survivors == ((1, 5), (7, 45))
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/test_proof_status_fast_core.py -q
```

Expected: fail with `ImportError` because `fast_core.py` does not exist.

- [ ] **Step 3: Implement `fast_core.py`**

Create `src/rational_distance/proof_status/fast_core.py`:

```python
from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from rational_distance.proof_status import methods as proof_methods


Pair = tuple[int, int]


@dataclass(frozen=True)
class CoreChunkResult:
    checked: int
    no_solution: int
    survivors: tuple[Pair, ...]


def evaluate_core_pair(A: int, B: int) -> bool:
    safe = proof_methods.run_safe_sieve(A, B)
    if safe.outcome == "no_solution":
        return False

    chain = proof_methods.run_chain_closure_mod_sieve(A, B)
    if chain.outcome == "no_solution":
        return False

    factor = proof_methods.run_factor_concordant(A, B)
    if factor.outcome == "no_solution":
        return False

    return True


def evaluate_core_chunk(pairs: Sequence[Pair]) -> CoreChunkResult:
    survivors: list[Pair] = []
    no_solution = 0
    for A, B in pairs:
        if evaluate_core_pair(A, B):
            survivors.append((A, B))
        else:
            no_solution += 1
    return CoreChunkResult(
        checked=len(pairs),
        no_solution=no_solution,
        survivors=tuple(survivors),
    )


def merge_core_results(results: Iterable[CoreChunkResult]) -> CoreChunkResult:
    checked = 0
    no_solution = 0
    survivors: list[Pair] = []
    for result in results:
        checked += result.checked
        no_solution += result.no_solution
        survivors.extend(result.survivors)
    return CoreChunkResult(
        checked=checked,
        no_solution=no_solution,
        survivors=tuple(survivors),
    )
```

- [ ] **Step 4: Run tests**

Run:

```bash
uv run pytest tests/test_proof_status_fast_core.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
git add src/rational_distance/proof_status/fast_core.py tests/test_proof_status_fast_core.py
git commit -m "feat: add pure fast core proof status evaluator"
```

---

## Task 3: Add Chunked Fast-Core Parallel Runner

**Files:**
- Modify: `src/rational_distance/proof_status/fast_core.py`
- Test: `tests/test_proof_status_fast_core.py`

- [ ] **Step 1: Add tests for chunking and parallel runner hook**

Append to `tests/test_proof_status_fast_core.py`:

```python

def test_iter_chunks_splits_pairs() -> None:
    from rational_distance.proof_status.fast_core import iter_chunks

    assert list(iter_chunks([(1, 2), (3, 4), (5, 6)], 2)) == [
        ((1, 2), (3, 4)),
        ((5, 6),),
    ]


def test_run_fast_core_uses_parallel_map(monkeypatch) -> None:
    from rational_distance.proof_status import fast_core

    calls = []

    def fake_parallel_map(fn, items, *, workers, chunksize, on_result, ordered, collect_results):
        calls.append(
            {
                "workers": workers,
                "chunksize": chunksize,
                "ordered": ordered,
                "collect_results": collect_results,
            }
        )
        results = []
        for item in items:
            result = fn(item)
            results.append(result)
            if on_result is not None:
                on_result(result)
        return results

    monkeypatch.setattr(fast_core, "parallel_map", fake_parallel_map)
    monkeypatch.setattr(fast_core, "evaluate_core_chunk", lambda chunk: fast_core.CoreChunkResult(len(chunk), len(chunk), ()))

    result = fast_core.run_fast_core(
        [(1, 5), (2, 7), (3, 11)],
        workers=2,
        pair_chunk_size=2,
        pool_chunksize=1,
    )

    assert result.checked == 3
    assert result.no_solution == 3
    assert result.survivors == ()
    assert calls == [{"workers": 2, "chunksize": 1, "ordered": False, "collect_results": True}]
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
uv run pytest tests/test_proof_status_fast_core.py -q
```

Expected: fail because `iter_chunks` and `run_fast_core` do not exist.

- [ ] **Step 3: Implement chunk runner**

Modify `src/rational_distance/proof_status/fast_core.py`:

```python
from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import islice

from rational_distance.parallel import parallel_map
```

Add below `merge_core_results()`:

```python
def iter_chunks(pairs: Iterable[Pair], chunk_size: int) -> Iterator[tuple[Pair, ...]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    iterator = iter(pairs)
    while True:
        chunk = tuple(islice(iterator, chunk_size))
        if not chunk:
            return
        yield chunk


def run_fast_core(
    pairs: Iterable[Pair],
    *,
    workers: int,
    pair_chunk_size: int = 50_000,
    pool_chunksize: int = 1,
    on_chunk: Callable[[CoreChunkResult], None] | None = None,
) -> CoreChunkResult:
    results = parallel_map(
        evaluate_core_chunk,
        iter_chunks(pairs, pair_chunk_size),
        workers=workers,
        chunksize=pool_chunksize,
        on_result=on_chunk,
        ordered=False,
        collect_results=True,
    )
    return merge_core_results(results)
```

- [ ] **Step 4: Run tests**

Run:

```bash
uv run pytest tests/test_proof_status_fast_core.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
git add src/rational_distance/proof_status/fast_core.py tests/test_proof_status_fast_core.py
git commit -m "feat: run proof status fast core in chunks"
```

---

## Task 4: Add CLI `--fast-core` Mode

**Files:**
- Modify: `scripts/prove_no_solution.py`
- Test: `tests/test_prove_no_solution_fast_mode.py`

- [ ] **Step 1: Write failing CLI test**

Create `tests/test_prove_no_solution_fast_mode.py`:

```python
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_cli_fast_core_audits_only_survivors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from rational_distance.proof_status.fast_core import CoreChunkResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"

    def fake_generate(max_hyp: int):
        assert max_hyp == 100
        return [(1, 5), (2, 7), (7, 45)]

    def fake_run_fast_core(pairs, *, workers, pair_chunk_size, pool_chunksize, on_chunk):
        assert list(pairs) == [(1, 5), (2, 7), (7, 45)]
        result = CoreChunkResult(checked=3, no_solution=2, survivors=((7, 45),))
        if on_chunk is not None:
            on_chunk(result)
        return result

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--force",
            "--no-progress",
        ],
    )

    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module

    monkeypatch.setattr(pair_module, "generate_ab_pairs", fake_generate)
    monkeypatch.setattr(fast_core_module, "run_fast_core", fake_run_fast_core)

    cli.main()

    out = capsys.readouterr().out
    assert "mode:             fast-core" in out
    assert "fast-core done checked=3 no_solution=2 survivors=1" in out

    conn = sqlite3.connect(db)
    total = conn.execute("SELECT COUNT(*) FROM pair_proof_status").fetchone()[0]
    assert total == 1
```

- [ ] **Step 2: Run test to verify failure**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py -q
```

Expected: fail because `--fast-core` does not exist.

- [ ] **Step 3: Add CLI arguments**

In `scripts/prove_no_solution.py`, add after `--force`:

```python
parser.add_argument(
    "--fast-core",
    action="store_true",
    help="快速核心筛模式：全量只跑核心筛，不写全量审计；只对疑难对写完整 proof_status。",
)
parser.add_argument(
    "--pair-chunk-size",
    type=int,
    default=50_000,
    help="--fast-core 每个 worker 任务包含的 pair 数量。",
)
```

- [ ] **Step 4: Import modules in a monkeypatch-friendly way**

Replace:

```python
from rational_distance.concordant.pairs import generate_ab_pairs, iter_ab_pairs
from rational_distance.proof_status import schema, workflow
```

with:

```python
from rational_distance.concordant import pairs as pair_module
from rational_distance.proof_status import fast_core, schema, workflow
```

Then update use sites:

```python
pairs = pair_module.generate_ab_pairs(args.max_hyp)
```

and:

```python
pairs = pair_module.iter_ab_pairs(args.max_hyp)
```

- [ ] **Step 5: Add fast-core branch before full-audit branch**

After the header print and before `if workers > 1:`, insert:

```python
if args.fast_core:
    if not args.max_hyp:
        raise SystemExit("--fast-core requires --max-hyp")
    if workers <= 1:
        raise SystemExit("--fast-core requires --workers > 1")

    print(
        f"[phase] fast-core start pairs={len(pairs)} workers={workers} "
        f"chunk_size={args.pair_chunk_size}",
        flush=True,
    )
    core_started = time.perf_counter()

    def _on_core_chunk(chunk_result) -> None:
        return

    core_result = fast_core.run_fast_core(
        pairs,
        workers=workers,
        pair_chunk_size=args.pair_chunk_size,
        pool_chunksize=1,
        on_chunk=_on_core_chunk,
    )
    core_elapsed = time.perf_counter() - core_started
    print(
        f"[phase] fast-core done checked={core_result.checked} "
        f"no_solution={core_result.no_solution} survivors={len(core_result.survivors)} "
        f"elapsed={core_elapsed:.1f}s",
        flush=True,
    )

    print(f"[phase] survivor audit start pairs={len(core_result.survivors)}", flush=True)
    audit_started = time.perf_counter()
    workflow.process_pairs_parallel(
        conn,
        core_result.survivors,
        workers=workers,
        commit_every=args.commit_every,
        skip_terminal=False,
        on_result=_on_result,
    )
    audit_elapsed = time.perf_counter() - audit_started
    print(f"[phase] survivor audit done elapsed={audit_elapsed:.1f}s", flush=True)
else:
    # existing workers > 1 / serial branches move under this else
```

When applying this step, indent the existing full-audit `if workers > 1:` and serial `else:` under the new `else:`.

- [ ] **Step 6: Run fast-mode test**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py -q
```

Expected: pass.

- [ ] **Step 7: Run CLI regression tests**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py tests/test_prove_no_solution_reset_db.py tests/test_prove_no_solution_batches.py -q
```

Expected: pass.

- [ ] **Step 8: Commit**

```bash
git add scripts/prove_no_solution.py tests/test_prove_no_solution_fast_mode.py
git commit -m "feat: add fast core proof status CLI mode"
```

---

## Task 5: Add Optional Fast-Core Summary File

**Files:**
- Modify: `scripts/prove_no_solution.py`
- Test: `tests/test_prove_no_solution_fast_mode.py`

- [ ] **Step 1: Add failing test for JSON summary**

Append to `tests/test_prove_no_solution_fast_mode.py`:

```python

def test_cli_fast_core_writes_summary_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import json

    from rational_distance.proof_status.fast_core import CoreChunkResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    summary = tmp_path / "summary.json"

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)

    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module

    monkeypatch.setattr(pair_module, "generate_ab_pairs", lambda _max_hyp: [(1, 5), (7, 45)])
    monkeypatch.setattr(
        fast_core_module,
        "run_fast_core",
        lambda pairs, **kwargs: CoreChunkResult(
            checked=2,
            no_solution=1,
            survivors=((7, 45),),
        ),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--fast-summary-json",
            str(summary),
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    payload = json.loads(summary.read_text())
    assert payload["checked"] == 2
    assert payload["no_solution"] == 1
    assert payload["survivor_count"] == 1
    assert payload["survivors"] == [[7, 45]]
```

- [ ] **Step 2: Run test to verify failure**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py::test_cli_fast_core_writes_summary_json -q
```

Expected: fail because `--fast-summary-json` does not exist.

- [ ] **Step 3: Add argument**

In `scripts/prove_no_solution.py`, add near `--fast-core`:

```python
parser.add_argument(
    "--fast-summary-json",
    type=Path,
    default=None,
    help="--fast-core: write aggregate summary and survivors to this JSON file.",
)
```

- [ ] **Step 4: Write summary after fast-core phase**

Import `json` at the top of `scripts/prove_no_solution.py`.

After `core_result` is computed, add:

```python
if args.fast_summary_json is not None:
    args.fast_summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.fast_summary_json.write_text(
        json.dumps(
            {
                "checked": core_result.checked,
                "no_solution": core_result.no_solution,
                "survivor_count": len(core_result.survivors),
                "survivors": [list(pair) for pair in core_result.survivors],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
```

- [ ] **Step 5: Run test**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py::test_cli_fast_core_writes_summary_json -q
```

Expected: pass.

- [ ] **Step 6: Run all fast-mode tests**

Run:

```bash
uv run pytest tests/test_prove_no_solution_fast_mode.py -q
```

Expected: pass.

- [ ] **Step 7: Commit**

```bash
git add scripts/prove_no_solution.py tests/test_prove_no_solution_fast_mode.py
git commit -m "feat: write fast core proof status summary"
```

---

## Task 6: Add Practical Benchmark Commands and Validation Gate

**Files:**
- Modify: `docs/superpowers/plans/2026-05-27-proof-status-fast-mode.md` only if results need recording.
- No code changes required.

- [ ] **Step 1: Run focused tests**

Run:

```bash
uv run pytest \
  tests/test_proof_status_fast_core.py \
  tests/test_prove_no_solution_fast_mode.py \
  tests/test_prove_no_solution_reset_db.py \
  tests/test_proof_status_executor_prescan.py \
  tests/test_prove_no_solution_batches.py \
  -q
```

Expected: all pass.

- [ ] **Step 2: Run core regression tests**

Run:

```bash
uv run pytest tests/test_proof_status.py tests/test_ab_sieve_benchmark.py tests/test_concordant.py -q
```

Expected: all pass.

- [ ] **Step 3: Run 10k fast-core smoke benchmark**

Run:

```bash
/usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_bench.sqlite3 \
  --max-hyp 10000 \
  --workers 6 \
  --fast-core \
  --force \
  --fast-summary-json results/proof_status_fast_10k_summary.json
```

Expected:

- Uses the same DB path each run.
- Summary JSON exists.
- DB contains only survivor audit rows, not 2.5M rows.
- Wall time is substantially below full-audit 10k.

Validate:

```bash
sqlite3 /tmp/proof_status_bench.sqlite3 "SELECT COUNT(*) FROM pair_proof_status"
```

Expected: close to the survivor count under the chosen core definition.

- [ ] **Step 4: Run 20k fast-core benchmark**

Run:

```bash
/usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_bench.sqlite3 \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --force \
  --fast-summary-json results/proof_status_fast_20k_summary.json
```

Expected:

- No new DB files except `/tmp/proof_status_bench.sqlite3` and transient SQLite sidecars.
- Sidecars are cleaned by next `--force` run.
- Summary survivor count should be near 1,361 with standard moduli.
- Wall time should be much closer to core-only benchmark than full-audit 191s.

- [ ] **Step 5: Commit benchmark result notes if requested**

If the benchmark is accepted, create or update a worklog. Use a concise title such as:

```bash
git add results/proof_status_fast_20k_summary.json docs/work-logs/<new-worklog>.md
git commit -m "docs: record proof status fast core benchmark"
```

Only commit result artifacts if the user explicitly wants them kept.

---

## Task 7: Optional Follow-Up — Sharded Full Audit Mode

Do this only if the user still needs full audit rows for every pair at 20k/50k.

**Files:**
- Create: `src/rational_distance/proof_status/sharded_audit.py`
- Create: `tests/test_proof_status_sharded_audit.py`
- Modify: `scripts/prove_no_solution.py`

Design:

- Split input pairs into N shards.
- Each worker writes its own SQLite shard file.
- Main process does not receive every `PairComputeResult`.
- Merge shard DBs after completion.

This is intentionally not part of the first implementation because fast-core gives the highest expected speedup with less risk.

---

## Self-Review

### Spec Coverage

- Fastest possible path: covered by Tasks 2-4.
- Avoid creating many DBs: covered by Task 1 and repeated benchmark commands using the same `/tmp/proof_status_bench.sqlite3` path.
- Progress without hot-loop slowdown: covered by phase-level output in Task 4.
- Refactor into smaller files: covered by new `fast_core.py`.
- Preserve existing behavior: full-audit path remains default.
- Support future full audit performance: optional Task 7.

### Placeholder Scan

No `TBD`, `TODO`, or undefined placeholders are used in implementation steps. Optional Task 7 is explicitly scoped as a follow-up and not required for the first deliverable.

### Type Consistency

- `CoreChunkResult.checked`, `no_solution`, and `survivors` are used consistently across tests and implementation.
- `Pair = tuple[int, int]` is used consistently.
- CLI argument names are `--fast-core`, `--pair-chunk-size`, and `--fast-summary-json`.
- Reset helper is `_reset_sqlite_db(db_path: Path) -> None`.

---

## Recommended Execution Order

1. Task 1: DB reset first, because it removes current benchmark friction immediately.
2. Task 2: pure fast-core evaluator.
3. Task 3: chunked parallel fast-core runner.
4. Task 4: CLI integration.
5. Task 5: summary JSON.
6. Task 6: validation benchmarks.
7. Task 7 only if full audit is still required.
