# d19 Theory Framework Audit

Date: 2026-06-07

Scope: audit the repository's theory framework for fatal or near-fatal errors that could overturn top-level conclusions. This audit did not try to prove Harborth's conjecture.

## 2026-06-09 Addendum

补审了 wl107-wl116 的 fixed-ratio / rational-ratio 分支。结论没有推翻 2026-06-07 的主审查：项目仍未声称全局证明，主线仍要区分证明、有限实验和路线猜想。

新增边界是：

- 整数固定比例 `A=kB` 是有效的低维理论切片，但它不能覆盖全局候选。归一化后的比例是 `λ=A/B∈Q_{>0}`，不一定是整数。
- 纯同余筛不能关闭固定比例分支；`B≡0, N1≡1, N2≡-1 (mod M)` 给出每个模数上的局部幸存。
- 有理比例 `R_λ` 版本已经有精确 `Fraction` 模块和测试，但它只记录恒等式与危险样本，不证明 `A=λB` 全灭。

补审文件：`subagent-notes/fixed-ratio-addendum.md`。

## Executive Summary

本次没有发现“当前 production 代码正在错误证明全局 Harborth 猜想”的直接致命 bug。当前 `proof_status` 核心路径已经把最危险的旧问题修掉了：它用 full-plane GEN-CLOSURE，而不是只用 `N1+N2=A+B`；`factor_concordant` 也用因子分解穷尽整数 `N`，不是有限 EC 搜索。

但仓库里确实有几处如果被当成当前结论就会推翻上层判断的风险：

- 旧文档和旧脚本还把 `N1+N2=A+B` 写得像全平面必要条件。它只覆盖正方形内部点。全平面必须用 `{N1+N2, |N1-N2|} ∩ {A+B, |A-B|} != empty`。
- reduced/coprime `(A,B)` 不是 WLOG。当前 reduced-pair 判定不能单独推出全局 Harborth 证明。
- `results/proof_status.db` 和 `results/chain.db` 都有旧语义/旧 schema 风险，不能直接当当前权威结果引用。
- fixed-ratio `A=kB` 只能覆盖整数比例切片。若把它写成全局路线，必须先升级到有理比例 `λ=A/B` 并证明新的 `R_λ` 交点命题。

更普通一点说：主线方向没塌，但旧地图上有几条路标还没改。如果后续 agent 按旧路标走，就可能把“局部/有限/互素/内部”的结论误读成“全局证明”。

## Fatal / High-Risk Results

| Severity | Result | Current impact |
|---|---|---|
| fatal if cited | Sum-only closure is not full-plane closure. | Current `proof_status` fixed; older docs/scripts need labels or updates. |
| fatal if cited | Coprime reduced `(A,B)` is not WLOG. | Current docs mostly warn correctly; global proof still absent. |
| high | Existing `results/proof_status.db` is stale after wl094. | Do not cite existing hard_case counts as current. |
| high | `safe_sieve` wrapper has no coprime guard. | Safe in generated reduced stream; unsafe for manual/full-space use. |
| high | `dual_closure_sieve` remains sum-only. | Treat as legacy inside-square tool. |
| high | Default `concordant` CLI is diagnostic/bounded. | Use factor/proof_status for proof-producing reduced-pair decisions. |

Details live in `risk-register.md`.

## What Looks Sound

- `factor_concordant` exhaustively enumerates integer concordant `N` for a fixed `(A,B)` using divisor pairs of `B^2-A^2`.
- `gen_closure_hit` implements the full-plane four-relation GEN-CLOSURE over the exhaustive concordant set.
- `run_chain_closure_mod_sieve` in current `proof_status` asks for `full_plane=True`.
- `gcd_aware_kills` is a sound necessary filter for arbitrary `(A,B)`.
- `chain-fast` remains a bounded baseline searcher, not a proof engine.
- Long-term directions are not mathematically dead; most are simply open, expensive, or currently lower ROI.

## Branch Status Summary

| Branch | Status |
|---|---|
| `concordant` | active main line |
| `chain-fast` | bounded baseline |
| `proof_status` | reduced-pair proof/diagnosis tool; current code sounder than old DB |
| multi-N / full-space scans | strong finite evidence, not global proof |
| fixed-ratio / rational-ratio | open theory slice; useful but not global by integer `k` alone |
| partner graph | useful finite/structural evidence; identity proved, infinite graph claims open |
| `parametric`, `ec`, `chain` | paused, not dead |
| Heegner / Chabauty / Brauer-Manin / K3 | open long-term, not closed by finite tests |

Full matrix: `branch-status.md`.

## Artifacts

- `claim-ledger.md`: major claims, status, dependencies, and failure modes.
- `risk-register.md`: serious findings with evidence and actions.
- `branch-status.md`: route-by-route status.
- `commands-run.md`: commands, outcomes, failed probes, and test results.
- `subagent-notes/`: slice reports and controller补审 notes.

Subagent reports saved:
- `subagent-notes/reduction-chain.md`
- `subagent-notes/chain-fast-baseline.md`
- `subagent-notes/concordant-multi-n.md`
- `subagent-notes/partner-graph.md`
- `subagent-notes/legacy-paused-routes.md`
- `subagent-notes/safe-filters.md`
- `subagent-notes/safe-filters-controller.md`
- `subagent-notes/advanced-directions-controller.md`
- `subagent-notes/fixed-ratio-addendum.md`

The `safe-filters` slice was first completed locally in `safe-filters-controller.md`; the later subagent return is saved as `safe-filters.md` and is consistent with the main risk register.

## Verification Results

- Full tests: `335 passed, 2 warnings`.
- Addendum full tests on 2026-06-09: `365 passed, 2 warnings`.
- Addendum fixed-ratio/rational-ratio focused tests: `19 passed`.
- Addendum targeted ruff on new fixed-ratio/rational-ratio files: pass.
- Focused safe/proof-status tests: `68 passed`.
- Ruff: failed with 250 existing lint/style errors. This is not a theory-soundness failure, but the repo is not lint-clean today.
- Smoke commands confirmed:
  - `chain-fast --max-hyp 200` found 0 bounded solutions.
  - default `concordant` CLI is bounded diagnostic.
  - factor/proof_status paths give stronger exhaustive reduced-pair decisions.

## Recommended Next Actions

1. Update or label `docs/MULTI_CONCORDANT_N_STRATEGY.md` as historical inside-square/sum-only unless rewritten around GEN-CLOSURE.
2. Rebuild or relabel `results/proof_status.db` and `results/chain.db`; add semantic/version provenance to `results/catalog.json`.
3. Add a coprime-domain guard or rename around `run_safe_sieve`; in particular, keep manual `--pair` inputs from storing coprime-only `safe_sieve` results as strong `no_solution` certificates unless `gcd(A,B)==1` is verified.
4. Mark `dual_closure_sieve` and `prove_no_solution_multi_first.py` as legacy sum-only, or upgrade to full-plane and rerun.
5. Clarify CLI output: `chain_compatible` means inside-square/sum diagnostic unless full GEN-CLOSURE is reported.
6. Keep full-space scans in the "strong empirical evidence" bucket until there is a theorem that closure never occurs.

## Residual Uncertainty

This audit did not independently rederive all external papers or rerun huge scans. It checked repo-internal claims, source code, tests, schemas, and representative result summaries. The biggest unresolved mathematical issue remains the project-level one: no global proof that full-space GEN-CLOSURE can never occur.
