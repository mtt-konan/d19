# wl282 — wl218 p+lambda shadow quartic boundary

日期：2026-06-22

## 1. 本轮目标

接 wl281。

wl281 显示：

```text
q == 15 mod 16 时，p+lambda shadow 在 q^2、q^3 层稳定存在。
```

本轮把这条局部管道接回 dual-slope 参数，弄清它到底落在哪个
代数门槛上。

普通话说：

```text
坏消息不是“到处都有坏点”。
坏点其实被钉在一条很窄的 quartic 门上；
只是这扇门在某些模素数世界里会打开。
```

---

## 2. dual-slope 参数

沿用 wl259-wl260：

```text
a = (1-t^2)/(2t)
b = (1-u^2)/(2u)
D = a+b-ab
x = b/D
y = a/D
lambda = 1/(x+y-1)
r = lambda*x
s = lambda*y
p = rs
```

化简得到：

```text
r = -2t / ((t-1)(t+1))
s = -2u / ((u-1)(u+1))
p = 4tu / ((t-1)(t+1)(u-1)(u+1))
```

并且：

```text
p-lambda numerator =
  (t^2 + 2t - 1)(u^2 + 2u - 1)
```

而危险的 `p+lambda` 分子是：

```text
F(t,u) =
 -t^2u^2 - 2t^2u + t^2
 -2tu^2 + 4tu + 2t
 +u^2 + 2u - 1
```

---

## 3. 单看 F=0 不能杀管道

把 `F` 当作 `u` 的二次式：

```text
disc_u(F) = 8(t^2+1)^2
```

所以精确等式 `F=0` 的通解含有 `sqrt(2)`：

```text
u =
(-t^2 + 2t +/- sqrt(2)(t^2+1) + 1)
/
(t^2 + 2t - 1)
```

普通话说：

```text
在 Q 里，这不是一条有理参数线。
但在 mod q 里，如果 sqrt(2) 存在，它就可能有根。
```

单看 `F=0` 只解释了为什么有 `sqrt(2)` 入口；再加上成员平方剩余
和 shared 条件后，才得到 wl280-wl281 的更窄现象：

```text
q == 7 mod16:
  p+lambda shadow 没出现；

q == 15 mod16:
  p+lambda shadow 出现并能 lift。
```

注意：这只说明 `p+lambda` 的局部门槛，不能说明全局有理解存在。

---

## 4. shared 条件还要 lambda^2=1

shared odd compensation 同时要求：

```text
lambda^2 - 1 == 0 mod q
p^2 - lambda^2 == 0 mod q
```

在 dual-slope 参数里：

```text
lambda^2-1 numerator =
  4(t+u)(tu-1)E(t,u)
```

其中：

```text
E(t,u) =
 t^2u^2 + t^2u - t^2
 +tu^2 - t - u^2 - u + 1
```

现在同时看 `p+lambda shadow`：

```text
F(t,u) == 0
lambda^2-1 == 0
```

在 `q == 3 mod 4` 下，前两条 obvious tube 不能承载 `F=0`：

```text
F(t,-t)   = -(t^2+1)^2
F(t,1/t) =  (t^2+1)^2 / t^2
```

因为 `t^2+1 == 0 mod q` 不可能。

所以 `p+lambda` shared 管道必须落到：

```text
F(t,u) = 0
E(t,u) = 0
```

普通话说：

```text
它不是贴着 t+u=0 或 tu=1 那两条 trivial tube 走。
真正剩下的是 F 和 E 的交点。
```

---

## 5. 交点给出 quartic

消去 `u`：

```text
resultant_u(F,E) =
  -(t^4 - 4t^3 - 6t^2 + 4t + 1)^2
```

记：

```text
Q(t) = t^4 - 4t^3 - 6t^2 + 4t + 1
```

它有更透明的写法：

```text
Q(t)/t^2 =
  (t - 1/t)^2 - 4(t - 1/t) - 4
```

令：

```text
z = t - 1/t
```

则：

```text
z^2 - 4z - 4 = 0
z = 2 +/- 2sqrt(2)
```

普通话说：

```text
这个 quartic 的门锁就是 sqrt(2)。
在有理数里门不开；
在某些有限域里 sqrt(2) 出现，门就会开。
```

另外：

```text
disc(Q) = 2^17
```

这也解释了为什么这里没有新的奇素数判别式，只有 2-adic / 16 次剩余现象。

---

## 6. 小素数局部核验

对 `q == 3 mod 4` 的小素数：

```text
q=31  mod16=15  Q roots = 2,15,21,28
q=47  mod16=15  Q roots = 9,26,29,34
q=79  mod16=15  Q roots = 4,48,51,59
q=127 mod16=15  Q roots = 11,22,23,75
q=191 mod16=15  Q roots = 7,109,126,144
```

而 `q == 3,7,11 mod16` 的 `q == 3 mod4` 小素数没有这种 `Q` 根。

进一步把 `F=E=0` 的点映回：

```text
r = -2t / ((t-1)(t+1))
s = -2u / ((u-1)(u+1))
```

得到正是 wl280 的 `p+lambda` 根：

```text
q=31:
  (r,s) = (9,24), (24,9)

q=47:
  (r,s) = (8,41), (41,8)

q=79:
  (r,s) = (10,71), (71,10)
```

这些就是：

```text
r,s = 1 +/- sqrt(2)  mod q
```

普通话说：

```text
wl280 的有限域根，不是孤立枚举现象；
它们就是 dual-slope quartic Q(t)=0 的影子。
```

---

## 7. 对证明路线的影响

可以安全说：

```text
1. p+lambda shared shadow 在 dual-slope 参数中被 F=E=0 控制；
2. F=E=0 消元到 quartic Q(t)=0；
3. Q(t) 等价于 z^2-4z-4=0, z=t-1/t；
4. 这解释了 q==15 mod16 的局部幸存；
5. p+lambda shadow 不是 trivial tube，而是 quartic shadow。
```

不能说：

```text
p+lambda shadow 已关闭。
shared odd compensation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

普通话说：

```text
我们现在知道坏管道在哪里，
但还没有证明真正的有理四平方点不能沿这条管道拼起来。
```

---

## 8. 下一步

下一步应把 `Q(t)=0 mod q` 的局部影子升级成全局 squareclass / descent 约束。

两个自然方向：

```text
A. squareclass route:
   假设某个 q==15 mod16 进入 p+lambda shadow。
   用 Q(t)=0 给出的 z=t-1/t 条件，追踪 x^2+1、y^2+1
   在 Q 中必须全为平方时会不会引入另一枚 q'==3 or 11 mod16。

B. descent route:
   用 z=t-1/t 与 u 的对应式，把一个非中心真解变换成更小参数。
   若能保持四个勾股斜率条件，就得到无限递降。
```

可复跑的核心符号核验：

```bash
PYTHONPATH=src uv run python - <<'PY'
import sympy as sp

t,u=sp.symbols("t u")
F=-t**2*u**2 - 2*t**2*u + t**2 - 2*t*u**2 + 4*t*u + 2*t + u**2 + 2*u - 1
E=t**2*u**2 + t**2*u - t**2 + t*u**2 - t - u**2 - u + 1
Q=t**4 - 4*t**3 - 6*t**2 + 4*t + 1

print(sp.factor(sp.discriminant(F,u)))
print(sp.factor(sp.resultant(F,E,u)))
print(sp.expand(Q/t**2 - ((t-1/t)**2 - 4*(t-1/t) - 4)))
PY
```

当前输出：

```text
8*(t**2 + 1)**2
-(t**4 - 4*t**3 - 6*t**2 + 4*t + 1)**2
0
```
