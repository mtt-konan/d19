# 术语对照表（d19 项目专用）

这份文档只回答一件事：项目里那些数学/工程英文术语，对应中文叫什么、一句话是什么意思。

对照原则：

- 优先用中文叫法（左边给英文，右边给中文 + 一句话解释）
- 给每个术语标注**在 d19 项目里第一次正式出现的位置**，方便溯源
- 不写完整数学定义，只够"日常对话用"

如果讨论时双方默契用同一套词，下面这张表是基准。

---

## 1. 椭圆曲线与有理点

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| elliptic curve `E` | **椭圆曲线** | 形如 $y^2 = $ 三次多项式的光滑曲线；d19 里专指 `y² = x(x + A²)(x + B²)` | [MATH.md](MATH.md) §3 |
| `E(\mathbb{Q})` | **E 的有理点群** | 椭圆曲线上坐标都是有理数的点构成的群 | [MATH.md](MATH.md) §3 |
| rank | **秩** / "独立解个数" | $E(\mathbb{Q})$ 里独立有理点的个数（不算挠点） | [wl 033](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| generator | **基础解** | 由它能生成 $E(\mathbb{Q})$ 中所有有理点的几个特殊点 | [wl 033](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| torsion / `E[n](\mathbb{Q})` | **挠点** / "n-挠点" | 满足 $nP = O$ 的有理点；d19 case 始终 $E[2](\mathbb{Q}) = (\mathbb{Z}/2)^2$ | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| height (of a point) | **高度** | 衡量有理点"复杂程度"的数；坐标分母分子越大越高 | [wl 031](work-logs/028-proof-status-ec-foundation-consolidated.md) |

## 2. 局部 vs 全局，沙群与塞尔默群

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| local solubility | **局部可解** | 在某个 $p$ 进数 $\mathbb{Q}_p$ 或实数 $\mathbb{R}$ 上有点 | [wl 037](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| global solubility | **全局可解** | 在有理数 $\mathbb{Q}$ 上有点 | [wl 037](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Hasse principle | **哈塞原则** | "局部都可解 ⟹ 全局可解"——很多场景错 | [wl 037](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Sha / Ш / `Sha(E)` | **沙群** | 局部都可解但全局无解的"覆盖"集合；衡量 Hasse 原则失败程度 | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Sha[2] / `Sha(E)[2]` | **沙群的 2 部分** | 沙群里阶数 ≤ 2 的元素 | [wl 036](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Selmer group / Sel(E, n) | **塞尔默群** | 局部上每个素数都没破绽的 n-覆盖集；包含沙群 | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| 2-cover / 2-descent | **两层覆盖 / 二层下降** | 通过"开根号"得到的辅助曲线，用来约束 $E(\mathbb{Q})$ | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| 2-isogeny | **2-同源映射** | 椭圆曲线之间一个 2-to-1 的特殊映射 | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| 2-isogeny cover | **2-同源覆盖** | ell2cover 输出的那些四次方程曲线 | [wl 036](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| sha2_lower | **沙下界** | PARI 算出的 $\dim_{\mathbb{F}_2} \Sha[2]$ 的最小可能值 | [wl 036](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Cassels-Tate pairing | **CT 配对** | 一个能从一对覆盖算出 0 或 1/2 的工具，用来证沙群非平凡 | [PROJECT_STATUS](PROJECT_STATUS.md) §9.9 |

## 3. PARI/GP 工具

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| `ellrank(E, effort)` | **秩计算** | PARI 算 $\text{rank}(E)$ 的内置函数；返回 `[rank_lo, rank_hi, sha2_lower, gens]` | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| effort | **力度** | PARI 算法的努力等级（1 浅，3 深） | [wl 033](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| `ell2cover(E)` | **两层覆盖工具** | PARI 返回所有 2-同源覆盖的四次方程 | [wl 036](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| `hyperellratpoints(g, h)` | **曲线找点** | PARI 在 $y^2 = g(x)$ 上找 $|x|, |y| \leq h$ 范围内的有理点 | [wl 036](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| `compute_rank` | **秩工具封装** | 项目里包装 `ellrank` 的 4 元组接口 | [wl 035](work-logs/028-proof-status-ec-foundation-consolidated.md) |

## 4. d19 项目特有概念

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| concordant form | **协同型** / "共轭对" | $\exists N: N^2+A^2, N^2+B^2$ 同为平方的 $(A, B)$ 对 | [MATH.md](MATH.md) §2 |
| chain / 4-chain | **链 / 4-链** | 4 个边距离都是有理数的四顶点配置 | [PROJECT_STATUS](PROJECT_STATUS.md) |
| hard_case | **疑难对** | 暂时既没找到解也没证无解的 $(A, B)$ 对 | [wl 030](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| survivor | **幸存疑难对** | 通过前置核心筛、仍需后续完整审计的 $(A, B)$ 对 | [wl 069](work-logs/053-partner-graph-fast-core-consolidated.md) |
| no_solution | **已证无解** | 用 cheap sieve（mod 1680, modular obstruction）证完全没有 N 满足条件的 (A, B) | [wl 030](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| safe_sieve | **安全前筛** | 不会误杀真解的快速过滤（mod 8, mod 1680 等） | [CHAIN_FAST_SAFE_FILTERS](archive/CHAIN_FAST_SAFE_FILTERS.md) |
| max_hyp | **最大斜边** | 扫描时给 $\sqrt{A^2+B^2}$ 设的上界 | [wl 030](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| chain-fast | **基线搜索器** | 当前最可信的 4 顶点搜索实现 | [PROJECT_STATUS](PROJECT_STATUS.md) |
| package-`x` | **旧 x 坐标打包** | 旧 AA+BB route 里把三个 package 的 x 坐标当成桥；已被 `wl469` / `wl470` 放弃 | [wl 469](work-logs/469-aa-bb-h2-coordinate-equivalence-audit.md) |
| `S~` | **伪 Selmer 容器** | AA+BB common-source 的旧上界容器；不是 theorem-level `Sel_2(E_L/Q)` | [wl 465](work-logs/465-aa-bb-pseudo-selmer-container-audit.md) |
| complete `d`-coordinate | **完整 d 坐标** | 完整 2-descent 使用的三元 squareclass 坐标 `(d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q)` | [wl 471](work-logs/471-aa-bb-complete-d-container-definition.md) |
| `C_d` | **d 覆盖曲线** | 给定完整 `d` 坐标后的二层覆盖对象；当前主线检查它的 local/global solubility | [wl 471](work-logs/471-aa-bb-complete-d-container-definition.md) |
| `M_tail` | **尾部矩阵** | solved local rows 后剩下的参数依赖 `F2` character matrix；尚未证明 uniform full rank | [wl 480](work-logs/480-aa-bb-d4-uniform-matrix-rank-bound-audit.md) |
| `u_3` | **u3 候选** | `AA, A=3, B=1` 样本中的 `d=(3,3,1)` tail candidate；有 ambient 全局点但不是 AA+BB admissible 点 | [wl 482](work-logs/482-aa-bb-m-tail-kernel-classification-gate.md) |
| `v_5` | **v5 refreshed support** | `wl494` bounded refresh 里的 active support family；`wl495` 中四个 route 为 global but not admissible，两个 deferred，`wl496` 把这两个 deferred ledgers 关闭为 globally not soluble；`wl528` 只对其中 `L=1,T=5,d=(5,1,5)` 做单个函数域 prototype | [wl 496](work-logs/archive/496-resolve-wl495-deferred-v5-ambient-c-d-global-solubility-ledgers.md) |
| `u_5` | **u5 shell support** | `wl499` finite shell `max(A,B)=5` 里出现；`wl500` 关闭 shell-5 `L=5,T=8,d=(5,5,1)` 为 ambient globally not soluble，`wl517` 把 shell-10 `L=10,T=11,d=(5,5,1)` 路由为 globally soluble but not AA+BB-admissible，`wl519` 又把 shared shell-10 `L=10,T=19,d=(5,5,1)` 解决为 globally soluble but not AA+BB-admissible；`wl521` 把这段历史保留为 theorem-candidate pattern，但明确不是 family theorem，并只选择后续 finite shell 11 | [wl 521](work-logs/archive/521-support-family-synthesis-after-wl519.md) |
| admissibility filter | **可准入过滤器** | 把 ambient `C_d` 全局点筛成 AA+BB common-source admissible / not admissible / missing data 的下一窄门 | [NEXT_RESEARCH_GATE](NEXT_RESEARCH_GATE.md) |
| common-source square obstruction | **同源闭合平方障碍** | `wl491` 里的点级条件：centered-even pullback 得到同一个 `N,M` 后，AA/BB 另一侧 `(N²+leg²)(M²+leg²)` 不是有理平方，则这个 ambient `C_d` 点不能进入 AA+BB admissible ledger；`wl523` 确认这不是 uniform cover-family theorem，`wl524` 只选择稍后尝试 uniform lemma，`wl525` 说明当前 finite taxonomy 不能直接推广成 uniform theorem | [wl 523](work-logs/523-try-common-source-square-obstruction-lemma-candidate.md) |
| post-wl523 route choice | **wl523 后路线选择** | `wl524` 比较 uniform cover-family squareclass lemma、finite shell 11 `M_tail` diagnostics、proof-level local/Hilbert row work、final candidate selection 后，只选择稍后尝试 uniform cover-family squareclass lemma；它不进入证明、不执行 shell 11、不选择 final candidate | [wl 524](work-logs/524-post-wl523-route-choice-audit.md) |
| uniform cover-family squareclass attempt | **一致覆盖族平方类尝试** | `wl525` 进入 `wl524` 选中的 proof attempt，但发现 `wl523`/`wl524` 只有点级 obstruction 与有限 taxonomy count，没有 cover-family function-field squareclass certificate；所以当前不能证明 uniform cover-family lemma，也不 refute 未来可能的 lemma | [wl 525](work-logs/525-attempt-uniform-cover-family-squareclass-obstruction-lemma.md) |
| post-wl525 route choice | **wl525 后路线选择** | `wl526` 比较 function-field proof-data scoping、finite shell / `M_tail` diagnostics、theorem-level complete-Selmer local/Hilbert row obligation、abandon obstruction line 后，只选择稍后收集最小 function-field squareclass proof data；它不建模型、不证明 uniform lemma、不执行 shell 11、不选择新 candidate | [wl 526](work-logs/526-post-wl525-route-choice-audit.md) |
| function-field proof-data scope | **函数域证明数据盘点** | `wl527` 进入 `wl526` 选中的 scoping gate，盘点 15 个 named not-admissible cover families 的 model/map/`N,M`/opposite-side squareclass target/exceptional checklist；结论是 0 个 ready，缺 `uniform_function_field_model_maps_and_squareclass_certificate`，不证明 uniform lemma | [wl 527](work-logs/527-function-field-squareclass-proof-data-scope.md) |
| function-field prototype | **函数域原型** | `wl528` 对单个 `support=v_5|L=1|T=5|d=(5,1,5)` family 建 chart/map/`N,M`，并用一个 checked specialization 证明 opposite product 在该 prototype 函数域里非平方；不是 divisor parity、specialization-survival 或 uniform cover-family theorem | [wl 528](work-logs/528-v5-l1-t5-function-field-prototype.md) |
| square-specialization locus | **平方特化轨迹** | `wl529` 对同一个 `v_5,L=1,T=5,d=(5,1,5)` prototype 构造 `U^2=t^4+78t^2+7921`，通过到椭圆商曲线的二次映射分类有理点，并排除 positivity domain 内的平方特化；只关闭这一 family，不是一致族定理 | [wl 529](work-logs/529-v5-l1-t5-square-locus.md) |
| candidate queue | **候选队列** | 从既有 `M_tail` diagnostics 排序下一批待审候选；`wl493` 的既有队列只有已处理的 `u_3` 降级项，没有 active 新候选；只是路由/优先级，不是新候选证明 | [wl 493](work-logs/archive/493-aa-bb-candidate-queue-from-existing-m-tail-diagnostics.md) |
| shell-6 diagnostic | **第 6 壳诊断** | `wl502` 按 `wl501` gate 执行 `max(A,B)=6` primitive shell；当前 row ledger 下 8 个样本全 rank 满，`active_new_kernel_supports=[]` 且 `excluded_duplicate_or_processed_supports=[]`；不是 uniform full-rank theorem | [wl 502](work-logs/archive/502-execute-next-finite-m-tail-shell-from-wl498-plan.md) |
| post-empty-shell route choice | **空壳后路线选择** | `wl503` 在 shell-6 空队列后只选择下一窄门为稍后执行 `max(A,B)=7` finite `M_tail` shell；它不执行 shell 7、不测试 ambient `C_d`、不应用 `wl491`、不证明 uniform `M_tail` full rank | [wl 503](work-logs/archive/503-post-wl502-empty-shell-route-choice-audit.md) |
| shell-7 diagnostic | **第 7 壳诊断** | `wl504` 按 `wl503` gate 执行 `max(A,B)=7` primitive shell；产生 12 个 active `M_tail` diagnostic supports 和 2 个 pure `u_3` processed exclusions；active outputs 仍需先过 ambient `C_d` solubility，不是 final candidates | [wl 504](work-logs/archive/504-execute-next-finite-m-tail-shell-from-wl498-plan.md) |
| shell-7 deferred ledger resolution | **第 7 壳 deferred 账本解决** | `wl506` 只解决 `wl505` 留下的 4 个 deferred ambient `C_d` ledgers：两个 `w_5` 为 globally not soluble，两个 `u_7+w_37` 为 globally soluble but not AA+BB-admissible；不是 final theorem | [wl 506](work-logs/archive/506-resolve-shell7-deferred-ambient-c-d-global-solubility-ledgers.md) |
| post-shell-7 route choice | **第 7 壳后路线选择** | `wl507` 在 shell-7 active/deferred ledgers 全部处置后只选择下一窄门为稍后执行 `max(A,B)=8` finite `M_tail` shell；它不执行 shell 8、不测试 ambient `C_d`、不应用 `wl491` | [wl 507](work-logs/archive/507-post-wl506-route-choice-audit.md) |
| shell-8 diagnostic | **第 8 壳诊断** | `wl508` 按 `wl507` gate 执行 `max(A,B)=8` primitive shell；14 个样本 full rank，2 个 pure `u_3` kernel outputs 被 processed guard 排除，active queue 为空；不是 uniform `M_tail` theorem | [wl 508](work-logs/archive/508-execute-next-finite-m-tail-shell-from-wl498-plan.md) |
| post-shell-8 route choice | **第 8 壳后路线选择** | `wl509` 在 shell-8 active queue 为空且 pure `u_3` outputs 已 processed 后只选择下一窄门为稍后执行 `max(A,B)=9` finite `M_tail` shell；它不执行 shell 9、不测试 ambient `C_d`、不应用 `wl491` | [wl 509](work-logs/archive/509-post-wl508-empty-shell-route-choice-audit.md) |
| shell-9 diagnostic | **第 9 壳诊断** | `wl510` 按 `wl509` gate 执行 `max(A,B)=9` primitive shell；24 个样本中 16 个 full rank、8 个有 kernel，产生 8 个 active `M_tail` diagnostic supports；这些还不是 ambient `C_d` 点、AA+BB admissible 点或 final candidates | [wl 510](work-logs/archive/510-execute-next-finite-m-tail-shell-from-wl498-plan.md) |
| shell-9 ambient route | **第 9 壳 ambient 路由** | `wl511` 将 8 个 active shell-9 supports 先过 ambient `C_d` solubility：4 个 exact global points 经 `wl491` 为 not-admissible，4 个 deferred；不是 shell 10、final candidate 或 Selmer theorem | [wl 511](work-logs/archive/511-route-active-shell9-m-tail-supports-through-ambient-c-d-solubility-then-wl491-filter.md) |
| shell-9 deferred ledger resolution | **第 9 壳 deferred 账本解决** | `wl512` 只分类 `wl511` 留下的 4 个 deferred shell-9 ambient `C_d` ledgers：两个 `v_13` refuted，两个 `u_7` 继续 deferred；不是 shell 10 或 final theorem | [wl 512](work-logs/archive/512-resolve-shell9-deferred-ambient-c-d-global-solubility-ledgers.md) |
| post-wl512 route choice | **wl512 后路线选择** | `wl513` 在两个 shell-9 `u_7` ledgers 仍 deferred 后只选择下一窄门为 targeted resolution of their shared `L=7,T=16,d=(7,7,1)` ambient `C_d` cover；它不进入该门、不执行 shell 10、不应用 `wl491` | [wl 513](work-logs/archive/513-post-wl512-route-choice-audit.md) |
| shell-9 u_7 cover resolution | **第 9 壳 u_7 cover 解决** | `wl514` 只进入 `wl513` 选定的 shared `L=7,T=16,d=(7,7,1)` cover，用 mod-17 Mordell-Weil-sieve no-lift certificate 关闭为 globally not soluble；不应用 `wl491`、不执行 shell 10 | [wl 514](work-logs/archive/514-resolve-remaining-shell9-u7-ambient-c-d-global-solubility-ledger.md) |
| post-wl514 route choice | **wl514 后路线选择** | `wl515` 在所有 shell-9 deferred ambient `C_d` ledgers 已分类后，只选择下一窄门为稍后按 `wl498` plan 执行 `max(A,B)=10` finite `M_tail` shell；它不执行 shell 10、不重开 closed shell-9 ledgers | [wl 515](work-logs/archive/515-post-wl514-route-choice-audit.md) |
| duplicate-support guard | **重复 support 保护** | `wl498` 定义的去重规则；后续 shell 用 `source_quotient,A,B,L,T,candidate_support` 识别已处置 route key，并加上 shell-5 `u_5`、shell-7 closed ledgers 与 shell-8 processed `u_3` exclusions，防止重开 `u_3`、bounded `v_5`、shell-5 `u_5`、shell-7 entries 或 shell-8 processed entries | [wl 510](work-logs/archive/510-execute-next-finite-m-tail-shell-from-wl498-plan.md) |

## 5. 模式狩猎 / 统计

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| chi² test | **卡方检验** | 看两组分布差异是否显著 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| feature / fingerprint | **特征 / 特征向量** | 用一组数刻画 (A, B) 的属性（squarefree、max_exp 等） | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| stratify | **分层** | 按某个特征把样本切成子组分别看 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| outlier | **异常项** | 偏离一般模式的特殊 case | [wl 039](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| n_covers | **覆盖数** | `ell2cover(E)` 返回的覆盖个数 | [wl 039](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| n_without_pt | **无点覆盖数** | 没找到有理点的覆盖个数（h=10⁴ 或 10⁵ 内） | [wl 039](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| max_exp(n) | **最大素幂次** | n 的素因子分解里出现的最大指数 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| squarefree | **无平方因子** | 素因子分解里所有指数都是 1 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |

## 6. 重型工具（长期方向）

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| Heegner point | **复乘点** / "Heegner 点" | 用复数二次域构造的特殊高度有理点，对秩=1 case 特效 | [OPEN_DIRECTIONS](OPEN_DIRECTIONS.md) |
| Mordell-Weil sieve | **MW 高度筛** | 用已知基础解逆向筛掉覆盖上不存在的点的位置 | [wl 039](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Chabauty method | **Chabauty 方法** | 用 p 进解析方法限制曲线上有理点 | [OPEN_DIRECTIONS](OPEN_DIRECTIONS.md) |
| Brauer-Manin obstruction | **BM 障碍** | 比沙群更细的"局部-全局失败"度量 | [OPEN_DIRECTIONS](OPEN_DIRECTIONS.md) |
| K3 surface | **K3 曲面** | 高维代数几何对象；4-chain 问题在某种意义上是 K3 上的有理点问题 | [archive/THEORY_DIRECTIONS_ADVANCED](archive/THEORY_DIRECTIONS_ADVANCED.md) |
| finite descent | **有限下降** | Peschmann §7 风格的"枚举有限多个候选" 方法 | [wl 037](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| Stoll sieve | **Stoll 筛** | 类似 MW 高度筛但更精细的高度约束方法 | [PROJECT_STATUS](PROJECT_STATUS.md) §9.9 |

## 7. 工程实现术语

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| worker | **单任务子进程** | 一次只处理一个 (A, B) 的脚本 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| driver / batch_*_v2 | **批量调度器** | 把任务分发给多个 worker，处理超时和续跑 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| timeout-safe | **超时安全** | 单个任务卡住不影响整体扫描 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| subprocess isolation | **子进程隔离** | 用独立子进程跑 PARI，避免 cypari2 内存泄漏污染主进程 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| fast-core | **快速核心筛** | `proof_status` 的两阶段快路径：先全量跑低成本严格筛，再只审计幸存疑难对 | [wl 069](work-logs/053-partner-graph-fast-core-consolidated.md) |
| JSONL | **JSON 行格式** | 每行一个 JSON 对象的纯文本格式，便于流式 append 和 grep | [wl 030](work-logs/028-proof-status-ec-foundation-consolidated.md) |
| resume / resumable | **断点续跑** | 中断后从上次进度继续，不重复已完成的任务 | [wl 038](work-logs/028-proof-status-ec-foundation-consolidated.md) |

---

## 用法说明

- 写 worklog 或 commit message 时，**第一次出现英文术语**带中文括号；后续可直接用中文
- 例如：第一次写 `Sha[2]（沙群的 2 部分）`，后续直接写"沙[2]"
- PARI 函数名、git 命令等代码符号保留英文（换中文反而看不懂）
- 见到不熟的术语 → 查这张表 → 如果表里没，补一行
