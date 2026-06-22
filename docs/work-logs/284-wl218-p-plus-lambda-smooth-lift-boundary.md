# wl284 — wl218 p+lambda smooth-lift boundary

日期：2026-06-22

## 1. 本轮目标

接 wl283。

wl283 澄清：

```text
p+lambda shadow 是 q-adic quartic shadow，
不能把 q | E 误当成 exact E=0。
```

本轮继续问一个更具体的问题：

```text
这个 q-adic shadow 会不会在 q^2 或 q^3 层，因为四平方条件自动死亡？
```

普通话说：

```text
如果模 q 看起来活着，但升到 q^2 后自己消失，
那 valuation 证明还有短路。
如果它能平滑升上去，就必须换全局打法。
```

结论：

```text
p+lambda quartic shadow 是 smooth lift。
单个 q-adic 平方条件不会杀掉它。
```

---

## 2. 局部对象

沿用 wl282-wl283：

```text
F =
 -t^2u^2 - 2t^2u + t^2
 -2tu^2 + 4tu + 2t
 +u^2 + 2u - 1

E =
 t^2u^2 + t^2u - t^2
 +tu^2 - t - u^2 - u + 1
```

在 `q == 15 mod16` 的 `p+lambda` shared shadow 上：

```text
F(t,u) = 0 mod q
E(t,u) = 0 mod q
```

对应的恢复平方值是：

```text
x^2 + 1 = X_num / D^2
y^2 + 1 = Y_num / D^2
```

其中 `D` 是 dual-slope 反构造分母。

---

## 3. 公共零点是光滑的

对 `F,E` 的 Jacobian：

```text
J = [[F_t, F_u],
     [E_t, E_u]]
```

在检查到的 `F=E=0 mod q` 点上：

```text
det(J) != 0 mod q.
```

例子：

```text
q=31:
  (t,u)=(2,21)  det(J)=9
  (t,u)=(2,28)  det(J)=19
  (t,u)=(15,21) det(J)=10
  (t,u)=(15,28) det(J)=28

q=47:
  (t,u)=(9,29)  det(J)=28
  (t,u)=(9,34)  det(J)=32

q=79:
  (t,u)=(4,48)  det(J)=36
  (t,u)=(4,51)  det(J)=21
```

因此每个 `mod q` 公共零点都有唯一 Hensel lift 到 `mod q^k`。

普通话说：

```text
这不是尖点或偶然交叉。
它是 p-adic 意义下的光滑点，所以会稳定往高阶升。
```

---

## 4. q^2 层平方条件仍然通过

枚举每个 `mod q` 根的所有一阶 lift：

```text
t = t0 + q A
u = u0 + q B
A,B in F_q
```

要求：

```text
F(t,u) = 0 mod q^2
E(t,u) = 0 mod q^2
```

得到：

```text
每个 mod q 根只有 1 个 mod q^2 lift。
```

并且这个唯一 lift 仍满足：

```text
x^2+1 是 mod q^2 的平方
y^2+1 是 mod q^2 的平方
```

统计：

```text
q=31:
  每个根 total q^2 choices = 961
  F=E mod q^2 lifts = 1
  square-preserving lifts = 1

q=47:
  每个根 total q^2 choices = 2209
  F=E mod q^2 lifts = 1
  square-preserving lifts = 1

q=79:
  每个根 total q^2 choices = 6241
  F=E mod q^2 lifts = 1
  square-preserving lifts = 1
```

普通话说：

```text
升到 q^2 后，没有大量自由度了；
但那条唯一的路没有死，而且仍然满足局部平方。
```

---

## 5. q^3 样例

以 `q=31` 的根：

```text
(t,u) = (2,21) mod 31
```

唯一 lift 到：

```text
mod 31^2:
  (t,u) = (188,362)

mod 31^3:
  (t,u) = (4993,5167)
```

并且在 `31^3` 上仍有：

```text
x^2+1 square
y^2+1 square
```

普通话说：

```text
这个影子不只是 q^2 假象；
至少在样例上，它继续稳定升到 q^3。
```

---

## 6. 对证明路线的影响

可以安全说：

```text
1. p+lambda quartic shadow 在 F,E 子系统里是 smooth q-adic branch；
2. q^2 层不会自动杀掉恢复平方条件；
3. q=31 的 q^3 样例也继续通过；
4. 单个 q 的局部平方条件不足以关闭 p+lambda shadow。
```

不能说：

```text
p+lambda shadow 已关闭。
高阶 lift 会自动死亡。
sum=A+B 已证明。
倒数定理已证明。
```

普通话说：

```text
如果要杀这条管道，不能继续等它自己在 q^k 层坏掉。
必须用全局平方类、多素数联动，或者真正的递降。
```

---

## 7. 下一步

下一版关键引理应改成：

```text
假设存在全局有理四平方点，并且某个 q==15 mod16 进入 p+lambda shadow。
由于 q-adic branch 本身能 lift，
必须从全局分子分母或其他素数的 squareclass 中找矛盾。
```

三个可试方向：

```text
1. 多素数路线：
   沿 q-adic branch 写出 Q(t) 的 q-adic 贴近，
   看 Q(t) 的有理分子是否必须带出另一枚 q'==3 or 11 mod16。

2. 递降路线：
   用 q-adic 贴近 E=0，把点投到 wl266 的 z-lemma/centerline pullback，
   证明高度下降或 q-adic 阶数上升。

3. norm 路线：
   把 Q(t)/t^2 = (t-1/t)^2 - 4(t-1/t) - 4
   看成 Q(sqrt(2)) 中的范数条件，
   用全局 norm/squareclass 排除有理四平方拼接。
```

---

## 8. 验证

Jacobian 和 lift 核验可复跑：

```bash
PYTHONPATH=src uv run python - <<'PY'
def F_t(t,u,q): return (-2*t*u*u -4*t*u +2*t -2*u*u +4*u +2)%q
def F_u(t,u,q): return (-2*t*t*u -2*t*t -4*t*u +4*t +2*u +2)%q
def E_t(t,u,q): return (2*t*u*u +2*t*u -2*t + u*u -1)%q
def E_u(t,u,q): return (2*t*t*u + t*t +2*t*u -2*u -1)%q

for q,t,u in ((31,2,21),(47,9,29),(79,4,48)):
    det=(F_t(t,u,q)*E_u(t,u,q)-F_u(t,u,q)*E_t(t,u,q))%q
    print(q, (t,u), det)
PY
```

当前输出：

```text
31 (2, 21) 9
47 (9, 29) 28
79 (4, 48) 36
```
