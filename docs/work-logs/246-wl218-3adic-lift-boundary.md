# wl246 — wl218 3-adic lift boundary

日期：2026-06-22

## 1. 本轮目标

接 wl245。

wl245 得到一个第一层局部约束：

```text
same-orientation both-pass => P ≡ Q (mod 3).
```

本轮检查它能不能提升为完整的 3-adic 矛盾。

普通话说：

```text
上一轮看到 mod 3 会逼 P 和 Q 同余。
这一轮问：继续看 mod 9、27、81，会不会越逼越紧，最后逼出矛盾？
```

---

## 2. 结果

答案是：

```text
不会自动逼出矛盾。
```

存在稳定的非中线 both-pass residue lift 塔。

例如 odd orientation，从：

```text
mod 9 residue: (m,n,u,v) = (0,1,1,3)
```

开始，可以逐层 lift：

```text
9  -> 27   count 81, v3(P-Q)=1 for all lifts
27 -> 81   count 81, v3(P-Q)=1 for all lifts
81 -> 243  count 81, v3(P-Q)=1 for all lifts
```

具体同一个代表链：

```text
mod 27 : (N,P,Q) = (13, 0, 21), P-Q = -21
mod 81 : (N,P,Q) = (67, 0, 75), P-Q = -75
mod 243: (N,P,Q) = (229,0,237), P-Q = -237
```

每一步：

```text
v3(P-Q) = 1.
```

even orientation 也有同样的 lift 塔。例如：

```text
mod 9 residue: (m,n,u,v) = (1,1,1,2)
```

同样逐层 lift：

```text
9  -> 27   count 81, v3(P-Q)=1 for all lifts
27 -> 81   count 81, v3(P-Q)=1 for all lifts
81 -> 243  count 81, v3(P-Q)=1 for all lifts
```

普通话说：

```text
mod 3 确实强迫 P-Q 能被 3 整除，
但它不强迫 P-Q 被 9、27、81 ... 越来越高次地整除。
```

---

## 3. 对证明路线的影响

这说明不能只靠：

```text
3 | (P-Q)
```

来关闭非中线分支。

因为有 3-adic 局部点一直活着，并且保持：

```text
v3(P-Q) = 1.
```

所以 wl245 的 mod 3 结论应被理解为：

```text
一个必要条件；
一个 gcd / valuation 分配入口；
不是单独的局部矛盾。
```

后续如果继续走 valuation，必须加入更多结构，例如：

```text
P-Q = ±2(mu+nv)(nu-mv)
P+Q = 2(mu-nv)(mv+nu)
N-P = a(d-c)
N-Q = c(b-a)
primitive gcd constraints
```

普通话说：

```text
3 这盏灯能指出 P-Q 有问题，
但它自己不能把门关上；还要看这个 3 落在 mu+nv、nu-mv、N-P、N-Q 的哪一侧。
```

---

## 4. 代码入口

新增 helper：

```text
sum_ab_same_orientation_both_pass_lift_summary(
    modulus=...,
    orientation=...,
    residue=(m,n,u,v),
    prime=3,
)
```

它统计一个 residue 类到下一层 `prime * modulus` 的 lift：

```text
lift_count
diff_valuation_counts  # v_p(P-Q) 分布
examples               # 少量 (m,n,u,v,N,P,Q)
```

新增测试：

```text
test_sum_ab_same_orientation_both_pass_lift_summary_tracks_3adic_survivors
```

测试锁住：

```text
odd/even 都有 mod 9 -> mod 27 的 81 个非中线 lifts；
这些 lifts 全部满足 v3(P-Q)=1。
```

---

## 5. 当前边界

可以安全说：

```text
1. same-orientation both-pass 的 mod 3 约束是真的；
2. 该约束不能单独提升成 3-adic 矛盾；
3. 存在非中线 3-adic lift 塔，且 v3(P-Q)=1；
4. 下一步要加入 gcd/primitive/global 因子分配。
```

不能说：

```text
sum=A+B 已证明。
3-adic valuation 已关闭 same-orientation。
mod 3 约束足以推出 P=Q。
```

---

## 6. 下一步

最具体的下一步不是继续单独升模，而是分析：

```text
3 | P-Q = ±2(mu+nv)(nu-mv)
```

时，`3` 落在：

```text
mu+nv
```

还是：

```text
nu-mv
```

并把它和：

```text
N-P=a(d-c)
N-Q=c(b-a)
```

及 primitive gcd 条件合并。

普通话说：

```text
现在不能只问 P-Q 被不被 3 整除。
要问这个 3 是从哪一个原始因子来的，
以及它会不会迫使另一个因子也带 3，从而破坏 primitive 或产生递降。
```
