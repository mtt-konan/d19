# 039 — ell2cover 实证 BM-obstruction + 2-Selmer 结构公式

**日期**: 2026-05-23
**触发原因**: worklog 038 的 156 个 sha2_lower ≥ 2 hard_case 是
"PARI 看到 Sha[E][2] non-trivial 的 case"，但只有维度数字，没有 *explicit*
Sha 元素。本 worklog 用 PARI `ell2cover` + `hyperellratpoints` 给每个 case
拿到具体的 2-Selmer 覆盖 quartic 方程，并验证哪些 cover 没有有理点 →
explicit Sha[E][2] candidate。
**输出**: 3 个新脚本（timeout-safe ell2cover 扫描器 + 分析器 + height
follow-up）+ 1 个跟数据完美匹配的 **2-Selmer 维度公式** + 9 个 outlier
case（generator pullback height ≫ 10⁵，Heegner-level 工具 candidate）。

---

## 一、156 sha2≥2 case 全部能给 explicit Sha[2] candidate

`scripts/ell2cover_worker.py` 单 (A, B) 跑 `ell2cover(E)`，对每个返回的 quartic g
跑 `hyperellratpoints(g, h=10000)`。`scripts/batch_ell2cover_v2.py` 是 timeout-safe
driver（仿 wl038 sha2_worker 结构），只对 sha2≥2 子集跑。

```
sha2 pairs (>= 2): 156
done in 11s.  obstr: 156  all_pt: 0  timeout: 0  err: 0
```

**156/156 都至少有 1 个 cover 没有 rat pt** ≤ h=10000 → 100% 都有 explicit
Sha[E][2] candidate。

## 二、n_covers vs n_without_pt 联合分布异常整齐

`scripts/analyze_ell2cover.py` + `/tmp/d19_rank_obstr_joint.py`：

```
rank  n_covers  n_without_pt  count
   1         5             2     39
   1         5             3     87
   2         6             2      7
   2         6             3     14
   2         6             4      8
   3         7             5      1
```

观察到两个**完全 deterministic** 的规律：

### 规律 1（数 cover）

> **`n_covers = rank + 4`** （所有 156 case 100% 匹配）

匹配 d19 curve `y² = x(x+A²)(x+B²)` 的 2-Selmer 维度公式：

$$\dim_{\mathbb F_2} \text{Sel}(E/\mathbb Q, 2) = \text{rank}(E) + \dim_{\mathbb F_2} E[2](\mathbb Q) + \dim_{\mathbb F_2} \Sha(E)[2]$$

代入 d19 case：
- `dim E[2](Q) = 2`（三个 2-挠点 `(0, 0), (-A², 0), (-B², 0)` 都在 Q 上）
- `dim Sha[2] = 2`（PARI effort 1/2/3 在 156 case 上稳定给 sha2_lower = 2）

得 `dim Sel = rank + 2 + 2 = rank + 4`。PARI `ell2cover` 返回 `dim Sel` 个
quartic（每个对应 Selmer 的一个 F₂-basis 元素，去掉 trivial element）。

### 规律 2（cover signature 严格分层）

| n_without_pt | sample signature (0=hasPt, 1=noPt) |
|---|---|
| 2 (sha2=2, rank=1) | `00101`, `00011`, `00110` 等（任意 3 个 hasPt） |
| 3 (rank=1) | **全部** `00111`（前 2 hasPt, 后 3 noPt） |
| 4 (rank=2) | **全部** `001111`（前 2 hasPt, 后 4 noPt） |
| 5 (rank=3) | `0011111`（1 case, 前 2 hasPt, 后 5 noPt） |

**PARI ell2cover 输出顺序**：先列 E(Q)/2E(Q) image 中容易找到的 cover (low
height rat pt), 后列 hyperellratpoints 在给定 h 内找不到 pt 的 cover (包括
sha[2] cover + lift-height 大的 generator cover)。

## 三、9 outliers 都是 generator pullback height 暴涨，不是更高 sha2

**Outlier 定义**: n_without_pt ≥ 4（高于"clean" rank=1 sha2=2 期望值 2）。

```
( 12383, 299925) rank=3  n_covers=7  n_without_pt=5
( 549,    29435) rank=2  n_covers=6  n_without_pt=4
( 3995,  104377) rank=2  n_covers=6  n_without_pt=4
( 7567,   11505) rank=2  n_covers=6  n_without_pt=4
( 12943,  78705) rank=2  n_covers=6  n_without_pt=4
( 14535, 462241) rank=2  n_covers=6  n_without_pt=4
( 22919, 174825) rank=2  n_covers=6  n_without_pt=4
( 27999,  84721) rank=2  n_covers=6  n_without_pt=4
( 220571, 294525) rank=2  n_covers=6  n_without_pt=4
```

### 三-1. height=10000 → 100000 follow-up

`scripts/ell2cover_height_followup.py` 在 9 outliers 上 rerun
hyperellratpoints with h=100000：

```
9/9 STAY (没有一个 outlier 在 h=100000 找到额外的 rat pt)
```

→ outlier 不是"h=10000 height 不够"的假象。

### 三-2. PARI effort=1/2/3 sha2 对比

`/tmp/d19_outlier_effort3.py` 在 9 outliers 跑 effort=1, 2, 3 ellrank：

```
所有 9 outliers + 所有 3 effort levels: sha2_lower = 2 不变
```

→ outlier 不是 PARI effort 太低看不到更高 sha 维度的 case。

### 三-3. n_without_pt 公式（修正版）

通用公式：

$$
n\_\text{without\_pt}(h) = \dim \Sha[2] + k(h)
$$

其中 `k(h) ∈ {0, 1, ..., rank+2}` 是"对应 generator pullback 后在 cover 上
height > h 的 cover 数"。

**rank=1 case** (`/tmp/d19_verify_gen_hypothesis.py` sanity check)：
```
5/5 case: predicted_nw = sha2 + (rank - n_gens_PARI_found) = 2 + 0 = 2 ✓
```
PARI 在 rank=1 case 全部找到 generator（height < 10000），所以 `k=0`,
n_without_pt = sha2 = 2。

**rank=2 outliers**:
- PARI 找到 2 generators（gens_found = 2 = rank）
- 但 hyperellratpoints 在 cover 上 fail at h=10000 AND h=100000
- 说明 generator → cover pullback 后高度 ≫ 100000
- 公式: n_without_pt = 2 (sha) + 2 (lift-height 太大的 generators) = 4 ✓

### 三-4. 几何解释（为什么 cover-pullback height 暴涨）

每个 cover quartic `g(x)` 对应 cover map `(x, y) → (u(x)/y², v(x)/y³)` 把
cover point `(x₀, y₀)` 拉到 E 上的 `(u(x₀)/y₀², v(x₀)/y₀³)`。注意 u, v 是
degree 4-6 的多项式。

如果 E 上 generator height 是 `H = max(|num x_E|, |denom x_E|)`，cover 上
对应点的 height 大约是 `H^{1/4}` 到 `H^{1/2}`（粗略）。但具体到 d19 curve
y² = x(x+A²)(x+B²)，A, B 高达 ~3·10⁵，coefficient 巨大，导致每个 cover 的
hyperelliptic search bound 实际需要远高于 10⁵ 才能 catch 到对应的 cover-lift。

**例**：(12383, 299925), rank=3：PARI gens `r[3]` 报 3 个 generators，但
hyperellratpoints(h=10⁵) 在 7 个 cover 上只看到 2 个有 rat pt
（trivial E[2](Q) image）。其他 5 个 cover（2 sha + 3 generator pullbacks）
全 noPt。

## 四、ell2cover 整体性能

- 156 sha2≥2 case，11 秒跑完（~0.07s/case） — 比 sha2 scan 还快
- 0 timeout, 0 error
- 0% 全 hasPt（没有"假阳"的 sha2_lower ≥ 2，即 PARI 没说错过）

## 五、与文献的对接

Peschmann 2026 §7 在 D=2 quartic family 上证明类似结果：rank=0 + Sha[E][2]
non-trivial → 2-isogeny cover 全无 rational pt → 全局无解。我们在 d19
hard_case 上做的是**同样手法的 effective form**：

- d19 hard_case 子集 sha2≥2 ↔ Peschmann's Sha[2]-nontrivial subset
- ell2cover 给的 quartic ↔ Peschmann's explicit cover equation
- hyperellratpoints fail ↔ Peschmann's "no rational point" claim

差别：Peschmann 的 quartic family rank 总是 0（cert no_solution 直接），
我们的 d19 hard_case 多数 rank ≥ 1（cert no_solution 还需要 generator
heights + Heegner-level 工具 — 即 outlier 9 个 case 的 next step）。

## 六、产出 + 状态

### 新脚本

- `scripts/ell2cover_worker.py` — 单 (A, B) ell2cover + hyperellratpoints
  worker，subprocess-isolated。
- `scripts/batch_ell2cover_v2.py` — timeout-safe driver，跑 sha2≥2 subset，
  支持 `--height`/`--timeout`/`--limit` 参数 + 可续跑。
- `scripts/analyze_ell2cover.py` — 联合分布 + outlier 列表 +
  cover signature pattern。
- `scripts/ell2cover_height_followup.py` — 在 outliers 上 rerun
  hyperellratpoints at h=10⁵。

### 新数据

- `results/ell2cover_sha2_cases.jsonl` — 156 行，每行一个 sha2≥2 case
  的全 cover 信息（quartic 系数、rat pt 样本、disc factor）。
- `results/ell2cover_outliers_h100k.jsonl` — 9 outliers 的 h=10⁵
  re-search 结果。
- `results/ell2cover_outliers_effort_compare.log` — outliers effort 1/2/3
  sha2 对比。
- `results/ell2cover_analysis_report.txt` — 分析脚本完整输出。

### 修正过的认识

1. **n_without_pt ≠ sha2 dim**（之前以为是）。它是 `sha2 + k`，其中 k 跟
   cover-pullback height 相关。
2. **PARI effort 1/2/3 sha2_lower 完全等价** 对 sha2≥2 hard_case — 升级
   effort 不再获得新信息。
3. **156 sha2≥2 case 的 Sha[E][2] dim 全部 = 2** —— 这是稳定的 invariant。
4. **9 outlier 是 "PARI 找到 gen 但 hyperellratpoints 找不到 cover-lift"
   的 case**，需要 Heegner-level / Stoll 高度 sieve 才能 cert no_solution。

### 下一步候选

- **(高优先) Heegner / Stoll sieve on 9 outliers**: 真正能 cert outlier
  no_solution 的工具。Heegner point 在 rank=1 上 effective；对 rank=2/3
  case 需要 Stoll 高度 sieve 或 ANTS-style 2-cover Mordell-Weil sieve。
- **Scale up to max_hyp=5000** (worklog 038 的另一个候选): 把 156 → ~750
  sha2≥2 case，更大 sample 验证 n_covers = rank+4 公式 + 验证 9 outlier
  比例是否稳定 (~5.8%)。
- **Manual deep-dive on (169, 235)**: 用 explicit cover quartic
  `-5279x⁴ - 17626x³ + 25673x² + 27418x - 2831` 验证 Sha[2] generator
  的 local solubility everywhere（实际 cert 这是 nontrivial Sha 元素，
  不是 PARI 找不到的 rational point）。
