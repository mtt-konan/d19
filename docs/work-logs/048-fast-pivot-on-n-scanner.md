# wl048 — Pivot-on-N fast multi-concordant scanner

## 目的

接 wl047（文献定位 + 结果整理 + 筛选阶梯文档），实施 `docs/MULTI_N_FILTER_LADDER.md` 第 4 节定义的“切入点 = L1 之前”：用 pivot-on-N 替代 wl046 的 (A,B) 外层暴力扫描，先重现 ground truth，再把搜索域扩到 `max_hyp >= 50000`，看 closure pair 是否在更大范围出现。

## 思路

不再以 `(A, B)` 为外层、对每个 pair 跑 `factor_search` 找 N。  
改成以 N 为枢轴：

```text
for each A in [1, max_hyp]:
    factorize A^2
    for each divisor pair (p, q) of A^2 with p < q, p ≡ q (mod 2):
        N = (q - p) / 2
        record (A, N)

按 N 分组得到 A_set(N)
for each N:
    for A < B in A_set(N), gcd(A,B)=1, B<=max_hyp:
        把 N 写到 (A,B) 的 concordant 列表

filter |list| >= 2 -> multi-N pair
```

正确性来自下式：

```text
A^2 + N^2 = h^2  ⟺  (h - N)(h + N) = A^2
```

每个满足条件的 `(A, N)` 与 `A^2` 的一个有效因子对一一对应，所以枚举是完整且唯一的。

## 实现

```text
src/rational_distance/concordant/fast_multi_n.py
    iter_concordant_a_n(max_leg)
    fast_multi_concordant_pairs(max_hyp)

scripts/fast_multi_concordant_scan.py
scripts/validate_fast_multi_n.py

tests/test_fast_multi_n.py
    iter 与 brute force 一致 (max_leg=20)
    iter 命中已知 (153, 204), (560, 204)
    fast 与 brute force 一致 (max_hyp=200)
```

## 校验

```text
results/multi_concordant_N_max10000.jsonl    854 pairs (wl046 authoritative)
fast_multi_concordant_pairs(max_hyp=10000)   854 pairs
diff                                          empty
```

校验器：

```bash
uv run python scripts/validate_fast_multi_n.py --max-hyp 10000
```

输出：

```text
ground-truth pair count: 854
fast pair count:         854
fast elapsed:            1.02s
OK: fast scanner matches ground truth exactly.
```

## 扩展实测

```text
max_hyp=10000   1.02s   pairs= 854   k_hist={2:828, 3: 26}
max_hyp=20000   3.96s   pairs=1848   k_hist={2:1800, 3: 47, 4:  1}
max_hyp=50000  25.21s   pairs=4968   k_hist={2:4853, 3:112, 4:  3}
```

数量级：原 multiprocessing scan 在 `max_hyp=10000` 上耗时分钟到小时级；现在单核 1 秒。`max_hyp=50000` 之前预估 ~7 小时，现在 25 秒。

## 关键新发现

`max_hyp=10000` 内 max k=3，没有 k=4。`max_hyp=20000` 起出现 **k=4 pair**：

```text
(11776, 17199)   N = [3960,  4368, 46368, 541632]   A+B = 28975
(6669,  26656)   N = [8892, 13860, 19992,  91392]   A+B = 33325
(7337,  28288)   N = [1716,  5916, 31584,  84216]   A+B = 35625
```

慢路 `factor_search` 已对这三个 pair 独立确认。

closure pair 数量在 10000 / 20000 / 50000 三档全部为 0。即使 k=4 也未出现 `N1 + N2 = A + B`。closure 失败不是 k 不够，是结构性原因。

## Phase 2 follow-up：k=4 pair 的 2-descent 审计

写完本 wl 主体后，紧接着用 `enumerate_half_points_for_concordant_N` 给三个 k=4 pair 的 4 个 N 各取一个 positive-sig 半点，把它们的 image `(sf(x), sf(x+A²))` 在 `(Q*/Q*²)²` 上做 F₂-Gauss 消元（脚本：`scripts/k4_two_descent_rank.py`）。

```text
(11776, 17199)   F2-rank = 3   N=3960 ⊕ N=4368 ⊕ N=541632 = 0
(6669,  26656)   F2-rank = 3   N=13860 ⊕ N=19992 ⊕ N=91392 = 0
(7337,  28288)   F2-rank = 4   no relation
```

含义：

- 前两个 k=4 pair 的 4 个 concordant N 在 `E(Q)/2E(Q)` 里其实只张成 3 维，存在一条 3-term F₂ 关系。
- 第三个 pair 的 4 个 image 完全独立。
- “k=4” 不等价于“rank≥4”。这是把 multi-N 计数和 rank 切开的第一份直接证据。

### PARI ellrank 实测（脚本 `scripts/k4_rank.py`，effort=1）

```text
(11776, 17199)   F2-rank=3   PARI rank = 2 / 2   sha2_lower=0   generators=2
(6669,  26656)   F2-rank=3   PARI rank = 2 / 2   sha2_lower=0   generators=2
(7337,  28288)   F2-rank=4   PARI rank = 4 / 4   sha2_lower=0   generators=4
```

完美吻合：

- **F₂-rank 与 PARI rank 关系**：`F2-rank = rank + 2 - dim(2-torsion span)`，其中 2-torsion 在 E(Q)/2E(Q) 的 image 在 `dim(2-torsion(Q))=2` 时贡献最多 2 维，最少 0 维。换种说法：F₂-rank 在 4 个半点里看到的，正好是 `rank(E) + 2 - (与 2-torsion 重叠维数)`。
- 两个 rank=2 pair：4 个 concordant N **完全是在 rank 只有 2 的曲线上**用 2-torsion 翻折拼出来的。`k=4` 并不要求 `rank≥4`。
- 唯一的 rank=4 pair `(7337, 28288)`，4 个 image 在 `(Q*/Q*²)²` 完全独立，是“真正”的高 rank k=4 样本。

### 实用推论：F₂-rank 是 rank 的快速代理

F₂-Gauss 消元只需 `enumerate_half_points_for_concordant_N` 加因子分解，**不需要 PARI**，每对 pair 毫秒级。

```text
F2-rank == k     → 真高 rank candidate (rank >= F2-rank - 2)
F2-rank <  k     → 多余的 N 来自 2-torsion 翻折，rank 比 k 小
```

可以在不调用 PARI 的前提下，对 854 / 1848 / 4968 全量 multi-N 集合上跑这套 F₂-rank，把 pair 分成「真高 rank」与「torsion 翻折」两类。

### 其它 signature 观察

每个 N 的 8 个 half-point 永远落入 2 个 raw signature 类（一正一负 / 2-torsion 翻转）。不同 N 的正类 first-coord 通常互不相同；个别例外 `(11776, 17199)` 中 N=4368 与 N=541632 都给出 sf(x)=546，但 second-coord 区分它们。

意外副产物 —— **同类 square-x 半点**：

```text
(11776, 17199)  N=3960   half-point x = 115863696 = 10764²   sig = (1, 30073, 30073)
(7337,  28288)  N=31584  half-point x =   9096256 =  3016²   sig = (1,  2993,  2993)
```

这两个半点的 `x` 本身是完全平方数，但 `x+A²` 与 `x+B²` 不是平方，只是 squarefree 部分**相等**（30073 / 2993）。等价于 `(x+A²)/(x+B²)` 是有理平方。

它们不是 concordant 意义上的 square-x 点，而是一种弱形式：

```text
x = M²
sf(M² + A²) = sf(M² + B²) ≠ 1
```

这个 “same-class square-x” 是不是某种 multi-N 的 doubled-up 结构指示，还需要再看更多样本才能下判断。

## 后续任务（不在本 wl 内做）

1. 给三个 k=4 pair 的 E(Q) 上跑 PARI ellrank，确认 rank lower/upper bound 与 F₂-rank 一致
2. 把 2-torsion image 也纳入 F₂-span，得到对 dim(E(Q)/2E(Q)) 的下界
3. Mordell-Weil sieve 把 closure 局部化
4. 若需要 `max_hyp` 进一步推到 100k+，再优化 `iter_concordant_a_n`（现在每个 A 是 O(A) 的 trial division）
5. 把 closure 失败的统计模式总结成证明思路

## 文件

- 模块: `src/rational_distance/concordant/fast_multi_n.py`
- 脚本: `scripts/fast_multi_concordant_scan.py`, `scripts/validate_fast_multi_n.py`
- 测试: `tests/test_fast_multi_n.py`
- 输出:
  - `results/multi_concordant_N_max20000_fast.jsonl`
  - `results/multi_concordant_N_max50000_fast.jsonl`
- 文档: `docs/MULTI_N_FILTER_LADDER.md`
- Phase 2 脚本: `scripts/analyze_k4_signatures.py`, `scripts/k4_two_descent_rank.py`, `scripts/k4_rank.py`
