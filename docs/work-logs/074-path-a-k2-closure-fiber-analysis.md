# wl074 — Path A: k=2 closure fiber analysis

承接 wl073（multi-N-first + 对偶筛实现 max_hyp ≤ 2M 全杀）。本 wl 切到
**理论路径 A**：试图证明"k=2 closure 必失败"，即对**所有** reduced coprime
safe-pass 的 multi-N pair `(A, B)` 满足 `concordant_N(A, B) = {N_1, N_2}` 时，
`N_1 + N_2 ≠ A + B` 是个 unconditional 定理（不依赖 max_hyp）。

为什么挑 k=2：wl062 数据，comp 0 中 **63.77% 顶点是 k=2**（197,488 个）；
整体 max_hyp=200k 实测 **99.3% 的 multi-N pair 是 k=2**。证完 k=2 直接覆盖
绝大多数候选。

## 一、数学 setup

固定 reduced coprime `(A, B)` 通过 safe sieve（A 奇, B 奇, `(A+B) % 4 == 0`）。
设 `S := A + B`。假设存在 k=2 closure 反例：

```
(1)  N_1² + A² = α²
(2)  N_1² + B² = β²
(3)  N_2² + A² = γ²
(4)  N_2² + B² = δ²
(5)  N_1 + N_2 = S    （closure）
```

7 个未知数 `(N_1, N_2, α, β, γ, δ)` minus 5 方程 = 2 维参数化；加上 (A, B)
是参数，每个具体 (A, B) 给出 1 维代数曲线 `C(A, B)`。

用 (5) 消 `N_2 = S - N_1`，得到 1 维代数曲线
`C(A, B) ⊂ Spec Z[N_1, α, β, γ, δ]`。

### 1.1 第一个 nontrivial identity

```
(1) - (3):  N_1² - N_2² = α² - γ²
            ⟺ (N_1 - N_2)(N_1 + N_2) = α² - γ²
            ⟺ (2N_1 - S) · S = α² - γ²       （代 N_2 = S - N_1）
(2) - (4):  N_1² - N_2² = β² - δ²
            ⟺ (2N_1 - S) · S = β² - δ²

⟹  α² - γ² = β² - δ²
⟹  α² + δ² = β² + γ²       ★ identity I
```

`(α, β, γ, δ)` 锁在 surface `x² + y² = z² + w²` 上。这是个**双有理 trivial** 的
surface（参数化为 `x = ac + bd, y = ad - bc, z = ac - bd, w = ad + bc`），但
配合下面的 identity II 后会变得 nontrivial。

### 1.2 第二个 identity

```
(1) - (2):  A² - B² = α² - β²
(3) - (4):  A² - B² = γ² - δ²

(α - β)(α + β) = (A - B) · S = (γ - δ)(γ + δ)    ★ identity II
```

`(α, β)` 和 `(γ, δ)` 都是 `(A-B) · S` 的"signed factorization pair"，并且
它们必须互相满足 identity I。

### 1.3 关键观察：(α, β, γ, δ) 在小代数空间

设 `D := A - B` （这里 D < 0 因为 A < B；取 |D|·S 也可），`T := |D| · S`。

```
α + β =: p          α - β =: q     pq = ±T   （p, q 同号或异号取决于 D 符号）
γ + δ =: r          γ - δ =: s     rs = ±T
```

identity I 给出：
```
α² + δ² = β² + γ²
⟺ (α-β)(α+β) = (γ-δ)(γ+δ) - 2(β² - γ²)       … 这条还不够干净
```

直接展开：
```
α² + δ² = β² + γ²
((p+q)/2)² + ((r-s)/2)² = ((p-q)/2)² + ((r+s)/2)²
⟹ pq - rs = -pq + rs           … 因为 (p+q)² - (p-q)² = 4pq, (r-s)² - (r+s)² = -4rs
⟹ 2pq = 2rs
⟹ pq = rs

但 pq = ±T 且 rs = ±T，所以 pq = rs 自动成立（同号）。

⟹ identity I 在 identity II 的前提下**自动成立**，没有给出新约束。
```

所以 (α, β, γ, δ) 的自由度其实只由 identity II 给出：`(p, q)` 是 T 的
factorization，`(r, s)` 是 T 的（另一个）factorization。

### 1.4 N_1 的约束（来自 (1)）

```
N_1² = α² - A² = ((p+q)/2)² - A²
```

要 `N_1` 为整数（或至少为非零有理数 → Z[1/2]），需要 `(p+q)/2 ≥ A` 且
`((p+q)/2)² - A² = N_1²` 是平方。

这条 ≡ 在 T = |D|·S 的某个 factorization 下，对应 (A, B, p, q) 满足
Pell-type 关系。

### 1.5 重新参数化（Pythagorean triple 视角）

(1) `N_1² + A² = α²` 是 Pythagorean triple. 用标准参数化：
```
N_1 = k(m² - n²) 或 2kmn,  A = 2kmn 或 k(m² - n²),  α = k(m² + n²)
```
（k, m, n ∈ Z, gcd(m, n) = 1, m > n > 0, m, n 不同奇偶）

A 是奇数（safe sieve），所以 `A = k(m² - n²)` (k 奇)，`N_1 = 2kmn`. 类似
(2) 给一个对 (m', n', k') 描述 B = k'(m'² - n'²) 和同一个 N_1 = 2k'm'n'.

⟹ `2kmn = 2k'm'n'` ⟹ `k m n = k' m' n'`. 这是 N_1 同时出现在两个
Pythagorean triple 里的条件。

`(N_1, A, B)` 满足"N_1 是 (A, ?) 的腿且 N_1 是 (B, ?) 的腿"⟺ N_1 ∈
concordant_N(A, B). 这个条件本身就是 multi-N 定义。

### 1.6 进一步压缩

由 (1)(2)：α² - β² = A² - B² = D · S, 即 α² - β² + D · S = 0. 这是固定
的 conic。同样 γ² - δ² + D · S = 0.

由 (1)(3)：(N_1 - N_2)(N_1 + N_2) = α² - γ². 用 (5) `N_1 - N_2 = 2 N_1 - S`,
得 `(2 N_1 - S) S = α² - γ²`. 设 `t := 2 N_1 - S`（"closure deviation"），
则 **`tS = α² - γ²`** 且同样 **`tS = β² - δ²`**.

所以核心系统：
```
α² = N_1² + A²            （Pythagorean）
β² = N_1² + B²            （Pythagorean）
γ² = α² - tS              （由 t 定义）
δ² = β² - tS              （由 t 定义）

t = 2 N_1 - S
γ² + δ² = α² + β² - 2tS  ⟹  γ² + δ² + 2tS = α² + β²

但 α² + β² = 2 N_1² + A² + B², 而 γ² + δ² = 2 N_2² + A² + B² =
2(S - N_1)² + A² + B² = 2 N_1² - 4 N_1 S + 2 S² + A² + B².

所以 (γ² + δ²) - (α² + β²) = -4 N_1 S + 2 S² = 2 S (S - 2 N_1) = -2tS.

与 γ² + δ² + 2tS = α² + β² 一致 ✓ — 同义反复，没新约束。
```

⟹ **核心是 (1)(2) 的 Pythagorean 系统 + α² - γ² = tS 是 perfect square**.

### 1.7 把 closure 翻译成单条 elliptic 条件

设 (1)(2) 给出 N_1 ∈ concordant_N(A, B), 即 N_1² = X 满足 E_{A,B}: Y² =
X(X+A²)(X+B²) 的 square-X 点（Ono Prop 1）。N_2² 同样。

closure 要求 `N_1 + N_2 = S`，即 `√X_1 + √X_2 = S` （取正根，N > 0）。

设 `X_1 = N_1², X_2 = N_2² = (S - N_1)²`. 那 `X_2 = X_1 - 2 N_1 S + S² =
X_1 - S(2N_1 - S) = X_1 - tS`.

把 `Y_1² = X_1(X_1 + A²)(X_1 + B²)` 和 `Y_2² = X_2(X_2 + A²)(X_2 + B²)` =
`(X_1 - tS)(X_1 - tS + A²)(X_1 - tS + B²)` 同时要求。

设 `X = X_1`, `Y_1`, `Y_2` 是两个 dependent variable. 系统：
```
Y_1² = X(X + A²)(X + B²)
Y_2² = (X - tS)(X - tS + A²)(X - tS + B²)
t² S² = (X - X_2)²·... 等等，t 由 X 决定: t = 2√X - S.
```

⟹ 把 t 替换：`X_2 = X_1 - tS = X_1 - (2√X_1 - S) S = X_1 - 2 S √X_1 + S²
= (√X_1 - S)² = (S - √X_1)²`. 自动等于 `(S - N_1)² = N_2²` ✓.

所以系统其实就是：
```
∃ N_1, N_2 ∈ Z>0  s.t.
  N_1² ∈ Sq-X(E_{A,B})   （square-X 点 X-coordinate）
  N_2² ∈ Sq-X(E_{A,B})
  N_1 + N_2 = S
```

### 1.8 用 Ono Prop 1 (Mordell-Weil 视角)

记 `Sq(E) := {N ∈ Z : ∃ P = (N², Y) ∈ E_{A,B}(Q)}`. Ono Prop 1: 每个
`P_N ∈ 2 E(Q)`. 即 `P_N = 2 Q_N` 某 `Q_N ∈ E(Q)`.

closure 条件 ⟺ `∃ N_1, N_2 ∈ Sq(E): N_1 + N_2 = S`.

关键问题：N_1, N_2 这两个**整数**的算术加法约束（N_1 + N_2 = S），在
E(Q) 的群加法下对应什么？

**待研究**：Q_{N_1} + Q_{N_2} 在 E(Q) 上的几何加法，是否锁定到某个特殊
位置（如某个 torsion coset 或 generator 的特定倍数）？

如果实证发现 "Q_{N_1} + Q_{N_2} 必落在某条件 X"，并且能反推到 closure，
则 closure 就翻译成 E(Q) 上的有界检索问题。

## 二、实验路线

写一个脚本 `scripts/analyze_k2_closure_fiber.py`：

1. 从 `results/dual_closure_max*.json` 取若干 k=2 multi-N pair `(A, B, N_1, N_2)`
2. 对每个 pair 构造 `E_{A,B}` 并用 PARI 算：
   - `E(Q)` 的 generator(s)（rank ≥ 1，已知）
   - torsion subgroup
   - `P_{N_1} = (N_1², ...)`, `P_{N_2} = (N_2², ...)`
   - `Q_{N_1}, Q_{N_2}` such that `2 Q_{Ni} = P_{Ni}`（half-points）
   - `Q_{N_1} + Q_{N_2}`（E(Q) 群加法）
3. 同时把 N_1 + N_2 实际值 vs S = A+B 记录（k=2 全实测不闭合，N_1 + N_2 ≠ S）
4. 看 `Q_{N_1} + Q_{N_2}` 落在 E(Q) 的什么位置（X 坐标？torsion？generator 倍数？）
5. 找规律：是否 `Q_{N_1} + Q_{N_2}` 在 N_1 + N_2 = S 与 N_1 + N_2 ≠ S 时有可区分的代数 signature？

## 三、最弱的 Plan B（如果 Q_{N_1} + Q_{N_2} 没规律）

退而求 2-descent 视角：

- `P_{N_1}, P_{N_2}` 都在 `2 E(Q)`. 即 `Q_{N_1}, Q_{N_2}` 都是 half-points
- 它们在 `E(Q)/2 E(Q) = Sel^{(2)}(E) modulo Sha[2]` 的 F_2 image 是什么？
- F_2-rank dimension 跟 N_i 数（k）的关系（wl048 已实测 k=4 时 F2-rank 通常 = k 或 k-1）
- 在 k=2 时，F2-rank 通常 2 或 1
- closure 条件 N_1 + N_2 = S 是否强制特殊的 F2 linear dependency？

## 四、若实证发现规律

把规律抽象成定理候选，然后：

1. 在更大 k=2 sample 上验证（万级）
2. 写出代数证明 sketch
3. 写论文向 deliverable

## 五、文件 / 引用

```
docs/MULTI_CONCORDANT_N_STRATEGY.md      closure 任务 C 原始定义
docs/PARTNER_GRAPH_THEORY.md             partner identity + Ono Prop 1
docs/work-logs/048-fast-pivot-on-n-scanner.md  k=4 pair 的 F2-rank 实测
docs/work-logs/060-...                   K_n hub 的 PARI rank
docs/work-logs/073-dual-closure-sieve... 当前 unconditional 范围 max_hyp=2M
scripts/analyze_k2_closure_fiber.py      （本 wl 待实现）实验脚本
```

## 六、首轮实证（重大发现）

`scripts/analyze_k2_closure_fiber.py` 对 max_hyp = 50,000 的 k=2 safe-pass
multi-N pair 跑 PARI `ellrank` + `elladd` + `ellbil` + `ellheight`。

### 6.1 数据

第一轮 max_hyp = 50,000，148 个 k=2 pair（PARI effort=1）：

```
rank=2: 48 (32.4%) | rank=3: 71 (48.0%) | rank=4: 29 (19.6%)
rank<2: 0 | imprecise: 0
P_{N_1} + P_{N_2} non-torsion: 148/148
```

第二轮 max_hyp = 200,000，**495 个 k=2 safe-pass pair**（PARI effort=1）：

```
rank=0: 3 | rank=1: 1 | rank=2: 152 | rank=3: 236
rank=4: 95 | rank=5: 7 | rank=6: 1
rank<2: 4   imprecise: 4
P_{N_1} + P_{N_2} non-torsion: 495/495
```

**对 4 个 imprecise case 用 PARI effort=2 复跑**（项目 wl036 已知 effort=1
会 systematically 给虚假 lower=0）：

| (A, B) | N_1, N_2 | effort=1 | effort=2 | sha2_lower |
|---|---|---|---|---|
| (9971, 58905)    | 12540, 64428    | [0,2] | **[2,2]** | 2 |
| (18821, 180999)  | 49140, 272580   | [0,2] | **[2,2]** | 2 |
| (104039, 149625) | 129948, 7854600 | [1,3] | **[3,3]** | 2 |
| (55115, 161161)  | 282348, 400452  | [0,2] | **[2,2]** | 2 |

**全部 4 个 case 升级到 rank ≥ 2**，且都伴随 **sha2_lower = 2**（非平凡
2-Sha，对应 wl036 已观察的"少数 k=2 pair 携带非平凡 Sha[2]"模式）。

最终统计（effort 复跑后）：

```
样本数:    495 个 k=2 multi-N pair (max_hyp=200k, safe-pass)
rank=2:    156 (31.5%)
rank=3:    237 (47.9%)
rank=4:    95  (19.2%)
rank=5:    7   (1.4%)
rank=6:    1   (0.2%)
rank<2:    0   ← Conjecture A1 universal on 495/495
P_{N_1} + P_{N_2} non-torsion: 495/495
```

### 6.1.1 扩到 max_hyp = 500,000

```
样本数:    1093 个 k=2 multi-N pair, safe-pass, 27 秒
rank=2:    308 (28.2%)
rank=3:    537 (49.1%)
rank=4:    217 (19.9%)
rank=5:    28  (2.6%)
rank=6:    3   (0.3%)
rank<2:    0   ← Conjecture A1 universal on 1093/1093
imprecise (post-rerank=2): 0
P_{N_1} + P_{N_2} non-torsion: 1093/1093
```

### 6.1.2 扩到 max_hyp = 1,000,000

```
样本数:    1879 个 k=2 multi-N pair, safe-pass, 68 秒
rank=2:    544 (28.9%)
rank=3:    916 (48.7%)
rank=4:    360 (19.2%)
rank=5:    56  (3.0%)
rank=6:    3   (0.2%)
rank<2:    0   ← Conjecture A1 universal on 1879/1879
imprecise (post-rerank=2): 2  ((120185,608139) 与 (695709,894311)，rank=[2,4]；
                               lower=2 仍满足 A1)
P_{N_1} + P_{N_2} non-torsion: 1879/1879
```

**Conjecture A1 在 max_hyp ≤ 1,000,000 全部 k=2 safe-pass 样本 1879/1879
universal verified**。rank 分布稳定：~29% rank=2、~49% rank=3、~19% rank=4，
更高 rank 占 ~3%。

### 6.2 主要观察

1. **rank ≥ 2 在所有样本上 universal**: 累计 1879/1879 实测（max_hyp ≤ 1M
   全部 k=2 safe-pass pair），跨 max_hyp 50k / 200k / 500k / 1M 多档独立验证；
   PARI effort=1 + 自动 effort=2 rerank。**这是非常强的 unconditional 信号** ——
   暗示数论上有 `multi-N k=2 ⇒ rank(E_{A,B}) ≥ 2` 的定理。
2. **P_{N_1} + P_{N_2} 永远非 torsion**: 该和点必落在 E(Q) 的非平凡部分
   （free part），没有任何样本退化成 torsion。这跟 closure（如果发生）所
   要求的 N_1+N_2=S 直接相关：如果 closure ⟺ P_{N_1}+P_{N_2} 在某特定
   torsion coset，则反例必然落在我们样本之外的"奇点"上。
3. **height pairing 无明确符号 pattern**：positive 和 negative 各占 ~50%，
   绝对值 0~6 之间，比 h(P_1), h(P_2) (~5-18) 显著小。意味着 P_1, P_2
   在 Mordell-Weil lattice 里"接近正交"。

### 6.3 关键定理候选（待证）

```
Conjecture A1 (k=2 ⇒ rank ≥ 2):
   对任意 reduced coprime safe-pass (A, B),
   |concordant_N(A, B)| = 2  ⇒  rank(E_{A,B}) ≥ 2.
```

证明思路（草稿）：

```
N_1, N_2 ∈ concordant_N(A, B) 各对应 P_{N_1}, P_{N_2} ∈ E_{A,B}(Q).
Ono 1996 Prop 1: P_{N_1}, P_{N_2} ∈ 2 E(Q).
即 ∃ Q_{N_1}, Q_{N_2} ∈ E(Q) s.t. 2 Q_{N_i} = P_{N_i}.

Q_{N_1}, Q_{N_2} 在 E(Q)/(2 E(Q) + image E[2](Q)) 里的 F_2 image
   = 2-descent map δ(Q_{N_i}) ∈ (Q*/Q*²)²
   (Halbeisen-Hungerbühler 2024 / Peschmann 2-descent map)

如果证 δ(Q_{N_1}), δ(Q_{N_2}) 是 F_2-independent 且都 ≠ E[2](Q) image,
   ⇒ rank(E) ≥ 2.
```

关键 step 是证 δ(Q_{N_1}) ≠ δ(Q_{N_2})。这等价于 P_{N_1} ≠ P_{N_2} mod
2 E(Q) — 但二者都 ∈ 2 E(Q)，需要 mod 4 E(Q) 比较。**留待下一步实证**。

### 6.4 推论：closure 的几何障碍

如果 Conjecture A1 成立，则 multi-N pair k=2 时 E(Q) 至少 2 维 free。
closure 要求 N_1 + N_2 = S 是个 1 维 Diophantine 条件，把 2 维空间切成
1 维 fiber。**该 fiber 上没有 Q-rational point** 是要继续证的目标。

具体路线：

- 实验路线 a: 用 PARI 把每个 P_{N_i} 表为 `n_1 G_1 + n_2 G_2 + T`
  （Mordell-Weil decomposition），看 (n_1, n_2) 的 pattern 是否有限
- 实验路线 b: 算 `δ(Q_{N_1})`, `δ(Q_{N_2})` 在 (Q*/Q*²)² 上的 F_2 image
  （类比 wl048 k=4 F2-rank 实验）

## 七、文件

```
docs/work-logs/074-path-a-k2-closure-fiber-analysis.md  本文件
scripts/analyze_k2_closure_fiber.py                     PARI 实验脚本（含 auto-rerank）
results/k2_closure_fiber_first5.jsonl                   首批 5 样本
results/k2_closure_fiber_first50.jsonl                  24 样本 (max_hyp=10k)
results/k2_closure_fiber_max50k.jsonl                   148 样本 (max_hyp=50k)
results/k2_closure_fiber_max200k.jsonl                  495 样本 (max_hyp=200k, 9s)
results/k2_closure_fiber_max500k.jsonl                  1093 样本 (max_hyp=500k, 27s)
results/k2_closure_fiber_max1m.jsonl                    1879 样本 (max_hyp=1M, 68s)
```

复现命令：

```bash
uv run python scripts/analyze_k2_closure_fiber.py \
    --max-hyp 1000000 --limit 10000 \
    --jsonl-out results/k2_closure_fiber_max1m.jsonl
```

## 八、状态

- ✅ 数学 setup + identity I, II
- ✅ closure 翻译为 "∃ N_1, N_2 ∈ Sq(E) with N_1 + N_2 = S"
- ✅ Conjecture A1 提出
- ✅ **实证 rank ≥ 2 universal on 1879/1879 (max_hyp ≤ 1M, multi 档独立验证)**
- ✅ PARI effort=1 + auto rerank effort=2 工作流（68 秒跑完 1M）
- ⏳ 计算 F_2 image of Q_{N_i} 验证 Conjecture A1 mechanism
- ⏳ Conjecture A1 严格代数证明（Ono Prop 1 + 2-descent independence）
- ⏳ closure-on-rank-2-fiber 的 height-bound / Chabauty 处理
