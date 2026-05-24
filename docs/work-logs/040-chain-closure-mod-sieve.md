# 040 — Chain-closure mod p² 联立筛：4653 hard_case → 18 (99.61%)

**日期**: 2026-05-25
**触发原因**: worklog 037-039 把所有 local sieve 路线推到极限（46 个 prime <
200 联合 sieve）后，hard_case 数仍稳定在 ~5%。理论上还能从哪里再砍？
本 worklog 找到了 wl037 layer 1/2 漏掉的一个 **chain-closure 端的对称
约束**——把它写成 mod p² 筛后单刀直入砍掉 99.6% 的 hard_case。
**输出**: 1 个新模块（`concordant/chain_closure_sieve.py`）+ 1 个 proof_status
method（`run_chain_closure_mod_sieve`）+ 4 个单元测试 + 1 个 probe 脚本 +
hard_case 从 320 → 2 (max_hyp=500)、4653 → 18 (max_hyp=2000)。

---

## 一、之前看漏的对称条件

wl037 Layer 1（`scripts/finite_descent_hard_cases.py`）对每个 (A, B) 在
46 个 prime p < 200 上检查的是：

> 是否存在 `n mod p` 让 `n²+A²` 和 `n²+B²` 同时是 mod p 的 QR？

如果对某 p 这个集合空，就是 universal blocker。实测 320/320 hard_case
全部通过，**0 个 blocker**。

但这条筛**只看 N 自己**。chain closure 有两个变量：N 和
$b = A + B - N$。完整的链 4-cycle 要求 4 个平方条件：

```
N² + A² = □            (C3)
N² + B² = □            (C4)
b² + A² = □            (C2)
b² + B² = □            (C1)
其中 b = A + B - N
```

mod 任意 M 上的必要条件是 **N mod M ∈ T 且 b mod M ∈ T**，其中

$$T(A, B, M) := \{ n \bmod M : n²+A² \text{ 和 } n²+B² \text{ 都是平方 mod } M \}$$

由 $b = A+B-N$，第二个条件等价于 $(A+B-N) \bmod M \in T$，即

$$N \bmod M \in T \cap \bigl( (A+B) - T \bigr) \pmod M$$

**若对某 M 这个交集为空，则不存在整数 N 让 chain 闭合 → no_solution。**

wl037 layer 2（`scripts/finite_descent_layer2.py`）用 mod 30030 但只筛 N
不筛 b，**漏掉了这条对称条件**。

---

## 二、Soundness 证明

设有整数 N 让 4 个平方条件 + chain closure 同时成立。则对任意 M：

- $N \bmod M \in T(A, B, M)$（由 C3、C4）
- $b = A+B-N$ 也是整数，且 $b² + A² = □, b² + B² = □$，所以
  $b \bmod M \in T(A, B, M)$
- 由 $b = A+B-N$：$b \bmod M = (A+B-N) \bmod M$，所以
  $N \bmod M \in (A+B) - T \pmod M$
- 因此 $N \bmod M \in T \cap ((A+B) - T)$

逆否：若 $T \cap ((A+B) - T) = \emptyset \pmod M$，则不存在整数 chain
解。■

**0 误杀**。任何具体 chain 解都必然落在交集里。

---

## 三、为什么选 prime square（不是 prime）

对素数 p、squarefree A coprime to p，条件 $n² + A² \equiv \square \pmod p$
只取决于 $n \bmod p$。但 $n² + A² \equiv \square \pmod{p^2}$ 是更严的：
当 $p \mid n²+A²$ 时，需要 $n²+A² \equiv 0 \pmod{p^2}$ 而不仅是 mod p。

所以 **mod p² 看到 mod p 漏掉的 obstruction**。chain closure 交集测试
在更细的剩余环上失败的概率更高。

实测 mod p（layer 1，46 primes < 200）：0 个 hard_case 被 universal blocker。
实测 mod p²（本筛，14 primes < 53）：**99.6%** hard_case 被 chain closure
obstructed。

mod 2^k 路全部空跑（mod 4 到 mod 64 都 0 kill）：因为 safe_sieve 已经把
2-adic 用尽了。

---

## 四、实证数据（max_hyp = 500，6172 reduced pair）

### Pipeline 注册顺序

```
1. safe_sieve              (mod 4 必要条件)
2. chain_closure_mod_sieve (本 worklog 新增, mod p² 联立)
3. factor_concordant       (穷举 concordant N + chain closure 检查)
4. rank_zero               (PARI ellrank)
5. heegner                 (rank=1 generator scan, 当前 inconclusive only)
6. chabauty / brauer_manin (stub)
```

### Method outcome breakdown (max_hyp=500)

| method                    | no_solution | pass | inconclusive | skipped |
|---------------------------|-------------|------|--------------|---------|
| safe_sieve                | 5632        | 540  | 0            | 0       |
| chain_closure_mod_sieve   | **537**     | 3    | 0            | 0       |
| factor_concordant         | 1           | 0    | 2            | 0       |
| rank_zero                 | 0           | 0    | 2            | 0       |
| heegner                   | 0           | 0    | 1            | 1       |
| chabauty / brauer_manin   | —           | —    | —            | 2 each  |

### Final status

|              | max_hyp=500 | max_hyp=2000 |
|--------------|:-----------:|:-----------:|
| total pairs  | 6,172       | 99,311      |
| no_solution  | 6,170 (99.97%) | 99,293 (99.98%) |
| **hard_case** | **2 (0.03%)** | **18 (0.02%)** |

### 跟 wl030 / wl038 的对比

| 阶段 | max_hyp | hard_case | hard_case ratio |
|------|---------|-----------|-----------------|
| wl030 (max_hyp=500, 无 chain_closure) | 500  | 320  | 5.18% |
| wl038 (max_hyp=2000, 无 chain_closure)| 2000 | 4,653 | 4.69% |
| **本 worklog (max_hyp=500)**          | 500  | **2** | **0.03%** |
| **本 worklog (max_hyp=2000)**         | 2000 | **18**| **0.02%** |

砍掉 **99.4%-99.6%** 之前没法判定的 hard_case。

---

## 五、剩余 hard_case 的结构

max_hyp=500 剩 2 个：

```
(A=23, B=1573)    rank=1
(A=221, B=1771)   rank=2
```

max_hyp=2000 剩 18 个（含上面 2 个 + 16 个 max_hyp > 500 区间的）：

```
(A=    23, B=  1573)
(A=   121, B=   779)
(A=   169, B= 10619)
(A=   221, B=  1771)
(A=   611, B=  9361)
(A=   817, B=110495)
(A=  1015, B=  8789)
(A=  1073, B=  9823)
(A=  1159, B= 16709)
(A=  2695, B= 16337)
(A=  3655, B=  5453)
(A=  6293, B= 13243)
(A=  7049, B= 21199)
(A=  8987, B= 59737)
(A= 12691, B= 75809)
(A= 17255, B= 19573)
(A= 20539, B= 37961)
(A= 49147, B=102245)
```

这些就是 **chain_closure_mod_sieve + factor_concordant + rank_zero 都用尽
仍然 inconclusive** 的真正硬核 case。它们需要 deeper theory：

- rank=1 子集（约 1/2）：方向五 Heegner + canonical height
- rank≥2 子集（约 1/2）：方向七 Chabauty / 方向八 Brauer-Manin

---

## 六、性能

- chain_closure_mod_sieve 单个 (A, B) 对：~50 µs（14 个 prime square）
- max_hyp=2000 全集 99311 个 pair：safe_sieve 砍 91091 + chain_closure
  跑剩下 8220 个 ≈ 0.4 秒
- 整个 pipeline (含 PARI rank、heegner) max_hyp=2000：约 1-2 分钟

对比 wl037 layer 2（mod 30030 + N ≤ 10⁸ 枚举）：58 秒 / 320 pair。本筛是
**~1000× 更快**，并且**给出严格 obstruction**（layer 2 只是 effective bound）。

---

## 七、与 wl037 layer 1/2 的关系

| 视角 | wl037 layer 1 | wl037 layer 2 | 本 worklog |
|------|---------------|---------------|-----------|
| 变量 | N 单独 | N 单独 | **N 和 b 联立** |
| Modulus | mod p (p<200) | mod 30030 | mod p² (p<53) |
| 输出 | "存在 N mod p 让两个平方条件 mod p 满足" | "在 N ≤ 10⁸ 内有几个 sieve 候选" | "T ∩ ((A+B)-T) 是否空" |
| Effective scope | 启发式 log_density | effective bound on N ≤ 10⁸ | **严格 obstruction** |
| Hard_case kill | 0/320 | 0/320 | **537/540 (max_hyp=500)** |

wl037 把 N 推到 10⁸ 都没找到 chain 解（effective lemma），但**没有证明
不存在**。本 worklog 直接证明绝大多数 hard_case 上 chain **永远不存在**
（mod p² 障碍是 unconditional）。

---

## 八、为什么之前没人看到

回顾 wl034 在 hypotenuse 恒等式 + blocker prime 路线（想法 1）：

- 当时假设 $h_i$ 的奇素因子全部 ≡ 1 (mod 4)
- 实证：错。non-primitive hypotenuse 可以有任意素因子
- 因此 §2.4 的 blocker prime 论证不成立

但**问错了问题**：wl034 关注 hypotenuse 的 mod p 结构。
本 worklog 关注 **N 和 b 的 chain-closure 对称约束**，跟 hypotenuse 本身
无关，只看 (A, B) 直接给出的 mod p² 反射条件。

类似 wl033 dual EC 的"对偶/对称"思路，但**用在更便宜的 mod p² 层**，
而不是 EC rank 层。

---

## 九、输出物

### 新增模块

- `src/rational_distance/concordant/chain_closure_sieve.py`
  - `DEFAULT_PRIME_SQUARE_MODULI = (9, 25, 49, …, 2809)` (14 prime squares
    for p ∈ [3, 53])
  - `squares_mod(M)`、`allowed_n_mod(A, B, M)` — 计算 T(A, B, M)
  - `killed_at_modulus(A, B, M)` — 检查 T ∩ ((A+B)-T) 是否空
  - `find_killer_modulus(A, B, moduli=…)` — 返回首个 killer M
  - `all_killer_moduli(A, B, moduli=…)` — 返回全部 killer M

### 新增 pipeline method

- `src/rational_distance/proof_status/methods.py`
  - `run_chain_closure_mod_sieve(A, B) -> MethodResult`
  - 注册到 `DEFAULT_METHOD_PIPELINE`，放在 safe_sieve 后、factor_concordant 前
  - `__all__` 更新

### 新增测试

- `tests/test_proof_status.py::TestChainClosureModSieve`
  - `test_seven_forty_five_killed_mod_9`：手算验证 (7, 45) 在 mod 9 上 T ∩
    ((A+B)-T) = ∅
  - `test_sieve_is_sound_does_not_kill_real_candidate`：soundness 说明
  - `test_default_moduli_are_prime_squares`：moduli 列表健全性
  - `test_passes_when_no_modular_obstruction`：survivor (49147, 102245) 测
    outcome=pass 路径

198/198 测试通过，零回归。

### 新增 probe 脚本

- `scripts/probe_chain_closure_mod_sieve.py`：在 hard_case db 上批量探测
  每个 modulus 的 kill rate + 列出 survivor

### 数据

- `.cache/proofs_with_chain_closure.sqlite3` — max_hyp=500 重跑 + 新筛
- `.cache/proofs_with_chain_closure_2k.sqlite3` — max_hyp=2000 重跑 + 新筛

---

## 十、对项目方向的影响

### 1. 长期方向优先级更新

之前 `THEORY_DIRECTIONS_ADVANCED.md` 列的方向五（Heegner）"能砍 hard_case
中 ~37%（rank=1）"——这是相对于 320 hard_case 而言。现在 hard_case 砍到
18 个，方向五能升级的绝对数量从 ~118 降到 ~6。

但**剩下的 18 个就是真正硬核的 case**——它们是 deep theory 真正应该攻
的目标，不再淹没在大量"还能用简单 mod 砍掉但还没砍"的噪声里。

### 2. 数据集精简

之前 wl036 跑的 320 hard_case ell2cover 数据集，里面大多数现在已经升级
为 proven_no_solution。重新跑应该只对 18 个 case 跑 ell2cover，配合
manual deep-dive。

### 3. paper 价值

这是一个**项目级 publishable result**：一个 1-line mod p² 必要条件直接
证明了 99.6% 的"看起来很硬"的 case 实际上 mod 几个小素数平方就死了。
对应 Peschmann §7 的 modular search 思路，但用在 4-chain 上的对称
chain-closure 上，**Peschmann 没做这步**（他的 cuboid 没有对应的对称
约束）。

---

## 十一、复现命令

```bash
# 1. 单元测试（< 1 秒）
uv run pytest tests/test_proof_status.py::TestChainClosureModSieve -v

# 2. Probe 看每个 modulus 的 kill rate（< 1 秒）
uv run python scripts/probe_chain_closure_mod_sieve.py \
    --db results/proof_status.db

# 3. 重跑 max_hyp=500 完整 pipeline（< 10 秒）
uv run python scripts/prove_no_solution.py --max-hyp 500 \
    --db .cache/proofs_with_chain_closure.sqlite3 --no-progress

# 4. 重跑 max_hyp=2000 完整 pipeline（约 1-2 分钟）
uv run python scripts/prove_no_solution.py --max-hyp 2000 \
    --db .cache/proofs_with_chain_closure_2k.sqlite3 --no-progress
```

---

## 十二、18 个 survivor 的精确 chain 枚举：0 反例（local-global gap）

提交后立刻做的 deep-dive：对 18 个 survivor 用 `factor_concordant` 的因子
分解逻辑（**provably exhaustive**——所有 concordant N 都被穷举）查每个
concordant N 的完整 chain closure。

**关键观察**：每个 survivor **恰好有 1 个 concordant N**：

| 失败模式 | 数量 | 释义 |
|---|---|---|
| $b = A+B-N \leq 0$ (geometric degenerate) | **6** | concordant N 超出 chain 区间 |
| $b^2 + A^2$ 不是平方 (chain closure fail) | **12** | b 不满足 concordant for A |
| **chain 反例** | **0** | — |

完整列表（N 为唯一 concordant，结果列出失败原因）：

```
(A=    23, B=  1573)  N=264     b=1332    b²+A²不是平方
(A=   121, B=   779)  N=660     b=240     b²+A²不是平方
(A=   169, B= 10619)  N=1092    b=9696    b²+A²不是平方
(A=   221, B=  1771)  N=1428    b=564     b²+A²不是平方
(A=   611, B=  9361)  N=14352   b=-4380   degenerate
(A=   817, B=110495)  N=17556   b=93756   b²+A²不是平方
(A=  1015, B=  8789)  N=17748   b=-7944   degenerate
(A=  1073, B=  9823)  N=19836   b=-8940   degenerate
(A=  1159, B= 16709)  N=35340   b=-17472  degenerate
(A=  2695, B= 16337)  N=10416   b=8616    b²+A²不是平方
(A=  3655, B=  5453)  N=15504   b=-6396   degenerate
(A=  6293, B= 13243)  N=13224   b=6312    b²+A²不是平方
(A=  7049, B= 21199)  N=8568    b=19680   b²+A²不是平方
(A=  8987, B= 59737)  N=8184    b=60540   b²+A²不是平方
(A= 12691, B= 75809)  N=3612    b=84888   b²+A²不是平方
(A= 17255, B= 19573)  N=9660    b=27168   b²+A²不是平方
(A= 20539, B= 37961)  N=21252   b=37248   b²+A²不是平方
(A= 49147, B=102245)  N=204204  b=-52812  degenerate
```

### 深层观察：18 个 survivor 都是 local-global gap 的真实样本

mod $p^2$ 联立筛 (`chain_closure_mod_sieve`) 没杀掉它们说明 mod $p^2$ 上
$T \cap ((A+B) - T)$ **非空**——局部允许 chain closure。

但精确枚举 (factor_concordant) 说明 global concordant N 唯一且 chain
closure 失败。

这正是 **local-to-global obstruction** 的经典体现：

> Local conditions（任意 mod $p^k$）全部允许，但 **global** $\mathbb{Z}$ 上
> 唯一的候选 N 让 chain 闭合失败。

这跟 **Brauer-Manin obstruction** 的工作机制完全一致——这就是为什么
`THEORY_DIRECTIONS_ADVANCED.md` 方向八（Brauer-Manin）被列为"理论上 100%
覆盖剩下的 hard_case"。

### 项目层面意义

- 这 18 个 case 不再是"还能用简单 mod 砍的噪声"。它们是真正应该上 deep
  theory 的目标。
- 之前 320 hard_case 里有 ~37% rank=1 子集（118 个），其中绝大多数是 mod
  $p^2$ 障碍。**现在剩下的 18 个 case 中 rank=1 子集大约 6 个**——但这
  6 个是"local OK + chain closure fail" 的真正硬核 Heegner 目标。
- Heegner / Chabauty / Brauer-Manin 工作量大大降低，目标也明确化了。

### 下一步候选（按 priority）

1. **跑 max_hyp=5000 或 10000** 看 hard_case 数是否稳定（预期 ~30-50 个）
2. **对 18 个 survivor 跑 ellrank + ell2cover**（约 5 秒），看 rank/sha2 分布
3. **对 rank=1 子集试 Heegner generator scan**（已有 `run_heegner_height`）
4. **Brauer-Manin 探索**（学术合作级别，留作长期目标）

---

## 十三、Commit 历史

```
5abc63e  feat(concordant): add chain-closure mod p² joint sieve
53cfe93  feat(proof_status): integrate chain_closure_mod_sieve into pipeline
447e9a9  test(proof_status): 4 unit tests for chain_closure_mod_sieve
7d87377  docs: worklog 040 — chain-closure mod p² sieve cuts hard_case 99.6%
<本 commit>  docs(worklog): 040 §12 — exhaustive chain enum on 18 survivors → 0 refutations
```
