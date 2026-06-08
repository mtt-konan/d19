# wl110 — 固定比例 A=kB：reciprocal orbit 可关闭，跨 orbit 仍是硬点

日期：2026-06-09

承接 wl109 的 exact multi-N / ratio 路线。本轮继续尝试证明：

```text
A = kB 是否一定不可能？
```

先写结论：

```text
还没有证明所有整数 k 都不可能。
但可以严谨证明一块：同一个 reciprocal orbit 里的两个真实 ratio 不可能满足 full-plane closure。
因此任何固定比例反例如果存在，必须来自两个不同 reciprocal orbit。
```

这一步有用，因为它把问题从“任意两个 N”压到更薄的结构：

```text
真实 ratio r = N/B
满足 r^2+1 是有理平方，r^2+k^2 是有理平方。
并且 r 会自动配对到 k/r。
```

---

## 1. 真实 ratio 的 reciprocal 对称

固定：

```text
A = kB,  k >= 1
r = N/B > 0
```

真实 `N` 的两个勾股条件等价于：

```text
r^2 + 1   = u^2
r^2 + k^2 = v^2
```

其中 `u,v` 是正有理数。

那么：

```text
r' = k/r
```

也是真实 ratio，因为：

```text
(k/r)^2 + 1   = (r^2+k^2)/r^2 = (v/r)^2
(k/r)^2 + k^2 = k^2(r^2+1)/r^2 = (ku/r)^2
```

所以真实 ratio 集合带有一个天然二元对称：

```text
r  <->  k/r
```

这解释了 wl109 小表里的成对现象，例如：

```text
k=7:   12/5  <->  35/12
k=10:  35/12 <->  24/7
k=14:  15/8  <->  112/15
```

---

## 2. 同一个 reciprocal orbit 不可能 closure

full-plane closure 在 ratio 层是四种关系：

```text
r1 + r2       = k + 1
r1 + r2       = |k - 1|
|r1 - r2|     = k + 1
|r1 - r2|     = |k - 1|
```

现在只看同一个 orbit：

```text
r2 = k/r1
```

下面记 `r=r1`。

### 2.1 sum = k+1

若：

```text
r + k/r = k + 1
```

则：

```text
r^2 - (k+1)r + k = 0
(r-1)(r-k) = 0
```

所以：

```text
r = 1  或  r = k
```

但：

```text
r=1  -> r^2+1 = 2，不是有理平方
r=k  -> r^2+1 = k^2+1，不可能是有理平方
```

后一条理由很朴素：正整数 `k` 时，`k^2 < k^2+1 < (k+1)^2`。

所以 `sum=k+1` 不可能。

### 2.2 sum = |k-1|

`k=1` 时右边是 0，两个正 ratio 的和不可能为 0。

`k>1` 时若：

```text
r + k/r = k - 1
```

则：

```text
r^2 - (k-1)r + k = 0
```

要有有理根，判别式必须是平方：

```text
D = (k-1)^2 - 4k = k^2 - 6k + 1
```

写成：

```text
D = m^2
(k-3)^2 - m^2 = 8
(k-3-m)(k-3+m)=8
```

整数因子分解只给出正整数 `k` 的候选：

```text
k=6, m=1
```

此时根是：

```text
r = 2 或 r = 3
```

但：

```text
2^2+1 = 5  不是有理平方
3^2+1 = 10 不是有理平方
```

所以 `sum=|k-1|` 也不可能。

### 2.3 diff = k+1

若：

```text
|r - k/r| = k + 1
```

无论取哪一个符号，都会得到判别式：

```text
D = (k+1)^2 + 4k = k^2 + 6k + 1 = (k+3)^2 - 8
```

若它是平方 `m^2`，则：

```text
(k+3-m)(k+3+m)=8
```

同奇偶的正因子对只能是 `(2,4)`，这会给：

```text
k+3 = 3
k = 0
```

和 `k>=1` 矛盾。所以 `diff=k+1` 不可能，甚至不需要再用勾股平方条件。

### 2.4 diff = |k-1|

`k=1` 时这要求：

```text
|r-k/r| = 0
```

即 `r=1`，但 `r^2+1=2` 不是有理平方。

`k>1` 时若：

```text
|r - k/r| = k - 1
```

对应的二次方程有判别式：

```text
D = (k-1)^2 + 4k = (k+1)^2
```

正根只能给：

```text
r = 1 或 r = k
```

但：

```text
r=1 -> r^2+1 = 2，不是有理平方
r=k -> r^2+1 = k^2+1，不可能是有理平方
```

其中后一条仍然是：

```text
k^2+1 是有理平方
```

这不可能。

所以 `diff=|k-1|` 不可能。

---

## 3. 当前已证明的命题

可以安全记录为：

```text
Proposition.
Fix an integer k>=1. Let r>0 be a rational number satisfying
r^2+1 square and r^2+k^2 square. Then the pair (r, k/r) cannot satisfy
any of the four full-plane closure relations:

r+k/r = k+1,
r+k/r = |k-1|,
|r-k/r| = k+1,
|r-k/r| = |k-1|.
```

普通话版本：

```text
固定 A=kB 后，每个真实 N/B 都自带一个镜像 kB/N。
这两个镜像数看起来很像一对候选，但它们永远拼不成正方形 closure。
```

---

## 4. 这还不能证明所有 A=kB

原因是：真实 ratio 集合可能不止一个 reciprocal orbit。

小 exact 扫描中已经看到多 orbit 的 `k`，例如：

```text
k=41, 52, 103
```

这些不是反例，只是说明：

```text
“同 orbit 排除”不能自动覆盖所有 k。
```

真正剩下的是跨 orbit 问题：

```text
是否存在两个不同 orbit 的真实 ratio r,s，
满足 r+s = k+1 或 |k-1|，
或者 |r-s| = k+1 或 |k-1|？
```

写成集合语言：

```text
R_k = { r in Q_{>0} :
        r^2+1 是有理平方，
        r^2+k^2 是有理平方 }

需要证明：
{r+s, |r-s| : r,s in R_k, r not in {s,k/s}}
与 {k+1, |k-1|} 不相交。
```

这是下一层真正的 theorem target。

---

## 5. 为什么不能直接把 Yang Ji 证明推广到所有 k

Yang Ji 的 Theorem 3 证明了：

```text
若正方形边长 = n * 点到某条边的距离，
并且 n 与 n^2+4 都是素数，
则四顶点距离不能全为有理数。
```

映射到 d19：

```text
inside branch:  n = k + 1
outside branch: n = k - 1
```

所以 Yang Ji 已经关闭一批固定比例线，但不是所有整数 `k`。

尝试去掉素数条件时会遇到真实障碍。Yang Ji 递降里会出现辅助方程：

```text
(a^2+b^2)^2 + (n a b)^2 = e^2
```

对很多复合 `n`，这个辅助方程有小整数解，例如：

```text
n=6, a=1, b=2, e=13
```

因为：

```text
(1^2+2^2)^2 + (6*1*2)^2
= 5^2 + 12^2
= 13^2
```

这不等于找到正方形反例；它只说明：

```text
Yang Ji 的素数条件不是随便多余的。
原证明那条无限递降不能不加新信息就推广到所有整数 n。
```

---

## 6. 下一步证明方向

最干净的下一步不是继续扩大 `B` 扫描，而是攻跨 orbit 方程。

把一个真实 ratio 参数化：

```text
r^2+1 = square
```

可令：

```text
r = (t^2-1)/(2t),  t in Q, t>1
```

再要求：

```text
r^2+k^2 = square
```

会得到一条 genus-1/椭圆曲线风格的条件。若再塞入 closure：

```text
s = k+1-r
s = |k-1|-r
s = r+(k+1)
s = r+|k-1|
```

就变成“同一条固定 k 曲线上的两个有理点，是否能有指定线性关系”的问题。

建议下一个 proof note 只做一件事：

```text
对跨 orbit closure 建立精确代数曲线；
先不要 claim 无解；
看它是否能被降到已知的中线/边线/固定 n 素数分支，
或是否需要 Mordell-Weil sieve / Chabauty 这类重工具。
```

当前最强结论：

```text
A=kB 尚未全局证明不可能。
但固定比例反例如果存在，不能来自最自然的 reciprocal pair；
它必须来自两个不同的 concordant ratio orbit。
```
