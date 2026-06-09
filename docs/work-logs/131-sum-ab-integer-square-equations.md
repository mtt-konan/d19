# wl131 — `sum=A+B` integer square equations

日期：2026-06-09

## 1. 本轮问题

wl130 已经能从两个 Euclid 参数生成：

```text
x, r
y = 1 - x + x/r
s = 1 - r + r/x
```

并用 Fraction 层检查：

```text
y^2 + 1 是否为有理平方
s^2 + 1 是否为有理平方
```

这轮把检查再往“可证明方程”方向推一步：

```text
z = a/b
z^2 + 1 是平方
等价于
a^2 + b^2 = c^2
```

普通话说：

```text
别只说 7/24 通过；
把它写成 7²+24²=25²。

别只说 1/4 失败；
把它写成 1²+4²=17，17 不是平方。
```

---

## 2. 新增诊断

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbThreePassEuclidModel` 新增：

```text
other_slope_integer_equation
failed_integer_equation
```

格式：

```text
(a, b, c_or_none)
```

含义：

```text
z = a/b
a^2 + b^2 = c^2      如果 c_or_none 是整数
a^2 + b^2 非平方     如果 c_or_none 是 None
```

---

## 3. 固定样例

wl122/wl129/wl130 的样例：

```text
x = 15/8
r = 45/28
y = 7/24
s = 1/4
```

现在输出：

```text
other_slope_integer_equation = (7, 24, 25)
failed_integer_equation      = (1, 4, None)
```

也就是：

```text
7^2 + 24^2 = 25^2
1^2 + 4^2 = 17, not square
```

失败项仍记录：

```text
failed squareclass = 17
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
model.other_slope_integer_equation == (7, 24, 25)
model.failed_integer_equation == (1, 4, None)
```

TDD 红灯时，失败原因是 `SumAbThreePassEuclidModel` 还没有这两个字段。

---

## 5. 能说什么，不能说什么

可以说：

```text
三通过 near-miss 的 y/s 检查现在可以落到整数平方方程。
后续可以对 a^2+b^2=c^2 或非平方的 a^2+b^2 做模条件、因式分解或递降尝试。
```

不能说：

```text
已经证明 s 一定失败。
已经推导出完整四变量曲线。
sum=A+B 分支已关闭。
```

这轮只是把 Fraction 诊断变成更适合证明的整数诊断。

---

## 6. 下一步

下一步可以展开：

```text
x = E(m,n)
r = E(u,v)
y = 1 - x + x/r = A(m,n,u,v) / B(m,n,u,v)
```

然后把：

```text
A^2 + B^2 = C^2
```

作为显式四参数曲线。再看失败项：

```text
s = 1 - r + r/x = D(m,n,u,v) / E(m,n,u,v)
D^2 + E^2
```

是否有固定 squareclass、模障碍或递降结构。

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
