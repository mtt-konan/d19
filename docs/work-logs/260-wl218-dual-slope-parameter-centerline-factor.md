# wl260 — wl218 dual slope parameter centerline factor

日期：2026-06-22

## 1. 本轮目标

接 wl259。

wl259 把 `sum=A+B` 真候选翻译成四个勾股斜率闭环：

```text
x, y, a, b 都是正有理勾股斜率
a = (x+y-1)/x
b = (x+y-1)/y
```

本轮把 `a,b` 参数化，观察反构造出来的 `x,y` 何时相等，以及恢复平方条件的差如何分解。

普通话说：

```text
现在从另一头出发：
先给 a,b 两个勾股斜率，
再反推出 x,y。
如果 x,y 也能成为勾股斜率，就得到真正危险的四勾股闭环。
```

---

## 2. 参数化

取：

```text
a = (1-t^2)/(2t)
b = (1-u^2)/(2u)
```

其中 `0<t,u<1` 时 `a,b>0`。

双斜率反构造为：

```text
D = a+b-ab
x = b/D
y = a/D
L = ab/D
```

也就是：

```text
L = x+y-1
a = L/x
b = L/y
```

普通话说：

```text
这一步保证 a,b 已经是勾股斜率。
剩下要问的是：反推出的 x,y 会不会也是勾股斜率？
```

---

## 3. 中心线因子

直接化简得到：

```text
x-y =
  -2(t-u)(tu+1)
  /
  (t^2u^2 + 2t^2u - t^2 + 2tu^2 - 2t - u^2 - 2u + 1)
```

所以在正参数区间里：

```text
x = y  <=>  t = u
```

更强的是，两个恢复平方值之差也带同一个中心线因子：

```text
(x^2+1) - (y^2+1)
=
-4(t-u)(t+u)(tu-1)(tu+1)
/
(t^2u^2 + 2t^2u - t^2 + 2tu^2 - 2t - u^2 - 2u + 1)^2
```

普通话说：

```text
不只 x-y 看见 t-u；
连“x 是否勾股”和“y 是否勾股”对应的两个平方值差，
也看见同一条中心线因子。
```

---

## 4. 中心线退化到 quartic

在中心线 `t=u` 上：

```text
x = y
```

并且恢复平方条件归到：

```text
t^4 + 8t^3 + 18t^2 - 8t + 1
```

这和已有 centerline quartic / Yang Ji 入口同属中线方向。

普通话说：

```text
中心线不是新问题。
一旦 t=u，问题又回到已经反复出现的中心线 quartic。
```

---

## 5. 固定样例

非中心样例：

```text
t = 1/4
u = 2/7
a = 15/8
b = 45/28
```

反构造：

```text
x = 24/7
y = 4
L = 45/7
```

这里：

```text
x^2+1 = 625/49 是平方
y^2+1 = 17 不是平方
```

普通话说：

```text
它说明只从 a,b 出发，可能只让一边恢复成勾股斜率。
真正危险的是两边同时恢复成功。
```

中心样例：

```text
t = u = 1/4
a = b = 15/8
x = y = 8
```

这里：

```text
x^2+1 = 65
```

不是平方。

普通话说：

```text
中心线本身也不会自动给真成员；
它还要过 centerline quartic 那一关。
```

---

## 6. 新 helper

新增 dataclass：

```text
SumAbDualSlopeParameterization
```

新增 helper：

```text
sum_ab_dual_slope_parameterization(t, u)
```

它记录：

```text
dual_slope_x = a
dual_slope_y = b
generated_x
generated_y
common_leg = L
generated_x_recovery_value = x^2+1
generated_y_recovery_value = y^2+1
generated_x_minus_y_factorized
recovery_value_difference_factorized
centerline_factor
centerline_recovery_quartic
```

新增测试：

```text
test_sum_ab_dual_slope_parameterization_exposes_centerline_factor
```

---

## 7. 对证明路线的影响

现在四勾股闭环有一个更明确的二参数表达：

```text
a,b 自动是勾股斜率；
x,y 由 t,u 反构造；
需要 x^2+1 和 y^2+1 同时为平方。
```

关键观察：

```text
两个恢复平方值的差含有中心线因子。
```

下一步可以尝试：

```text
1. 若两者同时平方，比较它们的差在 q == 3 mod 4 素数处的赋值；
2. 或把非中心同时平方解映射到更小参数，做递降。
```

普通话说：

```text
我们还没证明非中心不可能，
但现在知道非中心性具体藏在一个因子里。
后续估值应该盯这个因子，而不是盲扫所有项。
```

---

## 8. 当前边界

可以安全说：

```text
1. 双斜率闭环已参数化到 t,u；
2. x-y 和两个恢复平方值的差都显式暴露中心线因子；
3. 中心线退回已有 centerline quartic/Yang Ji 入口。
```

不能说：

```text
非中心双斜率闭环已排除。
sum=A+B 已证明。
全平面倒数定理已证明。
```
