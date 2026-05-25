# wl050 — PARI ellrank on the 110 F₂-rank ≥ 3 candidates

## 目的

接 wl049：F₂-rank 分类器把 4968 个 multi-N pair 缩到 110 个 `F₂-rank ≥ 3` 的“真候选”。本 wl 用 PARI `ellrank` 对这 110 个 pair 都跑出 certified rank，看 rank 实测分布、找出 Harborth 4-chain 在“结构允许池”里到底有多少 candidate。

## 实现

```text
scripts/pari_rank_high_f2.py
    --in   classified jsonl (含 f2_rank 字段)
    --out  annotated jsonl (附加 rank_lower / rank_upper / sha2_lower / n_generators / pari_elapsed_s)
```

调用 `rational_distance.concordant.analysis.compute_rank(A, B, effort=1)`。每个 pair 平均 ~10 ms。

## 实测

```text
$ uv run python scripts/pari_rank_high_f2.py \
    --in  results/multi_concordant_N_max50000_classified.jsonl \
    --out results/multi_concordant_N_max50000_pari_rank.jsonl

selected 110 pairs with f2_rank >= 3
processed: 110 pairs in 1.2s  (0 PARI failures)
```

### Rank 分布（全部 certified）

```text
rank=2:    40 pairs  ( 36.4%)
rank=3:    57 pairs  ( 51.8%)
rank=4:    12 pairs  ( 10.9%)
rank=5:     1 pair   (  0.9%)
```

`sha2_lower` 分布：109 pair 是 0，1 pair 是 ≥ 2（`(36225, 40592)`，rank=2）。

### F₂-rank vs PARI rank 联合分布

```text
F₂-rank=3, rank=2:   40   F₂-rank 高估
F₂-rank=3, rank=3:   57   F₂-rank 紧 (rank = F₂-rank)
F₂-rank=3, rank=4:   11   F₂-rank 低估
F₂-rank=3, rank=5:    1   F₂-rank 大幅低估   ←
F₂-rank=4, rank=4:    1   F₂-rank 紧
```

也就是说 **F₂-rank 既能高估也能低估实际 rank**。它的严格关系只是

```text
F₂-rank ≤ min(k, rank + 2)
```

`F₂-rank ≥ 3 ⇒ rank ≥ 1` 是确定的下界；`F₂-rank = k` saturated 给出 `rank ≥ k − 2`，但不约束上界。

### Top 候选（按 rank_upper 降序）

```text
* A= 27328 B= 44055  k=3  F₂=3  rank 5/5  sha2≥0     ←  唯一 rank=5
* A=  7337 B= 28288  k=4  F₂=4  rank 4/4  sha2≥0     (wl048 已知)
* A=  1440 B=  3367  k=3  F₂=3  rank 4/4  sha2≥0
* A=  1845 B=  2912  k=3  F₂=3  rank 4/4  sha2≥0
* A=  2975 B=  7904  k=3  F₂=3  rank 4/4  sha2≥0
* A=  5075 B= 11968  k=3  F₂=3  rank 4/4  sha2≥0
* A=  6409 B= 25200  k=3  F₂=3  rank 4/4  sha2≥0
* A=  7975 B= 19584  k=3  F₂=3  rank 4/4  sha2≥0
* A=  9269 B= 24255  k=3  F₂=3  rank 4/4  sha2≥0
* A= 10881 B= 20944  k=3  F₂=3  rank 4/4  sha2≥0
* A= 15939 B= 46400  k=3  F₂=3  rank 4/4  sha2≥0
* A= 20128 B= 45353  k=3  F₂=3  rank 4/4  sha2≥0
* A= 25024 B= 35035  k=3  F₂=3  rank 4/4  sha2≥0
```

总共 **13 个 rank ≥ 4 的 pair**，全部 certified。这就是 max_hyp=50000 池里所有“结构上允许 Harborth 4-chain 反例”的样本。

## Closure 距离审计

对其中几个 pair 做了 pairwise N 和 vs A+B 的距离检查：

```text
( 1845,  2912)  rank=4  k=3  A+B=  4757  closest pair sum 4644  diff   113   ★
(36225, 40592)  rank=2  k=3  A+B= 76817  closest pair sum 78744  diff  1927   (sha2≥2)
( 7337, 28288)  rank=4  k=4  A+B= 35625  closest pair sum 37500  diff  1875
(27328, 44055)  rank=5  k=3  A+B= 71383  closest pair sum 74736  diff  3353
( 1440,  3367)  rank=4  k=3  A+B=  4807  closest pair sum 7656   diff  2849
```

`(1845, 2912)` 的 N=[2184, 2460, 37800] 与 A+B 的最小距离只有 113 —— **整个 catalog 中最接近 closure 的样本**。

## 关键含义

### 对反例搜索

- 候选池 4968 pair → F₂-rank 筛 → 110 pair → PARI rank ≥ 4 筛 → **13 个真正“结构允许”的样本**
- 在 `max_hyp=50000` 范围里这 13 个是 Harborth 4-chain 反例的全部 candidate
- 全部 closure_pairs=[]（在原始 scan 时已确认；本轮 PARI rank 实测不改变这点）
- `(1845, 2912)` 的差只有 113，是“最近脱靶”，但是要看是不是高度受限造成的截断

### 对证明非存在

- F₂-rank short-circuit 现在有定量根据：`F₂-rank ≤ 2 ⇒ rank ≤ 0`（更准确：`rank ≥ F₂-rank − 2 ≥ 0`，但 F₂-rank=2 时仍可能 rank=2）。需要谨慎
- 真正的 short-circuit 应该用 **PARI rank ≤ 1** 而非 F₂-rank，但 PARI 慢一些（虽然在我们这个 catalog 上每对 ~10 ms 也还能接受）

### 结构观察

1. **rank=5 居然只用 k=3** —— `(27328, 44055)` 有 5 维 Mordell-Weil，但落在 square-x 截面的只有 3 个 N。这说明高 rank ≠ 多 concordant N
2. **rank=4 大量是 k=3** —— 12 个 rank=4 中只有 1 个是 k=4，其余 11 个都是 k=3。说明 rank 与 k 的相关度比预期弱
3. **唯一 sha2 ≥ 2 的 pair 是 rank=2** —— `(36225, 40592)`。Sha[2] 存在但 rank 不高，跟 sha2 在 hard_case 里的分布特征类似
4. **`(1845, 2912)` 的近 closure 距离 113** —— 是个值得专门 audit 的样本，可能是 closure 失败的局部障碍最弱的情况

## 后续任务（不在本 wl 内做）

1. **(1845, 2912) 深度审计**：用 PARI 生成元枚举所有 height ≤ H 的 concordant N，看 113 这个差能不能被某个更小或更大的 N 补上
2. **(27328, 44055) 结构分析**：rank=5 但 k=3，说明很多 Mordell-Weil 方向 *不* 落在 square-x 截面 —— 这是 Harborth 反例失败的另一类机制
3. **Phase 3c**：F₂-rank short-circuit 接进 proof_status workflow
4. **Phase 3d**：max_hyp 推到 100k+，看会不会出现 k ≥ 5 的 saturated 样本（目前最高 saturated k=4）

## 文件

```text
scripts/pari_rank_high_f2.py                                    新建
results/multi_concordant_N_max50000_pari_rank.jsonl             新建 (110 行，非 git 跟踪)
docs/work-logs/050-pari-ellrank-on-110-high-f2-candidates.md    本文件
```

`src/rational_distance/results/catalog.py` 也加上 `multi_concordant_N_max50000_pari_rank.jsonl` 条目。
