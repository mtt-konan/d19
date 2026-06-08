# wl113 — 固定比例：closure 后得到有理平方矩形

日期：2026-06-09

承接 wl112。本轮继续推 `A=kB` 的跨 orbit 分支。

结论先写前面：

```text
sum/diff closure 后，四个距离平方可以排成一个“有理平方矩形”：

X, X+U, X+V, X+U+V

四个全是有理平方。
```

这不是直接矛盾。它把问题接到了 Euler concordant forms / 椭圆曲线一类对象上。好处是：剩余问题更标准；坏处是：它不是一个初等同余筛能一刀切掉的东西。

---

## 1. sum closure 的 q 模型

固定：

```text
r,s ∈ R_k
r+s = T
```

其中：

```text
T = k+1 或 k-1
```

令：

```text
q = s-r
```

则：

```text
r = (T-q)/2
s = (T+q)/2
```

四个平方条件：

```text
r^2+1       是平方
s^2+1       是平方
r^2+k^2     是平方
s^2+k^2     是平方
```

乘以 4 后变成：

```text
X = (T-q)^2 + 4
Y = (T+q)^2 + 4
Z = (T-q)^2 + 4k^2
W = (T+q)^2 + 4k^2
```

要求：

```text
X,Y,Z,W 全是有理平方。
```

它们满足：

```text
Y - X = 4qT
W - Z = 4qT
Z - X = 4(k^2-1)
W - Y = 4(k^2-1)
```

所以：

```text
X, Y, Z, W
```

排成一个矩形：

```text
X ---- +4qT ---- Y
|                |
+4(k^2-1)        +4(k^2-1)
|                |
Z ---- +4qT ---- W
```

四个顶点都是有理平方。

另一个等价关系是：

```text
X + W = Y + Z
```

普通话版本：

```text
closure 以后，不是随便四个平方。
它们是一个矩形的四个角：左右差一样，上下差也一样。
```

---

## 2. diff closure 也进同一个模型

若：

```text
|r-s| = T
```

其中：

```text
T = k+1 或 k-1
```

把较大者写成：

```text
s = r + T
```

再令：

```text
L = r+s
```

则：

```text
r = (L-T)/2
s = (L+T)/2
```

四个平方条件乘以 4 后为：

```text
X = (L-T)^2 + 4
Y = (L+T)^2 + 4
Z = (L-T)^2 + 4k^2
W = (L+T)^2 + 4k^2
```

于是：

```text
Y - X = 4LT
W - Z = 4LT
Z - X = 4(k^2-1)
W - Y = 4(k^2-1)
```

也同样是有理平方矩形。

区别只是：

```text
sum branch:  T 固定，q=s-r 是变量
diff branch: T 固定，L=r+s 是变量
```

所以 sum/diff closure 可以统一看成：

```text
存在有理变量 M，使

(M-T)^2 + 4,
(M+T)^2 + 4,
(M-T)^2 + 4k^2,
(M+T)^2 + 4k^2

全是有理平方。
```

其中 `T` 是 `k+1` 或 `k-1`。

---

## 3. 为什么这不是直接矛盾

“四个平方排成矩形”本身不是不可能。

原因很简单：只要固定 `k` 有两个不同的真实 ratio：

```text
r,s ∈ R_k
```

就自动得到：

```text
r^2+1, s^2+1, r^2+k^2, s^2+k^2
```

四个平方，并且上下差都是：

```text
k^2-1
```

所以不能证明：

```text
有理平方矩形不存在。
```

我们真正需要证明的是更窄的版本：

```text
这个平方矩形的横向差不能刚好来自 closure target T=k±1。
```

换句话说，矩形存在，但不能有指定形状。

---

## 4. 与 rs=k 目标的关系

sum branch 里：

```text
p = rs = (T^2-q^2)/4
```

所以：

```text
q^2 = T^2 - 4p
```

wl112 里的目标：

```text
rs = k
```

在 q 模型中就是：

```text
q^2 = T^2 - 4k
```

这会把 `r,s` 逼回 reciprocal orbit。

因此现在的最强 theorem target 可以写成：

```text
若四个数

(T-q)^2 + 4,
(T+q)^2 + 4,
(T-q)^2 + 4k^2,
(T+q)^2 + 4k^2

都是有理平方，且 T=k±1，
则 q^2 = T^2 - 4k。
```

一旦这个命题成立：

```text
q^2 = T^2 - 4k
=> rs=k
=> s=k/r
=> wl110 排除。
```

边界：

```text
这个命题目前还没证明。
```

---

## 5. 代数抓手：对角和与交叉乘积

四个平方满足：

```text
X + W = Y + Z
```

也就是：

```text
X, Y, Z, W 是四个有理平方，且两组对角和相等。
```

交叉乘积差也有简单式子。

sum branch 中：

```text
XW - YZ = -16 q (k-1)(k+1)^2      when T=k+1
XW - YZ = -16 q (k-1)^2(k+1)      when T=k-1
```

统一看就是：

```text
XW - YZ = -16 q T (k^2-1)
```

这些关系还不能直接推出矛盾，因为平方差/平方乘积有很多表示。

但它们给后续 p-adic 或 2-descent 证明提供了可用结构：

```text
1. 四个顶点都是平方。
2. 横向差相等。
3. 纵向差固定为 4(k^2-1)。
4. 对角和相等。
5. closure target 固定 T=k±1。
```

---

## 6. 文献定位

这种“四个平方满足两个二次型/两个差条件”的问题不是 d19 独有。

相关关键词：

```text
Euler concordant forms
concordant forms
rational squares in arithmetic progressions
theta-congruent numbers
```

本地已有相关路线：

```text
docs/MULTI_CONCORDANT_N_STRATEGY.md
docs/literature/notes/ono-1996-concordant.md
```

外部参考可先看：

```text
Ken Ono, Euler's Concordant Forms
https://uva.theopenscholar.com/files/ken-ono/files/016_8.pdf

MathWorld, Concordant Form
https://mathworld.wolfram.com/ConcordantForm.html
```

注意：

```text
这些文献能说明问题落在椭圆曲线/二次型框架里，
但不能直接替我们证明 Harborth square fixed-ratio 分支无解。
```

---

## 7. 下一步

下一步最合理的是把 wl112 的 `p=rs` 和本 wl 的 `q` 矩形模型合并成一个可验证的 theorem target：

```text
Fixed-Ratio Closure Target:

For integer k>=2 and T∈{k+1,k-1}, prove there is no rational q with
0<|q|<T in the sum branch such that:

(T-q)^2 + 4,
(T+q)^2 + 4,
(T-q)^2 + 4k^2,
(T+q)^2 + 4k^2

are all rational squares,

except possibly q^2=T^2-4k, which reduces to reciprocal orbit and is
already impossible by wl110.
```

如果这条仍然太硬，退一步做：

```text
对固定小 k，把上面四平方矩形转成椭圆曲线交，
用 Sage/Mordell-Weil sieve 列尽 q。
```

普通话总结：

```text
我们没有把 A=kB 全证掉。
但剩余问题现在已经非常窄：
证明某个指定形状的“有理平方矩形”不存在。
```
