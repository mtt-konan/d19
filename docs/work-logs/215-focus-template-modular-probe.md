# wl215 — focus template modular probe

日期：2026-06-09

## 1. 本轮目标

wl214 给 focus 模板补上了 Euclid side conditions。

本轮做一个小模数诊断：

```text
这些模板约束 + closure 之后，
A^2 + N2^2 是否已经被小模数平方剩余挡住？
```

普通话说：

```text
先别急着证明。
先问最便宜的一层：

模 3、5、7 下，第四条边还有没有可能是平方？
```

---

## 2. 新脚本

新增：

```text
scripts/theory/probe_focus_template_modular.py
tests/test_probe_focus_template_modular.py
```

脚本枚举 focus 模板：

```text
A  = u*(p^2-q^2)
N1 = u*(2*p*q)

B  = v*(r^2-s^2)
N1 = v*(2*r*s)

B  = w*(x^2-y^2)
N2 = w*(2*x*y)

N1 + N2 = A + B
```

并检查：

```text
A^2 + N2^2 是否为平方剩余
```

输出分层计数：

```text
total_assignments
side_condition_pass
shared_constraint_pass
closure_pass
missing_square_pass
missing_square_obstructed
sample_survivors
```

---

## 3. 重要边界

这个脚本是：

```text
诊断工具
```

不是：

```text
证明工具
```

原因：

```text
1. 它只看有限小模数。
2. 它只看 residue 层，不看整数大小、valuation、真实参数提升。
3. 奇偶条件只在偶模数中直接表达；奇数模数下脚本不会检查 parity。
```

普通话说：

```text
如果小模数杀光了，那会是很强线索。
如果小模数没杀光，也不能说明无证明。
```

---

## 4. 本轮运行

已运行：

```text
uv run python scripts/theory/probe_focus_template_modular.py 3 5 7 --sample-limit 2
```

结果摘要：

| modulus | closure_pass | missing_square_pass | obstructed |
|---:|---:|---:|---:|
| 3 | 128 | 128 | 0 |
| 5 | 5120 | 4096 | 1024 |
| 7 | 51840 | 41472 | 10368 |

观察：

```text
mod 3 完全没有挡掉第四边。
mod 5、7 会挡掉一部分 closure residue，
但仍然有大量 survivor。
```

普通话说：

```text
单个小模数的平方剩余障碍，目前没有直接把这个 focus 模板杀光。
```

---

## 5. 下一步

更合理的后续不是盲目加大模数，而是：

```text
1. 加入 CRT 多模数合并，看 survivor 是否快速下降。
2. 加入 p-adic valuation 条件，而不是只看 residue。
3. 对 shared constraints 做因子分配分析：
   v*(r^2-s^2)=w*(x^2-y^2)
   u*(2pq)=v*(2rs)
```

尤其注意：

```text
wl108 / wl109 已经提醒过：
纯 residue survivor 不能当真实候选。
```

所以这条路线后续必须从 residue 走向 valuation 或 exact 参数。

---

## 6. 验证

已运行：

```text
uv run pytest \
  tests/test_probe_focus_template_modular.py \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py \
  tests/test_closure_first_three_square_search.py -q
```

结果：

```text
16 passed
```

已运行：

```text
uv run ruff check \
  scripts/theory/probe_focus_template_modular.py \
  tests/test_probe_focus_template_modular.py
```

结果：

```text
All checks passed
```
