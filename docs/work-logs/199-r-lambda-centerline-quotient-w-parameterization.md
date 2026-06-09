# wl199 — centerline quotient W-parameterization

日期：2026-06-09

## 1. 本轮目标

wl198 把中心线四次曲线除掉负倒数对称后，得到两个二次平方条件：

```text
Z^2 = u^2 + 8u + 20
W^2 = u^2 + 4
```

本轮继续问：

```text
如果先参数化 W^2 = u^2 + 4，
剩下会不会变简单？
```

结论：

```text
不会直接变成一次/简单同余。
剩下仍是一条带负倒数对称的四次条件。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quotient_w_parameterization(parameter)
```

返回：

```text
SumAbCenterlineQuotientWParameterization
```

记录：

```text
parameter
quotient_variable
w_value
w_condition_holds
remaining_quartic_value
z_square_value
z_square_value_is_square
negative_reciprocal_parameter
negative_reciprocal_remaining_quartic_value
negative_reciprocal_symmetry_holds
second_quotient_variable
second_quotient_quadratic_value
remaining_quartic_over_parameter_square
```

---

## 3. 参数化 `W^2 = u^2 + 4`

用标准勾股参数化：

```text
u = 4a / (1-a^2)
W = 2(1+a^2) / (1-a^2)
```

这保证：

```text
W^2 = u^2 + 4
```

普通话说：

```text
先吃掉“回到有理 t”的那条二次条件。
```

---

## 4. 剩余条件

还要满足：

```text
Z^2 = u^2 + 8u + 20
```

代入：

```text
u = 4a/(1-a^2)
```

得到：

```text
Z^2 = 4R(a)/(1-a^2)^2
```

其中：

```text
R(a)=5a^4-8a^3-6a^2+8a+5
```

所以剩下的问题是：

```text
R(a) 是有理平方。
```

普通话说：

```text
吃掉一个二次条件后，
没有直接结束，
而是换成了另一条四次曲线。
```

---

## 5. 新四次式也有负倒数对称

这个新四次式满足：

```text
R(-1/a) = R(a) / a^4
```

并且：

```text
R(a)/a^2 = 5v^2 - 8v + 4
v = a - 1/a
```

普通话说：

```text
结构又复制了一次。
这更像“循环/商变量图谱”，不是马上下降。
```

---

## 6. 样本

输入：

```text
a = 3/5
```

得到：

```text
u = 15/4
W = 17/4
W^2 = u^2 + 4
```

剩余：

```text
R(a)=164/25
Z^2 = 1025/16
```

所以：

```text
z_square_value_is_square = False
```

负倒数：

```text
-1/a = -5/3
R(-5/3)=4100/81
R(3/5)/(3/5)^4 = 4100/81
```

二次商变量：

```text
v = a - 1/a = -16/15
R(a)/a^2 = 164/9
5v^2 - 8v + 4 = 164/9
```

---

## 7. 可以说 / 不能说

可以说：

```text
中心线 quotient 的 W 条件可以完全参数化。
参数化后剩余条件是 R(a)=5a^4-8a^3-6a^2+8a+5 为平方。
R(a) 仍有 a -> -1/a 的负倒数对称。
```

不能说：

```text
中心线已经证明无解。
两个二次条件参数化后已经降成简单问题。
这一步已经给出无限递降。
```

因为：

```text
剩余四次式还没有列尽有理点，
也没有证明高度下降。
```

---

## 8. 路线影响

这轮有点像给路线泼冷水，但这是好事。

普通话说：

```text
“两个二次条件”确实更可读，
但不能天真地参数化一个就结束。
它会换出另一条自相似四次曲线。
```

下一步更合理的选择：

```text
1. 研究 R(a) 和 Q(t) 是否双有理等价，避免在同一结构里绕圈。
2. 直接把 Q(t) 或 R(a) 转成 Weierstrass 椭圆曲线，用 rank/torsion 列点。
3. 若要走 Yang Ji 风格递降，必须找到一个严格下降量，而不是只看负倒数对称。
```

普通话总结：

```text
中心线现在不是没结构，
而是结构太会复制自己。
下一步需要“列点”或“真正下降量”，不能只继续换参数。
```

---

## 9. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_remaining_quartic_matches_lambda_leg_value -q
```

结果：

```text
1 passed
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
