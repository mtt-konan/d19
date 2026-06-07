Slice:
partner-graph: partner graph / G_M / islands / component claims / degree-k distribution.

Files inspected:
- `docs/PARTNER_GRAPH_THEORY.md`
- `docs/CURRENT_FINDINGS.md`
- `docs/PROJECT_STATUS.md`
- `docs/work-logs/054-partner-pair-graph-analysis.md`
- `docs/work-logs/055-kn-equivalence-and-partner-k-distribution.md`
- `docs/work-logs/056-non-coprime-scan-and-partner-coverage-gap.md`
- `docs/work-logs/057-partner-graph-theory-grounding.md`
- `docs/work-logs/058-partner-bfs-graph-visualization.md`
- `docs/work-logs/059-cycle-algebra-mw-rank-deficit.md`
- `docs/work-logs/060-k8-rank-audit-deficit-confirmed.md`
- `docs/work-logs/061-partner-graph-full-bfs-supercomponent.md`
- `docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md`
- `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md`
- `docs/work-logs/064-parallel-map-reuse-and-benchmark.md`
- `docs/work-logs/065-k10-full-k9-sample-rank-audit-scaling-effect.md`
- `docs/work-logs/066-gm-clarify-and-delta-near-miss.md`
- `docs/work-logs/089-kn-hub-partner-identity-A1-A6.md`
- `docs/work-logs/094-gen-closure-landing-A9.md`
- `docs/work-logs/094-k9-k10-ellrank-full-audit.md`
- `docs/work-logs/096-comp0-truncation-vs-genuine-islands.md`
- `scripts/partner/*.py`, with closer reads of `partner_bfs.py`, `partner_full_bfs.py`, `full_gm_closure_scan.py`, `full_gm_delta_stats.py`, `comp0_analyze.py`, `comp0_island_analysis.py`, `verify_islands_unbounded.py`
- `src/rational_distance/concordant/cycle_relations.py`
- `src/rational_distance/concordant/dscale_kn.py`
- `src/rational_distance/concordant/fast_multi_n.py`
- `src/rational_distance/results/gm_closure_delta.py`
- `tests/test_gm_closure_delta.py`
- `tests/test_cycle_relations.py`
- `tests/test_dscale_kn.py`
- `results/partner/*summary*.json`
- Selected small/result jsonl files under `results/partner/`, including closure, BFS, component, island, and partner-pair samples.

Commands run:
- `rg --files docs scripts src tests results | rg ...`
- `git status --short`
- `find docs/audits/2026-06-07-theory-framework-audit -maxdepth 3 -type f`
- `nl -ba ... | sed -n ...` on the docs, work logs, scripts, tests, and source files listed above
- `rg -n "G_M|partner graph|island|component|closure|counterexample|degree|k=|K_" ...`
- `wc -l docs/work-logs/...`
- `sed -n '1,220p' results/partner/*summary*.json`
- `wc -l` and `sed -n '1,5p'` on selected jsonl result files
- `uv run pytest tests/test_gm_closure_delta.py tests/test_cycle_relations.py tests/test_dscale_kn.py`

Claims checked:
- Partner identity: if `(A,B)` has two concordant values `N_i,N_j`, then `(N_i,N_j)` is also multi-N and has `A,B` as concordant values.
- Definition of `G_M`: vertices are multi-N pairs; edges connect a pair to its partner pairs.
- Whether `K_n` is a real clique/subgraph in `G_M`, or only a shared-partner/star view of one high-k vertex.
- Whether `G_M @ max_value=1M` / `7M` component claims are finite-window evidence or global/infinite-graph claims.
- Whether `full_gm_closure_scan` gives a proof of no Harborth/Steiner-Beukers counterexample, or only bounded no-hit evidence.
- Whether degree distribution equals real `k` distribution or only visible/truncated `k_visible`.
- Whether islands are merely finite-window artifacts or closed components under the exact partner relation.
- Whether high-k / rank claims are proven global facts or experimental facts on sampled/generated hubs.
- Whether code-generated graph objects match the mathematical objects named in the docs.

Fatal findings:
- None for this slice. I did not find a reason to mark the partner graph framework globally unsound. The main issues are wording/object-boundary problems that can make readers overinterpret finite or auxiliary graph evidence.

High-risk findings:
- Core theory doc still describes `K_n` in a way that conflicts with the later and implemented `G_M` graph.
  Evidence: `docs/PARTNER_GRAPH_THEORY.md:134-155` says the partner pairs "彼此也通过 G_M 相连" and states the `N_i` are "两两在 G_M 中相邻"; this reads like a clique or direct-adjacency claim inside `G_M`. But the BFS implementation only adds edges from the current pair `p` to each partner pair `u` (`scripts/partner/partner_full_bfs.py:117-125`), and wl058 explicitly corrects the model: a `K_n` hub in `G_M` is a star, not a clique, and `(N_i,N_j)` has no direct edge to `(N_p,N_q)` unless another multi-N relation creates one (`docs/work-logs/058-partner-bfs-graph-visualization.md:73-82`).
  Risk: this is the biggest code-vs-doc object mismatch. It can inflate perceived graph density, confuse component/cycle counts, and make "K_n subgraph" sound like a graph-theoretic clique in `G_M` when it is really a high-k vertex with `C(k,2)` partner-neighbor vertices.
  Recommended fix: in the main claim ledger, say "`K_n shared-partner` means `k=n` for one multi-N pair; in `G_M` it appears as a star centered at that pair, not as a clique." Replace "两两相邻" with "每个 unordered pair `(N_i,N_j)` is a `G_M` vertex adjacent to `(A,B)`."

- Several "full/complete G_M" phrases are stronger than the finite object actually generated by code.
  Evidence: `partner_full_bfs.py` seeds only catalog coprime multi-N pairs (`scripts/partner/partner_full_bfs.py:80-90`) and discards partner vertices whose max coordinate exceeds `max_value` (`scripts/partner/partner_full_bfs.py:103-124`). wl061 correctly lists those mechanics (`docs/work-logs/061-partner-graph-full-bfs-supercomponent.md:15-19`), but also says "完整跑遍 G_M" and "G_M 全貌" (`docs/work-logs/061-partner-graph-full-bfs-supercomponent.md:9`, `docs/work-logs/061-partner-graph-full-bfs-supercomponent.md:40`) and "真正的 partner web 全貌" (`docs/work-logs/061-partner-graph-full-bfs-supercomponent.md:183-185`). wl061 itself later admits larger windows are needed to test whether `G_M` becomes connected at infinity (`docs/work-logs/061-partner-graph-full-bfs-supercomponent.md:203-204`).
  Risk: a reader can mistake a catalog-seeded, coordinate-windowed BFS fixed point for the induced finite graph on all multi-N pairs up to `M`, or worse for the infinite `G_M`.
  Recommended fix: name the object explicitly, e.g. `G_M[seed=catalog max_hyp=100k, W=1M]` or `catalog-seeded partner closure at W=1M`. Reserve bare `G_M` for the infinite graph defined in `docs/PARTNER_GRAPH_THEORY.md:122-132`.

- `full_gm_closure_scan` gives strong bounded no-hit evidence, not a proof of no counterexample.
  Evidence: the script reads the component dump and checks only those loaded vertices (`scripts/partner/full_gm_closure_scan.py:66-77`) for sum closure (`scripts/partner/full_gm_closure_scan.py:31-37`). The worklog records 338,225 scanned vertices and 0 hits (`docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:20-33`) but uses phrases like "反例彻底缺席", "反例彻底在 G_M @ max_value=1M 内不存在", and "G_M 反例彻底搜索" (`docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:21-23`, `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:36`, `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:153-156`). The same file does include the needed caveat: `G_M @ max_value=1M` misses `N > 1M`, `G_M @ max_value=∞` is not scanned, and `max_hyp > 100k` is outside the data (`docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:103-111`, `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:139-149`).
  Risk: the phrase "no counterexample" can be copied into a proof ledger without the finite-window/copy-of-dump qualifier.
  Recommended fix: ledger wording should be "0 sum-closure hits among 338,225 catalog-seeded `W=1M` partner-BFS vertices; strong experimental evidence only." Do not state "G_M has no counterexample" or "counterexample absent" without the window/seed qualifier.

Medium/low findings:
- Degree equals `C(k,2)` only for the visible/truncated neighbor count, not necessarily for real `k`.
  Evidence: wl062's title and conclusion say degree strictly equals `C(k,2)` and that degree distribution is `k` distribution (`docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md:1`, `docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md:201-204`). The body is more precise: degree is `C(k_visible,2)` after the `max_value=1M` cutoff (`docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md:34-40`). wl063 then shows a large gap between `k_real` and `k_visible`, including all six `k_real=10` hubs being invisible as degree-45 hubs in the truncated graph (`docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:52-75`). wl066 correctly codifies the distinction (`docs/work-logs/066-gm-clarify-and-delta-near-miss.md:46-62`).
  Recommended update: keep `degree = C(k_visible,2)` as the graph statement. Keep `k_real` distribution as a separate arithmetic statement computed by factor search.

- "Power-law", "scale-free", and "percolation" language is useful intuition but should stay experimental/modeling language.
  Evidence: wl062 calls the finite comp0 degree plot "typical scale-free network" (`docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md:104-121`, `docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md:123-140`), and wl096 describes giant-component growth as a standard percolation image (`docs/work-logs/096-comp0-truncation-vs-genuine-islands.md:112-117`).
  Recommended update: record as "finite-window empirical shape" or "analogy", not as a proved asymptotic law for infinite `G_M`.

- High-k rank claims are strong experiments on selected/generated hubs, not a family theorem.
  Evidence: wl094 checks 48 `K_9/K_10` hubs from 338,225 BFS vertices and 11 `K_11-K_13` D-scaling hubs (`docs/work-logs/094-k9-k10-ellrank-full-audit.md:26-32`, `docs/work-logs/094-k9-k10-ellrank-full-audit.md:124-156`) and summarizes 70/70 rank <= 4 (`docs/work-logs/094-k9-k10-ellrank-full-audit.md:158-168`). But `dscale_kn.py` explicitly says the rational `n` pool is not complete, because it is bounded by generator-multiple depth and `ellratpoints` height (`src/rational_distance/concordant/dscale_kn.py:33-40`).
  Recommended update: ledger should say "observed/generated high-k hubs k=6..13 all have rank 3 or 4" and not "rank <= 4 for concordant multi-N hubs" unless marked conjectural.

- `P_N` / `Q_N` naming drifts in the rank/cycle code path.
  Evidence: `docs/PARTNER_GRAPH_THEORY.md:68-71` names the integer square-x point as `P_N` and `docs/PARTNER_GRAPH_THEORY.md:212-228` reserves `Q_N` for a half-point with `2Q_N=P_N`. But `cycle_relations.py` calls the integer point `(N^2, ...)` `Q_{N_i}` and then studies relations among those points (`src/rational_distance/concordant/cycle_relations.py:7-18`, `src/rational_distance/concordant/cycle_relations.py:136-143`). The tests also phrase this as "every concordant point lies in 2*E(Q)" (`tests/test_cycle_relations.py:51-60`), which supports the `P_N` interpretation.
  Risk: low for graph construction, medium for theory prose. It can make "half-point sharing" claims sound stronger or different from what the code actually computes.
  Recommended update: in docs and result summaries, say "we compute coordinates/relations for `P_N`; separately verify `P_N` is 2-divisible. We do not explicitly choose half-points `Q_N` in `cycle_relations.py`."

- The old sum-only partner closure scan is not the later full-plane GEN-CLOSURE predicate.
  Evidence: `full_gm_closure_scan.py` checks only `N_i + N_j == A+B` (`scripts/partner/full_gm_closure_scan.py:31-37`). wl094 later defines GEN-CLOSURE as four possible sum/difference relations (`docs/work-logs/094-gen-closure-landing-A9.md:5-13`) and adds `gen_closure_hit` over exhaustive concordant sets (`docs/work-logs/094-gen-closure-landing-A9.md:31-35`).
  Recommended update: when citing wl063/wl066 for partner graph evidence, label it "sum closure" unless the same vertex set has been rechecked under GEN-CLOSURE.

- Some partner scripts still have old default output paths under `results/...` while the inspected artifacts live under `results/partner/...`.
  Evidence: `full_gm_delta_stats.py` defaults to `results/partner_full_bfs_components.jsonl` and `results/full_gm_delta_summary.json` (`scripts/partner/full_gm_delta_stats.py:92-107`), while existing artifacts inspected here are under `results/partner/`. wl094 notes a similar path correction for `k10_extract_and_ellrank.py` (`docs/work-logs/094-k9-k10-ellrank-full-audit.md:19-24`).
  Risk: low theory risk, but reruns can silently write/read the wrong location unless commands pass explicit paths.

Non-issues worth noting:
- Partner identity itself is sound and directly matches the code edge construction.
  Evidence: `docs/PARTNER_GRAPH_THEORY.md:93-120` proves the symmetric identity by expanding the four square conditions. `partner_full_bfs.py` uses exactly this rule to add partner-neighbor vertices from pairs of concordant `N` (`scripts/partner/partner_full_bfs.py:117-125`).

- The later island claim is stronger than a raw finite-window observation for the already discovered islands.
  Evidence: wl096's criterion says an island is closed if every vertex's full partner set stays inside the window (`docs/work-logs/096-comp0-truncation-vs-genuine-islands.md:17-30`). The code uses `exact_concordant_pair` for range-free partner enumeration (`scripts/partner/comp0_island_analysis.py:84-96`), and the unbounded island BFS verifies 8,959/8,959 close exactly to their original vertex sets (`scripts/partner/verify_islands_unbounded.py:54-115`; `results/partner/island_unbounded_bfs.json`). `exact_concordant_pair` is based on exhaustive divisor enumeration, not EC point sampling (`src/rational_distance/concordant/fast_multi_n.py:114-155`).
  Boundary: this proves closure for the 8,959 discovered 1M islands, not that all islands have been enumerated. wl096 explicitly says new islands appear at larger windows (`docs/work-logs/096-comp0-truncation-vs-genuine-islands.md:159-162`).

- The requested tests pass locally.
  Evidence: `uv run pytest tests/test_gm_closure_delta.py tests/test_cycle_relations.py tests/test_dscale_kn.py` collected 19 tests and all passed.

- Results files match the main finite-window numbers quoted in the worklogs.
  Evidence: `results/partner/partner_full_bfs_summary.json` records 338,225 vertices, 350,868 edges, 9,580 components, largest component 309,689. `results/partner/full_gm_closure_scan_summary.json` records 338,225 vertices, 0 closure hits, and `k_max=10`. `results/partner/full_gm_delta_summary.json` records 829,444 candidate pairs, 0 zero deltas, and global min `|Delta|=1`. `results/partner/comp0_island_analysis_1M_summary.json` records 620 branches and 8,959 islands.

Open uncertainties:
- Whether the infinite `G_M` has one or more infinite/giant components is still not proved by BFS. wl096 gives growth from 1M to 7M and D-scaling evidence for infinite vertex families, but finite BFS itself cannot prove infinitude (`docs/work-logs/096-comp0-truncation-vs-genuine-islands.md:112-117`).
- Whether there are components not reachable from the current catalog-seeded BFS and not represented in the current component dumps remains a catalog/seed coverage question. Direct non-coprime scans in wl056 already showed partner reduction covers only a thin slice at small `M` (`docs/work-logs/056-non-coprime-scan-and-partner-coverage-gap.md:38-56`, `docs/work-logs/056-non-coprime-scan-and-partner-coverage-gap.md:126-145`).
- Whether the `rank <= 4` phenomenon is a theorem, a high-k/D-scaling artifact, or a sampling bias remains open. Current high-k evidence is strong but bounded/generated.
- Whether sum-closure zero over the 338,225-vertex BFS set remains zero under the later full-plane GEN-CLOSURE relation for the same graph vertex set was not established by the old wl063 script.
- Whether larger windows introduce islands with higher `k`, different closure-near-miss behavior, or different gcd patterns is open; wl096 already found new islands and 7M `K_6` islands.

Recommended updates to main claim ledger:
- Replace "K_n subgraph in `G_M`" with "`K_n`/shared-partner hub = a multi-N pair with `k=n`; in `G_M` it is a star centered at that pair."
- Define and use a symbol for finite generated graphs, e.g. `G_M^{cat100k,W}` or `G_M[seed=catalog max_hyp=100k, W]`. Do not call this bare "the full `G_M`".
- Record wl063/wl066 as: "In the catalog-seeded `W=1M` partner graph, 338,225 vertices and 829,444 candidate `N` pairs have 0 sum-closure hits; nearest `|Delta|=1`." Mark as experimental bounded evidence.
- Record wl096 islands as: "The 8,959 1M islands are proven closed under the exact partner relation by range-free enumeration/unbounded BFS; new islands can still appear at larger windows."
- Split `k_visible`, graph degree, and `k_real` into separate ledger rows. Use `degree=C(k_visible,2)` for graph dumps; use factor-search summaries for `k_real`.
- Record high-k rank evidence as "70 checked/generated hubs with k=6..13 all rank 3 or 4" and keep the global rank-bound statement conjectural.
- Add a terminology note: `cycle_relations.py` currently computes with `P_N=(N^2,...)`; if the prose says `Q_N`, clarify whether it means the square-x point or a chosen half-point.
- Add a closure terminology note: wl063/wl066 partner graph closure is sum-only; wl094 GEN-CLOSURE is a broader full-plane predicate.

Plain-language summary:
The partner graph idea is basically sound: a pair `(A,B)` with many shared `N` values naturally creates partner edges, and the code follows that rule. The main danger is not a broken algorithm; it is wording. Several docs sometimes talk as if a finite, catalog-seeded, coordinate-cut graph is "the full `G_M`", or as if a high-`k` hub is a clique inside `G_M`. In the actual code, a high-`k` hub is a star, and the big 338K graph is a very useful finite experimental object, not the infinite graph.

The no-counterexample result is strong evidence, not proof: it says "no sum-closure hit in the current 1M generated graph." The island result is stronger for the islands already found: those 8,959 islands were checked with a range-free partner enumeration and really are closed finite components. But bigger windows can still reveal new islands and more graph structure.
