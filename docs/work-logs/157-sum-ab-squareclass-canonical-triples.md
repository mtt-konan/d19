# wl157 — `sum=A+B` squareclass canonical triples

日期：2026-06-09

## 1. 本轮问题

wl156 发现：

```text
同一个 failing squareclass 下，经常有 4 条 near-miss 记录。
```

但其中一半只是：

```text
P/Q 交换
```

所以这轮把交换对压掉，只看真正不同的 triple。

普通话说：

```text
先把镜子里的重复影子擦掉，
再看房间里到底有几件东西。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissSummary
```

新增：

```text
canonical_triples_by_failing_squareclass
```

定义：

```text
(N,P,Q) -> (N, min(P,Q), max(P,Q))
```

注意：

```text
这里只消掉 P/Q 交换；
不把 N 也排序掉。
```

普通话说：

```text
N 是共享腿，角色特殊，不能和 P/Q 混在一起随便排序。
```

---

## 3. max_m<=40 观察

按 failing squareclass 排名前几项：

```text
sc=17:
  count=4
  canonical_count=2
  triples:
    (7,24,28)
    (28,7,45)

sc=5713:
  count=4
  canonical_count=2
  triples:
    (231,476,520)
    (476,231,765)

sc=10193:
  count=4
  canonical_count=2
  triples:
    (304,297,403)
    (403,304,396)

sc=507809:
  count=4
  canonical_count=2
  triples:
    (425,168,572)
    (572,315,425)

sc=730:
  count=2
  canonical_count=1
  triple:
    (451,87,780)
```

普通话说：

```text
count=4 不是四个完全不同的东西。
它通常是两个真正 triple，每个再带一个 P/Q 交换影子。
```

---

## 4. 关键形状

最小的两个 family：

```text
sc=17:
  (7,24,28) -> (28,7,45)

sc=5713:
  (231,476,520) -> (476,231,765)
```

这两个形状很像：

```text
(N,P,Q) -> (Q, N, ?)
```

但第三项不是简单的：

```text
P+Q
P-Q
sqrt(...)
```

例如：

```text
(7,24,28) -> (28,7,45)
```

第三项 `45` 满足：

```text
28^2 + 45^2 = 53^2
```

普通话说：

```text
它像是“把失败边 Q 提升成新共享腿，
再找一个新的 passing partner”。
```

这如果能公式化，就可能靠近递降或链式结构。

---

## 5. 当前判断

可以说：

```text
failing squareclass 分组后，P/Q 交换噪声可以被 canonical triple 去掉。
小范围内 count=4 的 squareclass 通常对应两个 canonical triples。
```

不能说：

```text
已经找到 triple 变换公式。
已经证明可以递降。
这些 family 一定能无限延伸。
```

普通话说：

```text
现在我们看见了“两个节点一组”的影子；
还没有看见边的公式。
```

---

## 6. 下一步

下一步不要先扫更大。

应该先对两个 canonical triples 做代数解释：

```text
(7,24,28) -> (28,7,45)
(231,476,520) -> (476,231,765)
```

问题：

```text
1. 第二个 triple 的 N 是否总是第一个 triple 的失败边？
2. 第二个 triple 的 passing partner 是否由同一条 Pythagorean 参数变换生成？
3. 这个变换能否反向减小？
```

如果第 3 点成立：

```text
非退化 near-miss -> 更小 near-miss
```

才可能变成真正递降。

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
