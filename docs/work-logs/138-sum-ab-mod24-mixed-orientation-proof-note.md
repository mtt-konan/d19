# wl138 — `sum=A+B` mod 24 mixed-orientation proof note

日期：2026-06-09

## 1. 本轮问题

wl137 发现条件版 residue summary 在 `mod 24` 下给出强信号：

```text
odd/even: both_square_classes = 0
even/odd: both_square_classes = 0
```

这轮把它从“程序计数”整理成可审查的 proof note。

普通话说：

```text
看看 mixed orientation 到底是不是能用 mod 24 直接打掉。
```

结论先说清楚：

```text
在分母均非 0 mod 24 的条件子域里，mixed orientation 会被 mod 24 排除。
但这还没有覆盖所有真实 primitive Euclid 参数，因为真实分母可能是 0 mod 24。
```

---

## 2. 基本方程

`sum=A+B` 三通过模型里：

```text
x = a/b
r = c/d
```

重构：

```text
y = (bc - ac + ad) / bc
s = (ad - ac + bc) / ad
```

对应平方检查：

```text
(bc - ac + ad)^2 + (bc)^2 是否为平方
(ad - ac + bc)^2 + (ad)^2 是否为平方
```

在 `mod 24` 下，整数平方剩余只有：

```text
{0, 1, 4, 9, 12, 16}
```

所以如果某个平方和落到：

```text
10 或 17 mod 24
```

它一定不是平方。

---

## 3. 条件版 residue 子域

wl137 的 conditional helper 保留以下 residue class：

```text
gcd(m,n,24)=1
gcd(u,v,24)=1
m-n 为奇数
u-v 为奇数
选中的 slope denominator 非 0 mod 24
选中的 scaled-term denominator 非 0 mod 24
bc 非 0 mod 24
ad 非 0 mod 24
```

这些条件的意思是：

```text
参数看起来像 primitive Euclid 参数，
而且当前模 24 里相关分母没有退化成 0。
```

---

## 4. mixed orientation 的 `mod 24` 结果

在这个条件子域内，枚举得到一个更强的事实。

对：

```text
odd/even
```

所有合法 residue class 都满足：

```text
other_square_sum ≡ 17 mod 24
failed_square_sum ≡ 10 mod 24
```

对：

```text
even/odd
```

所有合法 residue class 都满足：

```text
other_square_sum ≡ 10 mod 24
failed_square_sum ≡ 17 mod 24
```

因为：

```text
10, 17 ∉ {0, 1, 4, 9, 12, 16}
```

所以在这个条件子域里：

```text
mixed orientation 不可能让 other 和 failed 任一项通过平方检查。
```

普通话说：

```text
只要 mixed orientation 的分母在 mod 24 里没有掉到 0，
那两条重构出来的平方方程都会直接卡在非平方余数上。
```

这解释了 wl137 的计数：

```text
odd/even:
  total=16384
  other=0
  failed=0
  both=0

even/odd:
  total=16384
  other=0
  failed=0
  both=0
```

---

## 5. 重要缺口：分母为 0 mod 24

这份 proof note 不能直接声称关闭所有 mixed orientation。

原因是：

```text
真实 primitive Euclid 参数可能让某些分母 ≡ 0 mod 24。
```

例子：

```text
m=12, n=1
gcd(12,1)=1
m-n=11 是奇数
even leg = 2mn = 24 ≡ 0 mod 24
```

所以：

```text
(m,n) 是真实 primitive Euclid 参数，
但 odd orientation 的 denominator 2mn 在 mod 24 下为 0。
```

conditional helper 会跳过这类 residue class。

普通话说：

```text
mod 24 已经打掉了一大块 mixed orientation，
但还有一批“分母刚好被 24 整除”的真实参数没有被这个论证覆盖。
```

---

## 6. 有限观察，不当证明

做过一个小范围真实参数观察：

```text
2 <= m,u <= 30
primitive parity 条件
positive reconstructed y,s
mixed orientation
```

结果：

```text
conditional 保留类里没有 both 通过。
denominator-zero 跳过类里也没有看到 both 通过。
```

但这只是有限观察。

不能写成：

```text
denominator-zero 子域也已证明失败。
```

---

## 7. 能说什么，不能说什么

可以说：

```text
mod 24 在分母非零子域里严格排除 mixed orientation。
mixed orientation 的主要剩余缺口是 denominator-zero 子域。
```

不能说：

```text
mixed orientation 已经全关。
sum=A+B 分支已关。
条件版 residue helper 覆盖了所有真实 primitive 参数。
```

---

## 8. 下一步

下一步不要继续盲扫大模数。

更有希望的是单独处理 denominator-zero 子域：

```text
1. 分类 mixed orientation 中哪些分母会是 0 mod 24：
   slope denominator
   scaled-term denominator
   bc
   ad

2. 对这些子域改用更低阶的模数或 2-adic valuation：
   例如 v2(2mn), v2(m^2-n^2)

3. 如果 denominator-zero 子域也能排除，
   mixed orientation 才能升级为真正 proof note。
```

普通话说：

```text
现在 mixed orientation 已经被打到一个角落里了：
不是普通余数类，而是分母被 24 整除的特殊类。
下一步就专门打这个角落。
```
