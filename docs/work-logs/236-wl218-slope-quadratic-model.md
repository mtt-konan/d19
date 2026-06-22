# wl236 — wl218 slope quadratic model

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支的 squareclass-ratio 引理。

上一轮 wl235 得到商变量：

```text
T = t - 1/t
U = u - 1/u
```

但这个变量其实有更直观的含义。

由于：

```text
x = (1-t^2)/(2t)
```

所以：

```text
T = t - 1/t = -2x.
```

同理：

```text
U = -2y.
```

普通话说：

```text
T,U 模型不是新世界。
它其实就是原来的两个勾股斜率 x,y，只是乘了 -2。
```

---

## 2. 直接的 `x,y` 二次型

在 `sum=A+B` 四斜率模型里：

```text
lambda = 1/(x+y-1)
r = lambda*x
s = lambda*y
```

剩余 squareclass-ratio 条件是：

```text
r^2+1 和 s^2+1 同 squareclass。
```

直接算：

```text
r^2+1 = P / (x+y-1)^2
s^2+1 = Q / (x+y-1)^2
```

其中：

```text
P = 2x^2 + 2xy - 2x + y^2 - 2y + 1
Q = x^2 + 2xy - 2x + 2y^2 - 2y + 1.
```

所以当前候选引理等价于：

```text
x,y 是正有理勾股斜率
x+y>1
P/Q 是有理平方
=> x=y.
```

普通话说：

```text
我们现在不用再提 t,u 或 T,U。
问题就是两个已经合法的勾股斜率 x,y，
看这两个二次型的比值能不能是平方。
```

---

## 3. 中线因子

有：

```text
P - Q = (x-y)(x+y).
```

在本问题里：

```text
x>0, y>0.
```

所以：

```text
P=Q <=> x=y.
```

普通话说：

```text
如果两个量完全相等，马上就是中线。
难点仍然是：它们会不会相差一个非平凡平方倍数。
```

---

## 4. `s,d` 形式

令：

```text
s = x+y
d = x-y
```

则：

```text
P = (d^2 + 2ds + 5s^2 - 8s + 4)/4
Q = (d^2 - 2ds + 5s^2 - 8s + 4)/4.
```

也就是说，`P` 和 `Q` 只差 `d` 的一次项符号。

如果写：

```text
P = k^2 Q
```

并把它看成 `d` 的二次式，判别式分解为：

```text
-(k^2s-k^2-ks-s+1)(k^2s-k^2+ks-s+1).
```

普通话说：

```text
非中线就是 d 不为 0。
方程对 d 是二次的，而且判别式已经裂成两个线性因子。
这比原来的四次式干净很多。
```

---

## 5. 放大空间仍有假反例

若只要求 `x,y` 是任意正有理数，命题是假的。

来自 wl235 的假反例：

```text
T = -7, U = -35/17
```

对应：

```text
x = 7/2
y = 35/34
```

这时：

```text
P/Q = 28561/15625 = (169/125)^2.
```

但：

```text
x^2+1 = 53/4        不是有理平方
y^2+1 = 2381/1156  不是有理平方.
```

所以必须保留：

```text
x,y 是勾股斜率。
```

普通话说：

```text
二次型本身不会排除所有假点。
真正强的条件是 x,y 已经各自来自直角三角形。
```

---

## 6. 代码入口

新增 helper：

```text
sum_ab_squareclass_ratio_slope_quadratic_model(x, y)
```

它记录：

```text
P
Q
P/Q 是否平方
x^2+1 是否平方
y^2+1 是否平方
```

测试：

```text
test_sum_ab_squareclass_ratio_slope_quadratic_model_matches_quotient_model
```

覆盖：

```text
1. 与 wl235 的 T,U 模型一致；
2. 放大空间假反例 P/Q 是平方，但 x,y 不是勾股斜率。
```

---

## 7. 当前证明边界

可以安全说：

```text
sum=A+B 的剩余核心已压缩成 x,y 二次型命题：

x,y 是正有理勾股斜率，x+y>1，
P/Q 是平方
=> x=y。
```

不能说：

```text
这个命题已经证明。
sum=A+B 已关闭。
倒数定理已证明。
```

---

## 8. 下一步

最合理的下一步是直接证明：

```text
x^2+1 square
y^2+1 square
P/Q square
=> x=y.
```

可选路线：

```text
1. 参数化 x,y 为勾股斜率后，对 d 判别式做局部符号；
2. 用 s=x+y, d=x-y 证明 d!=0 时 P/Q 的某个素因子奇次出现；
3. 将 P/Q square 看成两个二次型表示同一 squareclass，做 2-descent。
```
