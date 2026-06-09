# wl141 — `sum=A+B` same-orientation shared-leg helper

日期：2026-06-09

## 1. 本轮问题

wl140 发现 same orientation 的核心结构：

```text
other = N / (bc)
failed = N / (ad)
```

也就是：

```text
N^2 + (bc)^2 是否为平方
N^2 + (ad)^2 是否为平方
```

这轮把这个结构固化成代码 helper。

普通话说：

```text
不要每次都重新手算 N、bc、ad。
直接让代码把“共享腿 N 的两个勾股方程”吐出来。
```

---

## 2. 新增模型

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
SumAbSameOrientationSharedLegTerms
sum_ab_same_orientation_shared_leg_terms(...)
```

字段：

```text
orientation
slope_terms
scaled_term_terms
shared_numerator
other_denominator
failed_denominator
other_square_equation
failed_square_equation
square_difference
denominator_square_difference
```

其中：

```text
square_difference = [N^2 + (bc)^2] - [N^2 + (ad)^2]
denominator_square_difference = (bc)^2 - (ad)^2
```

测试确认二者相等。

---

## 3. 固定样例

沿用 near-miss 样例：

```text
slope = PythagoreanLegParam(4, 1, "odd")        -> 15/8
scaled = PythagoreanLegParam(7, 2, "odd")       -> 45/28
```

输出：

```text
shared_numerator = 105
other_denominator = 360
failed_denominator = 420
```

所以：

```text
other: 105^2 + 360^2 = 375^2
failed: 105^2 + 420^2 is not square
```

也就是：

```text
同一条腿 105，
搭配 360 成了勾股三角形，
搭配 420 没成。
```

---

## 4. 安全边界

这个 helper 只接受 same orientation：

```text
odd/odd
even/even
```

如果传：

```text
odd/even
even/odd
```

会抛出：

```text
ValueError
```

原因：

```text
mixed orientation 已经由 wl139 的 mod 8 lemma 关闭。
这里不要混用两套论证。
```

---

## 5. 能说什么，不能说什么

可以说：

```text
same orientation 现在有共享腿双勾股方程的代码入口。
后续可以直接参数化 N^2+P^2 和 N^2+Q^2。
```

不能说：

```text
same orientation 已关闭。
sum=A+B 分支已关闭。
shared-leg helper 是证明。
```

它只是把结构暴露出来。

---

## 6. 下一步

下一步建议：

```text
1. 参数化：
   N^2 + P^2 = H1^2
   N^2 + Q^2 = H2^2

2. 将 P=bc、Q=ad 代入。

3. 看是否能推出：
   P=Q
   或者出现递降。
```

普通话说：

```text
现在要证明的不是“某个数不是平方”，
而是“同一个 N 不能同时配出两个合法勾股三角形，除非退化/镜像”。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_shared_leg_terms_expose_square_difference -q
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_shared_leg_terms_reject_mixed_orientation -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
1 passed
All checks passed
```
