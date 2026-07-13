# scripts/ — 脚本入口索引

按主题分组. 顶层只放主入口与常用 lookup 工具. 每个子目录有自己的功能集合.

## 顶层 (主入口)

| 脚本 | 用途 |
|------|------|
| `search.py` | 主搜索 CLI (chain-fast / EC / parametric, 见 `--help`) |
| `prove_no_solution.py` | 增量证明 hard_case 不可解 (proof_status pipeline) |
| `prove_no_solution_multi_first.py` | multi-N first variant of `prove_no_solution` |
| `lookup_multi_n.py` | 给 (A, B) 查 concordant N 列表 (常用查询工具) |

## 子目录

### `benchmark/` — 性能基准

| 脚本 | 用途 |
|------|------|
| `benchmark_candidate_generators.py` | 比较 safe / non_coprime / multi_n 三种候选生成方式 (wl072) |
| `benchmark_ab_sieve_orders.py` | proof_status A/B sieve 顺序基准 (wl067-068) |
| `benchmark_parallel_executor.py` | parallel executor 复用 vs 重建池基准 (wl064) |
| `bench_mod_sieve.py` | mod sieve 微基准 |

### `multi_n/` — multi-N 枚举与目录

| 脚本 | 用途 |
|------|------|
| `fast_multi_concordant_scan.py` | pivot-on-N 快速枚举 (wl048) |
| `multi_concordant_n_scan.py` | 老版 (A,B)-pivot 枚举 (wl046, 慢但可对照) |
| `non_coprime_multi_n_scan.py` | 非互素 (a,b) multi-N 扫描 (wl056) |
| `build_results_catalog.py` | 结果目录构建 |
| `k_distribution_audit.py` | k 分布 (safe-pass vs unsafe) 统计 (wl084) |
| `validate_fast_multi_n.py` | fast scanner 与朴素扫描的一致性校验 |
| `dscale_kn_generator.py` | D-scaling K_n 快速生成器 (wl085, A.7 落地) |

### `partner/` — Partner graph (G_M) / K_n hub 分析

BFS / 全图构建:
- `partner_bfs.py` — 单源 BFS
- `partner_full_bfs.py` — 全 G_M BFS (并行)
- `partner_full_graph.py` — 全图持久化
- `partner_full_graph_query.py` — 查询接口
- `partner_pair_graph.py` — pair-level 图
- `partner_pair_k_distribution.py` — pair k 分布

分析 / 可视化:
- `partner_bfs_analyze.py` — BFS 结果分析
- `partner_bfs_plot.py` — 子图绘制
- `partner_kn_subgraphs.py` — K_n 子图抽取
- `comp0_analyze.py` — 超大 component 0 拓扑分析 (wl062)
- `export_gephi_component.py` — Gephi 导出
- `find_partner_origin.py` — partner 来源回溯
- `verify_missing_partner.py` / `verify_kn_equivalence.py` — 一致性校验

K_n 实例 + 全 G_M closure:
- `full_gm_closure_scan.py` — G_M 反例彻底搜索 (wl063)
- `full_gm_delta_stats.py` — delta near-miss 统计 (wl066)
- `k8_ellrank.py` — K_8 实例 ellrank (wl060)
- `k9_inspect.py` — K_9 hub 检查 (wl062)
- `k10_extract_and_ellrank.py` — K_10 实例分析 (wl065)
- `cycle_ellrank.py` — cycle / deficit 分析 (wl059)

### `theory/` — Path A / closure / F₂-rank 实证

Path A 主线 (k=2 → k=n):
- `analyze_k2_closure_fiber.py` — k=2 closure fiber 实证 (wl074)
- `analyze_k2_f2_rank.py` — k=2 F₂-rank 实证 (wl076)
- `analyze_k2_height_bound.py` — k=2 height bound 实证 (wl077)
- `analyze_kn_f2_rank.py` — 通用 k=n F₂-rank 实证 (wl084)
- `analyze_k4_signatures.py` — k=4 signatures 探索

Pythagorean / half-points:
- `analyze_a2_pythagorean.py` — A2 conjecture (wl081)
- `analyze_multi_n_half_points.py` — multi-N half-points 列表
- `audit_halfpoint_factorization.py` — half-point 因式分解 audit (wl083)
- `verify_a1_proof_chain.py` — A1 证明链端到端验证 (wl083, ⚠️ 见 wl084 修正)
- `d_valuation_analysis.py` — d_2/d_3 估值分析

F₂-rank 工具:
- `classify_multi_n_by_f2_rank.py` — F₂-rank 分类器 (wl049)
- `pari_rank_high_f2.py` — high F₂-rank pair PARI ellrank (wl050)
- `k4_rank.py` / `k4_two_descent_rank.py` — k=4 rank 实测
- `rank_mixed_closure_curves.py` — 闭合条件混合商曲线 rank 实验 (wl290)

Rank-zero Selmer / AA+BB audit helpers:
- `wl481-wl490` complete d-coordinate setup and first ambient `u_3` route.
- `wl491-wl522` AA+BB admissibility filter, finite `M_tail` shell routing,
  and support/cover taxonomy. Read
  `docs/work-logs/491-522-aa-bb-admissibility-taxonomy-consolidated.md` first.
- Latest compact executable checkpoint:
  `audit_closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint.py`.
- Current handoff:
  `wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop`.
  `wl527` found the named cover families were not ready for a later uniform
  squareclass proof attempt. `wl528` then builds only the first selected
  `support=v_5|L=1|T=5|d=(5,1,5)` prototype, derives the model/maps/`N,M`,
  and proves the opposite product is nonsquare in that prototype function
  field by specialization. `wl529` then classifies the rational points on the
  specialization-square locus through an elliptic quotient and proves that no
  square specialization lifts to the prototype in the positivity domain. It
  does not prove the uniform lemma, execute shell 11, or claim Selmer progress.
  `wl530` derives the exact symbolic pure `v_ell,L=1,T=ell,d=(ell,1,ell)`
  family and recovers those formulas at `ell=5`. `wl531` then handles M2 only
  to the exact `X`-fiber-product square-lift proposition: it eliminates the
  chart variables, handles square-`X`, positivity, and complete-`d` lift
  compatibility exactly, and stops at one remaining arithmetic proposition.
  `wl532` shrinks that proposition again: every odd prime `ell ≡ 3 (mod 4)` is
  excluded exactly, and the remaining `ell ≡ 1 (mod 4)` case is one
  `Q`-coordinate quartic-square obstruction rather than a proof of uniform
  exclusion or an M3 step. `wl533` then absorbs the `Q` and `ell-Q` square
  conditions into one rational parameter, and `wl534` removes the automatic
  lower-positivity / `Q=0` branches together with the auxiliary `C,Y` variables,
  leaving one rational parameter with two square predicates and one quartic
  inequality. `wl535` then removes the representation choice `a^2+b^2=ell`
  and the affine `u`-chart from the final statement, leaving the direct
  `q`-root coordinate together with two explicit square predicates, one direct
  positivity polynomial, and one explicit `q`-coordinate quartic curve
  equation. `wl536` excludes `ell ≡ 5 (mod 7)` by a direct 7-adic residue
  argument, and `wl537` independently excludes `ell ≡ 10 (mod 11)`, or
  `ell ≡ 21 (mod 44)` under the standing mod-4 condition. Both are partial
  M2 results. `wl538` adds `ell ≡ 15 (mod 19)`, equivalently
  `ell ≡ 53 (mod 76)`. The full `wl535` proposition remains open.
  `wl539` then adds `ell ≡ 5 (mod 92)` and proves those four auxiliary pairs
  exhaust the direct single-prime good-reduction residue method; another table
  of the same form is not a valid next gate.
  `wl540` then proves the parameter-prime unit/valuation split and shows that
  the simple Hensel-root branch can occur only for `ell ≡ 1 (mod 8)`.
  `wl541` then proves the parameter-prime algebraic square system always has
  a unit local point, so that place alone is exhausted as an obstruction.
  `wl542` couples the first two equations globally and proves every denominator
  prime splits completely in `Q(i,sqrt(ell))`; allowed denominator places then
  add no further local obstruction to the final square condition.
  `wl543` then uses prime-discriminant genus theory to turn the real-quadratic
  square ideal into `alpha=epsilon*beta^2`, leaving at most two totally
  positive unit squareclasses.
  `wl544` expands those classes into one or two exact integer quartic systems
  with full reconstruction of the Gaussian square, `G_ell` square, and
  positivity.
  `wl545` then gives the exact mod-8/2-adic parity split on the trivial unit
  branch and proves the `G` condition adds no further obstruction at `2`.
  `wl546` then replaces the trivial branch Gaussian square by two exact UFD
  orientations coupled to the real-quadratic descent.
  `wl547` then reduces the remaining `G` norm square to finitely many Gaussian
  squareclasses supported over `2(ell-1)`.
  `wl548` then proves the dyadic valuation is always even and removes `1+i`
  from the squarefree support, leaving only selected odd primes over `ell-1`.
  `wl549` then classifies the forced root-square condition at those odd primes
  and proves the standalone common-prime residue test is exhausted for every
  `p ≡ 7 (mod 8)`.
  `wl550` then proves both fixed Gaussian orientations are locally compatible
  with every surviving root-square class at the same common prime.
  `wl551` then uses the global norm square to pair conjugate split-prime
  generators and reduces the squarefree factor to rational
  `r|rad(ell-1)` up to a unit.
  `wl552` then uses dyadic coordinate parity to force the sole Gaussian unit
  class `eta=i` in both mod-8 branches.
  `wl553` then transfers positivity to a binary cone in the Gaussian-square
  coordinates and proves positivity alone is compatible in both branches.
  `wl554` then proves the rational squarefree class is the canonical odd
  squarefree kernel of `gcd(ell-1,R)`, not an independent divisor choice.
  `wl555` then rotates to the unit-free standard norm element
  `F+iE=r(a+ib)^2` and a single uniform positivity cone.
  `wl556` then uses dyadic parity to select `R_pi` for `ell ≡ 5 (mod 8)` and
  `B_pi` for `ell ≡ 1 (mod 8)`, eliminating one orientation per branch.
  `wl557` then classifies the exact valuation strata inside those surviving
  orientations and exhausts standalone dyadic analysis.
  `wl558` then derives the split-prime unit condition
  `Legendre(F/r,p)=1`, coupling each such place to the canonical global class.
  `wl559` then classifies the leading characters at positive even common
  valuations. `wl560` adds odd-common valuation and unifies all odd places
  over `ell-1` under one normalized split-prime master character.
  `wl561` then assembles those characters as an `F_2` system and proves the
  reciprocity product over split primes contained in `r`.
  `wl562` then gives exact mod-13 witnesses showing local source/orientation
  data admits both leading row bits in the same valuation stratum.
  `wl563` then uses the global product coordinate to force complementary
  squarefree parts and the exact scale equation `gMN=h|QD|`.
  `wl564` then assigns the factor `2` to one complementary side whenever it
  occurs, using the mod-8 branch and canonical `r`.
  `wl565` then assigns every inert odd factor by the normalized real-coordinate
  character and leaves only split odd allocation unresolved.
  `wl566` then refines each split factor by an exact quartic-sign rule and
  leaves a finite coupled quartic-character system.
  `wl567` then linearizes that system as an affine `F_2` matrix, removing the
  exponential allocation case split.
  `wl568` then proves the scale, cone, and actual-factorization affine rows add
  no independent obstruction and returns the live trivial-unit gate to the
  selected-orientation/norm-square intersection.
  `wl569` then proves `F<0`, selects the unique positive ordered norm-ratio
  branch, and transfers strict positivity to an exact interval for that ratio.
  `wl570` then eliminates the quartic square root and factors both source
  squares in one exact two-variable `(X,tau)` system with converse recovery.
  `wl571` then proves the product quartic is genus one, the complete generic
  cover is genus five, and `tau=1/2` is the unique genus-one drop.
  `wl572` then excludes that exceptional branch by integrality and positivity,
  leaving only the generic genus-five cover.
  `wl573` then couples the primitive denominators of `q` and `tau` and forces
  `Delta` to divide the positive homogeneous quartic.
  `wl574` then gives both source-factor products the same canonical
  `Delta`-squareclass and bounds their internal gcd support.
  `wl575` then identifies the exact scaled Gaussian rotation coupling the two
  source pairs and proves primitive odd-prime determinant support.
  `wl576` then classifies regular odd-prime side transport and isolates the
  singular higher-valuation determinant cases.
  `wl577` then eliminates all odd singular/crossed cases using `Delta|K`,
  leaving only the factor `2` to compare.
  `wl578` then proves dyadic same-side transport and makes the two
  complementary `k`-allocations identical.
  `wl579` then reduces the remaining projective magnitudes to a smooth
  genus-one Mobius squareclass curve with strict ordering.
  `wl580` then proves primitive reconstruction is unique and certifies the
  allocation/magnitude descent as exhausted after canonical self-consistency.
  `wl581` then maps the generic genus-five cover to a genus-two character
  quotient over `Q` and constructs its degree-two elliptic quotient over
  `Q(i)`, retaining the exact restricted affine candidate image.
  `wl582` then proves that the `S in Q`, non-two-torsion elliptic locus
  reconstructs the genus-two rational point exactly, so the apparent
  quadratic-lift condition is automatic and unrestricted elliptic analysis is
  exhausted.
  `wl583` then retains both individual source squares on a genus-one torsor
  over `Q` and proves that the generic genus-five cover is exactly its
  connected square-`X` fiber product.
  `wl584` then imposes the prime formula, identifies the fixed-`ell` source
  elliptic and its genus-one square-`X` cover, and proves the final norm
  discriminant is the only remaining independent lift.
  `wl585` then identifies the exact fixed-`ell` genus-seventeen cover, proves
  the selected `tau` interval is exactly positivity, and constructs the
  combined source-norm elliptic quotient over `Q`.
  The `wl530-wl585` consolidated checkpoint independently rechecks the key
  algebra, records the full exception audit, and marks the elliptic-quotient
  subroute exhausted without closing M2.
  `wl586` then uses `theory/aa_bb/wl586_route_selection.py`
  to verify three representative `wl522` cover families against the `wl527`
  proof-data inventory and the `wl585` restricted-image result. It records the
  quartic review only as a collapsed read-only candidate, creates no `wl588`,
  certifies the current pure-`v_ell` route dead, and proves the same generic
  opposite-side squareclass is nontrivial on pure-`u_7` and mixed
  `u_3+v_5+w_17`. Because this does not control square specializations, the
  representative-only divisor-parity route is also closed.
  `wl587` then uses `theory/aa_bb/wl587_pure_u7_d0_relative_2_descent.py`
  to construct the complete pure-`u_7` D0 source/divisor/Picard/factor-twist
  schema. It records 256 `Q(S,2)` candidates and 16 real/`Q_2` survivors while
  leaving odd bad-prime filtering and D1 explicitly unevaluated.
  `wl589` then uses `theory/aa_bb/wl589_mixed_d0_relative_2_descent.py`
  to construct the independent mixed `u_3+v_5+w_17` D0 schema. It verifies
  the exact mixed source and AA+BB lift, records the same candidate and
  real/`Q_2` survivor counts from independently derived arithmetic, and leaves
  all six odd bad-prime local images to a later explicitly selected D1 gate.
  `wl590` then uses `theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py`
  to compute the exact normalized `Q_5` factor-twist images for both frozen
  D0 schemas. It proves the pure image empty and the mixed image equal to
  `[5]`, deleting all 16 pure representatives and 12 of the 16 mixed
  representatives without processing another prime or entering D2.
  `wl591` then uses `theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py`
  to compute the exact normalized mixed `Q_7` image. It proves
  `I_{7,m}={[1]}`, deletes `5, 3045, 66045`, and retains `91205` with all
  source, pole, boundary, factor-zero, fixed-cover, and AA+BB lift checks.
  `wl592` then uses `theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py`
  to compute the exact normalized mixed `Q_17` image. It proves
  `I_{17,m}={[u]}`, excludes `91205=[17u]`, and retains the complete
  negative-valuation, denominator, factor-zero, fixed-cover, and AA+BB lift
  certificate without entering another prime or D2.

### `modular/` — Path B / mod p² 实证

| 脚本 | 用途 |
|------|------|
| `enumerate_mod_p2_classes.py` | (a, b) mod p² 类枚举 (wl078) |
| `enumerate_mod_p2_crt.py` | CRT 合并 mod p² (wl079) |
| `mod_p2_unused_analysis.py` | unused mod p² class 分析 (wl078) |
| `uniform_mod_p2_audit.py` | uniform mod p² audit (wl077-079) |
| `analyze_multi_n_mod_pattern.py` | multi-N mod pattern (wl079) |

### `utility/` — 工具

| 脚本 | 用途 |
|------|------|
| `extract_pdf_text.py` | PDF 文本抽取 (文献调研) |

### `archive/` — 历史归档

wl053 round-2 archive 之前的脚本. 不要新增. 见 `archive/README.md`.

---

## 路径约定

所有子目录脚本顶端用:
```python
ROOT = Path(__file__).parent.parent.parent  # → 项目 root
```
（顶层主入口仍用 `Path(__file__).parent.parent`.）

新增脚本时:
1. 选合适分类放进对应子目录
2. 顶部加一行 docstring 说明用途
3. 在本 README 对应 section 加一行索引
