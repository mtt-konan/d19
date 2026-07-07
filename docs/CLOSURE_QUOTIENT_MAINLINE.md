# Closure Quotient Mainline

这份文档把 `tmp.txt` 里的混合闭合商曲线方向正式并入 `concordant` 主线。它负责回答：

- 固定 `(A,B)` 后，怎样把被旧曲线忘掉的闭合腿 `M=A+B-N` 放回问题里；
- 哪些闭合商曲线已经能给出严格判据；
- 哪些地方还只是实验信号，不能写进 `proof_status`。

如果只想看临时判断，读 [wl294](work-logs/294-tmp-mixed-closure-answer.md)。如果要接着做这条线，
从本文开始。若要写成论文段落，读 [closure quotient partial result](paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md)。

## 1. 主线位置

当前项目仍以 `concordant` 为 active 主线。closure quotient 是 `concordant` 下面的新子方向。
当前口径已经从“继续堆单个 `(A,B)` 证书数量”切换为：

```text
closure quotient = 离线局部证书工具
主线目标 = lambda=A/B 层面的比例类结构证明
```

普通话说：closure quotient 已经证明它能在一些具体 pair 上严格排除闭合点；下一步不再把
“又排掉几个 pair”当主进展，而是看哪些本原比例 `A:B` 可以被 rank-zero、root-number、
2-cover 等机制整族解释。

旧主线问：

```text
是否存在 N，使 N^2 + A^2 与 N^2 + B^2 同时为平方？
```

closure quotient 问：

```text
若 M = A+B-N，也要求 M^2 + A^2 与 M^2 + B^2 为平方，会发生什么？
```

普通话说：旧曲线能解释半解，closure quotient 才开始看完整闭合。

## 2. 四条商曲线

内部和闭合关系取：

```text
M = A+B-N
```

四个平方条件是：

```text
NA: N^2 + A^2
NB: N^2 + B^2
MA: M^2 + A^2
MB: M^2 + B^2
```

把其中两个相乘，得到四条看见闭合关系的 genus-one 商曲线：

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

完整闭合点必须落在这四条商曲线上。任何一条商曲线能严格排除非平凡点，就能排除原闭合点。

## 3. 已经可用的判据

### 3.1 `AA/BB rank=0` torsion 回拉

`AA/BB` 有中点对称。令：

```text
t = 2N - (A+B)
z = 4y
```

它们化为偶四次：

```text
z^2 = t^4 + p t^2 + q
```

其中 `L=A` 对应 `AA`，`L=B` 对应 `BB`：

```text
p = 8L^2 - 2(A+B)^2
q = ((A+B)^2 + 4L^2)^2
```

对应的椭圆曲线是：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

反向回拉：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = ((A+B)+t)/2
```

所以当 PARI 认证 `rank_lower=rank_upper=0` 时，`E(Q)` 全由 torsion 点组成。枚举 `elltors(E)` 并回拉，
即可列出原四次曲线的全部仿射有理点。

论文级口径可以先写成下面这个引理：

```text
引理（AA/BB rank-0 torsion 回拉）。
设 Q_L 是 AA 或 BB 商曲线，L 分别取 A 或 B。若上面的 centered even model 非奇异，
且对应椭圆曲线 E 满足 rank E(Q)=0，则 Q_L 的全部仿射有理点来自 E(Q)_tors 的显式回拉。
其中 E 的单位元不给仿射点，X=-p 的 torsion 点对应四次曲线无穷远点。
其余 torsion 点按 t=V/(2(X+p)), z=X/2-t^2, N=((A+B)+t)/2 回拉。
若这些仿射回拉点没有 full-closed square 点，则 Q_L 排除原闭合曲线的完整仿射点。
```

普通话说：rank `0/0` 之后，椭圆曲线那边已经没有自由移动的点了。剩下有限个 torsion 点，
逐个拉回即可。两个例外点也有明确去处：一个是椭圆曲线无穷远点，一个是四次曲线无穷远点。
它们都不给有限的 `N`。

当前实现：

```text
src/rational_distance/concordant/mixed_closure_curves.py
  certify_rank_zero_even_quotient()

scripts/theory/rank_mixed_closure_curves.py
  --certify-rank0-torsion

scripts/theory/summarize_mixed_closure_results.py
  summarize rank/certificate JSONL files for paper tables
```

这个判据已经跑过两批样本：

```text
320 hard cases:
  AA/BB rank-0 certificates = 216
  strict excluded pairs = 178
  all certified
  all affine preimages are midpoint N=M=(A+B)/2
  full closed affine preimages = 0

64 local-global residual pairs:
  AA/BB rank-0 certificates = 59
  strict excluded pairs = 42
  all certified
  all affine preimages are midpoint N=M=(A+B)/2
  full closed affine preimages = 0
```

这已经是严格判据，不再是高度枚举。

独立审计入口：

```bash
uv run python scripts/theory/audit_mixed_closure_rank0_certificates.py \
  --input results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --input results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/mixed_closure_rank0_certificate_audit.json \
  --strict
```

真实审计结果：

```text
rank0_aabb_rows=275
certified_rows=275
strict_no_full_closed_rows=275
only_midpoint_rows=275
classification_detail_rows=275
classification_detail_point_count=550
violations=0
```

这一步只审计已经写入 JSONL 的 torsion-pullback 证书；rank 认证仍来自前面的 PARI rank
计算和 certificate 生成流程。审计不仅看 certificate 汇总布尔字段，也逐条检查
`affine_preimage_classifications`，确认每个 affine preimage 都是 midpoint 且不是 full-closed square。

代数公式审计入口：

```bash
uv run python scripts/theory/audit_mixed_closure_even_model_identities.py \
  --out results/mixed_closure_even_model_identity_audit.json \
  --strict
```

当前结果：

```text
all_verified=True
```

它只审计 centered even model 和双向映射公式，不认证 rank 或有理点。

### 3.2 root number 只作诊断

rank 输出现在记录 `root_number`。它帮助观察 parity pattern，但当前不作为无条件判据。

320 hard cases：

```text
AA root_number {-1: 166, 1: 154}
AB root_number { 1: 144, -1: 176}
BA root_number { 1: 144, -1: 176}
BB root_number { 1: 146, -1: 174}
```

64 residual pairs：

```text
AA { 1: 30, -1: 34}
AB {-1: 27,  1: 37}
BA {-1: 27,  1: 37}
BB { 1: 34, -1: 30}
```

## 4. 不能主线化的说法

不要把这条线写成“已经证明 Harborth 猜想”。

不要说 `AB` 是 rank-0 击杀器。两批样本里 `AB/BA` 都没有 rank `0`。

不要把 `AA/BB rank=0` 当作全体 pair 的判定器。它只处理 rank 已经 certified 为 `0/0` 的
`AA/BB` 行。

不要把 root number 当作无条件证明。它目前只是诊断字段。

## 5. 主线任务表

### P0：保持已完成结论可复现

已完成。

复现命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --certify-rank0-torsion

PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/mixed_closure_localglobal_residual64_pairs.jsonl \
  --out results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --certify-rank0-torsion

uv run python scripts/theory/summarize_mixed_closure_results.py \
  --input results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --input results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/mixed_closure_rank_summary.json
```

### P1：收紧不确定 rank bounds

320 hard cases 里仍有 `16` 条 rank bounds 不闭合，其中 `12` 条属于 `AA/BB`，`4` 条属于 `AB/BA`：

```text
AA/BB:
  0/2 = 11
  1/3 = 1

AB/BA:
  1/3 = 4
```

`ellrank(effort=2/3/4)` 都没收紧这 `16` 条。继续把 PARI effort 调大不是当前主线。
下一步要换 2-descent / Selmer / 模型化处理。

复现入口：

```text
results/mixed_closure_rank_summary.json
  uncertain_rank_rows
```

每条 residual 行都带 `model`、`root_number`、`sha2_lower`、`torsion_order`，可以直接转给
Sage / Magma / 后续 Selmer 工具。

### P1.1：AA/BB residual 已压成显式 2-cover 候选

已推进。

Sage Selmer 诊断和 PARI `ell2cover` 已把 `12` 条 `AA/BB` residual 从“rank bounds 不闭合”
进一步压成更具体的问题：

```text
12 AA/BB residual rows:
  Sage Selmer diagnostics: all ok
  PARI ell2cover probes: all ok
  covers_without_points_counts = {'2': 10, '3': 1, '4': 1}
  selmer_gap_alignment_counts = {'match': 12}
```

这里的 `selmer_gap` 指：

```text
selmer_rank_pari - torsion_two_dimension
```

普通话说：多出来的 Selmer 维数，正好对应 `ell2cover` 里高度 `100000` 内没找到点的 cover 数。
所以剩余问题不是散的 rank 黑箱，而是显式的 2-cover 无点候选。

复现命令：

```bash
uv run python scripts/theory/summarize_mixed_closure_residual_covers.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_aabb_residual_cover_summary.json
```

输出摘要：

```text
status_counts={'ok': 12}
covers_without_points_counts={'2': 10, '3': 1, '4': 1}
selmer_gap_alignment_counts={'match': 12}
evidence_level_counts={'bounded-search-no-point-candidate': 12}
```

跨文件证据审计入口：

```bash
uv run python scripts/theory/audit_mixed_closure_residual_evidence.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/mixed_closure_aabb_residual_evidence_audit.json \
  --strict
```

当前结果：

```text
target_rows=12
candidate_cover_total=27
violations=0
```

普通话说：这一步确认 `12` 条 AA/BB residual 在 rank summary、Sage Selmer、
PARI `ell2cover`、BSD 诊断四份文件里对得上；`27` 个 no-point cover 仍只标成
`candidate-not-proof`，没有被误升格成证明。

候选 cover 优先级表：

```bash
uv run python scripts/theory/prioritize_mixed_closure_residual_covers.py \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json \
  --out results/mixed_closure_aabb_residual_cover_priorities.json
```

当前结果：

```text
candidate_cover_total=27
top_target={'A': 115, 'B': 297, 'curve': 'AA', 'cover_index': 3}
```

前四个目标是：

```text
1. (115,297) AA cover 3, height 54060, BSD conditional rank 0
2. (115,297) AA cover 4, height 6281875, BSD conditional rank 0
3. (575,4641) AA cover 4, height 7095212, BSD conditional rank 0
4. (575,4641) AA cover 3, height 63929328, BSD conditional rank 0
```

普通话说：后续不要随机挑 cover 攻。先攻有 BSD 条件 rank 0 且 quartic 系数较小的目标；
这个排序只是工作队列，不是数学证明。

按优先级自动导出 top-4 handoff：

```bash
uv run python scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --top 4 \
  --out-dir results/mixed_closure_residual_handoffs
```

当前输出：

```text
wrote 2 priority handoff(s)
priority_001_115_297_AA_covers_3_4
priority_003_575_4641_AA_covers_4_3
```

第二组 handoff 的 Sage probe：

```bash
uv run python scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

结果同样是：

```text
status=ok
rank_bounds=[0, 2]
rank_proof_status=runtime-error
rank_probable=0
selmer_rank=4
torsion_two_dimension=2
cover_point_counts=[0, 0]
```

边界必须保留：

```text
PARI ell2cover 返回的是 everywhere locally soluble 2-covers。
hyperellratpoints 没找到点 != 严格证明 cover 无点。
当前只能叫 explicit Sha[2] candidate / 2-cover no-point candidate。
```

当前采集脚本已经保留每条 cover 的 quartic；重跑后还会保留 PARI 返回的
`covering_map_to_elliptic`。这使后续可以把具体 cover 交给 Magma / Cassels-Tate /
Brauer-Manin 方向，而不是只保留点数表。

下一步的严格化目标是从这些 no-point cover 中选最小代表，例如 `(115,297) AA` 的第 `3,4`
个 cover，尝试给出真正的无有理点证书。因为这些 cover 已经是局部处处可解，普通局部
obstruction 不是预期路线；更现实的是 Cassels-Tate/Brauer-Manin 解释、Mordell-Weil sieve、
或可引用的严格 rank/L-value 证书。

BSD/analytic-rank 条件性诊断入口：

```bash
uv run python scripts/theory/pari_bsd_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_bsd_mixed_aabb_t10.jsonl \
  --curve AA \
  --curve BB \
  --timeout 10
```

`timeout=10` 的真实结果：

```text
status_counts={'ok': 2, 'pari-error': 2, 'timeout': 8}
analytic_rank_counts={'0': 2}
```

成功的两条是 `(115,297) AA` 和 `(575,4641) AA`，都给出 `analytic_rank=0`。这只是
`bsd-conditional-diagnostic`，不是严格 rank 证书。`pari-error` 当前来自 PARI stack overflow；
加大到 `1GB` stack 后，`(567,3757) BB` 仍在 `20` 秒内超时。

论文数字一致性 gate：

```bash
uv run python scripts/theory/audit_closure_quotient_paper_claims.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --rank0-audit results/mixed_closure_rank0_certificate_audit.json \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --residual-evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json \
  --residual-local-witnesses results/mixed_closure_aabb_residual_local_witnesses.json \
  --priority-summary results/mixed_closure_aabb_residual_cover_priorities.json \
  --language-audit results/mixed_closure_residual_language_audit.json \
  --identity-audit results/mixed_closure_even_model_identity_audit.json \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/closure_quotient_paper_claim_audit.json \
  --expect rank0_torsion_certificates=275 \
  --expect strict_excluded_pair_count=220 \
  --expect rank0_aabb_rows=275 \
  --expect classification_detail_rows=275 \
  --expect classification_detail_point_count=550 \
  --expect cover_rows=12 \
  --expect cover_selmer_matches=12 \
  --expect residual_evidence_target_rows=12 \
  --expect residual_evidence_candidate_cover_total=27 \
  --expect residual_evidence_violations=0 \
  --expect residual_local_witness_candidate_cover_total=27 \
  --expect residual_local_witness_bad_prime_check_total=251 \
  --expect residual_local_witness_unresolved_bad_prime_total=0 \
  --expect residual_local_witness_all_bad_primes_witnessed=1 \
  --expect priority_candidate_cover_total=27 \
  --expect priority_top_a=115 \
  --expect priority_top_b=297 \
  --expect priority_top_cover_index=3 \
  --expect priority_top4_bsd_rank0_rows=4 \
  --expect language_audit_violations=0 \
  --expect language_audit_files=54 \
  --expect language_candidate_not_proof_hits=7 \
  --expect language_sha2_candidate_hits=5 \
  --expect language_bounded_search_not_proof_hits=2 \
  --expect language_bsd_not_strict_certificate_hits=1 \
  --expect even_model_identities_verified=1 \
  --expect bsd_ok_rows=2 \
  --expect bsd_analytic_rank0_rows=2 \
  --strict
```

当前结果：

```text
mismatches=0
```

这只检查 stored result files 和 paper-level 数字声明的一致性，不产生新的数学证书。
它现在也检查全量 residual local witness 数字：`27` 个候选 cover、`251` 个坏素数检查、
`0` 个未解决坏素数，以及 `all_bad_primes_witnessed=1`。

residual 语言边界审计：

```bash
uv run python scripts/theory/audit_mixed_closure_residual_language.py \
  --path docs/CLOSURE_QUOTIENT_MAINLINE.md \
  --path docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md \
  --path docs/work-logs/304-mixed-closure-residual-evidence-audit.md \
  --path docs/work-logs/305-sage-residual-handoff-probe.md \
  --path docs/work-logs/306-mixed-residual-cover-priority-queue.md \
  --path docs/work-logs/307-priority-handoff-export-and-second-sage-probe.md \
  --path docs/work-logs/308-priority-queue-paper-claim-gate.md \
  --path docs/work-logs/322-bsd-conditional-no-point-audit.md \
  --path docs/work-logs/323-residual-open-frontier-audit.md \
  --path docs/work-logs/324-rank-zero-frontier-queue.md \
  --path docs/work-logs/325-non-rankzero-frontier-queue.md \
  --path docs/work-logs/326-rank1-frontier-recheck.md \
  --path docs/work-logs/327-even-gap4-frontier-recheck.md \
  --path docs/work-logs/328-rankzero-frontier-recheck-567-3757.md \
  --path docs/work-logs/329-rankzero-frontier-recheck-5075-17901.md \
  --path docs/work-logs/330-rankzero-frontier-long-recheck-1625-5643.md \
  --path docs/work-logs/331-rankzero-frontier-recheck-8075-8613.md \
  --path docs/work-logs/332-rankzero-frontier-recheck-391-9009.md \
  --path docs/work-logs/333-rankzero-frontier-recheck-209-21735.md \
  --path docs/work-logs/334-rankzero-frontier-recheck-5083-12825.md \
  --path docs/work-logs/335-rankzero-frontier-recheck-5301-38675.md \
  --path docs/work-logs/336-residual-frontier-strategy-audit.md \
  --path docs/work-logs/337-frontier-target-handoff-1625-5643.md \
  --path docs/work-logs/338-all-rankzero-frontier-handoffs.md \
  --path docs/work-logs/339-non-rankzero-frontier-handoffs.md \
  --path docs/work-logs/340-frontier-handoff-audit.md \
  --path docs/work-logs/341-frontier-strictification-queue.md \
  --path docs/work-logs/342-frontier-strictification-attempt.md \
  --path docs/work-logs/343-frontier-rank-method-probe.md \
  --path docs/work-logs/344-frontier-batch-rank-method-probe.md \
  --path docs/work-logs/345-frontier-next-action-audit.md \
  --path docs/work-logs/346-rankzero-frontier-long-recheck-567-3757.md \
  --path docs/work-logs/347-rankzero-frontier-long-recheck-5075-17901.md \
  --path docs/work-logs/348-rankzero-frontier-long-recheck-8075-8613.md \
  --path docs/work-logs/349-rankzero-frontier-long-recheck-391-9009.md \
  --path docs/work-logs/350-rankzero-frontier-long-recheck-209-21735.md \
  --path docs/work-logs/351-rankzero-frontier-long-recheck-5083-12825.md \
  --path docs/work-logs/352-rankzero-frontier-long-recheck-5301-38675.md \
  --path docs/work-logs/353-frontier-escalation-queue.md \
  --path docs/work-logs/354-mwrank-frontier-rank-probe.md \
  --path docs/work-logs/355-sage-cover-tool-capability-audit.md \
  --path docs/work-logs/356-external-cover-descent-route-audit.md \
  --path docs/work-logs/357-external-cover-certificate-intake.md \
  --path docs/work-logs/358-frontier-external-certificate-intake.md \
  --path docs/work-logs/359-summary-gate-external-certificate-intake.md \
  --path docs/work-logs/360-paper-structure-audit.md \
  --path docs/work-logs/361-partial-result-dependency-audit.md \
  --path docs/work-logs/362-external-cover-descent-packages.md \
  --path docs/work-logs/363-closure-quotient-ray-ledger.md \
  --path docs/work-logs/364-closure-quotient-lambda-frontier.md \
  --path docs/work-logs/365-closure-quotient-ray-scale-invariance.md \
  --path docs/work-logs/366-rank-zero-family-candidates.md \
  --path docs/work-logs/367-rank-zero-primitive-models.md \
  --path docs/work-logs/368-root-number-lambda-triage.md \
  --out results/mixed_closure_residual_language_audit.json \
  --strict
```

当前结果：

```text
files=54
violations=0
required_boundary_hits={
  'candidate_not_proof': 7,
  'sha2_candidate': 5,
  'bounded_search_not_proof': 2,
  'bsd_not_strict_certificate': 1
}
```

这一步只审计措辞，防止把 bounded search / BSD 条件诊断 / Sha[2] candidate 写成证明。

residual frontier 策略审计：

```bash
uv run python scripts/theory/audit_mixed_closure_residual_frontier_strategy.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --out results/mixed_closure_residual_frontier_strategy_audit.json \
  --strict
```

当前结果：

```text
short_sage_retry_status=exhausted-without-proof
short_sage_retry_target_count=10
short_sage_retry_timeout_target_count=10
strict_promotion_count=0
next_strategy_counts={
  'external_rank_proof_or_cover_level_descent': 8,
  'rank1_generator_or_sha2_separation': 1,
  'even_gap4_deeper_descent_or_sha2_obstruction': 1
}
```

这一步只做 proof-work 路由：短时 Sage 队列已经扫完，但没有产生严格证明。

frontier handoff 内容审计：

```bash
uv run python scripts/theory/audit_mixed_closure_frontier_handoffs.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out results/mixed_closure_frontier_handoff_audit.json \
  --strict
```

当前结果：

```text
status=ok
handoff_group_count=10
target_cover_count=23
map_verified_group_count=10
local_witnessed_group_count=10
bounded_probe_group_count=10
strict_promotion_count=0
missing_files=[]
violations=[]
```

这一步检查 10 个 frontier handoff 包的内容是否和队列一致。它仍然不是无点证明；
`bounded_probe_group_count=10` 的意思只是 bounded Sage probe 已经复跑并留下诊断。

frontier strictification queue：

```bash
uv run python scripts/theory/summarize_mixed_closure_frontier_strictification.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --out results/mixed_closure_frontier_strictification_queue.json \
  --strict
```

当前结果：

```text
status=ok
target_count=10
cover_count=23
track_counts={'even-gap4-deeper-descent': 1, 'rank-one-sha2-separation': 1, 'rank-zero-rank-proof': 8}
strict_certificate_ready_count=0
first_target={'A': 1625, 'B': 5643, 'curve': 'AA', 'track': 'rank-zero-rank-proof', 'priorities': [5, 7], 'cover_indices': [3, 4]}
```

普通话说：这一步把“下一步怎么严谨收敛”排成队列。它不证明任何新 cover 无点；
它只说明每个目标需要什么严格证据才允许升级。

第一目标 strictification attempt ledger：

```bash
uv run python scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --probe sage-twodescent20:results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json \
  --probe sage-rank-methods-t90:results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json \
  --probe mwrank-default-1625:results/priority_005_1625_5643_AA_mwrank_rank_probe.json \
  --probe mwrank-b20-x30-t60-1625:results/priority_005_1625_5643_AA_mwrank_b20_x30_t60_probe.json \
  --probe mwrank-default-567:results/priority_006_567_3757_BB_mwrank_rank_probe.json \
  --probe mwrank-default-5075:results/priority_009_5075_17901_AA_mwrank_rank_probe.json \
  --probe mwrank-default-8075:results/priority_012_8075_8613_AA_mwrank_rank_probe.json \
  --probe mwrank-default-391:results/priority_013_391_9009_BB_mwrank_rank_probe.json \
  --probe mwrank-default-209-21735:results/priority_017_209_21735_BB_mwrank_rank_probe.json \
  --probe mwrank-default-5083-12825:results/priority_024_5083_12825_BB_mwrank_rank_probe.json \
  --probe mwrank-default-5301-38675:results/priority_025_5301_38675_BB_mwrank_rank_probe.json \
  --probe sage-rank-methods-t600-567:results/priority_006_567_3757_BB_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-5075:results/priority_009_5075_17901_AA_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-8075:results/priority_012_8075_8613_AA_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-391:results/priority_013_391_9009_BB_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-209-21735:results/priority_017_209_21735_BB_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-5083-12825:results/priority_024_5083_12825_BB_rank_methods_t600_twodescent40.json \
  --probe sage-rank-methods-t600-5301-38675:results/priority_025_5301_38675_BB_rank_methods_t600_twodescent40.json \
  --batch-probe rankzero-batch-t45:results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --out results/mixed_closure_frontier_strictification_attempt_audit.json \
  --strict
```

当前结果：

```text
status=ok
attempt_count=26
target_count_with_attempts=8
attempt_status_counts={'open-rank-bounds-not-proof': 7, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 3}
strict_certificate_ready_count=0
```

这记录了 `(1625,5643) AA` 的短 two-descent 尝试：180 秒预算内 timeout。
它不是 rank proof，也不是 cover no-point proof。

第一目标逐方法 rank probe：

```bash
uv run python scripts/theory/sage_probe_mixed_closure_rank_methods.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json \
  --sage sage \
  --timeout 90 \
  --method rank_bounds \
  --method rank_proof \
  --method selmer_rank \
  --method pari_ellrank \
  --method two_descent \
  --two-descent-second-limit 20 \
  --dot-sage /private/tmp/d19-dot-sage
```

当前结果：

```text
method_status_counts={'pari_ellrank:ok': 1, 'rank_bounds:ok': 1, 'rank_proof:runtime-error': 1, 'selmer_rank:ok': 1, 'two_descent:timeout': 1}
rank_zero_proof_candidate=False
```

普通话说：`rank_bounds`、PARI `ellrank=[0,2,0,[]]` 和 `selmer_rank`
这些诊断能跑通；严格 rank proof 没有出来，`two_descent` 在 90 秒内 timeout。

8 个 rank-zero frontier targets 的批量便宜 rank probe：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache DOT_SAGE=/private/tmp/d19-dot-sage uv run python scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --sage sage \
  --timeout 45 \
  --method rank_bounds \
  --method selmer_rank \
  --method pari_ellrank \
  --track rank-zero-rank-proof \
  --limit 8 \
  --dot-sage /private/tmp/d19-dot-sage \
  --strict
```

当前结果：

```text
status=ok
target_count=8
method_status_counts={'pari_ellrank:ok': 8, 'rank_bounds:ok': 8, 'selmer_rank:ok': 8}
rank_zero_proof_candidate_count=0
```

普通话说：8 个 rank-zero 目标全部仍是同一种开放形态：
`rank_bounds=[0,2]`、`selmer_rank=4`、PARI `ellrank=[0,2,0,[]]`。
这说明便宜诊断没有挑出已经闭合的目标；它仍然只是诊断，不是 rank-zero 证明。

frontier next-action audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_next_actions.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --batch-rank-methods results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --out results/mixed_closure_frontier_next_action_audit.json \
  --strict
```

当前结果：

```text
status=ok
cheap_rank_method_target_hopping_exhausted=True
rank_zero_rank_method_target_hopping_exhausted=True
recommended_mainline=escalate-beyond-cheap-rank-methods
```

普通话说：便宜 rank-method 的“换目标试一试”和 8 个 rank-zero 目标的同级
rank-method 长跑都已经收敛；下一步不应继续做同类加时，而应升级到更强 descent、
外部严格 rank proof、cover-level no-point certificate，以及 non-rankzero 两条专门路线。

frontier escalation queue：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_escalation_queue.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --next-action-audit results/mixed_closure_frontier_next_action_audit.json \
  --out results/mixed_closure_frontier_escalation_queue.json \
  --strict
```

当前结果：

```text
status=ok
target_count=10
cover_count=23
rank_zero_target_count=8
rank_zero_rank_method_target_hopping_exhausted=True
strict_certificate_ready_count=0
route_counts={'even-gap4-deeper-descent-or-cover-descent': 1, 'rank-one-generator-sha2-separation-or-cover-descent': 1, 'rank-zero-external-rank-proof-or-cover-descent': 8}
```

普通话说：这一步把“换证明武器”落成队列。8 个 rank-zero 目标走外部严格 rank proof
或逐 cover no-point certificate；1 个 rank-one 目标走 visible generator/Sha[2] 分离；
1 个 even-gap4 目标走 deeper descent 或独立 Sha[2] 障碍。它仍然不是证明。

Sage cover tool capability audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_sage_cover_tool_capabilities.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --sage sage \
  --timeout 30 \
  --strict
```

当前结果：

```text
status=ok
cover_count=2
genus_one_cover_count=2
sage_direct_no_point_capable_count=0
strict_certificate_ready_count=0
recommended_next_tool=magma-or-specialized-cover-descent
```

普通话说：Sage 能识别这些 quartic 是 genus-one cover，但这里只有有界找点接口，
没有直接 no-point 证明所需的 local/descent/Jacobian rank 接口。因此 cover-level
收敛下一步应转向 Magma 或专门的 Mordell-Weil sieve / cover descent。

External cover descent route audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_descent_route.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --sage-cover-capability-audit results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --out results/priority_005_1625_5643_AA_external_cover_descent_route.json \
  --magma magma \
  --strict
```

当前结果：

```text
status=ok
local_magma_available=False
proof_status=external-tool-gap-open
recommended_next_action=obtain-magma-or-specialized-cover-descent-environment
```

普通话说：这一步把“下一步该跑什么才算数”固定下来。本机没有 Magma，
Sage 当前也没有直接证书接口；所以下一份能推动证明的产物必须是外部
cover descent / Mordell-Weil sieve transcript，且需要给出逐 cover no-point
certificate，或把源椭圆 rank bounds 严格闭到 `[0,0]` 后再做 torsion-preimage audit。

External cover certificate intake：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_intake.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_external_cover_certificate_intake.json \
  --template-out results/priority_005_1625_5643_AA_external_cover_certificate_template.json \
  --strict
```

当前结果：

```text
status=ok
certificate_package_ready=False
strict_promotion_ready=False
```

普通话说：现在还没有外部 no-point 证书包。这个脚本生成未来证书包模板，
并检查目标、cover 覆盖、证书类型、结果字段和 transcript 文件是否齐全。
即使字段齐全，它也只把证书包标成“可审阅”，不自己验证外部数学。

Frontier external cover certificate intake：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_frontier_intake.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --certificate-dir results/mixed_closure_external_certificates \
  --out results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --template-index-out results/mixed_closure_external_cover_certificate_template_index.json \
  --strict
```

当前结果：

```text
status=ok
target_count=10
cover_count=23
certificate_package_ready_count=0
strict_promotion_ready_count=0
```

普通话说：全部 residual frontier 现在都有统一外部证书入口。它覆盖 10 个目标、
23 个 cover；当前还没有任何外部证书包 ready，所以没有新的严格提升。

Paper structure audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_paper_structure.py \
  --paper docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md \
  --claim-audit results/closure_quotient_paper_claim_audit.json \
  --residual-open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --frontier-strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --external-certificate-frontier-audit results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --out results/closure_quotient_paper_structure_audit.json \
  --strict
```

当前结果：

```text
status=ok
matched_section_count=5
matched_claim_count=14
```

普通话说：这只检查论文稿结构和关键边界文字是否到位，不验证数学。

partial-result 总摘要：

```bash
uv run python scripts/theory/summarize_closure_quotient_partial_result.py \
  --claim-audit results/closure_quotient_paper_claim_audit.json \
  --language-audit results/mixed_closure_residual_language_audit.json \
  --priority-summary results/mixed_closure_aabb_residual_cover_priorities.json \
  --priority-handoff-audit results/mixed_closure_priority_handoff_audit_top4.json \
  --residual-local-witnesses results/mixed_closure_aabb_residual_local_witnesses.json \
  --selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json \
  --residual-cover-map-verify results/mixed_closure_residual_cover_map_verify.json \
  --rank0-torsion-preimage-audit results/mixed_closure_rank0_sha2_torsion_preimage_audit.json \
  --bsd-conditional-no-point-audit results/mixed_closure_bsd_conditional_no_point_audit.json \
  --residual-open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --rank-zero-frontier-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-frontier-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --residual-frontier-strategy-audit results/mixed_closure_residual_frontier_strategy_audit.json \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --frontier-strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --frontier-strictification-attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --frontier-next-action-audit results/mixed_closure_frontier_next_action_audit.json \
  --external-certificate-frontier-audit results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --paper-structure-audit results/closure_quotient_paper_structure_audit.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --out results/closure_quotient_partial_result_summary.json \
  --strict
```

当前结果：

```text
ready_for_partial_result=True
blocking_issues=[]
strict_certificate.rank0_torsion_certificates=275
strict_certificate.strict_excluded_pair_count=220
residual_status.candidate_cover_total=27
priority_handoff_status.ready=True
priority_handoff_status.groups_checked=2
priority_handoff_status.target_cover_count=4
priority_handoff_status.map_verified_groups=2
priority_handoff_status.local_witnessed_groups=2
residual_local_witness_status.candidate_cover_total=27
residual_local_witness_status.bad_prime_check_total=251
residual_local_witness_status.unresolved_bad_prime_total=0
residual_selmer_gap_status.candidate_cover_total=27
residual_selmer_gap_status.rows_with_ok_diagnostics=27
residual_selmer_gap_status.rank0_sha2_gap2_cover_total=20
residual_selmer_gap_status.gap_type_counts={'even-rank-sha2-gap4-open': 4, 'rank0-sha2-gap2': 20, 'rank1-sha2-gap2-open': 3}
residual_cover_map_status.target_cover_count=27
residual_cover_map_status.verified_cover_count=27
residual_cover_map_status.failed_cover_count=0
rank0_torsion_preimage_status.target_cover_count=20
rank0_torsion_preimage_status.no_torsion_preimage_count=20
rank0_torsion_preimage_status.failed_cover_count=0
rank0_torsion_preimage_status.conditional_on_rank_zero=True
bsd_conditional_no_point_status.bsd_conditional_no_point_cover_count=4
bsd_conditional_no_point_status.rank0_sha2_gap2_cover_count=20
bsd_conditional_no_point_status.strict_no_point_cover_count=0
bsd_conditional_no_point_status.candidate_not_proof=True
bsd_conditional_no_point_status.proof_status=conditional-not-proof
residual_open_frontier_status.candidate_cover_total=27
residual_open_frontier_status.conditional_no_point_cover_count=4
residual_open_frontier_status.open_frontier_cover_count=23
residual_open_frontier_status.open_frontier_type_counts={'even-rank-gap4-needs-deeper-descent': 4, 'rank-zero-needs-rank-proof': 16, 'rank1-needs-visible-generator-or-descent': 3}
residual_open_frontier_status.strict_no_point_cover_count=0
residual_open_frontier_status.proof_status=open-frontier-not-proof
rank_zero_frontier_status.rank_zero_frontier_cover_count=16
rank_zero_frontier_status.rank_zero_frontier_target_count=8
rank_zero_frontier_status.closed_rank_zero_target_count=0
rank_zero_frontier_status.target_status_counts={'sage-timeout': 8}
rank_zero_frontier_status.proof_status=rank-proof-frontier-not-proof
non_rankzero_frontier_status.non_rankzero_frontier_cover_count=7
non_rankzero_frontier_status.non_rankzero_frontier_target_count=2
non_rankzero_frontier_status.target_type_counts={'even-rank-gap4-needs-deeper-descent': 1, 'rank1-needs-visible-generator-or-descent': 1}
non_rankzero_frontier_status.target_status_counts={'sage-timeout': 2}
non_rankzero_frontier_status.proof_status=non-rankzero-frontier-not-proof
residual_frontier_strategy_status.short_sage_retry_status=exhausted-without-proof
residual_frontier_strategy_status.short_sage_retry_target_count=10
residual_frontier_strategy_status.short_sage_retry_timeout_target_count=10
residual_frontier_strategy_status.strict_promotion_count=0
residual_frontier_strategy_status.next_strategy_counts={'even_gap4_deeper_descent_or_sha2_obstruction': 1, 'external_rank_proof_or_cover_level_descent': 8, 'rank1_generator_or_sha2_separation': 1}
residual_frontier_strategy_status.proof_status=strategy-not-proof
frontier_handoff_status.ready=True
frontier_handoff_status.handoff_group_count=10
frontier_handoff_status.target_cover_count=23
frontier_handoff_status.map_verified_group_count=10
frontier_handoff_status.local_witnessed_group_count=10
frontier_handoff_status.bounded_probe_group_count=10
frontier_handoff_status.strict_promotion_count=0
frontier_handoff_status.proof_status=handoff-not-proof
frontier_strictification_status.ready=True
frontier_strictification_status.target_count=10
frontier_strictification_status.cover_count=23
frontier_strictification_status.track_counts={'even-gap4-deeper-descent': 1, 'rank-one-sha2-separation': 1, 'rank-zero-rank-proof': 8}
frontier_strictification_status.strict_certificate_ready_count=0
frontier_strictification_status.proof_status=strictification-queue-not-proof
frontier_strictification_attempt_status.ready=True
frontier_strictification_attempt_status.attempt_count=26
frontier_strictification_attempt_status.target_count_with_attempts=8
frontier_strictification_attempt_status.attempt_status_counts={'open-rank-bounds-not-proof': 7, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 3}
frontier_strictification_attempt_status.strict_certificate_ready_count=0
frontier_strictification_attempt_status.proof_status=attempt-ledger-not-proof
frontier_next_action_status.ready=True
frontier_next_action_status.cheap_rank_method_target_hopping_exhausted=True
frontier_next_action_status.rank_zero_rank_method_target_hopping_exhausted=True
frontier_next_action_status.recommended_mainline=escalate-beyond-cheap-rank-methods
frontier_next_action_status.proof_status=next-action-routing-not-proof
external_certificate_frontier_status.ready=True
external_certificate_frontier_status.target_count=10
external_certificate_frontier_status.cover_count=23
external_certificate_frontier_status.certificate_package_ready_count=0
external_certificate_frontier_status.missing_certificate_package_count=10
external_certificate_frontier_status.strict_promotion_ready_count=0
external_certificate_frontier_status.proof_status=frontier-external-certificates-missing-not-proof
paper_structure_status.ready=True
paper_structure_status.matched_section_count=5
paper_structure_status.matched_claim_count=14
paper_structure_status.missing_claim_count=0
artifact_status.ready=True
artifact_status.required_file_count=318
artifact_status.missing_file_count=0
residual_status.proof_status=candidate-not-proof
```

Root-number lambda triage：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_root_number_lambda_triage.json \
  --strict
```

当前结果：

```text
target_class_count=148
target_pair_count=156
family_exclusion_proved_count=0
```

普通话说：这一步只给 `observed-open` 比例类做 root-number / rank-key 分流。
root number 不是证明，只用来决定下一步应该尝试哪种整族 rank/descent 问题。

Rank-zero primitive model index：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py \
  --candidates results/closure_quotient_rank_zero_family_candidates.json \
  --out results/closure_quotient_rank_zero_primitive_models.json \
  --strict
```

当前结果：

```text
candidate_class_count=200
model_count=243
model_counts_by_curve={'AA': 125, 'BB': 118}
family_exclusion_proved_count=0
```

普通话说：这一步把 200 个候选比例类落成 243 个本原 AA/BB 模型，
记录 `p,q,sqrt_q,weierstrass_model`。后续整族 rank-zero 证明应从这些本原模型入手。

Rank-zero family candidate list：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_rank_zero_family_candidates.json \
  --strict
```

当前结果：

```text
candidate_class_count=200
strict_observed_pair_count=220
family_exclusion_proved_count=0
certifying_curve_pattern_counts={'AA': 125, 'BB': 118}
```

普通话说：这一步把 200 个 `rank-zero-family-generalization` 类具体列出来，
并标明是 `AA`、`BB` 还是两者都给出局部 rank-zero 机制。它仍然只是整族证明候选清单。

Ray scale-invariance audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_ray_scale_invariance.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/closure_quotient_ray_scale_invariance_audit.json \
  --strict
```

当前结果：

```text
observed_ray_count=356
multi_scale_ray_count=14
coefficient_identity_verified_count=1536
coefficient_identity_violation_count=0
rank_key_consistent_group_count=56
rank_key_inconsistent_group_count=0
```

普通话说：若 `(A,B)=d(a,b)`，则四次商曲线通过 `N=d n, y=d^2 y0`
同构到本原 ray 的曲线；系数满足 `coeff_scaled[N^i]=d^(4-i)*coeff_primitive[n^i]`。
所以同一个本原 ray 上继续增加 scale 样本，不应算作新的结构进展。

Lambda frontier：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_lambda_frontier.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_lambda_frontier.json \
  --strict
```

当前结果：

```text
lambda_class_count=356
track_counts={
  'rank-zero-family-generalization': 200,
  'root-number-rank-structure-triage': 148,
  'two-cover-or-reviewable-no-point-certificate': 8
}
family_exclusion_proved_count=0
```

普通话说：这是后续 `lambda=A/B` 层面的任务队列，不是证明。以后主进展只算
整族 rank-zero 机制、严格 root-number/parity + rank/descent 论证、整族 2-cover/Selmer
障碍，或者可审阅的 cover-level no-point 证书。

Ray ledger / `c_-/c_+` 收尾：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_ray_ledger.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --rank-summary results/mixed_closure_rank_summary.json \
  --residual-cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --out results/closure_quotient_ray_ledger.json \
  --strict
```

当前结果：

```text
pair_count=384
primitive_ray_count=356
c_ratio_class_count=356
strict_c_ratio_class_count=200
residual_candidate_pair_count=8
```

普通话说：这里补上 `c_- = |A-B|`，并按本原比例 `A:B` 建 ledger。
`c_+/c_-` 识别的是无向比例类 `{A:B, B:A}`，不能单独区分 `lambda` 和 `1/lambda`。
所以它是比例类索引，不是整族证明。后续主线应研究哪些 `lambda` 类能被 rank-zero /
root-number / 2-cover 机制整族排除；剩余类只接受可审阅的 no-point 证书。

External cover-descent package export：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/export_external_cover_descent_packages.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out-dir results/mixed_closure_external_cover_descent_packages \
  --out results/mixed_closure_external_cover_descent_package_index.json \
  --strict
```

当前结果：

```text
status=ok
target_count=10
cover_count=23
strict_certificate_ready_count=0
```

Partial-result dependency audit：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_partial_dependencies.py \
  --summary results/closure_quotient_partial_result_summary.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --root . \
  --out results/closure_quotient_partial_dependency_audit.json \
  --strict
```

当前结果：

```text
status=ok
dependency_count=8
missing_summary_statuses=0
```

普通话说：这表示“partial result 证据包和措辞边界已经自洽”。其中 4 个 cover 现在是 BSD 条件下最强的无点候选；
但它们仍然不是严格无点证明，不能放进 strict certificate。剩余 23 个开放 cover
现在也被分桶成“差 rank-zero 证明”的 16 个、“rank-one 分离问题”的 3 个、
以及“even rank gap4 deeper descent”的 4 个。其中 16 个 rank-zero cover
又合并成 8 个 rank 证明目标；`(1625,5643) AA`、`(567,3757) BB`、`(5075,17901) AA`、
`(8075,8613) AA`、`(391,9009) BB`、`(209,21735) BB`、`(5083,12825) BB` 和 `(5301,38675) BB`
已做 Sage `second_limit=13,20`、120 秒重试，结果都是 timeout。最高优先级
`(1625,5643) AA` 又用 `second_limit=20,40`、600 秒预算重试，仍然 timeout。
这些都没有产生严格 rank-zero 证明。
另外 7 个非 rank-zero cover 合并成 2 个目标：`(209,5355) BB` 的 rank1/Sha[2]
分离目标，以及 `(1449,12155) BB` 的 even gap4 deeper descent 目标。`(209,5355) BB`
已做 Sage `second_limit=13,20`、120 秒重试，结果 timeout，没有产生 rank bounds
闭合或 cover-level 证明。`(1449,12155) BB` 也已用同样预算重试，结果 timeout；
因此 2 个非 rank-zero elliptic targets 都已记录为 Sage timeout，仍需要更强
descent 工具或 cover-level 证明。
策略审计把这 10 个 frontier targets 统一标记为 `exhausted-without-proof`：
这不是说 residual 已证明无点，而是说“短时 Sage 重试队列”已经不再是剩余工作；
后续应转向外部 rank proof、visible-rank 分离、deeper descent 或 cover-level `Sha[2]`
阻碍证明。
第一个外部 rank/cover-level 目标 `(1625,5643) AA` 已导出 handoff：
cover `4,3` 的 maps 在 Sage 中验证通过，bad-prime local witnesses 全部找到，
bounded handoff probe 仍为 `rank_bounds=[0,2]` 且 `rank_proof_status=runtime-error`。
这只是高质量交接材料，不是 residual no-point proof。
随后 8 个 rank-zero frontier targets 全部完成同格式 handoff：每个目标都有
JSON/Sage/Magma handoff、map verification、bad-prime local witness probe 和 bounded
Sage handoff probe。共同状态仍是 `strict_proof_status=open`、
`rank_bounds=[0,2]`、`rank_proof_status=runtime-error`、`cover_point_counts=[0,0]`。
两个 non-rank-zero frontier targets 也完成同格式 handoff。`(209,5355) BB`
保持 `rank_bounds=[1,3]`，对应 rank-one/Sha[2] 分离问题；`(1449,12155) BB`
保持 `rank_bounds=[0,4]`，对应 even gap4 deeper descent 问题。二者 maps 验证通过、
bad-prime local witnesses 全部找到，但仍没有 cover-level no-point proof。
frontier handoff 内容审计现在把这些 10 个 handoff group、23 个 cover 统一检查为
`handoff-not-proof`，并确认没有 strict promotion。
strictification queue 进一步把这 10 个目标排成可攻队列：先攻 `(1625,5643) AA`
的 rank-zero proof 或 cover-level no-point certificate；另外保留 1 个 rank-one/Sha[2]
分离目标和 1 个 even gap4 deeper descent 目标。
第一条实际 attempt 已记录：`sage-twodescent20` 在 180 秒预算内 timeout，所以
`strict_certificate_ready_count=0` 仍保持不变。
随后逐方法 probe 显示 `rank_bounds`、PARI `ellrank` 与 `selmer_rank` 可计算，
但 `rank_proof` 仍为 runtime-error，`two_descent` 在 90 秒预算内 timeout。
再随后，对全部 8 个 rank-zero frontier targets 批量跑 `rank_bounds`、`selmer_rank`
和 PARI `ellrank`，全部完成，但全部保持 `rank_bounds=[0,2]`、
`selmer_rank=4`、PARI `ellrank=[0,2,0,[]]`，没有任何
`rank_zero_proof_candidate`。

目标 cover handoff：

```bash
uv run python scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_115_297_AA_h100000_with_maps.jsonl \
  --bsd results/pari_bsd_mixed_115_297_AA.jsonl \
  --target 115,297,AA \
  --cover-index 3 \
  --cover-index 4 \
  --out-dir results/mixed_closure_residual_handoffs \
  --name 115_297_AA_covers_3_4
```

输出：

```text
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.sage
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.magma
```

Sage 文件已在本地验证能构造目标 cover。Magma 本地未安装，所以 `.magma` 文件只是 handoff 草案，
不是已验证 transcript。

Sage handoff probe：

```bash
uv run python scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

当前结果：

```text
status=ok
rank_bounds=[0, 2]
rank_proof_status=runtime-error
rank_probable=0
selmer_rank=4
torsion_two_dimension=2
cover_point_counts=[0, 0]
```

Sage 明确提示：

```text
This could be because Sha(E/Q)[2] is nontrivial.
```

也就是说，Sage 的严格 rank 证明接口没有关掉这条 residual，反而把它定位到当前主线正在追的
`Sha[2] / 2-cover` 障碍。带 `--two-descent-second-limit 13` 的同一 probe 在 `45` 秒预算下
超时；这说明 second descent 暂时不是一个稳定快速的本地证书入口。

### P2：解释 `AB/BA` 无 rank 0

两批样本中 `AB/BA` 全部 rank 正。需要判断这是偶然，还是闭合结构强迫。

`AB/BA` 的 rank 正不是黑箱现象。它们有两个通用仿射点：

```text
AB:
  N=A, y=2AB
  N=B, y=A^2+B^2

BA:
  N=A, y=A^2+B^2
  N=B, y=2AB
```

这些点来自闭合端点互换，不要求四个平方条件全成立。它们说明 `AB/BA` 本来就带着稳定的有理点，
所以把 `AB` 当 rank-0 击杀器的押注应降级。

更强的是，`AB/BA` 共享同一条 Weierstrass 模型：

```text
E_mix: Y^2 = X^3 + C X^2 - D X - CD
C = 2(A^2 + AB + B^2)
D = (2AB)^2
```

它上面有显式点：

```text
P_mix = (-(A^2+B^2), (A+B)^2(B-A))
```

对特化 `(A,B)=(7,45)`，PARI 验证 `P_mix` 在曲线上且 `ellorder(P_mix)=0`。因此
`P_mix` 不可能是泛族 torsion 点；否则每个好特化都会给 torsion 点。

当前两批样本的 `384` 个 distinct pair 中，这个点全部验证为 `ellorder=0`。所以
`AB/BA rank=0` 路线应正式降级：`AB/BA` 主要提供结构解释，不提供当前严格排除证书。

### P3：把 `AA/BB rank=0` 写成论文级引理

已推进到主文档引理草案，见 §3.1。

还要收紧的只是论文写法，不是代码证据：

- 把非奇异条件单独列出；
- 把 `X=-p` 对应四次曲线无穷远点写进证明；
- 把“没有 full-closed square 点”与“全部是中点”分开陈述，避免把中点-only 当成必要条件。

### P4：决定是否接入 `proof_status`

当前 partial-result 阶段不默认接入 `proof_status`。

原因：

- `AA/BB rank=0` 是严格证书，但需要 PARI rank 认证和 torsion 回拉；
- `proof_status` 现在的主流程更适合低成本、批量、稳定顺序的 pair 级筛；
- `AB/BA` 已降级，不提供 rank-zero 判据；
- 16 条 rank bounds 不闭合，已经确认不能靠提高 PARI effort 收掉。

所以当前收敛口径是：

```text
closure quotient = 离线严格证书工具
proof_status = 暂不默认调用 closure quotient
```

以后若要接入，应先设计 pair-level certificate 字段，再只接受下面这种结果：

```text
AA/BB rank=0
torsion certificate status = certified
certifies_no_full_closed_square = true
```

可选接法：

```text
factor_concordant / GEN-CLOSURE 后
  -> rank_mixed_closure_curves
  -> only when AA/BB rank=0 and torsion certificate says no full closed square
```

## 6. 主线停止条件

这条线继续推进时，必须设置停止条件。

可以继续的信号：

- `AA/BB rank=0` 覆盖越来越多 hard/residual pair；
- 不确定 rank bounds 能被 Selmer 收紧；
- `AB/BA` 出现可解释的结构，而不是只给分布表。

应该降级为辅助工具的信号：

- `AA/BB rank=0` 覆盖率停在小子集；
- `AB/BA` 被证明一般正秩；
- P1 的不确定 rank 需要重型工具但收益很小。

## 7. 入口清单

代码：

- `src/rational_distance/concordant/mixed_closure_curves.py`
- `scripts/theory/rank_mixed_closure_curves.py`
- `scripts/theory/sage_recheck_mixed_closure_residuals.py`
- `scripts/theory/sage_diagnose_mixed_closure_residuals.py`
- `scripts/theory/pari_ell2cover_mixed_residuals.py`
- `scripts/theory/summarize_mixed_closure_residual_covers.py`
- `scripts/theory/audit_mixed_closure_rank0_certificates.py`
- `scripts/theory/pari_bsd_mixed_closure_residuals.py`
- `scripts/theory/audit_mixed_closure_residual_evidence.py`
- `scripts/theory/audit_closure_quotient_paper_claims.py`
- `scripts/theory/export_mixed_closure_residual_handoff.py`
- `scripts/theory/sage_probe_mixed_closure_handoff.py`
- `scripts/theory/sage_verify_mixed_closure_handoff_maps.py`
- `scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py`
- `scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py`
- `scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py`
- `scripts/theory/audit_mixed_closure_residual_open_frontier.py`
- `scripts/theory/summarize_mixed_closure_rank_zero_frontier.py`
- `scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py`
- `scripts/theory/audit_mixed_closure_residual_frontier_strategy.py`
- `scripts/theory/audit_mixed_closure_frontier_handoffs.py`
- `scripts/theory/summarize_mixed_closure_frontier_strictification.py`
- `scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py`
- `scripts/theory/sage_probe_mixed_closure_rank_methods.py`
- `scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py`
- `scripts/theory/audit_mixed_closure_frontier_next_actions.py`
- `scripts/theory/audit_mixed_closure_frontier_escalation_queue.py`
- `scripts/theory/probe_mwrank_mixed_closure_rank.py`
- `scripts/theory/audit_sage_cover_tool_capabilities.py`
- `scripts/theory/audit_external_cover_descent_route.py`
- `scripts/theory/audit_external_cover_certificate_intake.py`
- `scripts/theory/audit_external_cover_certificate_frontier_intake.py`
- `scripts/theory/export_external_cover_descent_packages.py`
- `scripts/theory/sage_probe_mixed_closure_local_witnesses.py`
- `scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py`
- `scripts/theory/prioritize_mixed_closure_residual_covers.py`
- `scripts/theory/audit_mixed_closure_residual_language.py`
- `scripts/theory/audit_mixed_closure_priority_handoffs.py`
- `scripts/theory/audit_closure_quotient_paper_structure.py`
- `scripts/theory/audit_closure_quotient_partial_dependencies.py`
- `scripts/theory/summarize_closure_quotient_ray_ledger.py`
- `scripts/theory/summarize_closure_quotient_lambda_frontier.py`
- `scripts/theory/audit_closure_quotient_ray_scale_invariance.py`
- `scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py`
- `scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py`
- `scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py`
- `scripts/theory/summarize_closure_quotient_partial_result.py`
- `scripts/theory/audit_mixed_closure_even_model_identities.py`
- `scripts/theory/audit_closure_quotient_partial_artifacts.py`

测试：

- `tests/test_mixed_closure_curves.py`
- `tests/test_mixed_closure_rank_cli.py`
- `tests/test_sage_recheck_mixed_closure_residuals.py`
- `tests/test_sage_diagnose_mixed_closure_residuals.py`
- `tests/test_pari_ell2cover_mixed_residuals.py`
- `tests/test_mixed_closure_residual_cover_summary.py`
- `tests/test_mixed_closure_rank0_certificate_audit.py`
- `tests/test_pari_bsd_mixed_closure_residuals.py`
- `tests/test_mixed_closure_residual_evidence_audit.py`
- `tests/test_closure_quotient_paper_claim_audit.py`
- `tests/test_mixed_closure_residual_handoff.py`
- `tests/test_sage_probe_mixed_closure_handoff.py`
- `tests/test_sage_verify_mixed_closure_handoff_maps.py`
- `tests/test_sage_verify_mixed_closure_residual_cover_maps.py`
- `tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py`
- `tests/test_mixed_closure_bsd_conditional_no_point_audit.py`
- `tests/test_mixed_closure_residual_open_frontier_audit.py`
- `tests/test_mixed_closure_rank_zero_frontier_queue.py`
- `tests/test_mixed_closure_non_rankzero_frontier_queue.py`
- `tests/test_mixed_closure_residual_frontier_strategy.py`
- `tests/test_mixed_closure_frontier_handoff_audit.py`
- `tests/test_mixed_closure_frontier_strictification_queue.py`
- `tests/test_mixed_closure_frontier_strictification_attempts.py`
- `tests/test_sage_probe_mixed_closure_rank_methods.py`
- `tests/test_batch_sage_probe_mixed_closure_rank_methods.py`
- `tests/test_mixed_closure_frontier_next_action_audit.py`
- `tests/test_mixed_closure_frontier_escalation_queue.py`
- `tests/test_probe_mwrank_mixed_closure_rank.py`
- `tests/test_audit_sage_cover_tool_capabilities.py`
- `tests/test_audit_external_cover_descent_route.py`
- `tests/test_audit_external_cover_certificate_intake.py`
- `tests/test_audit_external_cover_certificate_frontier_intake.py`
- `tests/test_export_external_cover_descent_packages.py`
- `tests/test_sage_probe_mixed_closure_local_witnesses.py`
- `tests/test_mixed_closure_residual_selmer_gap_ledger.py`
- `tests/test_prioritize_mixed_closure_residual_covers.py`
- `tests/test_mixed_closure_residual_language_audit.py`
- `tests/test_mixed_closure_priority_handoff_audit.py`
- `tests/test_closure_quotient_paper_structure_audit.py`
- `tests/test_closure_quotient_partial_dependency_audit.py`
- `tests/test_closure_quotient_ray_ledger.py`
- `tests/test_closure_quotient_lambda_frontier.py`
- `tests/test_closure_quotient_ray_scale_invariance.py`
- `tests/test_closure_quotient_rank_zero_family_candidates.py`
- `tests/test_closure_quotient_rank_zero_primitive_models.py`
- `tests/test_closure_quotient_root_number_lambda_triage.py`
- `tests/test_summarize_closure_quotient_partial_result.py`
- `tests/test_mixed_closure_even_model_identity_audit.py`
- `tests/test_closure_quotient_partial_artifacts.py`

结果：

- `results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl`
- `results/mixed_closure_localglobal_residual64_pairs.jsonl`
- `results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl`
- `results/mixed_closure_rank_summary.json`
- `results/sage_mixed_closure_residual_recheck_limit13.jsonl`
- `results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl`
- `results/pari_ell2cover_mixed_aabb_h100000.jsonl`
- `results/mixed_closure_aabb_residual_cover_summary.json`
- `results/mixed_closure_aabb_residual_evidence_audit.json`
- `results/mixed_closure_aabb_residual_cover_priorities.json`
- `results/mixed_closure_aabb_residual_local_witnesses.json`
- `results/mixed_closure_residual_selmer_gap_ledger.json`
- `results/mixed_closure_residual_cover_map_verify.json`
- `results/mixed_closure_rank0_sha2_torsion_preimage_audit.json`
- `results/mixed_closure_bsd_conditional_no_point_audit.json`
- `results/mixed_closure_residual_open_frontier_audit.json`
- `results/sage_rankzero_frontier_recheck_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_1625_5643_AA_s20_40_t600.jsonl`
- `results/sage_rankzero_frontier_recheck_567_3757_BB_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_5075_17901_AA_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_8075_8613_AA_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_391_9009_BB_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_209_21735_BB_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_5083_12825_BB_s13_20_t120.jsonl`
- `results/sage_rankzero_frontier_recheck_5301_38675_BB_s13_20_t120.jsonl`
- `results/sage_rank1_frontier_recheck_209_5355_BB_s13_20_t120.jsonl`
- `results/sage_even_gap4_frontier_recheck_1449_12155_BB_s13_20_t120.jsonl`
- `results/mixed_closure_rank_zero_frontier_queue.json`
- `results/mixed_closure_non_rankzero_frontier_queue.json`
- `results/mixed_closure_residual_frontier_strategy_audit.json`
- `results/mixed_closure_frontier_handoff_audit.json`
- `results/mixed_closure_frontier_strictification_queue.json`
- `results/mixed_closure_frontier_strictification_attempt_audit.json`
- `results/priority_005_1625_5643_AA_covers_4_3_twodescent20_probe.json`
- `results/priority_005_1625_5643_AA_rank_methods_t90_twodescent20.json`
- `results/priority_006_567_3757_BB_rank_methods_t600_twodescent40.json`
- `results/priority_009_5075_17901_AA_rank_methods_t600_twodescent40.json`
- `results/priority_012_8075_8613_AA_rank_methods_t600_twodescent40.json`
- `results/priority_013_391_9009_BB_rank_methods_t600_twodescent40.json`
- `results/priority_017_209_21735_BB_rank_methods_t600_twodescent40.json`
- `results/priority_024_5083_12825_BB_rank_methods_t600_twodescent40.json`
- `results/priority_025_5301_38675_BB_rank_methods_t600_twodescent40.json`
- `results/priority_005_1625_5643_AA_mwrank_rank_probe.json`
- `results/priority_006_567_3757_BB_mwrank_rank_probe.json`
- `results/priority_009_5075_17901_AA_mwrank_rank_probe.json`
- `results/priority_012_8075_8613_AA_mwrank_rank_probe.json`
- `results/priority_013_391_9009_BB_mwrank_rank_probe.json`
- `results/priority_017_209_21735_BB_mwrank_rank_probe.json`
- `results/priority_024_5083_12825_BB_mwrank_rank_probe.json`
- `results/priority_025_5301_38675_BB_mwrank_rank_probe.json`
- `results/priority_005_1625_5643_AA_mwrank_b20_x30_t60_probe.json`
- `results/priority_005_1625_5643_AA_cover_tool_capabilities.json`
- `results/priority_005_1625_5643_AA_external_cover_descent_route.json`
- `results/priority_005_1625_5643_AA_external_cover_certificate_intake.json`
- `results/priority_005_1625_5643_AA_external_cover_certificate_template.json`
- `results/mixed_closure_external_cover_certificate_frontier_intake.json`
- `results/mixed_closure_external_cover_certificate_template_index.json`
- `results/mixed_closure_external_cover_descent_package_index.json`
- `results/closure_quotient_paper_structure_audit.json`
- `results/closure_quotient_partial_artifact_audit.json`
- `results/closure_quotient_partial_dependency_audit.json`
- `results/closure_quotient_ray_ledger.json`
- `results/closure_quotient_lambda_frontier.json`
- `results/closure_quotient_ray_scale_invariance_audit.json`
- `results/closure_quotient_rank_zero_family_candidates.json`
- `results/closure_quotient_rank_zero_primitive_models.json`
- `results/closure_quotient_root_number_lambda_triage.json`
- `results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json`
- `results/mixed_closure_frontier_next_action_audit.json`
- `results/mixed_closure_frontier_escalation_queue.json`
- `results/mixed_closure_priority_handoff_audit_top4.json`
- `results/mixed_closure_rank0_certificate_audit.json`
- `results/pari_bsd_mixed_aabb_t10.jsonl`
- `results/closure_quotient_paper_claim_audit.json`
- `results/closure_quotient_partial_result_summary.json`
- `results/closure_quotient_partial_artifact_audit.json`
- `results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.sage`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.magma`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_sage_probe.json`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_map_verify.json`
- `results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_local_witnesses.json`
- `results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4.json`
- `results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4.json`
- `results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_008_209_5355_BB_covers_5_4_3.json`
- `results/mixed_closure_residual_handoffs/priority_011_1449_12155_BB_covers_5_6_3_4.json`
- `results/mixed_closure_even_model_identity_audit.json`

论文草稿：

- [Closure Quotient Partial Result](paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md)

工作日志：

- [wl290](work-logs/290-mixed-closure-quotient-rank-smoke.md)
- [wl294](work-logs/294-tmp-mixed-closure-answer.md)
- [wl295](work-logs/295-sage-mixed-closure-residual-rank-recheck.md)
- [wl296](work-logs/296-mixed-closure-residual-cover-summary.md)
- [wl297](work-logs/297-mixed-closure-cover-map-handoff.md)
- [wl298](work-logs/298-mixed-closure-rank0-certificate-audit.md)
- [wl299](work-logs/299-mixed-closure-pari-bsd-diagnostics.md)
- [wl300](work-logs/300-closure-quotient-paper-claim-audit.md)
- [wl301](work-logs/301-mixed-closure-residual-handoff.md)
- [wl302](work-logs/302-mixed-closure-even-model-identity-audit.md)
- [wl303](work-logs/303-mixed-closure-rank0-classification-detail-audit.md)
- [wl304](work-logs/304-mixed-closure-residual-evidence-audit.md)
- [wl305](work-logs/305-sage-residual-handoff-probe.md)
- [wl306](work-logs/306-mixed-residual-cover-priority-queue.md)
- [wl307](work-logs/307-priority-handoff-export-and-second-sage-probe.md)
- [wl308](work-logs/308-priority-queue-paper-claim-gate.md)
- [wl309](work-logs/309-residual-language-overclaim-audit.md)
- [wl310](work-logs/310-language-audit-paper-claim-gate.md)
- [wl311](work-logs/311-closure-quotient-partial-result-summary.md)
- [wl312](work-logs/312-closure-quotient-partial-artifact-audit.md)
- [wl313](work-logs/313-priority-handoff-probe-audit.md)
- [wl314](work-logs/314-sage-cover-map-identity-verification.md)
- [wl315](work-logs/315-sage-local-witness-probe.md)
- [wl316](work-logs/316-all-residual-local-witnesses.md)
- [wl317](work-logs/317-residual-local-witness-paper-claim-gate.md)
- [wl318](work-logs/318-residual-selmer-gap-ledger.md)
- [wl319](work-logs/319-all-residual-cover-map-verification.md)
- [wl320](work-logs/320-residual-selmer-gap-frontier-split.md)
- [wl321](work-logs/321-rank0-torsion-preimage-audit.md)
- [wl322](work-logs/322-bsd-conditional-no-point-audit.md)
- [wl323](work-logs/323-residual-open-frontier-audit.md)
- [wl324](work-logs/324-rank-zero-frontier-queue.md)
- [wl325](work-logs/325-non-rankzero-frontier-queue.md)
- [wl326](work-logs/326-rank1-frontier-recheck.md)
- [wl327](work-logs/327-even-gap4-frontier-recheck.md)
- [wl328](work-logs/328-rankzero-frontier-recheck-567-3757.md)
- [wl329](work-logs/329-rankzero-frontier-recheck-5075-17901.md)
- [wl330](work-logs/330-rankzero-frontier-long-recheck-1625-5643.md)
- [wl331](work-logs/331-rankzero-frontier-recheck-8075-8613.md)
- [wl332](work-logs/332-rankzero-frontier-recheck-391-9009.md)
- [wl333](work-logs/333-rankzero-frontier-recheck-209-21735.md)
- [wl334](work-logs/334-rankzero-frontier-recheck-5083-12825.md)
- [wl335](work-logs/335-rankzero-frontier-recheck-5301-38675.md)
- [wl336](work-logs/336-residual-frontier-strategy-audit.md)
- [wl337](work-logs/337-frontier-target-handoff-1625-5643.md)
- [wl338](work-logs/338-all-rankzero-frontier-handoffs.md)
- [wl339](work-logs/339-non-rankzero-frontier-handoffs.md)
- [wl340](work-logs/340-frontier-handoff-audit.md)
- [wl341](work-logs/341-frontier-strictification-queue.md)
- [wl342](work-logs/342-frontier-strictification-attempt.md)
- [wl343](work-logs/343-frontier-rank-method-probe.md)
- [wl344](work-logs/344-frontier-batch-rank-method-probe.md)
- [wl345](work-logs/345-frontier-next-action-audit.md)
- [wl346](work-logs/346-rankzero-frontier-long-recheck-567-3757.md)
- [wl347](work-logs/347-rankzero-frontier-long-recheck-5075-17901.md)
- [wl348](work-logs/348-rankzero-frontier-long-recheck-8075-8613.md)
- [wl349](work-logs/349-rankzero-frontier-long-recheck-391-9009.md)
- [wl350](work-logs/350-rankzero-frontier-long-recheck-209-21735.md)
- [wl351](work-logs/351-rankzero-frontier-long-recheck-5083-12825.md)
- [wl352](work-logs/352-rankzero-frontier-long-recheck-5301-38675.md)
- [wl353](work-logs/353-frontier-escalation-queue.md)
- [wl354](work-logs/354-mwrank-frontier-rank-probe.md)
- [wl355](work-logs/355-sage-cover-tool-capability-audit.md)
- [wl356](work-logs/356-external-cover-descent-route-audit.md)
- [wl357](work-logs/357-external-cover-certificate-intake.md)
- [wl358](work-logs/358-frontier-external-certificate-intake.md)
- [wl359](work-logs/359-summary-gate-external-certificate-intake.md)
- [wl360](work-logs/360-paper-structure-audit.md)
- [wl361](work-logs/361-partial-result-dependency-audit.md)
- [wl362](work-logs/362-external-cover-descent-packages.md)
- [wl363](work-logs/363-closure-quotient-ray-ledger.md)
- [wl364](work-logs/364-closure-quotient-lambda-frontier.md)
- [wl365](work-logs/365-closure-quotient-ray-scale-invariance.md)
- [wl366](work-logs/366-rank-zero-family-candidates.md)
- [wl367](work-logs/367-rank-zero-primitive-models.md)
- [wl368](work-logs/368-root-number-lambda-triage.md)

数学总入口：

- [docs/MATH.md](MATH.md) §8.4.1
