# wl088 — C.2/C.3/C.4 工程批次：multi_n_sieve 接入 pipeline + rank_zero short-circuit + f2_rank schema 列

## 背景

OPEN_DIRECTIONS C 类里有三条低成本工程小项, 都对准「让 proof_status pipeline
更省 PARI + 更可分层查询」:

- **C.2** `multi_n_sieve` 接入 DEFAULT_METHOD_PIPELINE (出处 wl073)
- **C.3** `rank_zero` 在已知 F₂-rank ≥ 1 时 short-circuit, 跳过 PARI (出处 wl051)
- **C.4** `proof_status` schema 加 `f2_rank` 列, 给 hard_case 分层 (出处 wl051)

本 wl 一次把三条都落地。**不涉及任何长跑** —— 纯结构改动 + 单测。

## C.2 — `multi_n_sieve` 接入主 pipeline

**理由 (wl073 §2)**: 一个完整 4-chain 闭合两个共享候选点的直角三角形, 至少需要
**两个不同的** concordant 整数 N。所以 `k = #concordant_n < 2` 是**严格的
`no_solution`** —— 单个 (或零个) concordant N 永远闭不上 4-cycle。

实现 `run_multi_n_sieve(A, B, *, concordant_n=None)`:

- `k < 2` → `no_solution` (闭合不可能)
- `k >= 2` → `pass` (交给后续更深的方法)

**pipeline 位置**: 放在 `factor_concordant` **之后** (它先把 concordant 枚举做完,
`multi_n_sieve` 复用同一份 `concordant_n` 缓存, 零额外枚举成本):

```
safe_sieve → chain_closure_mod_sieve → factor_concordant
    → multi_n_sieve            ← 新增
    → f2_rank → rank_zero → heegner → chabauty → brauer_manin
```

`DEFAULT_METHOD_PIPELINE` 从 8 个方法变 9 个。`build_legacy_baseline_spec`
(ab_sieve_benchmark) 自动从 `DEFAULT_METHOD_PIPELINE` 派生, 无需改。

## C.3 — `rank_zero` 的 F₂-rank short-circuit

**理由 (wl051)**: 若更早的方法 (`f2_rank`) 已证明 rank ≥ 1, 那么 `rank_zero`
(靠 PARI `ellrank` 判 rank 上界是否为 0) **只可能返回 inconclusive** —— rank≠0,
判不了。此时那次 PARI `ellrank` 调用 (~64MB stack, 秒级) 是纯浪费。

实现:

- `run_rank_zero(A, B, *, rank_lower_hint=None)`: 当 `rank_lower_hint >= 1`,
  直接返回 `inconclusive`, `details={"rank_lower": ..., "short_circuit": "f2_rank"}`,
  **完全跳过** `_get_cached_pari()`。
- workflow 串状态: `f2_rank` 方法在 `_aggregate_details` 里把 `rank_lower`
  抬高 (已有逻辑), `_run_method_with_concordant_cache` 把累积的 `rank_lower`
  作为 `rank_lower_hint` 传给 `run_rank_zero`。
- 并行/benchmark 路 (`ab_sieve_methods.py`): `PairEvalContext` 加 `f2_rank` 字段,
  `run_f2_rank_ctx` 写入, `run_rank_zero_ctx` 读出并传 `hint = max(0, f2_rank-2)`。

注意 hint 用 `max(0, f2_rank - 2)` —— 与 `f2_rank` 方法本身的 `rank_lower =
max(0, f2_rank - 2)` 一致 (F₂-rank 含 2 个来自坐标的平凡贡献), 即 F₂-rank ≥ 3
才触发 short-circuit。

## C.4 — `proof_status` schema 加 `f2_rank` 列

给 hard_case 按 F₂-rank 分层查询。改动:

- `schema.py`: `pair_proof_status` 加 `f2_rank INTEGER` 列;
  `PROOF_DB_SCHEMA_VERSION` 1 → 2 (旧库会被 `_require_supported_schema` 拒绝,
  需重建 —— 与既有「不做 in-place migration」策略一致);
  `upsert_pair_status` 加 `f2_rank` 参数 (`COALESCE` 保留已有值);
  `get_pair_status` 读出。
- `types.py`: `PairProofStatus` 加 `f2_rank: int | None = None`。
- `workflow.py`: `_aggregate_details` 从 `f2_rank` 方法 details 取 `f2_rank`;
  `process_pair` / `compute_pair_status` 两条路都 thread 该列并写库;
  `PairComputeResult` 加 `f2_rank` 字段。

## 验证

```bash
PARI_MT_ENGINE=single PYTHONPATH=src uv run pytest -q     # 319 passed
uv run ruff format <changed files>                        # clean
uv run ruff check <changed src files>                     # 0 new errors
```

新增单测 (`tests/test_proof_status.py`):

- `TestMultiNSieveMethod`: k=1 (7,45) → no_solution; k=3 (153,560) → pass;
  pipeline 中 `multi_n_sieve` 紧跟 `factor_concordant`。
- `TestRankZeroMethod`: `rank_lower_hint=1` → inconclusive + `short_circuit="f2_rank"`
  (PARI-free, 即使无 cypari2 也过); `rank_lower_hint=0` 不触发 short-circuit。
- `TestF2RankSchemaColumn`: upsert `f2_rank=3` 后 `get_pair_status` 读回 3。

更新的既有测试 (反映**有意的** API 变更, 非「改测试凑过」):

- `test_default_method_pipeline_names_are_stable` / `test_legacy_baseline_matches_default_pipeline`:
  期望 pipeline 从 8 → 9 个方法 (新增 `multi_n_sieve`)。
- `test_cli_fast_core_audits_only_survivors`: `PairComputeResult` 构造加 `f2_rank=None`。

ctx 路 short-circuit 手验 (PARI-free):

```
PairEvalContext(f2_rank=3) → run_rank_zero_ctx → inconclusive, short_circuit=f2_rank
PairEvalContext()          → run_rank_zero_ctx → 落到真 PARI (inconclusive)
```

## 结论

C.2 / C.3 / C.4 全部落地, 已从 OPEN_DIRECTIONS 移除 (按「落地即移除」规则)。

- **正确性**: multi_n_sieve 的 k<2 ⇒ no_solution 是 wl073 已证的严格必要条件;
  rank_zero short-circuit 不改变任何 pair 的最终判定 (只把一个必然 inconclusive
  的 PARI 调用换成 inconclusive 短路), 纯性能 + 可观测性改进。
- **schema v2**: 旧 proof DB 需重建 (与既有策略一致, 无 in-place migration)。
