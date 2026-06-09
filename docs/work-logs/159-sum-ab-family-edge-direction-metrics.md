# wl159 — `sum=A+B` family edge direction metrics

日期：2026-06-09

## 1. 本轮问题

wl158 发现 family edge 是双向的：

```text
(7,24,28) <-> (28,7,45)
```

所以它本身不是递降。

这轮加几个方向候选指标：

```text
source_max
target_max
target_max_delta
target_n_delta
```

普通话说：

```text
桥是双向的。
现在先看桥的哪一边更低。
```

---

## 2. 新增字段

扩展：

```text
SumAbSquareclassFamilyEdge
```

新增属性：

```text
source_max = max(source)
target_max = max(target)
target_max_delta = target_max - source_max
target_n_delta = target_N - source_N
```

例如：

```text
(7,24,28) -> (28,7,45)

source_max = 28
target_max = 45
target_max_delta = 17
target_n_delta = 21
```

反向：

```text
(28,7,45) -> (7,24,28)

target_max_delta = -17
target_n_delta = -21
```

普通话说：

```text
同一条无向边，反过来走就能让这些量变小。
```

---

## 3. max_m<=40 观察

几个 family edge：

```text
sc=17:
  (7,24,28) -> (28,7,45)
    maxΔ=17, NΔ=21
  reverse:
    maxΔ=-17, NΔ=-21

sc=5713:
  (231,476,520) -> (476,231,765)
    maxΔ=245, NΔ=245
  reverse:
    maxΔ=-245, NΔ=-245

sc=10193:
  (304,297,403) -> (403,304,396)
    maxΔ=0, NΔ=99
  reverse:
    maxΔ=0, NΔ=-99

sc=507809:
  (425,168,572) -> (572,315,425)
    maxΔ=0, NΔ=147
  reverse:
    maxΔ=0, NΔ=-147
```

普通话说：

```text
max 有时不变。
N 更像可用方向指标：
在这些双节点 family 里，总能选一个方向让 N 变小。
```

---

## 4. 重要边界

这仍然不是递降证明。

原因：

```text
1. 目前只看到了同一 squareclass 下两个 canonical triples。
2. 双节点边当然可以选一个方向让 N 变小。
3. 真正递降需要从任意 near-miss 都能生成更小 near-miss。
```

普通话说：

```text
两个人站在桥两头，总有一个人海拔低。
这不等于整张地图一路下坡。
```

---

## 5. 当前判断

可以说：

```text
family edge 可按 N 选出局部下降方向。
max 不是稳定下降指标，因为有 maxΔ=0 的 family。
```

不能说：

```text
N 已经给出全局递降。
family edge 已经关闭 same orientation。
```

普通话说：

```text
N 是目前最像方向感的量。
但它还只是指南针，不是证明。
```

---

## 6. 下一步

下一步应该看：

```text
沿 N 下降方向走到较小 triple 后，
还能不能继续找到同 squareclass 或其他 squareclass 的 edge？
```

也就是从：

```text
pair/family
```

升级成：

```text
graph
```

如果图中每个非最小节点都有出边指向更小 N，
才可能接近递降。

如果图只是很多孤立双节点：

```text
这更像局部对称，不像全局递降。
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
