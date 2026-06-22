# wl259 — wl218 dual slope four-square model

日期：2026-06-22

## 1. 本轮目标

接 wl258。

wl258 把 `sum=A+B` 的真成员条件写成四个平方：

```text
x^2 + 1 square
y^2 + 1 square
P = x^2 + L^2 square
Q = y^2 + L^2 square
L = x + y - 1 > 0
```

本轮把后两个平方换一种更直观的说法。

普通话说：

```text
P 是平方，就是 x 和 L 能拼成直角三角形；
等价地，L/x 本身也是一个勾股斜率。
Q 同理给出 L/y。
```

---

## 2. 双斜率变换

定义：

```text
a = L/x
b = L/y
L = x + y - 1
```

则：

```text
P = x^2 + L^2 square  <=>  a^2 + 1 square
Q = y^2 + L^2 square  <=>  b^2 + 1 square
```

所以真候选等价于：

```text
x, y, a, b 都是正有理勾股斜率
a = L/x
b = L/y
L = x+y-1
```

从 `a,b` 也能反构造：

```text
D = a + b - ab
x = b / D
y = a / D
L = ab / D
```

普通话说：

```text
这不是多加了两个变量。
这是把“P,Q 是平方”翻译成：
原来那条公共腿 L，分别除以 x 和 y 后，也必须是勾股斜率。
```

---

## 3. 两种假象

样例 1：

```text
x = 15/8
y = 45/28
L = 139/56
```

这里：

```text
x^2+1 square
y^2+1 square
```

但：

```text
L/x = 139/105
L/y = 139/90
```

都不是勾股斜率。

普通话说：

```text
x,y 自己过关，不代表 P,Q 会过关。
```

样例 2：

```text
x = 7/2
y = 35/34
L = 60/17
```

这里：

```text
L/x = 120/119
L/y = 24/7
```

都是勾股斜率，所以 `P,Q` 各自平方。

但：

```text
x^2+1
y^2+1
```

不是平方。

普通话说：

```text
P,Q 过关，也不代表 x,y 自己过关。
真正危险的是四个斜率同时过关。
```

---

## 4. 新 helper

新增 dataclass：

```text
SumAbFourSquareDualSlopeModel
```

新增 helper：

```text
sum_ab_four_square_dual_slope_model(x, y)
```

它记录：

```text
common_leg = L
dual_slope_x = L/x
dual_slope_y = L/y
x_is_pythagorean
y_is_pythagorean
dual_x_is_pythagorean
dual_y_is_pythagorean
all_four_slopes_are_pythagorean
reconstructed_x
reconstructed_y
reconstructed_common_leg
self_dual_identity_holds
```

新增测试：

```text
test_sum_ab_four_square_dual_slope_model_records_both_pythagorean_halves
```

---

## 5. 对证明路线的影响

`sum=A+B` 第一分支现在可以写成一个更对称的子命题：

```text
x,y,a,b in Q_{>0}
all of x,y,a,b are Pythagorean leg ratios
a = (x+y-1)/x
b = (x+y-1)/y
=> x = y
```

或等价地：

```text
a,b are Pythagorean leg ratios
D = a+b-ab > 0
x = b/D
y = a/D
x,y are also Pythagorean leg ratios
=> x = y
```

普通话说：

```text
现在问题像一个闭环：
两个勾股斜率生成另外两个斜率；
如果另外两个也还是勾股斜率，是否只能是对称情况？
```

这给后续两条路线：

```text
1. 递降：若有非对称解，反构造会不会产生一个更小的非对称解；
2. 局部估值：四个勾股斜率同时存在，会不会强迫某个 3 mod 4 素数奇赋值矛盾。
```

小范围只读探针：

```text
枚举 a,b 为勾股斜率；
D = a+b-ab > 0；
x = b/D；
y = a/D；
检查 x,y 是否也为勾股斜率。
```

结果：

```text
max_m=8  hits=0 noncenter=0
max_m=12 hits=0 noncenter=0
max_m=16 hits=0 noncenter=0
max_m=20 hits=0 noncenter=0
```

普通话说：

```text
小范围里连四勾股闭环都没出现。
这支持“sum=A+B 真闭合为空”的方向，
但仍然只是有限线索。
```

---

## 6. 当前边界

可以安全说：

```text
1. 四平方条件已被翻译成四个勾股斜率的双斜率模型；
2. 这个模型能精确区分“x,y 过关但 P,Q 不过关”和“P,Q 过关但 x,y 不过关”；
3. 反构造恒等式已由测试锁住。
```

不能说：

```text
四勾股斜率闭环已证明只能对称。
sum=A+B 已证明。
全平面倒数定理已证明。
```
