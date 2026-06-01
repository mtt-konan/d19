# wl094 — A.9 落地：把生产闭合判据升级成全平面 GEN-CLOSURE 判定器

## 任务

承接 wl093（A.9 几何引理）：把 wl093 推出的**全平面充要条件** GEN-CLOSURE

```
{N₁+N₂, |N₁−N₂|} ∩ {A+B, |A−B|} ≠ ∅
```

从「只在脚本里验证」**落地进生产 pipeline**。此前生产判据只检验**和关系** `N₁+N₂=A+B`
（正方形内），所以全平面无反例只能报 `inconclusive`/`hard_case`；本次升级后，残余的
hard_case 在**全平面（互素腿）**下被判 `no_solution`。

因改 `no_solution` 语义、牵动既有测试，wl093 已声明留单独分支/PR。本 wl 即该落地。

## 改了什么

### 1. `concordant/chain_closure_sieve.py`：`killed_at_modulus(..., full_plane=)`

新增 `full_plane: bool = False` 参数（向后兼容默认不变），传到 `find_killer_modulus` /
`all_killer_moduli`。

- `full_plane=False`（旧）：只查和关系 `T ∩ ((A+B)−T)`，对应正方形内。
- `full_plane=True`（新，GEN-CLOSURE）：对 `s ∈ {A+B, |A−B|}` 各查
  - 和关系 `N₁+N₂≡s`：`T ∩ (s−T)`
  - 差关系 `N₁−N₂≡s`：`T ∩ (T+s)`
  四个全不可满足才算 killed。这是 mod-M 上 GEN-CLOSURE 的**健全**否证（任何真解
  reduce mod M 必落入某一关系），故无假阴性。

### 2. `concordant/analysis.py`：`gen_closure_hit(A, B, concordant_n)`

在**穷尽** concordant 集（factor_search 给出的全部整数 N）上做 GEN-CLOSURE 测试：枚举
N 对 `(Nᵢ,Nⱼ)`，命中任一关系即返回 `(Nᵢ,Nⱼ,relation)`，否则 `None`。`None` ⇒ 该约化
互素腿 `(A,B)` 无反例（modulo §8.6 gcd-scaling，见下）。原 `check_chain_compatibility`
保留为「正方形内（和关系）」的向后兼容诊断。

### 3. `proof_status/methods.py`：两个方法接上全平面语义

- `run_chain_closure_mod_sieve` 改调 `find_killer_modulus(..., full_plane=True)`。
  全平面 kill 率比 sum-only 严格低（max_hyp=2000：97.0% vs 99.4%），但**全平面健全**。
- `run_factor_concordant` 改用 `gen_closure_hit`：
  - 无 concordant N ⇒ `no_solution`（不变）。
  - 有 GEN-CLOSURE 命中 ⇒ `solution_found`（会反驳 Harborth）。
  - 否则（穷尽枚举无命中）⇒ **`no_solution`**（旧为 `inconclusive`）。

`run_factor_concordant` 因此成为**穷尽、全 rank、无 Magma** 的判定器（对约化互素腿）。在
默认 pipeline 顺序里它排在 PARI/EC 方法之前，会**提前终止**：`f2_rank`/`rank_zero`/
`heegner`/`chabauty`/`brauer_manin` 对到达它的对几乎不再触发（保留给显式/研究用 pipeline
及 §8.6 gcd 子问题）。`heegner` 仍保守（只记 rank-1 height 证据 + 正向 witness，永不报
`no_solution`）。

## 实测（全默认 pipeline，PARI-free 提前终止）

逐对跑 `compute_pair_status`（默认 pipeline），统计 `final_status`
（脚本 `scripts/theory/validate_gen_closure_pipeline.py`）：

| max_hyp | pairs | no_solution | hard_case | solution_found | 用时 |
|---|---|---|---|---|---|
| 400 | 3,825 | **3,825** | 0 | 0 | 0.1s |
| 2000 | 99,311 | **99,311** | 0 | 0 | 1.6s |

max_hyp=2000 的方法分解：`safe_sieve` 91,091 + `chain_closure_mod_sieve`（全平面）7,975
+ `factor_concordant`（GEN-CLOSURE）245 = 99,311。即升级后**全部互素约化对在 max_hyp≤2000
被判 no_solution，0 hard_case**，全程不调 PARI。其中 245 对是穿过全平面 mod 筛后由
穷尽 GEN-CLOSURE 因子判定器收口的（旧 sum-only 下这些会落到 `inconclusive`/EC 层）。

对照 wl092 的残余分析：当年 max_hyp=500 的 7 个残余 inconclusive hard_case 全是 rank≥2、
`heegner` 看不到；现在它们由 `factor_concordant` 的全平面 GEN-CLOSURE 直接判 `no_solution`，
无需任何 EC/height/Chabauty。

## 测试

322 测试全过。语义变化牵动的 8 个测试已按新语义更新（非「为过而改」，每处都标了 wl094 原因）：

- `test_factor_concordant_gen_closure_decides_no_solution`（原 legacy 测）/
  `test_finds_concordant_for_264_420`：(264,420) 4 个 concordant N，无 GEN-CLOSURE 命中
  ⇒ `no_solution`（旧断言 `inconclusive`），并断言 `gen_closure_hit is None`。
- `test_stops_after_first_killer_modulus`：monkeypatch 的假 `killed_at_modulus` 现接受
  `full_plane` kwarg 并断言 pipeline 传 `full_plane=True`。
- `test_gen_closure_pair_becomes_no_solution`（原 `..._becomes_hard_case`）：(7,45) ⇒
  `no_solution` via `factor_concordant`。
- `test_status_counts_aggregate`：(1,5)/(1,3)/(7,45) 全 `no_solution`（no_solution=3,
  hard_case=0）。
- cache-reuse / f2_rank-ordering 三测：`f2_rank_pipeline` fixture 现把 `f2_rank` 排在
  终止性 `factor_concordant` **之前**（默认顺序下 factor 终止，f2 不会跑），以继续覆盖
  f2_rank 步骤与共享 concordant-N 缓存；断言 `final_status == no_solution`、find 只调一次、
  `f2_rank` 索引 < `factor_concordant` 索引。

lint：我改的三个源文件未引入新错误（仓库既存的 RUF003 全角标点 / E402 与本次无关）。

## 仍开放（与 wl093 一致，未被本次改变）

- (a) **§8.6 gcd-scaling 覆盖**：`generate_ab_pairs` 只产互素对，非互素腿 `(gA',gB')` 的
  反例在约化对上不可见。这对 sum-only 与升级后判据**同样存在**，是独立 gap。GEN-CLOSURE
  把「互素腿无反例」做成了判定器，但彻底证明 Harborth 仍需覆盖 (a)。
- (b) rank≥2 的结论性外部工具（Chabauty B.1 / Brauer–Manin A.4）——GEN-CLOSURE 不依赖
  它们（这正是杠杆所在），但 (a) 仍需独立解决。
