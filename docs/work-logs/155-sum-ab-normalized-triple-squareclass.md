# wl155 — `sum=A+B` normalized triple squareclass

日期：2026-06-09

## 1. 本轮问题

wl154 把 near-miss 从 pair 提升到 triple：

```text
(N',P',Q') = (N,P,Q) / gcd(N,P,Q)
```

下一步自然是看：

```text
N'^2 + P'^2
N'^2 + Q'^2
```

各自属于哪个 squareclass。

普通话说：

```text
不要只问“差多少”。
要问“失败那条边为什么不是平方，它差在哪类平方因子上”。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissExample
```

新增：

```text
normalized_other_squareclass
normalized_failed_squareclass
```

规则：

```text
squareclass = 正整数平方自由部分
squareclass = 1 表示这个数本身是平方
```

例如：

```text
(N',P',Q') = (7,24,28)

7^2 + 24^2 = 625 = 25^2
squareclass = 1

7^2 + 28^2 = 833 = 49*17
squareclass = 17
```

普通话说：

```text
通过边的 squareclass 是 1；
失败边的 squareclass 告诉我们它被哪个平方类卡住。
```

---

## 3. 小范围分布

对 `max_m=20`：

```text
total near-miss = 20
passing squareclass:
  1: 20

failing squareclass:
  17: 4
  730: 2
  5713: 4
  10193: 2
  14177: 2
  24634: 2
  1517266: 2
  55141697: 2
```

对 `max_m=30`：

```text
total near-miss = 32
passing squareclass:
  1: 32

failing squareclass unique count = 12
```

普通话说：

```text
通过边当然都是 1。
失败边不是固定一个 squareclass。
所以“所有 near-miss 都被同一个素数卡住”这条路暂时不成立。
```

---

## 4. 典型样例

`max_m=30` 中几个例子：

```text
abs=1:
  triple=(7,24,28)
  pass_sc=1
  fail_sc=17

abs=11:
  triple=(231,476,520)
  pass_sc=1
  fail_sc=5713

abs=17:
  triple=(147,140,55)
  pass_sc=1
  fail_sc=24634

abs=23:
  triple=(403,396,304)
  pass_sc=1
  fail_sc=10193

abs=38:
  triple=(28,45,7)
  pass_sc=1
  fail_sc=17
```

可以看到：

```text
fail_sc=17 不只出现在 (7,24,28)。
fail_sc=5713、10193 等也会在不同 bucket 复现。
```

普通话说：

```text
不是一个固定障碍。
但按 squareclass 分组，可能比按 delta 或 abs bucket 分组更像“家族”。
```

---

## 5. 当前判断

可以说：

```text
normalized triple 保留了一边通过、一边失败的 squareclass 结构。
失败 squareclass 在小范围内是多样的，不是单一素数障碍。
```

不能说：

```text
squareclass 方法失败。
失败 squareclass 随机。
same orientation 已关闭。
```

更准确的判断是：

```text
单一 squareclass obstruction 不明显；
squareclass family grouping 仍值得看。
```

---

## 6. 下一步

下一步建议不要再只按：

```text
delta
|(P-Q)/g|
```

排序。

可以改成按：

```text
failing squareclass
normalized triple
Euclid 参数
```

三者一起分组。

如果同一个 failing squareclass 对应一族参数公式，
才可能进一步抽出模条件或递降结构。

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
