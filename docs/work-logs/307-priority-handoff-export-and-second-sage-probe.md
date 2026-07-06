# wl307 - priority handoff export and second Sage probe

日期：2026-07-07

## 一句话结论

优先级队列现在可以直接驱动 residual handoff 导出。

普通话说：不需要手工复制 `(A,B,curve,cover)` 了。给 exporter 一个 priority JSON 和 `--top 4`，
它会按目标分组生成 Sage/Magma/JSON handoff。

## 更新脚本

```text
scripts/theory/export_mixed_closure_residual_handoff.py
tests/test_mixed_closure_residual_handoff.py
```

新增模式：

```bash
--priorities results/mixed_closure_aabb_residual_cover_priorities.json
--top 4
```

原来的单目标模式仍然保留：

```bash
--target 115,297,AA --cover-index 3 --cover-index 4 --name ...
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --top 4 \
  --out-dir results/mixed_closure_residual_handoffs
```

输出：

```text
wrote 2 priority handoff(s) to results/mixed_closure_residual_handoffs
  priority_001_115_297_AA_covers_3_4: covers=[3, 4]
  priority_003_575_4641_AA_covers_4_3: covers=[4, 3]
```

注意：top-4 priority rows 只对应两个 `(A,B,curve)` 分组，所以生成两个 handoff。

## 第二组 Sage probe

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

输出：

```text
wrote Sage handoff probe to results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_sage_probe.json
status=ok
rank_bounds=[0, 2]
rank_proof_status=runtime-error
cover_point_counts=[0, 0]
```

关键字段：

```text
rank_bounds = [0, 2]
rank_probable = 0
selmer_rank = 4
torsion_two_dimension = 2
cover 4 genus = 1, rational_point_count = 0 at bound 100
cover 3 genus = 1, rational_point_count = 0 at bound 100
```

## 边界

这轮没有证明 cover 无点。

它推进的是：

```text
top-4 residual cover 可以一键导出为 handoff；
前两个 priority 分组都有 Sage probe 基线；
两组都表现为 rank_bounds [0,2] + probable rank 0 + Selmer gap 2；
这继续支持 Sha[2] / 2-cover 障碍定位，但仍不是证明。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_handoff.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/export_mixed_closure_residual_handoff.py \
  tests/test_mixed_closure_residual_handoff.py
```

结果：

```text
6 passed
All checks passed!
```
