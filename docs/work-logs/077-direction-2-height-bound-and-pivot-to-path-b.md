# wl077 — 方向 2 height-bound 失败 + 转向路径 B（uniform mod p²）

承接 wl076（A1 mechanism + 1879/1879 实证）。本 wl 评估 wl075 §六的方向 2
（closure-fiber Chabauty）的可行性，发现 height-bound 直接路径不通，并据此
**重新选定阶段 3 攻击点为路径 B**（uniform mod p² obstruction theorem）。

## 一、方向 2 的最初设想：height-bound

### 1.1 思路

A1 给 rank(E_{A,B}) ≥ 2。closure 假设 N_1 + N_2 = S = A + B：

```
max(N_1, N_2) ≤ S
⟹ X(P_{N_i}) = N_i² ≤ S²
⟹ ĥ(P_{N_i}) ≈ (1/2) log H(N_i²) = log N_i ≤ log S
```

更宽松：`ĥ(P_{N_i}) ≤ 2 log S + O(1)`（含 local height correction）。

如果实证：**对所有 k=2 multi-N pair，min(ĥ(P_{N_1}), ĥ(P_{N_2})) > 2 log(A+B)**，
那 closure 假设直接矛盾。

### 1.2 实证脚本与结果

`scripts/analyze_k2_height_bound.py`，读 wl074 的 `k2_closure_fiber_max1m.jsonl`：

```
margin := min(ĥ(P_{N_1}), ĥ(P_{N_2})) − 2 log(A + B)

实测 1879 个 k=2 pair:
  margin > 0:  0
  margin ≤ 0:  1879  (100%)

margin 分布: min=-20.09  q1=-12.02  median=-10.32  q3=-8.49  max=-0.93
```

**全部 violated**！HB 直接 fail。

### 1.3 为什么 fail

实测 multi-N pair 的 N 远**大于** S = A+B（wl066 数据：99% Δ < 0，即
N_1 + N_2 > S）。这意味着**实测 P_{N_i} 的 ĥ 比 closure 要求的 ĥ 大得多**，
但 HB 要求"实测 ĥ > 上界"，不是"实测 ĥ < 下界"。两者不矛盾。

具体：
- 实测 (A, B, N_1, N_2) 是 already-existing multi-N pair, N_1 + N_2 ≠ S
- closure 假设的反例 (A, B, N_1', N_2') 必须 N_1' + N_2' = S, 故 N_i' ≤ S
- 但 |concordant_N(A, B)| = 2 (k=2 假设), 所以 {N_1', N_2'} = {N_1, N_2}
- 而 N_1 + N_2 ≠ S 实测，所以 closure 假设 immediately false

⟹ 对 **k=2 case，closure check 是直接 boolean equality 检查**：N_1 + N_2 = S?
这就是 wl073 dual closure sieve 已经做的事。**没必要 Chabauty / height-bound**。

### 1.4 结论：方向 2 不是阶段 3 的最佳攻击点

对 k=2，closure 是 boolean property，对每个 (A, B) **直接检查**即可。
我们已经做了：max_hyp ≤ 2M 0 命中（wl073）。

要 unconditional：需要证"对所有可能的 (A, B)（包括 max_hyp > 2M 的），
N_1 + N_2 = A + B 永远不成立"。这是个 **uniformity 问题**，方向 2
的 Chabauty 工具栈不直接适用。

## 二、转向路径 B：uniform mod p² obstruction

### 2.1 路径 B 重述（来自 wl075）

> **猜测 B**：∃ 有限模数集 M_0（不依赖 A, B），使对任何 reduced coprime
> safe-pass multi-N pair 必有 M ∈ M_0 让对偶筛 chain_closure_mod_sieve 杀掉。

wl073 已实证：max_hyp ≤ 2M 上 14 个 prime² (M ≤ 53²) 完全够杀。

### 2.2 路径 B 的优势

- **覆盖面**: 100%（所有 k，不只 k=2）
- **工具栈**: 纯模算术，不需要 Magma/Sage
- **实证证据**: wl073 max_hyp ≤ 2M unconditional 全杀
- **证明 framework**: 把 chain_closure_mod_sieve 的 `T(A, B, M) ∩ ((A+B) − T)`
  写成 (A mod M, B mod M) 的 mod p² invariant，证某个 M 总能 kill

### 2.3 严格证明结构（待做）

```
Step 1: 对每个 prime p 和 M = p², 列举:
  - (A mod M, B mod M) ∈ (Z/MZ)² 通过 safe sieve 的所有 residue classes
    （A 奇, B 奇, A+B ≡ 0 mod 4 mod M）
  - 对每个 class, 计算 T(A, B, M) ∩ ((A+B) − T)：是否空？

Step 2: 对每个 M_i = p_i², 记录"非空 survivors" 的 (A, B) mod M_i classes.

Step 3: 取 M_0 = {M_1, ..., M_k} (e.g., k=14, primes 3..53), 检查:
  对所有"safe-passing"  (A, B) 的 mod prod M_i 类, 是否每个类都被
  至少一个 M_i kill?
  即 ∩_{i=1}^k (M_i 的 survivor class) = ∅?

Step 4: 如果 Step 3 yes ⟹ Conjecture B 严格证成立 (with M_0).
  如果 Step 3 no ⟹ 找出 universal survivor class, 它给出 closure
  反例的"必要 mod 形式", 进一步 attack 那个 finite set.
```

每个 Step 都是 **finite computation** in (Z/MZ)²，可枚举、可验证。

### 2.4 计算量估计

- 单个 M = p²: |(Z/MZ)²| = p⁴。对 p=3, M=9, p⁴=81. 对 p=53, M=2809,
  p⁴ ≈ 8 × 10⁶。可枚举。
- 多个 M_i 联合: |product M_i|² ≈ (53²·47²·...·3²)² ≈ 大但可分块计算
  via CRT (Chinese Remainder Theorem)
- 每个 (A mod M, B mod M, N_1 mod M, N_2 mod M) check 是 O(1)
- 总：对 14 个 prime² 全枚举 ≈ 10⁷-10⁸ 操作，单机几分钟可完成

## 三、实施路径

### 3.1 阶段 3a · 实证 + theorem candidate

1. 写 `scripts/uniform_mod_p2_audit.py`：对每对 (M_i, M_j) 枚举所有 safe-pass
   (A mod, B mod, N_1 mod, N_2 mod) 4-tuples 满足 chain closure conditions,
   按 (A mod, B mod) 分组，记录 surviving (N_1, N_2) mod 类
2. 跑 M = {9, 25, 49, ..., 2809} 全部 14 个，看是否对每个 (A mod, B mod)
   class 总有某 M_i 让 surviving (N_1, N_2) 为空
3. 如果是，这是 Conjecture B 严格证 (with finite M_0)

### 3.2 阶段 3b · 形式化为 paper

- 把 enumeration result 写成 LaTeX statement
- 整合 wl073 + wl076 + 本 wl 成 paper sketch:
  - main theorem: max_hyp 任意, 0 Harborth 反例
  - 工具: A1 (k=2 ⇒ rank≥2) + uniform mod p² obstruction (路径 B)

### 3.3 阶段 3c · 推到所有 k（不只 k=2）

A1 只覆盖 k=2 (99% pair)。剩 1% 是 k≥3。对 k≥3，相同 mod p² obstruction
应该 work（k 越高，concordant N 越多，但 closure 要求只 2 个 N 之和等于 S，
仍 boolean check）。直接套路径 B 即可。

## 四、文件 / 引用

```
docs/work-logs/074-path-a-k2-closure-fiber-analysis.md     PARI ĥ data
docs/work-logs/075-theory-direction-survey-and-path-a-pickup.md  路径 B 提出
docs/work-logs/076-conjecture-a1-proof-sketch.md           A1 mechanism
docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md  dual sieve 实证
scripts/analyze_k2_height_bound.py                         本 wl: HB 实证 (fail)
scripts/uniform_mod_p2_audit.py                            (待实现) 路径 B 实证
```

## 五、状态

- ✅ 方向 2 height-bound 实证 (1879/1879 fail，路径不通)
- ✅ 重新评估：阶段 3 从方向 2 (Chabauty) 转向路径 B (uniform mod p²)
- ⏳ 阶段 3a：写 `uniform_mod_p2_audit.py` 枚举 (A mod, B mod) class survivors
- ⏳ 阶段 3b：把 enumeration → theorem
- ⏳ 阶段 3c：推到 k≥3
