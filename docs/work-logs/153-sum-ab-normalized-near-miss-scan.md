# wl153 — `sum=A+B` normalized near-miss scan

日期：2026-06-09

## 1. 本轮问题

wl152 发现样例：

```text
P/g,Q/g = 6,7
|(P-Q)/g| = 1
```

这个形状很漂亮，容易让人误以为：

```text
near-miss 归一化后总是相邻数。
```

这轮写一个小扫描，专门确认这件事。

普通话说：

```text
先别被 6 和 7 骗了。
我们要看它是规律，还是刚好长得好看。
```

---

## 2. 新 helper

新增：

```text
sum_ab_same_orientation_normalized_near_miss_summary(max_m=...)
```

扫描口径：

```text
same orientation
primitive Euclid 参数
shared_numerator > 0
other / failed 两条重构边恰好一条过平方
```

记录：

```text
total_near_misses
abs_difference_over_gcd_counts
normalized_pair_counts
examples_by_abs_difference
```

其中：

```text
g = gcd(P,Q)
abs_difference_over_gcd = |(P-Q)/g|
normalized_pair = (P/g,Q/g)
```

普通话说：

```text
它只看“三条边已过，第四条没过”的 near-miss。
它不是反例搜索，也不是证明。
```

---

## 3. 小范围结果

运行：

```text
max_m = 8,12,16,20
```

得到：

```text
max_m=8  total=6   abs1=2  buckets=3
max_m=12 total=6   abs1=2  buckets=3
max_m=16 total=14  abs1=2  buckets=7
max_m=20 total=20  abs1=2  buckets=10
```

`max_m=20` 的 bucket 首项：

```text
|(P-Q)/g| = 1,11,17,23,38,61,178,231,377,391
```

每个 bucket 当前都是 2 个，通常对应交换：

```text
(P/g,Q/g)  <->  (Q/g,P/g)
```

普通话说：

```text
差 1 没有扩散成大规律。
它只是目前最小的一对交换 near-miss。
```

---

## 4. 典型样例

`max_m=20` 中每个 bucket 取一个例子：

```text
abs=1:
  odd  (4,1)  (7,2)   pair=(6,7)     sum/g=13

abs=11:
  odd  (7,2)  (13,4)  pair=(119,130)  sum/g=249

abs=17:
  even (6,1)  (8,3)   pair=(28,11)    sum/g=39

abs=23:
  odd  (2,1)  (19,8)  pair=(99,76)    sum/g=175

abs=38:
  even (4,1)  (4,3)   pair=(45,7)     sum/g=52
```

注意：

```text
abs=1 的 pair=(6,7) 是最漂亮的，
但其他 pair 并不相邻。
```

普通话说：

```text
如果要找证明，不能只靠“相邻数”这条直觉。
```

---

## 5. 当前判断

可以说：

```text
near-miss 归一化后会自然成交换对出现。
|(P-Q)/g|=1 在 max_m<=20 只出现一对交换样例。
```

不能说：

```text
near-miss 总是相邻 pair。
差 1 是普遍规律。
扫描证明了非退化分支不可能。
```

更靠谱的方向是：

```text
研究 normalized pair 是否能继续生成更小的 same-orientation 结构。
```

普通话说：

```text
6,7 不是钥匙本身；
它更像一把钥匙露出来的齿形。
我们要研究整把钥匙怎么切出来。
```

---

## 6. 下一步

下一步可以尝试两个方向：

```text
1. 对 normalized pair=(P/g,Q/g) 检查是否仍可作为某种更小 shared-leg 配对。
2. 对交换对做商掉对称后的统计，避免把同一个 near-miss 数两遍。
```

如果第 1 点成立，才可能通向递降：

```text
(N,P,Q) -> (N',P',Q')
```

如果第 1 点失败，也有价值：

```text
说明 gcd-normalized pair 只是观测量，不是递降对象。
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
