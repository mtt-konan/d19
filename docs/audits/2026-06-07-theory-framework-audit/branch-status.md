# Branch Status

## Status Matrix

| Branch / direction | Status | Justification | Risk guard |
|---|---|---|---|
| `concordant` | active | It is the main line for fixed `(A,B)` and common-leg `N`; current production path uses factor enumeration plus GEN-CLOSURE for reduced pairs. | Do not present reduced-pair output as global Harborth proof. |
| `chain-fast` | baseline | Direct bounded searcher for the four-vertex square problem; tests pass and it remains the comparison oracle. | Bounded no-hit only; old `chain.db` is legacy. |
| `proof_status` | engineering proof/diagnosis tool | Current methods can prove pair-level `no_solution` in their stated domain. Fast-core is useful for large reduced-pair diagnosis. | Existing `results/proof_status.db` is stale; domain is reduced pairs unless full-space pipeline is explicit. |
| safe-pair / modular / gcd-aware sieves | active supporting tools | `safe_sieve` is sound for coprime reduced input; `gcd_aware_kills` generalizes to arbitrary `(A,B)` as a necessary filter; full-plane mod p^2 is implemented. | Keep coprime-only and arbitrary-pair filters separate. |
| multi-`N` / high-rank concordant curves | active experimental/theory support | Multi-N pairs are real and exactly enumerable; observed full-space scans have 0 closure to high finite bounds. | Multi-N is necessary half-solution layer, not a complete solution. |
| fixed-ratio / rational-ratio | open theory slice | Integer `A=kB` reduces variables and gives useful identities, but global normalized candidates require rational `λ=A/B`. wl115-wl116 upgraded the language to `R_λ` and recorded exact identities. | Do not claim integer `k` coverage proves all rational ratios. Do not treat residue survivors or quadratic roots as true candidates. |
| partner graph / `G_M` / islands | experimental structure + some exact subclaims | Partner identity is algebraic; finite-window BFS and no-closure scans are empirical; discovered islands have stronger exact closure checks. | `K_n` is a star/hub in `G_M`, not necessarily a clique; finite graph is not infinite `G_M`. |
| `parametric` | paused | Three-vertex baseline and seed tool; retained with tests. | Not mathematically dead; old GPU bugs are not a route proof. |
| `ec` | paused | Three-vertex seed/orbit route; retained with tests and compatibility layer. | Do not confuse paused `ec` CLI route with concordant EC/proof_status tools. |
| `chain` | paused / structure reference | General 4-cycle/rectangle route informed reductions and identities; square baseline moved to chain-fast. | Bounded old no-hit statements stay bounded. |
| finite descent / path B | closed as simple fixed-modulus proof route | wl080 closes the simple mod-p^2 coverage program; later wl093/wl094 supersede sum-only closure and wl104 adds full-space scans. | Old dual closure is inside-square; path closure is not global theorem. |
| A1 rank proof route | open/empirical | wl084 retracts strict proof while preserving empirical support. | Do not cite wl083 as current theorem. |
| Heegner / height | diagnostic / witness route | Current code never returns `no_solution`; factor_concordant already exhausts integer N for reduced legs. | Do not treat bounded height scans as proof. |
| Chabauty / Quadratic Chabauty | open long-term | Stub only; could become a true finite rational-point enumerator. | Not dead due to lack of current tooling. |
| Brauer-Manin | open long-term | Stub only; potentially addresses local-global gaps. | Not killed by modular residual failures. |
| K3 / Mordell-Weil lattice | open speculative long-term | High-effort geometric framework. | Not current evidence; do not overpromise. |

## Plain-Language Route Map

`chain-fast` 是“直接搜”的基线机器。它告诉我们在某个范围里有没有看到完整正方形解。

`concordant` 是“拆成 `(A,B,N)` 后再看数论结构”的主线。它现在最强的一步是：对 reduced/coprime pair，可以穷尽所有整数 `N`，再用全平面的 GEN-CLOSURE 判定是否闭合。

非互素 pair 是单独战场。项目已经有 `gcd_aware_kills` 和 full-space finite scans，但还没有一个全局数学证明说闭合永远不会发生。

固定比例 `A=kB` 是另一种低维切法。它能减少变量，帮我们找结构；但全局候选给的是有理比例 `λ=A/B`。所以这条线的下一步不是继续只扫整数 `k`，而是证明或否定 `R_λ` 上的 full-plane closure 交点只能来自 `r <-> λ/r`。

旧路线没有被判死。它们只是现在不在主战场：`parametric` / `ec` 帮三顶点和种子；`chain` 帮结构理解；`chain-fast` 接过了直接四顶点 baseline 的角色。

## Branches That Need Wording Updates

- `docs/MULTI_CONCORDANT_N_STRATEGY.md`: update sum-only closure to GEN-CLOSURE or mark as historical inside-square strategy.
- `docs/PARTNER_GRAPH_THEORY.md`: replace `K_n clique/subgraph` language with `k=n shared-partner hub/star`.
- `docs/THEORY_DIRECTIONS_ADVANCED.md`: reconcile Heegner status: diagnostic after wl092, not current no-solution upgrade path.
- `results/README.md` / `results/catalog.json`: mark `chain.db` and `proof_status.db` provenance/staleness.
- `README.md`: fix links to archived method docs (`docs/archive/SEARCH_METHODS.md`, `docs/archive/METHOD_COMPARISON.md`).
