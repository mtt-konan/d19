# wl158 — `sum=A+B` squareclass family edges

日期：2026-06-09

## 1. 本轮问题

wl157 看到了同一 failing squareclass 下的两个 canonical triples：

```text
(7,24,28)
(28,7,45)
```

看起来像：

```text
(N,P,Q) -> (Q,N,R)
```

这轮把这种关系写成显式 edge。

普通话说：

```text
不是只看两块石头摆在一起，
而是问它们之间有没有一条边。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissSummary
```

新增：

```text
family_edges_by_failing_squareclass
```

每条 edge 记录：

```text
source
target
target_uses_source_failed_leg
target_uses_source_shared_leg
```

当前 edge 判定很保守：

```text
target 的 N 等于 source 的某条非共享边
target 的某条非共享边等于 source 的 N
```

普通话说：

```text
下一组把上一组的一条边拿来当共享腿，
同时保留上一组的共享腿当普通边。
```

---

## 3. max_m<=40 观察

出现两个 canonical triples 的 squareclass 都有这种 edge：

```text
sc=17:
  (7,24,28) <-> (28,7,45)

sc=5713:
  (231,476,520) <-> (476,231,765)

sc=10193:
  (304,297,403) <-> (403,304,396)

sc=507809:
  (425,168,572) <-> (572,315,425)

sc=51137:
  (7667,9212,13260) <-> (9212,7667,14805)
```

普通话说：

```text
这些不是随便同一个 squareclass。
它们确实共享一种“边换角色”的关系。
```

---

## 4. 重要降温

edge 是双向的：

```text
(7,24,28) -> (28,7,45)
(28,7,45) -> (7,24,28)
```

所以现在不能说：

```text
这就是递降。
```

普通话说：

```text
递降需要方向感。
现在看到的是一条无向边，
不是一条单向下坡路。
```

---

## 5. 当前判断

可以说：

```text
同一 failing squareclass 下的两个 canonical triples 有明确 edge 关系。
这个 edge 把某条非共享边提升成新共享腿，并把旧共享腿保留下来。
```

不能说：

```text
已经找到递降。
edge 一定能无限延伸成链。
same orientation 已关闭。
```

普通话说：

```text
现在我们至少知道两块石头之间真的有桥。
但桥通向哪里，还没有证明。
```

---

## 6. 下一步

下一步应给 edge 加方向候选。

可能的方向指标：

```text
min(N,P,Q)
max(N,P,Q)
N
failing leg
hypotenuse of passing side
Euclid 参数大小
```

真正有用的方向必须满足：

```text
沿 edge 单调变小
```

如果没有任何自然量单调变小：

```text
family edge 更像对称结构，不像递降结构。
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
