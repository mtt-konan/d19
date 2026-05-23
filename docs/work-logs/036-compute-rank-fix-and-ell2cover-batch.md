# 036 — compute_rank bug fix + 320 hard_case ell2cover batch

**日期**: 2026-05-23
**触发原因**: worklog 035 发现 cypari2 暴露的 PARI Selmer API 比项目当前使用
的多得多——`ellrank` 实际返回 4 元组而项目只用前 3 项，丢了 Sha[2] 信息。本
worklog 修该 bug 并把"无需装 Sage 的 2-descent"思路在 320 hard_case 上做了
首次实证。
**输出**: 1 项目级 bug 修复 + 1 个 effort 实测脚本 + 1 个 batch ell2cover 脚本 +
首次显式追踪到 2 个非平凡 Sha[2] hard_case。

---

## 一、effort 默认值实测（决定 compute_rank 的新默认）

worklog 033 在 dual EC probe 中发现：cypari2 的 `pari.ellrank(E)` 默认 effort
（无 effort 参数）会系统性给出虚假 `lower=0`。worklog 035 提议默认 effort=2，
但没拿数据。

`scripts/compare_ellrank_effort.py` 在 7 个 chain near-miss（worklog 033 的
deep recheck 升级 case）+ 4 个小 (A, B) 上跑了 effort = 0 / 1 / 2，得到：

| | hard certified | hard 总时 | small certified | small 总时 |
|---|---|---|---|---|
| effort=0 (现状) | **1/7** | 0.20s | 4/4 | <0.01s |
| **effort=1 (新默认)** | **7/7** | **0.27s (+33%)** | 4/4 | <0.01s |
| effort=2 | 7/7 | 0.64s (×3.2) | 4/4 | <0.01s |

**结论**：`effort=1` 是最佳折中，比 effort=0 仅多 33% 时间但 hard case 全部
certified；effort=2 多花 ×2.4 时间没多 certified。

输出: `results/ellrank_effort_compare.json`

## 二、compute_rank bug fix

### 旧签名（项目级 bug）

```python
def compute_rank(A, B, pari=None, *, profile=None) -> tuple[int, tuple[int, int], list]:
    # 实现里 pari.ellrank(E) 默认 effort=0
    # result[0], result[1] -> (lower, upper)
    # 跳过 result[2] = sha2_lower
    # result[3] -> generators
    return rank, (lower, upper), gens
```

两个 bug 叠加：
1. **静默丢失 sha2_lower**：PARI 的 `ellrank(E, effort)` 返回 4 元组
   `[rank_lower, rank_upper, sha2_lower, gens]`。我们一直只用前 3 项，
   `sha2_lower` 字段直接被忽略
2. **默认 effort 太浅**：worklog 033 hard case 上 6/7 给出虚假 `lower=0`

### 新签名

```python
def compute_rank(
    A, B, pari=None, *,
    profile=None,
    effort: int = 1,
) -> tuple[int, tuple[int, int], int, list]:
    # 显式 pari.ellrank(E, effort) 调用
    # 返回完整 4 元组
    return rank, (lower, upper), sha2_lower, gens
```

`ConcordantResult` dataclass 也加了 `sha2_lower: int | None = None` 字段，
`summary()` 在 `sha2_lower > 0` 时显示。

### 调用点适配（4 处）

| 文件 | 调用 | 改法 |
|---|---|---|
| `src/.../concordant/analysis.py` `analyze_pair` | 3-tuple unpack | 加 sha2_lower 解包，传给 ConcordantResult |
| `src/.../proof_status/methods.py` `_method_rank_zero` | 3-tuple unpack | 加 sha2_lower 进 details dict |
| `scripts/probe_dual_ec.py` `safe_rank` | 3-tuple unpack | 返回 5-tuple，调用点 unpack 5 元素，JSONL 加 sha2_ac/sha2_bd 字段 |
| `tests/test_concordant.py` 2 处 | 3-tuple unpack | 改 4-tuple，加 `assert sha2_lower >= 0` |

### 验证

`uv run pytest -x` → **194/194 通过**，零 regression。

## 三、320 hard_case 上的 ell2cover 批量

`scripts/batch_ell2cover_hard_cases.py` 从 `results/proof_status.db`（max_hyp=500
的 6172 个 reduced (A,B) pair，320 hard_case）拉每个 hard_case，跑：

- `pari.ellrank(E, 1)` 拿 rank + sha2_lower（4 元组完整）
- `pari.ell2cover(E)` 拿 Selmer 群的 quartic covers（系数列表）

**3.6 秒处理完 320 case**，输出 JSONL 每行包括 (A, B, rank, sha2, n_covers,
quartic_covers 系数列表, timing)。

### 全 320 hard_case rank 分布（与 wl031 一致）

| rank | 数量 | 占比 |
|---|---|---|
| 1 | 118 | 36.9% |
| 2 | 155 | 48.4% |
| 3 | 43 | 13.4% |
| 4 | 4 | 1.3% |

### Sha[2] 分布（**新发现**）

| sha2_lower | 数量 |
|---|---|
| 0 | 318 |
| **2** | **2** ← 项目首次追踪到非平凡 Sha[2] |

### 两个非平凡 Sha[2] case

| (A, B) | rank | sha2_lower | n_quartic_covers |
|---|---|---|---|
| (243, 1085) | 1 | 2 | 5 |
| (3969, 15895) | 1 | 2 | 5 |

观察：
- 两个都是 rank=1
- 243 = 3⁵, 1085 = 5 × 7 × 31, gcd(243, 1085) = 1
- 3969 = 3⁴ × 7², 15895 = 5 × 11 × 17², gcd(3969, 15895) = 1
- 两个 case 不互为倍数（3969/243 = 49/3）

之前 d19 项目从未显式追踪 Sha[2]——这是 worklog 035 修复 `compute_rank` 4-tuple
bug 的直接收益。这两个 case 的 Mordell-Weil generator + Selmer 结构值得后续深挑。

### Selmer 维度公式（实证）

```
n_quartic_covers = rank_lower + 2 + sha2_lower
```

318 个 sha2=0 case + 2 个 sha2=2 case 全部满足。这跟 PARI `ell2cover` 的
"Selmer 群 generators 模 trivial" 语义一致——常数 "+2" 来自 `dim_F2(E[2](Q)) - 1`
（$E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 三根全有理，$|E[2](Q)| = 4$，dim = 2）。

## 四、与 Peschmann §7 的对比（hard_case 视角）

| | Peschmann (cuboid) | d19 (chain) |
|---|---|---|
| 实验对象 | 5 hard specialisations × 175,418 lattice points | 320 hard_case (A, B) pairs |
| Selmer 群验证 | 42 个 $E_A$ + 54 个 $E'_A$ certified rank=0 | 0 个 hard_case rank=0（全 ≥ 1）|
| 非平凡 Sha[2] | 未显式报告 | 2/320 (0.625%) |
| Selmer dim 中位数 | 未报告 | 4（≈ rank=2 + 2） |

Peschmann 的 §7(2) modular search（45 primes < 200）在 d19 的对应物——把现有
safe_sieve（mod 1680, ~5 primes）扩展到这个规模——是 worklog 037 的目标。

## 五、可能的后续方向（worklog 037+）

### A. 扩展 safe_sieve 到 Peschmann §7(2) 规模

把现有 safe_sieve 从 mod 1680 (~5 primes) 升级到 45 primes < 200，对 320
hard_case 跑 finite-descent。可能让 hard_case 中一部分被 sieve 砍掉。

### B. 深挑 (243, 1085) 和 (3969, 15895)

- 用 `pari.ellgen(E)` 拿 Mordell-Weil generator，看 X 坐标
- 用 `pari.ellrootno(E)` 看 root number（影响 BSD 解析 rank 预测）
- 看这两个 (A, B) 在 chain near-miss 数据集中是否有对应的 chain 候选
- 看是否能用 Sha[2] 的非平凡构造提取 obstruction

### C. 对 sha2_lower > 0 的两个 case 做 Cassels-Tate pairing

PARI 有 `elltatepairing`，理论上能区分 Sha 中真正的元素。但需要先拿到 Sha[2]
的代表（quartic covers 给出）。

### D. 把 `compute_rank` 的 sha2_lower 接进 proof_status pipeline 的判定逻辑

当前 `_method_rank_zero` 只用 rank。理论上 sha2_lower > 0 给出更细致的诊断
信息（rank + Sha 共同决定 2-Selmer 大小）。但短期没明显收益，因为这两个 case
仍然是 hard_case（rank ≥ 1）。

---

## 输出物

### 新增脚本
- `scripts/compare_ellrank_effort.py` — effort=0/1/2 实测，决定默认 effort
- `scripts/batch_ell2cover_hard_cases.py` — 320 hard_case 上批量跑 Selmer covers

### 修改代码（带 test 验证）
- `src/rational_distance/concordant/analysis.py`
  - `compute_rank()` 签名扩展 + effort=1 默认
  - `ConcordantResult` 加 `sha2_lower` 字段
  - `analyze_pair` 适配新签名
- `src/rational_distance/proof_status/methods.py` — `_method_rank_zero` 适配
- `scripts/probe_dual_ec.py` — `safe_rank` 返回 5-tuple，JSONL 加 sha2 字段
- `tests/test_concordant.py` — 2 处 unpack 改 4-tuple

### 数据
- `results/ellrank_effort_compare.json` — 11 case × 3 effort
- `results/proof_status.db` — max_hyp=500 重建（4s）
- `results/ell2cover_hard_cases.jsonl` — 320 hard_case Selmer 数据

### 复现命令

```bash
# 1. effort 比较（< 1s）
uv run python scripts/compare_ellrank_effort.py

# 2. proof_status pipeline（4s）
uv run python scripts/prove_no_solution.py --db results/proof_status.db --max-hyp 500 --no-progress

# 3. 320 hard_case ell2cover 批量（3.6s）
uv run python scripts/batch_ell2cover_hard_cases.py

# 4. 测试（30s）
uv run pytest -x
```
