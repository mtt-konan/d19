# wl146 — `sum=A+B` same-orientation both-pass parameter frame

日期：2026-06-09

## 1. 本轮问题

wl145 已经能把一个通过的 shared-leg 方程写成：

```text
H-P = g r^2
H+P = g s^2
```

并还原：

```text
N = g r s
P = g(s^2-r^2)/2
H = g(s^2+r^2)/2
```

这轮搭 both-pass 的反证框架。

普通话说：

```text
假设 other 和 failed 都通过。
那同一个 N 会被两套勾股参数同时解释。
我们先把这套方程架子搭好。
```

---

## 2. both-pass 假设

same orientation 已经化成：

```text
other:  N^2 + P^2 = H1^2
failed: N^2 + Q^2 = H2^2
```

其中：

```text
P = bc
Q = ad
```

both-pass 假设下，引入两套参数：

```text
other:  (g1, r1, s1)
failed: (g2, r2, s2)
```

满足：

```text
N = g1 r1 s1 = g2 r2 s2
P = g1(s1^2-r1^2)/2
Q = g2(s2^2-r2^2)/2
```

普通话说：

```text
同一条腿 N，配出两条不同的勾股边 P 和 Q。
```

---

## 3. odd/odd 的 P,Q

odd orientation：

```text
a = m^2-n^2
b = 2mn
c = u^2-v^2
d = 2uv
```

所以：

```text
P = bc = 2mn(u^2-v^2)
Q = ad = 2uv(m^2-n^2)
```

也就是：

```text
P = 2mn(u-v)(u+v)
Q = 2uv(m-n)(m+n)
```

差和和有漂亮分解：

```text
P - Q = 2(mu+nv)(-mv+nu)
P + Q = 2(mu-nv)(mv+nu)
```

---

## 4. even/even 的 P,Q

even orientation：

```text
a = 2mn
b = m^2-n^2
c = 2uv
d = u^2-v^2
```

所以：

```text
P = bc = 2uv(m^2-n^2)
Q = ad = 2mn(u^2-v^2)
```

也就是 odd/odd 的 P,Q 对调。

分解为：

```text
P - Q = -2(mu+nv)(-mv+nu)
P + Q =  2(mu-nv)(mv+nu)
```

---

## 5. 为什么 P=Q 很重要

如果 both-pass 最后能推出：

```text
P = Q
```

那么 same orientation 下：

```text
bc = ad
```

也就是：

```text
b/a = d/c
```

普通话说：

```text
两个分母相等时，other 和 failed 其实变成同一个平方检查。
这很可能对应镜像/退化分支。
```

odd/odd 中：

```text
P-Q = 2(mu+nv)(-mv+nu)
```

正参数下：

```text
mu+nv > 0
```

所以：

```text
P=Q  等价于  nu = mv
```

如果再加：

```text
gcd(m,n)=gcd(u,v)=1
```

通常会逼近：

```text
(u,v) 与 (m,n) 同比例
```

primitive 情况下很可能就是同一组参数。

这正好接近主理论里的：

```text
s = lambda/r
```

---

## 6. 现在还缺什么

目前还没有证明：

```text
both-pass => P=Q
```

现在只是把 both-pass 写成：

```text
g1 r1 s1 = g2 r2 s2
g1(s1^2-r1^2)/2 = P
g2(s2^2-r2^2)/2 = Q
```

并且知道：

```text
P-Q
```

高度可分解。

普通话说：

```text
我们已经把“如果真的四通过，会长什么样”写清楚了。
但还没证明这种样子只能退化成 P=Q。
```

---

## 7. 下一步攻击点

下一步有三条可试：

```text
1. 直接尝试证明 both-pass => P=Q。
   看 g1,r1,s1 和 g2,r2,s2 的共享 N 是否强迫两个分母相等。

2. 对 P-Q 的因子做整除分析：
   P-Q = 2(mu+nv)(nu-mv)

3. 找递降：
   如果 P != Q 且 both-pass，
   用两套 shared-leg 参数构造更小的 both-pass。
```

普通话说：

```text
现在最像证明的路线是：
假设有 both-pass；
如果 P 不等于 Q，
就从两套因子里造出更小的例子；
无限递降矛盾。
```

---

## 8. 能说什么，不能说什么

可以说：

```text
same orientation both-pass 已有明确的参数方程框架。
P±Q 的 Euclid 因式分解非常干净。
P=Q 会自然接向镜像/退化。
```

不能说：

```text
both-pass 已排除。
same orientation 已关闭。
P=Q 已经被证明。
```

---

## 9. 下一步建议

建议下一步写一个小 helper 或 proof note，专门记录：

```text
same_orientation_denominator_sum_difference
```

输出：

```text
P-Q = ±2(mu+nv)(nu-mv)
P+Q =  2(mu-nv)(mv+nu)
```

这样后续能直接围绕 `nu-mv` 做退化/递降分析。
