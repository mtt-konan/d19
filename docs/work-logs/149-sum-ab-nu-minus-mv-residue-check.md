# wl149 — `sum=A+B` nu-minus-mv residue check

日期：2026-06-09

## 1. 本轮问题

wl148 说明：

```text
P=Q  <=>  nu-mv=0
```

并且 primitive positive 情况下会退回：

```text
(u,v)=(m,n)
```

这轮检查一个自然希望：

```text
same orientation 里，
如果 other 和 failed 在模 M 下都像平方，
是否会强迫 nu-mv ≡ 0 mod M？
```

普通话说：

```text
能不能靠小模数直接把 both-pass 压到 P=Q？
```

---

## 2. 扫描方式

扫过：

```text
M = 3,5,7,8,9,11,13,16,17,24,32,40
```

检查：

```text
primitive parity residue
same orientation
other square sum 是平方剩余
failed square sum 是平方剩余
nu-mv 是否为 0
```

后来又加了更严格条件：

```text
m,n,u,v 非 0 mod M
a,b,c,d 非 0 mod M
P=bc 非 0 mod M
Q=ad 非 0 mod M
```

目的是避免很多明显退化 residue class。

---

## 3. 结果

无论普通 residue 还是更严格 residue：

```text
both-square residue class 并不强迫 nu-mv ≡ 0。
```

即使在严格条件下，也有大量：

```text
both-square
nu-mv != 0
```

例如 `M=8` 严格条件下：

```text
odd/odd:
  both = 256
  nu=0 = 64
  nu!=0 = 192

even/even:
  both = 256
  nu=0 = 64
  nu!=0 = 192
```

`M=24` 严格条件下：

```text
odd/odd:
  both = 8192
  nu=0 = 1024
  nu!=0 = 7168

even/even:
  both = 8192
  nu=0 = 1024
  nu!=0 = 7168
```

普通话说：

```text
小模数看不出“both-pass 必须 P=Q”。
余数世界允许很多 nu-mv 非零的假影。
```

---

## 4. 当前判断

这条路线没有给出强模障碍：

```text
both-square residues => nu-mv=0
```

不成立。

所以后续不要继续盲扫：

```text
更多单模数
更大模数
```

除非有新的结构条件加入。

普通话说：

```text
模筛不能直接帮我们把非退化分支压成 P=Q。
要换成整除/递降。
```

---

## 5. 能说什么，不能说什么

可以说：

```text
小模数 residue 检查没有发现 both-pass 强迫 nu-mv=0。
非退化分支不能靠当前裸模筛关闭。
```

不能说：

```text
非退化分支存在。
same orientation 有反例。
模方法彻底失败。
```

这只是说明：

```text
当前这组 residue 条件太弱。
```

---

## 6. 下一步

更合理的下一步：

```text
1. 使用 both-pass 的两套 (g,r,s) 参数。
2. 做整除关系：
   N = g1 r1 s1 = g2 r2 s2
   P-Q = ±2(mu+nv)(nu-mv)
3. 尝试构造递降：
   如果 nu-mv != 0，生成更小的 same-orientation both-pass。
```

普通话说：

```text
现在剩下的不是“余数卡死”型问题，
而是“如果有非退化解，能不能变出更小解”的问题。
```
