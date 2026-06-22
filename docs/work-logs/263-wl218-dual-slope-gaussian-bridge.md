# wl263 — wl218 dual slope Gaussian bridge

日期：2026-06-22

## 1. 本轮目标

接 wl262。

wl262 的样例说明：

```text
y = 4
y^2+1 = 17
```

用 `17=4^2+1^2` 做 Gaussian absorption 后，失败侧回到已有的 `dual_x=15/8`。

本轮把这个现象改写成一个更一般的“角差”账本。

普通话说：

```text
不是 17 碰巧好用。
真正起作用的是：失败斜率和目标 dual 斜率之间差了一个高斯角。
这个高斯角自己的平方类，就是失败项的平方类。
```

---

## 2. 角差公式

给定：

```text
failed = F
target = T
```

定义：

```text
k = (F - T) / (TF + 1)
```

则：

```text
T = (F - k) / (1 + kF)
```

这是 Gaussian / tangent subtraction 形式。

如果：

```text
T^2+1 是平方
```

那么：

```text
k^2+1 和 F^2+1 有相同 squareclass。
```

普通话说：

```text
目标 T 已经是好斜率。
失败 F 到好斜率 T 的差，就是一个坏因子 k。
把这个 k 吸掉，就回到 T。
```

---

## 3. 固定样例

仍取：

```text
t = 1/4
u = 2/7
failed_side = y
target_side = dual_x
```

得到：

```text
failed = 4
target = 15/8
k = 1/4
k^2+1 = 17/16
```

所以：

```text
squareclass(k^2+1) = 17
squareclass(failed^2+1) = 17
```

并且：

```text
(failed - k)/(1+k*failed) = 15/8
```

普通话说：

```text
这解释了为什么上一轮的 Gaussian absorption 会回到 dual_x。
它吸掉的就是 failed 和 dual_x 之间的角差。
```

---

## 4. 新 helper

新增 dataclass：

```text
SumAbDualSlopeGaussianBridge
```

新增 helper：

```text
sum_ab_dual_slope_gaussian_bridge(
    t,
    u,
    failed_side="x"|"y",
    target_side="dual_x"|"dual_y",
)
```

它记录：

```text
failed_slope
target_slope
failed_squareclass
bridge_ratio = k
bridge_value = k^2+1
bridge_squareclass
squareclass_matches_failure
recovered_target
recovery_identity_holds
```

新增测试：

```text
test_sum_ab_dual_slope_gaussian_bridge_recovers_target_squareclass
```

---

## 5. 对证明路线的影响

现在 only-1-mod-4 失败可以被更系统地描述：

```text
failed side has squareclass d
target dual side is already Pythagorean
=> the Gaussian bridge k has the same squareclass d
```

这说明：

```text
1 mod 4 坏因子可以被看成两个斜率之间的角差。
```

下一步要证明的是更强的闭环命题：

```text
如果 x,y,dual_x,dual_y 都是勾股斜率，
这些 Gaussian bridge 不能形成非中心闭环；
否则会递降或回到 centerline。
```

普通话说：

```text
我们已经知道坏因子怎么被吸回去。
还差的是证明：如果四条边都是真的好边，
这个吸回机制会迫使整个图形对称。
```

---

## 6. 当前边界

可以安全说：

```text
1. dual-slope only-1-mod-4 失败的 Gaussian bridge 已可计算；
2. bridge squareclass 与失败 squareclass 匹配；
3. 样例中的回流到 dual_x 有通用角差解释。
```

不能说：

```text
所有非中心闭环已排除。
sum=A+B 已证明。
全平面倒数定理已证明。
```
