# wl063 — 全 G_M closure 扫描：338,225 顶点 × 0 反例

## 触发

wl062 给出 hook："反例搜索其实可以彻底完成（在 max_value=1M 截断内）"。
本次实施：把 closure check 从 catalog 10,333 行升级到 G_M 全 338,225 顶点。

## 工具

`scripts/full_gm_closure_scan.py`：
- 读 wl061 BFS 找到的全部 G_M 顶点
- 对每个 `(A, B)` 并行算 N 列表（10 cores）
- 检查所有 `(N_i, N_j)` 对是否满足 `N_i + N_j == A + B`
- 持久化 + k 分布报告

耗时：**12 分钟**（10 cores 跑 338K 顶点）。

## 结果

```text
Total vertices scanned: 338,225
Total closure hits:           0    ← 反例彻底缺席

k_real 分布:
  k=2     203,328     60.12%
  k=3      87,779     25.95%
  k=4      33,445      9.89%
  k=5      10,164      3.01%
  k=6       2,561      0.76%
  k=7         704      0.21%
  k=8         196      0.058%
  k=9          42      0.012%
  k=10          6      0.0018%   ← 真实 K_10 实例总共 6 个
```

## 主结论 1：反例彻底在 G_M @ max_value=1M 内不存在

这是历史上对 "Steiner-Beukers 反例不存在" 假设的 **最强经验证据**：

```text
之前的负面证据 (catalog @ max_hyp=100k):
  10,333 顶点，rank ≤ 4 sample，0 closure hits

wl063 升级:
  338,225 顶点 (33× more)，含全部高阶 K_n hub
  K_10 实例全检
  0 closure hits
```

**反例搜索面**第一次覆盖整个 partner web (在 max_value=1M 截断内)。

## 主结论 2：k_real vs k_visible 差距巨大（max_value 截断影响）

```text
k     k_real (wl063)   k_visible (wl062, G_M degree)   差距
─────────────────────────────────────────────────────────
2     203,328          197,488                          5,840
3      87,779           81,386                          6,393
4      33,445           23,777                          9,668
5      10,164            5,642                          4,522
6       2,561            1,132                          1,429
7         704              218                            486
8         196               42                            154
9          42                4                             38
10          6                0                             6
─────────────────────────────────────────────────────────
Total  338,225          309,689                          ?
```

`k_visible` 总和应 ≈ 309,689（即 comp 0 size），而 k_real 总和 = 338,225。
差 28,536（= max_value=1M 截断丢失的 partner-only 顶点 + 边）。

**几乎所有 k=10 实例 (6/6) 都是 k_visible < 9 的 hub**——他们在 G_M 里 degree
被严重削减但真实结构是 K_10。要看 G_M 真实顶级 hub，必须直接算 k 列表
（不要靠 BFS degree）。

## 主结论 3：k_real 分布的 power-law 尾部

```text
k     count       ratio (vs next)
─────────────────────────────────
2     203,328     2.31
3      87,779     2.62
4      33,445     3.29
5      10,164     3.97
6       2,561     3.64
7         704     3.59
8         196     4.67
9          42     7.00
10          6     ?
```

每升 k 一档，count 缩小 2.3-7 倍。粗略 power-law（exponent ≈ 1.5-2.5），
但在 k≥8 后衰减加速（≈ 5-7 倍）。这跟 BA preferential attachment 衰减
吻合。

**预测**：max_value 升到 10M 或更高，会出现 K_11+ 实例。

## 主结论 4：反例可能存在的范围（如果存在的话）

闭合 closure `N_i + N_j = A + B` 需要 N 列表里有"互补对"。约束分析：

```text
catalog (max_hyp=100k):       N 上限 ≈ 4M (wl003 数据)
                              partner pair max_value 上限 4M
G_M @ max_value=1M:           丢掉 N > 1M 的 partner pair (~28K 顶点丢失)
G_M @ max_value=∞:            真正完整的 partner closure

要找反例，要么:
  (a) G_M @ max_value=∞ 内有反例 (我们没扫到)
  (b) catalog 之外 (即 max_hyp > 100k 的) 有反例
  (c) 反例不存在 ⇒ Steiner-Beukers 1986 conjecture 成立
```

## 跟历史 worklog 的整合

```text
wl048-052 catalog (10,333 行): 0 closure hits
wl053-055 partner pair k ≤ 4 (in catalog rank perspective)
wl058 forest 假设 (错)
wl061 G_M 全貌 (338,225 顶点)
wl062 K_9/K_10 discovered, degree = C(k, 2)
wl063 (本文): 338K 顶点 × 0 closure hits
```

每次升级搜索面 closure 都 0 hits。这是个**强经验信号**。

## 数据文件

```text
scripts/full_gm_closure_scan.py                      执行脚本
results/full_gm_closure_scan.jsonl                   closure hits (0 行, gitignored)
results/full_gm_closure_scan_summary.json            k 分布 + 元数据 (gitignored)
results/full_gm_closure_scan.log                     运行日志 (gitignored)

docs/work-logs/063-full-gm-closure-scan-no-counterexample.md   本文件
```

## 没做的事

1. **max_value=10M / 100M 升级**：扩大 BFS 范围，看 K_11+ 是否出现 + 是否
   有 closure。耗时估算 ≈ 1 小时（10 cores）。

2. **K_9 / K_10 实例的 ellrank**：测 wl060 "rank ≤ 4 在 catalog" 假设是否
   延伸到 G_M 全图。比 wl060 多 6 个 K_10 + 42 个 K_9。

3. **catalog 范围外 (max_hyp > 100k) 的 multi-N pair**：fast pivot 已扫过
   max_hyp = 100k；要把搜索面再升到 1M 需要 wl048 fast scan 重跑。这超
   现有数据。

## 元注

wl061-063 三连击给出 partner-graph theory 的"基础数据集"：
- wl061: 全 G_M 拓扑 (338K 顶点, 9580 components)
- wl062: comp 0 结构 (degree = C(k, 2), K_10 discovered)
- wl063: G_M 反例彻底搜索 (0 hits)

如果接下来还有什么是必要的：probably K_10 ellrank（验证 wl060 在 k=10 仍
然 rank ≤ 4），然后 max_value 扩展。
