# wl313 - priority handoff probe audit

日期：2026-07-07

## 一句话结论

priority top-4 residual cover 现在有 handoff/probe 对齐审计。

普通话说：以前我们有 priority queue、handoff 文件、Sage probe 文件，但需要人自己核对
“这几个文件是不是同一批 cover”。现在有脚本统一检查：top-4 priority 行对应的两个 handoff
分组是否都有 JSON/Sage/Magma 文件、Sage probe 是否存在、cover index 和 quartic 是否对得上。
后续 wl314 又把 cover-to-elliptic map identity verification 接进了同一个 audit。
后续 wl315 又把 bad-prime Qp local witness probe 接进了同一个 audit。

## 新增脚本

```text
scripts/theory/audit_mixed_closure_priority_handoffs.py
tests/test_mixed_closure_priority_handoff_audit.py
```

它检查：

```text
priority top-N 是否能分组到 expected handoff name；
每组是否有 .json / .sage / .magma；
每组是否有 *_sage_probe.json；
如果启用 `--require-map-verifications`，每组是否有 *_map_verify.json；
如果启用 `--require-local-witnesses`，每组是否有 *_local_witnesses.json；
handoff JSON 的 target、cover index、quartic 是否和 priority row 对齐；
probe JSON 的 target、cover index、bounded point count 是否和 handoff 对齐；
selmer_rank - torsion_two_dimension 是否等于 priority row 记录的 selmer_gap；
map verification 是否显示所有 target cover 的 rational map identity verified；
local witness probe 是否显示所有坏素数都有 Qp witness。
```

## 真实运行

先补齐 priority_001 的 probe：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

输出：

```text
status=ok
rank_bounds=[0, 2]
rank_proof_status=runtime-error
cover_point_counts=[0, 0]
```

然后跑对齐审计：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_priority_handoffs.py \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --top 4 \
  --require-probes \
  --require-map-verifications \
  --require-local-witnesses \
  --out results/mixed_closure_priority_handoff_audit_top4.json \
  --strict
```

输出：

```text
ready=True
groups_checked=2
missing_files=[]
violations=[]
map_verify_status_counts.ok=2
local_witness_status_counts.ok=2
```

关键 JSON：

```text
priority rows checked = 4
target cover count = 4
probe_status_counts.ok = 2
map_verify_status_counts.ok = 2
local_witness_status_counts.ok = 2
group priority_001_115_297_AA_covers_3_4: rank_bounds=[0,2], selmer_minus_torsion2=2
group priority_003_575_4641_AA_covers_4_3: rank_bounds=[0,2], selmer_minus_torsion2=2
```

## 边界

这仍然不是 residual cover 无点证明。

它只是把“后续严格证明要处理哪几个 cover、当前 Sage 诊断是什么、PARI map 是否真的落到
目标椭圆曲线、坏素数 local side 是否有显式 witness、文件是否对齐”固定成机器可复查的 gate。
也就是说，它减少证据包出错的空间，但不提升 bounded search 或 Sage runtime-error 的证明等级。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_priority_handoff_audit.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_mixed_closure_priority_handoffs.py \
  tests/test_mixed_closure_priority_handoff_audit.py
```

结果：

```text
4 passed
All checks passed!
```
