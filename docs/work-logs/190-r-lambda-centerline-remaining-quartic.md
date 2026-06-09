# wl190 — `R_lambda` centerline remaining quartic

日期：2026-06-09

## 1. 本轮目标

wl189 参数化了 centerline 的第一条平方条件：

```text
center^2 + 1 是平方
```

本轮把剩下的第二条条件：

```text
center^2 + lambda^2 是平方
```

展开成一个明确四次式。

普通话说：

```text
中心线现在不是“两个平方条件”了；
第一条已经吃掉，
剩下就是一个四次式是不是平方。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_remaining_quartic(parameter)
```

返回：

```text
SumAbCenterlineRemainingQuartic
```

记录：

```text
parameter
coefficients
quartic_value
denominator_square
lambda_value
squareclass
is_square
```

---

## 3. 推导

从 wl189：

```text
center = 2t / (1 - t^2)
lambda = 2center - 1
```

所以：

```text
lambda = (t^2 + 4t - 1) / (1 - t^2)
```

于是：

```text
center^2 + lambda^2
= Q(t) / (1 - t^2)^2
```

其中：

```text
Q(t) = t^4 + 8t^3 + 18t^2 - 8t + 1
```

普通话说：

```text
分母本来就是平方，
所以问题变成 Q(t) 是否为有理平方。
```

---

## 4. 样本

输入：

```text
t = 3/5
```

得到：

```text
Q(t) = 2836/625
(1-t^2)^2 = 256/625
lambda_value = Q(t) / (1-t^2)^2 = 709/64
squareclass = 709
is_square = False
```

普通话说：

```text
四次式没给出平方，
所以这个 t 不产生中心线真点。
```

---

## 5. 一个小心点

这里的三次项是：

```text
+8t^3
```

不是：

```text
-8t^3
```

因为：

```text
lambda = (t^2 + 4t - 1)/(1-t^2)
```

平方展开时有：

```text
2 * t^2 * 4t = +8t^3
```

普通话说：

```text
这个符号很容易手算错，
后续以这个 ledger 和测试为准。
```

---

## 6. 可以说 / 不能说

可以说：

```text
centerline 真点问题已化为 Q(t) 是否为有理平方。
Q(t)=t^4+8t^3+18t^2-8t+1。
```

不能说：

```text
Q(t) 不可能是平方。
centerline 已经全局排除。
有理比例主定理已经证明。
```

因为：

```text
本轮只是正确展开剩余方程，
还没有证明四次曲线没有有理解。
```

---

## 7. 下一步

下一步可以直接攻：

```text
y^2 = t^4 + 8t^3 + 18t^2 - 8t + 1
```

可能路线：

```text
1. 做模 p 障碍，看是否覆盖所有有理 t 的原始整数形式。
2. 变换成椭圆曲线，看是否可用 rank / torsion 解释。
3. 寻找递降结构，作为 Yang Ji / 固定线证明样板。
```

普通话总结：

```text
中心线已经变成一条明确的四次曲线。
下一步不该再猜中心线，
该攻这条曲线。
```

---

## 8. 验证

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
