# wl283 — wl218 p+lambda exact-vs-adic boundary

日期：2026-06-22

## 1. 本轮目标

接 wl282。

wl282 把 `p+lambda` shared shadow 接到 dual-slope 参数：

```text
p+lambda shadow
=> F(t,u) = 0 mod q
=> shared 时还要 lambda^2-1 = 0 mod q
=> 在 q == 3 mod 4 下落到 F(t,u)=E(t,u)=0 mod q
```

本轮澄清一个容易误用的点：

```text
F=E=0 作为有理等式
```

和

```text
q | F, q | E 作为局部贴近
```

不是同一件事。

普通话说：

```text
如果真的等于 E=0，我们已经知道它会回到中线。
但 p+lambda shadow 只说“模某个 q 看起来像 E=0”，
不能直接当成“全球就在 E=0 上”。
```

---

## 2. exact F=E=0 的结构

沿用 wl282 的两个多项式：

```text
F =
 -t^2u^2 - 2t^2u + t^2
 -2tu^2 + 4tu + 2t
 +u^2 + 2u - 1

E =
 t^2u^2 + t^2u - t^2
 +tu^2 - t - u^2 - u + 1
```

消元给：

```text
Res_u(F,E) = -(t^4 - 4t^3 - 6t^2 + 4t + 1)^2
Res_t(F,E) = -(u^4 - 4u^3 - 6u^2 + 4u + 1)^2
```

Groebner 形式也显示公共零点是 0 维的：

```text
Q(t) = t^4 - 4t^3 - 6t^2 + 4t + 1 = 0
u^2 + (t^3 - 4t^2 - 5t)u - 1 = 0
```

其中：

```text
Q(t)/t^2 = (t - 1/t)^2 - 4(t - 1/t) - 4.
```

所以 exact `F=E=0` 会强迫：

```text
t - 1/t = 2 +/- 2sqrt(2).
```

普通话说：

```text
精确公共交点不是一条有理曲线；
它本身就带 sqrt(2)。
```

---

## 3. exact E=0 已经不是新出口

这要和 wl266 接起来。

wl266 处理的是 exact：

```text
E(t,u) = 0
```

把 `E` 看成 `u` 的二次式，它的判别式为：

```text
5t^4 + 8t^3 - 6t^2 - 8t + 5
```

所以有理 `u` 存在时，必须有：

```text
5t^4 + 8t^3 - 6t^2 - 8t + 5 = square.
```

令：

```text
z = t - 1/t
```

则：

```text
(5t^4 + 8t^3 - 6t^2 - 8t + 5)/t^2
= 5z^2 + 8z + 4.
```

同时：

```text
z^2 + 4 = (t + 1/t)^2.
```

于是 exact `E=0` 落到 wl241 的 z 引理：

```text
z^2 + 4          square
5z^2 + 8z + 4   square.
```

wl241 又把 z 引理归约到 centerline quartic/Yang Ji。

因此：

```text
exact E=0
=> z lemma
=> centerline/Yang Ji.
```

普通话说：

```text
如果候选点真的站在 E=0 这条线上，
那它不是新敌人；它会被送回中线问题。
```

---

## 4. 但 p-adic E=0 还没关闭

`p+lambda shadow` 在 shared odd prime 处只给：

```text
q | F(t,u)
q | E(t,u)
```

它不是：

```text
F(t,u)=0 in Q
E(t,u)=0 in Q.
```

有限域核验显示，对所有检查到的 `q == 15 mod 16`：

```text
Q(t)=0 mod q      有 4 个 t 根
F=E=0 mod q       有 8 个 (t,u) 点
```

例子：

```text
q=31:
  Q roots = 2,15,21,28
  F=E pairs =
    (2,21), (2,28), (15,21), (15,28),
    (21,2), (21,15), (28,2), (28,15)

q=47:
  Q roots = 9,26,29,34
  F=E pairs =
    (9,29), (9,34), (26,29), (26,34),
    (29,9), (29,26), (34,9), (34,26)
```

这些点映到：

```text
r,s = 1 +/- sqrt(2) mod q.
```

普通话说：

```text
模 q 时，E=0 的影子真实存在；
所以不能用“E=0 已归约到中线”一句话杀掉 p+lambda shadow。
真正要证明的是：这种模 q 的贴近不能由一个全局四平方有理点产生。
```

---

## 5. 对关键引理的更新

原始 valuation 路线想证明：

```text
shared odd compensation impossible.
```

现在必须改成更精确的分支：

```text
q == 3 or 11 mod16:
  shared odd compensation 直接死；

q == 7 mod16:
  只剩 p-lambda shadow；

q == 15 mod16:
  p-lambda shadow 仍需处理；
  p+lambda shadow 等价于贴近 F=E=0 quartic shadow。
```

其中 `p+lambda` 的下一版目标不是 exact `E=0`，而是：

```text
若某个 q == 15 mod16 同时整除 F 和 E，
且 x^2+1、y^2+1、a^2+1、b^2+1 都是 Q 中的平方，
则必须产生：

1. 另一枚 q' == 3 or 11 mod16 的奇赋值矛盾；或
2. 更高阶贴近 E=0 / centerline 的递降；或
3. 直接落到 exact E=0，从而回到 centerline/Yang Ji。
```

普通话说：

```text
下一步不是再找 F=E=0 的公式；
公式已经有了。
下一步是证明“只能局部像它，不能全局拼成真点”。
```

---

## 6. 当前状态

可以安全说：

```text
1. exact E=0 出口已由 wl266 归约到 centerline/Yang Ji；
2. p+lambda shared shadow 是 q-adic quartic shadow，不是 exact E=0；
3. q==15 mod16 的局部点已经被精确定位为 F=E=0 mod q；
4. sum=A+B 仍未证明。
```

不能说：

```text
p+lambda shadow 已被 E=0 归约关闭。
shared odd compensation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 验证

符号核验：

```bash
PYTHONPATH=src uv run python - <<'PY'
import sympy as sp

t,u=sp.symbols("t u")
F=-t**2*u**2 - 2*t**2*u + t**2 - 2*t*u**2 + 4*t*u + 2*t + u**2 + 2*u - 1
E=t**2*u**2 + t**2*u - t**2 + t*u**2 - t - u**2 - u + 1
Q=t**4 - 4*t**3 - 6*t**2 + 4*t + 1

print(sp.factor(sp.resultant(F,E,u)))
print(sp.factor(sp.resultant(F,E,t)))
print(sp.expand(Q/t**2 - ((t-1/t)**2 - 4*(t-1/t) - 4)))
PY
```

输出：

```text
-(t**4 - 4*t**3 - 6*t**2 + 4*t + 1)**2
-(u**4 - 4*u**3 - 6*u**2 + 4*u + 1)**2
0
```

局部核验：

```bash
PYTHONPATH=src uv run python - <<'PY'
from sympy import primerange

def F(t,u,q): return (-t*t*u*u -2*t*t*u + t*t -2*t*u*u +4*t*u +2*t +u*u +2*u -1)%q
def E(t,u,q): return (t*t*u*u + t*t*u - t*t + t*u*u - t - u*u - u + 1)%q
def Q(t,q): return (t**4-4*t**3-6*t*t+4*t+1)%q

for q in primerange(3,100):
    if q%4 != 3:
        continue
    roots=[t for t in range(1,q) if Q(t,q)==0]
    pairs=[(t,u) for t in roots for u in roots if F(t,u,q)==0 and E(t,u,q)==0]
    if roots:
        print(q, q%16, roots, pairs)
PY
```

输出：

```text
31 15 [2, 15, 21, 28] [(2, 21), (2, 28), ...]
47 15 [9, 26, 29, 34] [(9, 29), (9, 34), ...]
79 15 [4, 48, 51, 59] [(4, 48), (4, 51), ...]
```
