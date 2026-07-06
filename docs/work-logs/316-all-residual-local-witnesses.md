# wl316 - all residual local witnesses

日期：2026-07-07

## 一句话结论

27 个 `AA/BB` residual candidate covers 现在都有 bad-prime Qp local witness probe。

普通话说：wl315 先检查了 priority top-4。现在把同一个 Sage local witness 搜索扩到全部
27 个 candidate cover。结果是：251 个坏素数检查全部找到 witness，没有 unresolved。

## 更新脚本

```text
scripts/theory/sage_probe_mixed_closure_local_witnesses.py
tests/test_sage_probe_mixed_closure_local_witnesses.py
```

新增输入模式：

```text
--priorities results/mixed_closure_aabb_residual_cover_priorities.json
```

这会把 priority table 的每一行当成一个 cover target，并保留：

```text
priority
A
B
curve
cover_index
quartic
```

## 真实运行

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --out results/mixed_closure_aabb_residual_local_witnesses.json \
  --timeout 60 \
  --search-bound 300 \
  --max-denominator-power 3 \
  --strict
```

输出：

```text
status=ok
all_bad_primes_witnessed=True
candidate_cover_total=27
bad_prime_check_total=251
unresolved_bad_prime_total=0
```

## 放进 summary gate

partial-result summary 现在额外读取：

```text
results/mixed_closure_aabb_residual_local_witnesses.json
```

关键字段：

```text
residual_local_witness_status.candidate_cover_total = 27
residual_local_witness_status.bad_prime_check_total = 251
residual_local_witness_status.unresolved_bad_prime_total = 0
```

## 边界

这仍然不是 residual cover 无点证明。

它证明的是 local side 的显式 witness 覆盖：

```text
27 个 residual candidate cover 在脚本列出的坏素数处都找到了 Qp 点 witness。
```

它不证明：

```text
这些 cover 没有 Q 点；
Selmer gap 已经严格变成 Sha[2] 元素；
bounded search 可以当作无点证明。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_sage_probe_mixed_closure_local_witnesses.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  tests/test_sage_probe_mixed_closure_local_witnesses.py
```

结果：

```text
6 passed
All checks passed!
```
