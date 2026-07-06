# wl299 - PARI BSD diagnostics for mixed closure residuals

日期：2026-07-06

## 一句话结论

新增 PARI analytic/BSD 条件性诊断脚本。它能确认 `(115,297) AA` 这条最小目标 residual
有 `analytic_rank=0`，但全量 `AA/BB` 在小预算下大多 timeout。

普通话说：这条路能提供“很像 rank 0 + Sha[2]”的证据，但不是严格证明，也不是批量按钮。

## 新增脚本

```text
scripts/theory/pari_bsd_mixed_closure_residuals.py
tests/test_pari_bsd_mixed_closure_residuals.py
```

脚本特性：

- 逐条子进程运行，避免某条曲线卡死整批；
- 支持 `--curve`、`--target`、`--limit`；
- 支持 `--timeout`；
- 支持 `--stack-bytes`，因为 `ellanalyticrank` 默认 PARI stack 会溢出；
- 输出 `evidence_level = bsd-conditional-diagnostic`。

记录字段：

```text
root_number
ellrank_lower / ellrank_upper / ellrank_sha2_lower
analytic_rank
analytic_leading_value
bsd_factor
```

其中 `bsd_factor` 是 PARI `ellbsd(E)` 的输出。它是 BSD 公式里的实数因子，不是 Sha 阶。

## 目标样本结果

命令：

```bash
uv run python scripts/theory/pari_bsd_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_bsd_mixed_115_297_AA.jsonl \
  --target 115,297,AA \
  --timeout 20
```

结果：

```text
[1/1] (115,297) AA status=ok analytic_rank=0
status_counts={'ok': 1}
analytic_rank_counts={'0': 1}
```

关键字段：

```text
root_number = 1
ellrank = [0,2]
analytic_rank = 0
analytic_leading_value = 4.72955644264359
bsd_factor = 0.295597277665225
evidence_level = bsd-conditional-diagnostic
```

解释：

```text
这支持“rank 0 + Sha[2]”图景，但不是无条件 rank-0 证书。
```

## AA/BB 小预算批处理

命令：

```bash
uv run python scripts/theory/pari_bsd_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_bsd_mixed_aabb_t10.jsonl \
  --curve AA \
  --curve BB \
  --timeout 10
```

结果：

```text
status_counts={'ok': 2, 'pari-error': 2, 'timeout': 8}
analytic_rank_counts={'0': 2}
```

成功的两条：

```text
(115,297) AA
(575,4641) AA
```

两条 `pari-error` 是 PARI stack overflow。对 `(567,3757) BB` 单独加到 `1GB` stack：

```bash
uv run python scripts/theory/pari_bsd_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_bsd_mixed_567_3757_BB_stack1g.jsonl \
  --target 567,3757,BB \
  --timeout 20 \
  --stack-bytes 1073741824
```

仍然：

```text
status_counts={'timeout': 1}
```

所以这条诊断适合目标样本和低成本 evidence，不适合作为批量收敛主刀。

## 对当前方向的影响

现在 `(115,297) AA` 有三层证据：

```text
rank bounds: [0,2]
Selmer gap / no-point cover: 2 个 explicit Sha[2] candidate covers
analytic/BSD diagnostic: analytic_rank = 0
```

但严格边界仍然是：

```text
不能把 analytic_rank=0 写成无条件 rank=0。
不能把 BSD diagnostic 写成 Sha 证明。
不能把 bounded hyperellratpoints 写成 cover 无点证明。
```

下一步如果要真收敛，应继续攻 `(115,297) AA` cover 3、4 的严格无点证书，或找可引用的
严格 rank/L-value 非零证书。

## 验证

```bash
uv run pytest tests/test_pari_bsd_mixed_closure_residuals.py -q
uv run ruff check \
  scripts/theory/pari_bsd_mixed_closure_residuals.py \
  tests/test_pari_bsd_mixed_closure_residuals.py
```

结果：

```text
3 passed
All checks passed!
```
