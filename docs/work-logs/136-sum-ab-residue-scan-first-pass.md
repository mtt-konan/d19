# wl136 — `sum=A+B` residue scan first pass

日期：2026-06-09

## 1. 本轮问题

wl135 新增了：

```text
sum_ab_euclid_residue_summaries(modulus=M)
```

这轮实际扫一批小模数，看看是否能出现强信号：

```text
other 方程像平方，
但 failed 方程在模 M 下被强制不像平方。
```

普通话说：

```text
如果第三条边已经通过，第四条边是不是会被某个小模数直接卡死？
```

---

## 2. 扫描命令

使用当前 helper，保守枚举：

```text
m,n,u,v mod M
```

不加：

```text
m > n
u > v
gcd
primitive parity
分母非零
```

运行过的单模数：

```text
3, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 29, 31
```

运行过的小组合模数：

```text
15, 21, 24, 35, 40
```

---

## 3. 单模数结果概括

奇素数模数基本高度对称。

例如：

```text
M=3,5,7,11,13,17,19,23,29,31
```

四种 orientation 的计数相同，且都有大量：

```text
both_square_classes > 0
other_only_classes > 0
failed_only_classes > 0
```

普通话说：

```text
单个奇素数模数太弱。
它既不能推出 failed 必过，也不能推出 failed 必死。
```

2 的幂有结构：

```text
M=8:
  odd/odd 和 even/even 完全不卡。
  odd/even: other 总像平方，failed 有 1024 类不像平方。
  even/odd: failed 总像平方，other 有 1024 类不像平方。

M=16:
  mixed orientation 仍有方向性。
  但 odd/odd 和 even/even 不再完全不卡，也仍然不能关闭。
```

普通话说：

```text
2-adic 方向值得看，但单靠 mod 8 或 mod 16 还不够。
```

---

## 4. 小组合模数结果概括

试过：

```text
M=15,21,24,35,40
```

结果仍然都有大量：

```text
both_square_classes
```

没有看到：

```text
other_square_classes > 0
both_square_classes = 0
```

也没有看到：

```text
other_only_classes = 0
```

能真正关掉 failed 的情形。

普通话说：

```text
把几个小模数乘起来，还是没有直接把第四条边卡死。
条件太松时，余数世界里总有很多“看起来都可能”的类。
```

---

## 5. 一个工程观察

朴素扫描复杂度是：

```text
M^4
```

尝试直接扫到：

```text
56,88,104,120
```

会明显变慢，不适合继续交互式盲扫。

后续如果要做组合模数，应先优化：

```text
1. 预计算 (m,n) -> leg terms residue。
2. 按 leg term pair 压缩计数。
3. 再组合 slope_terms 和 scaled_term_terms。
```

---

## 6. 当前判断

单纯 residue-only helper 太保守。

这不是坏事：

```text
它告诉我们“裸模筛”不够强。
```

下一步更值得做的是条件版 residue summary：

```text
sum_ab_euclid_primitive_residue_summaries(...)
```

至少加上：

```text
gcd(m,n,M)=1 的 residue analogue
gcd(u,v,M)=1 的 residue analogue
m-n odd 的 parity analogue
u-v odd 的 parity analogue
denominator terms 非零 mod M
```

但必须注意：

```text
条件版 helper 不能替代 wl135 的 conservative helper。
名字和文档必须写清楚它筛掉了哪些 residue class。
```

---

## 7. 能说什么，不能说什么

可以说：

```text
裸平方剩余扫描没有发现能直接关闭 failed 的小模数。
2 的幂模数显示 mixed orientation 有方向性。
后续应加入 primitive/parity/denominator 条件，或转向因式分解和递降。
```

不能说：

```text
模筛路线失败。
sum=A+B 分支关闭。
near-miss 没有模解释。
```

---

## 8. 下一步

推荐下一步：

```text
1. 新增条件版 residue summary，先只支持小 M。
2. 对 M=8,16,24,40 比较 conservative vs conditional。
3. 如果 conditional 仍有大量 both，就转向符号因式分解。
```

普通话说：

```text
现在不是“模筛没用”，而是“裸模筛太粗”。
要么把 Euclid primitive 条件加进去，
要么别再扫，改看方程本身怎么分解。
```
