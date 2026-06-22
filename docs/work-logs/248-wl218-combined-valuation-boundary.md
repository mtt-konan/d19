# wl248 — wl218 combined valuation boundary

日期：2026-06-22

## 1. 本轮目标

接 wl247。

wl247 说明：

```text
P-Q = +/- 2(mu+nv)(nu-mv)
```

里的 `3` 不会固定落在某一个因子上。

本轮继续把账本扩大，同时看：

```text
P-Q = +/- 2(mu+nv)(nu-mv)
P+Q =    2(mu-nv)(mv+nu)
N-P
N-Q
```

普通话说：

```text
上一轮只盯 P-Q 这一个差。
这一轮把 P-Q、P+Q、N-P、N-Q 放在一张表里，
检查这些估值会不会合起来把非中线分支逼死。
```

---

## 2. 结果

结果仍然是边界结论：

```text
简单的 combined 3-adic residue 账本还不能关门。
```

在模 27 的 same-orientation 非中线 both-pass residue 中：

```text
orientation=odd:
  total survivors = 124416
  valuation patterns = 49

orientation=even:
  total survivors = 124416
  valuation patterns = 45
```

前两类最大 pattern 分别是：

```text
odd:
  (1,0,1,0,0,0,1,1): 23328
  (0,1,0,1,0,0,1,1): 23328

even:
  (1,0,0,1,0,0,1,1): 23328
  (0,1,1,0,0,0,1,1): 23328
```

pattern 的八个位置依次是：

```text
v3(mu+nv)
v3(nu-mv)
v3(mu-nv)
v3(mv+nu)
v3(N-P)
v3(N-Q)
v3(P-Q)
v3(P+Q)
```

普通话说：

```text
把账本扩成八列以后，局部世界仍然不是一条路。
它分成几十种活 pattern，所以还不能直接写成估值矛盾。
```

---

## 3. 零 offset 退化

这里额外记录一个危险细节。

估值是在原始整数多项式上算的；literal zero 用 sentinel `99` 记录。
在模 27 账本里，`N-P` 或 `N-Q` 为整数零的 pattern 个数是：

```text
odd  : 4
even : 4
```

普通话说：

```text
有些局部类不是“被 3 整除很多次”，而是某个 offset 在整数代表元上直接等于 0。
这类退化如果不单独处理，很容易把估值论证写错。
```

这些仍然只是 residue/local points，不是真整数反例。

---

## 4. 代码入口

新增 helper：

```text
sum_ab_same_orientation_combined_valuation_summary(
    modulus=27,
    orientation="odd" / "even",
    prime=3,
)
```

它统计非中线 both-pass residue 类中：

```text
(
  v_p(mu+nv),
  v_p(nu-mv),
  v_p(mu-nv),
  v_p(mv+nu),
  v_p(N-P),
  v_p(N-Q),
  v_p(P-Q),
  v_p(P+Q),
)
```

的分布，并给每类一个整数代表元例子。

新增测试：

```text
test_sum_ab_same_orientation_combined_valuation_summary_shows_many_local_patterns
```

测试锁住：

```text
mod 27 下 odd 有 49 类 pattern；
mod 27 下 even 有 45 类 pattern；
最大两类仍是非中线 survivor；
存在 zero-offset 退化 pattern。
```

---

## 5. 对证明路线的影响

可以排除又一条过于乐观的路线：

```text
both-pass
=> P-Q, P+Q, N-P, N-Q 的 v3 分布唯一
=> 直接推出 P=Q
```

这条路线在局部 residue 层失败。

现在更可信的下一步不是继续只升 `mod 3^k`，而是把局部账本和全局条件合并：

```text
primitive gcd constraints
真实四平方条件，而不是只看 residue square
positivity / ordering constraints
full-plane 四分支的目标 T 与判别式符号
```

普通话说：

```text
局部模 3 像一张粗筛网。
它能筛掉一些假路，但网眼还很大。
要证明倒数定理，需要再叠上“真成员”的全局平方条件和 gcd 条件。
```

---

## 6. 当前边界

可以安全说：

```text
1. same-orientation 的多因子 3-adic residue 账本已经可复跑；
2. mod 27 下仍有大量非中线 both-pass 局部 pattern；
3. 单纯 combined valuation 还不是证明；
4. sum=A+B 分支仍未闭合；
5. 全平面倒数定理还需要另外三个分支。
```

不能说：

```text
sum=A+B 已证明。
wl218 倒数定理已证明。
mod 27 combined valuation 已经排除全部非中线情形。
```

---

## 7. 下一步

下一步应从“局部 residue 活着”转向“全局真成员能不能活着”：

```text
1. 对这些 pattern 加 primitive gcd 条件；
2. 区分 literal zero offset 和高阶可整除；
3. 把四个 membership squares 重新拉回整数方程；
4. 若 sum=A+B 仍无法闭合，先找最小 global candidate 或证明局部 pattern 无法 lift 成真成员。
```

普通话说：

```text
局部账本告诉我们：这条捷径走不通。
但它也给出了下一步应该盯哪些缝隙：
不是只看 P-Q，而是看这些局部活分支能不能同时满足真正的四个平方条件。
```
