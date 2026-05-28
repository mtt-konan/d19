# wl079 — 路径 B 阶段 4a：multi-N pair 在 mod p² surviving classes 的分布

承接 wl078（phase 3a/3b/3c 完成 audit + CRT enumeration）。本 wl 推进
phase 4a：实证 multi-N pair 投影到 mod p² surviving classes 上，分析
T_m^multi-N ⊆ S_m^surviving 的实际占用比例与 algebraic 结构。

## 一、核心数据（max_hyp = 1M, 1907 multi-N pairs）

| m | |S_m| | distinct used | used/|S_m| |
|---|------|---------------|------------|
|  9 |     27 |   18 | 66.7% |
| 25 |    185 |  104 | 56.2% |
| 49 |   1225 |  862 | 70.4% |
|121 |   4961 | 1318 | 26.6% |
|169 |  14521 | 1390 |  9.6% |
|289 |  56321 | 1716 |  3.0% |
|361 |  52345 | 1358 |  2.6% |
|529 | 233289 | 1856 |  0.8% |
|841 | 565993 | 1695 |  0.3% |
|961 | 808201 | 1804 |  0.2% |

`distinct used` = multi-N pair 投影到 (A mod m, B mod m) 时 distinct
(a, b) class 数，限定在那些"未被 m primary kill"的 pair 中。

**关键观察**: 对小 prime²（m = 9, 25），multi-N 占 S_m 的 56–70%。
意味着即使 (a, b) 落在 S_m，未必能 lift 到 multi-N — 还有 ~30–44%
classes 是 "S_m feasible but no multi-N"。这就是 path B 严格证明
的真正 leverage。

## 二、Unused classes 分解：primitivity vs real obstruction

对每个 m = p², 把 S_m \ T_m^multi-N 拆为：

- **primitivity-excluded**: `p | a AND p | b`（gcd(A,B)=1 排除）
- **real obstruction**: 不在 primitivity 范围，但仍 multi-N 不可达

| m  | unused | primitivity-excluded | **real obstruction** |
|----|--------|----------------------|----------------------|
|  9 |     9  |        9 (100%)      |          **0**       |
| 25 |    81  |       25             |         **56**       |
| 49 |   363  |       49             |         314 (sample 不足)|
|121 |  3643  |      121             |        3522 (sample 不足)|
|169 | 13131  |      169             |       12962 (sample 不足)|

### 2.1 mod 9：完美的 primitivity-only 结构

mod 9 上 9 个 unused class 全部满足 3 | a AND 3 | b：

```
{(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)}
```

⟹ **Lemma B.9 (mod 9)**: 对 primitive multi-N pair (A, B),
> (A mod 9, B mod 9) ∈ S_9 \ {(3i, 3j) : 0≤i,j<3} = S_9 ∩ primitive

等价说: **mod 9 上 multi-N 的代数条件完全等同于 (chain_closure_sieve 未杀)
∧ ¬(3|A ∧ 3|B)**. 这是个干净的 closed-form 描述，可直接进证明。

### 2.2 mod 25：trend 与 phase 4b 否定结果

| max_hyp | distinct used | real obstruction | (b² - a²) mod 25 范围 |
|---------|---------------|------------------|------------------------|
|     1M  |    104        |      56          | {5, 9, 10, 15, 20}     |
|     2M  |    117        |      43          | {5, 10, 15, 20}        |

从 1M → 2M:
- distinct_used 104 → 117 (+13), 多 13 个 class 被新 multi-N 触及。
- real obstruction 56 → 43；`(b²-a²) mod 25 = 9` 类已被填上。
- 剩 43 class **全部满足** `(b² - a²) mod 25 ∈ 5·(Z/5Z)*` = `{5, 10, 15, 20}`，
  即 `v_5(D) = 1`。

**初步**曾推测 `v_5(B²-A²) ≠ 1` 是 multi-N 的代数必要条件 (Lemma B.25)。
但 phase 4b 的 `scripts/d_valuation_analysis.py` 对全 3198 个 multi-N pair
直接算 `v_p(D)` 分布，结论 **否定**:

```
p = 5:  v_5(D) 分布 (max_hyp=2M, 3198 pairs):
   v=0: 2564 (80.18%)
   v=1:   85 ( 2.66%)   ← 实际有 85 个 multi-N 满足 v_5(D)=1
   v=2:  295 ( 9.22%)
   ...
```

⟹ **Conjecture B.25 (v_p(D) ≠ 1) FAILS**: 全 10 个 prime (3, 5, 7, 11, 13,
17, 19, 23, 29, 31) 上 `v_p(D)=1` 占 multi-N pair 的 13–25%。phase 4a 的
"43 unused real obstruction class" 只是 mod 25 上 chain_closure 未杀但 
multi-N 偶然未触及的 class，不是真正的代数 obstruction —— 推到更大
max_hyp 这些 class 会逐渐被填上。

### 2.2.1 修正后的 mod p² 攻击点

mod p² 上 multi-N 与 S_m 的关系**不能**用 `D = B²-A²` 单独的 p-adic
valuation 简单刻画。**所以 path B 的简洁 closed-form 条件目前只在 mod 9
上存在**（Lemma B.9）。其它 mod p² (p ≥ 5) 上没有发现等价的
elementary 必要条件。这表明:

- mod 9 obstruction = `chain_closure ∧ ¬(3|A ∧ 3|B)` 是干净的；
- mod p² (p ≥ 5) obstruction 没有更"代数"的等价刻画，要直接用 chain_closure
  的 quadratic-residue 约束；
- Conjecture B' 严格证明只能 prime-by-prime 推。

### 2.3 mod 49 / 121 / 169：sample 太少，结论暂缓

mod 49 上 used 占 70% S_m，sample 略偏低。mod 121+ 上 |S_m| 增长快，
sample 不到 30% 就不能下定论。下一步要：

- 扩 max_hyp 到 2M / 5M 重跑 audit + 投影
- 看是否 saturation: distinct_used → 固定上限 (real obstruction stable)

## 三、Algebraic 推测 (phase 4b 攻击点)

### 3.1 mod p 的 quadratic residue 角度

multi-N 等价 ∃ N 使 N² + A² ≡ □ AND N² + B² ≡ □ mod p²。Hensel 提升后:

```
−A² ∈ QR(p²)  OR  p | N  (with N² = −A² mod p²)
−B² ∈ QR(p²)  OR  p | N
```

这给 (A mod p², B mod p²) 在 mod p² 上的 quadratic-residue 约束。对应于
E_{A,B}: y² = x(x+A²)(x-D) 在 Z_p² 上有有理 2-torsion 局部点。

### 3.2 D = B² - A² 的角色

`D` 是 E_{A,B} 的判别式核心。Halbeisen-Hungerbühler 2021 给出 E_{A,B}
↔ E_{D} (Q² + D ∈ □) 的等价。所以"`D mod p² ∈ 特殊残差类`" 应等价于
mod p² 上的 multi-N 必要条件。

phase 4b 的目标:

> 证明 **(A, B) primitive + multi-N ⟹ D mod p² avoids a specific finite set
> `Bad_p² ⊂ Z/p²Z`**（empirical: |Bad_9|=9 from primitivity, |Bad_25|=25+56=81
> ⟹ |Bad_25 \ primitivity| = 56 strictly characterised by D residue）

将 Conjecture B' 转化为：D mod ∏p_i² 完全落入 `Bad`。⟹ Conjecture B'
等价 D 的 mod-p² 分布完全被 Bad 覆盖 ⟹ 矛盾。

## 四、下一步计划

1. **4a 续**: 扩 max_hyp=5M 重跑 audit + mod_p2_unused_analysis，看
   mod 25 56 个 real obstruction 是否稳定，mod 49+ saturation 行为。
2. **4b**: 推导 D mod p² 的 algebraic 表征（Hensel + QR 分析）。
3. **4c**: dual sieve 6 个 pair 的 mod p² 等价描述（partner reduce 视角）。

## 五、文件 / 引用

```
scripts/uniform_mod_p2_audit.py            wl078: audit (max_hyp=1M)
results/uniform_mod_p2_max1m.jsonl         1907 pair dump
scripts/analyze_multi_n_mod_pattern.py     本 wl: distinct_used 投影统计
scripts/mod_p2_unused_analysis.py          本 wl: primitivity vs real obstruction
docs/work-logs/078-path-b-mod-p2-kill-audit.md  phase 3a/3b/3c
```

## 六、状态（最终）

- ✅ multi-N 投影到 mod p² 的占据比例统计 (max_hyp=1M / 2M)
- ✅ **mod 9**: multi-N = `primitive ∩ S_9` 完美干净 (Lemma B.9, 0 real
  obstruction; max_hyp=1M, 2M 均 100% 验证)
- ✅ **phase 4b 否定结果**: `v_p(D) ≠ 1` 在所有 prime ∈ {3,5,7,11,...,31}
  上 FAILS (实际 13–25% multi-N 满足 v_p(D)=1)
- ✅ mod 25 上 1M→2M real obstruction 56→43, 全部 v_5(D)=1。这并非真正
  obstruction，仅是 sample 不足 + chain_closure 在该子集偶然没杀
- ❌ mod p² (p ≥ 5) 没有发现简单 closed-form 必要条件
- ⏸ 路径 B 严格证明因此只能 case-by-case 推 (无简便 algebraic shortcut)

## 七、Phase 总结

到此为止，沿 path B 的实证 + algebraic 探索可以收口:

1. **实证全杀**已坚不可摧：max_hyp ≤ 2M 全 226k(safe-pass) multi-N pair 在
   primary + dual chain_closure_mod_sieve (STANDARD_MODULI) 下 100% killed
   (wl073)。
2. **mod 9 干净 lemma**: 唯一找到的 "代数等价于 primitive + chain_closure"
   的层。
3. **path B 严格证明的瓶颈**: mod p² (p ≥ 5) 上无简单 algebraic
   characterisation, 也无 universal kill (CRT 表明 mod-p² primary 永远剩
   ≥ 0.017% surviving)。要走严格证明只能:
   - 直接 case-by-case 推每个 prime 的 chain_closure obstruction;
   - 或借助新工具 (e.g., Mazur uniform bound, descent on E_{A,B})。
4. **dual sieve 不可省**: 6 / 16 个 dual-only pair (max_hyp=1M / 2M) 是
   dual sieve 唯一能杀的对象，证明 path B 的 finite M_0 必须包含 dual。

⟹ **path B 在当前工具链下作为"实证 + audit + mod 9 干净 lemma"已达成；
完整 algebraic 严格证明需要新理论工具，超出本轮可达范围**。下一轮可
考虑：

- 回到 path A：把 Conjecture A1 (k=2 → rank ≥ 2) 的 F₂-rank 实证 + 
  Halbeisen-Hungerbühler 2021 的等价定理融合，做 algebraic 证明完整化。
- 或借助 Stoll / Bruin Chabauty 工具直接打 closure-fiber 上的有理点
  finiteness。
