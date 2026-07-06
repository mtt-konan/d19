# wl305 - Sage residual handoff probe

日期：2026-07-07

## 一句话结论

`(115,297) AA` 的 residual handoff 现在有可复跑的 Sage probe。

普通话说：我们没有证明两个 cover 无点，但已经把 Sage 能做和不能做的事情固定成脚本输出。
当前 Sage 严格 rank 证明仍然卡住，并且错误信息正好指向 `Sha[2]`。

## 新增脚本

```text
scripts/theory/sage_probe_mixed_closure_handoff.py
tests/test_sage_probe_mixed_closure_handoff.py
```

脚本输入：

```text
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json
```

脚本输出：

```text
rank_bounds
rank_proof_status
rank_probable
selmer_rank
torsion_two_dimension
每个目标 cover 的 genus
每个目标 cover 的 Sage bounded rational_points 结果
```

## 真实运行

基础 probe：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

输出：

```text
wrote Sage handoff probe to results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4_sage_probe.json
status=ok
rank_bounds=[0, 2]
rank_proof_status=runtime-error
cover_point_counts=[0, 0]
```

关键 JSON：

```text
rank_bounds = [0, 2]
rank_probable = 0
rank_proof_status = runtime-error
rank_proof_error = rank not provably correct (lower bound: 0)
selmer_rank = 4
torsion_invariants = [2, 2]
torsion_two_dimension = 2
cover 3 genus = 1, rational_point_count = 0 at bound 100
cover 4 genus = 1, rational_point_count = 0 at bound 100
```

Sage stdout 明确提示：

```text
This could be because Sha(E/Q)[2] is nontrivial.
```

## second descent 尝试

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4_sage_probe_2descent13.json \
  --timeout 45 \
  --point-search-bound 100 \
  --two-descent-second-limit 13
```

结果：

```text
status=timeout
timeout_seconds=45
```

这说明 Sage 的 `two_descent(second_limit=13)` 暂时不是稳定快速的本地严格证书入口。

## 边界

这轮没有把 residual 关掉。

它推进的是：

```text
目标 cover 已确认是 genus 1；
Sage strict rank proof 仍失败；
失败原因与非平凡 Sha[2] 完全一致；
bounded rational_points 没找到点仍只是证据；
second descent 在当前预算下不可作为自动 gate。
```

下一步如果继续严格化，应该转向：

```text
Magma / Mordell-Weil sieve 的可验证 transcript；
Cassels-Tate / Brauer-Manin 解释；
或可引用的严格 analytic rank / L-value 非零证书。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_sage_probe_mixed_closure_handoff.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/sage_probe_mixed_closure_handoff.py \
  tests/test_sage_probe_mixed_closure_handoff.py
```

结果：

```text
4 passed
All checks passed!
```
