# wl257 — wl218 centerline shadow unit obstruction

日期：2026-06-22

## 1. 本轮目标

接 wl256。

wl256 把 inverse Gaussian `(plus, minus)` 分支写成了通式：

```text
r = (az-b)/(a+bz)
s = (az+b)/(a-bz)
d = a^2+b^2
lambda = r+s-1
p = rs
```

并且拆出了四个真正的成员项：

```text
r^2 + 1
s^2 + 1
r^2 + lambda^2
s^2 + lambda^2
```

本轮把一个直接可用的障碍固定成 helper：

```text
如果 z 是勾股斜率，且 d 是非平凡 squareclass，
那么这个 centerline shadow 不可能是真 R_lambda 成员对。
```

普通话说：

```text
一个假点如果能吸回到中线 z，
那它看起来像是从真勾股斜率变出来的。
但只要变换时乘回了非平凡的 d，
r^2+1 和 s^2+1 会立刻带上这个 d，
所以单项平方条件直接失败。
```

---

## 2. 公式原因

wl256 已有：

```text
r^2 + 1 =
  d (z^2 + 1) / (a + bz)^2

s^2 + 1 =
  d (z^2 + 1) / (a - bz)^2
```

如果：

```text
z^2 + 1 是有理平方
d 不是有理平方
```

那么：

```text
squareclass(r^2+1) = d
squareclass(s^2+1) = d
```

因此：

```text
r^2+1 和 s^2+1 都不是有理平方。
```

普通话说：

```text
product layer 只看两个 unit 项相乘。
两个 d 相乘会变成 d^2，于是乘积像平方。
但 R_lambda 要每一个 unit 项自己是平方；
这里每一个都还带着 d。
```

---

## 3. guard 复核

旧 guard：

```text
z = 4/3
d = 29 = 5^2+2^2
r_branch = plus
s_branch = minus
```

有：

```text
z^2 + 1 = 25/9
```

这是平方。

但：

```text
r^2 + 1 = 725/529
s^2 + 1 = 725/49
```

两者 squareclass 都是：

```text
29
```

因此 guard 被 unit 项直接挡住。

普通话说：

```text
guard 能骗过 A_p，因为 A_p=(r^2+1)(s^2+1)。
但它骗不过 R_lambda，因为 r^2+1 自己不是平方，s^2+1 自己也不是平方。
```

---

## 4. 新 helper

新增 dataclass：

```text
InverseGaussianCenterlineShadowObstruction
```

新增 helper：

```text
inverse_gaussian_centerline_shadow_obstruction(
    absorbed=z,
    squareclass=d,
    r_branch="plus",
    s_branch="minus",
)
```

它返回：

```text
absorbed_unit_value
absorbed_unit_value_is_square
squareclass_is_trivial
r_unit_squareclass
s_unit_squareclass
unit_squareclass_obstruction
true_member_pair_blocked
obstruction_reason
```

新增测试：

```text
test_inverse_gaussian_centerline_shadow_obstruction_blocks_unit_terms
```

---

## 5. 有限 root-grid 摘要

把这条 obstruction 接到已有 root-grid residual 摘要上。

新增 dataclass：

```text
GaussianShadowObstructionSummary
```

新增 helper：

```text
sum_ab_root_grid_gaussian_shadow_obstruction_summary(
    max_numerator=...,
    max_denominator=...,
)
```

它先枚举：

```text
sum_ab_product_square_residuals_from_root_grid(...)
```

再对每个 residual 做：

```text
residual_gaussian_absorption_ledger(...)
inverse_gaussian_centerline_shadow_obstruction(...)
```

测试锁住范围：

```text
max_numerator = 26
max_denominator = 23
```

结果：

```text
total_residuals = 1
centerline_shadow_count = 1
unit_obstructed_count = 1
nonobstructed_count = 0
obstruction_reason_counts = {
  nontrivial-squareclass-on-unit-terms: 1
}
```

普通话说：

```text
小范围里唯一看到的 product-layer residual，
不只是能吸回中线；
它还会立刻被 unit 单项平方条件挡住。
```

额外只读探针：

```text
26/23: total=1 shadow=1 unit_obstructed=1 nonobstructed=0
32/32: total=1 shadow=1 unit_obstructed=1 nonobstructed=0
40/40: total=1 shadow=1 unit_obstructed=1 nonobstructed=0
```

这些范围里仍只有旧 guard：

```text
lambda = 535/161
roots = (14/23, 26/7)
member_squareclass_pair = (29, 29)
```

这仍然不是无穷证明。

---

## 6. 对证明路线的影响

这条引理可以排除一种非常具体的假阳性：

```text
nontrivial only-1-mod-4 product residual
被 Gaussian absorption 吸回到同一个真勾股斜率 z
```

因为这种 residual 的 unit 项会带着非平凡 `d`。

但它还不是 `sum=A+B` 的完整证明。

剩下缺口是：

```text
必须证明任何 only-1-mod-4 residual 若想同时满足 product layer，
都会是这种 centerline shadow；
或者绕过 shadow 语言，直接从四个成员平方条件推出 p=lambda。
```

普通话说：

```text
我们现在能杀掉“已经确认是中线影子”的假点。
下一步要证明的是：
所有危险的 1 mod 4 假点都只能这样出现，
或者真成员条件根本不允许它们出现。
```

---

## 7. 当前边界

可以安全说：

```text
1. centerline shadow + nontrivial d 会被 unit 项平方条件排除；
2. guard residual 正是这样被排除；
3. 有限 root-grid 的已知 residual 被这个 obstruction 覆盖；
4. 这解释了 why product-square shadow is not true membership。
```

不能说：

```text
所有 only-1-mod-4 residual 都已证明是 centerline shadow。
sum=A+B 已证明。
全平面倒数定理已证明。
```
