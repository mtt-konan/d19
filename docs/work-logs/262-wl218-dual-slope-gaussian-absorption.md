# wl262 — wl218 dual slope Gaussian absorption

日期：2026-06-22

## 1. 本轮目标

接 wl261。

wl261 说明 dual-slope 恢复值的失败也可能只坏在 `1 mod 4` 素数上：

```text
y^2+1 = 17
17 == 1 mod 4
```

所以本轮检查这个 only-1-mod-4 坏因子是否能像旧 guard 的 `29` 一样被 Gaussian absorption 吸收。

普通话说：

```text
3 mod 4 抓不到 17。
那就用 17=4^2+1^2，把这个坏因子当成高斯因子除掉，
看除完以后会落到哪里。
```

---

## 2. 样例

取 dual-slope 参数：

```text
t = 1/4
u = 2/7
```

wl260 反构造得到：

```text
dual_x = 15/8
dual_y = 45/28
x = 24/7
y = 4
```

恢复值：

```text
x^2+1 = 625/49 = (25/7)^2
y^2+1 = 17
```

坏因子：

```text
17 = 4^2 + 1^2
```

对失败侧 `y=4` 做 Gaussian absorption：

```text
z_plus  = (4y+1)/(4-y)
z_minus = (4y-1)/(4+y)
```

这里：

```text
z_plus  在分母 0 处退化
z_minus = 15/8
```

而：

```text
15/8 = dual_x
```

普通话说：

```text
失败侧 y=4 不是随机失败。
把 17 这个坏平方类吸掉以后，它回到了原来的 dual_x。
```

---

## 3. 新 helper

新增 dataclass：

```text
SumAbDualSlopeGaussianAbsorption
```

新增 helper：

```text
sum_ab_dual_slope_gaussian_absorption(t, u, failed_side="x"|"y")
```

它记录：

```text
failed_slope
failed_value
failed_squareclass
two_square_decomposition
absorbed_plus
absorbed_minus
matching_absorptions
absorbs_to_existing_dual_slope
```

注意：

```text
某个 Gaussian 分支可能分母为 0。
```

所以本 helper 使用安全分支：

```text
undefined branch => None
defined branch   => Fraction
```

新增测试：

```text
test_sum_ab_dual_slope_gaussian_absorption_returns_failure_to_dual_slope
```

---

## 4. 对证明路线的影响

这不是 `sum=A+B` 证明。

但它把 only-1-mod-4 失败接回了 dual-slope 闭环：

```text
失败侧
  -- absorb squareclass d=a^2+b^2 -->
已有 dual slope
```

普通话说：

```text
1 mod 4 坏因子不是死胡同。
它会把我们送回闭环里的另一条边。
这很像一个递降/自对偶机制的入口。
```

下一步应尝试证明：

```text
如果非中心四勾股闭环存在，
对任一 only-1-mod-4 失败做 Gaussian absorption，
会产生更小的同类闭环，或直接回到 centerline。
```

---

## 5. 当前边界

可以安全说：

```text
1. dual-slope only-1-mod-4 失败可以安全做 Gaussian absorption；
2. 样例中的 17 吸收后回到已有 dual slope；
3. 这和旧 guard 的 Gaussian shadow 机制一致。
```

不能说：

```text
所有 only-1-mod-4 失败都会递降。
dual-slope 非中心闭环已排除。
sum=A+B 已证明。
全平面倒数定理已证明。
```
