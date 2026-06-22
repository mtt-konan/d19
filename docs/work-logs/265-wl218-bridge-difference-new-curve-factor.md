# wl265 — wl218 bridge difference and new-curve factor

日期：2026-06-22

## 1. 本轮目标

接 wl264。

wl264 把 dual-slope 四平方闭环改写成：

```text
k_x^2 + 1 square
k_y^2 + 1 square
```

本轮继续拆这两个 bridge 条件的差。

普通话说：

```text
如果两条角差桥都是真的好斜率，
那么它们的两个平方值之间必须有非常特殊的差。
这个差一拆开，直接露出 centerline 因子；
剩下的唯一额外出口 E=0，又回到了 wl240 那条新四次曲线。
```

---

## 2. 记号

仍用：

```text
dual_x = a = (1 - t^2)/(2t)
dual_y = b = (1 - u^2)/(2u)
D = a + b - ab
x = b/D
y = a/D
```

两条 cross bridge 是：

```text
k_x = (x - b)/(bx + 1)
k_y = (y - a)/(ay + 1)
```

---

## 3. 差分因式分解

符号化得到：

```text
(k_x^2+1) - (k_y^2+1)
= - C * (t+u)(tu-1)(t^2+2t-1)^2(u^2+2u-1)^2 * E
  / (DX^2 DY^2)
```

其中：

```text
C = (t-u)(t+u)(tu-1)(tu+1)
```

就是 centerline factor。

额外因子为：

```text
E =
t^2u^2 + t^2u - t^2
+ tu^2 - t - u^2 - u + 1.
```

普通话说：

```text
两条桥的平方值相等或出现特殊抵消时，
除了 centerline 之外，只剩一个明确的出口 E。
```

---

## 4. E 接回 wl240 新曲线

把 `E` 看成 `u` 的二次式：

```text
E = (t^2+t-1)u^2 + (t^2-1)u + (1-t-t^2).
```

它的判别式是：

```text
5t^4 + 8t^3 - 6t^2 - 8t + 5.
```

这正是 wl238-wl240 已经出现过的新四次曲线：

```text
Y^2 = 5t^4 + 8t^3 - 6t^2 - 8t + 5.
```

普通话说：

```text
E=0 不是新麻烦。
如果 E=0 有有理 u，那么 t 必须落在旧的新曲线上。
所以 bridge 差分路线和 wl240 的 z-lemma/rank-0 路线接上了。
```

---

## 5. 固定样例

取：

```text
t = 1/4
u = 2/7
```

得到：

```text
bridge_value_difference = 3211/203522
centerline_factor       = 2925/153664
E                       = 285/784
disc_u(E)               = 709/256
new_curve_value(t)      = 709/256
```

这里：

```text
disc_u(E) = new_curve_value(t)
```

完全匹配。

---

## 6. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgeDifferenceFactorization
```

新增 helper：

```text
sum_ab_dual_slope_bridge_difference_factorization(t, u)
```

它记录：

```text
bridge_value_difference
centerline_factor
extra_equal_bridge_factor = E
bridge_difference_factorized
factorization_holds
extra_factor_u_quadratic_coefficients
extra_factor_u_discriminant
new_curve_value_t
extra_factor_discriminant_matches_new_curve
```

新增测试：

```text
test_sum_ab_dual_slope_bridge_difference_factors_through_new_curve
```

---

## 7. 模素数观察

小范围有限域检查还看到：

```text
mod 5  affine 非退化 both-bridge-square 类都落在 centerline factor = 0
mod 11 affine 非退化 both-bridge-square 类都落在 centerline factor = 0
```

但这还不能直接当证明。

原因：

```text
1. 有理参数可能在这些素数下退化；
2. 单个模素数只给 centerline factor 的可除性，不给全局矛盾；
3. 还需要 p-adic 提升或全局递降来封口。
```

---

## 8. 当前证明状态

可以安全说：

```text
1. bridge 两平方条件的差分已精确因式分解；
2. 差分直接含 centerline factor；
3. 非 centerline 的特殊出口 E=0 必须落到 wl240 新四次曲线；
4. 这把 wl264 的 bridge-cycle 路线接回已有 z-lemma/new-curve 边界。
```

不能说：

```text
sum=A+B 已证明。
E=0 已完全排除。
mod 5 或 mod 11 已经给出全局证明。
全平面倒数定理已证明。
```

---

## 9. 下一步

现在最短证明路线变成两个可分离的小目标：

```text
A. 证明 wl240 新曲线只有边界点，排除 E=0 的非退化出口；
B. 在 E != 0 时，用 bridge 差分的 centerline 因子做 valuation/descent。
```

如果 A 能严格完成，那么 bridge 差分路线会少一个主要分支。

普通话说：

```text
我们还没证明倒数定理，
但现在知道一个关键逃生门不是新的：它就是之前那条新曲线。
```

---

## 10. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_gaussian_bridge_cycle_reduces_squares_to_bridges tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_difference_factors_through_new_curve -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
2 passed
All checks passed
git diff --check passed
```
