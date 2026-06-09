# wl128 — sum-only entrypoint boundary

日期：2026-06-09

## 1. 本轮问题

审计反复提到一个危险归约：

```text
N1 + N2 = A + B
```

这只描述 inside-square / sum-only 闭合。full-plane 反例还允许差关系和 `|A-B|` 目标：

```text
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}
```

旧脚本里还有一些入口名字像“closure scan / no-solution prover”，但实际只跑 sum-only。这会误导后续 agent，把正方形内结论接到全平面结论上。

普通话说：

```text
旧工具只看“两个数相加等于 A+B”这一扇门；
现在的问题有四扇门。
旧工具没坏，但门牌必须写清楚。
```

---

## 2. 处理范围

本轮只给三个最容易误读的入口加边界：

```text
src/rational_distance/concordant/dual_closure_sieve.py
scripts/prove_no_solution_multi_first.py
scripts/partner/full_gm_closure_scan.py
```

不改算法，不重跑历史结果。

---

## 3. 修改

### `dual_closure_sieve.py`

模块 docstring 现在明确：

```text
historical sum-only / inside-square
killed_at_modulus(..., full_plane=False)
not a full-plane GEN-CLOSURE proof tool
```

并提醒当前 full-plane 工作必须保留四关系：

```text
{N_i+N_j, |N_i-N_j|} ∩ {A+B, |A-B|} != ∅
```

### `prove_no_solution_multi_first.py`

脚本 docstring 和 `--help` 现在写明：

```text
Historical sum-only / inside-square multi-N-first driver;
not a full-plane GEN-CLOSURE proof tool.
```

### `full_gm_closure_scan.py`

脚本 docstring 和 `--help` 现在写明：

```text
Historical sum-only / inside-square G_M closure scan;
not a full-plane GEN-CLOSURE scan.
```

这个脚本名字里的 `full_gm` 指“扫完整 G_M 顶点集”，不是“full-plane closure”。

---

## 4. 新增测试

文件：

```text
tests/test_sum_only_provenance.py
```

测试要求以下入口文本都包含：

```text
sum-only
inside-square
full-plane
```

覆盖：

```text
dual_closure_sieve module docstring
prove_no_solution_multi_first.py --help
scripts/partner/full_gm_closure_scan.py --help
```

TDD 红灯时，三处都缺少至少一个边界词。

---

## 5. 能说什么，不能说什么

可以说：

```text
旧 sum-only / inside-square 入口现在会显式提醒边界。
后续读 help 或模块说明时，不应再把这些入口误当 full-plane 证明。
```

不能说：

```text
dual_closure_sieve 已经升级为 full-plane。
prove_no_solution_multi_first 已经可证明全平面无解。
full_gm_closure_scan 的旧 0 hit 已经等于 full-plane 0 hit。
```

这轮只是防误用。真正的 full-plane 路径仍是：

```text
chain_closure_mod_sieve(full_plane=True)
exact GEN-CLOSURE
full-plane delta scanner
```

---

## 6. 验证

运行：

```text
uv run pytest tests/test_sum_only_provenance.py -q
```

结果：

```text
2 passed
```

后续还应运行相关测试和全量测试。

---

## 7. 下一步

工程安全清理已经覆盖三块高风险入口：

```text
safe_sieve coprime guard
stale proof_status / results provenance
sum-only / inside-square entrypoint boundary
```

后续更值得回到理论线：

```text
rational-ratio λ
closure-first near-miss equationization
D4 对称变量
fixed-ratio / Yang Ji 推广
```
