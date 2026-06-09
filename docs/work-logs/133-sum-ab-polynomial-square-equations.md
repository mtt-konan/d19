# wl133 — `sum=A+B` polynomial square equations

日期：2026-06-09

## 1. 本轮问题

wl132 已经给出未约分的分子分母：

```text
y = (bc - ac + ad) / bc
s = (ad - ac + bc) / ad
```

这轮把它们直接变成未约分平方方程诊断。

普通话说：

```text
不只保存“这个数是 105/360”；
还直接保存“105²+360² 是不是平方”。
```

---

## 2. 新增字段

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbThreePassEuclidModel` 新增：

```text
other_slope_polynomial_equation
failed_polynomial_equation
```

格式：

```text
(unreduced_numerator, unreduced_denominator, hypotenuse_or_none)
```

---

## 3. 固定样例

沿用同一个样例：

```text
x = 15/8
r = 45/28
y = 105/360 = 7/24
s = 105/420 = 1/4
```

现在输出：

```text
other_slope_polynomial_equation = (105, 360, 375)
failed_polynomial_equation      = (105, 420, None)
```

含义：

```text
105^2 + 360^2 = 375^2
105^2 + 420^2 is not a square
```

约分后就是：

```text
7^2 + 24^2 = 25^2
1^2 + 4^2 = 17, not square
```

---

## 4. 新增测试

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
model.other_slope_polynomial_equation == (105, 360, 375)
model.failed_polynomial_equation == (105, 420, None)
```

TDD 红灯时，失败原因是模型还没有这两个字段。

---

## 5. 能说什么，不能说什么

可以说：

```text
sum=A+B 三通过模型现在直接给出未约分平方方程。
后续替换 Euclid 参数后，可以对整式平方方程做模筛、因式分解或递降尝试。
```

不能说：

```text
未约分方程已经证明失败项永远非平方。
四参数曲线已经分析完。
sum=A+B 分支已关闭。
```

---

## 6. 下一步

下一步可以新增一个纯符号说明或 helper，把：

```text
a,b,c,d
```

替换为：

```text
m^2-n^2, 2mn, u^2-v^2, 2uv
```

得到：

```text
(bc - ac + ad)^2 + (bc)^2 = Q^2
```

的显式四参数版本。

这一步之后，才适合认真看模条件或 squareclass 是否固定。

---

## 7. 验证

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
