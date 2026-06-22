# wl231 — wl218 squareclass-ratio lemma boundary

日期：2026-06-22

## 1. 本轮目标

继续推进倒数定理的第一分支：

```text
r,s in R_lambda
r+s = lambda+1
=> rs = lambda
```

全平面总目标仍然是四分支：

```text
{r+s, |r-s|} intersect {lambda+1, |lambda-1|} nonempty
=> rs=lambda
```

本轮只处理第一分支 `sum=A+B` 的剩余硬点。

普通话说：

```text
整件事仍是全平面定理。
现在只是先打一扇门：r+s=lambda+1。
这扇门里，真正没关上的是“非中线、但两个坏 squareclass 一样”的可能性。
```

---

## 2. 当前归约

`sum=A+B` 四斜率模型是：

```text
x = r/lambda
y = s/lambda
lambda = 1/(x+y-1)

x, y 是勾股斜率
r = lambda*x
s = lambda*y
```

真成员要求：

```text
x^2+1, y^2+1, r^2+1, s^2+1 全是有理平方。
```

其中 `x,y` 已经先作为勾股斜率选好，所以剩下要打的是：

```text
r^2+1 和 s^2+1。
```

product identity 的 `A_p` 平方只说明：

```text
r^2+1 和 s^2+1 在同一个 rational squareclass。
```

不说明它们各自是平方。

因此当前更准确的候选引理是：

```text
Let x,y be positive Pythagorean leg ratios with x+y>1.
Set lambda = 1/(x+y-1), r=lambda*x, s=lambda*y.

If r^2+1 and s^2+1 have the same rational squareclass,
then x=y.
```

一旦证明这个引理：

```text
true four-pass
=> same unit squareclass
=> x=y
=> centerline
=> Yang Ji centerline theorem closes the branch.
```

普通话说：

```text
不必直接证明 r^2+1、s^2+1 都不可能是平方。
只要证明它们连“坏得一样”都不可能，除非站到中线，就够了。
```

---

## 3. 为什么只看 `q == 3 mod 4` 估值不够

对任意正有理数 `z=a/b`，有：

```text
z^2+1 = (a^2+b^2)/b^2。
```

若素数：

```text
q == 3 mod 4
```

则 `q` 在两个平方和 `a^2+b^2` 里的估值总是偶数。

所以：

```text
z^2+1 的 rational squareclass 不含 q == 3 mod 4 的素数。
```

普通话说：

```text
3 mod 4 素数这盏灯，在 z^2+1 这类数上通常是灭的。
真正造成 squareclass 不为 1 的，主要是 2 和 1 mod 4 素数。
```

已有 near-miss 也吻合这个现象：

```text
normalized triple (7,24,28):
7^2+24^2 = 25^2       squareclass 1
7^2+28^2 = 833 = 17*49 squareclass 17

normalized triple (28,7,45):
28^2+7^2 = 833        squareclass 17
28^2+45^2 = 53^2      squareclass 1
```

这里失败素数是：

```text
17 == 1 mod 4
```

不是 `3 mod 4`。

因此用户原路线：

```text
用各个 p == 3 mod 4 的 valuation 强制 lambda^2-p^2 矛盾
```

需要升级为：

```text
完整 rational squareclass / Gaussian integer / Hilbert-symbol 分配。
```

---

## 4. `t,u` 参数方程

取勾股斜率参数：

```text
x = (1-t^2)/(2t)
y = (1-u^2)/(2u)
```

其中 `0<t,u<1` 对应正斜率。

由：

```text
lambda = 1/(x+y-1)
```

得到公共分母：

```text
E = t + u - 2tu - t^2u - tu^2
```

并且：

```text
r = u(1-t^2)/E
s = t(1-u^2)/E
```

于是：

```text
r^2+1 = A/E^2
s^2+1 = B/E^2
```

其中：

```text
A = u^2(1-t^2)^2 + E^2
B = t^2(1-u^2)^2 + E^2
```

一个非常有用的恒等式是：

```text
A - B = (t-u)(t+u)(tu-1)(tu+1).
```

普通话说：

```text
如果要求 r^2+1 和 s^2+1 完全相等，立刻得到 t=u，也就是 x=y。
但我们需要的是 A/B 是平方，这比 A=B 硬一层。
```

当前核心方程可以写成：

```text
A = k^2 B
```

需要证明在正有理 `0<t,u<1` 且 `E>0` 下：

```text
A/B 是有理平方 => t=u。
```

这就是候选引理的参数版本。

---

## 5. 有限证据

新增诊断 helper：

```text
sum_ab_four_slope_squareclass_witnesses(...)
```

它返回 bounded 四斜率模型里：

```text
r^2+1 和 s^2+1 有相同 squareclass
```

的具体 witness。

小范围结果：

```text
max_m  slope_count  equal  centerline  noncenter  true_four_pass
8      30           21     21          0          0
20     172          119    119         0          0
28     328          227    227         0          0
40     662          457    457         0          0
```

独立 `t,u` 网格：

```text
0<t,u<1, denominator(t), denominator(u) <= 80
A/B square, t != u
```

结果：

```text
none
```

这些都不是证明。

它们只说明：

```text
候选引理目前没有小反例；
下一步值得从 A=k^2B 这条曲线本身下手。
```

---

## 6. 当前证明边界

可以安全说：

```text
sum=A+B 已归约到四斜率模型。
mixed orientation 已有 mod 8 排除。
P=Q 分支归到 centerline，并由 Yang Ji 中线定理关闭。
非中线 P!=Q 分支等价于 squareclass-ratio 引理仍未证明。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
3 mod 4 valuation 已经足够。
有限扫描证明了 squareclass-ratio 引理。
```

---

## 7. 下一步

推荐下一步只做一个数学问题：

```text
证明 A/B 为有理平方时必有 t=u。
```

可选路线：

```text
1. Gaussian integer:
   把 A 和 B 看成两个平方和，
   比较它们在 Z[i] 里的 1 mod 4 素因子分配。

2. 曲线路线:
   固定 k，研究 A=k^2B；
   或改变量 w=(t-u)/(1-tu)，寻找 genus / descent 结构。

3. 递降路线:
   回到 same-orientation 的
   N^2+P^2=H1^2, N^2+Q^2=H2^2,
   N-P=a(d-c), N-Q=c(b-a),
   尝试从 P!=Q 构造更小的 same-orientation both-pass。
```

本轮最重要的修正是：

```text
把用户原来的 p == 3 mod 4 valuation 路线，
升级成完整 squareclass-ratio 引理。
```
