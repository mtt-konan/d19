# wl228 — wl218 `sum=A+B` shared-leg offset factorization

日期：2026-06-22

## 1. 本轮目标

继续推进 wl218 倒数定理的第一分支：

```text
r,s in R_lambda
r+s = lambda+1
=> rs = lambda
```

上一轮已经把这个分支化成 same-orientation 的共享腿问题：

```text
N^2 + P^2 = H1^2
N^2 + Q^2 = H2^2

P = bc
Q = ad
N = bc - ac + ad = ad - ac + bc
```

普通话说：

```text
同一条腿 N 要同时和 P、Q 拼成两个直角三角形。
但 P、Q 不是随便来的，它们是同两组 Euclid 参数交叉乘出来的。
```

本轮补一层更直接的恒等式：不仅 `P-Q`、`P+Q` 能分解，`N-P` 和 `N-Q` 也能分解。

---

## 2. 统一的短公式

令：

```text
x = a/b
r = c/d
```

由 `sum=A+B` 的 Mobius 重构：

```text
y = (bc - ac + ad) / bc
s = (ad - ac + bc) / ad
```

same orientation 下两个分子相同：

```text
N = bc - ac + ad = ad - ac + bc
P = bc
Q = ad
```

于是不用展开四次式，直接得到：

```text
N - P = a(d-c)
N - Q = c(b-a)
```

普通话说：

```text
N 离 P 有多远，只看第一组斜率的分子 a，乘上第二组斜率分母减分子 d-c。
N 离 Q 有多远，只看第二组斜率的分子 c，乘上第一组斜率分母减分子 b-a。
```

这比只写：

```text
N^2+P^2, N^2+Q^2
```

更强，因为它把共享腿双勾股和原始 Euclid 参数直接绑在一起。

---

## 3. odd/odd 展开

odd orientation：

```text
a = m^2-n^2
b = 2mn
c = u^2-v^2
d = 2uv
```

因此：

```text
N-P = (m^2-n^2)(2uv - (u^2-v^2))
    = -(m^2-n^2)(u^2 - 2uv - v^2)

N-Q = (u^2-v^2)(2mn - (m^2-n^2))
    = -(u^2-v^2)(m^2 - 2mn - n^2)
```

同时旧账本仍有：

```text
P-Q =  2(mu+nv)(nu-mv)
P+Q =  2(mu-nv)(mv+nu)
```

---

## 4. even/even 展开

even orientation：

```text
a = 2mn
b = m^2-n^2
c = 2uv
d = u^2-v^2
```

因此：

```text
N-P = 2mn((u^2-v^2) - 2uv)
    = 2mn(u^2 - 2uv - v^2)

N-Q = 2uv((m^2-n^2) - 2mn)
    = 2uv(m^2 - 2mn - n^2)
```

旧账本对应：

```text
P-Q = -2(mu+nv)(nu-mv)
P+Q =  2(mu-nv)(mv+nu)
```

---

## 5. 固定样例

样例：

```text
(m,n) = (4,1)
(u,v) = (7,2)
```

odd/odd：

```text
a,b = 15,8
c,d = 45,28
N,P,Q = 105,360,420

N-P = -255 = 15 * (28-45)
N-Q = -315 = 45 * (8-15)
```

even/even：

```text
a,b = 8,15
c,d = 28,45
N,P,Q = 556,420,360

N-P = 136 = 8 * (45-28)
N-Q = 196 = 28 * (15-8)
```

普通话说：

```text
这两个 offset 不是随机差值。
它们直接等于“一个腿分子”乘以“另一组分母减分子”。
```

---

## 6. 对证明路线的影响

both-pass 假设现在可以写得更紧：

```text
N^2 + P^2 = H1^2
N^2 + Q^2 = H2^2

N-P = a(d-c)
N-Q = c(b-a)
P-Q = bc-ad
```

同时，勾股平方条件可改写成因子对：

```text
(H1-P)(H1+P) = N^2
(H2-Q)(H2+Q) = N^2
```

所以后续可以比较三类因子来源：

```text
1. H1±P 和 H2±Q 对 N^2 的分配；
2. N-P 和 N-Q 的 Euclid 腿差分解；
3. P-Q = +/- 2(mu+nv)(nu-mv) 的非退化因子。
```

普通话说：

```text
以前只知道两个三角形共用 N。
现在还知道 N 分别离 P、Q 的距离必须来自很具体的两条腿差。
这给估值或递降多了一处下手点。
```

---

## 7. 小范围 sanity

为了确认没有已经暴露的小 both-pass 例子，本轮重新扫：

```text
primitive same-orientation Euclid 参数
m,u <= 20,40,80,120
N > 0
N^2+P^2 和 N^2+Q^2 同时平方
```

结果：

```text
M=20  both=0
M=40  both=0
M=80  both=0
M=120 both=0
```

这不是证明。

它只说明：

```text
新账本没有立刻撞上小反例；
same-orientation both-pass 仍然只应作为未闭合理论分支处理。
```

---

## 8. 代码入口

扩展：

```text
SumAbSameOrientationDenominatorFactorization
sum_ab_same_orientation_denominator_factorization(...)
```

新增字段：

```text
shared_numerator
shared_minus_other_denominator
shared_minus_failed_denominator
shared_minus_other_factorization
shared_minus_failed_factorization
```

其中：

```text
shared_minus_other_factorization = (a, d-c)
shared_minus_failed_factorization = (c, b-a)
```

测试覆盖：

```text
test_sum_ab_same_orientation_denominator_factorization_exposes_shared_leg_offsets
```

---

## 9. 当前状态

可以安全说：

```text
sum=A+B same-orientation 分支新增了 N-P、N-Q 的可引用因式账本。
这个账本比普通 shared-leg 双勾股更强。
```

不能说：

```text
same-orientation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

下一步建议：

```text
把 both-pass 的因子对
(H1-P)(H1+P)=N^2
(H2-Q)(H2+Q)=N^2

和
N-P=a(d-c)
N-Q=c(b-a)

合并做 gcd / valuation 分配。
特别关注 q == 3 mod 4 的奇次赋值是否必须落入
a, c, d-c, b-a, 或 nu-mv 的某一侧。
```
