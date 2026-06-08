# wl111 — 固定比例 A=kB：跨 orbit 等价于固定直线问题，Yang fixed-n 不能当黑盒

日期：2026-06-09

承接 wl110。本轮继续尝试证明固定比例：

```text
A = kB
```

wl110 已经证明：

```text
同一个 reciprocal orbit: r <-> k/r
不可能满足 full-plane closure。
```

本轮处理剩下的跨 orbit 情况。结论先写前面：

```text
跨 orbit 不是一个容易的小尾巴。
它正好等价于 square problem 中“点落在一条固定平行线 x=常数 上”的问题。
要证明所有 A=kB，无异于证明所有整数 n 的固定直线分支。
```

另外，本轮发现一个重要审查点：

```text
Yang Ji 的 fixed-n Theorem 3 不能在 d19 里无条件当黑盒使用。
至少论文中一个关键辅助方程“无整数解”的说法按原文是不成立的。
```

这不等于 Yang 的结论一定错，也不等于发现正方形反例；它只说明：

```text
我们不能靠那篇 fixed-n 证明直接关闭 k+1 / k-1 分支。
```

---

## 1. ratio closure 到固定直线

固定 `B=1` 做比例归一化：

```text
A = k
r = N1/B
s = N2/B
```

真实 `N` 条件是：

```text
r^2 + 1   是有理平方
r^2 + k^2 是有理平方
s^2 + 1   是有理平方
s^2 + k^2 是有理平方
```

### 1.1 inside sum target: r+s=k+1

若：

```text
r+s = k+1
```

令：

```text
n = k+1
```

则：

```text
k = n-1
s = n-r
```

四个平方条件变成：

```text
r^2 + 1^2         是有理平方
r^2 + (n-1)^2     是有理平方
(n-r)^2 + 1^2     是有理平方
(n-r)^2 + (n-1)^2 是有理平方
```

这正是一个边长为 `n` 的正方形，点在直线：

```text
x = 1
```

上的四顶点有理距离问题。也就是说，点到一条竖边的距离是 `1`，边长是 `n` 倍这个距离。

普通话版本：

```text
A=kB 且 N1+N2=A+B，
就是把点固定在离左边 1 格、离右边 k 格的位置。
正方形边长是 k+1 格。
```

### 1.2 outside target: r+s=k-1

若 `k>1` 且：

```text
r+s = k-1
```

令：

```text
n = k-1
```

则：

```text
k = n+1
s = n-r
```

平方条件变成：

```text
r^2 + 1^2         是有理平方
r^2 + (n+1)^2     是有理平方
(n-r)^2 + 1^2     是有理平方
(n-r)^2 + (n+1)^2 是有理平方
```

这对应点在正方形外侧：离近边距离 `1`，离远边距离 `n+1`，正方形边长是 `n`。

### 1.3 difference targets

若：

```text
|r-s| = k+1
或
|r-s| = k-1
```

只是把“上下方向”换成了外侧版本。经过 D4 旋转/反射后，本质仍是：

```text
边长 = n * 点到某条边的距离
```

其中：

```text
n = k+1 或 n = k-1
```

所以固定比例 `A=kB` 的跨 orbit 问题就是 fixed-line 问题。

---

## 2. 这解释了为什么纯 residue 筛不够

把固定直线问题齐次化。以 inside branch 为例，令：

```text
y = r
边长 = n
```

如果 `r=Y/Q`，则需要：

```text
Y^2 + Q^2                 是平方
Y^2 + (n-1)^2 Q^2         是平方
(nQ-Y)^2 + Q^2            是平方
(nQ-Y)^2 + (n-1)^2 Q^2    是平方
```

模任意 `M` 时，总有一种“无穷远”型局部幸存：

```text
Q ≡ 0,  Y ≡ 1  (mod M)
```

于是四个左边都退化成：

```text
1
```

都是平方。

这和 wl108 的 universal survivor：

```text
B ≡ 0, N1 ≡ 1, N2 ≡ -1
```

是同一件事。换句话说：

```text
纯模筛看到的是 projective closure 里的无穷远点。
```

所以“继续加模数”不会证明固定比例无解；必须控制分母/赋值，也就是需要：

```text
p-adic valuation
无限递降
或完整的曲线有理点列尽
```

---

## 3. Yang Ji fixed-n 证明的审查点

之前 wl107 / wl110 里提到：

```text
Yang Ji, Several special cases of a square problem
arXiv:2105.05250
```

论文声称证明：

```text
若边长 = n * 点到某条边的距离，
且 n 与 n^2+4 都是素数，
则四个顶点距离不能全为有理数。
```

但是本轮重读原文后发现，Theorem 3 的证明里有一个关键辅助方程：

```text
(a^2+b^2)^2 + (n a b)^2 = e^2
```

文中试图证明它没有整数解。按原文条件，这一步有明显反例：

```text
n = 5
a = 4
b = 3
e = 65
```

直接代入：

```text
(4^2+3^2)^2 + (5*4*3)^2
= 25^2 + 60^2
= 65^2
```

而：

```text
n = 5 是素数
n^2 + 4 = 29 也是素数
a=4 偶, b=3 奇, gcd(a,b)=1
```

所以至少可以确定：

```text
论文中“这个辅助方程无整数解”的证明步骤不能按字面成立。
```

边界要说清楚：

```text
这不是 square problem 的反例。
这个辅助方程只是 fixed-n 问题的必要中间条件，不是充分条件。
```

但对 d19 来说，影响很实际：

```text
不能再把 Yang Theorem 3 当作已经审计通过的黑盒。
若要引用，必须先补上缺失条件，或者只引用独立可核验的部分。
```

---

## 4. 当前安全结论

现在关于 `A=kB` 可以安全说的是：

```text
1. k=1 / centerline 分支仍应单独用 midline 证明处理。
2. 同一个 reciprocal orbit 已由 wl110 关闭。
3. 剩下的跨 orbit 分支等价于 fixed-line square problem。
4. fixed-line 的纯同余筛失败原因已解释为“无穷远局部幸存”。
5. Yang fixed-n 证明不能直接作为全局 closure 证书。
```

还不能说：

```text
所有 A=kB 已证明无解。
```

也不能说：

```text
Yang Theorem 3 已可靠关闭所有满足 prime-pair 条件的 k±1。
```

除非后续对该论文证明补完审查。

---

## 5. 下一步最合理的证明路线

下一步不该继续盲扫 `B`，而应该把 fixed-line 问题写成曲线。

Inside model：

```text
边长 n
点在 x=1
点的纵向坐标 y
```

方程为：

```text
y^2 + 1^2             = square
y^2 + (n-1)^2         = square
(n-y)^2 + 1^2         = square
(n-y)^2 + (n-1)^2     = square
```

Outside model：

```text
边长 n
点在正方形外侧，离近边 1
```

方程为：

```text
y^2 + 1^2             = square
y^2 + (n+1)^2         = square
(n-y)^2 + 1^2         = square
(n-y)^2 + (n+1)^2     = square
```

建议下一篇 proof note 做：

```text
1. 用 y^2+1=square 参数化 y。
2. 把第二个同边条件变成一条 quartic / elliptic curve。
3. 再加入 y -> n-y 的镜像条件。
4. 看能不能对固定 n 得到 Mordell-Weil sieve / Chabauty 可验证模型。
```

一句话：

```text
A=kB 的证明没有死，但它已经变成 fixed-line square problem；
这比原来想象的“筛子推广一下”要硬很多。
```
