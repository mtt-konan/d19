# 033 — 想法 4 实证：chain 候选的对偶 EC rank 分布

**日期**: 2026-05
**触发原因**: `docs/CHAIN_STRUCTURE_IDEAS.md` §5 (想法 4) 提出对每个 4-chain 候选
`(a, b, c, d)` 同时考虑两条对角线椭圆曲线
$E_{a,c}: Y^2 = X(X+a^2)(X+c^2)$ 和 $E_{b,d}: Y^2 = X(X+b^2)(X+d^2)$，
试图寻找"对偶 EC rank=0" 作为 free obstruction。
**输出**: 三个脚本 + 两份 JSON/JSONL + 一个清晰的负面结论。

---

## 背景

### 想法 4 的数学结构

对一个完整 4-chain `(a, b, c, d)`（满足 C1-C4 全部 Pythagorean + 正方形闭合
`a+c = b+d`），§5.2 给出双 EC 视角下的有理点对应：

| 对偶 EC | 有理点 $X$ | 来源条件 |
|---|---|---|
| $E_{a,c}$ | $X = b^2$ | C1 + C2 |
| $E_{a,c}$ | $X = d^2$ | C3 + C4 |
| $E_{b,d}$ | $X = c^2$ | C2 + C3 |
| $E_{b,d}$ | $X = a^2$ | C1 + C4 |

**核心观察**：如果 $E_{b,d}$ 的 rank = 0，则它只剩 6 个 torsion X 坐标
$\{0, -b^2, -d^2, +bd, -bd\}$，而要 $X = a^2$ 出现就必须 $a^2 \in$ 这 6 个值之一。
由于 $a^2 > 0$ 且非平方倍数，几乎一定不可能（最强约束是 $a^2 = bd$，要求 $bd$
是完全平方）。

→ **dual rank=0 几乎确定地排除整个 chain 候选**。

### 数据来源

`results/chain.db` 现状（来自 chain_fast 已有 5 次跑）：
- `chain_solutions`: **0 行**（与 PROJECT_STATUS 一致，尚未找到正方形 chain 解）
- `chain_near_misses`: **202 行**，定义为 C1, C2, C3 全过、C4 差一点（`c3_ok=1, c4_ok=0`）

从 `chain_fast/kernel.py:361-394` 可验证：chain_fast 通过 §7 化简使得
`a + c = b + d` **自动成立**，因此 near-miss 是真正的"完整正方形 chain 候选，
仅 C4 没闭合"——正好是想法 4 想要的对象。

---

## 实证流程

### 三个脚本

1. **`scripts/probe_dual_ec.py`** — 主探测
   - 从 chain_near_misses 读 `(a, b, c, d)`
   - D4 去重（旋转 4 + 反射 4 = 8 个变换，取 lex-min）
   - 调用 `rational_distance.concordant.compute_rank` 拿 `(rank, bounds, gens)`
   - 输出 rank 联合分布 + JSONL

2. **`scripts/analyze_dual_ec_probe.py`** — 后处理
   - 区分 "certified rank=0"（lower=upper=0）和 "unproven rank=0"
     (lower=0, upper>0)
   - 这一步发现了**关键陷阱**（见下）

3. **`scripts/deep_rank_recheck.py`** — 深度复核
   - 用 `ellrank(E, effort=2)` 重做所有 unproven rank=0 的候选
   - **默认关闭** `ellanalyticrank`（带 `--analytic-rank` 才开）
   - `--max-magnitude` 限制候选规模，避免 PARI 卡死

### 两阶段实证

**阶段 1**: 全 150 个 D4-distinct 样本，default `ellrank`：

```
Joint rank distribution (rank_ac, rank_bd) -> count
  rank_ac= 0, rank_bd= 0:    1  (  0.7%)   ← 看起来双 obstruction
  rank_ac= 0, rank_bd= 2:    5  (  3.3%)
  rank_ac= 0, rank_bd= 3:    1  (  0.7%)
  rank_ac= 1, rank_bd= 1:   17  ( 11.3%)
  rank_ac= 1, rank_bd= 2:   15  ( 10.0%)
  ...
Dual E_bd rank=0:      4/150  ( 2.7%)
Total runtime: 4.1s (0.03s per sample)
```

初步看似有 **2.7% 免费 obstruction**。

**阶段 2**: 用 `analyze_dual_ec_probe.py` 检查 bounds，全部 4 个 `rank_bd=0` 都是
**unproven**（bounds=[0, 2]），即 PARI 只证了 rank ≤ 2，没证明真的 = 0。

**阶段 3**: `deep_rank_recheck.py` 用 effort=2 重算 11 个未证候选：

```
  id side           A           B  old      deep[lo,hi]  t_rank  status
  574 ac       240331       66585  [0,2]    [2,2]          0.11  CERTIFIED rank=2
  470 ac       262031       39721  [0,2]    [2,2]          0.10  CERTIFIED rank=2
   95 ac       331917       61215  [0,2]    [2,2]          0.07  CERTIFIED rank=2
   51 bd        22345      678503  [0,2]    [2,2]          0.05  CERTIFIED rank=2
   94 ac       713687      683865  [0,2]    [2,2]          0.09  CERTIFIED rank=2
   94 bd      1384320       13232  [0,2]    [2,2]          0.11  CERTIFIED rank=2
  382 ac       959180      194040  [0,2]    [2,2]          0.07  CERTIFIED rank=2
  103 bd      3394965     5509011  [0,2]    [2,2]          0.13  CERTIFIED rank=2
  536 ac      7713648     8587392  [0,2]    [2,2]          0.05  CERTIFIED rank=2
  346 ac     39457972    31944528  [0,2]    [2,2]          0.10  CERTIFIED rank=2
  342 bd     28988813   138746791  [0,2]    [2,2]          0.13  CERTIFIED rank=2

CERTIFIED rank=0 :  0
CERTIFIED rank>0 :  11
```

**11 个看似 rank=0 的候选，effort=2 下全部升级到 rank=2。**

---

## 关键发现

### 1. 主结论（负面）

> 在 150 个 D4-distinct chain near-miss 候选上，
> **0 个 dual EC 是 certified rank=0**。
> 想法 4 在 chain near-miss 上**不提供 free obstruction**。

这与 d19 主线观察"chain pair rank 过滤率 0%"完全一致——
对偶 EC 视角也得到 0% 过滤率。

### 2. PARI ellrank effort 陷阱（重要工程教训）

`pari.ellrank(E)` 返回 `(lower, upper)`：
- `lower`: 通过**找有理点**给出的 certified lower bound
- `upper`: 通过 2-descent 给出的 certified upper bound

**关键事实**：`effort=0`（默认）只做 quick point search，对很多曲线找不到非
torsion 点，于是 `lower=0`，但**这不代表 rank=0**。

实测对比同一批候选：
| effort | 11 个候选给出的 `lower` |
|---|---|
| 0 (默认) | 全部 = 0（误判） |
| 2 | 全部 = 2（与 upper 吻合，certified） |

**工程结论**：`compute_rank` 当前默认 `effort=0`，在 chain candidates 这种
conductor 较大的曲线上会系统性给出虚假的 "rank=0"。**汇报 rank=0 之前必须
重跑 effort≥2 验证**。

→ 这条已加入项目 memory，影响未来所有 chain/dual EC 相关脚本。

### 3. ellanalyticrank 性能陷阱（极重要）

最初的 `deep_rank_recheck.py` 默认开启了 `pari.ellanalyticrank(E)` 作为
analytic rank 对照。**结果在中等大小的 chain candidates 上每条 EC 跑了
906s ~ 6929s**（最长接近 2 小时一条），整个 recheck 跑了若干小时。

实测时间分布：
```
A=262031,  B=39721    →  906s
A=331917,  B=61215    → 1336s
A=713687,  B=683865   → 5253s
A=1384320, B=13232    → 6929s
A=959180,  B=194040   → 1073s
```

`ellanalyticrank` 需要算 L 函数，conductor 即便看起来不大也可能极慢。

**已记入 memory**：
- 任何脚本默认必须关闭 `ellanalyticrank`，由 flag 显式开启
- 强烈不推荐在 batch 模式下用，单条预算 ≥ 1h
- 想要 BSD-conditional rank 应该走 SageMath `E.rank()` (用 mwrank 或 simon-2descent)

### 4. rank 分布的边缘事实（信息性）

最终 certified 分布（effort=2 修正后估计；阶段 1 表的 bd=0 / ac=0 全部应改读成
rank=2）：
- `rank_ac` 主流：1, 2, 3，少量 4
- `rank_bd` 主流：1, 2, 3，少量 4
- **chain candidates 的对偶 EC 系统性地 rank ≥ 1**

这是新的实证规律：chain near-miss 上 dual EC 不会偶然落到 rank 0。
对偶 obstruction 这条路被这批数据否定。

---

## 后续路线

### 短期 (next worklog)

1. **修 `concordant.analysis.compute_rank` 的 effort 默认值**：从隐式 0 改为 ≥2，
   或在文档里明确警告 default 不足以判定 rank=0。
2. **想法 5（IDEAS §6 的"对偶约束"）**: 既然 dual rank 全部 ≥ 1，应转而问"有没有
   一组特定的二次扭/Selmer 信息能 obstruct？"。这是 Peschmann 2026 在 perfect
   Euler brick 上用的路径。

### 中期

3. **想法 3 (Sage 2-descent)**: PARI `ellrank` 在 chain candidates 上给出
   非平凡 rank 信息，但 d19 还没用 Sage `E.two_descent()` / `mwrank` 拿 Selmer
   group 结构。Selmer 给出的是 mod 平方约束，比 rank 更细。
4. **想法 7 (specific local obstructions)**: 探索 mod-p 障碍而非 EC 层面。

### 长期

5. **改 chain_fast 让它能直接处理"closed 4-chain"（即 C4 也满足的）**，再用 dual
   EC 在那批样本上做 rank distribution——这是真正的 hard case，但样本可能很稀少。

---

## 输出物

### 脚本
- `scripts/probe_dual_ec.py` — 主探测，从 chain.db 抽 D4-distinct 样本算双 EC rank
- `scripts/analyze_dual_ec_probe.py` — 区分 certified vs unproven
- `scripts/deep_rank_recheck.py` — effort=2 复核，默认关 ellanalyticrank

### 数据
- `results/dual_ec_probe.jsonl` — 150 个样本的 default-effort 双 EC bounds
- `results/dual_ec_deep_full.json` — 11 个 unproven 候选的 effort=2 复核结果

### 文档 / 记忆
- 本 worklog
- Memory: "cypari2 性能陷阱：ellanalyticrank 在大 conductor 上极慢"
- 待更新: `docs/CHAIN_STRUCTURE_IDEAS.md` §5 加上"实证结论：无 free obstruction"

---

## 复现命令

```bash
# 1. 主探测（默认 effort，~ 5 秒）
uv run python scripts/probe_dual_ec.py \
    --limit 200 \
    --out-jsonl results/dual_ec_probe.jsonl

# 2. 区分 certified vs unproven
uv run python scripts/analyze_dual_ec_probe.py \
    results/dual_ec_probe.jsonl

# 3. 用 effort=2 复核 unproven 候选（~ 1 秒，最大放到 200M）
uv run python scripts/deep_rank_recheck.py \
    results/dual_ec_probe.jsonl \
    --max-magnitude 200000000 \
    --out results/dual_ec_deep_full.json

# 注意：不要加 --analytic-rank，那会让单条 EC 跑数小时。
```
