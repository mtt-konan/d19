# wl092 — 方向五"把 Heegner 升级成判定器（补 height bound）"评估：冗余 / 已被 factor_search 取代

## 任务

承接用户选择"把 Heegner 从过滤器升级成判定器（补 canonical-height bound，长期最高
杠杆）"。`heegner_height.py` 现只扫 `|n|≤12` 个 MW 倍数、找不到点只返回
`inconclusive`，文档（THEORY_DIRECTIONS_ADVANCED 方向五）说要补一个 height bound
H、"证明若存在解其 ĥ≤H"或"证明所有 square-X coset 已覆盖"才能升级成 `no_solution`。

**结论先行**：这条路 **冗余 / 不必做**。pipeline 里 `factor_concordant`（方法 3，
排在 `heegner` 之前）**已经是 integer-N concordance 的穷尽判定器**，对所有 rank 成立、
无需任何 height bound；而需要用来"认证有界扫描已覆盖"的那个 height 上界，
wl077/B.6 已实证不成立（方向不对）。两条独立理由都指向同一结论。

## 一、为什么 height bound 这条路不必走

### 1.1 factor_search 已穷尽枚举所有 concordant 整数 N

`concordant/factor_search.py::find_concordant_by_factorization(A,B)`：
由恒等式 `h4²−h3² = B²−A² = (h4−h3)(h4+h3)`，**每个**整数解 (N,h3,h4) 恰对应
`B²−A²` 的一个 divisor pair。所以枚举 `B²−A²` 的因子即可恢复**全部** concordant
整数 N，**无上界参数**，复杂度 `O(√(B²−A²))`（docstring 自证完整性）。

这正是方向五想要的"覆盖所有 square-X coset / 认证无遗漏"——**已经实现，而且对所有
rank 成立**（不只 rank=1）。`run_factor_concordant` 据此给出：
- 无 concordant N ⇒ `no_solution`；
- 有 chain-compatible N ⇒ `solution_found`；
- 有 concordant N 但无一闭合 4-chain ⇒ `inconclusive`（**仅因"闭合是否必要"这一
  几何问题存疑，并非搜索不完整**）。

### 1.2 pipeline 顺序：heegner 只在 factor_concordant 已穷尽后才被调用

`DEFAULT_METHOD_PIPELINE` = safe_sieve → chain_closure_mod_sieve →
**factor_concordant** → multi_n_sieve → f2_rank → rank_zero → **heegner** → …
（遇 `no_solution`/`solution_found` 即停）。所以 `heegner` 收到的每个 pair，
`factor_concordant` 都已**枚举完所有 concordant 整数 N 且验证无一 chain-compatible**。
rank=1 的有界 MW 扫描只是重看其中一个**真子集**，对判定**零贡献**。

### 1.3 实测（`scripts/theory/heegner_vs_factor_decider.py`，max_hyp=500）

穷尽 factor 判定器对全部 540 个 safe-pass pair，**24.8 ms** 全部判完：

| 桶 | 数量 | pipeline 结论 |
|---|---|---|
| 无 concordant N | 220 | `no_solution` |
| 恰 1 个 concordant N | 313 | `no_solution`（closure 需 ≥2，multi_n_sieve） |
| k≥2 但无一闭合 | 7 | `inconclusive`（= heegner 目标） |
| chain-compatible | **0** | 无反例 |

7 个 inconclusive hard_case 与 rank-1 有界扫描对比：

| (A,B) | concordant_N（穷尽因子法） | rank | heegner `|n|≤12` 扫到 | 被有界扫描漏掉 |
|---|---|---|---|---|
| (25,91) | [60, 312] | [3,3] | [] (rank≠1) | [60,312] |
| (85,351) | [132, 720] | [2,2] | [] | [132,720] |
| (1377,23023) | [18564, 35100] | [3,3] | [] | 全部 |
| (1615,5733) | [2856, **260820**] | [2,2] | [] | 全部 |
| (1771,9945) | [1428, 2700] | [3,3] | [] | 全部 |
| (2261,5175) | [2280, 6900] | [4,4] | [] | 全部 |
| (9207,24157) | [13260, 47124] | [3,3] | [] | 全部 |

两个致命观察：
1. **7 个残余 hard_case 全是 rank≥2**，`heegner`（仅 rank=1）对它们全部 `skipped`，
   一个 concordant N 都没看到。方向五声称能砍 ~37% rank-1 hard_case，但在这个残余
   population 上 rank-1 占比为 **0**。
2. 因子法找到的 N（如 260820、47124）**远超**任何有界 MW 倍数 / `ellratpoints`
   高度窗口（ec_bound=1e5 只覆盖 N≤316，`|n|≤12` 更小）。要靠 height bound 让有界
   扫描覆盖到 N=260820，需要的 M 巨大且 rank-1 限定——而因子法瞬间、无界、全 rank
   就拿到了。

### 1.4 height 上界本身也不成立（wl077 / B.6）

即便想沿"ĥ 上界"认证，wl077 已实证：closure 假设给出 `ĥ(P_{N_i}) ≤ 2 log(A+B)+O(1)`，
但实测 1879/1879 个 k=2 pair 的 `min ĥ > 2 log(A+B)` **全部 violated**（margin
中位数 −10.3，方向反了）。wl077 §1.3 独立得到同一结论：**对 k=2，closure 就是对
（已知有限的）concordant N 做一次 `N₁+N₂=A+B` 布尔检查，不需要 Chabauty / height
bound**。这与 §1.1 的因子穷尽完全一致。

## 二、真正的开放杠杆在哪

`inconclusive` 之所以没升级成 `no_solution`，**不是**因为"还没找全有理点"（已找全），
而是因为一个**归约完整性 / 几何**问题：

> 对一个 Harborth 反例，闭合 4-chain（`b=A+B−N` 也 concordant）是否**必要**？

若能证"必要"，则"concordant N 全部不闭合 ⇒ `no_solution`"立即对**所有 rank**成立
（因子法已枚举全部 N）。这是纯数论/几何引理，**与 Heegner 点、canonical height 无关**。
其余尝试（path B uniform mod p²：wl078-079 已关闭；height-bound：B.6 已关闭）也都不在
Heegner 方向上。rank≥2 主流 hard_case 的结论性工具仍是 Chabauty（需 Magma，见 wl090
F.2）/ Brauer–Manin。

## 三、结论 / 建议

- **方向五"补 height bound 把 Heegner 升级成判定器"判为冗余**：integer-N 的穷尽判定
  已由 `factor_concordant` 完成（全 rank、无 height bound、毫秒级），rank-1 有界 Heegner
  扫描是其严格子集；且残余 hard_case 全 rank≥2，Heegner 根本不适用。
- 不新增 height-bound 代码（避免重走 B.6/wl077 已关闭的路）。
- 文档据此更新：THEORY_DIRECTIONS_ADVANCED 方向五标注"integer-N 覆盖已由 factor_search
  完成；剩余 gap 是 closure-necessity，非 height"；OPEN_DIRECTIONS 收口。
- 把真正的开放问题明确为 **closure-necessity 引理** + rank≥2 Chabauty/Brauer–Manin。

## 复现

```bash
PYTHONPATH=src PARI_MT_ENGINE=single uv run python \
  scripts/theory/heegner_vs_factor_decider.py --max-hyp 500 --with-rank
```

## 参考

- `src/rational_distance/concordant/factor_search.py`（穷尽因子枚举，自证完整）
- `src/rational_distance/proof_status/methods.py`（`run_factor_concordant` 在
  `run_heegner_height` 之前；`DEFAULT_METHOD_PIPELINE`）
- `docs/MATH.md` §8.3（concordant 目标是**整数** N）、§8.5（concordant N 存在但不闭合）
- wl077 / OPEN_DIRECTIONS B.6（height-bound obstruction 已关闭）
- wl078-079（path B uniform mod p² 已关闭）、wl090（F.2 Chabauty 工具调研）
