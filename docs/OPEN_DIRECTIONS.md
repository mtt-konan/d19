# Open Directions

这份文档只保留当前还值得推进的方向。旧的长清单已经归档到
[archive/EXPLORATION_MAP.md](./archive/EXPLORATION_MAP.md) 和阶段 worklog。

## P0: Finish Or Falsify The Rank-Zero Selmer Route

当前第一优先级。

当前窄门：

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

如果 `wl491` 已存在，这个 filter contract 已经有第一版；后续必须先用它把
ambient `C_d` 全局点和 AA+BB common-source admissible 点分开，再继续挑新的
`M_tail` / kernel candidate。`wl492` 若存在，则已确认当前已知 ambient
point ledgers 没有未过滤点：`u_3` 已是 not_admissible，下一步应先从现有
`M_tail` diagnostics 建候选队列，而不是直接随手挑新 candidate。`wl493`
若存在，则既有队列已经确认 active unprocessed candidate 为空；下一步是扩展
或刷新 `M_tail` diagnostics，再让新 support 依次经过 ambient `C_d` solubility
和 `wl491` admissibility filter。`wl494` 若存在，则 `M_tail` diagnostics 已经
用 `1 <= A,B <= 4` 的 primitive AA/BB 样本网格刷新；active diagnostic output
是 `v_5` support entries，但它们还不是 ambient `C_d` 点、不是 AA+BB
admissible 点，也不是 final obstruction candidates。`wl495` 若存在，则这些
entries 已经全部显式分类：四个 exact ambient global `C_d` points 都经
`wl491` route 为 `not_admissible`，另外两个 entries 仍停在 ambient `C_d`
global-solubility deferred ledger；这还不是 obstruction candidate selection。
`wl496` 若存在，则这两个 deferred ledgers 已被同一个 `L=4,T=5,d=(5,1,5)`
cover 的 targeted Mordell-Weil torsion-lift certificate 关闭为 ambient globally
not soluble。`wl496` 没有应用 `wl491` filter、没有产生 admissible point、没有
选择 final obstruction candidate。`wl497` 若存在，则它只做 post-`wl496`
route choice：确认 `u_3` 和有界 refreshed `v_5` supports 都已经处置，选择下一
窄门为 `structure_next_M_tail_diagnostic_extension`，但没有刷新新网格、没有证明
新 local row、没有测试新的 `C_d` solubility，也没有进入 `wl498`。`wl498` 若存在，
则下一批 `M_tail` diagnostic extension 的 finite-shell axes、exclusion ledger、
duplicate-support guard、未来输出 schema 和 stop conditions 已经定义；下一步才是
按这个 plan 执行有限 shell。`wl498` 本身没有刷新新网格、没有计算新 support、
没有测试新的 `C_d` solubility，也没有进入 `wl499`。`wl499` 若存在，则这个
finite shell 已执行在 `max(A,B)=5`，得到两个 active `u_5` `M_tail`
diagnostic supports：`AA_A5_B3_u_5_m_tail_shell5_candidate` 和
`BB_A3_B5_u_5_m_tail_shell5_candidate`。它没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有选 final candidate，也没有进入 `wl500`。
`wl500` 若存在，则这两个 active `u_5` entries 已路由 through ambient
`C_d` solubility：共同 `L=5,T=8,d=(5,5,1)` cover 被 targeted
Mordell-Weil torsion-lift certificate 关闭为 ambient globally not soluble。
因此 `wl491` 没有应用，且没有 admissible point、final obstruction candidate
或 `wl501` route choice。`wl501` 若存在，则它只做 post-`wl500` route
choice：确认 shell-5 `u_5` ledgers 已经处置，选择下一窄门为
`execute_next_finite_M_tail_shell_from_wl498_plan`，也就是稍后从既有 `wl498`
plan 执行下一个 finite primitive shell（`max(A,B)=6`）。`wl501` 没有刷新或
执行新 shell/grid、没有计算新 support、没有测试新的 `C_d` solubility、没有应用
`wl491`，也没有进入 `wl502`。`wl502` 若存在，则这个 shell-6 diagnostic
extension 已经执行：8 个 primitive AA/BB samples 全 rank 满，没有 active new
kernel support，也没有 duplicate/processed support output。它仍没有测试 ambient
`C_d` solubility、没有应用 `wl491`、没有选 final candidate，也没有进入 `wl503`。
`wl503` 若存在，则它只做 post-`wl502` empty-shell route choice：确认 shell-6
空队列后，选择下一窄门为稍后按既有 `wl498` plan 执行下一个 finite primitive
shell（`max(A,B)=7`）。`wl503` 没有执行 shell 7、没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有证明 new local row，也没有声称 uniform
`M_tail` full-rank theorem。`wl504` 若存在，则它已经执行 shell-7 finite
`M_tail` diagnostic extension，产生 12 个 active diagnostic supports 和 2 个
pure `u_3` processed exclusions。active outputs 还不是 ambient `C_d` 全局点、
不是 AA+BB-admissible points、不是 final obstruction candidates；下一步若继续，
必须先做 ambient `C_d` global solubility route，再只在 global point 已证时应用
`wl491`。`wl505` 若存在，则这个 route 已执行：12 个 active shell-7 supports
中 8 个有 exact integral ambient witness 且经 `wl491` 归入 not-admissible，
4 个仍是 deferred ambient `C_d` global-solubility ledgers；没有重开两个 pure
`u_3` processed exclusions，也没有选 final candidate 或证明 Selmer/rank 结论。
`wl506` 若存在，则这 4 个 deferred ledgers 已解决：两个 `w_5` ledgers 为
ambient globally not soluble，两个 `u_7+w_37` ledgers 为 ambient globally
soluble 但经 `wl491` 仍 not AA+BB-admissible；`wl506` 没有进入 post-route
choice、没有选 final candidate、也没有证明 Selmer/rank 结论。`wl507` 若存在，
则 post-`wl506` route choice 已经做完：下一窄门是稍后按既有 `wl498` plan
执行 finite primitive shell `max(A,B)=8`，但 shell 8 尚未执行，也没有新的
ambient `C_d` solubility / `wl491` / local-row / Selmer-rank 结论。`wl508`
若存在，则 shell 8 已作为 `M_tail` diagnostic extension 执行：两个 kernel
outputs 都是 pure `u_3` processed-support repeats，active queue 为空；这不是
ambient `C_d` route、不是 `wl491` result、不是 final candidate，也不是 uniform
`M_tail` theorem。`wl509` 若存在，则 post-`wl508` route choice 已经做完：
确认 shell 8 的两个 pure `u_3` outputs 只是 processed exclusions，active
queue 仍为空，下一窄门是稍后按既有 `wl498` plan 执行 finite primitive shell
`max(A,B)=9`。`wl509` 没有执行 shell 9、没有新的 ambient `C_d` solubility /
`wl491` / local-row / Selmer-rank 结论。
`wl510` 若存在，则 shell 9 已作为 `M_tail` diagnostic extension 执行：
24 个 primitive AA/BB samples 中 16 个 full rank、8 个有 kernel，产生 8 个
active diagnostic supports 且没有 duplicate / processed supports。这些 active
outputs 还不是 ambient `C_d` 全局点、不是 AA+BB-admissible points、不是 final
obstruction candidates；下一步若继续，必须先做 ambient `C_d` global solubility
route，再只在 global point 已证时应用 `wl491`。
`wl511` 若存在，则这 8 个 active shell-9 supports 已经先过 ambient `C_d`
solubility：4 个 exact ambient global points 经 `wl491` route 为
not_admissible，4 个 entries 仍停在 ambient `C_d` global-solubility deferred
ledger。不要重开已过滤的 4 个 not-admissible ledgers，不要执行 shell 10，也不要
把 deferred ledgers 当成 globally not soluble 或 final obstruction candidates。
`wl512` 若存在，则这 4 个 deferred ledgers 已被单独分类：两个 `v_13`
entries 的 `L=4,T=13,d=(13,1,13)` cover 为 ambient globally not soluble，两个
`u_7` entries 的 `L=7,T=16,d=(7,7,1)` cover 仍 genuinely deferred，因为没有
exact ambient point 或 exhaustive no-lift certificate。不要重开两个 refuted
`v_13` ledgers，不要执行 shell 10，不要把这两个 `u_7` ledgers 当成 final
obstruction candidates。`wl513` 若存在，则 post-`wl512` route choice 已经做完：
下一窄门是 targeted resolution of the shared shell-9 `u_7` ambient `C_d` cover
`L=7,T=16,d=(7,7,1)`，但该门尚未进入。不要执行 shell 10，不要重开 `wl512`
`v_13` refutations 或 `wl511` not-admissible shell-9 ledgers，不要直接应用
`wl491`、证明 local row 或选择 final candidate。`wl514` 若存在，则它只进入
`wl513` 选定的窄门：用 single-cover mod-17 Mordell-Weil-sieve no-lift
certificate 把 shared shell-9 `u_7` cover `L=7,T=16,d=(7,7,1)` 关闭为
ambient globally not soluble。因此 `wl491` 没有应用，也没有 post-`wl514`
route choice、shell 10、final candidate、Selmer 上界或 family theorem。`wl515`
若存在，则 post-`wl514` route choice 已经做完：所有 shell-9 deferred ambient
`C_d` ledgers 都已分类，下一窄门是稍后按既有 `wl498` plan 执行 finite primitive
shell `max(A,B)=10`。`wl515` 没有执行 shell 10、没有重开 closed shell-9 ledgers、
没有应用 `wl491`、没有选择 final candidate、没有进入 proof-level row work，也
没有声明 Selmer/rank/family theorem。`wl516` 若存在，则 shell 10 已作为
`M_tail` diagnostic extension 执行：16 个 primitive AA/BB samples 中 6 个
full rank、10 个有 kernel，产生 10 个 active diagnostic supports，且没有
duplicate / processed supports。这些 active outputs 还不是 ambient `C_d`
全局点、不是 AA+BB-admissible points、不是 final obstruction candidates；
下一步若继续，必须先做 ambient `C_d` global solubility route，再只在 global
point 已证时应用 `wl491`。`wl517` 若存在，则这 10 个 shell-10 active
supports 已经路由：8 个 globally soluble but not AA+BB-admissible，2 个
仍 deferred；不要把 deferred covers 当成 refuted，也不要进入 shell 11 或
final-candidate selection。`wl518` 若存在，则 `wl491`-`wl517` ledgers 已经按
support family / cover family 聚合：唯一 genuinely deferred cover family 是
shared shell-10 `u_5` `L=10,T=19,d=(5,5,1)`。这只是 theorem-candidate pattern，
不是 theorem；下一窄门是 targeted resolution of that shared cover，且 `wl518`
没有进入该门、没有执行 shell 11、没有 proof-level generalization，也没有
Selmer/rank/family 结论。`wl519` 若存在，则该 shared shell-10 `u_5` cover
已经由 exact rational ambient `C_d` point 解决为 globally soluble；两个 mirror
entries 经 `wl491` 后都是 globally soluble but not AA+BB-admissible。下一步若
继续，是单独的 post-`wl519` route choice；不要把它改写成 shell 11、proof-level
generalization、final-candidate selection 或 Selmer/rank/family 结论。`wl520`
若存在，则 post-`wl519` route choice 已选择下一窄门为
`synthesize_support_and_cover_families_after_wl519`，但没有进入该 synthesis；
不要跳到 shell 11、proof-level generalization、final-candidate selection 或
Selmer/rank/family 结论。`wl521` 若存在，则该 synthesis 已经进入并完成：
`wl491`-`wl519` ledgers 中没有 genuinely deferred cover family，也没有
AA+BB-admissible cover family；保留下来的 `u_5` 历史只是 finite
theorem-candidate pattern，不是 theorem，也没有隔离 named proof gap。下一窄门只
是稍后按既有 `wl498` plan 执行 finite shell `max(A,B)=11`，但 shell 11
尚未执行。

目标：

```text
for AA / BB / AA+BB rank-zero families:
  prove local image constraints
  prove dyadic local condition
  prove global Selmer dimension bound
  conclude rank(E_lambda)=0
```

已有材料：

- odd-prime formal-lift reviewable segments for several kernels;
- package ledgers under `results/closure_quotient_rank_zero_selmer_packages/`;
- intake/materialization scripts and tests.

还缺：

- if `wl506` is not present, resolve the four deferred shell-7 ambient `C_d`
  global-solubility ledgers without re-opening the eight not-admissible
  shell-7 ledgers or the two pure `u_3` processed exclusions;
- if `wl506` is present but `wl507` is not present, do not re-open those
  resolved ledgers; the next route choice is not entered by `wl506`;
- if `wl507` is present but `wl508` is not present, do not re-open shell-7
  ledgers; shell 8 is only the selected next gate and has not been executed;
- if `wl508` is present, do not invent an ambient `C_d` route for shell 8;
  the active queue is empty after the two pure `u_3` processed exclusions;
- if `wl509` is present but `wl510` is not present, do not re-open shell-8
  processed `u_3` exclusions; shell 9 is only the selected next gate and has
  not been executed;
- if `wl510` is present, do not skip directly from active shell-9 `M_tail`
  supports to `wl491` or final-candidate selection; they must first route
  through ambient `C_d` global solubility;
- if `wl511` is present, do not re-open the four shell-9 globally soluble but
  not-admissible ledgers; the remaining current gap is the four deferred
  shell-9 ambient `C_d` global-solubility ledgers, not shell 10 or final
  candidate selection;
- if `wl512` is present but `wl513` is not present, do not re-open the two
  refuted shell-9 `v_13` ledgers or the four shell-9 globally soluble but
  not-admissible ledgers from `wl511`; the remaining current gap is the two
  `u_7` shell-9 ambient `C_d` global-solubility deferred ledgers, not shell 10
  or final candidate selection;
- if `wl513` is present, do not treat the selected `u_7` cover resolution gate
  as entered; the next explicit work is to resolve the shared
  `L=7,T=16,d=(7,7,1)` ambient `C_d` cover by exact point or exhaustive
  no-lift certificate, not to execute shell 10 or re-open closed shell-9
  ledgers;
- if `wl514` is present but `wl515` is not present, do not treat the
  post-`wl514` route choice as made; the shared shell-9 `u_7` cover has been
  refuted as ambient globally not soluble, `wl491` was not applied, and the
  next explicit work is a separate route-choice gate;
- if `wl515` is present but `wl516` is not present, do not execute shell 10
  unless that is the explicit next task; do not re-open any closed shell-9
  ledger, apply `wl491` to a refuted cover, pivot to proof-level row work
  without a named proof gap, or treat shell diagnostics as theorem-level
  Selmer progress;
- if `wl516` is present, do not skip directly from active shell-10 `M_tail`
  supports to `wl491` or final-candidate selection; they must first route
  through ambient `C_d` global solubility;
- if `wl517` is present, do not re-open the eight shell-10 not-admissible
  ledgers, do not treat the two deferred shell-10 covers as refuted without a
  certificate, and do not execute shell 11 or select a final candidate;
- if `wl518` is present, do not treat the support-family synthesis as a
  certificate; the next explicit work is targeted resolution of the shared
  shell-10 `u_5` `L=10,T=19,d=(5,5,1)` ambient `C_d` cover, not shell 11,
  proof-level generalization, or final-candidate selection;
- if `wl519` is present, do not re-open the two shared shell-10 `u_5`
  not-admissible ledgers; the next explicit work is a separate post-`wl519`
  route choice, not shell 11, proof-level generalization, or final-candidate
  selection;
- if `wl520` is present, do not treat the selected post-`wl519` synthesis as
  entered; the next explicit work is support/cover-family synthesis over
  `wl491`-`wl519`, not shell 11, proof-level generalization,
  final-candidate selection, or a family theorem claim;
- if `wl521` is present, do not treat shell 11 as executed and do not turn the
  finite `u_5` mixed refuted/not-admissible history into a named proof gap or
  family theorem; the next explicit work is only the later finite shell
  extension at `max(A,B)=11` from the existing `wl498` plan;
- complete dyadic theorem;
- complete local-image theorem;
- global Selmer dimension bound;
- final rank-zero theorem.

判定标准很简单：如果不能推出 global Selmer dimension bound，就不要把 package
数量增长当成证明进展。

## P1: Closure Quotient Certificate Ledger

保留并清理当前严格证书账：

```text
AA/BB rank=0
  -> torsion enumeration
  -> pullback
  -> midpoint only
  -> Yang Ji midpoint exclusion
```

这条线的用途是记录已经严格排除的 ratio / pair。它不是通用证明，但它是当前最干净的
有限证据。

## P1: Residual Two-Cover / Sha[2] Frontier

当前 residual covers 是 explicit candidates，不是 no-point proofs。

可做方向：

- Mordell-Weil sieve;
- Cassels-Tate pairing;
- external Magma/Sage certificate;
- Brauer-Manin style obstruction.

优先级低于 rank-zero Selmer，因为它更偏逐个 residual target，不如 family theorem
有杠杆。

## P2: Lambda / Root-Number Map

给 `lambda=A/B` 画地形图：

- 哪些 ratio class 已有 rank-zero certificate；
- 哪些被 root number 奇偶性挡住；
- 哪些落入 two-cover residual；
- 哪些需要新工具。

这能帮助判断 rank-zero 刀的理论覆盖上限，但本身不是证明。

## Closed Or Paused

下面这些不再当主线：

- more pair counting / larger `required_count`;
- `AB/BA` rank-zero knife;
- pure mod-`p^2` universal obstruction;
- old fixed-ratio `sum=A+B` proof route;
- partner graph / high-`k` as proof route;
- Heegner height as global decider;
- raw proof_status scaling as proof progress.

## Rule Of Thumb

新的 work 只有满足下面之一，才算主线进展：

- 产生可复核 theorem/proof segment；
- 缩小 global Selmer bound 的缺口；
- 把 candidate 变成 strict certificate；
- 证明某条旧路线确实不能用，从而减少搜索空间。

只增加样本数、package 数、候选数，不算主线进展。
