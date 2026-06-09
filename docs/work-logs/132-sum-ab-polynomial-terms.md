# wl132 — `sum=A+B` polynomial numerator terms

日期：2026-06-09

## 1. 本轮问题

wl131 把 `y` 和 `s` 的检查写成整数平方方程：

```text
y = a/b  ->  a^2 + b^2 = c^2
s = d/e  ->  d^2 + e^2 = h^2
```

下一步要把 `a,b,d,e` 写成 `x,r` 的分子分母公式。

普通话说：

```text
先别急着证明。
先把“这个数的分子分母到底是什么”写死。
```

---

## 2. 公式

令：

```text
x = a/b
r = c/d
```

Möbius 模型：

```text
y = 1 - x + x/r
s = 1 - r + r/x
```

展开：

```text
y = 1 - a/b + (a/b)/(c/d)
  = 1 - a/b + ad/bc
  = (bc - ac + ad) / bc
```

```text
s = 1 - c/d + (c/d)/(a/b)
  = 1 - c/d + bc/ad
  = (ad - ac + bc) / ad
```

所以后续的整数方程可以写成：

```text
(bc - ac + ad)^2 + (bc)^2 = Q^2
(ad - ac + bc)^2 + (ad)^2 = H^2
```

其中 `a,b,c,d` 可以再替换成 Euclid 参数：

```text
a = m^2 - n^2 或 2mn
b = 2mn 或 m^2 - n^2
c = u^2 - v^2 或 2uv
d = 2uv 或 u^2 - v^2
```

---

## 3. 固定样例

wl122/wl129/wl130/wl131 的样例：

```text
x = 15/8
r = 45/28
```

因此：

```text
a=15, b=8, c=45, d=28
```

公式给：

```text
y numerator   = bc - ac + ad = 8*45 - 15*45 + 15*28 = 105
y denominator = bc = 360
```

所以：

```text
y = 105/360 = 7/24
```

另一个：

```text
s numerator   = ad - ac + bc = 15*28 - 15*45 + 8*45 = 105
s denominator = ad = 420
```

所以：

```text
s = 105/420 = 1/4
```

对应：

```text
7^2 + 24^2 = 25^2
1^2 + 4^2 = 17, not square
```

---

## 4. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbThreePassEuclidModel` 新增：

```text
other_slope_polynomial_terms
failed_polynomial_terms
```

格式：

```text
(unreduced_numerator, unreduced_denominator)
```

对样例：

```text
other_slope_polynomial_terms = (105, 360)
failed_polynomial_terms      = (105, 420)
```

---

## 5. 测试和一个纠错

文件：

```text
tests/test_rational_ratio.py
```

扩展：

```text
test_sum_ab_mobius_model_from_euclid_params_exposes_square_equations
```

新增断言：

```text
model.other_slope_polynomial_terms == (105, 360)
model.failed_polynomial_terms == (105, 420)
```

测试过程抓到一个手算错误：

```text
我一开始把 y 的分母写成 bd。
正确分母是 bc，因为 x/r = ad/bc。
```

这正是把公式写进测试的价值。

---

## 6. 能说什么，不能说什么

可以说：

```text
sum=A+B 三通过模型已经有未约分的多项式分子分母。
下一步可以把它们直接替换成 Euclid 参数，得到显式四参数平方方程。
```

不能说：

```text
四参数方程已经分析完成。
s 的失败已经被证明。
sum=A+B 分支已关闭。
```

---

## 7. 下一步

直接展开：

```text
(bc - ac + ad)^2 + (bc)^2 = Q^2
```

并把：

```text
a,b,c,d
```

替换为两组 Euclid legs。然后看：

```text
(ad - ac + bc)^2 + (ad)^2
```

是否有固定 squareclass、模障碍或可递降结构。

---

## 8. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
21 passed
All checks passed
```
