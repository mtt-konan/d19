# wl245 — wl218 Layer 4 and mod 3 both-pass boundary

日期：2026-06-22

## 1. 本轮目标

接 wl244。

wl244 推到第三层：

```text
K = k^2
P = KQ 作为 y 二次式有有理根
```

但这还不够，因为解出来的 `y` 还必须满足：

```text
y^2 + 1 是有理平方。
```

普通话说：

```text
上一轮已经能摸到 y。
这一轮检查：摸到的 y 是否真的是合法勾股斜率。
```

---

## 2. Layer 4 消元结果

把：

```text
x = (1-a^2)/(2a)
y = (1-b^2)/(2b)
K = k^2
```

代入：

```text
P = k^2 Q
```

得到一个关于 `b` 的四次方程。

它不是随机四次式。关于 `b` 的判别式分解为：

```text
a^4 (a^2+1)^2
* F_-(a,k)^2
* F_+(a,k)^2
* R(a,k^2)
```

其中 `F_-,F_+` 正是 wl244 的 Layer-3 两个因子，`R(a,k^2)` 正是 wl242 的剩余 quartic 层。

普通话说：

```text
把 y 的真勾股条件放回去以后，代数没有变成一行矛盾。
它把 wl242 的 R 层和 wl244 的 D_y 层重新扣在一起。
```

所以这一轮不能说：

```text
Layer 4 已关闭。
sum=A+B 已证明。
```

可以说：

```text
Layer 4 的消元没有发现新的简单因子；继续换变量会回到原问题的自相似 quartic。
```

---

## 3. same-orientation 模 3 入口

换回 same-orientation 共享腿模型：

```text
N^2 + P^2 是平方
N^2 + Q^2 是平方
P = bc
Q = ad
N = bc - ac + ad
```

本轮发现一个很短的模 3 约束：

```text
same-orientation both-pass => P ≡ Q (mod 3).
```

普通话说：

```text
如果两个共享腿三角形都想在模 3 里过关，
那么 P 和 Q 至少在 mod 3 这一层必须相等。
```

手算理由如下。

在 `F_3` 中，primitive Euclid 腿余数只能是：

```text
(±1,0) 或 (0,±1).
```

因为 `m^2,n^2` 只可能是 `0,1`。

而在 `F_3` 中平方类是：

```text
0,1.
```

所以：

```text
N^2+P^2 是平方
```

排除 `N` 与 `P` 同时非零，因为那时：

```text
N^2+P^2 = 1+1 = 2
```

不是平方。

因此：

```text
N=0 或 P=0.
```

同理：

```text
N=0 或 Q=0.
```

分情况：

```text
1. N=0，则 both-pass 同时允许，但由同 orientation 的 residue 结构推出 P=Q；
2. N!=0，则必须 P=0 且 Q=0，也有 P=Q。
```

有限 residue helper 验证了这个结论：

```text
sum_ab_same_orientation_both_pass_residue_summary(3)

noncenter_survivor_count_by_orientation = {odd: 0, even: 0}
p_equals_q_count_by_orientation         = {odd: 32, even: 32}
```

---

## 4. 这个模 3 结果还不是 3-adic 证明

模 3 无非中线幸存，但模 9 立刻有：

```text
sum_ab_same_orientation_both_pass_residue_summary(9)

noncenter_survivor_count_by_orientation = {odd: 1728, even: 1728}
```

例子：

```text
odd:  (m,n,u,v,N,P,Q) = (0,1,1,3,4,0,3)
even: (m,n,u,v,N,P,Q) = (0,1,1,3,3,3,0)
```

普通话说：

```text
mod 3 第一层会强迫 P≡Q。
但 mod 9 允许 P 和 Q 只差一个 3 的倍数。
所以不能把 mod 3 结论直接升级成完整矛盾。
```

类似地：

```text
mod 4 无非中线幸存；
mod 8 有幸存。
```

这说明当前更像一个估值/递降入口：

```text
both-pass + P!=Q
=> 3 | (P-Q)
```

但还需要证明更强的提升，例如：

```text
3^e | (P-Q) 迫使更高的 3-adic 约束，
或能构造更小的 same-orientation both-pass。
```

---

## 5. 代码入口

新增 helper：

```text
sum_ab_same_orientation_both_pass_residue_summary(modulus)
```

它枚举模 `M` 的 same-orientation primitive residue 类，并统计：

```text
P≡Q 的类数量；
P不等于Q 但两个平方条件都过关的幸存类数量；
少量幸存例子。
```

新增测试：

```text
test_sum_ab_same_orientation_both_pass_residue_summary_tracks_mod3_boundary
```

测试刻意同时锁住：

```text
mod 3: 非中线幸存为 0；
mod 9: 非中线幸存非 0。
```

普通话说：

```text
这个测试防止后续把“mod 3 第一层约束”误写成“3-adic 已证明”。
```

---

## 6. 对用户原 valuation 路线的更新

用户原思路是看 `p ≡ 3 mod 4` 的赋值。

现在更准确的说法是：

```text
3 mod 4 素数不会直接出现在 z^2+1 的 squareclass 中，
但在 same-orientation both-pass 的共享腿结构里，p=3 的 residue 第一层确实有强约束。
```

所以后续可以尝试证明：

```text
P != Q
=> 3 | (P-Q)
=> 3 | 2(mu+nv)(nu-mv)
```

再结合：

```text
P-Q = ±2(mu+nv)(nu-mv)
P+Q = 2(mu-nv)(mv+nu)
N-P = a(d-c)
N-Q = c(b-a)
```

做 gcd / valuation 分配。

下一步最具体目标：

```text
把 mod 3 的 P≡Q 提升成对 nu-mv 或 mu+nv 的 3-adic 控制，
看是否能推出递降或 primitive 矛盾。
```

---

## 7. 本轮边界

可以安全说：

```text
1. Layer 4 消元没有直接关闭分支；
2. same-orientation both-pass 有严格的 mod 3 第一层约束；
3. mod 9 仍有非中线 residue 幸存，因此还不是完整证明。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
mod 3 已经给出完整矛盾。
```
