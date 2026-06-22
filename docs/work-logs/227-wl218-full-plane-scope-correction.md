# wl227 — wl218 full-plane scope correction

日期：2026-06-22

## 1. 本轮修正

用户修正要求：

```text
可以在全平面，不一定是只在正方形里。
```

这是当前 wl218 的控制口径：

```text
sum=A+B 只作为第一分支先攻；
最终倒数定理必须覆盖全平面四种闭合关系。
```

普通话说：

```text
我们要证明的不是“正方形内部的一条线”。
我们要证明的是：只要在全平面里满足任何一种闭合线性关系，
并且 r,s 都是真 R_lambda 成员，就必须是倒数对 rs=lambda。
```

---

## 2. 精确命题

仍然固定：

```text
lambda in Q_{>0}
R_lambda = { r in Q_{>0} : r^2+1 和 r^2+lambda^2 都是有理平方 }
```

全平面闭合条件是：

```text
{r+s, |r-s|} intersect {lambda+1, |lambda-1|} nonempty
```

也就是四个分支：

```text
1. r+s   = lambda+1
2. r+s   = |lambda-1|
3. |r-s| = lambda+1
4. |r-s| = |lambda-1|
```

目标定理是：

```text
r,s in R_lambda
并且满足上述任一分支
=> rs=lambda
```

当 `lambda=1` 时，`|lambda-1|=0`，正有理的 sum/diff 分支需要单独判掉零目标。

---

## 3. 对当前 proof queue 的影响

`sum=A+B`：

```text
r+s=lambda+1
```

仍然可以作为第一分支继续攻，因为它已有最多局部结构：

```text
四斜率模型
mixed orientation 的 mod 8 排除
centerline 的 Yang Ji 排除
same orientation 的 P,Q 共享腿框架
```

但它只能证明：

```text
Branch 1 closed
```

不能写成：

```text
full-plane reciprocal theorem proved
```

普通话说：

```text
先打第一扇门可以。
但整栋房子有四扇门，第一扇开了不等于全部开了。
```

---

## 4. 当前第一分支状态

第一分支已经严格化成：

```text
x = r/lambda
y = s/lambda
lambda = 1/(x+y-1)

x, y, lambda*x, lambda*y 都是勾股斜率
```

其中：

```text
rs=lambda <=> (x-1)(y-1)=0
```

因为 `1^2+1=2` 不是有理平方，若第一分支真能推出 `rs=lambda`，它实际上会进一步推出：

```text
r+s=lambda+1 分支没有正有理真闭合对。
```

这不是全平面结论；它只是第一分支的结论。

当前未闭合硬点仍是 same orientation：

```text
N^2+P^2 = H1^2
N^2+Q^2 = H2^2

P=bc
Q=ad
P-Q = +/- 2(mu+nv)(nu-mv)
```

需要证明：

```text
both-pass => P=Q
```

或在 `P!=Q` / `nu-mv!=0` 时做出矛盾或递降。

---

## 5. 后续证明顺序

推荐继续顺序：

```text
1. 关闭 r+s=lambda+1 的 same-orientation 非退化分支。
2. 把 product identity 用统一 T, epsilon 形式迁移到另外三支。
3. 对每支重新检查判别式符号、正性、centerline/zero-target 特例。
4. 只有四支都关闭后，才标记 wl218 倒数定理完成。
```

统一账本仍可用：

```text
T = closure target
p = rs
epsilon = -1 for sum relations
epsilon = +1 for diff relations

A_p = p^2 + epsilon*2p + T^2 + 1
B_p = p^2 + epsilon*2lambda^2*p + lambda^2*T^2 + lambda^4

B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

但要继续保留真成员条件：

```text
r^2+1          square
s^2+1          square
r^2+lambda^2   square
s^2+lambda^2   square
```

不能只用 `A_p,B_p` 平方代替。

---

## 6. 不能再误写的说法

不能说：

```text
sum=A+B 是正方形内问题，所以全平面可以先不管。
sum=A+B 证完就等于倒数定理证完。
A_p,B_p 平方就是 R_lambda 真成员。
有限扫描没有 true-nonreciprocal，所以定理成立。
```

可以说：

```text
sum=A+B 是全平面四分支之一。
当前先攻它，是因为已有最多代数结构。
最终定理必须覆盖四个全平面闭合关系。
```
