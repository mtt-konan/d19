# wl108 — 固定比例 A=kB：纯同余筛的边界

日期：2026-06-08

承接 wl107 和用户问题：

```text
能不能用现有筛子，理论证明 A = kB 这种固定比例分支做不到？
```

本轮把这个想法写成可执行的同余证书检查器，结果是一个负结论。这里说的是
**纯 residue 筛**，不是后续 wl109 的真实 multi-N / 因子分解路线：

```text
当前 chain-closure / full-plane 这类纯同余筛，不能单独证明 A = kB 无解。
不是因为模数不够多，而是因为每个模数都有一个 universal primitive local survivor。
```

---

## 1. 固定比例下筛子要检查什么

固定：

```text
A = kB
```

若存在反例，对某两个竖向长度 `N1,N2`，必须满足：

```text
B^2 + N_i^2      是平方
(kB)^2 + N_i^2   是平方
```

并满足 full-plane closure 四关系之一：

```text
N1 + N2 = A + B       = (k+1)B
N1 + N2 = |A - B|     = |k-1|B
|N1-N2| = A + B       = (k+1)B
|N1-N2| = |A - B|     = |k-1|B
```

把它模 `M` 化以后，理论证书的理想形态是：

```text
模 M 下不存在 primitive residue (B,N1,N2)。
```

因为真正的整数反例可以先除掉：

```text
gcd(A,B,N1,N2)
```

在 `A=kB` 分支里，这等价于只需要考虑：

```text
gcd(B,N1,N2) = 1
```

所以如果某个模数能强迫所有局部解都满足：

```text
gcd(B,N1,N2,M) > 1
```

就可以接无限递降/primitive contradiction。

---

## 2. 关键发现：每个模数都有同一个幸存类

对任意整数 `k >= 1`、任意模数 `M >= 2`，都有：

```text
B  ≡ 0      (mod M)
N1 ≡ 1      (mod M)
N2 ≡ -1     (mod M)
```

此时：

```text
A = kB ≡ 0                       (mod M)
N1^2 + B^2  ≡ 1                  (mod M)，是平方
N1^2 + A^2  ≡ 1                  (mod M)，是平方
N2^2 + B^2  ≡ 1                  (mod M)，是平方
N2^2 + A^2  ≡ 1                  (mod M)，是平方
N1 + N2     ≡ 0 ≡ A+B            (mod M)
```

而且它是 primitive 的：

```text
gcd(B,N1,N2,M) = gcd(0,1,-1,M) = 1
```

这说明：

```text
任何只看这些模同余条件的 finite sieve，都不可能给出“无 primitive residue”的证书。
```

这不只杀掉单个模数。给定任意有限模数集合，取它们的 lcm 作为一个大模数，同一个 residue 仍然活：

```text
B  ≡ 0      (mod lcm(M_i))
N1 ≡ 1      (mod lcm(M_i))
N2 ≡ -1     (mod lcm(M_i))
```

所以“多加几个模数”也不能解决这个证明问题。

---

## 3. 新增代码

新增模块：

```text
src/rational_distance/concordant/fixed_ratio_sieve.py
```

核心接口：

```text
fixed_ratio_allowed_n_mod(k, b, modulus)
universal_zero_b_witness(k, modulus)
is_fixed_ratio_witness(k, modulus, witness)
certify_fixed_ratio_modulus(k, modulus)
find_fixed_ratio_killer_modulus(k, moduli)
```

新增测试：

```text
tests/test_fixed_ratio_sieve.py
```

测试覆盖：

```text
固定比例 allowed-N residue 与直接平方条件一致。
universal witness 对任意 k、M 是合法 primitive witness。
k=2, M=9 报告 local_survives，而不是误判 mod_killed。
k=1..7 在 (9,25,49,121) 下都找不到 killer modulus。
任意有限模数包合成 lcm 后，universal witness 仍然活。
```

---

## 4. 这对 A=kB 证明意味着什么

当前结论不是：

```text
A = kB 可行。
```

当前结论是：

```text
用现有 full-plane closure 同余筛，无法直接证明 A = kB 不可行。
```

这比“试了没找到”强，因为纯 residue 层已经有结构性原因：

```text
B ≡ 0, N1 ≡ 1, N2 ≡ -1
```

会穿过任何有限同余包。注意：这个 residue witness 不是一个真实反例候选，真实
`N1,N2` 仍必须由 `find_concordant_by_factorization(A,B)` 生成。wl109 改走的就是
这条 exact multi-N 路线。

所以若要继续证明固定比例，必须加入当前筛子没表达的信息，例如：

```text
勾股参数化的 gcd/奇偶细节，而不是只看平方剩余；
Yang Ji 式无限递降；
B 被模数整除时的 p-adic 赋值传播；
固定 k 后的椭圆曲线/高亏格曲线有理点列尽；
对 B,N1,N2 的大小/正性/精确等式信息，而不是只看 residue。
```

---

## 5. 下一步建议

不要继续尝试：

```text
加更多 p^2 模数来直接 kill A=kB。
```

更有希望的路线：

```text
1. 写 center-line-impossibility proof note，先把 k=1 本地化关闭。
2. 拆 Yang Ji 固定 n 定理，找它在复合 n 时失败的具体 gcd 步。
3. 对 A=kB 加入 p-adic valuation，而不是只枚举 residue。
4. 对小 k 建椭圆曲线/曲线切片，尝试列尽有理点。
```

一句话：

```text
固定比例仍值得攻，但不能靠当前纯同余筛单独完成。下一步要用真实 multi-N / ratio
结构，再把“筛子”升级成“递降 + valuation”的证明，而不是再堆模数。
```
