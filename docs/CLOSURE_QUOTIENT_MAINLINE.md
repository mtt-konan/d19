# Closure Quotient Mainline

这份文档只保留当前主线。详细逐轮材料已经进 worklog；这里负责回答：

- closure quotient 到底证明了什么；
- 哪些数字只是统计，不是证明进展；
- 下一步如果继续走 rank-zero Selmer，缺口在哪里。

入口：

- [PROJECT_STATUS.md](./PROJECT_STATUS.md)
- [OPEN_DIRECTIONS.md](./OPEN_DIRECTIONS.md)
- [wl294 closure quotient foundation](./work-logs/294-closure-quotient-foundation-consolidated.md)
- [wl386 rank-zero Selmer package](./work-logs/386-rank-zero-selmer-package-consolidated.md)

## 1. 核心对象

旧 concordant 曲线只问：

```text
N^2 + A^2 = square
N^2 + B^2 = square
```

它会忘掉闭合腿。内部闭合时取

```text
M = A + B - N
```

全平面 GEN-CLOSURE 还需要同时考虑差关系；本质上常数只剩

```text
c_plus  = A + B
c_minus = |A - B|
M = c - N
```

对固定 `c`，四个平方条件是：

```text
NA = N^2 + A^2
NB = N^2 + B^2
MA = M^2 + A^2
MB = M^2 + B^2
```

取两两乘积得到四条 genus-one 商曲线：

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

完整闭合点必须落在这四条商曲线上。任何一条商曲线能严格排除非平凡仿射点，就能排除原闭合点。

## 2. 已经严格可用的证书

当前唯一干净证书是：

```text
AA/BB rank = 0
  -> enumerate torsion
  -> pull back to quartic
  -> only midpoint points
  -> Yang Ji midpoint theorem excludes them
```

`AA/BB` 有中点对称。令

```text
t = 2N - c
z = 4y
```

则偶四次为

```text
z^2 = t^4 + p t^2 + q
p = 8L^2 - 2c^2
q = (c^2 + 4L^2)^2
```

其中 `L=A` 对应 `AA`，`L=B` 对应 `BB`。对应椭圆曲线可取：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

仿射反向回拉：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = (c+t)/2
```

所以只要 `rank_lower=rank_upper=0` 被认证，`E(Q)` 就只剩 torsion；枚举 `elltors(E)` 并回拉即可列尽原四次曲线的仿射有理点。`O` 不给仿射点，`X=-p` 对应四次曲线无穷远点。

当前统计口径：

```text
rank-zero certificate rows = 275
strictly excluded distinct (A,B) candidates = 220
```

这 275 行都只回拉到中点 `N=M=c/2`，没有 full-closed square point。注意：这是严格有限证书，但只覆盖已经认证 rank-zero 的行；它不是全局 Harborth 证明。

## 3. AB/BA 的结论

`AB/BA` 不是 rank-zero 击杀器。它们有结构性万能点，例如在 `c=A+B` 时取

```text
N = A
M = B
y = 2AB
```

于是

```text
(N^2+A^2)(M^2+B^2) = 2A^2 * 2B^2 = (2AB)^2
```

这解释了为什么两批样本里 `AB/BA rank 0 = 0`。以后 `AB/BA` 可以作为结构校验或生成元来源，不要再当 rank-zero 刀。

## 4. 射线账本

商曲线齐次。若 `(A,B,N,y)` 是点，则

```text
(A,B,N,y) -> (kA,kB,kN,k^2 y)
```

保持方程同形。因此证书天然按比例

```text
lambda = A/B
```

生效，而不是只按单个整数 pair 生效。正确账本应该按本原射线 `(a:b)` 建键，记录：

```text
c_plus_cert
c_minus_cert
AA_or_BB
rank_certificate
torsion_pullback_audit
midpoint_exclusion_reference
ray_dead = c_plus_cert and c_minus_cert
```

`c_minus=|A-B|` 是完整射线证书的必要另一半；`lambda=1` 时 `c_minus=0` 退化，需单独走中线定理。

## 5. Selmer Family Route

有限证书只能杀一批 ratio。若想变成证明线，需要把 `AA/BB` 的 rank-zero 现象提升为 family theorem：

```text
local image theorems
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank(E_lambda)=0
```

最近 worklog 的 package 段落是在补这条链的材料。它们的意义是“证明段落更可审阅”，不是“命题已经更接近完成”。真正跨步只看一件事：

```text
能否推出 global Selmer dimension bound
```

当前压缩状态：

- odd-prime formal-lift 段落已经有多份 reviewable package；
- dyadic 分支已经把点级 2-primary compatibility 压到 `(1,1,1)`；
- 剩余核心不是继续采样，而是把点级 compatibility lift 到 Selmer 层；
- 没有 Selmer-layer lift，就没有 rank-zero family theorem。

最近的完整 `d`-坐标主线已经放弃旧 package-`x` 的 `S~` 桥，改走
`C_d` / `M_tail`。`wl489` 只处理一个点级问题：`AA, A=3, B=1` 的
`d=(3,3,1)` 全局点可回拉到 `AA` 四次商上的 `N=4, M=0`，但同一
common source 在 `BB` 侧给出 `(N^2+B^2)(M^2+B^2)=17`，不是平方。
所以这个点不是 AA+BB common-source 闭合点。`wl490` 只把它从当前
obstruction / admissible ledgers 移到“ambient globally soluble but not
AA+BB-admissible”诊断账本。`wl491` 定义了 reusable
ambient-`C_d`-to-AA+BB admissibility filter：任何 ambient global `C_d`
点进入 admissible ledger 前，必须先通过 centered-even pullback、AA/BB
common-source square products、以及正性/非退化检查；已知 `u_3` 样本按该
filter 回归为 `not_admissible`。这仍不是 Selmer 上界、rank-zero 结论或
family exclusion。`wl492` 只做下一步路由：当前已知 ambient 点没有未过滤
ledger 可继续用，下一窄门应从既有 `M_tail` diagnostics 建候选队列，并把
`u_3` 标为已处理 / not_admissible，而不是直接跳到无序的新 candidate。
`wl493` 建出的既有队列没有 active unprocessed candidate：唯一的 `wl481`
kernel support 是已处理的 `u_3`，只保留为 processed/deprioritized 账本项。
`wl494` 用有界 primitive AA/BB 样本网格刷新 `M_tail` diagnostics；这只产生
诊断层的新 active `v_5` support entries，并保留 `u_3` 的 processed /
not-admissible 状态。它没有证明新的 local row、ambient `C_d` solubility、
AA+BB admissibility、Selmer 上界或 rank-zero 结论。下一步若继续这条线，
必须先把这些 refreshed supports 送过 ambient `C_d` solubility gate，再用
`wl491` filter 路由。`wl495` 执行这一步但不越界：六个 refreshed `v_5`
entries 全部保留；四个有 exact ambient global `C_d` point，随后被 `wl491`
filter 路由为 `not_admissible`；剩下两个只进入 ambient `C_d` solubility
deferred ledger。没有新的 admissible point、final obstruction candidate、
Selmer 上界或 rank-zero 结论。`wl496` 只解决这两个 deferred ledgers：
它们共享 `L=4,T=5,d=(5,1,5)`，通过 targeted single-cover Mordell-Weil
torsion-lift certificate 被记录为 ambient globally not soluble。因为没有
ambient global `C_d` point，`wl491` filter 不应用；这仍不是 final
obstruction candidate、Selmer 上界或 family rank-zero theorem。`wl497`
只做后续路线选择：在 `u_3` 和有界 refreshed `v_5` supports 都已处置后，选择
`structure_next_M_tail_diagnostic_extension` 作为下一窄门，并停止在执行之前。
这不是新网格刷新、不是新 local row、不是新的 `C_d` solubility 测试，也不是
`wl498`。`wl498` 若存在，则它只把下一批 `M_tail` diagnostic extension 结构化：
允许的轴是 finite primitive shell、`side in {AA,BB}`、`gcd(A,B)=1`、
`max(A,B)>4`；同时记录 `u_3` family exclusion、bounded `v_5` route-key
exclusions、duplicate-support guard、未来输出 schema 和新 support 的后续 routing
contract。它没有刷新新网格、没有计算新 support、没有测试新的 `C_d` solubility，
也没有进入 `wl499`。`wl499` 执行这个 plan 的第一个 finite primitive shell：
`max(A,B)=5`、`side in {AA,BB}`、`gcd(A,B)=1`。这一步只得到两个新的
`M_tail` diagnostic supports：
`AA_A5_B3_u_5_m_tail_shell5_candidate` 和
`BB_A3_B5_u_5_m_tail_shell5_candidate`。它没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有选 final obstruction candidate、没有证明
Selmer 上界，也没有进入 `wl500`。`wl500` 只路由这两个 active `u_5`
entries：它们共享 `L=5,T=8,d=(5,5,1)` complete `C_d` cover，并通过
targeted Mordell-Weil torsion-lift certificate 记录为 ambient globally not
soluble。因为没有 ambient global `C_d` point，`wl491` filter 不应用；这仍不是
admissible point、final obstruction candidate、Selmer 上界或 family
rank-zero theorem，也没有进入 `wl501`。`wl501` 只做 post-`wl500` route choice：
在 shell-5 `u_5` ledgers 已处置后，选择下一窄门为
`execute_next_finite_M_tail_shell_from_wl498_plan`，稍后应执行既有 `wl498` plan
的下一个 finite primitive shell `max(A,B)=6`。`wl501` 没有刷新或执行新
shell/grid、没有测试新的 `C_d` solubility、没有应用 `wl491`，也没有进入
`wl502`。`wl502` 执行这个 shell-6 `M_tail` diagnostic extension，但只得到空
queue：8 个 primitive AA/BB 样本全 rank 满，
`active_new_kernel_supports=[]` 且
`excluded_duplicate_or_processed_supports=[]`。这不是 uniform `M_tail`
full-rank theorem，也没有进入 ambient `C_d` solubility、`wl491` filter、final
candidate selection 或 `wl503`。`wl503` 只做 post-empty-shell route choice：
确认 shell-6 空队列不是 ambient route 也不是 uniform theorem，并选择下一窄门为
稍后按既有 `wl498` plan 执行 shell `max(A,B)=7`。它没有执行 shell 7、没有证明
local row、没有测试新的 `C_d` solubility，也没有进入任何 Selmer/rank theorem
claim。`wl504` 执行这个 shell-7 `M_tail` diagnostic extension，得到 12 个
active diagnostic supports 和 2 个 pure `u_3` processed exclusions；这些 active
outputs 仍不是 ambient global `C_d` points、AA+BB admissible points 或 final
obstruction candidates，下一窄门才是 ambient `C_d` solubility route。`wl505`
执行该 route：8 个 shell-7 entries 有 exact ambient points 但经 `wl491` 为
not AA+BB-admissible，4 个 entries 仍 deferred。`wl506` 只解决这 4 个
deferred ambient ledgers：两个 `w_5` entries 的 `L=4,T=11,d=(1,5,5)` cover
为 ambient globally not soluble，两个 `u_7+w_37` entries 的
`L=7,T=10,d=(7,259,37)` cover 为 globally soluble 但仍 not AA+BB-admissible。
`wl507` 只做 post-`wl506` route choice，选择稍后按既有 `wl498` plan 执行
shell `max(A,B)=8`，但没有执行 shell 8、没有测试新的 `C_d` solubility、没有
应用 `wl491`。这没有产生 final obstruction candidate、local row、Selmer 上界或
family rank-zero theorem。`wl508` 执行这个 shell-8 `M_tail` diagnostic
extension：16 个 primitive AA/BB 样本中 14 个 full rank，2 个 pure `u_3`
kernel outputs 被归入 duplicate / processed queue，active queue 为空。它仍然
没有测试新的 `C_d` solubility、没有应用 `wl491`、没有产生 final obstruction
candidate、local row、Selmer 上界或 family rank-zero theorem，也不是 uniform
`M_tail` full-rank theorem。`wl509` 只做 post-`wl508` route choice：确认
shell-8 没有 active support 可路由，两个 pure `u_3` outputs 已作为 processed
exclusions 关闭，并选择稍后按既有 `wl498` plan 执行 shell `max(A,B)=9`。它没有
执行 shell 9、没有测试新的 `C_d` solubility、没有应用 `wl491`、没有产生 final
obstruction candidate、local row、Selmer 上界或 family rank-zero theorem。
`wl510` 执行这个 shell-9 `M_tail` diagnostic extension：24 个 primitive
AA/BB samples 中 16 个 full rank、8 个有 kernel，产生 8 个 active diagnostic
supports，没有 duplicate / processed output。它没有测试新的 `C_d` solubility、
没有应用 `wl491`、没有产生 final obstruction candidate、local row、Selmer
上界或 family rank-zero theorem；这些 active outputs 下一步仍必须先过
ambient `C_d` solubility route。`wl511` 执行该 route：4 个 shell-9 entries 有
exact integral ambient points 但经 `wl491` 为 not AA+BB-admissible，4 个 entries
仍 deferred。它没有执行 shell 10、没有证明 deferred covers globally not
soluble、没有产生 final obstruction candidate、local row、Selmer 上界或 family
rank-zero theorem。`wl512` 只分类这 4 个 deferred shell-9 ledgers：两个
`v_13` entries 的共同 `L=4,T=13,d=(13,1,13)` cover 被 targeted
Mordell-Weil torsion-lift certificate 记录为 ambient globally not soluble；两个
`u_7` entries 的共同 `L=7,T=16,d=(7,7,1)` cover 仍 deferred，因为这里没有
exact ambient point 或 exhaustive no-lift certificate。它没有执行 shell 10、
没有应用 `wl491`、没有选择 final obstruction candidate、没有产生 local row、
Selmer 上界或 family rank-zero theorem。`wl513` 只做 post-`wl512` route
choice：选择下一窄门为 targeted resolution of the remaining shared shell-9
`u_7` ambient `C_d` cover `L=7,T=16,d=(7,7,1)`，但没有进入该门、没有执行
shell 10、没有重开 closed shell-9 ledgers、没有应用 `wl491`、没有选择 final
obstruction candidate、没有产生 local row、Selmer 上界或 family rank-zero
theorem。`wl514` 只进入这个 selected gate：用 mod-17 Mordell-Weil-sieve
no-lift certificate 把该 shared shell-9 `u_7` cover 关闭为 ambient globally
not soluble。`wl491` 没有应用；它也没有执行 shell 10、没有做 post-route
choice、没有产生 final obstruction candidate、Selmer 上界或 family rank-zero
theorem。`wl515` 只做 post-`wl514` route choice：所有 shell-9 deferred
ambient `C_d` ledgers 已分类，下一窄门是按既有 `wl498` plan 稍后执行
finite primitive shell `max(A,B)=10`。`wl515` 没有执行 shell 10、没有重开
closed shell-9 ledgers、没有应用 `wl491`、没有选择 final candidate，也没有产生
Selmer 上界或 family rank-zero theorem。`wl516` 执行这个 shell-10 `M_tail`
diagnostic extension：16 个 primitive AA/BB samples 中 6 个 full rank、10 个
有 kernel，产生 10 个 active diagnostic supports，没有 duplicate / processed
output。它没有测试新的 `C_d` solubility、没有应用 `wl491`、没有产生 final
obstruction candidate、local row、Selmer 上界或 family rank-zero theorem；这些
active outputs 下一步仍必须先过 ambient `C_d` solubility route。`wl517` 已经
只把这 10 个 shell-10 active supports 路由过 ambient `C_d` solubility：8 个
有 exact integral ambient points，并经 `wl491` 归入 globally soluble but not
AA+BB-admissible；2 个仍是 deferred ambient-solubility ledgers。它没有执行
shell 11、没有选择 final candidate、没有证明 local row、Selmer 上界或 family
rank-zero theorem。`wl518` 已经把 `wl491`-`wl517` ledgers 按 support family /
cover family 聚合：唯一 genuinely deferred cover family 是 shared shell-10
`u_5` `L=10,T=19,d=(5,5,1)`，并选择 targeted resolution of that shared cover
作为下一窄门但不进入。这个 `u_5` pattern 不是 theorem，也不是 Selmer progress。
`wl519` 只进入这个 selected gate：给出 exact rational ambient `C_d` point，把
shared shell-10 `u_5` `L=10,T=19,d=(5,5,1)` cover 解决为 globally soluble；
随后对两个 mirror entries 应用 `wl491`，两者都进入 globally soluble but not
AA+BB-admissible ledgers。它没有做 post-`wl519` route choice、没有执行 shell
11、没有选择 final candidate、没有证明 Selmer 上界或 family rank-zero theorem。
`wl520` 只做这个 post-`wl519` route choice：在该 shared cover 已分类且没有
AA+BB-admissible / final candidate 后，选择下一窄门为
`synthesize_support_and_cover_families_after_wl519`。它没有进入 synthesis、没有
执行 shell 11、没有转 proof-level local row、没有选择 final candidate，也没有
证明 Selmer 上界或 family rank-zero theorem。
`wl521` 进入这个 selected synthesis：用 `wl520` 作 immediate input，把
`wl491`-`wl519` ledgers 按 support family / cover family 重新聚合；结果没有
genuinely deferred cover family、没有 AA+BB-admissible cover family，只保留
`u_5` 的 `d=(5,5,1)` mixed refuted / not-admissible 历史作为
theorem-candidate pattern。这个 pattern 不是 theorem，也没有隔离 named
proof gap；`wl521` 只选择稍后按既有 `wl498` plan 执行 finite shell
`max(A,B)=11`，但不执行 shell 11，不计算 supports，不测试 ambient `C_d`，不应用
`wl491`，不证明 Selmer 上界或 family rank-zero theorem。`wl522` 只做
support/cover taxonomy checkpoint：用 `wl521` 作 latest state，把 `wl491`-`wl521`
ledgers 按 support family、cover family、classification 和 failure mode 压缩。
结果没有 deferred 或 AA+BB-admissible cover family；5 个 cover families 是
ambient globally not soluble，15 个 cover families 是 globally soluble but not
AA+BB-admissible，2 个是 processed / duplicate。它隔离了唯一下一
theorem-candidate：
`common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families`，
但没有进入证明、没有执行 shell 11、没有选择 final obstruction candidate，也没有
证明 Selmer 上界或 family rank-zero theorem。
`wl523` 只尝试这个 named theorem-candidate 的 statement/proof-layer 拆分：
点级 common-source square obstruction 已经由 `wl491` contract 给出，centered-even
pullback 得到有理 `N,M` 后，opposite-side product 不是平方就不能进入 AA+BB
admissible ledger；但这不是 uniform cover-family theorem，15 个 not-admissible
cover families 仍只是 finite taxonomy data。它没有执行 shell 11、没有计算新
support、没有测试新 ambient `C_d`、没有对新点应用 `wl491`、没有选择 final
candidate，也没有证明 Selmer 上界或 family theorem。`wl524` 只做 post-`wl523`
route choice：比较 uniform cover-family squareclass lemma attempt、稍后返回
finite shell 11 `M_tail` diagnostics、proof-level local / Hilbert row work、final
obstruction candidate selection；选择下一窄门为稍后尝试新的 uniform cover-family
squareclass obstruction lemma，但不进入该证明尝试。shell 11 被 defer，local /
Hilbert row work 等待 named Selmer row gap，final candidate selection 被 reject。
`wl524` 没有证明 uniform lemma、没有执行 shell 11、没有选择 final candidate、
没有产生 Selmer 上界或 family rank-zero theorem。`wl525` 进入 `wl524`
选中的 uniform cover-family squareclass obstruction attempt，但在
statement/proof input 层失败：现有 `wl523` / `wl524` 输入只有点级 `wl491`
obstruction 和有限 taxonomy count，没有 cover-family function-field models、
有理 `N,M` maps、divisor parity data 或 specialization argument。因此 15 个
cover families / 29 个 entries 不能被提升成 uniform theorem。`wl525` 不数学上
refute 未来可能的 uniform lemma，只 refute 从当前 finite taxonomy 直接推广；
它没有进入下一 roadmap step，没有执行 shell 11，没有计算新 support，没有测试
新 ambient `C_d`，没有应用 `wl491` 到新点，也没有产生 Selmer 上界或 family
rank-zero theorem。`wl526` 只做 post-`wl525` route choice：比较最小
function-field squareclass proof-data scoping、返回 finite shell / `M_tail`
diagnostics、命名 theorem-level complete-Selmer local / Hilbert row obligation、
以及 abandon 当前 obstruction line 后选择别的 candidate。它选择的下一窄门只是
稍后 scope named cover families 的最小 function-field proof data；不建
function-field models、不证明 uniform lemma、不命名 Selmer row、不选择新
candidate、不执行 shell 11，也不产生 theorem-level progress。`wl527` 只进入
`wl526` 选中的 proof-data scoping gate：对 15 个 named globally soluble but
not AA+BB-admissible cover families 盘点 cover-family model availability、
source-side maps、candidate `N,M` function-field elements、opposite-side
product squareclass / divisor-parity target、以及 exceptional specialization /
positivity separation。结论是 0 个 cover family ready，精确缺口是
`uniform_function_field_model_maps_and_squareclass_certificate`：还缺显式
function-field models、rational source-side maps、`N,M` function-field
elements、opposite-side squareclass/divisor-parity certificate 和 exceptional
specialization / positivity separation。`wl527` 不证明也不 refute uniform
lemma，不进入下一 roadmap step，不产生 Selmer 上界或 family rank-zero
theorem。

## 6. 不要再主线化的东西

下面这些不要写成证明进展：

- certificate count / required count 继续增加；
- 更大范围的 pair counting；
- `AB/BA` rank-zero 尝试；
- 单纯 root number 观察；
- 单纯 mod-`p^k` 筛；
- residual two-cover 的 bounded search no-point candidate。

它们可以是诊断或候选材料，但不是全局证明。

## 7. 保留入口

常用脚本：

```text
scripts/theory/rank_mixed_closure_curves.py
scripts/theory/summarize_mixed_closure_results.py
scripts/theory/audit_mixed_closure_rank0_certificates.py
scripts/theory/audit_mixed_closure_even_model_identities.py
```

常用结果：

```text
results/mixed_closure_rank_summary.json
results/mixed_closure_rank0_certificate_audit.json
results/mixed_closure_even_model_identity_audit.json
results/closure_quotient_rank_zero_selmer_packages/
```

## 8. 停止条件

继续这条线的判断标准很简单：

```text
If global Selmer dimension bound appears possible:
    keep formalizing
else:
    stop treating package growth as proof progress
```

当前主线仍值得保留，但它的瓶颈已经很明确：不是数据不够，而是 Selmer 层兼容性还没证明。
