# 043 — wl042 后的方向地图与决策框架（待决策）

**日期**: 2026-05-25 (wl042 commit f531361 之后)
**触发原因**: wl042 跑完 13 个 sha2≥2 case 的 ell2cover deep-dive 后，用户提出
"不发 paper，从实用主义角度后续干啥"。本 worklog **不实现任何新代码**，
只整理对话演进出来的方向地图、外部输入（别人给的 18 条建议）、
Obstruction vs Construction 的二分法、当前实证状态汇总、决策框架，
等待用户从中选择下一步。
**输出**: 策略整理文档；不修改任何 code/data；可作为未来重启时的 entry point。

---

## 一、对话脉络（wl042 commit 之后到现在）

时间线：

1. **wl042 commit (f531361)** — 13 sha2≥2 case 三分类（4 clean / 7 mid / 2 outlier）
2. 用户问 #1（"那 4 个 clean case 怎么算"） → AI 实测 (36001, 218051) 的两个候选 quartic
   在 h=10⁶ 内仍无有理点 + 小素数 mod p 全过 → 给出 (a)+(b)+(c)+(d) 四步路线图
3. 用户表态 **不发 paper，从实用主义视角评估**
4. AI 第一次回答倾向 **封盘**（B + 推 max_hyp 收尾）
5. 用户提供别人写的 18 条方向地图（覆盖 A-E 五组），观感比 AI 乐观
6. AI 用 wl040-042 后的最新状态重新打分那 18 条 → 大半失效或缩水，
   **valid 的只有 C1 (CT pairing on 13 case) + C2 (cert-pipeline 集成)**
7. 用户追问关键："**做完 C1+C2 后，如果还信反例存在，反例会出现在哪？**"
8. AI 回答 **C1+C2 跟找反例几乎无关**——326 hard_case 已经被 wl040 §12
   chain enumeration 排除，反例只能在 max_hyp > 10000 范围
9. 用户问 Peschmann 2026 perfect cuboid 是什么、跟 d19 对比"好懂"程度
10. AI 给出对比表：Peschmann 4 个自由参数 / genus 3 / 300 年未解，
    d19 2 个自由参数 / genus 1 / 90 年未解 → **Peschmann 旁证：
    在更难、更老、工具更深的问题上 max param=10³ 也 0 反例**
11. 用户提出**核心观点**："这种问题就是构造法，暴力穷举不行了，应该
    在减小空间里直接穷举或构造反例，或者用想不到的技巧"
12. AI 看 `docs/archive/CHAIN_STRUCTURE_IDEAS.md` 查阅历史想法 →
    发现 **construction 方向被严重 underexplored**，承认之前的回答不够充分

## 二、当前实证状态汇总（封盘前的快照）

```
所有 (A, B) pair (max_hyp=10000)
  └─ 2.5M pair, 0 反例
     ↓ safe_sieve (mod 4)             砍 91%
     ↓ chain_closure_mod_sieve         砍 99.6% (mod p² 联立, wl040)
     ↓ factor_concordant + chain enum  逐个枚举 concordant N (wl040 §12)
     ↓ → 326 hard_case
        ├─ 88 rank=1
        ├─ 146 rank=2
        ├─ 92 rank≥3
        ├─ 13 sha2_lower=2 (Sha[E,2] candidate, wl042)
        │   ├─ 4 clean (n_without_pt = 2 = sha2)         ← Sha[E,2] dim=2 直接候选
        │   ├─ 7 mid   (n_without_pt = 3)
        │   └─ 2 outlier (n_without_pt = 4)
        └─ 0 chain refutation across all 326 (wl040 §12)
```

工程：

- proof_status pipeline 8-worker parallel，max_hyp=10000 跑 1m25s
- chain-fast pipeline 1m23s 配套（wl041）
- proof_status.db 970MB，包含全部 method-level results

数学：

- 0 反例（2.5M pair）
- 13 个 explicit Sha[E,2] candidate（4 clean）
- chain_closure_mod_sieve 是项目第一个**联立 N 和 b 的必要条件**（wl040）

## 三、外部输入：别人的 18 条方向地图（wl040-042 后重新打分）

地图原始时点是 wl039（4653 hard_case + 156 sha2=2 + 9 outliers）。
chain_closure_sieve 之后状态完全变了。重新打分：

| 组 | 方向 | 原评分 | wl040-042 后真实状态 | 不发 paper 价值 |
|---|---|---|---|---|
| A | A1 max_hyp=5000 | 易/半天/中 | ✅ 已超额（max_hyp=10000） | — |
| A | A2 chi² on 156 sha2=2 quartic | 易/半天/中-高 | ❌ sample 13 太小，chi² 失效 | ❌ |
| A | A3 DB 整合 | 中/半天/中 | ✅ 已完成 | — |
| B | B1 (169, 235) 深挖 | 中/1-2天/高 | ⚠️ 不在新 priority queue | △ 换个 case 才有意义 |
| B | B2 Heegner 9 outliers | 高/2-3天/高 | ⚠️ 9 → 2 outliers | △ 纯学习 Heegner |
| B | B3 MW 高度筛 9 outliers | 中-高/1-2天/高 | ⚠️ 9 → 2 outliers | △ |
| C | **C1 CT pairing 13 case** | 中/2天/高 | ✅ **半天可跑** | ⭐⭐⭐ |
| C | **C2 cert-pipeline 集成** | 中/2-3天/极高 | △ **部分完成**，可补 | ⭐⭐⭐ |
| C | C3 Galois chi² | 高/3天/中-高 | ⚠️ sample 326，部分能做 | △ |
| D | D1 K3 BM 障碍 | 极高/数周/极高 | paper-level | ❌ 不发 paper 价值 0 |
| D | D2 cover Chabauty | 高/数周/高 | paper-level | ❌ |
| D | D3 modular forms | 极高/数月/极高 | paper-level | ❌ |
| E | E1 特殊家族 | 易/半天/低-中 | wl041/042 已 cover | ❌ |
| E | E2 wl037 升级 N≤10¹⁰ | 易/1天/中 | trend 已 0 解，期望仍 0 | ❌ |
| E | E3 KSS/Ono 文献对接 | 中/文献天/中 | 文献工作 | △ |

地图作者乐观背后的三个 mistake：

1. **基于过时数据**：他没看到 chain_closure_sieve 把 hard_case 4653→326、
   sha2=2 156→13、outliers 9→2
2. **价值列默认可发表**：D1-D3 的"极高价值"基于 paper-level 假设
3. **A2/C1/C3 chi² 套路在 sample 缩小后失效**

## 四、用户的"构造法"观点（被忽略的方向）

用户提出："这种问题就是构造法，暴力穷举不行了，应该在减小空间里
直接穷举或构造反例，或者用想不到的技巧。"

### 这个直觉为什么对

| 理由 | 论据 |
|---|---|
| 暴力穷举边际收益 ≈ 0 | max_hyp 每 ×10 = pair ×100，但 ratio 不增长，反例如果存在必然在 deep |
| 历史上 Diophantine 反例多是构造的 | Bremner-Cassels 1984 在 $y^2=x(x²+p)$ 上 p=877 才出现 generator |
| 项目已经把空间压到 0.013% | chain_closure_sieve 是天花板级 obstruction sieve |

### 项目里"构造法 vs obstruction" 二分法

| 视角 | d19 项目状态 |
|---|---|
| **Obstruction**（证无解） | ✅ **天花板**：safe_sieve + chain_closure_sieve + factor_concordant + ell2cover/sha2/CT |
| **Construction**（找反例 / 找代数 family） | ❌ **几乎没做** |

打开 `docs/archive/CHAIN_STRUCTURE_IDEAS.md`，4 个想法回顾：

| 想法 | 状态 | 实证结论 |
|---|---|---|
| **1** Hypotenuse identity + blocker prime | △ 部分 | 恒等式 100% 验证 ✅；blocker prime 论证错（h_i non-primitive 时奇素因子不必 ≡1 mod 4）❌ |
| **2** 正方形 vs 长方形条件强度 | — | 写 paper intro 的观察，不 actionable |
| **3** 2-descent on $E_{A,B}$ | ✅ 全力采纳 | wl035-042 |
| **4** Dual EC ($E_{a,c}$ vs $E_{b,d}$) | ❌ 实证否定 | wl033 — 150 chain near-miss 上 0 个 dual EC certified rank=0 |

**关键观察**：用户 4 个想法**全部偏构造 / 代数结构**方向。被否定的只有
"dual EC 0 free obstruction"，**hypotenuse identity 核心是对的**（只是
blocker prime 推论错），**2-descent 被全力采纳成主线**。

但即便如此，项目从 wl001 到 wl042 **从未认真做过 construction-finding**——
所有方向都是 obstruction，不是 construction。

## 五、真正未做的 Construction 方向（候选 X1-X3）

### X1: rank≥1 hard_case 的 EC generator lattice search

234 个 hard_case 是 rank≥1（88 rank=1 + 146 rank=2）。每个 PARI 都给了
generator(s)。**没人问过**：

> generator 的整数倍 $\{P, 2P, 3P, ..., kP\}$（rank=1）
> 或 $\{aP + bQ : |a|, |b| \leq K\}$（rank=2）
> 在 EC 上的 X 坐标里，有没有 $X = N^2$ 且 $N$ 满足 chain closure？

这是 constructive search：不暴力 N 枚举，而在 EC generator lattice 上枚举。
Heegner 是其特殊化（CM 给特殊高度的 generator）。

工程：

- rank=1: 每 case 1-5 分钟（regulator 决定 multiplication 上限）
- rank=2: 每 case 5-30 分钟（lattice 2D 扫描）
- 234 case 全跑：估计 半天-1 天

价值：

- 找到反例 → Harborth 解决，论文
- 找不到反例 → 项目第一次完整 cert "constructive 方向也排除了"

### X2: Hypotenuse identity 升级为 parametric family

wl034 找到的 identity：

$$(h_1 h_3)^2 - (h_2 h_4)^2 = (d-b)(a-c) \cdot S^2$$

这把 6 个 quantity（4 h_i + d-b + a-c）联系起来。

**没人问过**：能否用这个 identity 把 4-chain 问题约简到一个低维代数簇？
如果能压到 surface（dim 2）且 surface 是 rational / Enriques / K3，
则反例的密度有理论判据：

- rational surface → 反例密集存在
- Enriques → 反例稀疏但存在
- K3 → 反例可能不存在
- general type → 反例几乎不存在

工程：纯数学推导。需要代数几何嗅觉，不是计算 task。

价值：项目历史上第一次从 surface 视角看 4-chain 问题。

### X3: Chain 整体看作 K3 surface（Peschmann §8 future direction 的同类）

Peschmann 2026 §8 提到 K3 surface 上的 Brauer-Manin 是他的 future direction。
d19 上同样思路：把 4-chain 整体（4 个 squares 联立）当代数 surface 算。

工程：长期数学方向，需要 SageMath/Magma + 代数几何 expertise。

价值：paper-level，不发 paper 价值 ≈ 0。

## 六、当前所有可选方向汇总

不发 paper 的实用主义视角下：

| 方向 | 类型 | 时间 | 实用价值 | 找反例概率 |
|---|---|---|---|---|
| **直接封盘**（写 README + 归档） | — | 1-2 小时 | 干净 snapshot | — |
| **推 max_hyp** 到 20k/50k/100k | obstruction | 5-240 分钟 | 边际数据点 | 接近 0 |
| **C1**: CT pairing on 13 sha2≥2 case | obstruction | 半天 | 严格 cert Sha[E,2] dim≥2 | — |
| **C2**: cert-pipeline 集成 ell2cover/CT | 工程 | 1-2 天 | 工程基础设施完整 | — |
| **X1**: Generator lattice search | **construction** | 半天-1 天 | **第一次 construction 方向** | < 0.1% |
| **X2**: Hypotenuse identity 升级 | construction | 几周纯数学 | 学习投资 | 需要数学突破 |
| **X3**: K3 surface 分析 | construction | 数月，需 Magma | paper-level | paper 才有意义 |
| **完全停手** | — | 0 | 沉没成本归零 | — |

## 七、决策框架

不发 paper 的两个独立 dimension：

```
                          保留可能找到反例的 1%
                                  ↑
                                  │
                                  │   X1 (construction)
                                  │   推 max_hyp (brute)
                                  │
                  ───────────┼─────────── 完全收尾
                                  │
                                  │   C1+C2（数学严格性 + 工程完整）
                                  │   直接封盘
                                  ↓
                          完全收尾，不再投入
```

**4 个真正可选的组合**：

| 组合 | 内容 | 适合什么人 |
|---|---|---|
| **直接封盘** | 1-2 小时写 README + commit | 真·纯实用主义 |
| **C1+C2 然后封盘** | 2-3 天，数学+工程完整 | 想留个漂亮 snapshot，不在乎找反例 |
| **X1 然后封盘** | 1 天，第一次构造法尝试 | 想"再试一把"找反例 |
| **C1+C2 + X1 全套** | 3-4 天 | 一次到位，封盘前把 obstruction 和 construction 都做到天花板 |

之外的选项（推 max_hyp / X2 / X3）从实用主义视角都不推荐：

- 推 max_hyp = 等于 X1 的弱化版（X1 在 234 case 上做得更精确）
- X2 / X3 = paper-level，不发 paper 没意义

## 八、状态：待用户决策

本 worklog **不实现任何 code**，只整理思路。等待用户从上面 4 个组合中选择
（或提出其他思路）。在用户决策前，项目当前状态保留：

- 最新 commit: `f531361` (wl042)
- proof_status.db: max_hyp=10000 完整数据
- 13 sha2≥2 ell2cover JSONL: `results/ell2cover_sha2_10k.jsonl`、
  `results/ell2cover_sha2_10k_h100k.jsonl`
- 326 case rank/sha2 数据: `results/ell2cover_10k.jsonl`

所有数据可重启时秒读，所有 pipeline 可秒跑。

## 九、Commit 历史（背景）

```
f531361  docs(worklog): 042 sha2≥2 clean 13 deep-dive on max_hyp=10k
d797d7c  docs(worklog): 041 parallel pipeline + max_hyp=10k scaling
1b9d89a  feat(proof_status): parallel pipeline + batched commits
c75377b  docs(worklog): 040 §12 — exhaustive chain enum on 18 survivors → 0 refutations
7d87377  docs: worklog 040 — chain-closure mod p² sieve cuts hard_case 99.6%
447e9a9  test(proof_status): 4 unit tests for chain_closure_mod_sieve
53cfe93  feat(proof_status): integrate chain_closure_mod_sieve into pipeline
5abc63e  feat(concordant): add chain-closure mod p² joint sieve
```

## 十、相关文档

- 数学方向汇总：`docs/THEORY_DIRECTIONS_ADVANCED.md`、`docs/CHAIN_STRUCTURE_IDEAS.md`（archive）
- 文献：`docs/literature/notes/peschmann-2604-09328.md`（最相关旁证）
- 工具：`scripts/batch_ell2cover_v2.py`、`scripts/ell2cover_worker.py`、`scripts/prove_no_solution.py`
- 数据：`results/ell2cover_10k.jsonl`、`results/ell2cover_sha2_10k*.jsonl`、`/tmp/proofs_parallel_10k.sqlite3`
