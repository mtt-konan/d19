# wl247 — wl218 difference-factor valuation split

日期：2026-06-22

## 1. 本轮目标

接 wl246。

wl246 说明：

```text
3 | (P-Q)
```

不能单独升级成 3-adic 矛盾。

本轮继续问更细的问题：

```text
P-Q = ±2(mu+nv)(nu-mv)
```

里，这个 `3` 是否总落在同一个因子上？

普通话说：

```text
如果 3 永远落在 nu-mv，可能能做递降；
如果 3 永远落在 mu+nv，也可能有另一条固定路线。
这一轮检查它到底有没有固定归属。
```

---

## 2. 结果

结果是：

```text
没有固定归属。
```

在模 27 的 same-orientation 非中线 both-pass residue 中，odd/even 都出现完全相同的四类分布：

```text
(v3(mu+nv), v3(nu-mv), v3(P-Q))

(0,1,1): 46656
(0,2,2): 15552
(1,0,1): 46656
(2,0,2): 15552
```

普通话说：

```text
3 可以落在 mu+nv；
也可以落在 nu-mv。
可以只落一层；也可以落两层。
所以“3 必在某个固定因子上”不是定理。
```

---

## 3. 例子

odd orientation：

```text
(0,1,1): (m,n,u,v,N,P,Q,mu+nv,nu-mv)
         = (0,1,3,1,2,0,21,1,3)

(1,0,1): (m,n,u,v,N,P,Q,mu+nv,nu-mv)
         = (0,1,1,3,13,0,21,3,1)
```

even orientation：

```text
(0,1,1): (m,n,u,v,N,P,Q,mu+nv,nu-mv)
         = (1,1,1,4,8,0,24,5,-3)

(1,0,1): (m,n,u,v,N,P,Q,mu+nv,nu-mv)
         = (1,1,1,2,13,0,21,3,-1)
```

这些例子都只是 residue/local points，不是真整数反例。

普通话说：

```text
它们的作用是告诉我们：
不能写“因为 3 整除 P-Q，所以 3 必整除 nu-mv”这种证明。
局部世界里两边都能发生。
```

---

## 4. 代码入口

新增 helper：

```text
sum_ab_same_orientation_difference_factor_valuation_summary(
    modulus=27,
    orientation="odd" / "even",
    prime=3,
)
```

它统计非中线 both-pass residue 类中：

```text
(v_p(mu+nv), v_p(nu-mv), v_p(P-Q))
```

的分布，并给每类一个例子。

新增测试：

```text
test_sum_ab_same_orientation_difference_factor_valuation_summary_splits_branches
```

测试锁住：

```text
mod 27 下 odd/even 都有四类分支；
3 不会被强制落在单一因子。
```

---

## 5. 对证明路线的影响

现在可以排除一个过于乐观的路线：

```text
both-pass => 3 | P-Q
P-Q = ±2(mu+nv)(nu-mv)
=> 3 必整除 nu-mv
=> 递降 / P=Q
```

这条推理在局部 residue 层已经失败。

后续如果继续走 valuation，必须同时使用更多条件：

```text
N-P = a(d-c)
N-Q = c(b-a)
P+Q = 2(mu-nv)(mv+nu)
primitive gcd constraints
positivity / ordering constraints
```

普通话说：

```text
3 的确在 P-Q 里出现，
但它可以从两扇不同的小门进来。
要关大门，必须同时看整栋结构，而不是只盯一个因子。
```

---

## 6. 当前边界

可以安全说：

```text
1. mod 3 both-pass 约束是真的；
2. 3-adic lift 塔存在；
3. 3 在 P-Q 的两个主因子上都可能出现；
4. 单因子 valuation 引理不够。
```

不能说：

```text
sum=A+B 已证明。
3-adic valuation 路线已关闭分支。
3 必须落在 nu-mv 或 mu+nv 的某一固定侧。
```

---

## 7. 下一步

下一步应改成“多因子联动”而不是“单因子归属”：

```text
同时统计 / 分析
v3(mu+nv), v3(nu-mv),
v3(mu-nv), v3(mv+nu),
v3(N-P), v3(N-Q),
以及 gcd(a,c), gcd(b,d).
```

寻找是否存在强一点的组合规则，例如：

```text
3 落在 P-Q 的某一侧时，
P+Q 或 N-P/N-Q 必须出现不兼容的估值分配。
```

普通话说：

```text
单独追 P-Q 已经不够。
下一步要看 P-Q、P+Q、N-P、N-Q 四张账同时怎么平衡。
```
