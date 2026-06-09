# wl151 — `sum=A+B` cross-gcd denominator source

日期：2026-06-09

## 1. 本轮问题

wl150 说明普通 shared-leg 双勾股不是矛盾。

真正剩下的是：

```text
same orientation
both-pass
nu-mv != 0
```

而且必须使用额外结构：

```text
P = bc
Q = ad
```

普通话说：

```text
P 和 Q 不是随便两条边。
它们来自同两组 Euclid 腿的交叉乘。
```

所以这轮先把交叉乘的 gcd 结构暴露成代码入口。

---

## 2. 新 helper

新增：

```text
sum_ab_same_orientation_cross_gcd_terms(...)
```

它接收两组 same-orientation Euclid 参数：

```text
x = a/b
r = c/d
```

并记录：

```text
P = bc
Q = ad
gcd(P,Q)
gcd(a,b)
gcd(c,d)
gcd(a,c)
gcd(a,d)
gcd(b,c)
gcd(b,d)
```

关键恒等式是：

```text
若 gcd(a,b)=gcd(c,d)=1，
则 gcd(bc,ad)=gcd(a,c)gcd(b,d)。
```

普通话说：

```text
两条原始腿各自已经约分干净时，
P 和 Q 的共同因子只能从 a/c 的共同因子、b/d 的共同因子来。
不会从 a/b 或 c/d 内部偷出来。
```

这正好是后续做整除吸收 / 递降时需要的第一层账本。

---

## 3. 样例

继续使用之前的 near-miss：

```text
(m,n) = (4,1), odd
(u,v) = (7,2), odd

a,b = 15,8
c,d = 45,28

N = 105
P = bc = 8*45  = 360
Q = ad = 15*28 = 420
```

gcd 账本：

```text
gcd(a,b) = 1
gcd(c,d) = 1

gcd(a,c) = 15
gcd(b,d) = 4

gcd(P,Q) = gcd(360,420) = 60
gcd(a,c)gcd(b,d) = 15*4 = 60
```

所以：

```text
P-Q = -60
(P-Q)/gcd(P,Q) = -1
```

同一组参数换成 even/even：

```text
P = 420
Q = 360
gcd(P,Q) = 60
(P-Q)/gcd(P,Q) = 1
```

普通话说：

```text
这个样例里 P 和 Q 的差刚好只剩一个 gcd 单位。
这不是证明，但很像递降入口：
共同因子剥掉后，非退化量 nu-mv 还剩多少？
```

---

## 4. 能说什么，不能说什么

可以说：

```text
same-orientation 分支现在有代码入口检查 P=bc, Q=ad 的交叉 gcd 来源。
primitive 情况下 gcd(P,Q)=gcd(a,c)gcd(b,d) 可被直接验证。
```

不能说：

```text
same orientation 已关闭。
nu-mv != 0 已矛盾。
near-miss 样例已经给出一般规律。
```

这轮只是把账本补齐。

普通话说：

```text
我们还没有抓到犯人，
但现在知道每一笔钱从哪个账户进出。
```

---

## 5. 下一步

下一步不要再扫普通 shared-leg。

应该把这层 gcd 账本接到 both-pass 的两套因子参数：

```text
N = g1 r1 s1 = g2 r2 s2
P = g1(s1^2-r1^2)/2
Q = g2(s2^2-r2^2)/2
```

并同时使用：

```text
gcd(P,Q)=gcd(a,c)gcd(b,d)
P-Q = ±2(mu+nv)(nu-mv)
P+Q = 2(mu-nv)(mv+nu)
```

最值得看的量：

```text
(P-Q)/gcd(P,Q)
(P+Q)/gcd(P,Q)
nu-mv 与 gcd(P,Q) 的关系
```

如果 `nu-mv != 0` 时这些量能生成更小的 same-orientation both-pass，
才可能变成递降证明。

---

## 6. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_cross_gcd_terms_expose_denominator_source -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
28 passed
392 passed, 2 warnings
```
