# wl258 — wl218 slope individual square layer

日期：2026-06-22

## 1. 本轮目标

接 wl257。

前几轮主要处理 product-layer residual 和 Gaussian centerline shadow。
本轮回到 `sum=A+B` 的真成员条件，把四个平方条件在斜率模型里拆开。

普通话说：

```text
以前我们经常问 P/Q 是不是平方。
但真 R_lambda 成员更强：
不只是两个东西的比例像平方，
而是每一个东西自己就必须是平方。
```

---

## 2. 斜率模型

若：

```text
r,s in R_lambda
r+s = lambda+1
```

令：

```text
x = r/lambda
y = s/lambda
L = x+y-1 = 1/lambda
```

因为：

```text
r^2 + lambda^2 是平方
s^2 + lambda^2 是平方
```

所以：

```text
x^2 + 1 是平方
y^2 + 1 是平方
```

而：

```text
r = x/L
s = y/L
```

因此：

```text
r^2 + 1 = (x^2 + L^2) / L^2
s^2 + 1 = (y^2 + L^2) / L^2
```

记：

```text
P = x^2 + L^2
Q = y^2 + L^2
```

展开就是 wl236 的两个二次型：

```text
P = 2x^2 + 2xy - 2x + y^2 - 2y + 1
Q = x^2 + 2xy - 2x + 2y^2 - 2y + 1
```

普通话说：

```text
sum=A+B 的真候选，在 x,y 语言里要同时满足四件事：
x 是勾股斜率，y 是勾股斜率，
P 是平方，Q 是平方。
```

---

## 3. 比值平方不够

旧的弱条件是：

```text
P/Q 是平方
```

真条件更强：

```text
P 是平方
Q 是平方
```

但即使 `P,Q` 各自平方，也仍然不够；还必须要求 `x,y` 自己是勾股斜率。

放大空间假反例：

```text
x = 7/2
y = 35/34
```

这时：

```text
P/Q = 28561/15625 = (169/125)^2
P 是平方
Q 是平方
```

但：

```text
x^2 + 1 不是平方
y^2 + 1 不是平方
```

所以它不是 `sum=A+B` 的真候选。

普通话说：

```text
P,Q 过关，只说明 r^2+1 和 s^2+1 过关。
还要 x,y 过关，才说明 r^2+lambda^2 和 s^2+lambda^2 也过关。
四个平方少一个都不行。
```

---

## 4. 新字段

扩展 helper：

```text
sum_ab_squareclass_ratio_slope_quadratic_model(x, y)
```

新增字段：

```text
numerator_is_square
denominator_is_square
individual_unit_terms_are_squares
```

新增测试：

```text
test_sum_ab_squareclass_ratio_slope_model_tracks_individual_squares
```

它锁住两件事：

```text
1. 一个正常勾股斜率样例里，P/Q 不平方，P,Q 也不各自平方；
2. 放大空间假反例里，P,Q 各自平方，但 x,y 不是勾股斜率。
```

---

## 5. 有限线索

已有 helper：

```text
sum_ab_four_slope_squareclass_summary(max_m)
```

直接在 `x,y` 是勾股斜率的空间里统计弱命中。

本轮只读探针：

```text
max_m=8  : equal=21  center=21  noncenter=0  true_four_pass=0
max_m=20 : equal=119 center=119 noncenter=0  true_four_pass=0
max_m=28 : equal=227 center=227 noncenter=0  true_four_pass=0
max_m=36 : equal=368 center=368 noncenter=0  true_four_pass=0
```

尝试 `max_m=44` 时整数分解变慢，已中断；不把它作为结论。

普通话说：

```text
在这些小范围里，只要 x,y 已经是勾股斜率，
弱的 P/Q 平方命中都落在 x=y 中线。
没有非中线真候选。
```

这仍然不是证明。

---

## 6. 对证明路线的影响

现在 `sum=A+B` 第一分支可以被压成一个更精确的子命题：

```text
x,y in Q_{>0}
x^2+1 square
y^2+1 square
x+y>1
P = x^2 + (x+y-1)^2 square
Q = y^2 + (x+y-1)^2 square
=> x=y
```

若 `x=y`，回到 centerline；centerline 已由 wl226 / wl241 接到 Yang Ji
或本地 quartic 缺口。

普通话说：

```text
真正要打的不是一个平方比值，
而是两组直角三角形共享同一个 L=x+y-1。
如果能证明这种共享只能发生在 x=y，
sum=A+B 就会关到 centerline。
```

---

## 7. 当前边界

可以安全说：

```text
1. 真成员条件在斜率模型中已拆成 x,y,P,Q 四个平方；
2. P/Q square、甚至 P 和 Q individually square，都不是完整条件；
3. 小范围中，x,y 为勾股斜率时没有非中线弱命中。
```

不能说：

```text
四平方斜率子命题已证明。
sum=A+B 已证明。
全平面倒数定理已证明。
```
