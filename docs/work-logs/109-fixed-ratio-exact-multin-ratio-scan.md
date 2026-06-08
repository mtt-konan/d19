# wl109 — 固定比例 A=kB：改用真实 multi-N / ratio 扫描

日期：2026-06-09

承接用户纠正：

```text
N1,N2 不是随便来的 residue，必须由真实勾股条件生成。
不能拿 B≡0, N1≡1, N2≡-1 这种模 witness 当真实候选。
应该按旧 multi-N / factor-concordant 算法求 N，再证明。
```

这个纠正是对的。本轮新增一条 exact 路线：固定 `A=kB`，用现有精确因子分解算法求真实 concordant `N`，再把 `N/B` 化成 ratio 检查 closure。

---

## 1. 旧算法怎样求真实 N

真实 concordant `N` 满足：

```text
N^2 + A^2 = h3^2
N^2 + B^2 = h4^2
```

两式相减：

```text
h4^2 - h3^2 = B^2 - A^2
(h4-h3)(h4+h3) = B^2 - A^2
```

于是枚举 `B^2-A^2` 的因子对：

```text
d1 = h4-h3
d2 = h4+h3
h3 = (d2-d1)/2
h4 = (d2+d1)/2
N^2 = h3^2 - A^2
```

最后检查 `N^2` 是否真平方。仓库里的精确函数是：

```text
src/rational_distance/concordant/factor_search.py
find_concordant_by_factorization(A, B)
```

这条路径没有搜索上界，不依赖 PARI，也不会产生随便的模 residue。

---

## 2. 固定比例后的 ratio 化

固定：

```text
A = kB
```

则：

```text
B^2 - A^2 = (1-k^2)B^2
```

更重要的是，closure 四关系都能整体除以 `B`。令：

```text
r_i = N_i / B
```

full-plane closure 变成：

```text
r1 + r2 = k + 1
r1 + r2 = |k - 1|
|r1-r2| = k + 1
|r1-r2| = |k - 1|
```

所以固定比例分支的理论目标可以改写成：

```text
先刻画所有可能的真实 ratio r = N/B。
再证明这些 ratio 之间不能满足上面四个线性关系。
```

这比直接扫大整数更接近证明。

---

## 3. 新增代码

新增 exact 模块：

```text
src/rational_distance/concordant/fixed_ratio_exact.py
```

核心接口：

```text
fixed_ratio_concordant_n(k, b)
fixed_ratio_ratios_for_b(k, b)
collect_fixed_ratio_ratios(k, max_b)
find_fixed_ratio_ratio_hits(k, ratios)
```

新增扫描脚本：

```text
scripts/theory/scan_fixed_ratio_exact.py
```

用法：

```text
PYTHONPATH=src uv run python scripts/theory/scan_fixed_ratio_exact.py \
  --k-min 1 --k-max 40 --max-b 500 \
  --jsonl-out results/fixed_ratio_exact_k1_40_b500.jsonl
```

新增测试：

```text
tests/test_fixed_ratio_exact.py
tests/test_scan_fixed_ratio_exact.py
```

测试覆盖：

```text
k=7,b=5 真实 N=[12]。
k=7,b=12 真实 N=[35]。
k=7,max_b=30 去重后 ratio 为 12/5 和 35/12。
ratio 层能检出人为构造的 sum=A+B hit。
centerline hit 单独报告，不混入非中心线 hit。
脚本 JSON 输出稳定。
```

---

## 4. 小范围 exact 扫描结果

运行：

```text
PYTHONPATH=src uv run python scripts/theory/scan_fixed_ratio_exact.py \
  --k-min 1 --k-max 40 --max-b 500 \
  --jsonl-out results/fixed_ratio_exact_k1_40_b500.jsonl
```

输出中只列有真实 ratio 的 `k`：

| k | ratios N/B | noncenter closure hit |
|---:|---|---|
| 7 | `12/5`, `35/12` | none |
| 10 | `35/12`, `24/7` | none |
| 11 | `21/20`, `220/21` | none |
| 12 | `45/28`, `112/15` | none |
| 14 | `15/8`, `112/15` | none |
| 17 | `528/455` | none |
| 19 | `1155/68` | none |
| 22 | `40/9`, `99/20` | none |
| 23 | `13685/468` | none |
| 27 | `99/20`, `60/11` | none |
| 28 | `2112/65` | none |
| 29 | `165/52`, `1508/165` | none |
| 30 | `275/252`, `1512/55` | none |
| 33 | `1288/255` | none |
| 39 | `6160/111` | none |
| 40 | `1600/399`, `399/40` | none |

边界：

```text
这是有限 exact 扫描，不是证明。
但它说明固定 k 后，真实 N/B ratio 的种类非常少，缩放 B 主要重复同一批 ratio。
```

---

## 5. 修正 wl108 口径

wl108 的结论应这样理解：

```text
纯 residue 筛不能单独证明 A=kB。
```

它不否定 exact multi-N 路线。用户指出得对：

```text
真实 N 不是任意 residue，必须由 factor-concordant 生成。
```

所以后续不要继续拿 universal residue 当真实候选。它只说明：

```text
有限模筛看不到足够信息。
```

真正应继续的是本 wl 的 exact ratio 路线。

---

## 6. 下一步

最值得做的理论步骤：

```text
1. 对固定 k 推导所有可能 r=N/B 的有理参数化。
2. 用 r1±r2=k±1 代入参数化，尝试变成无解方程。
3. 优先 k=7,10,11,12,14，因为它们在小范围里已有两个真实 ratio，足够测试 closure 失败机制。
4. k=1 仍走 Yang Ji 中线证明，不要用本扫描替代。
```

一句话：

```text
固定比例路线没有死；只是不能靠 residue 筛。现在的正确入口是：真实 N -> ratio N/B -> closure 线性关系。
```
