# wl139 — `sum=A+B` mixed-orientation mod 8 proof

日期：2026-06-09

## 1. 本轮问题

wl138 把 mixed orientation 推到一个缺口：

```text
mod 24 可以排除分母非零子域，
但分母为 0 mod 24 的真实 primitive 参数还没覆盖。
```

这轮继续看 denominator-zero 子域，结果发现更简单的事实：

```text
mixed orientation 不需要 mod 24。
直接用 mod 8 就能排除。
```

普通话说：

```text
之前绕了一圈看 24，其实 8 就够了。
```

---

## 2. Euclid primitive parity 的基本余数

对 primitive Euclid 参数：

```text
gcd(m,n)=1
m-n 为奇数
```

必有：

```text
m,n 一奇一偶
```

所以：

```text
odd leg  = m^2 - n^2 是奇数
even leg = 2mn 是 4 的倍数
```

在 `mod 8` 下：

```text
odd leg  ∈ {1,3,5,7}
even leg ∈ {0,4}
```

平方剩余为：

```text
{0,1,4}
```

因此：

```text
2 mod 8 一定不是平方。
```

---

## 3. `odd/even` orientation

令：

```text
x = a/b  使用 odd orientation
r = c/d  使用 even orientation
```

则在 `mod 8` 下：

```text
a 为奇数
b ∈ {0,4}
c ∈ {0,4}
d 为奇数
```

重构方程：

```text
other numerator = bc - ac + ad
other denominator = bc

failed numerator = ad - ac + bc
failed denominator = ad
```

因为：

```text
bc ≡ 0 mod 8
ac ≡ 0 或 4 mod 8
ad 为奇数
```

所以：

```text
other numerator 为奇数
other denominator ≡ 0 mod 8
```

于是：

```text
other square sum ≡ 1 mod 8
```

这项在 `mod 8` 下不矛盾。

但：

```text
failed numerator = ad - ac + bc
```

其中：

```text
ad 为奇数
ac, bc 为 0 或 4 mod 8
```

所以 `failed numerator` 也是奇数。

同时：

```text
failed denominator = ad
```

也是奇数。

因此：

```text
failed square sum ≡ 1 + 1 ≡ 2 mod 8
```

而 `2` 不是平方剩余。

结论：

```text
odd/even mixed orientation 不可能让 failed 项通过平方检查。
```

---

## 4. `even/odd` orientation

对称地，令：

```text
x = a/b  使用 even orientation
r = c/d  使用 odd orientation
```

则：

```text
a ∈ {0,4}
b 为奇数
c 为奇数
d ∈ {0,4}
```

这次：

```text
other denominator = bc
```

是奇数。

并且：

```text
other numerator = bc - ac + ad
```

也是奇数。

所以：

```text
other square sum ≡ 1 + 1 ≡ 2 mod 8
```

不是平方。

结论：

```text
even/odd mixed orientation 不可能让 other 项通过平方检查。
```

---

## 5. 程序 sanity check

用 residue 枚举复核：

```text
mod 8 square residues = {0,1,4}

odd/even:
  other_square_sum ≡ 1 mod 8
  failed_square_sum ≡ 2 mod 8

even/odd:
  other_square_sum ≡ 2 mod 8
  failed_square_sum ≡ 1 mod 8
```

这与上面的手推一致。

---

## 6. 能关闭什么

可以关闭：

```text
sum=A+B 三通过 Euclid equationization 中的 mixed orientation：
odd/even
even/odd
```

普通话说：

```text
如果一条已知勾股斜率取 odd leg / even leg，
另一条已知勾股斜率取 even leg / odd leg，
那重构出来的两项里必有一项卡在 2 mod 8，
所以不可能四项都通过。
```

---

## 7. 不能关闭什么

还不能关闭：

```text
odd/odd
even/even
整个 sum=A+B 分支
整个 full-plane closure
```

原因：

```text
mod 8 对 same orientation 不给同样矛盾。
```

下一步应集中看：

```text
odd/odd 和 even/even。
```

---

## 8. 和 wl138 的关系

wl138 的 `mod 24` note 仍然有价值，因为它暴露了 mixed orientation 的结构。

但本轮更新后的判断是：

```text
mod 24 不是必要工具。
mixed orientation 可以更干净地用 mod 8 关闭。
```

普通话说：

```text
wl138 是绕远路发现门在哪；
wl139 是发现门其实没锁，用 mod 8 就开了。
```

---

## 9. 下一步

建议下一步：

```text
1. 把 mixed orientation closed 作为 sum=A+B equationization 的正式 lemma。
2. 对 odd/odd、even/even 分别展开同 orientation 方程。
3. 优先检查 same orientation 是否有因式分解或递降结构。
```

尤其要避免：

```text
把 mixed orientation closed 误写成 sum=A+B closed。
```
