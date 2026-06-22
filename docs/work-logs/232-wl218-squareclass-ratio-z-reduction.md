# wl232 — wl218 squareclass-ratio `z = u - 1/u` reduction

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支的候选引理：

```text
x,y 是正有理勾股斜率，x+y>1
lambda = 1/(x+y-1)
r = lambda*x
s = lambda*y

r^2+1 和 s^2+1 同 squareclass
=> x=y
```

上一轮 wl231 把它写成：

```text
A/B 是有理平方 => t=u
```

其中：

```text
x = (1-t^2)/(2t)
y = (1-u^2)/(2u)
0<t,u<1
```

本轮目标是降低 `A = h^2 B` 的代数复杂度。

普通话说：

```text
之前的问题是一个看起来很硬的四次方程。
这轮发现它不是普通四次方程；换一个变量后，它会降成二次方程。
这还不是证明，但证明入口明显变窄了。
```

---

## 2. 原始 squareclass-ratio 方程

定义：

```text
E = t + u - 2tu - t^2u - tu^2
```

则：

```text
r = u(1-t^2)/E
s = t(1-u^2)/E
```

所以：

```text
r^2+1 = A/E^2
s^2+1 = B/E^2
```

其中：

```text
A = u^2(1-t^2)^2 + E^2
B = t^2(1-u^2)^2 + E^2
```

同 squareclass 等价于：

```text
A/B = h^2
```

即：

```text
A - h^2 B = 0.
```

直接展开为 `u` 的四次式：

```text
-(2h^2-1)t^2 u^4
- 2t(h^2-1)(t^2+2t-1) u^3
+ C(t,h) u^2
+ 2t(h^2-1)(t^2+2t-1) u
-(2h^2-1)t^2 = 0
```

其中：

```text
C(t,h)
= -h^2t^4 -4h^2t^3 +2h^2t^2 +4h^2t -h^2
  +2t^4 +4t^3 -2t^2 -4t +2.
```

注意 `u^4` 和常数项相同，`u^3` 和 `u` 项相反。

普通话说：

```text
这个四次式有“反回文”结构。
它在提醒我们：不要把它当普通四次曲线硬打。
```

---

## 3. 关键降维变量

令：

```text
z = u - 1/u.
```

把四次式除以 `u^2` 后，`u^2 + 1/u^2` 可由 `z^2+2` 表示，
`u - 1/u` 就是 `z`。

于是：

```text
A - h^2B = 0
```

等价于一个关于 `z` 的二次方程：

```text
R(t,z,h) = 0
```

其中：

```text
R(t,z,h)
= -h^2t^4 -2h^2t^3z -4h^2t^3
  -2h^2t^2z^2 -4h^2t^2z -2h^2t^2
  +2h^2tz +4h^2t -h^2
  +2t^4 +2t^3z +4t^3
  +t^2z^2 +4t^2z
  -2tz -4t +2.
```

更有用的是它对 `h^2` 是线性的。

把 `H=h^2` 解出来：

```text
H =
(2t^4 +2t^3z +4t^3 +t^2z^2 +4t^2z -2tz -4t +2)
/
(t^4 +2t^3z +4t^3 +2t^2z^2 +4t^2z +2t^2 -2tz -4t +1).
```

也就是：

```text
h^2 = Phi(t,z).
```

普通话说：

```text
以前要问 A/B 是不是平方。
现在可以问一个更小的问题：Phi(t,z) 是不是平方。
```

但要记住：

```text
z 必须来自有理 u。
```

这等价于：

```text
z^2 + 4 是有理平方。
```

因为：

```text
u^2 - zu - 1 = 0.
```

---

## 4. 判别式

把 `R(t,z,h)` 当作 `z` 的二次式，它的判别式为：

```text
-4t^2
*(h^2t^2 + 2h^2t - h^2 - ht^2 - h - t^2 + 1)
*(h^2t^2 + 2h^2t - h^2 + ht^2 + h - t^2 + 1).
```

普通话说：

```text
判别式分成两个线性因子。
这说明这个二次式不是随机的；它有可做局部符号或递降的结构。
```

在中心线 `h=1` 时：

```text
R(t,z,1) = -(-t^2 + tz + 1)(t^2 + tz - 1)
```

根为：

```text
z = t - 1/t
z = -t + 1/t.
```

在本问题 `0<t,u<1` 下：

```text
u=t
=> z=t-1/t < 0.
```

所以中心线对应其中一支。

---

## 5. 对证明路线的影响

之前候选引理是：

```text
A/B square => t=u.
```

现在可以更细地写成：

```text
0<t<1,
z^2+4 square,
Phi(t,z) square
=> z=t-1/t.
```

因为：

```text
z=t-1/t
```

正好恢复：

```text
u=t.
```

普通话说：

```text
我们不用直接打 t,u 两个变量的四次式。
只要证明：同时满足“z 来自某个有理 u”和“Phi(t,z) 是平方”的点，
只能是中线那一支。
```

---

## 6. 代码入口

新增 helper：

```text
sum_ab_squareclass_ratio_z_reduction(t, u)
```

它记录：

```text
z = u - 1/u
direct_ratio = A/B
reduced_ratio = Phi(t,z)
ratio_is_square
u_recovery_square = z^2+4
```

测试：

```text
test_sum_ab_squareclass_ratio_z_reduction_matches_direct_terms
```

用于防止后续手工公式抄错。

---

## 7. 当前状态

可以安全说：

```text
squareclass-ratio 方程已从 u 的四次式降成 z 的二次式。
中心线在 z 方程里是一条显式分支 z=t-1/t。
```

不能说：

```text
候选引理已证明。
sum=A+B 已关闭。
倒数定理已证明。
```

下一步最自然的证明目标是：

```text
证明 0<t<1 且 z^2+4 square 且 Phi(t,z) square
只能给 z=t-1/t。
```

可试两条路：

```text
1. 把 z^2+4 square 参数化，再研究 Phi(t,z) square；
2. 直接对 Phi(t,z) 做 Hilbert-symbol / Gaussian norm 分配，
   证明另一支会产生局部矛盾或递降。
```
