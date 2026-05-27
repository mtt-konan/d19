# Worklog 073: 对偶 closure 筛 + N 侧理论方向

## 背景

本次对话起于两件事：

1. 用户在 `prove_no_solution.py` 中加了 `--moduli minimal` 档位后，发现 fast-core
   阶段送进 PARI 的 pair 数远多于预期，怀疑是 minimal 模数杀伤力不足导致下游
   compute 成本反而上升。
2. 用户希望从理论上找 concordant `N` 的性质，类似已有的 AB 端筛子，最理想是
   把所有可能的 `N` 都用 AB 端筛证伪，从而证明 Harborth 反例不存在。

## 一、模数档位对 fast-core 的影响（实测）

`scripts/prove_no_solution.py --fast-core` 当前流水线：

```
safe_sieve  →  chain_closure_mod_sieve  →  factor_concordant  →  PARI audit
```

`max_hyp=20000` 实测：

| 档位 | 模数数 | mod_sieve 后 | factor 后 (送 PARI) |
|------|-------:|-------------:|--------------------:|
| minimal  | 2  | 26,259 | 10,419 |
| standard | 14 |  3,194 |  1,361 |

`minimal` 在 mod_sieve 阶段省了时间，但下游 survivor 多 7.7 倍，PARI 时间暴增。
**结论**：`--fast-core` 模式应使用 `standard` 或 `balanced`，不要用 `minimal`。

## 二、safe_sieve 推导口径修正

讨论 safe_sieve 的两个条件（A、B 都奇 + `A+B ≡ 0 mod 4`）时，我先给的"基本
concordant 不成立"的解释是错的。具体反例：(5, 16) 在 N=12 处 `12²+5²=13²` 且
`12²+16²=20²` 同时成立，混合奇偶下基本 concordant 是有解的。

正确口径见 `docs/archive/CONCORDANT_SAFE_FILTERS.md`：safe_sieve 检查的是
**完整 4-chain 的 2-adic 必要条件**，要求

```
N² + A² = □
N² + B² = □
b² + A² = □    (b = A+B-N)
b² + B² = □
```

四条同时成立。两条平方关系单独有解，但四条联立时 mod 4 / mod 8 推导给出：

- A 奇 → N、b 都偶 → 进一步 N、b 都 ≡ 0 mod 4
- 若 A、B 奇偶不同，由 `N+b = A+B` 推出 0 mod 4 = 奇 ≠ 0，矛盾
- 若 A、B 都奇，则 `A+B = N+b ≡ 0 mod 4`

(5, 16) 在完整链下 `b = 5+16-12 = 9`，`b²+A² = 81+25 = 106` 非平方，链断。

## 三、concordant N 的性质盘点

### 已实现的筛子

| 名称 | 内容 | 文件 |
|------|------|------|
| `safe_sieve` | AB 2-adic 必要条件 | `concordant/safe_pair_sieve.py` |
| `chain_closure_mod_sieve` | `T(A,B,M) ∩ ((A+B)−T) = ∅`，含 closure 联立 | `concordant/chain_closure_sieve.py` |
| `factor_concordant` | 因子分解穷举所有 concordant N | `concordant/factor_search.py` |
| `multi_n_sieve` | k ≥ 2 必要（closure 需两个 N） | `proof_status/ab_sieve_methods.py` |

### 未做的：对偶视角筛子

按 partner identity（wl054、wl055、`PARTNER_GRAPH_THEORY.md` §2.5）：

```
(A, B) 是 multi-N pair, N_i, N_j ∈ concordant_N(A, B)
⇒ (N_i, N_j) 自身是 multi-N pair, A, B ∈ concordant_N(N_i, N_j)
```

Harborth 反例对称形式：

```
(A, B) 上：∃ N_1, N_2 ∈ concordant_N(A, B)，N_1 + N_2 = A + B
对偶  ：(N_1, N_2) 上：∃ M_1, M_2 ∈ concordant_N(N_1, N_2)，M_1 + M_2 = N_1 + N_2
        其中 M_1 = A, M_2 = B 自动满足
```

因此 (N_1, N_2) 也必须通过 AB 端筛子。这给出**新的必要条件**：

```
对每对 concordant (N_i, N_j) ∈ concordant_N(A, B)：
  把 (N_i, N_j) 约化（除 gcd）后当作新 AB pair
  跑 chain_closure_mod_sieve
  若该对被某 mod p² 杀 → (N_i, N_j) 不能闭合任何 4-chain
若所有 (N_i, N_j) 都被杀 → (A, B) 无 Harborth 反例
```

### 实测：max_hyp=10000 全杀

现有 pipeline 后存活 326 hard_case：

| 子集 | 数量 | 状态 |
|------|------|------|
| k=1（concordant N 只有 1 个） | 325 | closure 需 2 个 N，自动无解；现有主线未接入 `multi_n_sieve` 故没杀 |
| k=2 | 1 | (26611, 680561)，concordant N = [48048, 89148] |

对 (26611, 680561)：

```
N pair = (48048, 89148), gcd = 12
约化后  = (4004, 7429)
对偶 chain_closure_mod_sieve: 在 M = 53² = 2809 上被杀
```

**结论**：max_hyp=10000 范围内，`safe_sieve + chain_closure_mod_sieve +
factor_concordant + multi_n_sieve + 对偶 closure 筛`= 0 hard_case。整个搜索范围
仅靠纯模算术即可全部排除，不需要 PARI / Heegner / rank。

## 四、N 侧理论方向（务实路径）

用户提出的根本方向：找出 N 的代数/数论性质，用 AB 端筛把所有可能的 N 全部
排除，从而证明反例不存在。

### N 已知性质（理论上已证）

1. mod 8 推导：`N ≡ 0 mod 4`（同样 `b ≡ 0 mod 4`）
2. `factor_search` 给出 N 是有限可枚举集，来自 `B²−A²` 的因子分解
3. partner identity：`(N_i, N_j)` 自身是 multi-N pair
4. Ono 1996：每个 N 对应 `E_{A,B}` 上的 square-x 点 `P_N ∈ 2E(ℚ)`，
   存在 half-point `Q_N`

### 核心理论命题（待证 / 待否）

存在一个有限模数集 `M = {p_1², ..., p_k²}` 使得对任意 reduced `(A, B)`
（A、B 奇、`A+B ≡ 0 mod 4`），下列至少一条成立：

```
(a) chain_closure_mod_sieve(M) 杀 (A, B) 自身
(b) 对每对 (N_i, N_j) ∈ concordant_N(A, B) 经约化，
    chain_closure_mod_sieve(M) 至少杀其中一对
```

若该命题成立，Harborth 反例不存在被严格证明（除有限 small case 外）。

### 务实路径

```
路径 1: 实证扩展                                          [短期，立即可做]
  - 实现 dual_chain_closure_mod_sieve
  - 接入 DEFAULT_METHOD_PIPELINE (附带把 multi_n_sieve 也接上)
  - 跑 max_hyp = 20k / 50k / 100k，看是否仍 0 survivor
  - 若仍 0 → paper-grade lemma：max_hyp ≤ X 的 Harborth 反例
    可纯模算术证否

路径 2: 解析数论估计                                       [中期，1-2 周]
  - 分析对偶筛在 mod p² 上的失败概率
  - 看能否解析地证明"足够大 (A, B) 必被某筛杀"

路径 3: 因子结构 → mod 关联定理                            [中期，2-4 周]
  - (A, B) → (N_i, N_j) 的 mod p² 映射写显式
  - 因 (N_i, N_j) 由 B²−A² 的因子分解决定，
    其 mod p² 行为完全由 (A mod p², B mod p²) 决定
  - 寻找一个固定模数集的覆盖性证明

路径 4: 椭圆曲线 height + Selmer + Brauer-Manin           [长期]
  - 见 docs/THEORY_DIRECTIONS_ADVANCED.md
  - Heegner（rank=1，118/320 case）
  - Quadratic Chabauty（rank ≥ 2）
  - Brauer-Manin obstruction
```

### 路径 1 实施（multi-N-first + 对偶筛）

实现要点：

```
src/rational_distance/concordant/dual_closure_sieve.py
  - dual_pair_killed(N_i, N_j, moduli)
      reduce by gcd, run chain_closure_mod_sieve, return killer modulus or None
  - all_n_pairs_killed(ns, moduli)
  - find_surviving_n_pair(ns, moduli)

scripts/prove_no_solution_multi_first.py
  pipeline:
    1. fast_multi_concordant_pairs(max_hyp)   # 直接生成 multi-N 候选
    2. allow_reduced_pair                     # 2-adic safe filter
    3. chain_closure_mod_sieve on (A, B)      # primary closure
    4. find_surviving_n_pair on ns            # dual closure on N pairs
    5. survivors → 上层方法（PARI 等）
```

测试 `tests/test_dual_closure_sieve.py`：7 项全部通过，包含
(26611, 680561) 在 mod 53² 上被 dual 杀的 regression case。

### 生成器优化（multi-N 候选生成的瓶颈攻关）

wl048 第 5 项 follow-up：「若需要 max_hyp 推到 100k+，再优化 `iter_concordant_a_n`
（现在每个 A 是 O(A) 的 trial division）」。本 wl 把这一步做了：

1. **线性筛 SPF 表**：`_build_smallest_prime_factor(max_leg)` 一次性 O(max_leg)
   建表，每个 A 的因子分解从 O(√A) trial division 降到 O(log A)。
2. **A² divisor 枚举去 sort**：`_smaller_divisors_from_factors` 用 list
   comprehension 在 C 层一次性展开所有素因子幂次，去掉了原版的 sorted。
3. **配对阶段奇偶预过滤**：multi-N 配对里 (even, even) 对 gcd 必 ≥ 2，
   直接跳过，gcd 调用数从 42.6M 降到 20.7M（节省一半）。

`fast_multi_concordant_pairs(1_000_000)` 由 ~75s 降到 ~45s（**1.68× 加速**）。
进一步加速需要 numpy 向量化或 C 扩展。

### 实测结果（unconditional 全杀，含优化后耗时）

| max_hyp | multi-N | safe killed | primary killed | dual killed | survivors | 总耗时 |
|---:|---:|---:|---:|---:|---:|---:|
|    10,000 |     854 |    830 |     24 |  0 | **0** |  0.10s |
|    20,000 |   1,848 |  1,794 |     54 |  0 | **0** |  0.30s |
|    50,000 |   4,968 |  4,818 |    150 |  0 | **0** |  0.80s |
|   100,000 |  10,333 | 10,053 |    280 |  0 | **0** |  1.74s |
|   500,000 |  54,414 | 53,300 |  1,113 |  1 | **0** | 14.14s |
| **1,000,000** | 111,090 | 109,183 | 1,901 |  6 | **0** | **44.57s** |
| **2,000,000** | 226,120 | 222,922 | 3,182 | 16 | **0** | **424.66s** |

观察：

1. `max_hyp ≤ 100k`：`safe_sieve + chain_closure_mod_sieve on (A,B)` 已经全杀，
   对偶筛贡献为 0。
2. `max_hyp ≥ 200k`：对偶筛开始抓到 primary 漏掉的 case（500k 1 个、1M 6 个、
   2M 16 个）。**对偶筛是 200k 以上不可缺的安全网**，且其贡献量随 max_hyp 增长。
3. `max_hyp = 2,000,000`：0 survivor，425 秒。瓶颈仍在 `fast_multi_concordant_pairs`
   （sieve 本身仅 0.07s）。
4. 全程 unconditional：纯 2-adic + mod p² 必要条件，不依赖 PARI / rank /
   Heegner。

### 实证 lemma（worklog 073 主要 deliverable）

> **Lemma (effective, unconditional mod p² descent)**: 对 `max_hyp ≤ 2,000,000`
> 的所有 reduced coprime pair `(A, B)` with `1 ≤ A < B ≤ max_hyp`，**不存在**
> Harborth 4-chain 反例。
>
> 证明：`fast_multi_concordant_pairs(2,000,000)` 给出全部 226,120 个 multi-N
> 候选；其中 222,922 个被 safe_sieve（2-adic 必要条件）排除，3,182 个被
> `chain_closure_mod_sieve(STANDARD_MODULI)` 直接排除，16 个被对偶
> chain_closure_mod_sieve（同一组模数）排除。`k < 2` 的 pair 因 closure 需要
> 两个不同的 concordant N 而平凡排除。

复现命令：

```bash
uv run python scripts/prove_no_solution_multi_first.py \
    --max-hyp 2000000 --moduli standard --workers 1 \
    --json-out results/dual_closure_max2000000.json
```

### 后续

- 把 `multi_n_sieve`（k ≥ 2 必要条件）接入主线 `DEFAULT_METHOD_PIPELINE`
- 进一步加速 `fast_multi_concordant_pairs`（已 1.68× 提速；剩余瓶颈是 Python
  解释器循环本身，需要 numpy 向量化或 C 扩展才能再翻倍）
- 把 `max_hyp ≤ 10^7` 范围拉进 unconditional 证否
- 路径 2 / 3：把"对偶筛对所有 (A, B) 总能杀"做成解析定理
- 路径 4：survivor（万一未来某 max_hyp 出现）转 PARI / Heegner / Selmer 处理

## 五、文件 / 引用

```text
docs/archive/CONCORDANT_SAFE_FILTERS.md   safe_sieve 完整推导
docs/MULTI_CONCORDANT_N_STRATEGY.md       multi-N 主线 + closure 任务 C
docs/PARTNER_GRAPH_THEORY.md              partner identity / G_M / K_n
docs/THEORY_DIRECTIONS_ADVANCED.md        Heegner / Chabauty / BM obstruction
docs/work-logs/040-chain-closure-mod-sieve.md  chain_closure_mod_sieve
docs/work-logs/054-partner-pair-graph-analysis.md  partner identity 起源
src/rational_distance/concordant/chain_closure_sieve.py  现有联立筛
src/rational_distance/concordant/factor_search.py        N 穷举
src/rational_distance/concordant/fast_multi_n.py         multi-N pivot-on-N 生成器
src/rational_distance/concordant/dual_closure_sieve.py   对偶筛 (本 wl 新增)
src/rational_distance/proof_status/ab_sieve_methods.py   multi_n_sieve（实验态）
scripts/prove_no_solution_multi_first.py                 multi-N-first driver (本 wl 新增)
tests/test_dual_closure_sieve.py                          对偶筛回归测试 (本 wl 新增)
results/dual_closure_max{10000,...,1000000}.json         实测全杀数据 (本 wl 新增)
```
