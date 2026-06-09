# wl213 — focus sample template constraints

日期：2026-06-09

## 1. 本轮目标

wl212 把小样本 `(7,45,24,28)` 写成了数值方程网络。

本轮再提升一层：

```text
从数值网络变成符号模板。
```

普通话说：

```text
不要只写：

B = 45 = 3*(4^2-1^2) = 1*(7^2-2^2)

还要写：

B = v*(r^2-s^2) = w*(x^2-y^2)
```

这样后续才能做消元、递降或模检验。

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
tests/test_equationize_closure_first_near_miss.py
```

`equationize_sample(...)` 新增：

```text
template_constraints
```

它包含：

```text
scope
passed_edge_templates
shared_constraints
closure_constraint
missing_square_constraint
```

注意：

```text
template_constraints 是从已有 Euclid ledger 自动生成的。
不是把 (7,45,24,28) 硬编码进去。
```

---

## 3. 小样本模板

样本：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
missing = A-N2
```

scope：

```text
focus_bucket_sum_ab_B_odd_odd_N1_even_even
```

三条已通过边：

```text
A  = u*(p^2-q^2)
N1 = u*(2*p*q)

u=1, p=4, q=3
```

```text
B  = v*(r^2-s^2)
N1 = v*(2*r*s)

v=3, r=4, s=1
```

```text
B  = w*(x^2-y^2)
N2 = w*(2*x*y)

w=1, x=7, y=2
```

共享变量给出两条模板等式：

```text
v*(r^2-s^2) = w*(x^2-y^2)
u*(2*p*q)  = v*(2*r*s)
```

closure：

```text
N1 + N2 = A + B
```

缺边问题：

```text
A^2 + N2^2 = square?
```

普通话说：

```text
这个 focus 样本现在已经变成一个符号系统：

B  被两套 odd-leg 公式生成；
N1 被两套 even-leg 公式生成；
closure 把 N2 接进来；
最后问 A-N2 能不能也是勾股边。
```

---

## 4. 下一步

下一步不必再整理账本，可以直接从模板出发：

```text
1. 用 u*(2pq)=v*(2rs) 研究 N1 的因子分配。
2. 用 v*(r^2-s^2)=w*(x^2-y^2) 研究 B 的双 odd-leg 表示。
3. 用 N1+N2=A+B 消去 N2 或 A。
4. 检查 A^2+N2^2 是否被模条件挡住。
```

一个更窄的第一步：

```text
先把小样本赋值去掉，只研究：

B odd/odd
N1 even/even
closure sum=A+B
missing A-N2
```

也就是这个 scope：

```text
focus_bucket_sum_ab_B_odd_odd_N1_even_even
```

---

## 5. 边界

可以说：

```text
focus 样本已经从数值 near-miss 提升为符号模板。
```

不能说：

```text
模板已经证明这个桶无解。
```

原因：

```text
本轮只是建立模板。
还没有执行消元、递降或平方剩余分析。
```

---

## 6. 验证

已运行：

```text
uv run pytest \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py \
  tests/test_closure_first_three_square_search.py -q
```

结果：

```text
14 passed
```

已运行：

```text
uv run ruff check \
  scripts/theory/equationize_closure_first_near_miss.py \
  tests/test_equationize_closure_first_near_miss.py
```

结果：

```text
All checks passed
```
