# wl080 — Path B 收尾 + wl073–wl079 阶段总结

承接 wl079（phase 4a/4b 否定结果）。本 wl 不引入新工作，只做**两件事**:

1. 把 path B 这条线**正式关闭**（标记为不再投入）
2. 把最近 7 个 wl (073–079) 的实际产出按"实证 / 工程 / 理论 / 否定"分类
   汇总，避免重复造轮子

## 一、关闭 path B 的理由

path B 的目标: 找 finite `M_0 ⊂ N` 使

> ∀ primitive safe-pass multi-N (A, B), 存在 `m ∈ M_0` 让
> `chain_closure_mod_sieve(A, B, m) = killed` (or dual partner killed)

实证已经在 wl073 验证 max_hyp ≤ 2M 上 100% 用 `M_0 = STANDARD_MODULI`
（14 个 prime²）覆盖。但 wl078–wl079 的 audit + 枚举 + 代数推测全部表明:

- **mod-p² primary 永远剩 surviving**（CRT，wl078 §10）即使把所有
  prime² ≤ 47² 都用上仍剩 0.017% (a, b) class 未杀。
- **`v_p(D) ≠ 1` 等简单 closed-form 必要条件 fail**（wl079）：所有
  prime ∈ {3,5,…,31} 上 13–25% multi-N 实际满足 `v_p(D)=1`。
- **mod 9 唯一干净的 lemma 是 trivial**: `unused S_9 = {(3i, 3j)}` 
  本质等价于 primitivity 假设，无新约束。
- 严格证明只能 prime-by-prime 推每个 chain_closure 的 quadratic-residue
  约束 — 没有 algebraic shortcut。

⟹ path B 在当前理论工具链下没有进一步可达的进展，正式**关闭**。

## 二、wl073–wl079 实际产出汇总

按"对穷举有用 / 对证明有用 / 否定结果"分类。

### 2.1 对穷举有用（**工程进展，可被后续直接调用**）

| 项 | wl | 文件 |
|----|----|----|
| `dual_closure_sieve` 实现 + 6/16 dual-only pair 证据 | 073 / 078 | `src/rational_distance/concordant/dual_closure_sieve.py` |
| `fast_multi_concordant_pairs`（SPF 因子分解 + pivot-on-N 枚举优化） | 073 | `src/rational_distance/concordant/fast_multi_n.py` |
| `prove_no_solution_multi_first` driver（multi-N-first pipeline） | 073 | `scripts/prove_no_solution_multi_first.py` |
| `uniform_mod_p2_audit` audit 工具 | 078 | `scripts/uniform_mod_p2_audit.py` |
| audit 数据 dump (max_hyp=1M, 2M) | 078 / 079 | `results/uniform_mod_p2_max{1m,2m}.jsonl` |
| `enumerate_mod_p2_classes` / `enumerate_mod_p2_crt`（CRT-style 枚举工具） | 078 | `scripts/enumerate_mod_p2_{classes,crt}.py` |

**实证全杀已验证范围**: max_hyp ≤ 2,000,000，226k safe-pass multi-N pair
全部被 primary + dual chain_closure 杀。dual sieve 不可省 (max_hyp=1M
6 个 dual-only pair, max_hyp=2M 16 个)。

### 2.2 对证明有用（实证支撑，**未升级为严格证明**）

| 项 | wl | 现状 |
|----|----|------|
| Conjecture A1 实证 (k=2 → rank ≥ 2) 1879/1879 | 074 / 076 | PARI ellrank + F₂-rank 2-descent 双验证, max_hyp=1M |
| A1 严格证明 sketch (half-point doubling + 2-descent map δ) | 076 | mechanism 写出来了, **未完整形式化** |
| F₂-rank 2-descent 实证脚本 | 076 | `scripts/analyze_k2_f2_rank.py`, 实测每对 mod E[2] image 独立 |

A1 的严格证明仍是**最有希望突破**的方向，但本轮没启动。

### 2.3 否定结果（**已排除的错误路线**）

| 项 | wl | 原因 |
|----|----|------|
| 方向 2 height-bound 假设 (`min ĥ(P_{N_i}) > 2 log(A+B)`) | 077 | 实证全部 fail，反例从 max_hyp=1k 起就有 |
| Conjecture B.p² (`v_p(B²-A²) ≠ 1`) | 079 | 全 10 prime 上 fail (13–25% multi-N 满足 v_p=1) |
| path B 简单 mod-p² obstruction (单靠 `M_0` cover 全空间) | 078 / 079 | CRT 表明永远剩 ≥ 0.017% (a,b) class |

### 2.4 文档/sketches（理论梳理）

| 项 | wl |
|----|----|
| 多 concordant N 与 K_{2,2} 等价 + 椭圆曲线 fiber 关系 | 073 |
| Path A vs Path B 选择讨论 | 075 |
| 文献注记: Ono 1996, Halbeisen-Hungerbühler 2021 | 073 / 075 |

## 三、当前实证上限 + 工程瓶颈

```
max_hyp = 1,000,000:  fast_multi_concordant_pairs ~30s  + audit ~1min
max_hyp = 2,000,000:  ~4 min total
max_hyp = 5,000,000:  ~25-30 min (估计, 没跑完, 5M jsonl 未生成)
```

工程瓶颈是 `fast_multi_concordant_pairs` 的 N 枚举和 chain_closure 的
mod-p² 检查在 max_hyp=5M+ 上未优化。要推到 max_hyp ≥ 5M 必须先做工程优化:

- N 枚举的并行化（pivot-on-N 不易并行，可改 chunk-on-A 并行）
- chain_closure_mod_sieve 的 (a, b, m) 三层 loop 用 numpy / Cython 重写
- 数据本身的 incremental cache (max_hyp=1M dump → 增量到 2M, 5M)

## 四、下一轮可考虑的方向（**本 wl 不做**）

### 4.1 path A 严格证明（最有希望）

把 wl076 的 A1 sketch 完整形式化:

- δ map E(ℚ)/2E(ℚ) → (ℚ\*/ℚ*²)² 的代数描述
- 半点 P_{N_i} 的 signature 计算（已实证 mod E[2] independent）
- 半点 sum 不在 E[2] image ⟹ rank ≥ 2 的代数推导
- 与 Halbeisen-Hungerbühler 2021 的 K_{2,2} 等价定理 + Ono 1996 rank-0
  family 矛盾（即 multi-N k=2 ↔ rank ≥ 2 但 closure 在 rank ≥ 2 fiber 上
  也不存在）

风险: closure-fiber 上有理点 finiteness 仍需独立工具 (Chabauty / Mordell-
Weil sieve)。

### 4.2 工程加速：max_hyp 推到 5M / 10M+

不为了证明，纯为了实证范围扩大:

- profile + 优化 `fast_multi_concordant_pairs` (大 N 范围)
- 并行 audit
- 这能给 path A 提供更广的实证支撑

### 4.3 其他长尾

- chain_db 升级（增量缓存 + cross-run sharing）
- 文献深挖：Stoll-Bruin、Mazur uniform bound 是否能用于 closure 闭包
- 看 K4/K5 的 partner identity 能否 push 类似 path A 的论证到更高 k

## 五、本轮工作量与价值评估

| 维度 | 评分 | 说明 |
|------|------|------|
| 穷举上限突破 | ❌ | max_hyp 仍是 wl073 的 ~2M |
| 严格证明进展 | ❌ | A1 sketch 仍未形式化, B 路被否定 |
| 排除错误路线 | ✅ | height-bound + Conjecture B.p² + path B 简单形式都被否决 |
| 工程基础设施 | ⚪ | audit 工具 / CRT enumeration 工具新增, 未来可用 |
| 文档 | ✅ | 7 个 wl 把 path B 全过程留档, 后续不会重做 |

**净结论**: 本轮主要价值是**关闭错误路线**，避免后续再投入。穷举与证明
的实质突破都没有。下一轮应聚焦 path A 严格证明 OR 工程加速 5M。

## 六、状态

- ✅ Path B 关闭, 不再投入
- ✅ wl073–wl079 阶段汇总完成
- ⏸ Path A 严格证明（已 sketch，未形式化, 暂搁置）
- ⏸ 工程加速（暂搁置）
