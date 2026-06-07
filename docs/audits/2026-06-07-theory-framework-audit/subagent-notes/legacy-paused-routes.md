Slice:
legacy-paused-routes: parametric / ec / chain paused routes.

Files inspected:
- README.md
- docs/DIRECTIONS.md
- docs/PROJECT_STATUS.md
- docs/IMPLEMENTATION.md
- docs/archive/SEARCH_METHODS.md
- docs/archive/METHOD_COMPARISON.md
- docs/work-logs/archive/README.md
- docs/work-logs/archive/001-initial-parametric-search.md
- docs/work-logs/archive/002-numpy-vectorization.md
- docs/work-logs/archive/004-side-exclusion-filter.md
- docs/work-logs/archive/005-gpu-search.md
- docs/work-logs/archive/006-int64-overflow-fix.md
- docs/work-logs/archive/007-pytorch-astype-fix.md
- docs/work-logs/archive/010-ec-search-foundation.md
- docs/work-logs/archive/012-ec-vectorization-gpu.md
- docs/work-logs/archive/013-parametric-shared-core.md
- docs/work-logs/archive/014-ec-db-analysis.md
- docs/work-logs/archive/014-pythagorean-chain-search.md
- docs/work-logs/archive/015-cross-product-family-exclusion.md
- docs/work-logs/archive/017-chain-reduction-math.md
- docs/work-logs/archive/018-chain-fast-implementation.md
- docs/work-logs/archive/019-parity-filter-and-ec-analysis.md
- docs/work-logs/archive/020-ec-concordant-analysis-pipeline.md
- docs/work-logs/archive/023-chain-fast-mod-sieve-experiment.md
- docs/work-logs/archive/024-chain-fast-100k-structure-findings.md
- docs/work-logs/archive/025-chain-fast-safe-pair-sieve.md
- docs/work-logs/028-proof-status-pipeline.md
- docs/work-logs/029-legacy-stub-cleanup.md
- docs/work-logs/033-dual-ec-probe.md
- docs/work-logs/034-hypotenuse-identity.md
- docs/work-logs/035-pari-selmer-api.md
- docs/work-logs/036-compute-rank-fix-and-ell2cover-batch.md
- docs/work-logs/037-finite-descent-on-hard-cases.md
- docs/work-logs/040-chain-closure-mod-sieve.md
- docs/work-logs/041-parallel-pipeline-and-max-hyp-10k.md
- docs/work-logs/043-post-wl042-direction-map.md
- docs/work-logs/053-round2-archive-src-legacy.md
- src/rational_distance/_legacy/*.py
- src/rational_distance/ec_search/*.py
- src/rational_distance/cli/search/*runner.py
- tests/test_parametric.py
- tests/test_ec.py
- tests/test_chain.py
- tests/test_cli.py
- results/archive/pattern_hunt_summary.txt
- results/archive/dual_ec_probe.jsonl
- results/archive/finite_descent_layer2.jsonl

Commands run:
- `pwd`
- `git status --short`
- `rg --files` over requested docs/source/test/result patterns
- `find docs/work-logs -maxdepth 2 -type f -name '*.md' | sort`
- `find results/archive -maxdepth 2 -type f | sort`
- `rg -n "parametric|elliptic|ec|chain|paused|legacy|archive|failed|bug|rank|result|route|method" ...`
- `nl -ba ... | sed -n ...` for cited evidence lines
- `test -e docs/SEARCH_METHODS.md`
- `test -e docs/METHOD_COMPARISON.md`
- `uv run pytest tests/test_parametric.py tests/test_ec.py tests/test_chain.py tests/test_cli.py -q`

Claims checked:
- Claim: `parametric` / `ec` / `chain` are paused, not deleted or mathematically ruled out.
- Claim: `paused` is an engineering and focus status, not a proof of route death.
- Claim: old worklogs and archived docs are historical evidence, not current authority.
- Claim: old parametric GPU/int64/PyTorch bugs should not be used to dismiss the route today.
- Claim: three-vertex `ec` should not be confused with later concordant/dual-EC rank diagnostics.
- Claim: `chain` is mostly rectangle / 4-cycle structure now, while `chain-fast` is the square-problem baseline.
- Claim: negative experiments such as no hits in bounded searches, rank-filter failure, and blocker-prime failure are bounded or idea-specific, not global impossibility claims.

Fatal findings:
- None in this slice.

High-risk findings:
- None found that would force changing the main paused-route claim.
- The main claim "parametric / ec / chain are paused rather than dead" is supported by current docs and tests. Current docs say `paused` routes are retained and not the main focus: README.md:5-10, docs/DIRECTIONS.md:5-10, docs/PROJECT_STATUS.md:14-24, docs/archive/SEARCH_METHODS.md:14-19.

Medium/low findings:
- Medium: README links two archived method docs as if they still live at top-level `docs/`. README.md:74-75 points to `docs/SEARCH_METHODS.md` and `docs/METHOD_COMPARISON.md`, but both paths are absent in the current filesystem; docs/DIRECTIONS.md:36 correctly points readers to `docs/archive/SEARCH_METHODS.md` as archived reference. This is not a math issue, but it can make a reader miss the "archived, reference only" status and over-trust old method-comparison wording.
- Medium: docs/PROJECT_STATUS.md has one broad sentence that can be misread as "local sieves cannot prove no-solution for any pair." It says current local sieves can reduce space but "不能证明无解" at docs/PROJECT_STATUS.md:230-235. Later the same document states chain-closure mod p^2 is an unconditional pair-level obstruction with 0 false kills at docs/PROJECT_STATUS.md:413-421. The safe ledger wording should be: these sieves do not prove the global Harborth problem unsolvable, but some do prove individual `(A,B)` pairs impossible.
- Low: `ec` naming remains easy to confuse. docs/DIRECTIONS.md:68-70 defines paused `ec` as a three-vertex seed/orbit route. docs/PROJECT_STATUS.md:259-266 and docs/work-logs/033-dual-ec-probe.md:1-8 discuss dual/concordant EC rank probes on chain near-misses. Those are related mathematical tools but not the same paused CLI route. Any ledger claim saying "EC failed" should specify which EC layer failed.
- Low: `_legacy` and `deprecated` wording can sound like "mathematically dead" even though it is mostly repo zoning. docs/IMPLEMENTATION.md:217-220 says `_legacy/` should receive no new code but still has real callers. docs/work-logs/053-round2-archive-src-legacy.md:126-132 says old tests still cover `_legacy/` and are useful as regression tests. Prefer "legacy implementation / compatibility zone" over "dead route" in the main ledger.

Non-issues worth noting:
- The core status docs already frame paused as focus/priority. README.md:10 says parametric/ec/chain are retained as research tools and background routes. docs/PROJECT_STATUS.md:97 says they still have value for validation, seeds, and structure understanding, while docs/PROJECT_STATUS.md:130-137 explains the current priority is concordant plus chain-fast baseline.
- `parametric` was not paused because its old GPU bugs remain unaddressed. The old known issue is real in wl005/wl006/wl007: GPU int64 overflow and PyTorch `.astype()` issues are documented at docs/work-logs/archive/005-gpu-search.md:35, docs/work-logs/archive/006-int64-overflow-fix.md:34-48, and docs/work-logs/archive/007-pytorch-astype-fix.md:10-12. Current code centralizes exact verification and fallback in `parametric_core`: src/rational_distance/_legacy/parametric_core.py:1-6 and src/rational_distance/_legacy/search_gpu.py:13-16. The tests explicitly check CPU/GPU-numpy consistency and forced exact fallback: tests/test_parametric.py:285-331.
- `ec` remains a real three-vertex tool, not a removed idea. Its old foundation says it extends from bounded seed points along elliptic-curve orbits: docs/work-logs/archive/010-ec-search-foundation.md:9-13. Current implementation still has a canonical `ec_search/` package and a compatibility re-export: src/rational_distance/ec_search/workflow.py:179-193 and src/rational_distance/_legacy/search_ec.py:1-10. Tests cover seed equations, known seed recovery, D4 deduplication, DB resume, and analysis output: tests/test_ec.py:82-115, tests/test_ec.py:141-183, tests/test_ec.py:197-227, tests/test_ec.py:356-405.
- `chain` being paused is justified as role change, not deletion. The route intentionally searches rectangle/general 4-cycles unless `--require-square` is supplied: docs/archive/SEARCH_METHODS.md:95-99 and src/rational_distance/_legacy/search_chain.py:1-19. It produced useful structure: cross-product family exclusion is proven in docs/work-logs/archive/015-cross-product-family-exclusion.md:25-41, and the O(n^4) chain view led to the O(n^2) chain-fast reduction in docs/work-logs/archive/017-chain-reduction-math.md:121-132.
- Old bounded "no result" statements are properly bounded in the inspected sources. For example, chain only claims no fifth-constraint hit up to `max_val=500` in docs/work-logs/archive/014-pythagorean-chain-search.md:39-46, and chain-fast only says tested `max_hyp <= 20000` found no solution in docs/work-logs/archive/018-chain-fast-implementation.md:51-53.
- The old rank-filter / dual-EC negative result is idea-specific. wl033 first saw apparent rank-0 cases, then showed they were unproven/default-effort artifacts and all upgraded under deeper effort: docs/work-logs/033-dual-ec-probe.md:67-107. It explicitly warns default `ellrank` lower=0 is not rank=0 at docs/work-logs/033-dual-ec-probe.md:121-140. wl036 records the fix: effort=1 default and full 4-tuple return at docs/work-logs/036-compute-rank-fix-and-ell2cover-batch.md:33-63.
- The hypotenuse blocker-prime path was partly corrected, not erased. wl034 confirms identities A and C on 1005 chains at docs/work-logs/034-hypotenuse-identity.md:37-53, but rejects the blocker-prime premise because non-primitive hypotenuse scale can carry arbitrary prime factors at docs/work-logs/034-hypotenuse-identity.md:57-107.
- The four requested test files pass now: `70 passed in 5.61s` for `tests/test_parametric.py`, `tests/test_ec.py`, `tests/test_chain.py`, and `tests/test_cli.py`.

Open uncertainties:
- I did not reprove the mathematics from scratch. This audit checks documentation and code evidence for this slice only.
- I did not inspect every later worklog after 045. I only sampled wl053 because it directly explains the current `_legacy/` placement.
- I did not inspect large SQLite databases, only archived summaries/small JSONL samples under `results/archive`.
- I did not evaluate whether future construction-oriented work after wl043 changes the paused status; that is outside this slice.
- The README broken-link issue was confirmed from current filesystem state, not git history.

Recommended updates to main claim ledger:
- Add: "`parametric`, `ec`, and `chain` are paused as engineering/research-priority statuses. They are not deleted, not mathematically ruled out, and still have tests/CLI entry points."
- Add: "`parametric` and three-vertex `ec` are sample/seed/structure tools for 3-of-4 rational-distance points; current docs do not claim they are incapable of ever informing the four-vertex problem."
- Add: "`chain` is a structure/reference route for rectangle/general 4-cycles. Its main square-problem role was largely absorbed by `chain-fast` and then by `(A,B),N`/concordant analysis."
- Add caution: "Do not cite bounded no-hit runs as global impossibility. Always include the bound, such as `max_val=500`, `max_hyp<=20000`, `N<=10^8`, or pair-level mod obstruction."
- Add caution: "Old PARI `ellrank` default-effort rank=0 observations are invalid unless rechecked with certified bounds after wl036."
- Add caution: "Hypotenuse identity remains useful; the blocker-prime argument based on all hypotenuse odd primes being 1 mod 4 is false for non-primitive scaled triples."
- Add cleanup item: "Fix README method-doc links to point to `docs/archive/SEARCH_METHODS.md` and `docs/archive/METHOD_COMPARISON.md`, or restore top-level forwarding docs if that is desired."
- Add wording guard: "When saying local/modular sieves cannot prove no-solution, specify global no-solution. Pair-level no-solution can be proved by chain-closure mod p^2 obstruction."

Plain-language summary:
普通话版本：这三条路线现在更像"先放一边"而不是"已经证明没用"。`parametric` 和三顶点 `ec` 主要帮我们找三顶点样例、种子和轨道；它们没有直接打穿四顶点主问题，但也没有被证明走不通。`chain` 的价值主要被保留下来当结构参考，因为它帮项目看清了四边闭环、排除了一个确定不可能的子族，并导向了更快的 `chain-fast` / `(A,B),N` 主线。需要避免的说法是："旧路线失败了，所以数学上死了。"更准确的说法是："当前要解决主问题，资源优先给 concordant 和 chain-fast；旧路线保留作工具、对照和历史证据。"
