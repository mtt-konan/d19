# wl052 — max_hyp=100000 scan + 全量 F₂-rank/PARI 审计

## 目的

接 wl048-051：在 `max_hyp=100000` 上重跑 pivot-on-N、F₂-rank 分类、PARI ellrank 审计，
看更大尺度下：
1. 多少 multi-N pair
2. F₂-rank=4 saturated 的比例是不是仍然稀有
3. 是否会出现 k=5 或更高的 saturated pair
4. closure 是不是仍然全部失败

## 工程量

```text
pivot-on-N (fast scanner)            99.0s  ->  10333 multi-N pair
F₂-rank classifier                    2.1s  ->  190 个 F₂-rank ≥ 3 candidates
PARI ellrank (effort=1) × 190        2.1s  ->  全部 certified
                                     ---
total                               ~100s
```

可对比：max_hyp=50000 之前 PARI 步骤 ~1.2s，现在 ~2.1s（线性）。

## F₂-rank 分布对比

```text
max_hyp     pairs   F₂=2          F₂=3          F₂=4
10000        854    829 (97.1%)    25 (2.9%)     0
20000       1848   1803 (97.6%)    45 (2.4%)     1 (0.05%)
50000       4968   4858 (97.8%)   109 (2.2%)     1 (0.02%)
100000     10333  10143 (98.2%)   184 (1.8%)     6 (0.06%)
```

跨尺度规律：

- `F₂-rank=2`：占比 ~98%，慢增
- `F₂-rank=3`：占比缓降（从 2.9% 到 1.8%）
- `F₂-rank=4`：从 1 跳到 6，**密度上升**（0.06%）

## 联合 (k, F₂-rank) 分布（max_hyp=100k）

```text
k=2  F₂=2: 10132
k=3  F₂=2:    11
k=3  F₂=3:   181    ←
k=4  F₂=3:     3
k=4  F₂=4:     6    ←  五个新的 saturated k=4 pair
```

**6 个 saturated k=4 pair**（vs max_hyp=50000 的 1 个）：

```text
(  7337, 28288)   N = [1716,  5916,  31584,  84216]     A+B=  35625   (已知)
( 15457, 93632)   N = [13776, 70224, 316680, 4119276]   A+B= 109089   新
( 26784, 76475)   N = [11160, 42240, 183540, 240312]    A+B= 103259   新
( 30016, 67275)   N = [4020,  29640, 502320, 2010960]   A+B=  97291   新
( 34307, 53568)   N = [6324,  30576, 48360,  413424]    A+B=  87875   新
( 44928, 84847)   N = [54096, 125904, 538200, 1313760]  A+B= 129775   新
```

仍然没有 `k ≥ 5` saturated pair。

## PARI ellrank 实测分布（190 个 F₂-rank ≥ 3 候选）

```text
rank=2:  63   ( 33.2%)
rank=3:  93   ( 48.9%)
rank=4:  31   ( 16.3%)
rank=5:   3   (  1.6%)
```

**rank=5 pair**（全部 k=3 F₂-rank=3 deficient，PARI 揭示真 rank=5）：

```text
(26163, 59455)   N = [...]    新
(27328, 44055)   N = [23496, 51240, 102396]   A+B = 71383   (wl050 已知)
(40273, 58240)   N = [...]    新
```

`sha2_lower ≥ 2`：2 个（vs 50k 的 1 个）。

## Closure 距离审计（rank ≥ 4 的 34 个）

按最小 pairwise-sum 差值排序，前 10：

```text
  diff       A      B    rk    k     A+B       N (前 3 个)
   113    1845   2912   4/4    3    4757    [2184, 2460, 37800]
   205   25024  35035   4/4    3   60059    [10032, 50232, 142800]
   839    7808  81567   4/4    3   89375    [29256, 59280, 118944]
  1561   15939  46400   4/4    3   62339    [15180, 48720, 672000]
  1841    7975  19584   4/4    3   27559    [1188, 6960, 22440]
  1875    7337  28288   4/4    4   35625    [1716, 5916, 31584, 84216]
  2849    1440   3367   4/4    3    4807    [3456, 4200, 8580]
  3353   27328  44055   5/5    3   71383    [23496, 51240, 102396]
  5869    6409  25200   4/4    3   31609    [1740, 24000, 92820]
  7137    5075  11968   4/4    3   17043    [9900, 14280, 73500]
```

**(1845, 2912) 仍然是最接近 closure 的 pair（diff = 113）**。
新发现 `(25024, 35035)` 是第二接近，diff = 205。

所有 34 个 rank ≥ 4 candidate 的 closure 检查仍然全部失败 —— 这与 wl050 的结论一致。

## 关键含义

### 数量趋势

- `F₂-rank=4 saturated` 数量：50k 的 1 个 → 100k 的 6 个 (~6 倍)
- `rank=5` 数量：50k 的 1 个 → 100k 的 3 个 (~3 倍)
- `rank ≥ 4` 数量：50k 的 13 个 → 100k 的 34 个 (~2.6 倍)

`max_hyp` 翻倍，rank ≥ 4 candidate 约翻 ~2.6 倍。**子线性增长**。

外推到 `max_hyp=200k` 估计 ~80 个 rank≥4 candidate；要找到 saturated k=5（rank ≥ 3） 还得等到 `max_hyp` 在 500k–1M 量级，且即便找到也不一定有 closure。

### Closure 仍然结构性失败

10333 个 multi-N pair 里 closure_pairs=0。即使 rank=5 也没出现 closure。

`(1845, 2912)` 的差只有 113 但已经穷尽了所有 concordant N（factor_search 是穷尽算法）。**这个 pair 真的 closure 失败**，113 只是算术巧合，不是高度截断造成。

### 下一步该看哪儿

- 三个 rank=5 pair 是结构最丰富的样本，值得做 Mordell-Weil generator 的完整审计
- `(1845, 2912)`, `(25024, 35035)` 的 113/205 距离是不是有 mod p² 解释？
- 是否所有 closure 失败都能局部 (mod p²) 解释？

## 文件

```text
results/multi_concordant_N_max100000_fast.jsonl              新, 10333 行
results/multi_concordant_N_max100000_classified.jsonl        新, 10333 行
results/multi_concordant_N_max100000_pari_rank.jsonl         新, 190 行
src/rational_distance/results/catalog.py                     register 三个新 artifact
docs/work-logs/052-max-hyp-100k-scan-and-rank-audit.md       本文件
```

## 复现

```bash
uv run python scripts/fast_multi_concordant_scan.py \
    --max-hyp 100000 \
    --out results/multi_concordant_N_max100000_fast.jsonl

uv run python scripts/classify_multi_n_by_f2_rank.py \
    --in  results/multi_concordant_N_max100000_fast.jsonl \
    --out results/multi_concordant_N_max100000_classified.jsonl

uv run python scripts/pari_rank_high_f2.py \
    --in  results/multi_concordant_N_max100000_classified.jsonl \
    --out results/multi_concordant_N_max100000_pari_rank.jsonl
```
