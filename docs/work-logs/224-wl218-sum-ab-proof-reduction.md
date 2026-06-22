# wl224 — wl218 `sum=A+B` proof reduction

日期：2026-06-22

## 1. 本轮目标

用户目标是倒数定理：

```text
lambda in Q_{>0}
R_lambda = { r in Q_{>0} : r^2+1 和 r^2+lambda^2 都是有理平方 }

若 r,s in R_lambda 且满足 full-plane closure，
则 rs = lambda。
```

这轮只推进第一条关系：

```text
sum=A+B:
r+s = lambda+1
```

普通话说：

```text
先看全平面四种闭合关系里的第一条线。
它不等于“只在正方形里”，只是全平面条件分解后的一个分支。
如果这条都关不严，后面 sum=|A-B| 和两个 diff 分支不能急着宣称全平面定理。
```

---

## 2. 先把命题换成真正保留四个平方的形式

设：

```text
x = r/lambda
y = s/lambda
```

因为：

```text
r in R_lambda
<=> r^2+1 是平方，且 (r/lambda)^2+1 是平方
```

所以 `r in R_lambda` 等价于：

```text
r 是勾股斜率
x = r/lambda 是勾股斜率
```

同理 `s in R_lambda` 等价于：

```text
s 是勾股斜率
y = s/lambda 是勾股斜率
```

`sum=A+B` closure 给：

```text
lambda*x + lambda*y = lambda + 1
lambda(x+y-1) = 1
lambda = 1/(x+y-1)
```

因此第一分支等价于：

```text
不存在正有理 x,y，使得

x+y > 1,
x 是勾股斜率,
y 是勾股斜率,
x/(x+y-1) 是勾股斜率,
y/(x+y-1) 是勾股斜率。
```

这是比 `p=rs` 更强的坐标，因为它没有把四个单项平方压成两个乘积平方。

普通话说：

```text
弱 p 模型只问“两双鞋的乘积是不是好看”。
四斜率模型直接问“四只鞋每只是不是合脚”。
```

---

## 3. `rs=lambda` 在这个坐标里的含义

在 `sum=A+B` 里：

```text
rs = lambda
```

等价于：

```text
lambda^2 xy = lambda
lambda xy = 1
```

而 closure 已经给：

```text
lambda(x+y-1)=1
```

所以：

```text
xy = x+y-1
(x-1)(y-1)=0
```

也就是说：

```text
rs=lambda  <=>  x=1 或 y=1。
```

但：

```text
1^2+1 = 2
```

不是有理平方，所以 `x=1` 或 `y=1` 不是勾股斜率。

因此在 `sum=A+B` 分支里，若能证明：

```text
r,s in R_lambda 且 r+s=lambda+1 => rs=lambda
```

就会进一步得到：

```text
sum=A+B 分支其实没有真闭合对。
```

这不是矛盾，而是这条分支的正确几何含义。

---

## 4. 用 Euclid 参数展开四斜率条件

每个勾股斜率可写成：

```text
odd orientation:  (m^2-n^2)/(2mn)
even orientation: (2mn)/(m^2-n^2)
```

取两个已经通过的斜率：

```text
x = a/b
r = c/d
```

其中 `x` 和 `r=lambda*x` 都是勾股斜率。

由 closure 反推出另外两个量：

```text
y = 1 - x + x/r = (bc - ac + ad)/(bc)
s = 1 - r + r/x = (ad - ac + bc)/(ad)
```

要四项全通过，还必须：

```text
y^2 + 1 是平方
s^2 + 1 是平方
```

这个模型已经在代码里对应：

```text
PythagoreanLegParam
sum_ab_three_pass_mobius_model_from_params
sum_ab_euclid_orientation_equations
```

普通话说：

```text
先选 x 和 r 两个已经合法的直角三角形斜率。
closure 会强行生成 y 和 s。
问题变成：这两个被生成出来的数还能不能也都是直角三角形斜率？
```

---

## 5. mixed orientation 已有可审查的局部证明

若 `x` 和 `r` 的 Euclid orientation 一奇一偶：

```text
odd/even
even/odd
```

则 mod 8 直接排除。

理由很短：

primitive Euclid 参数满足一奇一偶，所以：

```text
odd leg  是奇数
even leg 是 4 的倍数
```

在 `odd/even` 情况，`s` 的重构分子和分母都是奇数，因此：

```text
s numerator^2 + s denominator^2 ≡ 1+1 ≡ 2 (mod 8)
```

但平方剩余 mod 8 只有：

```text
0,1,4
```

所以 `s^2+1` 不可能是平方。

`even/odd` 对称地让 `y` 卡在：

```text
2 (mod 8)
```

结论：

```text
mixed orientation 不可能给出四项全通过。
```

这个结论来自 wl139，可作为 `sum=A+B` 证明的正式局部引理。

---

## 6. same orientation 化成共享腿双勾股问题

剩下的是：

```text
odd/odd
even/even
```

这时两个重构项共享同一个分子。

令：

```text
N = bc - ac + ad = ad - ac + bc
P = bc
Q = ad
```

则需要同时：

```text
N^2 + P^2 = H1^2
N^2 + Q^2 = H2^2
```

普通话说：

```text
同一条腿 N，要同时和 P、Q 拼出两个直角三角形。
```

这本身不矛盾；普通共享腿双勾股很常见。真正的约束是：

```text
P = bc
Q = ad
```

它们不是随便两条腿，而是来自同两组 Euclid 参数的交叉乘。

---

## 7. same orientation 的关键因式

对 odd/odd：

```text
a = m^2-n^2
b = 2mn
c = u^2-v^2
d = 2uv
```

有：

```text
P-Q =  2(mu+nv)(nu-mv)
P+Q =  2(mu-nv)(mv+nu)
```

对 even/even：

```text
P-Q = -2(mu+nv)(nu-mv)
P+Q =  2(mu-nv)(mv+nu)
```

所以：

```text
P=Q => nu-mv=0。
```

primitive 情况下，`nu=mv` 会把两组 Euclid 参数压成同一比例；这正是退化/镜像方向。

因此 same orientation 的核心未闭合引理应是：

```text
若 N^2+P^2 和 N^2+Q^2 都是平方，
且 P=bc, Q=ad 来自同 orientation 的 primitive Euclid 参数，
则必须 P=Q。
```

一旦能证明这个引理，`sum=A+B` 分支就会压到：

```text
P=Q
```

更精确地说，`P=Q` 不是立刻等于 `rs=lambda`。在 primitive positive
same-orientation 情况下，`P=Q` 先给 `(u,v)=(m,n)`，所以 `r=x`，再由
`lambda=1/(x+y-1)` 和 `r=lambda*x` 得到 `lambda=1`、`y=2-x`。

因此 `P=Q` 分支落到：

```text
lambda=1
x+y=2
x,y 都是勾股斜率
```

这正是 `R_1` 的 `sum=A+B` 中线写法，已由 wl202 / wl226 的 Yang Ji
中线定理排除。

所以 same-orientation 后续真正要打的是：

```text
P != Q
```

也就是：

```text
nu-mv != 0
```

一旦能证明 both-pass 强制 `P=Q`，第一分支会被中线定理关闭；它不需要再
额外产生一个真实 reciprocal closure pair。

---

## 8. 对用户提出的 valuation 路线的评价

用户建议用：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

并在各个 `q ≡ 3 (mod 4)` 的 valuation 上逼矛盾。

这条路线仍可继续，但本轮看到一个重要限制：

```text
只盯 q ≡ 3 (mod 4) 可能太窄。
```

原因是已有四斜率假候选的失败 squareclass 不总是单个 `3 mod 4` 素数障碍。例如：

```text
x=3/4, y=4/3:
lambda=12/13
r=9/13   失败 squareclass = 10 = 2*5
s=16/13  失败 squareclass = 17
```

这里 `17 ≡ 1 (mod 4)`，而 `10` 包含 `2` 和 `5`。

普通话说：

```text
障碍不只藏在 3 mod 4 的素数里。
如果只拿这一把钥匙，可能开不完门。
```

更稳的升级是：

```text
1. 用完整 squareclass / Hilbert-symbol 语言描述四单项平方；
2. 或者走 same-orientation shared-leg 递降，证明 P != Q 会产生更小解。
```

---

## 9. 当前状态

可以安全说：

```text
sum=A+B 已经被严格化成四斜率模型。
mixed orientation 可用 mod 8 排除。
same orientation 已化成带交叉乘结构的共享腿双勾股问题。
```

不能说：

```text
sum=A+B 分支已证明。
倒数定理已证明。
valuation 路线已经闭合。
```

当前真正剩余的数学硬点是：

```text
same orientation both-pass => P=Q
```

配合已关闭的中线分支，这会关闭 `sum=A+B`。等价的非退化目标是：

```text
nu-mv != 0 时，从 P±Q 的因子和双勾股参数中推出矛盾或递降。
```

---

## 10. 下一步

建议下一轮只做一个引理：

```text
Same-orientation descent lemma.

Assume primitive Euclid data (m,n),(u,v) with matching orientation.
Let x=a/b, r=c/d, and reconstruct y,s by sum=A+B.
If y and s are both Pythagorean leg ratios, prove P=Q.
```

可先从整数因式开始：

```text
N^2+P^2 = H1^2
N^2+Q^2 = H2^2
```

参数化为：

```text
P = G1(U1^2 - V1^2),  N = 2G1 U1 V1
Q = G2(U2^2 - V2^2),  N = 2G2 U2 V2
```

然后把 `P=bc`、`Q=ad`、`P-Q=±2(mu+nv)(nu-mv)` 代入，寻找：

```text
nu-mv != 0 => 更小的 same-orientation both-pass
```

如果递降失败，就记录具体卡在哪个 gcd 分配上；那会告诉我们需要的不是初等递降，而是更强的局部符号或曲线工具。

---

## 11. 当前验证入口

相关代码与测试：

```text
src/rational_distance/concordant/rational_ratio.py
tests/test_rational_ratio.py
```

重点 helper：

```text
sum_ab_euclid_orientation_equations
sum_ab_same_orientation_shared_leg_terms
sum_ab_same_orientation_denominator_factorization
sum_ab_same_orientation_cross_gcd_terms
sum_ab_same_orientation_normalized_near_miss_summary
```

建议验证：

```bash
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```
