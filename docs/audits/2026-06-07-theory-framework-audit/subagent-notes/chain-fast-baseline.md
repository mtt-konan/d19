Slice:
chain-fast-baseline (baseline 搜索语义 / 边界 / near-miss / result storage)

Files inspected:
- docs/IMPLEMENTATION.md
- docs/PROJECT_STATUS.md
- docs/CURRENT_FINDINGS.md
- docs/archive/CHAIN_FAST_SAFE_FILTERS.md
- docs/archive/CHAIN_FAST_BUCKET_STATS.md
- docs/archive/CHAIN_FAST_MOD_SIEVE.md
- docs/archive/CHAIN_FAST_STRUCTURE_FINDINGS.md
- docs/archive/CHAIN_FAST_OPTIMIZATION.md
- docs/archive/CHAIN_FAST_PERFORMANCE.md
- docs/work-logs/archive/018-chain-fast-implementation.md
- docs/work-logs/archive/019-parity-filter-and-ec-analysis.md
- docs/work-logs/archive/020-ec-concordant-analysis-pipeline.md
- docs/work-logs/archive/021-chain-numpy-db.md
- docs/work-logs/archive/022-chain-fast-profile-cache.md
- docs/work-logs/archive/023-chain-fast-mod-sieve-experiment.md
- docs/work-logs/archive/024-chain-fast-100k-structure-findings.md
- docs/work-logs/archive/025-chain-fast-safe-pair-sieve.md
- docs/work-logs/041-parallel-pipeline-and-max-hyp-10k.md
- docs/work-logs/052-max-hyp-100k-scan-and-rank-audit.md
- docs/work-logs/064-parallel-map-reuse-and-benchmark.md
- src/rational_distance/chain_fast/__init__.py
- src/rational_distance/chain_fast/api.py
- src/rational_distance/chain_fast/bucket_stats.py
- src/rational_distance/chain_fast/kernel.py
- src/rational_distance/chain_fast/mod_sieve.py
- src/rational_distance/chain_fast/safe_pair_sieve.py
- src/rational_distance/chain_fast/workflow.py
- src/rational_distance/cli/search/chain_fast_runner.py
- src/rational_distance/cli/search/parser.py
- src/rational_distance/cli/search/output.py
- src/rational_distance/_legacy/chain_db.py
- src/rational_distance/_legacy/search_chain.py
- src/rational_distance/_legacy/search_chain_fast.py
- src/rational_distance/math_utils.py
- tests/test_chain_fast.py
- tests/test_chain_fast_cli.py
- results/README.md
- results/catalog.json
- results/chain.db schema and summary rows via read-only sqlite3

Commands run:
- `pwd`
- `git status --short`
- `rg --files docs src tests results`
- `rg -n "chain[-_ ]fast|baseline|proof|prove|prover|no solution|unsolved|not found|未找到|无解|max_hyp|near[- ]miss|result|catalog|sound|safe" ...`
- `rg -n "max_hyp|near|miss|result|catalog|numpy|np\.|int64|overflow|parity|even|odd|mod|safe|proof|prove|no solution|not found|baseline|hypotenuse|storage|json" ...`
- `nl -ba` / `sed -n` on the files listed above for line-number evidence
- `ls -l src/rational_distance/search_chain_fast.py`
- `ls -l src/rational_distance/chain_db.py src/rational_distance/chain_analysis.py src/rational_distance/search_chain.py`
- `sqlite3 -readonly results/chain.db ".schema chain_runs"`
- `sqlite3 -readonly results/chain.db ".schema chain_near_misses"`
- `sqlite3 -readonly results/chain.db "SELECT id,max_hyp,backend,status,found_count,near_miss_count,n_triples,last_t1_index,elapsed_s FROM chain_runs ORDER BY id DESC LIMIT 10;"`
- `uv run pytest tests/test_chain_fast.py tests/test_chain_fast_cli.py -q`

Claims checked:
- `chain-fast` 是否应被称为可信 bounded baseline 搜索器，而不是证明器。
- `max_hyp` 的含义是否清楚：限制本原勾股三元组斜边，不限制最终 `(a,b,c,d)` 边长。
- Python / numpy 后端在边界、溢出、平方检测和奇偶 / mod 条件上是否有明显不一致风险。
- `near-miss` 是否只是 C3-pass/C4-fail 的接近样本，而不是“解”或“反证”。
- 结果持久化是否会把“未找到”误写成“无解”，或把失败的 near-miss 存储误读成“没有 near-miss”。
- docs/IMPLEMENTATION.md、docs/PROJECT_STATUS.md、docs/CURRENT_FINDINGS.md 与当前代码 / 结果索引是否一致。

Fatal findings:
- None for this slice. I did not find evidence that current `chain-fast` should be called globally sound/unsound, and I did not find code that directly turns a bounded zero-hit search into a global proof.

High-risk findings:
- `results/chain.db` is a legacy chain-fast DB, but `results/README.md` still presents it as the top-level chain-fast SQLite result DB. Current code explicitly rejects legacy schemas: `_require_supported_schema()` rejects old chain tables without `chain_meta` in `src/rational_distance/_legacy/chain_db.py:71` and `src/rational_distance/_legacy/chain_db.py:89`. The README lists `chain.db` as the chain-fast result DB in `results/README.md:9`. Read-only schema evidence shows the DB only has old `chain_runs`, `chain_solutions`, `chain_near_misses`, and no `chain_meta` / `chain_triples` / profile fields:

```text
CREATE TABLE chain_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  max_hyp INTEGER NOT NULL,
  backend TEXT NOT NULL DEFAULT 'python',
  status TEXT NOT NULL DEFAULT 'running',
  ...
  n_triples INTEGER NOT NULL DEFAULT 0,
  found_count INTEGER NOT NULL DEFAULT 0,
  near_miss_count INTEGER NOT NULL DEFAULT 0
);
```

  The same DB has an old `max_hyp=40000, backend=numpy, status=running` row, while current code forces `backend='numpy'` to fail above `_NUMPY_MAX_HYP=36000` in `src/rational_distance/chain_fast/api.py:140` and `src/rational_distance/chain_fast/api.py:145`. If the main ledger cites `results/chain.db`, it should mark it legacy / historical, not current authoritative evidence.

- Large-range raw near-miss persistence is still unsafe in current code, not merely historical. Current schema stores `sq3`, `sq4`, `h3`, `h4`, and deficits as SQLite `INTEGER` in `src/rational_distance/_legacy/chain_db.py:168`, and `record_near_misses()` casts those fields to Python `int` before insertion in `src/rational_distance/_legacy/chain_db.py:442`. The 100k archive says the search completed but failed while writing near-misses with `OverflowError: Python int too large to convert to SQLite INTEGER` in `docs/archive/CHAIN_FAST_STRUCTURE_FINDINGS.md:149`; CURRENT_FINDINGS repeats the boundary in `docs/CURRENT_FINDINGS.md:137`. Because the runner records near-misses before `finish_run()` in `src/rational_distance/cli/search/chain_fast_runner.py:208`, such a run can complete computation but remain `running` / partially persisted. A later `--resume` starts from `last_t1_index + 1` in `src/rational_distance/cli/search/chain_fast_runner.py:117`; if that is already past the triple list, `run_chain_fast()` returns an empty execution in `src/rational_distance/chain_fast/api.py:211`, and `finish_run()` can then mark the run `done` using only rows that survived storage in `src/rational_distance/_legacy/chain_db.py:478`. This creates a real storage-semantics risk: "no stored near-miss rows" is not the same thing as "no near-misses were seen."

Medium/low findings:
- `docs/IMPLEMENTATION.md` is stale for chain-fast compatibility paths. It says top-level stubs like `src/rational_distance/search_chain_fast.py`, `src/rational_distance/search_chain.py`, `src/rational_distance/chain_db.py`, and `src/rational_distance/chain_analysis.py` still exist in `docs/IMPLEMENTATION.md:15` and `docs/IMPLEMENTATION.md:63`. In the current tree, those top-level files do not exist; the actual compatibility files are under `src/rational_distance/_legacy/`, and the main implementation is under `src/rational_distance/chain_fast/`. This is not a runtime bug for current tests, but it is a documentation mismatch for anyone following IMPLEMENTATION.md.
- `results/catalog.json` does not list `chain.db`, while `results/README.md` lists it as a top-level result. The catalog lists multi-concordant artifacts and `proof_status.db` in `results/catalog.json:1`, but no chain-fast DB artifact. This makes result storage provenance uneven: the README exposes a legacy chain-fast DB that the machine-readable catalog does not qualify.
- `--near-miss` CLI help says it logs to `--db` and "requires --db" in `src/rational_distance/cli/search/parser.py:319`, but the runner only enforces `--db` for `--bucket-stats` in `src/rational_distance/cli/search/chain_fast_runner.py:19`. Without `--db`, near-misses are counted through `_NearMissTopK` but not persisted because DB writes are inside `if db_conn is not None` in `src/rational_distance/cli/search/chain_fast_runner.py:196`. This is mostly UX / storage wording risk, not search correctness risk.
- `docs/PROJECT_STATUS.md:30` says `chain-fast` "已经证明了" direct exhaustive pair + engineering optimization can run stably. In context this reads like ordinary wording about engineering evidence, not a theorem, and later lines correctly call it baseline. Still, main claims should prefer "验证/显示它能稳定跑" over "证明" to avoid proof-language drift.
- Automated equivalence tests for safe/mod/numpy are small-range checks. Tests compare numpy vs Python at `max_hyp=300` in `tests/test_chain_fast.py:185`, forced numpy overflow guard in `tests/test_chain_fast.py:210`, mod-sieve preservation at `max_hyp=500` in `tests/test_chain_fast.py:571`, and safe-pair preservation at `max_hyp=500` in `tests/test_chain_fast.py:597`. This is reasonable for regression tests, but large-range claims still rely on documented runs, not broad formal proof.

Non-issues worth noting:
- The main project docs mostly use the right role: `PROJECT_STATUS` sets `chain-fast = baseline` in `docs/PROJECT_STATUS.md:14`, says it is a baseline / comparison path in `docs/PROJECT_STATUS.md:63`, and says future necessary conditions should be checked against it in `docs/PROJECT_STATUS.md:136`. `CURRENT_FINDINGS` calls it the most trusted baseline searcher in `docs/CURRENT_FINDINGS.md:104`.
- `proof_status` is correctly separated from `chain-fast`: `docs/IMPLEMENTATION.md:94` describes proof_status as cumulative pair-level proof workflow, and `docs/IMPLEMENTATION.md:120` explicitly says it is not a searcher and does not replace `chain-fast` / `concordant`.
- `max_hyp` generation has no obvious off-by-one leak in this slice. `build_chain_fast_triples()` uses `ceil(sqrt(max_hyp)) + 1` and filters `c <= max_hyp` in `src/rational_distance/chain_fast/api.py:135`; the shared generator includes both orientations in `src/rational_distance/math_utils.py:30`.
- numpy overflow is actively guarded. `_NUMPY_MAX_HYP = 36000` is documented in `src/rational_distance/chain_fast/api.py:37`; forced numpy raises above that line in `src/rational_distance/chain_fast/api.py:145`, while `auto` falls back to Python in `src/rational_distance/chain_fast/api.py:153`. Tests cover the forced guard in `tests/test_chain_fast.py:210`.
- numpy square hits are not trusted blindly. The vectorized path uses float sqrt with +/-1 checks, then re-verifies actual hits with Python `isqrt` before appending a solution in `src/rational_distance/chain_fast/kernel.py:151` and `src/rational_distance/chain_fast/kernel.py:263`. That reduces false-positive risk from float rounding.
- `safe_pair_sieve` and `mod_sieve` remain experimental and non-default. The CLI suppresses their help flags in `src/rational_distance/cli/search/parser.py:340`, and `safe_pair_sieve` is rejected unless the effective backend is Python in `src/rational_distance/chain_fast/api.py:183`.
- CLI output says "Found N unit-square 4-cycle solution(s)" in `src/rational_distance/cli/search/chain_fast_runner.py:240`; it does not print "proved no solution." Zero found should be read as bounded zero-hit search output.

Open uncertainties:
- I did not re-audit the mathematical derivation that every relevant unit-square 4-cycle appears from the ordered primitive-triple-pair construction; this note only checks the implementation/storage slice.
- I did not rerun the 100k chain-fast search. Large-range statements here rely on archived worklogs and current code inspection.
- I did not repair or migrate `results/chain.db`; it remains a legacy artifact in the working tree.
- I did not check every historical CHAIN_FAST archive line-by-line. I used keyword search across all `docs/archive/CHAIN_FAST_*.md` plus line-number reads of the relevant storage, numpy, safe-filter, mod-sieve, structure, and performance sections.

Recommended updates to main claim ledger:
- Use: "`chain-fast` is the trusted bounded baseline searcher / regression oracle for the direct unit-square 4-cycle search." Avoid: "`chain-fast` proves Harborth" or "`chain-fast` proves no solution" without a specific finite bound and method assumptions.
- State the bound explicitly: "`max_hyp` bounds primitive triple hypotenuses; output side values can be `O(max_hyp^2)`."
- Add a storage qualifier: "For large `max_hyp`, raw near-miss SQLite rows are not reliable unless large integer fields are stored as TEXT/BLOB/JSON or only aggregate samples are persisted."
- Mark `results/chain.db` as legacy or rebuild it under current schema before citing it. Do not treat the existing DB as current authoritative chain-fast evidence.
- Update docs/IMPLEMENTATION.md to point chain-fast DB / analysis compatibility files to `_legacy/` or remove the claim that top-level stubs still exist.
- Add a ledger note that `results/catalog.json` currently indexes proof-status and multi-N artifacts but not the chain-fast DB; either add a qualified chain-fast artifact entry or keep the README from implying cataloged authority.

Plain-language summary:
`chain-fast` 现在适合被叫作“可信的有限范围 baseline 搜索器”。它像一台很稳定的筛查机器：在给定 `max_hyp` 和运行配置里，逐个检查候选，没找到就只能说“这个范围没找到”，不能顺口升级成“全局无解”。代码对 numpy 溢出、平方复查、实验筛开关这些核心边界处理得比较谨慎。真正需要小心的是结果仓库：现有 `results/chain.db` 是旧库，和当前代码 schema 不匹配；大范围 near-miss 明细也会撞 SQLite 64-bit 整数上限。所以主台账应把 chain-fast 的数学/工程角色写清楚，并把旧 DB 与 near-miss 存储边界单独标红。
