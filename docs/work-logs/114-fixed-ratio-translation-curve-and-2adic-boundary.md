# wl114 — 固定比例：R_k 上的固定平移问题与 2-adic 边界

日期：2026-06-09

承接 wl113。本轮继续把 `A=kB` 的跨 orbit closure 往标准曲线语言里压。

结论：

```text
固定比例剩余问题可以看成：
R_k 这条 concordant 曲线上的两个点，横坐标相差一个固定值。

已知 involution r -> k/r 保持 R_k；
closure 要求的是 r -> T-r 或 r -> r+T 也把一个点送回 R_k。
```

我们想证明：

```text
closure 的固定平移/反射没有产生新点；
如果产生，只能落回 r -> k/r 的 reciprocal orbit。
```

目前还没有证明，但这个表述比“扫 N”更接近椭圆曲线工具。

---

## 1. R_k 是一条 concordant 曲线

定义：

```text
R_k = { r in Q_{>0} : r^2+1 和 r^2+k^2 都是有理平方 }
```

令：

```text
a = 2r
```

则条件变成：

```text
a^2 + 4      是有理平方
a^2 + 4k^2   是有理平方
```

这就是一条 Euler concordant form 型曲线：

```text
x^2 + 4      = square
x^2 + 4k^2   = square
```

换成椭圆曲线语言，它对应：

```text
E_{4,4k^2}: y^2 = x(x+4)(x+4k^2)
```

这里的 `x` 是平方截面变量，不要和上面的 `a` 混淆；重点是：

```text
R_k 不是有限列表，而是一条椭圆曲线型对象的特殊有理点集合。
```

---

## 2. closure 是 R_k 上的固定平移/反射

sum branch：

```text
r+s = T
```

等价于：

```text
s = T-r
```

diff branch：

```text
|r-s| = T
```

等价于：

```text
s = r+T
```

其中：

```text
T = k+1 或 k-1
```

所以剩余问题是：

```text
R_k ∩ (T - R_k)
R_k ∩ (R_k - T)
```

是否只有 reciprocal orbit 带来的退化点。

普通话版本：

```text
我们有一条曲线 R_k。
已知把 r 换成 k/r 还在曲线上。
现在问：把 r 平移/反射一个固定距离 T 后，还会不会也在曲线上。
```

---

## 3. 为什么这通常比单条椭圆曲线更硬

单个 `r ∈ R_k` 已经是 genus-1 / 椭圆曲线问题。

closure 要求：

```text
r ∈ R_k
T-r ∈ R_k
```

或：

```text
r ∈ R_k
r+T ∈ R_k
```

这相当于两份同一曲线在 `r` 轴上的固定平移交。

若先只参数化：

```text
r^2+1 是平方
```

可写：

```text
r = (t^2-1)/(2t)
```

再要求：

```text
r^2+k^2 是平方
(T-r)^2+1 是平方
(T-r)^2+k^2 是平方
```

会得到多条四次条件同时成立。一般不再是简单 conic，而是更高约束的曲线交。

这解释了为什么：

```text
1. 小搜索里 ratio 很少，但不能当证明；
2. 纯模筛会被无穷远点骗过；
3. 需要 2-descent / Mordell-Weil sieve / Chabauty 类工具。
```

---

## 4. 2-adic 小观察：只能剪枝，不能证明

把 q 模型齐次化。

sum branch：

```text
q = Q/D,  gcd(Q,D)=1
T = k±1
```

四个平方条件之一是：

```text
(Q-TD)^2 + 4D^2 是平方。
```

另一个同边条件是：

```text
(Q+TD)^2 + 4D^2 是平方。
```

看模 `8/16` 可以得到一个小限制：

```text
如果 T 是奇数，则 D 不能是奇数。
```

理由：

```text
D 奇数时，若 Q±TD 为奇数，则 (Q±TD)^2+4D^2 ≡ 5 (mod 8)，不是平方。
所以 Q-TD 和 Q+TD 都必须为偶数。
若 T 也是奇数，则这迫使 Q 与 D 同奇偶，和 gcd(Q,D)=1 矛盾。
```

更精细地看模 `16`，可得到一些 `Q±TD` 的整除限制。

但这仍然不是证明：

```text
T 奇数时，D 可以是偶数；
T 偶数时，D 可以是奇数；
后续条件并不会在 2-adic 层立刻矛盾。
```

普通话版本：

```text
奇偶能砍掉一些分母形态，但不能把固定比例全砍掉。
```

---

## 5. 当前最安全的证明目标

结合 wl112 / wl113 / 本 wl，当前最干净的 theorem target 是：

```text
For integer k>=2 and T∈{k+1,k-1},
prove that every rational r satisfying:

r ∈ R_k
T-r ∈ R_k

or:

r ∈ R_k
r+T ∈ R_k

must satisfy the reciprocal relation

r(T-r)=k       in the sum branch
or
r(r+T)=k       in the diff branch.
```

然后：

```text
reciprocal relation => wl110 排除。
```

这条如果太硬，可以先做分层版本：

```text
1. 先证明若 T 奇数，则 denominator 必须偶数，并研究 2-adic 赋值是否无限上升。
2. 对固定 k，把 R_k 和其平移交转成 Sage 模型，列尽有理点。
3. 找到低 rank 的 k 家族，先证明一批 k。
4. 再尝试把 rank-zero / squareclass obstruction 参数化成 k 的同余类。
```

---

## 6. 现在不能说什么

还不能说：

```text
A=kB 已证明无解。
```

也不能说：

```text
2-adic 已经足够关闭固定比例。
```

能说的是：

```text
固定比例剩余问题已经从整数搜索变成：
concordant 曲线 R_k 与自身固定平移的交点问题。
```

这已经是一个更标准、更可审计的理论目标。
