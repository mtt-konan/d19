# Closure Quotient Mainline

这份文档把 `tmp.txt` 里的混合闭合商曲线方向正式并入 `concordant` 主线。它负责回答：

- 固定 `(A,B)` 后，怎样把被旧曲线忘掉的闭合腿 `M=A+B-N` 放回问题里；
- 哪些闭合商曲线已经能给出严格判据；
- 哪些地方还只是实验信号，不能写进 `proof_status`。

如果只想看临时判断，读 [wl294](work-logs/294-tmp-mixed-closure-answer.md)。如果要接着做这条线，
从本文开始。若要写成论文段落，读 [closure quotient partial result](paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md)。

## 1. 主线位置

当前项目仍以 `concordant` 为 active 主线。closure quotient 是 `concordant` 下面的新子方向。

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
- `scripts/theory/prioritize_mixed_closure_residual_covers.py`
- `scripts/theory/audit_mixed_closure_even_model_identities.py`

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
- `tests/test_prioritize_mixed_closure_residual_covers.py`
- `tests/test_mixed_closure_even_model_identity_audit.py`

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
- `results/mixed_closure_rank0_certificate_audit.json`
- `results/pari_bsd_mixed_aabb_t10.jsonl`
- `results/closure_quotient_paper_claim_audit.json`
- `results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json`
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

数学总入口：

- [docs/MATH.md](MATH.md) §8.4.1
