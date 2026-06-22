# wl251 — wl218 residual prime-class summary

日期：2026-06-22

## 1. 本轮目标

接 wl250。

wl250 暴露的关键问题是：

```text
旧 guard 假点的坏 squareclass 是 29，
而 29 ≡ 1 (mod 4)。
```

所以只看 `q ≡ 3 mod 4` 的成员赋值，不会抓住这个假点。

本轮继续问：

```text
这只是一个孤立 guard，
还是 finite root-grid product-layer residual 里确实会出现
“只坏在 1 mod 4”的类别？
```

普通话说：

```text
上一轮看到一只假点从 3 mod 4 网眼里漏过去。
这一轮把它放进一个小扫描摘要里，确认这个漏法会被工具稳定记录，
而不是手算时偶然看到的现象。
```

---

## 2. 新 helper

新增：

```text
sum_ab_root_grid_residual_prime_class_summary(
    max_numerator=...,
    max_denominator=...,
)
```

它枚举 root-grid residual：

```text
r, s in bounded positive rationals
lambda = r+s-1
r+s = lambda+1
A_p, B_p are squares
not centerline
not reciprocal
not true R_lambda members
```

然后对每个 residual 调用：

```text
closure_member_prime_valuation_ledger(...)
```

按 member squareclass prime 分类：

```text
trivial_squareclass
has_3_mod_4_squareclass
only_1_mod_4_squareclass
```

普通话说：

```text
这个 helper 不证明无穷情形。
它只是把 product-layer 假点按“坏素数属于哪一类”分桶，
帮助我们判断下一条引理该盯哪里。
```

---

## 3. 小范围结果

测试锁住的范围：

```text
max_numerator  = 26
max_denominator = 23
```

得到：

```text
total_residuals = 1
bucket_counts = {
  only_1_mod_4_squareclass: 1
}
squareclass_prime_counts = {
  (29,): 1
}
three_mod_four_squareclass_prime_counts = {
  (): 1
}
```

唯一例子仍是：

```text
lambda = 535/161
r = 14/23
s = 26/7
member_squareclass_pair = (29, 29)
```

普通话说：

```text
这个小范围里出现的唯一 residual，
正好就是“只坏在 1 mod 4”的类型。
没有任何 3 mod 4 的坏 squareclass prime。
```

---

## 4. 为什么这对证明有用

用户原第 4 点想要：

```text
用 q ≡ 3 mod 4 的赋值矛盾强制 p=lambda。
```

现在更精确地说，必须先补一个前置引理：

```text
若 sum=A+B 存在非倒数真闭合候选，
则它的共同坏 squareclass 不能全部来自 1 mod 4 素数。
```

或者改走更宽路线：

```text
同时处理 q ≡ 1 mod 4 的共同坏 squareclass。
```

普通话说：

```text
如果坏因子都像 29 这样落在 1 mod 4，
那 3 mod 4 赋值工具看不见它。
所以证明必须解释为什么真闭合里不会发生这种事，
或者把 1 mod 4 也纳入主证明。
```

---

## 5. 当前边界

可以安全说：

```text
1. product-layer residual 的 prime-class 摘要已经可复跑；
2. bounded root-grid 的已知 residual 是 only_1_mod_4_squareclass；
3. 这继续说明原 3 mod 4 valuation 引理需要前置条件。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
only_1_mod_4 情形已被排除。
```

---

## 6. 下一步

下一步应该直接研究 only-1-mod-4 情形。

两个具体方向：

```text
1. 在 Euclid/斜率模型中追共同 squareclass d，
   假设 d 的素因子全是 1 mod 4，
   看是否能通过 Gaussian norm 吸收成新的有理斜率参数；

2. 扩大 root-grid / slope-grid 摘要，但只记录 prime-class bucket，
   不再输出大对象，避免扫描本身拖慢。
```

普通话说：

```text
我们现在知道 3 mod 4 不是第一刀。
第一刀可能应该是：
“全是 1 mod 4 的坏因子，到底能不能被重新参数化掉？”
```
