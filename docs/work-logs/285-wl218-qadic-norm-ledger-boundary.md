# wl285 — wl218 q-adic norm ledger boundary

日期：2026-06-22

## 1. 本轮目标

接 wl284。

wl284 说明：

```text
p+lambda quartic shadow 是 smooth q-adic branch；
单个 q-adic 平方条件不会让它在 q^2/q^3 层自动死亡。
```

本轮尝试把这条 q-adic branch 接到全局 norm / squareclass 语言。

普通话说：

```text
既然局部不会自己死，就问：
它是不是会强迫某个全局范数或平方类带出坏素数？
```

结论是：

```text
Q(t) 确实是 Q(sqrt(2)) 的范数；
q-adic branch 也等价于 Q(t),Q(u) 的高阶可除；
但四平方条件没有直接逼 Q(t) 成为有理平方。
```

所以 norm 路线有入口，但还不是一行证明。

---

## 2. Q(t) 的 norm 形式

wl282 的 quartic 是：

```text
Q(t) = t^4 - 4t^3 - 6t^2 + 4t + 1.
```

在 `K = Q(sqrt(2))` 中：

```text
Q(t)
= Norm_K/Q(t^2 + (-2+2sqrt(2))t - 1).
```

等价地，令：

```text
z = t - 1/t,
```

则：

```text
Q(t)/t^2
= z^2 - 4z - 4
= Norm_K/Q(z - 2 + 2sqrt(2)).
```

普通话说：

```text
p+lambda shadow 的门锁确实是二次域 Q(sqrt(2)) 的范数。
```

---

## 3. F,E 直接控制 Q(t),Q(u)

沿用：

```text
F =
 -t^2u^2 - 2t^2u + t^2
 -2tu^2 + 4tu + 2t
 +u^2 + 2u - 1

E =
 t^2u^2 + t^2u - t^2
 +tu^2 - t - u^2 - u + 1
```

Groebner reduction 给出：

```text
Q(t) in ideal(F,E)
Q(u) in ideal(F,E)
```

更具体地：

```text
Q(t) = E + (...)F      （在所用 lex basis 下商为 [0,1]）
```

所以如果有：

```text
q^k | F(t,u)
q^k | E(t,u),
```

那么：

```text
q^k | Q(t)
q^k | Q(u)
```

实际 lift 样例也显示：

```text
q=31:
  k=1: v_q(Q(t))=v_q(Q(u))=1
  k=2: v_q(Q(t))=v_q(Q(u))=2
  k=3: v_q(Q(t))=v_q(Q(u))=3
  k=4: v_q(Q(t))=v_q(Q(u))=4
```

同样模式在 `q=47,79` 的样例中成立。

普通话说：

```text
这条 shadow 可以用 Q(t) 的全局分子来追踪。
如果它贴近 q^k，那么 Q(t) 也带着 q^k。
```

---

## 4. 四平方条件没有直接让 Q(t) 成平方

把恢复平方分子记为：

```text
x^2+1 = X_num / D^2
y^2+1 = Y_num / D^2
```

在 exact `E=0` 上做消元：

```text
Res_u(E, X_num)
  = (t-1)^4 (t+1)^4 (t^2+1)^4

Res_u(E, Y_num)
  = (t-1)^4 (t+1)^4
    (5t^4 + 8t^3 - 6t^2 - 8t + 5)^2
```

第二条就是 wl266 的新曲线 / z-lemma / centerline 入口。

但注意：

```text
gcd(Q(t), Res_u(E, X_num)) = 1
gcd(Q(t), Res_u(E, Y_num)) = 1
```

普通话说：

```text
恢复平方条件确实和 E=0 有联系，
但它没有直接把 wl282 的 Q(t) 变成有理平方。
```

这意味着：

```text
Q(t) 是 norm
```

还不能立刻推出：

```text
Q(t) 是 square
```

也不能立刻推出：

```text
存在 q' == 3 or 11 mod16 的矛盾素数。
```

---

## 5. 小型全局探针

构造贴近 `q=31` 的 `mod 31^2` 分支的有理点：

```text
(t,u) == (188,362) mod 31^2
```

并取小分母样本，恢复平方类出现大素数，例如：

```text
t=61/77, u=5/77:
  v_31(Q(t)) = 2
  v_31(Q(u)) = 2
  squareclass(x^2+1) = 545050311562
  squareclass(y^2+1) = 211590847301

t=20/41, u=5/77:
  v_31(Q(t)) = 2
  v_31(Q(u)) = 2
  squareclass(x^2+1) = 2872183895401
  squareclass(y^2+1) = 294988273826
```

这个探针只是线索，不是证明。
它说明：

```text
贴近 q-adic branch 的全局有理点确实会产生复杂 squareclass；
但没有立刻显现简单的 q' == 3 or 11 mod16 universal obstruction。
```

普通话说：

```text
坏素数会出现，但不是一眼就按 mod16 分类排队出现。
```

---

## 6. 对证明路线的影响

可以安全说：

```text
1. p+lambda shadow 有 Q(sqrt(2)) norm 表达；
2. q-adic F=E 贴近会强迫 Q(t),Q(u) 同阶可除；
3. 这给全局 squareclass 账本一个可追踪量；
4. 但四平方条件没有直接让 Q(t) 成有理平方；
5. norm 路线仍需更强的全局理想/平方类分配。
```

不能说：

```text
norm 路线已关闭 p+lambda shadow。
Q(t) 必须是 square。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步不应再只查单个 `q` 的 Hensel lift。
更合理的是建立一个全局账本：

```text
For a true global four-square point:

1. factor Q(t), Q(u), X_num, Y_num;
2. record primes in Q(t),Q(u) with odd valuation;
3. compare them with squareclasses of X_num/D^2 and Y_num/D^2;
4. test whether every q==15 mod16 p+lambda shadow forces another odd
   obstruction prime outside the allowed squareclasses.
```

普通话说：

```text
现在要从“一个素数会不会死”换成“所有素数的平方类账本能不能同时平衡”。
```

---

## 8. 验证

可复跑的 norm 核验：

```bash
PYTHONPATH=src uv run python - <<'PY'
import sympy as sp

t,s=sp.symbols("t s")
Q=t**4-4*t**3-6*t**2+4*t+1
A=t**2 + (-2+2*s)*t - 1
B=t**2 + (-2-2*s)*t - 1
G=sp.groebner([s**2-2],s,t,order="lex")
print(sp.factor(G.reduce(A*B-Q)[1]))
PY
```

输出：

```text
0
```

消元核验使用的 `X_num,Y_num` 是 wl284 中 `x^2+1,y^2+1`
的分子展开；完整展开较长，本轮实际用 sympy 脚本直接定义后运行：

```bash
PYTHONPATH=src uv run python - <<'PY'
import sympy as sp

t,u=sp.symbols("t u")
E=t**2*u**2 + t**2*u - t**2 + t*u**2 - t - u**2 - u + 1
# Xn, Yn are the expanded numerators of x^2+1 and y^2+1 from wl284.

print(sp.factor(sp.resultant(E,Xn,u)))
print(sp.factor(sp.resultant(E,Yn,u)))
PY
```

输出：

```text
(t - 1)**4*(t + 1)**4*(t**2 + 1)**4
(t - 1)**4*(t + 1)**4*(5*t**4 + 8*t**3 - 6*t**2 - 8*t + 5)**2
```
