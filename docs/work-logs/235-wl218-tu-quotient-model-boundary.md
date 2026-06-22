# wl235 — wl218 `T=t-1/t`, `U=u-1/u` quotient model boundary

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支的 squareclass-ratio 引理：

```text
A(t,u)/B(t,u) 是有理平方 => t=u.
```

前面 wl232-wl234 说明：

```text
z = u - 1/u
```

能揭示自相似结构，但单靠继续参数化不会证明引理。

本轮改看这个自相似结构的商变量。

普通话说：

```text
既然 t -> -1/t 和 u -> -1/u 都不改变比值，
就把这两个对称性除掉，看看真正剩下的问题是什么。
```

---

## 2. 商变量

令：

```text
T = t - 1/t
U = u - 1/u
```

对于：

```text
0<t,u<1
```

有：

```text
T < -2
U < -2.
```

并且一个有理 `T` 能来自有理 `t`，当且仅当：

```text
T^2 + 4 是有理平方。
```

`U` 同理。

---

## 3. 二次型压缩

原来的 squareclass ratio 可以写成：

```text
A(t,u)/B(t,u)
```

除掉 `t -> -1/t`、`u -> -1/u` 对称后，变成：

```text
N(T,U) / D(T,U)
```

其中：

```text
N = 2T^2 + 2TU + 4T + U^2 + 4U + 4
D = T^2 + 2TU + 4T + 2U^2 + 4U + 4.
```

而且：

```text
N - D = (T-U)(T+U).
```

在本问题区域 `T,U<-2`，有：

```text
T+U < 0.
```

所以：

```text
N=D <=> T=U <=> t=u.
```

普通话说：

```text
完全相等时，还是马上落到中线。
但目标仍然是平方倍数：N/D 是平方。
```

---

## 4. 更强命题是假的

如果忘掉恢复条件，只在任意有理：

```text
T,U < -2
```

里问：

```text
N/D 是有理平方 => T=U
```

这是假的。

小反例：

```text
T = -7
U = -35/17
N/D = 28561/15625 = (169/125)^2.
```

但它不能回到有理 `t,u`，因为：

```text
T^2 + 4 = 53          不是有理平方
U^2 + 4 = 2381/289   不是有理平方
```

普通话说：

```text
把问题放大以后确实有假反例。
真正保护我们的不是二次型本身，而是 T、U 必须能还原成有理 t、u。
```

所以正确的压缩命题是：

```text
T,U < -2
T^2+4 和 U^2+4 都是有理平方
N(T,U)/D(T,U) 是有理平方
=> T=U.
```

---

## 5. `V,W` 形式

再令：

```text
V = T + U
W = T - U
```

则：

```text
N-D = VW.
```

在 `T,U<-2` 区域：

```text
V < -4.
```

中心线是：

```text
W=0.
```

若写：

```text
N = H D
```

并把方程看成 `W` 的二次式，它的判别式为：

```text
-16 * (H^2 V^2 - 3H V^2 + 4HV - 4H + V^2).
```

这可以作为后续 local-symbol / descent 的更小入口。

---

## 6. 代码入口

新增 helper：

```text
sum_ab_squareclass_ratio_tu_quotient_model(T, U)
```

它记录：

```text
N(T,U)
D(T,U)
N/D 是否平方
T^2+4 是否平方
U^2+4 是否平方
```

测试：

```text
test_sum_ab_squareclass_ratio_tu_quotient_model_tracks_recovery_conditions
```

测试同时覆盖：

```text
1. 一个真实 t,u 样本能和原 A/B 一致；
2. 放大空间假反例 N/D 是平方，但恢复条件失败。
```

---

## 7. 当前证明边界

可以安全说：

```text
squareclass-ratio 引理已压缩成 T,U 二次型模型；
更强的“任意 T,U<-2”版本是假的；
必须使用 T^2+4、U^2+4 这两个恢复平方条件。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
二次型模型本身已排除非中线。
```

---

## 8. 下一步

现在最具体的证明目标是：

```text
T,U < -2,
T^2+4 = square,
U^2+4 = square,
N/D = square
=> T=U.
```

这比原来的 `t,u` 四次式更清楚。

可能路线：

```text
1. 对 T^2+4 与 U^2+4 参数化，寻找 descent；
2. 对三平方条件组成的曲面做 Hilbert-symbol obstruction；
3. 用 V,W 形式证明 W != 0 时判别式局部不可平方。
```
