# wl252 — wl218 one-mod-four Gaussian absorption

日期：2026-06-22

## 1. 本轮目标

接 wl251。

wl251 的结论是：

```text
已知 product-layer residual 的共同坏 squareclass 是 29，
而 29 ≡ 1 (mod 4)。
```

这说明只看 `q ≡ 3 mod 4` 的赋值，还不能解释这个假点。

本轮改问：

```text
如果共同坏 squareclass 的素因子全是 1 mod 4，
它是否能被二平方 / Gaussian norm 吸收到新的勾股斜率里？
```

普通话说：

```text
3 mod 4 看不见 29。
那就换个角度：29 是 5^2+2^2，
能不能把这个坏因子当成一个高斯整数因子除掉？
```

---

## 2. 新 helper

新增：

```text
squareclass_two_square_absorption(ratio, squareclass)
```

它做三件事：

```text
1. 找 squareclass = a^2+b^2 的整数分解；
2. 用 Gaussian division 的两个共轭符号吸收 squareclass；
3. 检查吸收后的新 ratio 是否满足 z^2+1 是平方。
```

当前规范：

```text
two_square_decomposition = (a,b), with a >= b
```

两个吸收分支写成：

```text
z_plus  = (a*r + b) / (a - b*r)
z_minus = (a*r - b) / (a + b*r)
```

普通话说：

```text
如果 r^2+1 = d * square，
而 d=a^2+b^2，
那么用 a+bi 去除 r+i，
有机会把 d 这个坏 squareclass 从 norm 里除掉。
```

---

## 3. guard 假点

旧 guard：

```text
r = 14/23
s = 26/7
d = 29 = 5^2 + 2^2
```

对 `r=14/23`：

```text
z_plus  = (5r+2)/(5-2r) = 4/3
z_minus = (5r-2)/(5+2r) = 24/143
```

并且：

```text
(4/3)^2 + 1     = 25/9       = (5/3)^2
(24/143)^2 + 1  = 21025/20449 = (145/143)^2
```

对 `s=26/7`：

```text
z_minus = (5s-2)/(5+2s) = 4/3
z_plus  = (5s+2)/(5-2s) = -144/17
```

其中 `4/3` 同样是真勾股斜率。

普通话说：

```text
29 并不是一个随机坏因子。
它可以被 5+2i 吸收掉，
吸收以后原来的假成员值变成真正的勾股斜率。
```

---

## 4. 对证明路线的影响

这不是证明 `sum=A+B`。

它给 only-1-mod-4 情形一个更具体的下一步：

```text
如果共同坏 squareclass d 的素因子全是 1 mod 4，
则 d 是二平方；
用 Gaussian factor 吸收 d 后，
弱成员斜率可能转成真勾股斜率。
```

这提示下一条引理不应直接写成：

```text
only-1-mod-4 情形不可能。
```

而更可能是：

```text
only-1-mod-4 情形可以被重新参数化；
重新参数化后应落回已知 squareclass-ratio / centerline / reciprocal shadow 结构。
```

普通话说：

```text
1 mod 4 坏因子不是一堵墙，
更像一个可以除掉的高斯因子。
证明要做的是：
除掉以后，闭合关系会变成什么？
```

---

## 5. 代码与测试

新增 dataclass：

```text
SquareclassTwoSquareAbsorption
```

新增 helper：

```text
squareclass_two_square_absorption(...)
```

新增测试：

```text
test_one_mod_four_squareclass_absorption_turns_guard_roots_into_leg_slopes
```

测试锁住：

```text
29 = 5^2 + 2^2
r=14/23 吸收到 4/3 和 24/143
s=26/7 的一个分支也吸收到 4/3
吸收后的正分支满足 z^2+1 是平方
```

---

## 6. 下一步

下一步应研究吸收变换如何作用在整个 `sum=A+B` 闭合关系上。

具体问题：

```text
r,s 共享同一个 only-1-mod-4 squareclass d；
分别选择 Gaussian absorption 分支后得到 x,y；
那么 x,y 是否满足已有的 squareclass-ratio 模型？
是否必然落到 centerline 或 reciprocal shadow？
```

普通话说：

```text
我们已经会把单个坏斜率修成好斜率。
还没证明的是：
两个斜率一起修以后，原来的闭合关系会不会强迫它们回到已知无解结构。
```

---

## 7. 当前边界

可以安全说：

```text
1. only-1-mod-4 squareclass 可通过二平方结构做 Gaussian absorption；
2. guard 假点的 d=29 确实能被吸收到真勾股斜率；
3. 这给 only-1-mod-4 分支一个重新参数化入口。
```

不能说：

```text
only-1-mod-4 分支已排除。
sum=A+B 已证明。
倒数定理已证明。
```
