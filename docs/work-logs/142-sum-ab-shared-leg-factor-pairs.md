# wl142 — `sum=A+B` shared-leg factor pairs

日期：2026-06-09

## 1. 本轮问题

wl141 已经把 same orientation 暴露成：

```text
N^2 + P^2 = H1^2
N^2 + Q^2 = H2^2
```

其中：

```text
P = bc
Q = ad
```

这轮把每个通过的平方方程进一步写成因子对：

```text
H^2 - P^2 = N^2
(H-P)(H+P) = N^2
```

普通话说：

```text
如果 N 和 P 真的组成勾股三角形，
那 N^2 可以拆成两块：H-P 和 H+P。
```

这比只记录 `H` 更接近递降证明。

---

## 2. 新增字段

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbSameOrientationSharedLegTerms` 新增属性：

```text
other_hypotenuse_factor_pair
failed_hypotenuse_factor_pair
```

格式：

```text
(H - denominator, H + denominator)
```

如果对应平方方程不通过，则返回：

```text
None
```

---

## 3. 固定样例

沿用：

```text
N = 105
P = 360
Q = 420
```

other 通过：

```text
105^2 + 360^2 = 375^2
```

因此：

```text
(375 - 360, 375 + 360) = (15, 735)
```

并且：

```text
15 * 735 = 11025 = 105^2
```

failed 不通过：

```text
105^2 + 420^2 is not square
```

所以：

```text
failed_hypotenuse_factor_pair = None
```

---

## 4. 为什么这有用

same orientation 要同时通过，必须存在两组因子对：

```text
(H1-P)(H1+P) = N^2
(H2-Q)(H2+Q) = N^2
```

也就是：

```text
同一个 N^2 被拆成两种方式，
并且两种拆法分别要恢复 P=bc 和 Q=ad。
```

普通话说：

```text
现在问题不只是“两个数是不是平方”，
而是“同一个平方 N^2 能不能被拆出两个受 Euclid 参数约束的半差”。
```

这很适合下一步做：

```text
因子包含关系
gcd(H-P, H+P)
奇偶性
递降
```

---

## 5. 能说什么，不能说什么

可以说：

```text
same orientation 现在有 factor-pair 诊断入口。
通过项能直接落到 (H-P)(H+P)=N^2。
```

不能说：

```text
same orientation 已关闭。
factor pair 已经推出递降。
两个 factor pair 不可能同时存在。
```

---

## 6. 下一步

建议下一步：

```text
1. 对通过方程记录 gcd(H-P, H+P)。
2. 用标准勾股参数化重写：
   N = 2xy 或 x^2-y^2
   P = x^2+y^2 的相关半差形式。
3. 比较 P=bc 和 Q=ad 能否同时由同一个 N 生成。
```

普通话说：

```text
下一步要看同一个 N 的两套因子拆法之间有没有包含/整除关系，
这才像递降证明的入口。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_shared_leg_terms_expose_square_difference -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
