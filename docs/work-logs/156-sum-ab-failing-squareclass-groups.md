# wl156 — `sum=A+B` failing squareclass groups

日期：2026-06-09

## 1. 本轮问题

wl155 建议：

```text
不要只按 delta 或 |(P-Q)/g| 排序。
改成按 failing squareclass 分组。
```

这轮把这个分组直接做进 summary helper。

普通话说：

```text
如果第四条边不是平方，
那就先问它属于哪个“失败平方类”。
同一个失败平方类下面，可能藏着同一族 near-miss。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissSummary
```

新增：

```text
failing_squareclass_counts
examples_by_failing_squareclass
```

注意：

```text
failing squareclass 不是固定取 normalized_failed_squareclass。
如果 failed 边通过、other 边失败，就取 normalized_other_squareclass。
```

普通话说：

```text
哪条边失败，就拿哪条边的 squareclass。
这样交换 pair 不会被记错。
```

---

## 3. 小范围分布

扫描结果：

```text
max_m=8:
  total=6
  unique failing squareclass=2
  top:
    17: 4
    24634: 2

max_m=20:
  total=20
  unique failing squareclass=8
  repeated:
    17: 4
    5713: 4

max_m=30:
  total=32
  unique failing squareclass=12
  repeated:
    17: 4
    5713: 4
    10193: 4
    507809: 4

max_m=40:
  total=54
  unique failing squareclass=22
  repeated:
    17: 4
    5713: 4
    10193: 4
    51137: 4
    507809: 4
```

普通话说：

```text
多数 squareclass 只出现交换对的 2 次。
但有些 squareclass 稳定出现 4 次，
说明它合并了不止一个 abs bucket。
```

---

## 4. 例子：squareclass 17

`fail_sc=17` 下：

```text
odd  (4,1) (7,2)
  diff/g = -1
  triple = (7,24,28)

odd  (7,2) (4,1)
  diff/g = 1
  triple = (7,28,24)

even (4,1) (4,3)
  diff/g = 38
  triple = (28,45,7)

even (4,3) (4,1)
  diff/g = -38
  triple = (28,7,45)
```

它合并了两个不同的 abs bucket：

```text
abs=1
abs=38
```

普通话说：

```text
按 abs 看，它们像两件事。
按 failing squareclass 看，它们可能是一家人。
```

---

## 5. 例子：squareclass 5713

`fail_sc=5713` 下：

```text
odd  (7,2)  (13,4)
  diff/g = -11
  triple = (231,476,520)

odd  (13,4) (7,2)
  diff/g = 11
  triple = (231,520,476)

even (13,4) (20,13)
  diff/g = 178
  triple = (476,765,231)

even (20,13) (13,4)
  diff/g = -178
  triple = (476,231,765)
```

这里也合并了：

```text
abs=11
abs=178
```

而且 triple 里出现了数字轮换：

```text
231, 476, ...
```

普通话说：

```text
这不像随机 delta。
更像某种变换把一组 near-miss 送到另一组 near-miss。
```

---

## 6. 当前判断

可以说：

```text
failing squareclass grouping 比 abs bucket 更能合并 near-miss。
一些 squareclass 在小范围内稳定出现 4 次：两组参数，各自再加交换。
```

不能说：

```text
已经找到递降。
squareclass=17 或 5713 代表全局族。
same orientation 已关闭。
```

普通话说：

```text
我们看到的是门缝，不是房间。
但这条门缝比 delta 更像通往结构。
```

---

## 7. 下一步

下一步应研究同一 failing squareclass 下的 triple 变换。

最小目标：

```text
(7,24,28) -> (28,45,7)
(231,476,520) -> (476,765,231)
```

问：

```text
这是不是统一公式？
它是否来自 Pythagorean parameter transformation？
它是否能反向变小，从而形成递降？
```

如果能把这类变换写成公式，
那比继续扫更多 delta 更有理论价值。

---

## 8. 验证

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
