# Claim Ledger

状态标签：
- `proved`: 仓库内有清楚证明或代码穷尽判定，且前提写明。
- `empirical`: 有有限扫描或样本证据。
- `engineering baseline`: 工具可信但只在给定范围/配置内给结论。
- `conjectural`: 方向或猜想，未证明。
- `obsolete`: 被后续 worklog 或代码替代。
- `unclear`: 证据不足或文件口径混杂。

## High-Level Claims

| ID | Claim in plain Chinese | Source evidence | Status | Upstream dependencies | Downstream use | Code/tests/results support | Fatal failure mode |
|---|---|---|---|---|---|---|---|
| C1 | `concordant` 是当前主线。 | `README.md:5-10`, `PROJECT_STATUS.md:14-24`, `DIRECTIONS.md:5-10` | engineering baseline | Project prioritization, not theorem | Work planning | Docs consistent | If treated as proof that other routes are dead. |
| C2 | `chain-fast` 是直接四顶点问题的可信 bounded baseline。 | `README.md:7-8`, `PROJECT_STATUS.md:63-76`, chain-fast subagent | engineering baseline | Primitive triple pair search, bounded `max_hyp` | Regression oracle, comparison | Full tests pass; smoke `max_hyp=200` found 0 | If "bounded no hit" is promoted to global proof. |
| C3 | `parametric` / `ec` / `chain` are paused, not deleted/dead. | `README.md:10`, `PROJECT_STATUS.md:90-98`, legacy subagent | engineering baseline | Route role split | Future seeds / sanity checks | Focused tests 70 passed | If old route failures are cited as mathematical death. |
| C4 | Pair-level `mod1680` concordant pre-sieve is empty/useless. | `CURRENT_FINDINGS.md:23-49` | empirical / obsolete runtime direction | Only checks existence of some `N mod M` | Avoids wasted runtime filter | Docs say it kills 0 at max_hyp=2000 | If reused as meaningful runtime filter. |
| C5 | Reduced-pair safe conditions `A` odd, `B` odd, `(A+B)%4==0` are safe only for reduced/coprime full-chain setting. | `CURRENT_FINDINGS.md:51-71`, `MATH.md:439-443`, `safe_pair_sieve.py:1-23` | proved under coprime input | coprime mod-12 theorem | `safe_sieve` | `tests/test_coprime_mod12.py`, focused tests pass | If used on non-coprime pairs without gcd-aware replacement. |
| C6 | A full-plane counterexample implies at least two concordant `N`, but not necessarily `N1+N2=A+B`; full condition is GEN-CLOSURE. | Old: `MULTI_CONCORDANT_N_STRATEGY.md:64-92`; corrected: `MATH.md:252-260`, wl093 | old sum-only obsolete; GEN-CLOSURE proved | Geometry of `|u|`, `|u-n|` legs | proof_status terminal decider | `gen_closure_hit`, tests pass | Sum-only version misses outside-square cases. |
| C7 | Multi-`N` pairs exist and are meaningful, but observed examples do not close. | `MULTI_CONCORDANT_N_STRATEGY.md:5-35`, `MULTI_N_FILTER_LADDER.md:101-127`, wl104 scans | empirical | Exact factor enumeration / fast pivot | Candidate generation | `fast_multi_n` tests pass; full-space scans to 1M show 0 closure | If finite 0 closure becomes global proof. |
| C8 | Positive rank / strong concordance explains many half-solutions but does not give full square solution. | `CURRENT_FINDINGS.md:7-22`, `MULTI_CONCORDANT_N_STRATEGY.md:123-178` | proved as scope warning; examples empirical | Ono translation, square-x special section | Prevents rank-only proof claims | two_descent/half-point tests pass | If positive rank is used as sufficient for integer `N` or closure. |
| C9 | `proof_status` and fast-core are reduced-pair diagnosis/proof tools, not a global Harborth proof. | `PROOF_STATUS_FAST_MODE.md:8-55`, `methods.py:19-28`, `MATH.md:498-513` | engineering baseline with proved pair methods | reduced pair generator; method pipeline | Result DB, fast-core summaries | Current tests pass; existing DB stale | If DB summaries are cited without reduced/full-space scope. |
| C10 | Partner graph / island/component results are experimental graph structure unless exact closure is stated. | `PARTNER_GRAPH_THEORY.md`, partner subagent | mixed: identity proved, graph scans empirical | partner identity, finite BFS window | Graph strategy | Tests pass; result summaries match | If finite `G_M` window is treated as infinite graph proof. |
| C11 | Heegner, Chabauty, Brauer-Manin, finite descent, K3 are not dead merely due to early negative experiments. | `THEORY_DIRECTIONS_ADVANCED.md:17-24`, `OPEN_DIRECTIONS.md:14-24` | conjectural/open | external tools/theorems | Long-term research | Stubs conservative | If "low ROI now" becomes "mathematically impossible." |
| C12 | The repo has not found a four-vertex square solution and does not prove Harborth globally. | `MATH.md:24-29`, `README.md:57`, wl104 `仍开放` | proved as project status | All above scope boundaries | Final headline | Full tests pass; no solution_found in smoke | If reduced/fullspace finite scans are overstated. |
| C13 | Fixed integer ratio `A=kB` is an open low-dimensional theory slice; it is not a global route unless upgraded to rational `λ=A/B`. | `wl115:11-27`, `wl116:5-19`, fixed-ratio addendum | conjectural/open with proof-side tooling | normalized square coordinates, rational `A/B`, true concordant `N` | fixed-line strategy, center-line generalization | `rational_ratio.py`; fixed-ratio focused tests pass | If "all integer k closed" is cited as "all rational ratios closed." |

## Reduction Chain Ledger

| ID | Reduction | Current status | Evidence | Main risk |
|---|---|---|---|---|
| R1 | Rational point to integer distance equations. | proven / standard within docs | `MATH.md:7-29`, wl093 `:36-57` | None found beyond finite parameter bounds in old search. |
| R2 | Inside-square 4-chain to `a+c=b+d`. | proved only inside square | `MATH.md:252-260` | Fatal if used for all-plane. |
| R3 | Full-plane geometry to GEN-CLOSURE. | proved in wl093 and implemented | `wl093:59-84`, `analysis.py:298-315` | Must use four relations, not just sum. |
| R4 | `(A,B,N)` concordant to curve `Y^2=X(X+A^2)(X+B^2)`, `X=N^2`. | one-way plus verification needed | `MATH.md:357-388` | Square-x on curve alone is not sufficient. |
| R5 | Factor enumeration recovers all integer concordant `N`. | proved for fixed positive unequal `(A,B)` | `factor_search.py:1-23`, `:88-133` | Trial division cost only; not a logical issue. |
| R6 | Reduced/coprime `(A,B)` covers global search. | false / not WLOG | `MATH.md:498-513` | Fatal if used for global proof. |
| R7 | Full-space finite scan via direct multi-N generation. | empirical finite | `wl104:49-74` | Supports confidence, not proof. |

## Safe Filter Ledger

| ID | Filter | Status | Evidence | Scope |
|---|---|---|---|---|
| S1 | `safe_sieve` / `classify_reduced_pair` | proved under coprime input | `MATH.md:408-443`, `safe_pair_sieve.py:1-23` | reduced/coprime only |
| S2 | `gcd_aware_kills` / `D_g` | proved necessary filter for arbitrary `(A,B)` | `MATH.md:445-497`, `safe_pair_sieve.py:61-93` | arbitrary `(A,B)`, not complete |
| S3 | `chain_closure_mod_sieve(full_plane=True)` | sound modular obstruction | `chain_closure_sieve.py:146-182`, `methods.py:137-170` | pair-level modular kill |
| S4 | `factor_concordant + gen_closure_hit` | terminal reduced-pair decider | `methods.py:213-287`, `analysis.py:298-315` | reduced/coprime legs; gcd gap remains |
| S5 | `dual_closure_sieve` | obsolete/inside-square | `dual_closure_sieve.py:10-27`, `:66-69` | do not cite as full-plane |
| S6 | `proof_status.fast_core` | engineering core summary | `fast_core.py:20-33`, `PROOF_STATUS_FAST_MODE.md:164-193` | reduced pair stream |
| S7 | fixed-ratio pure congruence sieve | negative result / boundary certificate | `fixed_ratio_sieve.py:1-13`, fixed-ratio addendum | cannot kill fixed-ratio branch by finite residue survivor exhaustion alone |
| S8 | rational-ratio identities | proof-side exact algebra, not a decider | `rational_ratio.py:1-6`, `rational_ratio.py:92-161`, `rational_ratio.py:181-293` | records `R_λ`, full-plane relations, product and rectangle identities |

## Experiment / Proof Boundary Ledger

| Claim | Correct label | Evidence | Wording guard |
|---|---|---|---|
| max_hyp scans with 0 solution | empirical | wl104 `:49-74`, chain-fast subagent | Say the bound and generator domain. |
| `chain-fast` no hits | engineering baseline | smoke + tests | Say "bounded search found none." |
| Partner `G_M` closure 0 hits | empirical finite graph | partner subagent | Say seed/window. |
| 8,959 islands closed | proved for discovered islands | partner subagent / wl096 | Say discovered 1M islands only. |
| A1 `k=2 => rank>=2` | empirical/open | wl084 | Do not cite wl083 as current theorem. |
| Heegner height scan | diagnostic | `heegner_height.py:10-16`, `methods.py:503-571` | Never `no_solution` today. |
| fixed integer `A=kB` scans | empirical / theorem-target generator | wl109, wl115-wl116 | Say integer `k`, finite `B` bound, and not all rational `λ`. |
| rational-ratio `R_λ` module | exact algebra support | `rational_ratio.py`, `tests/test_rational_ratio.py` | Say it records identities; it does not prove non-existence. |

## Data Provenance Ledger

| Artifact | Status | Evidence | Action |
|---|---|---|---|
| `results/proof_status.db` | stale after wl094 | SQLite shows `factor_concordant inconclusive` and `hard_case=4653` | rebuild or mark stale |
| `results/chain.db` | legacy schema | SQLite schema lacks current `chain_meta` | mark legacy; do not cite as current |
| `results/catalog.json` | partial index | lists proof_status but not chain.db | add semantic/version metadata |
| `results/multi_n/full_scan_max*.json` | empirical scan summaries | wl104 | cite with bounds |
