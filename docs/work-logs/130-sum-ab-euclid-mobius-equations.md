# wl130 — `sum=A+B` Euclid-Möbius equations

日期：2026-06-09

## 1. 本轮问题

wl129 把三通过 near-miss 写成 Möbius 公式：

```text
输入: x, r
λ = r/x
y = 1 - x + x/r
s = 1 - r + r/x
```

其中 `x` 和 `r` 是已经通过的勾股斜率。下一步是把这两个通过条件显式参数化。

普通话说：

```text
x 和 r 不再只是两个有理数；
它们来自两个直角三角形参数。
然后 y 和 s 被 closure 公式推出。
```

---

## 2. Euclid 参数

新增参数对象：

```text
PythagoreanLegParam(m, n, orientation)
```

两种方向：

```text
orientation="odd"  -> (m^2-n^2)/(2mn)
orientation="even" -> (2mn)/(m^2-n^2)
```

要求：

```text
m > n > 0
```

这不是新的搜索器。它只是把“这个 ratio 是勾股斜率”写成可追踪的参数来源。

---

## 3. 固定样例

wl122/wl129 的样例：

```text
x = 15/8
r = 45/28
```

现在写成：

```text
x = (4^2-1^2)/(2*4*1) = 15/8
r = (7^2-2^2)/(2*7*2) = 45/28
```

Möbius 公式给：

```text
λ = 6/7
y = 7/24
s = 1/4
```

平方方程诊断：

```text
y^2 + 1 = (25/24)^2
s^2 + 1 = 17/16
```

所以：

```text
y 通过
s 失败，squareclass = 17
```

---

## 4. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
PythagoreanLegParam
SumAbThreePassEuclidModel
pythagorean_leg_ratio_from_param(param)
sum_ab_three_pass_mobius_model_from_params(slope, scaled_term)
```

`SumAbThreePassEuclidModel` 包含：

```text
slope_param
scaled_term_param
mobius
other_slope_square_equation
failed_square_equation
failed_squareclass
```

其中 square equation 形如：

```text
(z^2+1, square_root^2 或 None)
```

如果第二项是 `None`，说明 `z^2+1` 不是有理平方。

---

## 5. 新增测试

文件：

```text
tests/test_rational_ratio.py
```

新增：

```text
test_sum_ab_mobius_model_from_euclid_params_exposes_square_equations
```

测试固定：

```text
PythagoreanLegParam(4,1,"odd") -> x=15/8
PythagoreanLegParam(7,2,"odd") -> r=45/28
```

并检查：

```text
y = 7/24
s = 1/4
y^2+1 = (25/24)^2
s^2+1 = 17/16, no rational square root
failed squareclass = 17
```

测试过程中曾抓到一个参数笔误：

```text
(8,1) gives 63/16, not 45/28
```

正确参数是：

```text
(7,2)
```

---

## 6. 能说什么，不能说什么

可以说：

```text
三通过 Möbius 模型现在能从 Euclid 参数直接生成。
y 是否通过、s 如何失败都能以显式平方方程显示。
```

不能说：

```text
y 条件已经完全消元。
s 的 squareclass 已被证明永远非 1。
sum=A+B 分支已关闭。
```

这轮只是把 near-miss 方程化又往前推了一格。

---

## 7. 下一步

真正的理论目标现在更清楚：

```text
令 x = E(m,n), r = E(u,v)
y = 1 - x + x/r

要求 y^2 + 1 是平方。
```

下一步可以把：

```text
y^2 + 1 = q^2
```

展开成四个 Euclid 参数和一个新平方变量的曲线。

如果能再推出：

```text
s = 1 - r + r/x
s^2 + 1
```

的 squareclass 不能是 1，就能解释三通过 near-miss 为什么总卡在第四条。

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
