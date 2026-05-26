# wl055 — K_n 等价定理 + partner pair 完整 k 分布（K_3 到 K_8）

## 起点：用户洞察

wl054 用 partner 图意外发现 K_4 / K_5 子图，通过"共享 partner"路径枚举得到
17 个 K_3+。但用户在审视 K_5 实例 `{1287, 1700, 4437, 19712, 43520}` +
`shared_partner = (2640, 21216)` 时一句话指出：

> "K_5 其实不就是 (2640, 21216) 有 5 个 concordant N 吗，好像就是换了个说法而已。"

这是对的，而且是个**严格的数学等价**。沿着这条线把 wl054 的图论枚举
完全 reframe 成了一维问题。

## 等价定理（partner 恒等式的对偶）

```text
原始恒等式：
  (A, B) 是 multi-N pair, concordant_N = [N_1, ..., N_k]
  ⇔
  对任意 i ≠ j, (N_i, N_j) 也是 multi-N pair（且其 N 列表 ⊇ {A, B}）

对偶/重述：
  partner pair (P_a, P_b) 是 k = n 的 multi-N pair
  ⇔
  其 N 列表 [N_1, ..., N_n] 形成 K_n
  （n 个数两两都是 multi-N pair，且都共享 partner (P_a, P_b)）
```

也就是说，"K_n（共享 partner）"不是新结构，是 multi-N pair 的对偶视角。
一组 K_n 实例 = 一个 k = n 的 multi-N pair。**枚举 K_n 等价于枚举 multi-N pair 按 k 排序。**

## 实证：把 wl054 的 17 个 K_n 反查 partner k

`scripts/verify_kn_equivalence.py` 对 wl054 输出的 17 个 K_n 实例逐个跑
factor_search 取 partner 自身的 N 列表，对照：

```text
EQUAL    12   partner 的 N 列表 ≡ K_n 节点集（partner 自己就是 k = n multi-N pair）
SUPERSET  5   partner 的 N 列表 ⊋ K_n 节点集（partner 自己 k > n，K_n 是它的子集）
MISMATCH  0   ← 这一行是 0，partner 恒等式从未失败
```

5 个 SUPERSET 案例最关键 —— wl054 脚本"漏掉"了 partner 真正的全部 N，因为它只用
catalog 入边推 K_n 节点。比如：

```text
wl054 报 K_5  partner (2640, 21216) k = 6, 实际 K_6
wl054 报 K_4  partner (5460, 59400) k = 6, 实际 K_6
wl054 报 K_4  partner (17160, 31920) k = 5, 实际 K_5
wl054 报 K_4  partner (13260, 115500) k = 5, 实际 K_5
wl054 报 K_3  partner (1716, 5916) k = 4, 实际 K_4
```

**wl054 系统性低估**：它只看 partner 的"互素入边"，但 partner 的 N 列表里有些
N 之间是**非互素** multi-N（不在 catalog），需要 factor_search 才发现。

## 全扫：所有 partner pair 的 k 分布

`scripts/partner_pair_k_distribution.py` 对 catalog 的所有 unique partner
（10,533 个）跑一遍 factor_search，78.6 秒（≈134/s）。结果：

```text
catalog rows                10,333    （max_hyp=100000 互素 multi-N，wl048 产物）
unique partner pairs        10,533

  k = 2    8,474   非互素 multi-N pair, 但不形成 K_3+
  k = 3    1,461   K_3
  k = 4      415   K_4
  k = 5      136   K_5
  k = 6       41   K_6
  k = 7        4   K_7  ← 首次见
  k = 8        2   K_8  ← 极其稀有

K_3 +     2,059
K_5 +       183
K_6 +        47
K_7 +         6
K_8           2

max_k = 8（catalog 范围内 partner 最大 k）
```

**全部 10,533 个 partner pair 都是非互素的**（gcd ≥ 12 起步），都不在 catalog。
这是 wl054 末尾"项 1"完备性审计的最终答案。

## K_8 顶级实例（K_n 阶梯顶端）

```text
K_8  (55440, 445536)  gcd = 1008
     N = [7552, 27027, 35700, 59670, 93177, 413952, 608580, 913920]
     这 8 个数两两都是 multi-N pair（C(8, 2) = 28 对，全部 multi-N）

K_8  (58800,  98280)  gcd =  840
     N = [7875, 25792, 28665, 73710, 78400, 179046, 201600, 733824]
```

这是 max_hyp=100000 catalog 反推出的最大 K_n，K_9+ 在该范围内不存在。

## K_7 / K_6 取样

```text
K_7  (10200,  37128)  gcd = 408   N=[2975, 7904, 15470, 24480, 42750, 76160, 127296]
K_7  (10920, 118800)  gcd = 120   N=[4851, 9152, 34650, 37440, 60350, 95238, 141750]
K_7  (50160, 403104)  gcd = 912   N=[24453, 32300, 71500, 84303, 374528, 550620, 826880]
K_7 (102000, 303600)  gcd = 1200  N=[51982, 98325, 126500, 244800, 515200, 633420, 1732500]

K_6  ( 2640,  21216)  gcd = 48    N=[1287, 1700, 4437, 19712, 28980, 43520]
K_6  ( 3696,   8160)  gcd = 48    N=[495, 2380, 3978, 9350, 12672, 60928]
K_6  ( 4680,  95760)  gcd = 360   N=[2698, 4914, 9600, 22575, 46683, 91200]
... 共 41 个 K_6
```

完整表见 `results/partner_pair_k_distribution.jsonl`。

## reduce 不保 multi-N（wl054 末尾 + 本次的二次确认）

K_4 实例 `{3744, 22631, 44631, 70720}` 的 6 条边：

```text
互素那 4 对在 catalog                非互素那 2 对 reduce 后
─────────────────────────             ─────────────────────────────────
( 3744, 22631)  k = 2                 ( 3744, 44631) gcd = 9
(22631, 44631)  k = 2                 reduce → (416, 4959) k = 1  ⚠ 不是 multi-N
(22631, 70720)  k = 2                 
(44631, 70720)  k = 2                 ( 3744, 70720) gcd = 416
                                      reduce → (9, 170) k = 0    ⚠ 没有任何 N
```

也就是：**(3744, 44631) 是 multi-N pair**（k = 3），但**它的 reduce 形式 (416, 4959)
不是 multi-N**。reduce 操作不保 multi-N 性质。这意味着：

```text
仅靠互素扫描 + reduce 复原                找不到非互素 multi-N pair
仅靠 partner 反推                          找到了 10,533 个非互素 multi-N pair
```

**catalog 在互素约定下完备 ≠ catalog 是 multi-N pair 全集**。前者是事实
（wl054 验证），后者远不成立 —— max_hyp=100000 范围内，已知非互素 multi-N pair
至少 10,533 个，是互素 catalog（10,333）的 1.02 倍。这还只是"partner 反推
能看到的"那部分；实际非互素 multi-N 总数大于 10,533。

## Catalog 的修正定义

```text
旧定义：catalog = max_hyp 范围内所有 multi-N pair
真实： catalog = max_hyp 范围内所有"互素" multi-N pair (a, b) (gcd = 1)
       且其 partner 反推得到 ≥ 10,533 个非互素 multi-N pair (这是真子集，但目前最大
       已知子集)
```

如果要造"全量" multi-N catalog，需要：

1. 现在的 fast scanner 互素扫描 → 10,333 行
2. partner 反推 → 至少 10,533 行非互素
3. 直接非互素扫描（`gcd(a, b) > 1`，按 a, b 上界枚举跑 factor_search）→ 未知
   多少行额外

partner 反推（步骤 2）非常便宜（< 80 秒），强烈建议把它作为 catalog 的标准
派生层，命名 `multi_concordant_N_max100000_partners.jsonl`。

## 算法简化的意义

**K_n 枚举从图论问题降级为一维问题**：

```text
旧路径（wl054 partner_kn_subgraphs.py）       新路径（用户洞察后）
─────────────────────────────────             ──────────────────────────────
1. 建 partner 图                              1. 列出所有 partner pair
2. 找高入度顶点                                2. 每个跑 factor_search 拿 k
3. 验证 source-pair 节点集合两两 multi-N        3. 按 k 降序 = K_n 阶梯
4. 容易漏 SUPERSET 的额外节点 ⚠
```

新路径产物比旧路径**更完整**（不会漏 SUPERSET）、**更直接**（不需要图论）、
**更快**（10,533 partner / 78s ≈ 一次性扫完整库）。

## Partner 路径作为搜索加速

用户在 wl054 末尾问的"用这种方法是不是能更快找到 multi-N pair" —— 答案是
**对，而且只对一类目标**：

```text
找互素 multi-N (a, b)              fast scanner（wl048）继续是主路径，partner 帮不上
找非互素 multi-N (a, b)            partner 反推是目前唯一已知方法，提速无穷大
找 K_n (n ≥ 3) 大子图              partner 反推就是答案，不必额外算图
统计高 k multi-N pair              partner 反推完整覆盖（≤ catalog 范围内）
```

## 哪些工作没做（钩子）

1. **partner 反推 vs 直接非互素扫描**的差距没量化：可能存在非互素 multi-N pair
   `(a, b)` 它的 N 池里**没有** catalog 的任何互素 multi-N 行，那 partner 反推
   就漏了它。要量化这个差距，需要单独跑非互素扫描（`gcd > 1` 直接枚举 (a, b)）。
2. **K_8 / K_7 实例的 PARI ellrank / F2-rank 还没算**。这些是 catalog 之外的
   非互素 multi-N pair，wl050 / wl051 的工具流没把它们当输入跑过。鉴于 K_8 只有
   2 个、K_7 只有 4 个，跑一次几分钟内完成。
3. **K_n 与 4-chain 反例的关系**还没厘清。K_n 是"n 个 a 两两 multi-N"，反例是
   几何 4 点链；用户在 wl054 讨论里指出"反例可能是孤立的 K_1 或不属于任何 K_n"，
   这个直觉在 K_8 数据下还没法验证（需要 K_n 节点集与已知反例搜索范围对接）。
4. **max_hyp=300k / 1M 全扫**会让 K_n 阶梯继续上升 —— K_8 在 100k 已经现身，
   推到 300k 大概率出现 K_9 / K_10。

## 文件

```text
scripts/partner_kn_subgraphs.py                   wl054 的图论枚举（被本次 supersede）
scripts/verify_kn_equivalence.py                  对 wl054 17 个 K_n 实例做 partner-k 反查
scripts/partner_pair_k_distribution.py            全扫所有 partner pair 拿 k 分布
results/partner_kn_subgraphs.jsonl                wl054 的 17 个 K_n 实例
results/partner_kn_subgraphs_summary.json
results/partner_pair_k_distribution.jsonl         10,533 partner pair 完整 k 列表
results/partner_pair_k_distribution_summary.json  分布 + top K_5+ 实例
docs/work-logs/055-kn-equivalence-and-partner-k-distribution.md   本文件
```
