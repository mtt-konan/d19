# wl161 — `sum=A+B` N-descending graph summary

日期：2026-06-09

## 1. 本轮问题

wl160 用临时脚本观察到：

```text
N-descending family edges 没有继续链。
```

这轮把这个统计做进 summary helper。

普通话说：

```text
不要每次都手算“下坡后还有没有路”。
让工具自己告诉我们。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissSummary
```

新增：

```text
n_descending_edge_count
n_descending_continuation_count
```

定义：

```text
n_descending_edge_count:
  family_edges 中 decreases_n=True 的边数

n_descending_continuation_count:
  这些下降边的 target 是否还能作为另一条下降边的 source
```

普通话说：

```text
第一项问“有几条下坡边”。
第二项问“下坡以后还能不能继续下坡”。
```

---

## 3. 小范围结果

扫描：

```text
max_m=8:
  total=6
  n_edges=1
  continuations=0

max_m=20:
  total=20
  n_edges=2
  continuations=0

max_m=40:
  total=54
  n_edges=5
  continuations=0

max_m=60:
  total=116
  n_edges=9
  continuations=0
```

普通话说：

```text
范围变大后，下坡边变多了。
但它们仍然没有接成长链。
```

---

## 4. 当前判断

可以说：

```text
当前 family edge 图像更像孤立双节点。
N-descending edge 暂时没有形成连续下降链。
```

不能说：

```text
递降路线彻底失败。
same orientation 已关闭。
near-miss family 不重要。
```

普通话说：

```text
这条路不像直接证明主路；
但它仍然告诉我们 same-orientation near-miss 有局部成族结构。
```

---

## 5. 对下一步的影响

不建议继续单纯扩大：

```text
max_m
```

因为目前扩大范围只得到：

```text
更多孤立双节点
```

更值得做的是回到参数层：

```text
为什么 (7,24,28) 会连到 (28,7,45)？
为什么 (231,476,520) 会连到 (476,231,765)？
```

如果这些 edge 来自一个可逆对称变换：

```text
它更像分类结构。
```

如果存在额外跨 family edge：

```text
才可能重新接近递降。
```

---

## 6. 建议切换焦点

这条 near-miss family 线已经有足够诊断工具。

下一步更建议回到主目标之一：

```text
有理比例 λ 的 closure theorem
或 Yang Ji / A=kB 特殊线证明样板
```

普通话说：

```text
near-miss 这条小路已经探到一个岔口：
它有结构，但暂时不像直接通向山顶。
该留好路标，然后回主路。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_normalized_near_miss_summary_counts_patterns -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
29 passed
393 passed, 2 warnings
```
