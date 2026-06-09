# wl160 — `sum=A+B` N-descending family edge graph

日期：2026-06-09

## 1. 本轮问题

wl159 说明：

```text
family edge 可以按 N 选出局部下降方向。
```

但这还不等于递降。

这轮把方向变成布尔字段，并看小范围图里能不能连续走下去。

普通话说：

```text
不是只问“这一步能不能下坡”，
而是问“下坡之后还有没有下一步”。
```

---

## 2. 新增字段

扩展：

```text
SumAbSquareclassFamilyEdge
```

新增：

```text
decreases_n
decreases_max
```

定义：

```text
decreases_n   <=> target_N < source_N
decreases_max <=> max(target) < max(source)
```

例子：

```text
(7,24,28) -> (28,7,45):
  decreases_n = False
  decreases_max = False

(28,7,45) -> (7,24,28):
  decreases_n = True
  decreases_max = True
```

普通话说：

```text
同一条桥，反向走才是下坡。
```

---

## 3. max_m<=60 图观察

用 canonical triple 当节点。

只保留：

```text
decreases_n = True
```

得到：

```text
total near-miss = 116
N-descending edges = 9
nodes with outgoing N-desc edge = 9
nodes with incoming N-desc edge = 9
continued descending chains = 0
```

典型边：

```text
sc=17:
  (28,7,45) -> (7,24,28)
  NΔ=-21
  maxΔ=-17

sc=5713:
  (476,231,765) -> (231,476,520)
  NΔ=-245
  maxΔ=-245

sc=10193:
  (403,304,396) -> (304,297,403)
  NΔ=-99
  maxΔ=0

sc=507809:
  (572,315,425) -> (425,168,572)
  NΔ=-147
  maxΔ=0
```

普通话说：

```text
现在看到的是很多“一步下坡”。
但下去以后没有继续下坡的边。
```

---

## 4. 当前判断

可以说：

```text
family edge 可以按 N 选方向。
小范围内 N-descending edge 像孤立双节点的下坡边。
max 不够稳定，因为有 maxΔ=0。
```

不能说：

```text
已经得到递降。
near-miss 图会沿 N 一直下降。
same orientation 已关闭。
```

普通话说：

```text
N 是指南针，但地图现在还是断的。
```

---

## 5. 对路线的影响

这对“递降证明”是一个降温信号。

如果递降存在，可能还缺少一种 edge：

```text
跨 failing squareclass 的 edge
或不只来自 count=4 family 的 edge
或回到 Euclid 参数层的 edge
```

普通话说：

```text
现在这条桥只能从 A 走到 B。
要证明一路下山，还需要 B 后面接着有路。
```

---

## 6. 下一步

下一步不建议继续盲目加大 max_m。

更合理的是：

```text
1. 回到 Euclid 参数层，解释 edge 为什么存在。
2. 看 edge 的两个 triple 是否来自明确参数变换。
3. 如果参数变换可逆且有不变量，再判断是否可能递降。
```

如果参数变换只是一个对称操作：

```text
这条 near-miss family 路线更像结构分类，不像证明主路。
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
