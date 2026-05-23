# 037 — Finite-descent on 320 hard_case (Peschmann §7(2) 风格)

**日期**: 2026-05-23
**触发原因**: worklog 036 结尾给出三条 worklog 037 候选路线，用户选了
"finite-descent on hard_case enumeration"。本 worklog 实现两层 modular
search，把 d19 的"无 chain solution" effective bound 从 $N \leq 10^5$ 推到
$N \leq 10^8$。
**输出**: 2 个新脚本 + 2 个 JSONL + 严格 effective bound 的实证 lemma。

---

## 一、设计：两层 modular search

Peschmann 2026 §7(2) 在 5 个 hard cuboid specialisation 上做了 "175,418
lattice points × 45 primes < 200" 的 modular search，得到 0 candidate。
d19 的对应物分两层：

### Layer 1: per-prime universal blocker probe（cheap）

对每个 hard_case $(A, B)$ 和每个 prime $p < 200$，问"是否存在残余
$n \bmod p$ 使 $n^2+A^2$ 和 $n^2+B^2$ **同时**是 mod $p$ 平方"。
如果对某 $p$ 这个集合空 → universal obstruction（不需要 N 上界）。

如果不存在 universal blocker，记录 `log_density = ∑ log(|allowed_p|/p)`
作为 Hardy-Littlewood-style heuristic：
- $|\text{allowed}| / M \approx e^{\text{log\_density}}$
- 期待 N ≤ $N_{\max}$ 范围内的候选数 ≈ $e^{\text{log\_density}} \cdot N_{\max}$

### Layer 2: CRT-merged enumeration（expensive but exact）

对小 prime 集 $P_{\text{small}} = \{2, 3, 5, 7, 11, 13\}$，构造 mod
$M = 30030$ 的联合允许集 `allowed_M`。然后在 $N \in [1, N_{\max}]$ 范围内
**只枚举属于 allowed_M 残余类的 N**，对每个做精确平方判定 + 4-chain closure
检查。

这是 Peschmann §7(2) lattice search 的简化版（用 6 primes 代替他的 45 primes，
但保留枚举本质）。

## 二、Layer 1 结果（all 320 hard_case，0.1s）

```
Using 46 primes <= 200
Loaded 320 hard_case pairs

  blocked (universal obstruction): 0
  passing                        : 320

log_density distribution among passing pairs:
  min:    -61.294
  10 %ile: -59.553
  median: -57.643
  90 %ile: -56.048
  max:    -53.991
```

### 解读

- **0 个 universal blocker**：所有 320 hard_case 在每个 $p < 200$ 都有非空
  allowed 残余集。这跟 worklog 035 的理论分析一致——chain candidate 在 dual
  EC 上自动落入 trivial 2-descent class，所以 simple Selmer obstruction 必然
  失效。
- **log_density 集中在 [-61, -54]**：median ≈ $e^{-58} \approx 10^{-25}$。
  Heuristic 上意味着要 $N_{\max} \sim 10^{25}$ 才期待出现 1 个候选——远超
  brute-force enumeration 范围。
- 这跟 d19 项目主线观察一致："半解很多，完整解极少"——concordant N（任意一个
  N 让 $N^2+A^2, N^2+B^2$ 都是平方）密度足够，但满足 chain closure 的 N 几乎
  不可能存在。

## 三、Layer 2 结果（all 320 hard_case × N ≤ $10^8$，58s）

```
Using primes [2, 3, 5, 7, 11, 13]; joint M = 30030
N_max = 100,000,000

  Chain-compatible N found across all pairs: 0
  Pairs blocked by sieve (0 survivors): 0
  Total candidates surviving sieve: 482,077,849
```

**320/320 hard_case 在 $N \leq 10^8$ 范围内 0 chain solution**。这是一个比 d19
现有 ec_bound = $10^5$ 大 1000 倍的严格 effective bound。

### 实证 lemma（worklog 037 主要 deliverable）

> **Lemma (effective)**: 对 max_hyp = 500 的全部 320 个 hard_case $(A, B)$，
> 不存在整数 $N \in [1, 10^8]$ 使得：
> $N^2 + A^2$ 和 $N^2 + B^2$ 都是完全平方，且 $b = A+B-N$ 给出有效 4-chain
> closure（即 $b \geq 1$ 且 $b^2 + A^2$, $b^2 + B^2$ 也都是完全平方）。

证明就是 `scripts/finite_descent_layer2.py` 的运行（58 秒，可复现）。

### 数据样例

| (A, B) | density_M | pass_sieve | concordant_N (≤ 10^8) | chain |
|---|---|---|---|---|
| (7, 45) | 1.26e-02 | 1,258,741 | [24] | 0 |
| (9, 35) | 2.10e-02 | 2,097,902 | [12] | 0 |
| (11, 25) | 1.50e-02 | 1,498,502 | [60] | 0 |
| **(243, 1085)** ← sha2=2 | 1.80e-03 | 179,820 | [3276] | 0 |
| **(3969, 15895)** ← sha2=2 | 2.10e-02 | 2,097,902 | [7140] | 0 |

观察 (243, 1085) 的 concordant N=3276：$b = A + B - N = 243 + 1085 - 3276
= -1948 < 0$，所以 chain closure 自动失败（degenerate）。即使 concordant
条件满足，几何上无效。

## 四、与 Peschmann §7 的对比

| | Peschmann (cuboid) | d19 (chain, wl 037) |
|---|---|---|
| 实验对象 | 5 hard specialisations | 320 hard_case (A, B) |
| 候选 N 数 | 175,418 lattice points | 482M sieve survivors |
| Prime 集 | 45 primes < 200 | 6 primes < 14（CRT layer 2）+ 46 primes < 200（layer 1） |
| 结果 | 0 candidates for $f(P) \in \mathbb{Q}^{*2}$ | 0 chain-compatible N in $N \leq 10^8$ |
| 计算时间 | 不报告 | layer 1: 0.1s; layer 2: 58s |
| 结论 | empirical, 不声称 unconditional 证明 | 同样 — empirical effective bound |

Peschmann 比我们 prime 集大但 candidate 集小（他做 lattice 上的 Mordell-Weil
spans），我们 prime 集小但 candidate 范围大（直接 enumerate $N$）。两条路的
data shape 互补。

## 五、关键观察 / 后续方向

### A. concordant N 几乎全部 degenerate

实测看到的 concordant N（sha2=2 例子如 N=3276）几乎都让 $b = A+B-N$ 变成
非正数，即"概念上的 N"超出了 chain 几何允许范围。这是 chain 问题特有的
constraint，cuboid 没有。

### B. layer 2 可以推到更大 N_max

layer 2 在 $N \leq 10^8$ 用 58s。线性外推：
- $N \leq 10^9$：~10 分钟
- $N \leq 10^{10}$：~2 小时
- $N \leq 10^{12}$：~约 9 天

但 heuristic log_density 暗示就算推到 $N \leq 10^{20}$ 也仅期待 ~1 个 chain
candidate per pair——所以 brute-force 不能给出 unconditional 证明，只能给出
更强的 effective bound。

### C. 对 sha2=2 case 没看到特殊现象

(243, 1085) 和 (3969, 15895) 在 layer 2 表现跟其他 hard_case 相同（找到 1 个
concordant N，degenerate 不能 chain）。Sha[2] 的非平凡性需要更精细的工具
（Cassels-Tate pairing, 或 Quadratic Chabauty）才能转化为 obstruction。

### D. 真正的 unconditional obstruction 仍需 Selmer / Heegner / Brauer-Manin

worklog 035 已经分析过：chain candidate 自动落入 trivial 2-descent class，
所以经典 Selmer obstruction 不直接适用。要严格证明无解，仍然需要：
- **Heegner**（仅 rank=1，118/320 case）：方向五，需 height theory 2-4 周
- **Quadratic Chabauty**（rank ≥ 2）：方向七，长期
- **Brauer-Manin**：方向八，最 powerful 但学术合作级别

worklog 037 的 effective bound（$N \leq 10^8$）作为这些方向的"baseline 实证"
和 paper 的 §X 实验章节是 publishable 的。

---

## 输出物

### 新增脚本
- `scripts/finite_descent_hard_cases.py` — Layer 1: per-prime universal
  blocker probe + log_density 分析
- `scripts/finite_descent_layer2.py` — Layer 2: CRT-merged sieve + N enumeration

### 数据
- `results/finite_descent_hard_cases.jsonl` — 320 case × 46 primes log_density
- `results/finite_descent_layer2.jsonl` — 320 case × $N \leq 10^8$ enum

### 复现命令

```bash
# 1. Layer 1 (universal blocker probe, 0.1s)
uv run python scripts/finite_descent_hard_cases.py

# 2. Layer 2 (CRT mod 30030 + N <= 10^8 enum, 58s)
uv run python scripts/finite_descent_layer2.py \
    --small-prime-bound 14 --n-max 100000000

# 3. Verify with smaller N_max first (3s)
uv run python scripts/finite_descent_layer2.py \
    --small-prime-bound 14 --n-max 1000000
```
