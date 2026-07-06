# wl315 - Sage local witness probe

日期：2026-07-07

## 一句话结论

priority top-4 residual cover 现在有 bad-prime Qp local witness probe。

普通话说：PARI `ell2cover` 说这些 2-cover 是 everywhere locally soluble。现在我们不只保存这句话，
而是在 Sage 里对每个 target quartic 的坏素数找显式局部 witness：

```text
要么 leading coefficient 是 Qp 平方，给出无穷远点；
要么找到一个有理 x，使 f(x) 是 Qp 平方，给出有限 Qp 点。
```

## 新增脚本

```text
scripts/theory/sage_probe_mixed_closure_local_witnesses.py
tests/test_sage_probe_mixed_closure_local_witnesses.py
```

## 真实运行

第一组：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  --handoff results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_local_witnesses.json \
  --timeout 60 \
  --search-bound 300 \
  --max-denominator-power 3 \
  --strict
```

输出：

```text
status=ok
all_bad_primes_witnessed=True
```

第二组：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  --handoff results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_local_witnesses.json \
  --timeout 60 \
  --search-bound 300 \
  --max-denominator-power 3 \
  --strict
```

输出：

```text
status=ok
all_bad_primes_witnessed=True
```

合并到 priority handoff audit 后：

```text
ready=True
groups_checked=2
local_witness_status_counts.ok=2
violations=[]
```

## 边界

这不是 residual cover 无点证明。

它证明的是 local side 的显式 witness：

```text
这四个 priority target cover 在脚本列出的坏素数处都有 Qp 点 witness。
```

它不证明：

```text
cover 没有 Q 点；
Selmer gap 已经严格变成 Sha[2] 元素；
bounded search 可以当成无点证明。
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
4 passed
All checks passed!
```
