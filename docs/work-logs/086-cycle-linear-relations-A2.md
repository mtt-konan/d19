# wl086 — cycle 线性关系追踪（OPEN_DIRECTIONS A.2 / E.3 落地）

## 背景与动机

OPEN_DIRECTIONS A.2 / E.3 提议: wl058 在 (153,560) BFS 中发现 6-cycle,
wl059 发现 "cycle 与 rank deficit 高度相关", 但具体的线性关系
`c₁ Q_{N₁} + c₂ Q_{N₂} + ... = 0 ∈ E(ℚ)` 从未被算出来。

本 worklog 把这件事做完: 对每个 multi-N pair `(A, B)`, 把每个 concordant
点 `Q_N` 表成 Mordell-Weil generator 的整数线性组合 (mod torsion), 抽取整数
关系格的基, 并用 PARI 点运算**逐条精确验证**。

## 记号

concordant 曲线 `E: Y² = X(X+A²)(X+B²)`。对 concordant 整数 N
(即 N²+A²=□, N²+B²=□), 取整数点

```
Q_N = (X, Y) = (N², N·√(N²+A²)·√(N²+B²))  ∈ E(ℚ)
```

## 算法 (`src/rational_distance/concordant/cycle_relations.py`)

1. `compute_rank` (PARI `ellrank`, effort=1) 得 rank r 与 free generator
   G_1,...,G_r。
2. 高度配对法求坐标: 高度配对矩阵 H_{ij}=⟨G_i,G_j⟩ (PARI `ellheight(E,G_i,G_j)`),
   对每个 Q_N 解 `H c = v`, 其中 v_j=⟨Q_N,G_j⟩, 四舍五入得整数坐标 c。
3. **精确验证坐标**: 残差 R = Q_N − Σ c_i G_i 用 PARI `ellsub`/`ellmul` 直接算,
   确认 R 是 torsion (`ellorder` ∈ {1,2,4})。不依赖浮点 round 的信任。
4. **2-可除性**: 对每个 Q_N 调 PARI `ellisdivisible(E, Q_N, 2)`。
5. 整数关系格: 坐标矩阵 M (k×r) 的整数左零空间 (sympy nullspace + 清分母),
   每条关系 λ 满足 Σ λ_i·coord(Q_{N_i}) = 0。
6. **精确验证关系**: 对每条 λ 直接算 Σ λ_i Q_{N_i} (PARI 点运算), 确认结果
   是 torsion。

CLI: `scripts/multi_n/cycle_relations.py`。

## 验证 — 8/8 wl058 6-cycle pair 全部精确确认

```bash
PARI_MT_ENGINE=single uv run python scripts/multi_n/cycle_relations.py \
  --catalog results/partner/cycle_ellrank_wl058_6cycle.jsonl \
  --out results/multi_n/cycle_relations_wl058.jsonl
```

```
pairs analyzed:                 8
all Q_N divisible by 2 in E(Q): 8/8
all relations verified exactly: 8/8
relations found (total):        13
#relations == k - coord_rank:   8/8
```

典型输出 (rank=1 的 (420,1344)):

```
(A=420, B=1344): k=3 rank=1 deficit=2 relations=2
  Q_560  = [2]*G + T(ord 2)
  Q_1008 = [-2]*G
  Q_2925 = [4]*G + T(ord 2)
  relation: 1*Q_560 + 1*Q_1008  = T(ord 2)
  relation: 2*Q_560 + -1*Q_2925 = T(ord 2)
```

## 关键发现

### 1. 每个 concordant 点都在 2·E(ℚ) 里 (8/8 普遍, ellisdivisible 精确确认)

每个 `Q_N` 的 Mordell-Weil 坐标**全是偶数** (样本中全是 ±2 / ±4), 且
`ellisdivisible(E, Q_N, 2) = 1`。

**原因 (descent-trivial)**: 2-descent 映射
`E(ℚ)/2E(ℚ) ↪ ℚ*/ℚ*² × ℚ*/ℚ*²`, `P=(x,y) ↦ (x, x+A²)`。
对 `Q_N` 有 `x=N²=□`, `x+A²=N²+A²=□`, `x+B²=N²+B²=□` —— 这正是 concordant
的定义。所以 `Q_N` 的 descent 像是平凡的 `(1,1)`, 即 `Q_N ∈ 2E(ℚ)`
(half-point 是有理点, 与 `half_points.py` 一致)。

这在 Mordell-Weil 格层面**重新确认了 wl035 / CURRENT_FINDINGS §5.2 的预测**:
chain candidate 的 2-descent class 恒为 (1,1,1)。

### 2. 所有 cycle 关系都被 2-可除性 + 坐标秩亏完全解释

`#relations == k − coord_matrix_rank` 在 8/8 上成立。关系的残差几乎都是
2-torsion (13 条里 11 条), 系数普遍为 ±1/±2。**没有出现任何无法由格结构
解释的"额外"关系。**

### 3. 真正的"deficit"是 k − coord_rank, 不是 k − MW_rank

(153,560): MW rank=3=k (wl059 的 k_minus_rank=0), **但** 三个 Q_N 只张成
rank-2 子格 (Q_204=[2,0,0], Q_420=[-2,0,0] 都是 G_0 的倍数), 仍有 1 条关系。
wl059 "cycle ↔ rank deficit 相关" 的更准确陈述: cycle 对应 Q_N 坐标矩阵的
秩亏, 而坐标矩阵恒落在 2·(MW 格) 内, 所以秩亏频繁出现。

## 诚实评价 — A.2 不提供独立的 closure 障碍

cycle 线性关系是真实的、可精确验证的, 但它们**完全是 concordant 点 2-可除性
的复述**。这个 2-可除性对**任何** concordant 点都成立 —— 无论 4-chain
是否闭合。因此:

- ✅ 正面价值: 在 MW 格层面严格确认了 "concordant ⟹ descent class (1,1,1)";
  给出了 wl059 经验相关性的精确机制 (秩亏来自 2·格 约束)。
- ❌ 不能区分反例: 它对闭合 (反例) 与不闭合给出相同结构, 不构成 closure
  的必要条件强化。

所以 A.2 作为"找新必要条件"的路线**到此关闭** (negative but informative),
与 wl033 / wl035 的 2-descent 平凡性结论一致。

## 后续

- A.2/E.3 的"代数障碍"希望落空 ⟹ 真正的杠杆仍在 **height bound** (把 Heegner
  过滤器升级成判定器) 与 rank≥2 的 Chabauty (F.2 调研)。
- E.3 的另一半 ("是否所有 G_M cycle 都过某个 K_n hub") 是纯图论问题, 与本
  代数结论独立, 可在 E.1/E.2 时顺带统计。

## 文件

- `src/rational_distance/concordant/cycle_relations.py` — 核心
- `scripts/multi_n/cycle_relations.py` — CLI
- `tests/test_cycle_relations.py` — 8 测试
- `results/multi_n/cycle_relations_wl058.jsonl` — 8 pair 结果
