# wl051 — F₂-rank as a proof_status pipeline method

## 目的

把 wl049 的 `f2_rank_of_concordant_pair` 接进 `proof_status` 工作流，作为一个新的 informational method。每个 multi-N pair 在跑 PARI rank 之前先记一笔 F₂-rank 证据，材料化到 `pair_method_attempts` 和 `pair_proof_status.rank_lower` 上。

## 设计

### 不是 short-circuit，是 information layer

最初的设想是"F₂-rank ≤ 2 ⇒ no_solution"。wl050 的实测推翻了这点：F₂-rank 只是 rank 的**下界**

```text
F₂-rank ≤ rank(E) + 2
=> rank(E) ≥ max(0, F₂-rank − 2)
```

不能给出 rank 的上界 ⇒ 不能直接证 no_solution。

所以 F₂-rank 不是 no_solution-decider，而是 **evidence recorder**：它把 `rank_lower` 抬到一个 PARI 没运行也能得到的下限。

### 在 pipeline 里的位置

```text
safe_sieve              # 2-adic 障碍
chain_closure_mod_sieve # mod p² closure 障碍
factor_concordant       # 枚举 N + 检查 closure
f2_rank                 # 新增, informational
rank_zero               # PARI ellrank
heegner                 # rank-1 height 诊断
chabauty / brauer_manin # stubs
```

放在 `factor_concordant` 后是因为 F₂-rank 需要 concordant N 列表，且当 `factor_concordant` 已经做出终结判决（`no_solution` 因无 N，或 `solution_found`）时 pipeline 已经停了，F₂-rank 不会跑。

放在 `rank_zero` 前是因为 F₂-rank 提供的 `rank_lower` 可以作为 PARI 结果的合理性检查（PARI rank ≥ F₂-rank − 2 应当总成立）。

## 实现

### `src/rational_distance/proof_status/methods.py`

```python
def run_f2_rank(A: int, B: int) -> MethodResult:
    """Compute F₂-rank of half-point images for concordant N.

    Outcome is always 'pass' (informational, never terminal).
    Records f2_rank, saturated flag, rank_lower (=max(0, F₂-rank-2)),
    and minimal_relation if F₂-rank < k.
    Skipped when concordant_N count < 2.
    """
```

### `src/rational_distance/proof_status/workflow.py`

`_aggregate_details` 学会读 `f2_rank` 方法的 `rank_lower` 贡献：

```python
if method == "f2_rank":
    candidate = _coerce_int(details.get("rank_lower"), None)
    if candidate is not None and (rank_lower is None or candidate > rank_lower):
        rank_lower = candidate
```

只允许**抬高**已有的 `rank_lower`，绝不让 F₂-rank 的下界覆盖一个更紧的现有值（防止 PARI 紧 bound 被覆盖回去；虽然 pipeline 顺序保证这不会发生）。

### `DEFAULT_METHOD_PIPELINE`

```python
DEFAULT_METHOD_PIPELINE: tuple[tuple[str, MethodFn], ...] = (
    ("safe_sieve", run_safe_sieve),
    ("chain_closure_mod_sieve", run_chain_closure_mod_sieve),
    ("factor_concordant", run_factor_concordant),
    ("f2_rank", run_f2_rank),
    ("rank_zero", run_rank_zero),
    ("heegner", run_heegner_stub),
    ("chabauty", run_chabauty_stub),
    ("brauer_manin", run_brauer_manin_stub),
)
```

## 测试

`tests/test_proof_status.py` 增加：

```text
TestF2RankMethod
    test_skipped_when_no_concordant_n         (A, B) = (1, 3)
    test_skipped_with_only_one_concordant_n   (A, B) = (7, 45)
    test_reports_f2_rank_for_known_multi_n_pair  (A, B) = (153, 560), F₂-rank=3 saturated
    test_records_minimal_relation_when_deficient (A, B) = (11776, 17199), F₂-rank=3 deficient

TestWorkflow
    test_f2_rank_pipeline_records_rank_lower_for_multi_n
        (A, B) = (9269, 24255)  odd-odd, A+B mod 4 = 0
        workflow records f2_rank attempt and rank_lower=1 in pair_proof_status
```

新增一个 `f2_rank_pipeline` fixture（PARI-free pipeline = safe_sieve + factor_concordant + f2_rank）。

234 tests pass。

## 已知限制

1. **重复因子分解**：`run_f2_rank` 和 `run_factor_concordant` 都调用 `find_concordant_by_factorization(A, B)`。后续若加方法间状态传递可以省。当前每 pair 约 ms 级开销，可接受。
2. **safe_sieve 后的过滤偏差**：我们的 multi-N catalog 里**所有**条目都满足 mixed-parity 或 odd-odd-wrong-mod4，这意味着它们**全部**被 safe_sieve 第一步杀掉，`f2_rank` 实际上跑不到。只有理论上构造的 odd-odd 且 A+B mod 4 = 0 的 multi-N pair（如 (9269, 24255)）才能走到 f2_rank。这是 chain 而非 concordant 层面的 parity 障碍，仍要看后续是否值得把 `f2_rank` 也对 concordant-only 通路开放。

   实测：max_hyp=50000 catalog 里仅 **2 个 pair**通过 safe_sieve：
   ```text
   ( 9269, 24255)  k=3   passes safe_sieve
   (10879, 30821)  k=3   passes safe_sieve
   ```
   其余 4966 个被 safe_sieve 在第一步杀掉。

3. **没改 rank_zero**：当前 F₂-rank 不能减少 PARI 调用。如果以后想让 F₂-rank ≥ 3 时短路 PARI（"反正 rank ≥ 1, rank_zero 帮不了忙"），需要给方法间传递状态——下次再做。

## 后续

- 在 `rank_zero` 里加一个内部 F₂-rank 检查，F₂-rank ≥ 3 时直接返回 inconclusive 并附 `pari_skipped=True`，节省 PARI 调用。
- 把 `proof_status` 数据库 schema 加一个 `f2_rank` 列，方便对 hard_case 做按 F₂-rank 分层的查询。

## 文件

```text
src/rational_distance/proof_status/methods.py      新增 run_f2_rank 与 pipeline 条目
src/rational_distance/proof_status/workflow.py     _aggregate_details 学会 f2_rank
tests/test_proof_status.py                         新增 TestF2RankMethod 与一个 workflow 集成测试
docs/work-logs/051-f2-rank-method-in-proof-status.md  本文件
```
