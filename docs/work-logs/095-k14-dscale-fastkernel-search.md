# wl095 — K_14+ 搜索：D-scaling 瞄准 + 快速因子核精确数 k，rank ≤ 4 守到 K_16

## 触发

E.2（wl094）把 "rank ≤ 4" 假设从 k=6–8（wl060）延伸到 k=9–13（合计 70 hub，0 反例），
并在 E.2 section 留了一个钩子：

> 剩余钩子：跑全 primitive 库（854 个）看 K_14+。

用户进一步问：之前 wl093 那个"生成多-N pair 的算法特别快，能不能结合二者去操作"。
本 worklog 就是把两个工具**合并**成一条流水线，跑全库找 K_14+，并对新 hub 跑 ellrank。

## 两个工具，互补

| | 快速多-N 扫描 (wl093) | D-scaling 生成器 (wl085) |
|---|---|---|
| 方向 | 自底向上穷举 | 自顶向下构造 |
| 核心 | 枚举 A² 的因子对 (h−N)(h+N)=A² 拿整数 concordant N | PARI ellrank+ellratpoints 拿**有理** n 池，扫 d 看哪些有理 n 落成整数 |
| 强项 | 给定 (A,B) 精确、完备地数出整数 concordant N | 能构造范围外任意高 k（K_11/12/13 就这么来的） |
| 短板 | 受扫描范围限制（max_value=1M 内只到 K_10） | 每个 primitive 要跑 PARI；k_for_d 只是**下界**（有理池不完备） |

**关键观察**：D-scaling 的 `k_for_d` = 池中分母整除 d 的有理 n 个数，是真实整数
concordant 数的**下界**；而因子核对具体 (A,B) 给出的是**精确、完备**的整数 concordant
集合（枚举 A²/B² 的全部因子对，对 N 不设上界）。所以二者天然互补：

- **D-scaling 负责瞄准**：每个 primitive 跑一次 PARI 拿有理池，再用一个廉价的
  "分母除数筛"在 d∈[1,d_max] 上找出最可能产生高阶 hub 的若干 d（无需扫 (a,b)≤max_value）。
- **因子核负责精确数 k**：对每个瞄准到的 (A,B)=(d·a₀, d·b₀)，求
  `concordant_n_for_leg(A) ∩ concordant_n_for_leg(B)` 的真实大小，即认证的 hub 阶数 k。
- **ellrank 负责收尾**：只对确认的高阶 hub 跑 2-descent，复核 rank ≤ 4。

因为 A=d·a₀、B=d·b₀ 中 d、a₀、b₀ 都小，A、B 的素因子全小 —— 直接合并
（缓存的）d、a₀、b₀ 的因子分解即可，**不需要 Pollard-rho**。

## 实现

1. `src/rational_distance/concordant/fast_multi_n.py` 新增两个复用因子对逻辑的函数：
   - `concordant_n_for_leg(a, factor_items=None)`：给定 a 的全部正整数 N 使 a²+N²=□
     （穷举完备，对 N 无范围上界；可传入预算好的因子分解跳过试除）。
   - `exact_concordant_pair(a, b, ...)`：上者对 a、b 取交集 = (a,b) 的真实整数 concordant 集。
2. `scripts/multi_n/k14_search.py`（新）：合并流水线 CLI。
   - 对每个 primitive：`enumerate_rational_n` 拿有理池 → 分母除数筛挑 top-d →
     对每个候选 d 用因子核精确数 k → 取该 primitive 的最大 k hub。
   - 输出每 primitive 一行 JSONL + 控制台 ladder（各 k 的最小坐标 hub）。

正确性验证：
- `exact_concordant_pair` 在 wl085 已知 K_13 hub (458640, 4989600) 上精确复现 13 个 N；
- 新增 4 个 pytest，把它与 brute force 及仓库现成的 `find_concordant_by_factorization`
  对齐（含一个坐标 ~10⁸ 的放大 K_14 hub）。

运行：

```bash
PARI_MT_ENGINE=single uv run python scripts/multi_n/k14_search.py \
    --d-max 50000 --top-d 64 --out results/multi_n/k14_search.jsonl
```

854 个 primitive 共 ~628s（单核；瓶颈是每 primitive 一次 PARI ellrank+ratpoints）。

## 结果

**可达 hub 阶数（d_max=50000 内）随 primitive rank 单调走**：

| primitive rank | #primitive | 该 rank 最大可达 k |
|---|---|---|
| 1 | 216 | K_5 |
| 2 | 412 | K_8 |
| 3 | 206 | K_11 |
| 4 | 20 | **K_16** |

best_k 分布：`{3:267, 4:187, 5:162, 6:120, 7:50, 8:32, 9:9, 10:2, 11:4, 12:3, 13:1, 16:1}`
（另有 16 个 primitive 因有理池为空或分母全 > d_max 未产出）。

**K_14+ 确实出现**：在 d_max=50000 内，恰有一个 catalog primitive 越过 K_14——
`(2975, 7904)`（rank 4，有理池 728）在 d=27720 处给出

```
K_16 hub: (a, b) = (82467000, 219098880)
16 个 concordant N，全部满足 N²+a²=□ 且 N²+b²=□
```

> 注：K_14+ 的"出现"本质是构造性的——任何 rank ≥ 1 的 primitive 有理池足够大，
> d 取得够大（更多分母的公倍数）就能机械地拔高 k。d_max 是坐标预算，不是数学上界。
> 真正有信息量的结论是：(a) 可达 k 与 primitive rank 强相关；(b) rank 守住。

**ellrank 复核（9 个 k≥11 hub，含 K_16）全部通过**：

| k | (a, b) | rank | ==primitive? | certified |
|---|---|---|---|---|
| 16 | (82467000, 219098880) | 4 | ✓ | ✓ |
| 13 | (50139936, 114760800) | 4 | ✓ | ✓ |
| 12 | (25322220, 76003200) 等 3 个 | 4 | ✓ | ✓ |
| 11 | (277200, 1009008) 等 4 个 | 3 | ✓ | ✓ |

全部 rank ≤ 4、sha2[2]=0、`lower==upper` certified，且放大 hub 的 rank 精确等于
其 primitive rank —— 在 k=16 处再次从算术上验证 D-scaling 的 rank 不变性
(E_{a₀,b₀} ≅ E_{d·a₀,d·b₀} over ℚ，wl065/wl085)。

## 结论

- "rank ≤ 4" 假设现已从 k=6 一路验证到 **k=16**，无一例外。
- 可达 hub 阶数 = primitive rank 的函数（rank↑ → 有理池↑ → 可达 k↑），与 wl086
  "Q_N 坐标矩阵秩亏 = rank deficit" 图像一致。
- 合并流水线（D-scaling 瞄准 + 因子核精确数 k）比单用任一工具都强：比纯 D-scaling
  的 k_for_d 多了**完备精确**的整数计数，比纯快速扫描多了**范围外构造**能力。

## 产物

- `scripts/multi_n/k14_search.py`（新流水线 CLI）
- `src/rational_distance/concordant/fast_multi_n.py`：`concordant_n_for_leg` /
  `exact_concordant_pair`
- `tests/test_fast_multi_n.py`：+4 测试
- `results/multi_n/k14_search.jsonl`（854 行）、`k14_search_ladder.json`、
  `k14_ellrank.jsonl`（9 个高阶 hub 认证）、`k14_search_run.log`

## 剩余钩子

- 对 rank=4 hub 找共同 2-descent 像（跨 hub closure 障碍）——已被 A.1 negative 关闭。
- 若要给 paper 补"K_n 阶梯"图，可调大 d_max 把 ladder 顶端继续往上推（机械，无新结论）。
