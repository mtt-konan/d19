# Project Status

这份文档是当前入口。旧的逐轮记录已经压缩到
[worklog index](./work-logs/README.md)。

## Current Mainline

项目现在的主线是：

```text
closure quotient
  -> lambda = A/B 射线账本
  -> AA/BB rank-zero certificates
  -> rank-zero Selmer family proof attempt
```

入口：

- [CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)
- [NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md)
- [294-closure-quotient-foundation-consolidated.md](./work-logs/294-closure-quotient-foundation-consolidated.md)
- [363-lambda-mainline-consolidated.md](./work-logs/363-lambda-mainline-consolidated.md)
- [386-rank-zero-selmer-package-consolidated.md](./work-logs/386-rank-zero-selmer-package-consolidated.md)

普通话说：现在不是继续数更多 `(A,B)`，而是想证明一整批
`lambda=A/B` ratio family 的 `AA/BB` quotient rank 为 0。

## What Is Proved

Strictly proved or safely usable:

- GEN-CLOSURE 是正确的全平面闭合语言：
  `{N1+N2, |N1-N2|}` 必须和 `{A+B, |A-B|}` 相交。
- 旧 concordant 曲线会漏掉闭合腿 `M=A+B-N` 的信息。
- `AA/BB rank=0 + torsion pullback` 是严格有限证书。
- 已认证的 `AA/BB rank=0` 行只回拉到中点，没有完整闭合点。
- 中点分支由 Yang Ji 定理关闭。
- `AB/BA` 不是 rank-zero 击杀器。

## What Is Not Proved

还没有证明：

- Harborth 全局命题。
- 所有 `lambda` family 的 rank-zero 定理。
- residual two-cover / Sha[2] candidate 没有有理点。
- `required_count` 或 certificate count 增长本身不是数学进展。

## Current Bottleneck

当前瓶颈是 Selmer/rank-zero family proof：

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

最近的 worklog 主要是在补这些 proof package 的可审阅段落。它们是证明链材料，
但每多一个 package 段落并不等于命题更接近完成；只有合成出 global Selmer
dimension bound 才算真正跨一步。

`wl490` 之后的窄瓶颈更具体：定义并使用 reusable
ambient-`C_d`-to-AA+BB admissibility filter。`wl491` 若在当前工作区中，
就是这个 filter contract 的第一版。也就是说，任何 ambient complete
`d`-coordinate `C_d` 全局点，都必须先通过 AA+BB common-source 闭合约束，
才能进入 admissible-point ledger。否则它只能留在诊断账本，不能当成
obstruction，也不能当成 AA+BB 解的证据。`wl492` 若存在，则当前已知
ambient ledger 已过滤完：`u_3` 是 not_admissible，下一窄门是从现有
`M_tail` diagnostics 建候选队列。`wl493` 若存在，则这个既有队列已经建完：
唯一的 `wl481` kernel support 是已处理的 `u_3`，active queue 为空。`wl494`
若存在，则已经用有界 primitive AA/BB 样本网格刷新 `M_tail` diagnostics：
新出现的 active diagnostic supports 是 `v_5`，但还没有证明 ambient `C_d`
solubility，也还没有通过 `wl491` admissibility filter。`wl495` 若存在，则
这六个 `v_5` entries 已经全部显式路由：四个有 exact ambient `C_d` global
point，随后经 `wl491` filter 归入 `not_admissible`；剩下两个没有被丢弃，
而是进入 ambient `C_d` global-solubility deferred ledger。`wl496` 若存在，
则这两个 deferred entries 已用同一个 `L=4,T=5,d=(5,1,5)` 的 targeted
Mordell-Weil torsion-lift certificate 关闭为 ambient globally not soluble；
`wl491` filter 没有应用，因为没有 ambient global `C_d` point 可过滤。`wl496`
没有选择后续候选。`wl497` 若存在，则它只选择下一窄门：
`structure_next_M_tail_diagnostic_extension`。也就是说，当前有界 `u_3` / `v_5`
路线已处置完，下一步若继续，应先结构化下一批 `M_tail` diagnostics，并显式不重开
这些已处置 ledger；`wl497` 本身没有刷新新网格、没有证明新 local row、没有测试
新的 `C_d` solubility，也没有进入 `wl498`。`wl498` 若存在，则这个结构化计划
已经写出：下一批只能是声明过的 finite primitive shell，`max(A,B) > 4`，
必须用 route key
`source_quotient,A,B,L,T,candidate_support` 做 duplicate guard，`u_3` support
family 继续排除/降级，bounded `wl494`-`wl496` 的 `v_5` route keys 不得重开。
`wl498` 没有刷新新网格、没有计算新 support、没有测试新的 `C_d` solubility，
也没有进入 `wl499`。`wl499` 若存在，则它已经按 `wl498` plan 执行唯一的
finite primitive shell `max(A,B)=5`，得到两个 active `u_5` `M_tail`
diagnostic supports：
`AA_A5_B3_u_5_m_tail_shell5_candidate` 和
`BB_A3_B5_u_5_m_tail_shell5_candidate`。它没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有选 final candidate，也没有进入 `wl500`。
`wl500` 若存在，则这两个 active `u_5` entries 已经通过 ambient `C_d`
solubility gate：它们共享 `L=5,T=8,d=(5,5,1)` cover，并由 targeted
Mordell-Weil torsion-lift certificate 记录为 ambient globally not soluble；
因此 `wl491` filter 没有应用，也没有产生 admissible point、final candidate
或 `wl501` route choice。`wl501` 若存在，则它只选择 post-`wl500` 下一窄门：
`execute_next_finite_M_tail_shell_from_wl498_plan`。也就是说，shell-5 `u_5`
路线已处置完，下一步若继续，应按既有 `wl498` finite-shell plan 执行下一壳
`max(A,B)=6`；`wl501` 本身没有刷新或执行新 shell/grid、没有证明新 local row、
没有测试新的 `C_d` solubility、没有应用 `wl491`，也没有进入 `wl502`。`wl502`
若存在，则它已经执行这个 shell-6 `M_tail` diagnostic extension：8 个 primitive
AA/BB 样本全 rank 满，`active_new_kernel_supports=[]` 且
`excluded_duplicate_or_processed_supports=[]`。它没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有选择 final candidate，也没有进入 `wl503`。
`wl503` 若存在，则它只做 post-`wl502` empty-shell route choice：确认 shell-6
没有 active support 或 duplicate / processed support output，选择下一窄门为
继续按既有 `wl498` plan 执行下一个 finite primitive shell（`max(A,B)=7`）。
`wl503` 没有执行 shell 7、没有测试 ambient `C_d` solubility、没有应用 `wl491`、
没有证明 new local row，也没有把 shell-6 full-rank 样本写成 uniform `M_tail`
theorem。`wl504` 若存在，则它已经执行这个 shell-7 `M_tail` diagnostic
extension：24 个 primitive AA/BB 样本中 12 个 full rank、12 个有 kernel，
产生 12 个 active diagnostic supports 和 2 个 pure `u_3` processed exclusions。
它没有测试 ambient `C_d` solubility、没有应用 `wl491`、没有选择 final
candidate、没有证明 local row，也没有进入后续 route。`wl505` 若存在，则它
已经把这 12 个 active shell-7 supports 先路由过 ambient `C_d` solubility：
8 个有 exact integral ambient witness，并经 `wl491` 归入 globally soluble but
not AA+BB-admissible；4 个仍是 deferred ambient-solubility ledgers。两个 pure
`u_3` processed exclusions 没有被重开。`wl505` 没有选择 final candidate、没有
证明 local row、没有运行 broad Selmer/rank diagnostics，也没有进入下一步。
`wl506` 若存在，则它只解决这四个 `wl505` deferred ledgers：两个 `w_5`
entries 的共同 `L=4,T=11,d=(1,5,5)` cover 被记录为 ambient globally not
soluble；两个 `u_7+w_37` entries 的共同 `L=7,T=10,d=(7,259,37)` cover 有
exact rational ambient point，但经 `wl491` 仍是 not AA+BB-admissible。`wl506`
没有重开八个 shell-7 not-admissible ledgers 或两个 pure `u_3` exclusions，也没有
选择 final candidate、证明 local row、运行 broad Selmer/rank diagnostics，或进入
下一步 route choice。`wl507` 若存在，则它只做 post-`wl506` route choice：
确认 shell-7 active/deferred route 已全部处置，选择下一窄门为按既有 `wl498`
plan 执行下一个 finite primitive shell（`max(A,B)=8`）。`wl507` 没有执行
shell 8、没有测试新的 `C_d` solubility、没有应用 `wl491`、没有选择 final
candidate、没有证明 local row，也没有声明任何 Selmer/rank/family theorem。
`wl508` 若存在，则它已经执行这个 shell-8 `M_tail` diagnostic extension：
16 个 primitive AA/BB 样本中 14 个 full rank、2 个有 pure `u_3` kernel，
两个 kernel outputs 都被 processed-support guard 归入
`excluded_duplicate_or_processed_supports`，所以
`active_new_kernel_supports=[]`。它没有测试 ambient `C_d` solubility、没有应用
`wl491`、没有选择 final candidate、没有证明 local row，也没有把 shell-8
结果写成 uniform `M_tail` theorem。
`wl509` 若存在，则它只做 post-`wl508` empty-active-shell route choice：
确认 shell-8 active queue 为空且两个 kernel outputs 都是 pure `u_3` processed
exclusions，选择下一窄门为继续按既有 `wl498` plan 执行下一个 finite primitive
shell（`max(A,B)=9`）。`wl509` 没有执行 shell 9、没有测试 ambient `C_d`
solubility、没有应用 `wl491`、没有选择 final candidate、没有证明 local row，
也没有把 shell-8 full-rank samples 或空 active queue 写成 uniform `M_tail`
theorem。
`wl510` 若存在，则它已经执行这个 shell-9 `M_tail` diagnostic extension：
24 个 primitive AA/BB 样本中 16 个 full rank、8 个有 kernel，产生 8 个
active diagnostic supports，且没有 duplicate / processed support output。它
没有测试 ambient `C_d` solubility、没有应用 `wl491`、没有选择 final candidate、
没有证明 local row，也没有把 shell-9 输出写成 Selmer/rank/family theorem。
`wl511` 若存在，则它已经把这 8 个 active shell-9 supports 先路由过
ambient `C_d` solubility：4 个有 exact integral ambient witness，并经 `wl491`
归入 globally soluble but not AA+BB-admissible；4 个仍是 deferred ambient
`C_d` global-solubility ledgers。它没有执行 shell 10、没有选择 final candidate、
没有证明 local row、没有运行 broad Selmer/rank diagnostics，也没有把 deferred
ledgers 写成 globally not soluble。`wl512` 若存在，则它只分类这 4 个
`wl511` deferred ledgers：两个 `v_13` entries 的共同 `L=4,T=13,d=(13,1,13)`
cover 被记录为 ambient globally not soluble；两个 `u_7` entries 的共同
`L=7,T=16,d=(7,7,1)` cover 仍然 deferred，因为没有记录 exact ambient
`C_d` point 或 exhaustive no-lift certificate。`wl512` 没有执行 shell 10、
没有应用 `wl491`、没有选择 final candidate、没有证明 local row、没有运行 broad
Selmer/rank diagnostics，也没有推进到 `wl513`。`wl513` 若存在，则它只做
post-`wl512` route choice：确认唯一剩余具体缺口是两个 `u_7` shell-9 ledgers
共享的 `L=7,T=16,d=(7,7,1)` ambient `C_d` cover，并选择下一窄门为 targeted
resolution of that cover。`wl513` 没有进入该门、没有执行 shell 10、没有测试新的
solubility、没有应用 `wl491`、没有证明 local row、没有选择 final candidate，
也没有声明 Selmer/rank/family theorem。`wl514` 若存在，则它只进入这个
`wl513` 选定窄门：用 mod-17 Mordell-Weil-sieve no-lift certificate 关闭
shared shell-9 `u_7` cover `L=7,T=16,d=(7,7,1)` 为 ambient globally not
soluble。因为没有 ambient global point，`wl491` 没有应用；`wl514` 也没有做
post-route choice、shell 10、final candidate、Selmer 上界或 family theorem。
`wl515` 若存在，则它只做 post-`wl514` route choice：确认所有 shell-9
deferred ambient `C_d` ledgers 已分类，并选择下一窄门为稍后按既有 `wl498`
plan 执行 finite primitive shell `max(A,B)=10`。`wl515` 没有执行 shell 10、
没有重开 closed shell-9 ledgers、没有应用 `wl491`、没有进入 proof-level row
work、没有选择 final candidate，也没有声明 Selmer/rank/family theorem。
`wl516` 若存在，则它已经执行这个 shell-10 `M_tail` diagnostic extension：
16 个 primitive AA/BB 样本中 6 个 full rank、10 个有 kernel，产生 10 个
active diagnostic supports，且没有 duplicate / processed support output。它
没有测试 ambient `C_d` solubility、没有应用 `wl491`、没有选择 final candidate、
没有证明 local row，也没有把 shell-10 输出写成 Selmer/rank/family theorem。
`wl517` 若存在，则这 10 个 active shell-10 supports 已经先过 ambient
`C_d` solubility：8 个有 exact integral ambient points，并经 `wl491` 归为
globally soluble but not AA+BB-admissible；2 个仍是 deferred ambient-solubility
ledgers。它没有执行 shell 11、没有选择 final candidate、没有证明 local row，
也没有声明 Selmer/rank/family theorem。`wl518` 若存在，则它只把
`wl491`-`wl517` ledger outputs 按 support family / cover family 重新聚合：
唯一仍 genuinely deferred 的 cover family 是 shared shell-10 `u_5`
`L=10,T=19,d=(5,5,1)` cover。`u_5` 的 refuted / not-admissible / deferred
历史只是 theorem-candidate pattern，不是 family theorem；`wl518` 选择下一窄门为
targeted resolution of that shared cover，但没有进入该门、没有执行 shell 11、没有
选择 final candidate、没有运行 broad rank/Selmer diagnostics，也没有声明
Selmer/rank/family theorem。`wl519` 若存在，则它进入这个 selected gate，用
exact rational ambient `C_d` point 把 shared shell-10 `u_5`
`L=10,T=19,d=(5,5,1)` cover 分类为 globally soluble，并在应用 `wl491` 后把
两个 mirror entries 都路由为 globally soluble but not AA+BB-admissible。它没有
做 post-`wl519` route choice、没有执行 shell 11、没有选择 final candidate，也
没有声明 Selmer/rank/family theorem。`wl520` 若存在，则它只做 post-`wl519`
route choice：确认唯一 `wl518` deferred cover family 已分类且没有
AA+BB-admissible 或 final candidate，比较 support/cover-family synthesis、
shell 11、proof-level generalization / local-row work 和 final-candidate
selection，选择下一窄门为 `synthesize_support_and_cover_families_after_wl519`。
它没有进入该 synthesis、没有执行 shell 11、没有选择 final candidate，也没有声明
Selmer/rank/family theorem。`wl521` 若存在，则它只进入这个 selected synthesis：
把 `wl491`-`wl519` ledgers 按 support family / cover family 重新聚合，确认没有
genuinely deferred cover family、没有 AA+BB-admissible cover family，并把 `u_5`
的 mixed refuted / not-admissible 历史只保留为 theorem-candidate pattern。它没有
隔离 named proof gap，没有执行 shell 11、没有计算新 supports、没有测试新的
ambient `C_d` solubility、没有选择 final candidate，也没有声明
Selmer/rank/family theorem；下一窄门只是稍后按既有 `wl498` plan 执行
`max(A,B)=11` finite shell。`wl522` 若存在，则它只做 taxonomy checkpoint：
用 `wl521` 作 latest state，把 `wl491`-`wl521` ledgers 压成 support/cover
family、classification、failure-mode taxonomy。结果是 5 个 ambient globally
not soluble cover families、15 个 globally soluble but not AA+BB-admissible
cover families、2 个 processed / duplicate cover families、没有 deferred 或
AA+BB-admissible cover families。它隔离的唯一下一 proof-level theorem-candidate
是
`common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families`，
但没有进入证明、没有执行 shell 11、没有计算新 support、没有测试新的 ambient
`C_d` solubility、没有选择 final candidate，也没有声明 Selmer/rank/family
theorem。

## Historical Routes

历史大路线已经压缩：

- `wl028-wl052`: proof-status / elliptic curve / Selmer 工具。
- `wl053-wl072`: partner graph / fast-core 工程。
- `wl073-wl104`: GEN-CLOSURE / modular filters / full-space scans。
- `wl105-wl161`: fixed-ratio / `sum=A+B` 探索。
- `wl162-wl202`: `R_lambda` / centerline。
- `wl203-wl293`: wl218 full-plane reciprocal route，未证明成功。

这些不是当前主线，只在需要追溯旧路线为什么关闭时阅读。

## Practical Next Step

继续主线时先看当前窄门，再看 Selmer 总门：

1. reusable ambient-`C_d`-to-AA+BB admissibility filter 是否已定义并测试。
2. 是否已经从现有 `M_tail` diagnostics 建出下一批候选队列，并排除/降级
   已处理的 `u_3`。
3. 是否已经刷新 `M_tail` diagnostics，并把新 support 仍停在 diagnostic 层。
4. 新 ambient `C_d` 点是否先过 admissibility filter，再进入任何 admissible ledger。
5. `wl496` 是否已经解决 `wl495` 后两个 deferred `v_5` ambient `C_d`
   ledgers；若已解决，不要重开这两个 entries。
6. `wl497` 是否已经选择 post-`wl496` 下一窄门；若已选择，下一步是结构化下一批
   `M_tail` diagnostics，而不是重开 `u_3` / bounded `v_5`。
7. `wl498` 是否已经定义下一批 `M_tail` diagnostics 的 finite-shell axes、
   exclusion ledger、duplicate-support guard、输出 schema 和停止条件；若已定义，
   下一步才是按这个计划执行有限 shell，而不是测试 `C_d` 或选 final candidate。
8. `wl499` 是否已经执行 shell `max(A,B)=5`；若已执行，新的 `u_5` supports
   仍只是 `M_tail` diagnostic outputs，下一步才是 ambient `C_d` solubility
   路由，然后才可能应用 `wl491`。
9. `wl500` 是否已经关闭这两个 active `u_5` ambient ledgers；若已关闭，
   不要重开它们，也不要把 globally not soluble 误写成 admissible / not
   admissible point。
10. `wl501` 是否已经选择 post-`wl500` 下一窄门；若已选择，下一步才是按
   `wl498` plan 执行下一个 finite `M_tail` shell，而不是重开旧 ledgers 或先做
   broad theorem-level diagnostics。
11. `wl502` 是否已经执行 shell `max(A,B)=6`；若已执行且 queue 为空，下一步
   才是单独的 post-`wl502` route choice，不要把 shell-6 full-rank 样本误写成
   uniform `M_tail` proof。
12. `wl503` 是否已经选择 post-empty-shell 下一窄门；若已选择，下一步才是按
   `wl498` plan 执行 shell `max(A,B)=7`，不是重开 shell-6 ambient route。
13. `wl504` 是否已经执行 shell `max(A,B)=7`；若已执行且有 active queue，下一步
   才是把 active shell-7 supports 先路由过 ambient `C_d` solubility，再按需应用
   `wl491`，不要直接选 final candidate。
14. `wl505` 是否已经路由 active shell-7 supports；若已路由，则不要重开 8 个
   globally soluble but not-admissible ledgers 或 2 个 pure `u_3` processed
   exclusions，剩下的是 4 个 deferred ambient `C_d` global-solubility ledgers。
15. `wl506` 是否已经解决这 4 个 deferred ledgers；若已解决，不要把其中两个
    globally soluble but not-admissible entries 当作 AA+BB 点，也不要把两个
    refuted entries 当作 final obstruction candidate。
16. `wl507` 是否已经选择 post-`wl506` 下一窄门；若已选择，下一步才是按
    `wl498` plan 执行 shell `max(A,B)=8`，不是重开 shell-7 ledgers 或先做
    broad theorem-level diagnostics。
17. `wl508` 是否已经执行 shell `max(A,B)=8`；若已执行且 active queue 为空，
    下一步才是单独的 post-`wl508` route choice，不要把 shell-8 full-rank
    samples 或空 active queue 写成 uniform `M_tail` proof。
18. `wl509` 是否已经选择 post-`wl508` 下一窄门；若已选择且 `wl510` 尚不存在，
    下一步才是按 `wl498` plan 执行 shell `max(A,B)=9`，不是重开 shell-8
    processed exclusions 或先做 ambient route。
19. `wl510` 是否已经执行 shell `max(A,B)=9`；若已执行且有 active queue，
    下一步才是把 active shell-9 supports 先路由过 ambient `C_d` solubility，
    再按需应用 `wl491`，不要直接选 final candidate。
20. `wl511` 是否已经路由 active shell-9 supports；若已路由且 `wl512` 尚不存在，
    则不要重开 4 个 globally soluble but not-admissible ledgers，剩下的是 4 个
    deferred ambient `C_d` global-solubility ledgers；不要执行 shell 10 或把
    deferred ledgers 写成 refuted。
21. `wl512` 是否已经分类这 4 个 deferred ledgers；若已分类，则不要重开两个
    refuted `v_13` ledgers 或四个 `wl511` not-admissible ledgers。只剩两个
    `u_7` shell-9 ambient `C_d` global-solubility ledgers仍 deferred；不要执行
    shell 10、不要选 final candidate、不要把它们写成 globally soluble /
    globally not soluble，除非有 explicit certificate。
22. `wl513` 是否已经选择 post-`wl512` 下一窄门；若已选择，下一步才是 targeted
    resolution of the shared shell-9 `u_7` cover `L=7,T=16,d=(7,7,1)`，不是
    shell 10、不是重开 closed ledgers、不是直接应用 `wl491`。
23. `wl514` 是否已经解决这个 shared shell-9 `u_7` cover；若已解决且 `wl515`
    尚不存在，则不要把 post-`wl514` route choice 当成已经做完，也不要把这个
    single-cover no-lift certificate 写成 uniform `M_tail` theorem 或
    Selmer/rank 结论。
24. `wl515` 是否已经选择 post-`wl514` 下一窄门；若已选择且 `wl516` 尚不存在，下一步才是按
    `wl498` plan 执行 shell `max(A,B)=10`，不是重开 closed shell-9 ledgers、
    不是直接应用 `wl491`，也不是无 named proof gap 的 proof-level pivot。
25. `wl516` 是否已经执行 shell `max(A,B)=10`；若已执行且有 active queue，
    下一步才是把 active shell-10 supports 先路由过 ambient `C_d` solubility，
    再按需应用 `wl491`，不要直接选 final candidate。
26. `wl517` 是否已经路由 shell-10 active supports；若已路由，则不要重开 8 个
    not-admissible ledgers，也不要把 2 个 deferred covers 当成已 refuted 或
    直接进入 shell 11 / final-candidate selection。
27. `wl519` 是否已经解决 shared shell-10 `u_5` cover；若已解决且 `wl520`
    尚不存在，下一步只是 post-`wl519` route choice，不是 shell 11、proof-level
    generalization 或 final-candidate selection。
28. `wl520` 是否已经选择 post-`wl519` 下一窄门；若已选择，下一步才是
    `wl491`-`wl519` support/cover-family synthesis，不是执行 shell 11 或声明
    family theorem。
29. `wl521` 是否已经完成 post-`wl519` synthesis；若已完成且 `wl522` 尚不存在，
    下一步才是 taxonomy checkpoint 或显式选择的后续门，不是把 `u_5` finite
    history 写成 named proof gap、family theorem 或 Selmer/rank 结论。
30. `wl522` 是否已经隔离 common-source square obstruction theorem-candidate；
    若已完成，下一步只是尝试该 lemma candidate，不是 shell 11、final
    obstruction candidate、Selmer 上界或 rank-zero theorem。
31. `AA/BB/AA+BB` 的 remaining package 是否真的补成完整 local-image theorem。
32. dyadic local condition 是否能和 odd-prime 段落合并。
33. global Selmer dimension bound 是否能推出 rank zero。

如果第 19 步做不出来，这条 rank-zero Selmer 证明线就只是材料堆积，需要换方向。
