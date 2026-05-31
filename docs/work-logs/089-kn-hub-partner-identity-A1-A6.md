# wl089 — A.1 / A.6：K_n hub partner identity 分析 + 修复 compute_rank 有理 generator bug

## 背景

OPEN_DIRECTIONS **A.1**（K_n hub partner identity 推广，HIGH-ROI）想知道：一个
K_n hub（n 个 multi-N pair 共享一组 partner / 构成团）是否给出单个 multi-N pair
没有的代数 closure 障碍 —— 即能否把 path-A 的论证推到更高 k。**A.6** 是它的纸面
地基：K_n 与 4-chain 的严格关系。

本 wl 用既有的 wl086（A.2）machinery 把这两条一起做掉，并在过程中**修了一个真
bug**（`compute_rank` 把有理 generator 坐标 int 截断）。无长跑。

## A.6 — 两个结构事实（先于 A.1）

用 `results/partner/partner_kn_subgraphs.jsonl`（28 个 hub）核验：

**(1) shared_partner 对偶**：shared_partner K_n（n 个节点共享一个 partner pair
(P_a, P_b)）**等价于** partner pair (P_a, P_b) 自身是 k≥n 的 multi-N pair，其
concordant-N 集合包含这 n 个节点 —— 即 (A,B) ↔ N 的对偶。对全部 17 个
shared_partner hub 跑权威 `find_concordant_by_factorization`：**17/17 成立**
（nodes ⊆ N(partner)）。

```
partner=(2640,21216) gcd=48 n=5 k(partner)=6 nodes⊆N=True
partner=(168,660)    gcd=12 n=3 k(partner)=3 nodes⊆N=True
... (17/17)
```

**(2) general K_n 上限**：general K_n 要求 n 个节点两两都是 multi-N pair（C(n,2)
条边全在 catalog）。在 max100000 互素 catalog 中**只有 11 个 general K_3，0 个
K_4+**。这印证了 A.1 文档里诚实标注的风险（"reduced coprime safe-pass 里没有
K≥5"）—— 想靠 general K_n 拿到更高 k 的结构，在现有尺度是空的。

## A.1 — 每条 hub 边的 2-可除性

对每个 hub 的每条边 (a,b)（general hub 用其显式 edge 列表的 shared
concordant_N；shared_partner hub 用 partner pair 本身这条对偶 multi-N 曲线），复用
wl086 的 `analyze_cycle_relations`，检查 shared concordant 点 Q_N 是否落在
2·E_{a,b}(ℚ)：

```
[A.1 summary] edges checked=49 all_two_divisible=49/49 skipped=1
```

**49/49 全部 2-可除**（唯一 skip 是 b=139308 超过 cost guard 的那条）。

**结论（negative but informative，A.1 关闭）**：每个 shared concordant 点在它**自己
那条曲线**上就是 2-可除的（与 wl086/A.2 对单 pair 的结论一致），这与 hub 是否
"共享" 无关。K_n hub 的 "sharing" 只是不同曲线（一般 j-invariant 不同）之间
N 值的巧合，**不是代数 linkage**，因此不提供跨边的 closure 障碍。A.1 撞上和 A.2
同一堵墙：要把 path-A 推到更高 k，需要的是一个**新的**代数恒等式，而不是 hub
的巧合。真正的杠杆仍是 height bound（Heegner 过滤器→判定器）与 rank≥2 Chabauty。

## 顺手修的 bug：`compute_rank` 截断有理 generator 坐标

跑 A.1 时约 40% 的曲线报 `PariError: domain error in ellheight: point not on E`。
根因：`analysis.compute_rank` 提取 generator 时用 `(int(pt[0]), int(pt[1]))`，但
PARI `ellrank` 返回的 generator **可以有有理坐标**，例如 (425,1001)：

```
gen 2 = [-5504345/9, 8661181760/27]   # int 截断 -> (-611593, 320784509)，不在曲线上
```

int 截断把点弄坏，喂给 `ellheight`/`elladd` 即报 "point not on E"。这是 wl086
`cycle_relations` 一直存在的隐性 bug（只是 wl058 6-cycle sample 恰好都是整坐标
generator，没触发）。

**修法**（最小、低风险）：

- `analysis.py`：抽出 `_ellrank_raw()`（跑一次 ellrank，返回**原始 PARI 点对象**，
  有理坐标精确保留）；`compute_rank` 仍对外返回 int 截断的 (x,y)（向后兼容所有
  现有 caller，行为逐字节不变）；新增 `compute_rank_exact_points()` 返回精确点。
- `cycle_relations.mw_coordinates`：改用 `compute_rank_exact_points`，直接拿精确
  PARI 点做 height pairing / `elladd`；`CycleRelationResult.generators` 改存精确
  坐标字符串（可能是分数）。

修复后 A.1 分析从 31 checked / 19 skipped → **49 checked / 1 skipped**。

注：少数边 `all_verified=False`，是因为高 rank 曲线上 float height-pairing 的
`_solve_round` 没能精确定出某些点的整数坐标；但 `two_divisible` 是直接用
`ellisdivisible` 判的，与坐标求解无关，故 49/49 的 2-可除结论稳健。

## 验证

```bash
PARI_MT_ENGINE=single PYTHONPATH=src uv run pytest -q     # 323 passed
uv run ruff format --check / ruff check                   # clean
PARI_MT_ENGINE=single uv run python scripts/partner/kn_partner_identity.py
```

新增回归测试 `test_rational_generator_coords_do_not_raise`：(425,1001) 含有理
generator，分析不再抛错、`all_two_divisible` 为真、`generators` 含分数字符串。

产物：`scripts/partner/kn_partner_identity.py`、
`results/partner/kn_partner_identity.jsonl`。

A.1 / A.6 已在 OPEN_DIRECTIONS 标记完成。
