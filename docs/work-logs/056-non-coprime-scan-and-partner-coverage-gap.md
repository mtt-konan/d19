# wl056 — 直接非互素扫描 + partner 反推覆盖率审计：从 91% 到 94% 都被漏掉

## 起点：用户的可疑样本

用户在 IDE 跑了：

```text
$ uv run python scripts/search.py concordant --pair 264,420 --concordant-method factor
(A=264, B=420): concordant_n=[77, 315, 352, 1440]
```

(264, 420) gcd=12 是非互素 multi-N pair（k=4），用户问"是不是被 partner 全扫漏掉了"。

实测 partner 全扫**没漏**这一例：

```text
$ grep '"a": 264, "b": 420' results/partner_pair_k_distribution.jsonl
{"a": 264, "b": 420, "gcd": 12, "coprime": false, "k": 4, "concordant_N": [77, 315, 352, 1440],
 "source": "factor_search", "in_catalog": false}
```

并且 `scripts/find_partner_origin.py 264 420` 显示它由 catalog 行 `(77, 1440)` 和
`(315, 352)` 各抛出一次。但这只是**一个特定例子没漏**，不能推到一般。wl055 末尾
"钩子 1" 明确留了"partner 反推 vs 直接非互素扫描的差距尚未量化"这个口子，
现在补上。

## 工具

`scripts/non_coprime_multi_n_scan.py`：

- 输入参数：`--max M`（扫描上界），`--partner-set`（partner 反推结果，默认
  `results/partner_pair_k_distribution.jsonl`）。
- 行为：枚举所有 `1 <= a < b <= M` 且 `gcd(a, b) > 1` 的 pair，跑权威
  `find_concordant_by_factorization`，对比 partner 集。
- 输出：`results/non_coprime_scan_max{M}.jsonl`（k>=2 实例）+
  `results/non_coprime_scan_max{M}_summary.json`（覆盖率 + missing top20）。

## 数据：M=500 / M=2000

```text
M=500
  扫描 gcd>1 pair         48,635
  multi-N pair (k>=2)        191
    in partner 集             17
    NOT in partner 集        174   91.10% miss
  覆盖率                  8.90%
  用时                    0.5s

M=2000
  扫描 gcd>1 pair        782,413
  multi-N pair (k>=2)      1,802
    in partner 集            110
    NOT in partner 集      1,692   93.90% miss
  覆盖率                  6.10%
  用时                    26.8s
```

## 第一个反直觉：覆盖率随 M 增大反而**降低**

```text
M=500    8.90%
M=2000   6.10%
```

按 wl055 直觉，partner 集（10,533 条）应该覆盖大部分非互素 multi-N。实际上不仅
没有，反而 M 越大、漏的越多。原因：

```text
partner 集 = catalog 互素行 (A, B) 的 concordant_N 列表里所有 (N_i, N_j) 对
catalog 互素行的 N 通常是大数（互素 + max_hyp 的双重过滤把小 N 都筛走了）
⇒ partner 反推捞到的 (P_a, P_b) 也偏大
⇒ 小 (a, b) 的非互素 multi-N pair 完全在 catalog 视野之外
```

## 第二个反直觉：(15, 48) ↔ (20, 36) 是孤立 partner cycle

漏掉的最小 multi-N pair：

```text
(15, 48)  k=2  N=[20, 36]      ←—— 自身 multi-N，partner 是 (20, 36)
(20, 36)  k=2  N=[15, 48]      ←—— 自身 multi-N，partner 是 (15, 48)
```

两者**互为 partner**，但**两者都不在 partner 集**。意味着：

```text
catalog 互素行里没有任何一行 (A, B) 的 concordant_N 同时包含 {15, 48}
catalog 互素行里也没有任何一行 (A, B) 的 concordant_N 同时包含 {20, 36}
```

也就是说，`{(15, 48), (20, 36)}` 形成一个**与 catalog 完全脱节的 2-cycle**。
他们彼此互验 multi-N，但没有任何"上游" catalog 行能反推到他们。这是
partner 反推的根本盲区：**arbitrary multi-N pair 不必从 catalog 出发可达**。

## 第三个反直觉：高 k 实例几乎全漏

M=2000 范围内 k 分布：

```text
k    扫到 (total)   漏掉 (miss)   漏比 (%)
2     1,647         1,556          94.5
3       135           122          90.4
4        20            14          70.0
```

**K_4 实例 20 个，漏掉 14 个**。即 wl055 报告的"全 partner 范围内 K_4=415"
是**严重低估** —— 仅在 a, b ≤ 2000 这个小窗口里，直接扫描就找出 14 个 K_4
不在 partner 集里。按密度外推到 catalog 全范围（max ≈ 100000），真实 K_4
数量可能是 wl055 数字的 5-50 倍。

漏掉的 K_4 顶 5 个：

```text
( 195,  960)  gcd=  15  k=4  N=[216, 400, 468, 1456]
( 300, 1092)  gcd=  12  k=4  N=[455, 720, 2240, 3744]   ←—— N 含 3744
( 390, 1920)  gcd=  30  k=4  N=[432, 800, 936, 2912]
( 459, 1680)  gcd=   3  k=4  N=[612, 1260, 6188, 11700]
( 525, 1152)  gcd=   3  k=4  N=[700, 864, 1040, 9180]
```

`(300, 1092)` 的 N 列表里出现 `3744` —— 这正是 wl054 K_4 实例
`{3744, 22631, 44631, 70720}` 的一个节点。说明 K_n 之间存在跨级 partner 链接
（partner 不止抽 catalog 的 N，N 池里的某些数本身又是另一个 partner pair 的
节点）。这是 wl054/wl055 的 partner 图都没充分挖掘的结构。

## 修正的数学图景

```text
旧 wl055 假设
─────────────
multi-N pair 全集 = catalog (互素) ∪ partner 反推 (非互素)
                  = 10,333 + 10,533 = 20,866

新 wl056 数据
─────────────
仅 a,b ≤ 2000 范围内：
  互素 catalog 行的覆盖：少（catalog 里 a,b ≤ 2000 的行数有限）
  partner 反推覆盖：6.10%
  非互素 multi-N 实际数量：1,802（仅这个小窗口）

按密度外推到 a,b ≤ 100000：
  非互素 multi-N 总数预计 >> 100,000
  partner 反推捞到 10,533 → 覆盖率预计 < 5%
  catalog ∪ partner 反推远不足以代表"multi-N 全集"
```

## Catalog 工作流的修正建议

要拿到"全量 multi-N catalog"，**必须**加上直接非互素扫描这一层：

```text
现在（wl048 + wl055）              修正后建议
───────────────────                ─────────────────────────
fast pivot scanner (互素)           fast pivot scanner (互素)
  → catalog_coprime.jsonl             → catalog_coprime.jsonl
                                        +
partner 反推 (非互素子集)           直接非互素扫描 a,b<=M, gcd>1
  → partner_pairs.jsonl                 → catalog_non_coprime.jsonl
                                        +
                                      partner 反推 (无须，已被上面覆盖)
                                        +
                                      合并去重
                                      → catalog_full.jsonl
```

工期估计：

```text
直接非互素扫描的复杂度
  M=2000     782,413 pair    27s
  M=10000   ~20M pair        ~12 min  （并行化后 ≈ 2-3 min）
  M=50000   ~600M pair       ~6 hours （并行化后 ≈ 1 hour）
  M=100000  ~2.5B pair       ~24h    （并行化后 ≈ 4-6 hour）
```

考虑到 partner 集已经能给出 K_8 这种顶级实例，直接非互素扫描不必扫到 max=100000
才有用 —— **M=10000 已经能让 K_3/K_4 计数变得真实**，并且只要 2-3 分钟（并行）。

## wl055 需要修正的句子

wl055 末尾原文：

> "Partner reduction is currently the only known way to systematically extract
> the non-coprime layer."

应改为：

> Partner reduction extracts a thin slice (≈6% at M=2000) of the non-coprime
> layer biased toward large (a, b). To get full coverage, direct non-coprime
> scan over (a, b) pairs is needed and is feasible (M=10000 in 2-3 minutes
> when parallelized).

## 文件

```text
scripts/find_partner_origin.py                            给定 partner 反推 catalog 来源
scripts/non_coprime_multi_n_scan.py                       直接扫描 + partner 集对比
results/non_coprime_scan_max500.jsonl                     M=500 实例
results/non_coprime_scan_max500_summary.json
results/non_coprime_scan_max2000.jsonl                    M=2000 实例（1,802 行）
results/non_coprime_scan_max2000_summary.json
docs/work-logs/056-non-coprime-scan-and-partner-coverage-gap.md   本文件
```

## 没做的事

1. **M=10000 / M=50000**：要重新跑（有并行化版本更佳）。
2. **K_5+ 在直接扫描下的真实计数**：M=2000 范围内只有 K_4 出现，K_5 partner
   的最小 (a, b) 在 wl055 是 `(2640, 21216)` —— 推到 M=10000 应该能见到几个
   K_5 直接扫描结果。
3. **catalog 工作流整合**：把直接非互素扫描包装成与 fast scanner 同口径的
   pipeline 步骤，需要重新审视 wl048 的 catalog schema。
4. **K_n 跨级 partner 链接**（如 `(300, 1092)` 的 N 列表含 3744 这种）尚未
   作为图结构挖掘。
