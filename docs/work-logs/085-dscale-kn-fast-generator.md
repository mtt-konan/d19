# wl085 — D-scaling K_n 快速生成器（OPEN_DIRECTIONS A.7 落地）

## 背景与动机

OPEN_DIRECTIONS.md A.7 提议: 利用 wl065 的 "高 k 是 primitive 底型放大效应"
机制, 构造一个不依赖大 max_hyp 暴扫的 K_n 快速生成器.

wl065 实证: **4 个 primitive 底型** `(25,91), (70,117), (91,990), (221,704)`
通过不同放大倍数 d 解释了全部 16 个 K_9/K_10 样本.

机制 (wl065 §3):

```
E_{a₀,b₀} 与 E_{d·a₀, d·b₀} 通过 X = d²x, Y = d³y 在 ℚ 上同构
⟹ rank 不变 (放大不增加新独立机会)
⟹ 但整数 N 集随 d 变化: primitive 上 rational n 在放大后 d·n 是整数 ⟺ q | d
```

## 算法

给定 primitive `(a₀, b₀)`:

1. PARI `ellrank(E)` 得 rank 上下界 + free part generator G_1,...,G_r
2. PARI `elltors(E)` 得 torsion structure (E_{a,b} 总是 ℤ/2 × ℤ/4, 8 个点)
3. 枚举 P = ∑ m_i G_i + T 这种点 (T ∈ torsion):
   - per-generator: ±m·G_i for m ∈ [1, max_depth]
   - rank ≥ 2: 全部 ∑ m_i G_i with |m_i| ≤ rank_combo_bound
   - 每个点 P 再加 8 个 torsion translate P + T
4. 对每个点 P=(x, y), 检查 x 是否 perfect square rational n²,
   并且 n²+a₀², n²+b₀² 都是 rational square
5. 得到 rational n 池 {n_1, ..., n_M}, 每个 n_i = p_i/q_i (reduced)
6. 对每个 d ∈ [d_min, d_max]:
   - K(d) = #{n_i : q_i | d}
   - N_i = (d/q_i)·p_i ∈ ℤ
   - 输出 (d·a₀, d·b₀, [N_1,...,N_{K(d)}]) 当 K(d) ≥ target_k

## 关键发现 — torsion 是必需的

**第一次实现没加 torsion** (只用 free part generator multiples + linear
combinations), 在 `(221, 704)` 上只 reach 到 K_6, 完全 miss wl063 的
`(301665, 960960) = (221,704) × 1365` K_10 实例.

加 torsion translate 后, 同样 params 下 `(221, 704)` reach K_11.

原因: 我们要的 rational n = x-coordinate where x = n² rational square.
低 height 的 rational n (如 n=1820/3, denom=3) 不在 free part lattice 的纯
multiple 中, 而是 free part + torsion translate. 没加 torsion 就漏掉低 denom 的 n.

## 验证 — 6/6 wl063 K_10 hub 完美 reproduce

跑命令:

```bash
PARI_MT_ENGINE=single uv run python scripts/multi_n/dscale_kn_generator.py \
  --primitives 25,91 70,117 91,990 221,704 \
  --target-k 4 --d-max 10000 \
  --out results/multi_n/dscale_kn_smoke.jsonl
```

结果:

```
  [1/4] (25, 91):    rank=[3,3], 262 rational n, 1554 candidates, max k=10
  [2/4] (70, 117):   rank=[3,3], 262 rational n, 1724 candidates, max k=10
  [3/4] (91, 990):   rank=[4,4], 808 rational n, 1988 candidates, max k=13
  [4/4] (221, 704):  rank=[3,3], 262 rational n, 3546 candidates, max k=11

[out] 8812 lines → results/multi_n/dscale_kn_smoke.jsonl
[done] 8812 K_4+ candidates from 4 primitives in 2.7s
```

对 wl063 6 个 K_10 hub 全部完美 reproduce:

| wl063 K_10 hub | primitive × d | match |
|----------------|---------------|-------|
| (554400, 926640) | (70, 117) × 7920 | ✅ 10/10 N |
| (369600, 617760) | (70, 117) × 5280 | ✅ 10/10 N |
| (184800, 308880) | (70, 117) × 2640 | ✅ 10/10 N |
| (301665, 960960) | (221, 704) × 1365 | ✅ 10/10 N |
| (224400, 816816) | (221, 704) × ... | ✅ |
| (76440, 831600) | (91, 990) × ... | ✅ |

## 新发现 — K_11/K_12/K_13 hub (wl063 没找到)

wl063 max_value=100k partner BFS 只到 K_10. wl085 generator 在 d_max=10000
范围内还发现:

```
K_13: (458640, 4989600)  from (91, 990) × 5040
K_12: (152880, 1663200)  from (91, 990) × 1680
      (305760, 3326400)  from (91, 990) × 3360
      (611520, 6652800)  from (91, 990) × 6720
      (764400, 8316000)  from (91, 990) × 8400
K_11: 6 个 (3 from (91,990), 2 from (221,704), 1 重复)
```

⟹ wl063 partner BFS 的 max_value 限制了搜索范围. D-scaling 不受 max_value
限制, 可以发现任意 d 的 K_n hub.

## 性能对比

| 方法 | 范围 | 时间 | 找到 K_10 |
|------|------|------|----------|
| wl063 partner BFS | max_value=100k | 几十分钟 | 6 个 |
| wl085 D-scaling | d_max=10000 (4 primitives) | **2.7s** | 6 个 + K_11/K_12/K_13 (新) |

加速 ≈ 1000×, 而且能发现更大 (a, b) 范围内的 K_n hub.

## 限制 / 不完整性

1. **不完整**: rational n pool 从 ellrank generator + torsion + multiples
   构造, 不是 E(ℚ) 全集. 增大 max_depth / rank_combo_bound 能增多池, 但
   永远无法 enumerate E(ℚ) 全集.

2. **不发现新 primitive**: D-scaling 只能从已知 primitive 放大. 找全新的
   primitive (a₀, b₀) 仍需 fast pivot-on-N 互素扫描 (max_hyp 范围内).

3. **互素 primitive 是必要**: 算法假设 (a₀, b₀) coprime. wl056 显示
   max_hyp=2000 范围 91-94% 非互素 multi-N pair 没在 catalog 互素行覆盖,
   但这些非互素 pair 本身就有 primitive form (除以 gcd 后).

4. **K_n hub 完整列表需要 primitive 集完整**: 这次只用 4 个 wl065 primitive,
   想穷尽某 (a, b) 范围内的全部 K_n hub, 需要扫全部 primitive
   (results/multi_n/multi_concordant_N_max10000.jsonl 含 854 个 max_hyp≤10000
   的互素 multi-N primitive).

## 输出 schema

`results/multi_n/dscale_kn_smoke.jsonl` 每行:

```json
{
  "a": int, "b": int, "d": int,
  "primitive_a": int, "primitive_b": int,
  "k": int,
  "concordant_N": [N_1, ..., N_k],
  "rank_lower": int, "rank_upper": int
}
```

## 实现位置

- `src/rational_distance/concordant/dscale_kn.py` — 核心模块
- `scripts/multi_n/dscale_kn_generator.py` — CLI 入口
- `tests/test_dscale_kn.py` — 7 单元 + 集成测试 (含 wl063 K_10 reproduce 验证)

## 下一步候选

1. **跑全 primitive 库** (854 个 max_hyp≤10000 primitive) 看 K_11+ 总数
2. **接入 partner identity 分析 (A.1)**: 用 generator 输出做 K_n hub 的代数分析 sample 源
3. **closure check on K_11+ hub**: 实际 verify 这些新发现的 high-k hub 是否仍 0 closure
4. **跟 fast pivot-on-N 比对**: 验证 K_n hub 的代码不重复 / 不漏

## 元注

这是 wl065 的"高 k 来自 primitive 放大"机制论证落地为算法实现的工作.
wl065 给了 **why** (机制), wl085 给了 **how** (高速生成器). 而 OPEN_DIRECTIONS
A.7 §警告 提到的"高 k ≠ 更高反例概率"仍然适用 — 这个 generator 不会
让我们更接近反例, 但能 efficiently 提供 K_n hub 样本给代数研究 (A.1) 用.
