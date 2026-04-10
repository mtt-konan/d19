# Copilot Instructions

## Commands

```bash
uv sync                              # install dependencies
uv run pytest                        # run all tests
uv run pytest tests/test_math_utils.py::test_rational_sqrt_perfect_squares  # single test
uv run python scripts/search_3vertex.py              # run search (default params)
uv run python scripts/search_3vertex.py --help       # all CLI options
uv run python scripts/search_4vertex.py              # same as --min-rational 4
```

No linter is configured. There is no build step (`package = false` in pyproject.toml).

## Architecture

The library lives in `src/rational_distance/` and is not installed as a package. Both scripts and tests add `src/` to `sys.path` manually:

```python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

**Data flow:**
1. `math_utils.py` generates primitive Pythagorean triples `(p, q, r)` — always both orientations `(p,q,r)` and `(q,p,r)`
2. `search.py` iterates triples × coprime pairs `(a,b)` to form rational points `P = (ap/br, aq/br)`
3. Distance rationality is checked purely with integer `isqrt` (no `Fraction` in hot loop)
4. `square.py`'s `RationalPoint` (frozen dataclass) is only constructed after a hit passes the integer filter
5. `scripts/search_3vertex.py` is the sole CLI entry point; `search_4vertex.py` just patches `sys.argv` and calls `main()`

**Multiprocessing pattern** (`search.py`):
- `_init_worker` + `_WORKER_PAIRS` global: the coprime-pair list is built once per worker process via `ProcessPoolExecutor(initializer=_init_worker, initargs=...)`. Do not call `gcd` in the inner loop.
- `_worker` must be a **module-level function** (not a lambda or nested def) — macOS uses `spawn` for multiprocessing, which requires picklability.

## Key Conventions

**`distances` tuple is always length 4**, ordered `(dA, dB, dC, dD)` matching `VERTICES` in `square.py`. `None` means irrational (not unknown). Indices: 0=A(0,0), 1=B(1,0), 2=C(1,1), 3=D(0,1).

**Both triple orientations are always emitted.** `primitive_pythagorean_triples` appends both `(a,b,c)` and `(b,a,c)`. This is intentional — it ensures symmetry between x and y coordinates is covered without needing separate anchor points for vertices B and D.

**Integer distance formula** — the core math that makes the search fast:

```
d(B)² rational  ⟺  (ar−bp)² + (bq)² is a perfect integer square
d(D)² rational  ⟺  (ar−bq)² + (bp)² is a perfect integer square
d(C)² rational  ⟺  (ar−b(p+q))² + (b(p−q))² is a perfect integer square
```

All checks use `s = isqrt(t); ok = s*s == t`.

**Deduplication happens twice**: once inside `_search_triple_int` (per-triple, via a `seen` set of reduced `(xn,xd,yn,yd)` tuples), and once globally in `parametric_search_fast` (across all triples, keyed by `(Fraction x, Fraction y)`). When merging, the entry with the higher `rational_count` wins.

**Raw dicts stay integers** — `_search_triple_int` returns `list[dict]` with raw `(numerator, denominator)` int tuples, not `Fraction`. The conversion to `RationalPoint` via `_raw_to_point` is deferred until after the parallel phase to avoid pickling `Fraction` objects across processes.
