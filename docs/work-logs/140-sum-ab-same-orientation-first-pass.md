# wl140 — `sum=A+B` same-orientation first pass

日期：2026-06-09

## 1. 本轮问题

wl139 已经关闭 mixed orientation：

```text
odd/even
even/odd
```

剩下：

```text
odd/odd
even/even
```

这轮先看 same orientation 是否也能被简单模数打掉。

普通话说：

```text
四个方向已经关掉两个。
现在看剩下两个是不是也能靠小模数直接卡死。
```

---

## 2. 小模数初筛

扫过：

```text
3,5,7,8,9,11,13,16,17,24,32,40
```

条件：

```text
primitive parity residue
same orientation
```

观察：

```text
mod 8 / mod 16 / mod 32 对 same orientation 基本不卡。

odd/odd:
  mod 8 下 other 和 failed 都 ≡ 1

even/even:
  mod 8 下 other 和 failed 都 ≡ 0
```

`mod 24`、`mod 40` 有一部分失败类，但仍有大量：

```text
both_square_residue classes
```

所以：

```text
same orientation 不能像 mixed orientation 那样被一个简单 mod 8 lemma 关掉。
```

---

## 3. 关键代数结构

令：

```text
x = a/b
r = c/d
```

重构：

```text
y = (bc - ac + ad) / bc
s = (ad - ac + bc) / ad
```

注意：

```text
other numerator = bc - ac + ad
failed numerator = ad - ac + bc
```

其实是同一个数：

```text
N = bc - ac + ad = ad - ac + bc
```

也就是说：

```text
other = N / (bc)
failed = N / (ad)
```

平方检查变成：

```text
N^2 + (bc)^2 是否为平方
N^2 + (ad)^2 是否为平方
```

普通话说：

```text
same orientation 不是两个完全不同的失败项。
它们共享同一个分子 N，只是分母不同。
```

这比模表更重要。

---

## 4. odd/odd 展开

odd orientation：

```text
a = m^2 - n^2
b = 2mn
c = u^2 - v^2
d = 2uv
```

同分子：

```text
N =
-m^2u^2 + 2m^2uv + m^2v^2
+2mnu^2 - 2mnv^2
+n^2u^2 - 2n^2uv - n^2v^2
```

两个分母：

```text
P = bc = 2mn(u^2-v^2)
Q = ad = 2uv(m^2-n^2)
```

需要同时：

```text
N^2 + P^2 = square
N^2 + Q^2 = square
```

---

## 5. even/even 展开

even orientation：

```text
a = 2mn
b = m^2 - n^2
c = 2uv
d = u^2 - v^2
```

同分子：

```text
N = 2(
  m^2uv
  + mnu^2
  - 2mnuv
  - mnv^2
  - n^2uv
)
```

两个分母：

```text
P = bc = 2uv(m^2-n^2)
Q = ad = 2mn(u^2-v^2)
```

也需要同时：

```text
N^2 + P^2 = square
N^2 + Q^2 = square
```

---

## 6. 两个平方候选的差

记：

```text
O = N^2 + P^2
F = N^2 + Q^2
```

则：

```text
O - F = P^2 - Q^2
      = (bc)^2 - (ad)^2
      = (bc-ad)(bc+ad)
```

代入 odd/odd：

```text
O-F = 4(mu-nv)(mu+nv)(-mv+nu)(mv+nu)
```

代入 even/even：

```text
O-F = -4(mu-nv)(mu+nv)(-mv+nu)(mv+nu)
```

普通话说：

```text
如果 O 和 F 都是平方，
那就是两个平方相差一个高度可分解的数。
这看起来更像“平方差/递降”问题，而不是普通模筛问题。
```

---

## 7. 有限真实参数观察

小范围扫过：

```text
2 <= m,u < 40
primitive parity
positive reconstructed terms
```

结果：

```text
odd/odd:
  other_pass = 10
  failed_pass = 10
  both = 0

even/even:
  other_pass = 16
  failed_pass = 16
  both = 0
```

这符合 near-miss 现象：

```text
会出现三通过；
但没有看到四通过。
```

但这只是有限观察，不是证明。

---

## 8. 当前判断

same orientation 的下一步不应继续盲扫小模数。

更有希望的是：

```text
1. 参数化共享腿 N 的两个勾股三角形：
   N^2 + P^2 = H1^2
   N^2 + Q^2 = H2^2

2. 利用 P=bc、Q=ad 的特殊结构。

3. 研究平方差：
   H1^2 - H2^2 = P^2 - Q^2
```

普通话说：

```text
剩下的 same orientation 不是“余数一眼死”。
它像是两个勾股三角形共享同一条腿，
而另外两条腿又被 Euclid 参数强绑定。
```

---

## 9. 能说什么，不能说什么

可以说：

```text
sum=A+B 的 mixed orientation 已关闭。
same orientation 已化成共享分子 N 的双平方问题。
```

不能说：

```text
same orientation 已关闭。
sum=A+B 分支已关闭。
有限扫到 both=0 就是证明。
```

---

## 10. 下一步

建议下一步：

```text
1. 新增一个 lemma note：
   same orientation = shared-leg double-Pythagorean problem。

2. 把 N^2+P^2 和 N^2+Q^2 同时为平方参数化。

3. 优先看是否能推出 P=Q 或某个递降结构。
```

如果最后能证明：

```text
P=Q
```

那在几何上可能对应镜像/退化分支，正好接回主理论目标里的：

```text
s = lambda / r
```
