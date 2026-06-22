# wl229 — wl218 `P=Q` branch is centerline, not an automatic reciprocal proof

日期：2026-06-22

## 1. 本轮修正

在 `sum=A+B` same-orientation 分支里，旧笔记把目标说成：

```text
both-pass => P=Q
```

然后很快接到：

```text
rs=lambda
```

这一步需要补严。

普通话说：

```text
P=Q 当然是强退化。
但它不是自动把我们送到一个合法倒数对；
它先把问题送到 lambda=1 的中线分支。
中线分支已经由 Yang Ji 关掉。
```

---

## 2. `P=Q` 的精确含义

same orientation 里：

```text
P = bc
Q = ad
```

已有因式：

```text
P-Q = +/- 2(mu+nv)(nu-mv)
```

正参数下：

```text
mu+nv > 0
```

所以：

```text
P=Q <=> nu-mv=0
```

也就是：

```text
nu = mv
```

若两组 Euclid 参数 primitive：

```text
gcd(m,n)=gcd(u,v)=1
```

则：

```text
nu=mv => (u,v)=(m,n)
```

因此同向腿相同：

```text
c=a
d=b
```

所以：

```text
r = c/d = a/b = x
```

---

## 3. 回到四斜率模型

`sum=A+B` 四斜率模型是：

```text
x = r/lambda
y = s/lambda
lambda = 1/(x+y-1)
```

如果 `r=x`，则：

```text
r = lambda*x = x
```

因为 `x>0`，得到：

```text
lambda = 1
```

再代回：

```text
lambda = 1/(x+y-1)
```

得到：

```text
x+y = 2
```

并且四项通过条件变成：

```text
x 是勾股斜率
y 是勾股斜率
r=x
s=y
```

普通话说：

```text
P=Q 不是产生一个新闭合点。
它说 lambda=1，而且两个纵向比例加起来正好是 2。
这就是正方形中线。
```

---

## 4. 几何翻译

当：

```text
lambda = 1
r+s = lambda+1 = 2
```

在 d19 的比例写法中：

```text
A = B
N1 + N2 = 2B
```

这就是 vertical centerline：

```text
A=B
```

或按轴交换看，就是 wl202 / center-line proof note 里的中线分支。

Yang Ji Theorem 2 + Remark 1 已经排除全平面中线上的四有理距离点。

所以：

```text
P=Q 分支关闭，依据是 centerline theorem。
```

而不是：

```text
P=Q 分支自动给出一个真实 reciprocal closure pair。
```

---

## 5. 本地 quartic 复核

在纯 `R_lambda` 语言里，`lambda=1`、`r+s=2` 可写成：

```text
y = 2-x
x^2+1 是平方
y^2+1 是平方
```

若用参数：

```text
x = (1-t^2)/(2t)
```

则第二个平方条件落到 wl226 同一个 centerline quartic：

```text
Y^2 = t^4 + 8t^3 + 18t^2 - 8t + 1
```

当前 PARI 诊断：

```text
rank 0
torsion order 4
original quartic small rational points only degenerate
proof_status = needs-birational-pullback
```

因此本地代数仍是复核入口；正式关闭仍引用 Yang Ji 中线定理。

---

## 6. 对 same-orientation 主线的影响

现在 `sum=A+B` 的 same-orientation 分支应分成两块：

```text
1. P=Q:
   primitive => (u,v)=(m,n) => lambda=1, x+y=2
   => centerline
   => Yang Ji 关闭。

2. P!=Q:
   等价于 nu-mv != 0。
   这是唯一仍需证明的非退化 both-pass 分支。
```

普通话说：

```text
以后不要再把 P=Q 当成“还需要证明 reciprocal 的分支”。
它已经被中线定理吃掉。
真正没打完的是 P 不等于 Q。
```

---

## 7. 小扫描

作为 sanity check，扫描 primitive 勾股斜率池：

```text
x+y=2
x,y 都是勾股斜率
```

到 `max_m=1000` 未发现样本：

```text
max_m=100:  0
max_m=500:  0
max_m=1000: 0
```

这不是证明，只是和中线定理一致。

---

## 8. 当前状态

可以安全说：

```text
same-orientation 的 P=Q 分支已归约到 centerline，并由 Yang Ji 关闭。
```

不能说：

```text
same-orientation 已全部关闭。
sum=A+B 已证明。
倒数定理已证明。
```

剩余核心仍是：

```text
P!=Q 且 both-pass
```

也就是：

```text
nu-mv != 0
```

下一步应继续把 wl228 的：

```text
N-P=a(d-c)
N-Q=c(b-a)
```

和 both-pass 因子对：

```text
(H1-P)(H1+P)=N^2
(H2-Q)(H2+Q)=N^2
```

合并做 valuation / gcd 分配。
