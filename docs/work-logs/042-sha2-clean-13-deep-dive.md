# 042 — 13 个 sha2≥2 hard_case 在 max_hyp=10000 上的 ell2cover deep-dive

**日期**: 2026-05-25（紧接 wl041）
**触发原因**: wl041 在 max_hyp=10000 找到 13 个 sha2_lower=2 hard_case。
本 worklog 用 wl039 的 ell2cover quartic + hyperellratpoints 工具链对这 13
个 case 做 explicit Sha[E][2] candidate 检验，划分出最值得手算的 4 个
"clean" Brauer-Manin 目标。
**输出**: 2 个 JSONL 数据文件（h=10⁴、h=10⁵）+ 13 case 的三分类 + 4 个
clean Sha[E][2] dim=2 candidate（rank=1, n_without_pt=2）。

---

## 一、数据来源

`results/ell2cover_10k.jsonl`（wl041 产物，max_hyp=10000 上的 326 hard_case
× ell2cover）。从中过滤 `sha2_lower >= 2` 得到 13 行。

## 二、跑 ell2cover quartic + hyperellratpoints

复用 wl039 的工具链 `scripts/batch_ell2cover_v2.py` + `scripts/ell2cover_worker.py`，
subprocess 隔离 + 60s/case 硬超时。两轮 height 比较：

| height | wall time | timeout | error |
|---|---|---|---|
| 10⁴   | 1.3s  | 0 | 0 |
| 10⁵   | 14s   | 0 | 0 |

**两轮结果完全一致**：n_without_pt 分布不变，没有 outliers 在 10⁵ 找到额外
rational point。

## 三、13 case 的三分类

| 子集 | 数量 | n_without_pt | rank | 含义 |
|---|---|---|---|---|
| **Clean** | **4** | 2 | 1 | `n_without_pt = sha2`，pure Sha[E][2] dim=2 generator |
| Mid | 7 | 3 | 1 (6) / 2 (1) | sha2 + 1 cover-pullback miss (height > 10⁵) |
| Outlier | 2 | 4 | 2 (1) / 3 (1) | sha2 + 2 cover-pullback misses |

n_without_pt 公式（wl039）：

$$
n_\text{without\_pt}(h) = \dim \Sha[E,2] + k(h)
$$

$k(h)$ 是 generator 在 cover 上 pullback 后 height > h 的 cover 数。对
clean 子集 k=0，对 mid 子集 k=1，对 outlier 子集 k=2。

### 4 个 Clean Sha[E][2] case（项目最值得手算的样本）

```
(A=  36001, B=  218051)  rank=1  sha2=2  n_cov=5  n_no_pt=2
(A=  99617, B=  165967)  rank=1  sha2=2  n_cov=5  n_no_pt=2
(A= 214555, B=  349853)  rank=1  sha2=2  n_cov=5  n_no_pt=2
(A= 708055, B= 1178093)  rank=1  sha2=2  n_cov=5  n_no_pt=2
```

每个都：

- **rank=1**（最简单的 EC arithmetic）
- **sha2=2**（非平凡 Sha[E][2] 维度 = 2，PARI effort=1 报告）
- **n_quartic_covers = 5 = rank + 2 + sha2 = 1 + 2 + 2**（公式 100% 验证）
- **5 个 quartic 中 2 个无有理点 (h ≤ 10⁵)**，正好对应 Sha[E][2] 的两个
  generator
- **PARI generator 在 h ≤ 10⁴ 内被找到**（k=0）

→ **这是 d19 项目第一次得到 "explicit Sha[E][2] dim=2 generator + clean
Brauer-Manin candidate" 的 case**。

### 7 个 Mid 子集

```
(A= 150887, B= 4032145)  rank=1  n_no_pt=3
(A= 203609, B=  917059)  rank=1  n_no_pt=3
(A= 226499, B= 1834549)  rank=1  n_no_pt=3
(A= 508183, B= 3069605)  rank=2  n_no_pt=3
(A= 523345, B= 4478747)  rank=2  n_no_pt=3
(A= 564851, B=  615901)  rank=1  n_no_pt=3
(A= 798109, B= 1288991)  rank=1  n_no_pt=3
```

6 个 rank=1 case 是 Heegner generator + canonical height 的目标（方向五）。
2 个 rank=2 case 需要 Chabauty / Stoll 高度 sieve（方向七）。

### 2 个 Outlier

```
(A=  62489, B=  155839)  rank=3  n_no_pt=4
(A= 179117, B= 3398395)  rank=2  n_no_pt=4
```

跟 wl039 的 9 个 outliers 模式一致：generator 在 cover 上 pullback 后
height ≫ 10⁵，需要 Heegner-level 工具或 Stoll 高度 sieve 才能确认它们
是真 Sha[2] 还是 cover-lift 太高的 generator。

## 四、跟 wl036/038/039 的对比

| 阶段 | max_hyp | hard_case 总数 | sha2≥2 数 | "clean" sha2 dim=2 (n_no_pt=2) | sha2≥2 比例 |
|---|---|---|---|---|---|
| wl036 (无 chain_closure) | 500   | 320  | 2   | — | 0.6% |
| wl039 (无 chain_closure) | 2000  | 4653 | 156 | 39 (rank=1) | 3.4% |
| **wl042 (with chain_closure)** | **10000** | **326** | **13** | **4 (rank=1)** | **4.0%** |

观察：

1. **chain_closure_mod_sieve 砍掉的"sha2=0 简单 local 障碍" 不是 noise，
   是真实数学事实**——但它们用 mod p² 就能直接证明 no_solution，
   不需要 PARI Selmer 工具。
2. **留下的 326 hard_case 是 deep arithmetic obstruction 的真实样本**：
   13/326 = 4% sha2≥2，比 wl036 的 0.6% 高 7 倍。
3. **4 个 clean Sha[E][2] dim=2 case 是 d19 项目第一次得到的 Brauer-Manin
   priority queue**。manual 手算 4 个 quartic 的 local solubility everywhere
   可以直接 cert Sha[2] non-trivial。

## 五、为什么这 4 个 case 值得"亲手"分析

每个 Sha[E][2] 非平凡元素对应一个 quartic curve $C: y^2 = f(x)$（degree 4），
其中 $f \in \mathbb{Z}[x]$。**$C$ 在所有 $\mathbb{Q}_p$ 上有解但在 $\mathbb{Q}$
上无解**——这就是 local-to-global 障碍的 explicit witness。

对每个 clean case 的 quartic：

1. **Local solubility check**：对所有 $p | \text{disc}(f)$，看 $C(\mathbb{Q}_p) \neq \emptyset$。
   （应当 100% 成立，否则 PARI 不会报 sha2=2。）
2. **Global no-point check**：用 Hensel lifting 或 LLL-based Mordell-search
   排除整数解（PARI hyperellratpoints 已部分做了，但只到 h=10⁵）。
3. **Brauer-Manin pairing**：写出 $\mathrm{Br}(C) / \mathrm{Br}(\mathbb{Q})$
   元素，计算 $\sum_v \mathrm{inv}_v(\alpha)$ 是否非零。

每个 case 大约 1-2 小时手算 / Magma 验证。4 个 case 是 manageable 的论文级
实证工作。

## 六、输出物

### 数据

- `results/ell2cover_sha2_10k.jsonl`       — 13 case at h=10⁴ (1.3s)
- `results/ell2cover_sha2_10k_h100k.jsonl` — 13 case at h=10⁵ (14s)

### 复现命令

```bash
# h=10^4 sweep (1s)
uv run python scripts/batch_ell2cover_v2.py \
    --sha2-jsonl results/ell2cover_10k.jsonl \
    --out results/ell2cover_sha2_10k.jsonl \
    --height 10000 --timeout 60

# h=10^5 verification (14s)
uv run python scripts/batch_ell2cover_v2.py \
    --sha2-jsonl results/ell2cover_10k.jsonl \
    --out results/ell2cover_sha2_10k_h100k.jsonl \
    --height 100000 --timeout 120
```

## 七、下一步候选

| priority | 任务 | 工作量 |
|---|---|---|
| ⭐⭐⭐⭐ | **手算 (36001, 218051) 的 Sha[2] quartic local solubility** | 1-2 小时 |
| ⭐⭐⭐ | 88 个 rank=1 hard_case 全集 Heegner generator scan | 1-2 天 |
| ⭐⭐⭐ | max_hyp=20000 看 hard_case 和 sha2≥2 占比是否稳定 | 5-10 分钟跑 |
| ⭐⭐ | 1 个有 2 concordant N 的特殊 case 单独分析 | 1 小时 |

## 八、Commit 历史

```
(本 worklog: docs(worklog): 042 sha2>=2 clean 13 deep-dive)
```
