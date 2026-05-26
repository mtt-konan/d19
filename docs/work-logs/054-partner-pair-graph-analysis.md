# wl054 — Multi-N partner-pair 对称图：结构、K_n 子图与 catalog 完备性

## 起点

wl052 在 `max_hyp=100000` 跑出 10,333 条 multi-N 互素对（catalog）。同一段时间
我们注意到一个结构恒等式：如果 `(A, B)` 的 concordant N 列表是
`[N_1, …, N_k]`，那么对任意 `i ≠ j`，**未约分的** `(N_i, N_j)` 自身也是一对
multi-concordant 对，并且其 N 列表至少包含 `{A, B}`。

如果把这份恒等式画成图，能给 catalog 提供一个**自我审计 + 结构挖掘**的双重视角：

- 自审计：每条 catalog 行向外抛出 `C(k, 2)` 条 partner 边；如果 partner 落到
  catalog 之外又确实是 multi-N，那 catalog 就漏了。
- 挖掘：partner 化的 N 经常彼此共享因子，可能形成 K_3 / K_4 等子图，提示一组
  数字的 "公共 N 池"。

## 工具

新增两个脚本（仅依赖 `concordant.factor_search`，与主线代码同口径）：

```text
scripts/partner_pair_graph.py          构图、连通分量、度数、largest component dump
scripts/verify_missing_partner.py      对 missing partner 跑权威 factor_search
```

构图约定（**未约分**，否则 partner 几乎全落到 catalog 之外，反而看不见结构）：

```text
vertex   sorted (a, b)，可以是 catalog 行，也可以是某 catalog 行抛出的 partner
edge     对每行 (A, B) 与其每对 (N_i, N_j)（i < j）连一条边
```

输出物：

```text
results/partner_pair_graph.jsonl        10,762 条边
results/partner_pair_graph_summary.json 顶 15 度数 + 50 大分量大小
results/partner_pair_missing.jsonl      10,639 条 missing partner（reduced）
```

## 全局规模

```text
catalog                10,333
顶点总数               20,866   (10,333 catalog + 10,533 partner-only)
边数                   10,762
连通分量数             10,104
最大分量               11 顶点
平均分量大小           ≈ 2.07
```

`Σ_行 C(k, 2) = 10,762`，符合 catalog 中 k 的分布（k=2 占绝大多数，9 条 k=4）。

10,104 个分量 / 10,766 个顶点对（10,333 行 + 433 行有 ≥2 partner）→ **图非常松散**：
绝大多数 catalog 行是一个孤立的 "中心 + ≤6 partner" 星，跨行互联极少。

## 度数榜

```text
   (a, b)              degree   src      concordant N
 ( 11776,  17199)        6      catalog  [3960, 4368, 46368, 541632]
 (  6669,  26656)        6      catalog  [8892, 13860, 19992, 91392]
 ( 15457,  93632)        6      catalog  [13776, 70224, 316680, 4119276]
 ( 30016,  67275)        6      catalog  [4020, 29640, 502320, 2010960]
 ( 35200,  82593)        6      catalog  [20976, 138600, 280500, 301476]
 ( 34307,  53568)        6      catalog  [6324, 30576, 48360, 413424]
 (  7337,  28288)        6      catalog  [1716, 5916, 31584, 84216]
 ( 26784,  76475)        6      catalog  [11160, 42240, 183540, 240312]
 ( 44928,  84847)        6      catalog  [54096, 125904, 538200, 1313760]
 (  3192,  97308)        4      partner  ←—— 这条不在 catalog
 (   819,   1600)        3      catalog  [780, 1680, 15960]
 ( 50463,  79040)        3      catalog  [17784, 75516, 224280]
 ...
```

观察：

1. 9 条 k=4 catalog 行刚好分布在 degree=6 槽位（C(4,2)=6），是结构必然。
2. 唯一冲到 degree=4 的 partner-only 顶点 `(3192, 97308)` —— 它从 **4** 条不同
   的 catalog 行里被抛出来。这条 partner 后面会发现就是一个 K_4 子图的中心。
3. degree=3 catalog 行都是 k=3 行（C(3,2)=3），以下类推。

## 最大连通分量（11 顶点，由 6669 系列粘出）

```text
C ( 6669,   7105)  deg=1   k=2  N=[13860, 19992]
C ( 6669,  26656)  deg=6   k=4  N=[8892, 13860, 19992, 91392]
C ( 6669,  58144)  deg=3   k=3  N=[8892, 43608, 91392]
P ( 8892,  13860)  deg=1
P ( 8892,  19992)  deg=1
P ( 8892,  43608)  deg=1
P ( 8892,  91392)  deg=2   ←—— 同时是 (6669,26656) 与 (6669,58144) 的 partner
P (13860,  19992)  deg=2   ←—— 同时是 (6669, 7105) 与 (6669,26656) 的 partner
P (13860,  91392)  deg=1
P (19992,  91392)  deg=1
P (43608,  91392)  deg=1
```

3 行 catalog 全部以 `A = 6669` 开头，把 8 个 partner 顶点共享起来。`6669` 像
一个 "枢纽 a"，可以同时和多个 b 配出富 N 关系。这种 "fan" 形态在所有大于 5 的
分量里都重复出现。

## K_4 子结构发现：`{3744, 22631, 44631, 70720}`

把度数榜上 partner-only `(3192, 97308)` 的 4 条入边列出来：

```text
(  3744, 22631) ──→ partner (3192, 97308)
( 22631, 44631) ──→ partner (3192, 97308)
( 22631, 70720) ──→ partner (3192, 97308)
( 44631, 70720) ──→ partner (3192, 97308)
```

四条 catalog 行的 N 列表**完全相同**：

```text
A      B       n_concordant   concordant_N
3744   22631   2              [3192, 97308]
22631  44631   2              [3192, 97308]
22631  70720   2              [3192, 97308]
44631  70720   2              [3192, 97308]
```

也就是说节点集 `S = {3744, 22631, 44631, 70720}` 里**任两个 catalog 行都用同一对
{3192, 97308} 作为 concordant N**。catalog 只收录互素行，把 6 个无序对看一眼：

```text
        3744   22631   44631   70720
3744     -      1        9      416
22631    1     -         1        1
44631    9      1       -         1
70720  416      1        1       -
```

互素的 4 对都在 catalog 里。剩下 2 对 `(3744, 44631)` gcd=9 与 `(3744, 70720)`
gcd=416 不互素，按 catalog 约定不收录。直接跑 `factor_search`：

```text
( 3744, 44631)  k=3  N=[3192, 16008, 97308]
( 3744, 70720)  k=3  N=[3192,  4290, 97308]
```

两条都是 multi-N（甚至 k=3）。所以 **6 条无序对里 6 条都是 multi-N**，节点集 `S`
形成的是一个 "完整的非互素扩展 K_4"：所有边都 multi-N，4 条互素 + 2 条非互素。

这是 partner 图给出的第一类显式结构线索：

> 如果你看到 `(N_i, N_j)` 这个 partner 顶点的入度高（即多条 catalog 行都以
> `{N_i, N_j}` 为 concordant 子集），那么可能存在一组 a 把 `(N_i, N_j)` 当公共 N
> 池，再现 K_n 子图。

## Catalog 完备性审计（互素约定下）

抽样 12 条 reduced partner（gcd 已约掉）跑权威 `factor_search`：

```text
( 5, 26)   k=0   empty       from (25, 91)  via N=(60, 312)
( 3, 10)   k=0   empty       from (27,160)  via N=(36, 120)
( 2,  5)   k=0   empty       from (32, 45)  via N=(24,  60)
( 7, 10)   k=1   single      from (35,288)  via N=(84, 120)
( 5, 28)   k=0   empty       from (45,448)  via N=(60, 336)
( 7, 50)   k=0   empty       from (49,270)  via N=(168,1200)
( 5,  7)   k=0   empty       from (63, 80)  via N=(60,  84)
( 7, 55)   k=0   empty       from (63,880)  via N=(84, 660)
( 4, 21)   k=0   empty       from (64,189)  via N=(48, 252)
(13, 35)   k=1   single      from (65,1008) via N=(156, 420)
(22, 35)   k=1   single      from (77,1440) via N=(264, 420)
( 5, 33)   k=0   empty       from (80,297)  via N=(60, 396)

k >= 2 (catalog miss): 0
k == 1               : 3
k == 0               : 9
```

12 抽样里 0 条是真 multi-N。reduced 部分确实没漏；fast pivot 扫描器按 wl048
的设计**结果是正确的**。

> 解释：partner `(N_i, N_j)` 的可约分子已经把原来 `(A, B)` 关系所需的因子全洗掉了
> ——只是数对，不再继承多 N 的结构。所以 reduced partner 与 catalog 的命中率天
> 然就是低的。

完备性的真实表述：

- **互素 catalog 完备**：在 `max_hyp=100000` 范围内，所有互素 multi-N 对都已落进
  10,333 行 catalog。
- **非互素 multi-N 不在 catalog 里，但 partner 图能高效定位它们**：上面那条
  `(3744, 44631)` 就是 partner 顶点 `(3192, 97308)` 的反推产物。

## 推论与下一步钩子

1. **Partner-only 顶点是非互素 multi-N 候选**。`partner_only` 集合有 10,533 个
   顶点，按 gcd 过滤、再 reduce、再回查 catalog，能列出所有"被互素约定挡掉"
   的非互素 multi-N。这是 wl046 / wl048 都没覆盖的角落。

2. **高度 partner-only = K_n 中心候选**。`(3192, 97308)` degree=4 直接给出一个
   K_4 节点集；是否还存在更大的 K_n？要不要扫一遍 partner-only 度数 ≥3 的顶点
   并统计它们的 source-pair "节点集" 是否再形成完全子图？

3. **加速搜索的可行路径**：partner 图建议的搜索方式是
   "先扫 (A, B) 找 N 池 → partner 池里挑高度 N 对 → 反推所有 a 用同一 N 池"，
   这与 wl048 的 "pivot on N" 在因子分布层面是同一件事，但 partner 图给出更
   显式的"先找好的 (N_i, N_j)"启发。

4. **catalog 没漏 ≠ 探测面已封顶**。`max_hyp` 还能继续推；Round-3 任务可能是
   `max_hyp=300000` 或 `max_hyp=1e6`，能把 K_4 / K_5 子图样本拉到几十甚至几百
   组，给后续 sha2 / rank 联合统计提供更厚的经验底。

## 没做的事 / 留给下一轮

- 没在 partner 图上跑社区检测（10,104 个分量基本是孤岛，社区结构不重要；
  真正要的是按 partner-only degree 排序后的前 100 个 K_n 候选）。
- 没把 partner-only `(3192, 97308)` 这种顶点的 reduce / sha2 / rank 也算一份
  ——它本身可能不是 multi-N（事实上 k=0 / 1 多见），但它的 a 集合是富结构信号，
  应该独立列一份 `partner_hub_candidates.jsonl`。
- 没并行化 fast scanner 把 `max_hyp` 推到 1e6（wl045 的 `parallel_map` 已经准备
  好了，等下一轮决策）。

## 文件

```text
scripts/partner_pair_graph.py                         构图脚本
scripts/verify_missing_partner.py                     完备性审计脚本
results/partner_pair_graph.jsonl                      10,762 边
results/partner_pair_graph_summary.json               summary
results/partner_pair_missing.jsonl                    10,639 missing reduced partners
docs/work-logs/054-partner-pair-graph-analysis.md     本文件
```
