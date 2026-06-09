# wl198 — centerline negative-reciprocal quotient

日期：2026-06-09

## 1. 本轮目标

wl197 发现中心线自相似二次方程的两个根满足：

```text
t1 * t2 = -1
```

所以两个根互为负倒数。

本轮继续问：

```text
t -> -1/t 是不是中心线四次曲线自己的真实对称？
```

结论：

```text
是。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_negative_reciprocal_quotient(parameter)
```

返回：

```text
SumAbCenterlineQuarticNegativeReciprocalQuotient
```

记录：

```text
parameter
negative_reciprocal
quotient_variable
quartic_value
negative_reciprocal_quartic_value
negative_reciprocal_symmetry_holds
scaled_quartic_value
quotient_quadratic_value
reconstructing_quadratic_coefficients
reconstruction_discriminant
reconstruction_discriminant_is_square
reconstruction_roots
```

---

## 3. 负倒数是曲线对称

中心线四次式：

```text
Q(t)=t^4+8t^3+18t^2-8t+1
```

满足：

```text
Q(-1/t) = Q(t) / t^4
```

所以如果：

```text
Y^2 = Q(t)
```

那么：

```text
(Y/t^2)^2 = Q(-1/t)
```

普通话说：

```text
t 是曲线上的点，
-1/t 也是同一条曲线上的点。
```

这解释了 wl197 的根乘积 `-1`：

```text
它不是偶然，
而是曲线本身的对称。
```

---

## 4. 商变量

对称：

```text
t -> -1/t
```

的不变量可以取：

```text
u = t - 1/t
```

直接计算：

```text
Q(t) / t^2
= t^2 + 8t + 18 - 8/t + 1/t^2
= (t - 1/t)^2 + 8(t - 1/t) + 20
= u^2 + 8u + 20
```

如果令：

```text
Z = Y/t
```

中心线四次曲线就变成：

```text
Z^2 = u^2 + 8u + 20
```

普通话说：

```text
四次曲线除掉负倒数对称后，
只剩一个二次平方条件。
```

---

## 5. 不能漏掉反解条件

但是从 `u` 回到 `t`，还要解：

```text
t - 1/t = u
```

也就是：

```text
t^2 - u t - 1 = 0
```

判别式：

```text
u^2 + 4
```

所以 `t` 有理还要求：

```text
u^2 + 4 是有理平方
```

因此中心线问题可以改写成：

```text
Z^2 = u^2 + 8u + 20
W^2 = u^2 + 4
```

普通话说：

```text
不是一条二次曲线就解决了；
还要同时过另一条二次曲线。
```

这很像 Yang Ji 风格：

```text
两个勾股条件绑在同一个参数上。
```

---

## 6. 样本

输入：

```text
t = 3/5
```

负倒数：

```text
-1/t = -5/3
```

商变量：

```text
u = t - 1/t = -16/15
```

四次式：

```text
Q(3/5) = 2836/625
Q(-5/3) = 2836/81
Q(-5/3) = Q(3/5) / (3/5)^4
```

商变量二次式：

```text
Q(t)/t^2 = 2836/225
u^2 + 8u + 20 = 2836/225
```

反解判别式：

```text
u^2 + 4 = 1156/225 = (34/15)^2
```

反解根：

```text
-5/3
3/5
```

---

## 7. 可以说 / 不能说

可以说：

```text
t -> -1/t 是 centerline quartic 的真实对称。
商变量 u=t-1/t 把 Q(t) square 降成 Z^2=u^2+8u+20。
但要回到有理 t，还必须同时满足 W^2=u^2+4。
```

不能说：

```text
centerline 已证明无解。
四次曲线已经完全列尽。
只看 Z^2=u^2+8u+20 就等价于原问题。
```

因为：

```text
单独的 u 二次条件太弱；
必须带着反解条件 W^2=u^2+4。
```

---

## 8. 下一步

最自然的下一步：

```text
把
Z^2 = u^2 + 8u + 20
W^2 = u^2 + 4
```

相减：

```text
Z^2 - W^2 = 8u + 16 = 8(u+2)
```

这可能给出一个新的因式分解/递降入口：

```text
(Z-W)(Z+W)=8(u+2)
```

普通话总结：

```text
负倒数不是麻烦，而是对称。
把这个对称除掉后，中心线变成两个二次平方条件绑在同一个 u 上。
这比直接啃四次式更像可读证明的入口。
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
