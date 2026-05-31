# wl087 — D.1 收尾：F₂-rank ≥ 3 pair 的 PARI ellrank 审计已完整 + 独立复现

## 背景

OPEN_DIRECTIONS **D.1** 记着 "wl050 跑了一部分但没完整 110 pair audit"。本 worklog
核对后发现该说明**已过时**：审计早在 wl050 + wl052 就完整跑过, 本 wl 做独立复现确认,
并把 D.1 收尾。

## 现状核对

D.1 想要的 "把 F₂-rank ≥ 3 的真候选全部跑 certified PARI ellrank" 已在两个尺度完成:

| 尺度 | F₂-rank≥3 候选 | 审计文件 | worklog |
| --- | --- | --- | --- |
| max_hyp=50000 | 110 | `results/multi_n/multi_concordant_N_max50000_pari_rank.jsonl` | wl050 |
| max_hyp=100000 | 190 | `results/multi_n/multi_concordant_N_max100000_pari_rank.jsonl` | wl052 |

两个文件都是 `rank_lower == rank_upper` 全 certified (0 uncertified)。

## 独立复现 (本 wl)

用现成脚本对 max100000 的 190 个候选**从头重跑** PARI `ellrank` (effort=1):

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/pari_rank_high_f2.py \
  --in results/multi_n/multi_concordant_N_max100000_classified.jsonl \
  --out /tmp/d1_recheck_max100000.jsonl     # ~2s
```

与已提交文件逐 pair 比对:

```
new rows: 190   old rows: 190   same pair set: True
rank/sha2 disagreements: 0
uncertified in fresh run: 0
```

**完全一致** —— 审计可复现, D.1 数据可信。

## 完整 certified 结论 (两尺度合并)

```
                     max_hyp=50000      max_hyp=100000
F₂-rank≥3 候选            110                190
  rank=2                  40                 63
  rank=3                  57                 93
  rank=4                  12                 31
  rank=5                   1                  3
rank≥4 ("结构允许")        13                 34
Sha[2]≥2                   1                  2
all certified            是                 是
```

### Sha[2] ≥ 2 的 pair

- max50000: `(36225, 40592)` rank=2 (wl050 已记)
- max100000 新增: `(34307, 74000)` rank=2

即扩到 max100000 后, 结构允许 Harborth 4-chain 反例的候选从 13 增到 34 个,
非平凡 Sha[2] 的 pair 从 1 增到 2 个。**全部 pair 的 closure_pairs 仍为空**
(无反例), 与 wl050/wl052 结论一致。

## 结论

D.1 完整闭环, 无需新计算。F₂-rank ≥ 3 的全部 "真候选" 在 max_hyp ≤ 100000 内都有
certified rank。"结构允许池" 的精确大小 (13 @ 50k, 34 @ 100k) 已确定, 是后续
height-bound 判定器 / Chabauty (rank≥2 占多数) 的目标集合。

## 文件

- 复核脚本 (现成): `scripts/theory/pari_rank_high_f2.py`
- 审计结果: `results/multi_n/multi_concordant_N_max{50000,100000}_pari_rank.jsonl`
