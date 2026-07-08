# Closure Quotient Partial Result

**Status:** draft note for a partial result. This document does not claim a proof of the
Harborth conjecture. It packages the current closure quotient result into a form that
can become a paper section.

## 1. Claim Level

The current result is a strict local certificate for a specific class of closure
quotient curves.

Given positive integers `(A, B)`, set

```text
M = A + B - N
```

and define the four closure square conditions:

```text
NA = N^2 + A^2
NB = N^2 + B^2
MA = M^2 + A^2
MB = M^2 + B^2
```

The four closure-aware genus-one quotients are:

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

A full closed point must map to all four quotients. Therefore one quotient can rule
out a full closed point if it can list all of its affine rational points and none of
them satisfy the four square conditions.

## 2. Main Lemma Draft

For `AA` or `BB`, write `L=A` or `L=B` respectively. With

```text
t = 2N - (A+B)
z = 4y
```

the quotient becomes the centered even quartic

```text
z^2 = t^4 + p t^2 + q
p = 8L^2 - 2(A+B)^2
q = ((A+B)^2 + 4L^2)^2
```

Use the elliptic curve

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
```

with maps

```text
X = 2(z + t^2)
V = 2t(X+p)
```

and, on the affine branch with `X+p != 0`,

```text
t = V / (2(X+p))
z = X/2 - t^2
N = ((A+B)+t)/2
```

**Lemma.** Suppose the centered even model is non-singular and PARI certifies
`rank_lower=rank_upper=0` for `E`. Then every affine rational point on the original
`AA` or `BB` quartic comes from a torsion point of `E(Q)` through the inverse map
above. The identity of `E` has no affine preimage. A torsion point with `X=-p`
maps to a point at infinity on the quartic.

**Certificate rule.** For a rank-zero `AA` or `BB` quotient, enumerate `elltors(E)`.
Pull back every torsion point. If the affine pullbacks contain no point for which
`NA`, `NB`, `MA`, and `MB` are all rational squares, then this quotient strictly
rules out a full closed affine point for `(A, B)`.

This is stronger than a height search. The finite set comes from the rank-zero
Mordell-Weil group, not from a bound on `N`.

## 3. Certified Census

The current certificate has been run on two datasets.

### 3.1 320 hard cases

Input:

```text
results/archive/ell2cover_hard_cases.jsonl
```

Output:

```text
results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl
```

Rows:

```text
1280 = 320 pairs x 4 quotients
```

Rank split by quotient:

```text
AA: 113 rank 0, 5 rank 0/2, 162 rank 1, 36 rank 2, 4 rank 3
BB: 103 rank 0, 6 rank 0/2, 164 rank 1, 1 rank 1/3, 37 rank 2, 9 rank 3
AB: 0 rank 0, 117 rank 1, 2 rank 1/3, 137 rank 2, 57 rank 3, 7 rank 4
BA: 0 rank 0, 117 rank 1, 2 rank 1/3, 137 rank 2, 57 rank 3, 7 rank 4
```

Certified torsion pullback:

```text
AA/BB rank-0 certificates = 216
strict excluded pairs = 178
certificate status = certified for all 216
affine preimages per certificate = 2
all affine preimages are midpoint N=M=(A+B)/2
full closed affine preimages = 0
```

### 3.2 64 local-global residual pairs

Input:

```text
results/mixed_closure_localglobal_residual64_pairs.jsonl
```

Output:

```text
results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl
```

Rows:

```text
256 = 64 pairs x 4 quotients
```

Rank split by quotient:

```text
AA: 27 rank 0, 34 rank 1, 3 rank 2
BB: 32 rank 0, 30 rank 1, 2 rank 2
AB: 0 rank 0, 20 rank 1, 35 rank 2, 7 rank 3, 2 rank 4
BA: 0 rank 0, 20 rank 1, 35 rank 2, 7 rank 3, 2 rank 4
```

Certified torsion pullback:

```text
AA/BB rank-0 certificates = 59
strict excluded pairs = 42
certificate status = certified for all 59
affine preimages per certificate = 2
all affine preimages are midpoint N=M=(A+B)/2
full closed affine preimages = 0
```

Across both datasets, the strict `AA/BB` certificate covers `275` rank-zero quotient
rows. Every certified row has exactly two affine preimages, and none gives a full
closed square point. At pair level, these certificates strictly exclude `220`
distinct `(A, B)` pairs across the two datasets.

```text
AA/BB rank-0 certificates = 275
strict excluded pairs = 220
```

The stored certificates are audited separately with:

```bash
uv run python scripts/theory/audit_mixed_closure_rank0_certificates.py \
  --input results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --input results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/mixed_closure_rank0_certificate_audit.json \
  --strict
```

The current audit result is:

```text
rank0_aabb_rows = 275
certified_rows = 275
strict_no_full_closed_rows = 275
only_midpoint_rows = 275
classification_detail_rows = 275
classification_detail_point_count = 550
violations = 0
```

This audit checks the stored torsion-pullback certificates. It is not a separate
rank-certification algorithm. It also checks every stored affine preimage
classification, rather than only trusting the certificate's aggregate flags.

The algebraic identities used by the lemma are also audited symbolically:

```bash
uv run python scripts/theory/audit_mixed_closure_even_model_identities.py \
  --out results/mixed_closure_even_model_identity_audit.json \
  --strict
```

Current result:

```text
all_verified = True
```

This checks the centered even quartic formula and both rational maps. It does not
certify ranks or rational points.

### 3.3 Unclosed rank bounds

The 64 residual-pair dataset has no unclosed rank bounds. The 320 hard-case dataset
has 16 unclosed rows:

```text
AA/BB:
  0/2 = 11
  1/3 = 1

AB/BA:
  1/3 = 4
```

A targeted `ellrank(effort=4)` recheck did not close any of these 16 rows. This
sets the next tool boundary: further progress needs a different rank-certification
method, such as 2-descent, Selmer computation, or a better model. Raising PARI effort
inside the current workflow is not a good next bet.

The generated `results/mixed_closure_rank_summary.json` file records each residual
row in `uncertain_rank_rows` with its Weierstrass model, root number, `sha2_lower`,
and torsion order. That field is the handoff point for Sage, Magma, or any later
Selmer-specific tool.

### 3.4 Residual 2-cover candidates

The `AA/BB` part of the residual set has now been diagnosed one level deeper.
Sage Selmer diagnostics and PARI `ell2cover` agree on all 12 `AA/BB` residual rows:

```text
status_counts = {'ok': 12}
covers_without_points_counts = {'2': 10, '3': 1, '4': 1}
selmer_gap_alignment_counts = {'match': 12}
```

Here the Selmer gap is

```text
selmer_rank_pari - torsion_two_dimension.
```

Thus the extra 2-Selmer dimensions are represented by explicit 2-cover quartics
on which `hyperellratpoints` found no rational point up to height `100000`. This is
useful evidence, but it is not yet a strict certificate. A bounded point search
does not prove that a cover has no rational point.

```text
bounded search is not a proof
```

PARI `ell2cover` returns everywhere locally soluble 2-covers, so these rows should
not be advertised as local-obstruction candidates. The right interpretation is
that they are explicit candidates for non-trivial `Sha[2]` classes. The current
collector records the quartic equations, and on rerun also records PARI's covering
map to the elliptic curve.

The correct paper-level wording is:

```text
The remaining AA/BB residual rows produce explicit Sha[2] candidate covers.
They are not currently accepted by the strict certificate rule.
```

The current summary is reproducible with:

```bash
uv run python scripts/theory/summarize_mixed_closure_residual_covers.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_aabb_residual_cover_summary.json
```

A stricter cross-file audit aligns the residual rows across the rank summary,
Sage Selmer diagnostics, PARI `ell2cover` output, and BSD diagnostics:

```bash
uv run python scripts/theory/audit_mixed_closure_residual_evidence.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/mixed_closure_aabb_residual_evidence_audit.json \
  --strict
```

Current result:

```text
target_rows = 12
candidate_cover_total = 27
violations = 0
```

This is still an evidence audit, not a no-point proof. Its main purpose is to
make sure the residual rows and candidate-cover language remain consistent.

Prioritize the explicit no-point candidates for follow-up:

```bash
uv run python scripts/theory/prioritize_mixed_closure_residual_covers.py \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json \
  --out results/mixed_closure_aabb_residual_cover_priorities.json
```

Current result:

```text
candidate_cover_total = 27
top_target = {'A': 115, 'B': 297, 'curve': 'AA', 'cover_index': 3}
```

The first four targets are the two `AA` rows with BSD-conditional analytic rank
zero, ordered by quartic coefficient height:

```text
1. (115,297) AA cover 3, height 54060
2. (115,297) AA cover 4, height 6281875
3. (575,4641) AA cover 4, height 7095212
4. (575,4641) AA cover 3, height 63929328
```

This table is only a work queue for strictification. It is not a proof that any
cover has no rational point.

The priority queue can also drive handoff export directly:

```bash
uv run python scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --top 4 \
  --out-dir results/mixed_closure_residual_handoffs
```

Current output:

```text
priority_001_115_297_AA_covers_3_4
priority_003_575_4641_AA_covers_4_3
```

The second handoff, `(575,4641) AA covers 4,3`, has also been probed with Sage:

```text
rank_bounds = [0, 2]
rank_proof_status = runtime-error
rank_probable = 0
selmer_rank = 4
torsion_two_dimension = 2
cover_point_counts = [0, 0]
```

So the first two priority groups share the same local picture: BSD-conditional
rank zero, unresolved strict rank bounds, and two genus-one cover candidates
with no points found by the bounded Sage probe.

There is also a PARI analytic/BSD diagnostic script:

```bash
uv run python scripts/theory/pari_bsd_mixed_closure_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_bsd_mixed_aabb_t10.jsonl \
  --curve AA \
  --curve BB \
  --timeout 10
```

With this budget, the current result is:

```text
status_counts = {'ok': 2, 'pari-error': 2, 'timeout': 8}
analytic_rank_counts = {'0': 2}
```

The two successful rows give BSD-conditional support for `rank 0`; they do not
replace the strict rank-zero certificate rule. The failed rows are tool-budget
failures, not mathematical counterevidence.

## 4. Reproducibility

Run the hard-case census:

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --certify-rank0-torsion
```

Run the residual-pair census:

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/mixed_closure_localglobal_residual64_pairs.jsonl \
  --out results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --certify-rank0-torsion
```

Build the paper summary table:

```bash
uv run python scripts/theory/summarize_mixed_closure_results.py \
  --input results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --input results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/mixed_closure_rank_summary.json
```

Audit the numeric claims used in this note:

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
  --expect language_audit_files=71 \
  --expect language_candidate_not_proof_hits=7 \
  --expect language_sha2_candidate_hits=5 \
  --expect language_bounded_search_not_proof_hits=3 \
  --expect language_bsd_not_strict_certificate_hits=1 \
  --expect even_model_identities_verified=1 \
  --expect bsd_ok_rows=2 \
  --expect bsd_analytic_rank0_rows=2 \
  --strict
```

Current result:

```text
mismatches = 0
```

This is a consistency gate for stored result files and paper-level numeric claims.
It does not create new mathematical certificates.
It also checks the full residual local-witness totals: `27` candidate covers,
`251` bad-prime checks, `0` unresolved bad-prime checks, and
`all_bad_primes_witnessed = 1`.

Audit residual wording so evidence is not promoted to proof:

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
  --path docs/work-logs/369-two-cover-lambda-frontier.md \
  --path docs/work-logs/370-lambda-route-partition-audit.md \
  --path docs/work-logs/371-lambda-mainline-audit.md \
  --path docs/work-logs/372-rank-zero-proof-seeds.md \
  --path docs/work-logs/373-rank-zero-seed-identities.md \
  --path docs/work-logs/374-rank-zero-certifying-invariants.md \
  --path docs/work-logs/375-rank-zero-forced-torsion.md \
  --path docs/work-logs/376-root-number-proof-seeds.md \
  --path docs/work-logs/377-two-cover-proof-seeds.md \
  --path docs/work-logs/378-lambda-proof-seed-coverage.md \
  --path docs/work-logs/379-lambda-mainline-proof-seed-gate.md \
  --path docs/work-logs/380-lambda-convergence-priorities.md \
  --path docs/work-logs/381-rank-zero-family-obligations.md \
  --path docs/work-logs/382-rank-zero-symbolic-descent-inputs.md \
  --path docs/work-logs/383-rank-zero-isogeny-templates.md \
  --path docs/work-logs/384-rank-zero-selmer-obligations.md \
  --path docs/work-logs/385-rank-zero-selmer-package-index.md \
  --out results/mixed_closure_residual_language_audit.json \
  --strict
```

Current result:

```text
files = 71
violations = 0
required_boundary_hits = {
  'candidate_not_proof': 7,
  'sha2_candidate': 5,
  'bounded_search_not_proof': 3,
  'bsd_not_strict_certificate': 1
}
```

This wording audit does not verify the mathematics. It only guards the paper
language against turning bounded search, BSD-conditional diagnostics, or
`Sha[2]` candidates into proof claims.

Audit the residual frontier proof strategy:

```bash
uv run python scripts/theory/audit_mixed_closure_residual_frontier_strategy.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --out results/mixed_closure_residual_frontier_strategy_audit.json \
  --strict
```

Current result:

```text
short_sage_retry_status = exhausted-without-proof
short_sage_retry_target_count = 10
short_sage_retry_timeout_target_count = 10
strict_promotion_count = 0
next_strategy_counts = {
  'external_rank_proof_or_cover_level_descent': 8,
  'rank1_generator_or_sha2_separation': 1,
  'even_gap4_deeper_descent_or_sha2_obstruction': 1
}
```

This is routing information, not a proof.

Audit the frontier handoff packages:

```bash
uv run python scripts/theory/audit_mixed_closure_frontier_handoffs.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out results/mixed_closure_frontier_handoff_audit.json \
  --strict
```

Current result:

```text
status = ok
handoff_group_count = 10
target_cover_count = 23
map_verified_group_count = 10
local_witnessed_group_count = 10
bounded_probe_group_count = 10
strict_promotion_count = 0
missing_files = []
violations = []
```

This checks package consistency only. It does not prove that the residual
2-covers have no rational point.

Build the frontier strictification queue:

```bash
uv run python scripts/theory/summarize_mixed_closure_frontier_strictification.py \
  --rank-zero-queue results/mixed_closure_rank_zero_frontier_queue.json \
  --non-rankzero-queue results/mixed_closure_non_rankzero_frontier_queue.json \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --out results/mixed_closure_frontier_strictification_queue.json \
  --strict
```

Current result:

```text
status = ok
target_count = 10
cover_count = 23
track_counts = {'even-gap4-deeper-descent': 1, 'rank-one-sha2-separation': 1, 'rank-zero-rank-proof': 8}
strict_certificate_ready_count = 0
first_target = {'A': 1625, 'B': 5643, 'curve': 'AA', 'track': 'rank-zero-rank-proof', 'priorities': [5, 7], 'cover_indices': [3, 4]}
```

This queue says which strict proof object is needed next. It is not itself a
proof.

Audit the first strictification attempt:

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

Current result:

```text
status = ok
attempt_count = 26
target_count_with_attempts = 8
attempt_status_counts = {'open-rank-bounds-not-proof': 7, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 3}
strict_certificate_ready_count = 0
```

The underlying Sage handoff probe used `two_descent_second_limit=20` and a
180-second timeout on `(1625,5643) AA`; it timed out. This is not a rank proof.

Run the same target through separate Sage rank-method subprocesses:

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

Current result:

```text
method_status_counts = {'pari_ellrank:ok': 1, 'rank_bounds:ok': 1, 'rank_proof:runtime-error': 1, 'selmer_rank:ok': 1, 'two_descent:timeout': 1}
rank_zero_proof_candidate = False
```

Batch-run the cheap rank methods over all 8 rank-zero frontier targets:

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

Current result:

```text
status = ok
target_count = 8
method_status_counts = {'pari_ellrank:ok': 8, 'rank_bounds:ok': 8, 'selmer_rank:ok': 8}
rank_zero_proof_candidate_count = 0
```

For each of the 8 targets, the cheap diagnostics remain
`rank_bounds=[0,2]`, `selmer_rank=4`, and PARI `ellrank=[0,2,0,[]]`.
This is not a rank-zero proof.

Audit the frontier next-action route:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_next_actions.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --batch-rank-methods results/mixed_closure_rank_zero_frontier_batch_rank_methods_t45.json \
  --out results/mixed_closure_frontier_next_action_audit.json \
  --strict
```

Current result:

```text
status = ok
cheap_rank_method_target_hopping_exhausted = True
rank_zero_rank_method_target_hopping_exhausted = True
recommended_mainline = escalate-beyond-cheap-rank-methods
```

This is a routing gate, not a proof. It records that cheap rank-method
target-hopping and same-level rank-method long rechecks have converged without a
strict certificate. The next mainline should escalate to stronger descent,
external strict rank proof, or cover-level no-point certificates.

Audit the frontier escalation queue:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_escalation_queue.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --next-action-audit results/mixed_closure_frontier_next_action_audit.json \
  --out results/mixed_closure_frontier_escalation_queue.json \
  --strict
```

Current result:

```text
status = ok
target_count = 10
cover_count = 23
rank_zero_target_count = 8
rank_zero_rank_method_target_hopping_exhausted = True
strict_certificate_ready_count = 0
route_counts = {'even-gap4-deeper-descent-or-cover-descent': 1, 'rank-one-generator-sha2-separation-or-cover-descent': 1, 'rank-zero-external-rank-proof-or-cover-descent': 8}
```

This queue records the next strict evidence route. It is not a proof.

Audit Sage cover-level tool capability for the first escalation target:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_sage_cover_tool_capabilities.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --sage sage \
  --timeout 30 \
  --strict
```

Current result:

```text
status = ok
cover_count = 2
genus_one_cover_count = 2
sage_direct_no_point_capable_count = 0
strict_certificate_ready_count = 0
recommended_next_tool = magma-or-specialized-cover-descent
```

This is a tool-capability audit, not a proof. It records that Sage's built-in
interfaces here expose bounded point search, but not a direct cover-level
no-point certificate route.

Audit the external cover-descent route for the same escalation target:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_descent_route.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --sage-cover-capability-audit results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --out results/priority_005_1625_5643_AA_external_cover_descent_route.json \
  --magma magma \
  --strict
```

Current result:

```text
status = ok
local_magma_available = False
proof_status = external-tool-gap-open
recommended_next_action = obtain-magma-or-specialized-cover-descent-environment
```

This is a route audit, not a proof. It records that this local machine still
lacks the external cover-descent environment needed for a reproducible
no-point or rank-closing transcript.

Audit external cover-certificate intake for the same target:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_intake.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_external_cover_certificate_intake.json \
  --template-out results/priority_005_1625_5643_AA_external_cover_certificate_template.json \
  --strict
```

Current result:

```text
status = ok
certificate_package_ready = False
strict_promotion_ready = False
```

This is an intake gate, not a mathematical verifier. It creates the expected
external-certificate package shape and prevents incomplete external evidence
from being promoted.

Audit frontier-wide external cover-certificate intake:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_frontier_intake.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --certificate-dir results/mixed_closure_external_certificates \
  --out results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --template-index-out results/mixed_closure_external_cover_certificate_template_index.json \
  --strict
```

Current result:

```text
status = ok
target_count = 10
cover_count = 23
certificate_package_ready_count = 0
strict_promotion_ready_count = 0
```

This extends the external evidence intake from one target to the full residual
frontier. It is not a proof and currently records no strict promotion.

Audit the paper-note structure:

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

Current result:

```text
status = ok
matched_section_count = 5
matched_claim_count = 14
```

This is a paper-structure gate, not a mathematical verifier.

Summarize the full partial-result gate:

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

Current result:

```text
ready_for_partial_result = True
blocking_issues = []
rank0_torsion_certificates = 275
strict_excluded_pair_count = 220
candidate_cover_total = 27
residual proof_status = candidate-not-proof
priority_handoff_status.ready = True
priority_handoff_status.groups_checked = 2
priority_handoff_status.target_cover_count = 4
priority_handoff_status.map_verified_groups = 2
priority_handoff_status.local_witnessed_groups = 2
residual_local_witness_status.candidate_cover_total = 27
residual_local_witness_status.bad_prime_check_total = 251
residual_local_witness_status.unresolved_bad_prime_total = 0
residual_selmer_gap_status.candidate_cover_total = 27
residual_selmer_gap_status.rows_with_ok_diagnostics = 27
residual_selmer_gap_status.rank0_sha2_gap2_cover_total = 20
residual_selmer_gap_status.gap_type_counts = {'even-rank-sha2-gap4-open': 4, 'rank0-sha2-gap2': 20, 'rank1-sha2-gap2-open': 3}
residual_cover_map_status.target_cover_count = 27
residual_cover_map_status.verified_cover_count = 27
residual_cover_map_status.failed_cover_count = 0
rank0_torsion_preimage_status.target_cover_count = 20
rank0_torsion_preimage_status.no_torsion_preimage_count = 20
rank0_torsion_preimage_status.failed_cover_count = 0
rank0_torsion_preimage_status.conditional_on_rank_zero = True
bsd_conditional_no_point_status.bsd_conditional_no_point_cover_count = 4
bsd_conditional_no_point_status.rank0_sha2_gap2_cover_count = 20
bsd_conditional_no_point_status.strict_no_point_cover_count = 0
bsd_conditional_no_point_status.candidate_not_proof = True
bsd_conditional_no_point_status.proof_status = conditional-not-proof
residual_open_frontier_status.candidate_cover_total = 27
residual_open_frontier_status.conditional_no_point_cover_count = 4
residual_open_frontier_status.open_frontier_cover_count = 23
residual_open_frontier_status.open_frontier_type_counts = {'even-rank-gap4-needs-deeper-descent': 4, 'rank-zero-needs-rank-proof': 16, 'rank1-needs-visible-generator-or-descent': 3}
residual_open_frontier_status.strict_no_point_cover_count = 0
residual_open_frontier_status.proof_status = open-frontier-not-proof
rank_zero_frontier_status.rank_zero_frontier_cover_count = 16
rank_zero_frontier_status.rank_zero_frontier_target_count = 8
rank_zero_frontier_status.closed_rank_zero_target_count = 0
rank_zero_frontier_status.target_status_counts = {'sage-timeout': 8}
rank_zero_frontier_status.proof_status = rank-proof-frontier-not-proof
non_rankzero_frontier_status.non_rankzero_frontier_cover_count = 7
non_rankzero_frontier_status.non_rankzero_frontier_target_count = 2
non_rankzero_frontier_status.target_type_counts = {'even-rank-gap4-needs-deeper-descent': 1, 'rank1-needs-visible-generator-or-descent': 1}
non_rankzero_frontier_status.target_status_counts = {'sage-timeout': 2}
non_rankzero_frontier_status.proof_status = non-rankzero-frontier-not-proof
residual_frontier_strategy_status.short_sage_retry_status = exhausted-without-proof
residual_frontier_strategy_status.short_sage_retry_target_count = 10
residual_frontier_strategy_status.short_sage_retry_timeout_target_count = 10
residual_frontier_strategy_status.strict_promotion_count = 0
residual_frontier_strategy_status.next_strategy_counts = {'even_gap4_deeper_descent_or_sha2_obstruction': 1, 'external_rank_proof_or_cover_level_descent': 8, 'rank1_generator_or_sha2_separation': 1}
residual_frontier_strategy_status.proof_status = strategy-not-proof
frontier_handoff_status.ready = True
frontier_handoff_status.handoff_group_count = 10
frontier_handoff_status.target_cover_count = 23
frontier_handoff_status.map_verified_group_count = 10
frontier_handoff_status.local_witnessed_group_count = 10
frontier_handoff_status.bounded_probe_group_count = 10
frontier_handoff_status.strict_promotion_count = 0
frontier_handoff_status.proof_status = handoff-not-proof
frontier_strictification_status.ready = True
frontier_strictification_status.target_count = 10
frontier_strictification_status.cover_count = 23
frontier_strictification_status.track_counts = {'even-gap4-deeper-descent': 1, 'rank-one-sha2-separation': 1, 'rank-zero-rank-proof': 8}
frontier_strictification_status.strict_certificate_ready_count = 0
frontier_strictification_status.proof_status = strictification-queue-not-proof
frontier_strictification_attempt_status.ready = True
frontier_strictification_attempt_status.attempt_count = 26
frontier_strictification_attempt_status.target_count_with_attempts = 8
frontier_strictification_attempt_status.attempt_status_counts = {'open-rank-bounds-not-proof': 7, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 3}
frontier_strictification_attempt_status.strict_certificate_ready_count = 0
frontier_strictification_attempt_status.proof_status = attempt-ledger-not-proof
frontier_next_action_status.ready = True
frontier_next_action_status.cheap_rank_method_target_hopping_exhausted = True
frontier_next_action_status.rank_zero_rank_method_target_hopping_exhausted = True
frontier_next_action_status.recommended_mainline = escalate-beyond-cheap-rank-methods
frontier_next_action_status.proof_status = next-action-routing-not-proof
external_certificate_frontier_status.ready = True
external_certificate_frontier_status.target_count = 10
external_certificate_frontier_status.cover_count = 23
external_certificate_frontier_status.certificate_package_ready_count = 0
external_certificate_frontier_status.missing_certificate_package_count = 10
external_certificate_frontier_status.strict_promotion_ready_count = 0
external_certificate_frontier_status.proof_status = frontier-external-certificates-missing-not-proof
paper_structure_status.ready = True
paper_structure_status.matched_section_count = 5
paper_structure_status.matched_claim_count = 14
paper_structure_status.missing_claim_count = 0
artifact_status.ready = True
artifact_status.required_file_count = 464
artifact_status.missing_file_count = 0
```

Audit the lambda mainline gate:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_mainline.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --lambda-frontier results/closure_quotient_lambda_frontier.json \
  --route-partition results/closure_quotient_lambda_route_partition_audit.json \
  --two-cover-frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --proof-seed-coverage results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --rank-zero-transcript-intake results/closure_quotient_rank_zero_selmer_transcript_intake.json \
  --out results/closure_quotient_lambda_mainline_audit.json \
  --strict
```

Current result:

```text
status = ok
lambda_class_count = 356
covered_class_count = 356
violations = []
```

This is the current evidence-boundary gate for the lambda-level mainline.
It includes the rank-zero transcript-intake boundary: transcript material can be
accepted for review, but this gate does not verify Selmer mathematics or promote
family exclusions.

Audit lambda proof seed coverage:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py \
  --route-partition results/closure_quotient_lambda_route_partition_audit.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --root-number-seeds results/closure_quotient_root_number_proof_seeds.json \
  --two-cover-seeds results/closure_quotient_two_cover_proof_seeds.json \
  --out results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --strict
```

Current result:

```text
lambda_class_count = 356
seed_ledger_class_count = 356
violations = []
```

This checks that the rank-zero, root-number, and two-cover routes all have
proof-seed ledgers. It does not prove any family exclusion theorem.

Audit lambda convergence priorities:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py \
  --proof-seed-coverage results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --rank-zero-identity-audit results/closure_quotient_rank_zero_seed_identity_audit.json \
  --rank-zero-invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --rank-zero-forced-torsion results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --root-number-seeds results/closure_quotient_root_number_proof_seeds.json \
  --two-cover-seeds results/closure_quotient_two_cover_proof_seeds.json \
  --out results/closure_quotient_lambda_convergence_priorities.json \
  --strict
```

Current result:

```text
status = ok
lambda_class_count = 356
priority_order = ['rank_zero', 'root_number', 'two_cover']
family_exclusion_proved_count = 0
```

This fixes the next proof order without claiming completion: rank-zero family
theorems first, root-number/rank structure second, strict two-cover certificates
third.

Audit rank-zero family obligations:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py \
  --convergence-priorities results/closure_quotient_lambda_convergence_priorities.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --identity-audit results/closure_quotient_rank_zero_seed_identity_audit.json \
  --invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --forced-torsion results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --out results/closure_quotient_rank_zero_family_obligations.json \
  --strict
```

Current result:

```text
status = ok
rank_zero_family_proof_complete = False
rank_zero_family_obligation_count = 3
family_exclusion_proved_count = 0
```

This records that the rank-zero route is now three open family theorem obligations:
`AA`, `AA+BB`, and `BB`. More individual rank rows are diagnostics only.

Audit rank-zero symbolic descent inputs:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_symbolic_descent_inputs.json \
  --strict
```

Current result:

```text
status = ok
primitive_model_count = 243
symbolic_formula_verified_count = 243
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This records the uniform symbolic descent input
`p=8L^2-2T^2`, `sqrt_q=T^2+4L^2`, with root differences
`-16L^2`, `4T^2`, and `4(T^2+4L^2)`. It does not prove the Selmer/rank bound.

Audit rank-zero isogeny templates:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py \
  --symbolic-inputs results/closure_quotient_rank_zero_symbolic_descent_inputs.json \
  --out results/closure_quotient_rank_zero_isogeny_templates.json \
  --strict
```

Current result:

```text
status = ok
primitive_model_count = 243
isogeny_template_verified_count = 729
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This records the three 2-isogeny target templates. It does not compute Selmer
groups or prove rank zero.

Audit rank-zero Selmer obligations:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py \
  --family-obligations results/closure_quotient_rank_zero_family_obligations.json \
  --isogeny-templates results/closure_quotient_rank_zero_isogeny_templates.json \
  --out results/closure_quotient_rank_zero_selmer_obligations.json \
  --strict
```

Current result:

```text
status = ok
family_obligation_count = 3
kernel_count = 3
selmer_obligation_count = 9
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This records the nine open uniform isogeny-Selmer rank-bound obligations.

Export rank-zero Selmer proof package index:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py \
  --selmer-obligations results/closure_quotient_rank_zero_selmer_obligations.json \
  --isogeny-templates results/closure_quotient_rank_zero_isogeny_templates.json \
  --out results/closure_quotient_rank_zero_selmer_package_index.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
open_package_count = 9
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This turns the nine open Selmer obligations into reviewable proof-package inputs.

Materialize rank-zero Selmer proof packages:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py \
  --package-index results/closure_quotient_rank_zero_selmer_package_index.json \
  --packages-dir results/closure_quotient_rank_zero_selmer_packages \
  --out results/closure_quotient_rank_zero_selmer_package_materialization.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
open_package_count = 9
materialized_json_count = 9
materialized_markdown_count = 9
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This writes one JSON task file and one Markdown review file for each open
package. These files record the formulas and required transcript fields; they
do not prove any Selmer bound or family exclusion.

Audit rank-zero Selmer local supports:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py \
  --package-index results/closure_quotient_rank_zero_selmer_package_index.json \
  --out results/closure_quotient_rank_zero_selmer_local_supports.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
support_entry_count = 9
local_condition_proved_count = 0
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
```

This records symbolic support candidates for future local Selmer conditions.
The common candidate bad factors are `2, L, T, T^2+4L^2`. This is not a local
condition computation or a Selmer bound.

Audit rank-zero Selmer coprime supports:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py \
  --local-supports results/closure_quotient_rank_zero_selmer_local_supports.json \
  --out results/closure_quotient_rank_zero_selmer_coprime_supports.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
coprime_support_entry_count = 9
local_condition_proved_count = 0
```

For primitive `A:B`, the odd-prime support splits into primes dividing `L`,
primes dividing `T`, and primes dividing `T^2+4L^2`; the prime `2` remains the
separate 2-adic case. This is still not a local condition proof.

Audit rank-zero Selmer odd-prime cases:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py \
  --coprime-supports results/closure_quotient_rank_zero_selmer_coprime_supports.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_cases.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
odd_prime_case_count = 27
two_adic_case_count = 9
local_condition_proved_count = 0
```

This records the open local-case checklist for future transcripts. It does not
close any local condition.

Audit rank-zero Selmer odd-prime valuations:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py \
  --odd-prime-cases results/closure_quotient_rank_zero_selmer_odd_prime_cases.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json \
  --strict
```

Current result:

```text
status = ok
package_count = 9
odd_prime_valuation_case_count = 27
local_condition_proved_count = 0
```

This records the symbolic valuation shapes of `a2`, `a4`, and the quadratic
discriminant in each open odd-prime branch. It is not a local Selmer image
computation and does not close any local condition.

Audit rank-zero Selmer odd-prime lemma queue:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py \
  --odd-prime-valuations results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json \
  --strict
```

Current result:

```text
status = ok
input_valuation_case_count = 27
lemma_obligation_count = 9
local_lemma_proved_count = 0
```

This collapses repeated package-level valuation cases into nine uniform
`kernel x odd-prime support` lemma obligations. It is not a local-condition
proof.

Audit rank-zero Selmer odd-prime reduction shapes:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py \
  --odd-prime-lemma-queue results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.json \
  --strict
```

Current result:

```text
status = ok
input_lemma_obligation_count = 9
reduction_shape_count = 9
reduction_shape_proved_count = 9
local_condition_proved_count = 0
```

This proves the displayed reduced cubic factorization shape for each odd-prime
lemma branch. It does not prove the required isogeny-Selmer local image.

Audit rank-zero Selmer odd-prime local-image schemas:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py \
  --odd-prime-reduction-shapes results/closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --strict
```

Current result:

```text
status = ok
input_reduction_shape_count = 9
local_image_schema_count = 4
local_image_schema_proved_count = 0
local_condition_proved_count = 0
```

This reduces the odd-prime local-image work to four nodal model schemas:
the double root is either nonzero or zero, and the tangent squareclass is
separately `1` or `-1`. The local-image theorem is still open.

Audit rank-zero Selmer tangent-one normal forms:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.py \
  --odd-prime-local-image-schemas results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --strict
```

Current result:

```text
status = ok
input_schema_count = 4
tangent_one_schema_count = 2
normal_form_proved_count = 2
local_image_schema_proved_count = 0
```

This proves the square-unit coordinate normalization for the two tangent-one
schemas. The local-image theorem is still open.

Audit rank-zero Selmer tangent-one unit branch:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_unit_branch.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_unit_branch.json \
  --strict
```

Current result:

```text
status = ok
input_normal_form_count = 2
unit_branch_count = 2
unit_branch_squareclass_consequence_proved_count = 2
local_image_schema_proved_count = 0
```

On the two tangent-one standard models, the unit branch with both `X` and
`X - 1` units gives `X = (Y/(X - 1))^2` and `X - 1 = (Y/X)^2`; hence the
displayed squareclass is trivial on each unit branch. These are only
branch-level consequences, not the local-image theorem.

Audit rank-zero Selmer tangent-one non-node branches:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --strict
```

Current result:

```text
status = ok
input_normal_form_count = 2
nonnode_branch_count = 2
nonnode_squareclass_consequence_proved_count = 2
local_image_schema_proved_count = 0
```

On `Y^2 = X*(X - 1)^2`, every branch with `X - 1 != 0` gives
`X = (Y/(X - 1))^2`. On `Y^2 = X^2*(X - 1)`, every branch with `X != 0`
gives `X - 1 = (Y/X)^2`. These cover the non-node tangent-one branches,
but they are still not the local-image theorem.

Audit rank-zero Selmer tangent-one node values:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_node_values.py \
  --tangent-one-normal-forms results/closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
  --strict
```

Current result:

```text
status = ok
input_normal_form_count = 2
node_value_count = 2
node_reduction_value_proved_count = 2
node_local_lift_analysis_proved_count = 0
local_image_schema_proved_count = 0
```

The node values are reduction-level data: `(X,Y)=(1,0)` gives `X=1` on
`Y^2 = X*(X - 1)^2`, and `(X,Y)=(0,0)` gives `X-1=-1` on
`Y^2 = X^2*(X - 1)`. This does not prove the local squareclass image for
local points lifting to the node.

Audit rank-zero Selmer tangent-one punctured nodes:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.json \
  --strict
```

Current result:

```text
status = ok
input_nonnode_branch_count = 2
input_node_value_count = 2
punctured_node_neighborhood_control_proved_count = 2
node_center_lift_analysis_proved_count = 0
local_image_schema_proved_count = 0
```

The punctured neighborhoods of the tangent-one nodes are controlled by the
non-node identities. This narrows the remaining tangent-one gap to node-center
formal lift compatibility; it still does not prove the local-image theorem.

Audit rank-zero Selmer tangent-one reduction partition:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.py \
  --nonnode-branches results/closure_quotient_rank_zero_selmer_tangent_one_nonnode_branches.json \
  --node-values results/closure_quotient_rank_zero_selmer_tangent_one_node_values.json \
  --punctured-nodes results/closure_quotient_rank_zero_selmer_tangent_one_punctured_nodes.json \
  --out results/closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.json \
  --strict
```

Current result:

```text
status = ok
reduction_partition_count = 2
reduction_partition_exhausted_count = 2
formal_lift_compatibility_proved_count = 0
local_image_schema_proved_count = 0
```

At the reduction level, the tangent-one standard models now have candidate
squareclass sets `{trivial}` for tracked `X` on `Y^2 = X*(X - 1)^2`, and
`{trivial, -1}` for tracked `X - 1` on `Y^2 = X^2*(X - 1)`. This remains a
reduction-level ledger, not a local-image theorem.

Audit rank-zero Selmer transcript intake:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_intake.py \
  --materialization results/closure_quotient_rank_zero_selmer_package_materialization.json \
  --out results/closure_quotient_rank_zero_selmer_transcript_intake.json \
  --template-index-out results/closure_quotient_rank_zero_selmer_transcript_template_index.json \
  --root . \
  --strict
```

Current result:

```text
status = ok
package_count = 9
transcript_package_ready_count = 0
strict_promotion_ready_count = 0
```

This records the review gate for future Selmer transcripts. A complete
transcript package can be accepted as review material, but this audit does not
verify the Selmer mathematics or promote a family exclusion.

Audit lambda route partition:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_route_partition.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --rank-zero-candidates results/closure_quotient_rank_zero_family_candidates.json \
  --root-number-triage results/closure_quotient_root_number_lambda_triage.json \
  --two-cover-frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --out results/closure_quotient_lambda_route_partition_audit.json \
  --strict
```

Current result:

```text
lambda_class_count = 356
rank_zero_class_count = 200
root_number_class_count = 148
two_cover_class_count = 8
covered_class_count = 356
missing_classes = []
overlap_classes = []
unexpected_classes = []
family_exclusion_proved_count = 0
```

This checks route coverage only; it does not prove any family exclusion theorem.

Summarize the two-cover / Selmer lambda frontier:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_two_cover_lambda_frontier.json \
  --strict
```

Current result:

```text
target_class_count = 8
target_pair_count = 8
candidate_cover_total = 18
selmer_gap_counts = {'2': 7, '4': 1}
family_exclusion_proved_count = 0
```

These are remaining frontier classes, not no-point theorems.

Summarize two-cover proof seeds:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py \
  --frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --out results/closure_quotient_two_cover_proof_seeds.json \
  --strict
```

Current result:

```text
seed_group_count = 7
target_class_count = 8
candidate_cover_total = 18
family_exclusion_proved_count = 0
```

This groups the final 2-cover route by strict certificate need. It still accepts
only a family 2-cover/Selmer obstruction or reviewable no-point certificates for
every listed cover.

Summarize root-number lambda triage:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_root_number_lambda_triage.json \
  --strict
```

Current result:

```text
target_class_count = 148
target_pair_count = 156
family_exclusion_proved_count = 0
```

This is a routing ledger. Root number is not used as a standalone proof.

Summarize root-number proof seeds:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py \
  --triage results/closure_quotient_root_number_lambda_triage.json \
  --out results/closure_quotient_root_number_proof_seeds.json \
  --strict
```

Current result:

```text
seed_group_count = 21
target_class_count = 148
target_pair_count = 156
family_exclusion_proved_count = 0
```

This groups the root-number/rank-structure route into 21 combined proof seeds.
The largest three groups cover 100 classes. It is a routing ledger, not a
no-point proof.

Summarize primitive models for rank-zero family candidates:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py \
  --candidates results/closure_quotient_rank_zero_family_candidates.json \
  --out results/closure_quotient_rank_zero_primitive_models.json \
  --strict
```

Current result:

```text
candidate_class_count = 200
model_count = 243
model_counts_by_curve = {'AA': 125, 'BB': 118}
family_exclusion_proved_count = 0
```

This fixes the primitive AA/BB models for future family-level rank-zero proof
work.

Summarize rank-zero proof seeds:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_proof_seeds.json \
  --strict
```

Current result:

```text
seed_group_count = 3
candidate_class_count = 200
model_count = 243
family_exclusion_proved_count = 0
```

This groups the 200 rank-zero candidates into three proof-seed patterns:
`AA` has 82 classes, `AA+BB` has 43 classes, and `BB` has 75 classes. It is a
ledger for future family proof work, not a family exclusion theorem.

Audit rank-zero seed identities:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --out results/closure_quotient_rank_zero_seed_identity_audit.json \
  --strict
```

Current result:

```text
coefficient_identity_verified_count = 243
coefficient_identity_violation_count = 0
p_sign_novel_signal_count = 0
```

This audit shows that the observed `p` signs are forced by the ordered
primitive ray `0<a<b`: AA has negative `p`, and BB has positive `p`. The sign
pattern is not a rank-zero family proof signal.

Summarize rank-zero certifying invariants:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/closure_quotient_rank_zero_certifying_invariants.json \
  --strict
```

Current result:

```text
primitive_model_count = 243
matched_primitive_model_count = 243
matched_rank_row_count = 275
rank_key_counts = {'0/0': 243}
torsion_order_counts = {'4': 243}
root_number_counts = {'1': 243}
family_exclusion_proved_count = 0
```

This collapses the certifying rank rows to primitive `class+curve` lambda
models. The shared observed target is rank `0/0`, torsion order `4`, and root
number `1`; this is a family-proof target, not a proved family theorem.

Audit forced torsion in rank-zero primitive models:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --certifying-invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --out results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --strict
```

Current result:

```text
primitive_model_count = 243
forced_full_two_torsion_count = 243
observed_exact_torsion_order_four_count = 243
family_exclusion_proved_count = 0
```

The full rational 2-torsion is forced by
`X^3+pX^2-4qX-4pq=(X+p)(X^2-4q)` and `q=sqrt_q^2`. Thus torsion order `4`
should not be treated as the main family-proof signal; the rank-zero family
problem remains the rank statement.

Summarize rank-zero family candidates:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_rank_zero_family_candidates.json \
  --strict
```

Current result:

```text
candidate_class_count = 200
strict_observed_pair_count = 220
family_exclusion_proved_count = 0
certifying_curve_pattern_counts = {'AA': 125, 'BB': 118}
```

This list identifies family-level rank-zero proof candidates. It is not itself
a family exclusion theorem.

Audit scale invariance along primitive rays:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_ray_scale_invariance.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/closure_quotient_ray_scale_invariance_audit.json \
  --strict
```

Current result:

```text
observed_ray_count = 356
multi_scale_ray_count = 14
coefficient_identity_verified_count = 1536
coefficient_identity_violation_count = 0
rank_key_consistent_group_count = 56
rank_key_inconsistent_group_count = 0
```

The quotient models for `(A,B)=d(a,b)` are isomorphic to the primitive ray model
under `N=d n` and `y=d^2 y0`.

Summarize the lambda frontier:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_lambda_frontier.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_lambda_frontier.json \
  --strict
```

Current result:

```text
lambda_class_count = 356
track_counts = {
  'rank-zero-family-generalization': 200,
  'root-number-rank-structure-triage': 148,
  'two-cover-or-reviewable-no-point-certificate': 8
}
family_exclusion_proved_count = 0
```

This is a routing ledger for future family-level proof work, not a family
exclusion theorem.

Summarize the primitive ray ledger:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_ray_ledger.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --rank-summary results/mixed_closure_rank_summary.json \
  --residual-cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --out results/closure_quotient_ray_ledger.json \
  --strict
```

Current result:

```text
pair_count = 384
primitive_ray_count = 356
c_ratio_class_count = 356
strict_c_ratio_class_count = 200
residual_candidate_pair_count = 8
```

Here `c_- = |A-B|`, and `c_+/c_-` records the unordered primitive ratio class
`{A:B, B:A}`. This is a ledger key, not a family-level theorem.

Export external cover-descent task packages:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/export_external_cover_descent_packages.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out-dir results/mixed_closure_external_cover_descent_packages \
  --out results/mixed_closure_external_cover_descent_package_index.json \
  --strict
```

Current result:

```text
status = ok
target_count = 10
cover_count = 23
strict_certificate_ready_count = 0
```

Audit partial-result dependency traceability:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_partial_dependencies.py \
  --summary results/closure_quotient_partial_result_summary.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --root . \
  --out results/closure_quotient_partial_dependency_audit.json \
  --strict
```

Current result:

```text
status = ok
dependency_count = 8
missing_summary_statuses = 0
```

The word `ready` here means the stored evidence and wording gates are internally
consistent for a partial-result note, and the required evidence-package artifacts
are present. It does not mean the residual covers have been strictly proven
pointless.

Among the residual covers, 4 now have BSD-conditional rank-zero support and no torsion
preimage under the verified map. This is useful narrowing information, not a theorem:
the strict residual no-point problem remains open.

The other 23 residual candidate covers are also sorted by the next missing proof
ingredient: 16 need a strict rank-zero proof, 3 need the rank-one part separated
from the residual Sha[2] class, and 4 need a deeper descent or independent Sha[2]
obstruction.

The 16 rank-zero-frontier covers share 8 elliptic rank targets. The current queue
records Sage retries on `(1625,5643) AA`, `(567,3757) BB`, `(5075,17901) AA`,
`(8075,8613) AA`, `(391,9009) BB`, `(209,21735) BB`, `(5083,12825) BB`, and `(5301,38675) BB`, with `second_limit=13,20` and a
120-second budget. All timed out. The top target
`(1625,5643) AA` was also retried with `second_limit=20,40` and a 600-second
budget; it still timed out, so it did not close the rank bound.

The 7 non-rank-zero residual covers share 2 elliptic targets: `(209,5355) BB` for
the rank-one/Sha[2] separation problem, and `(1449,12155) BB` for the even gap4
deeper-descent problem. The `(209,5355) BB` target was retried in Sage with
`second_limit=13,20` and a 120-second budget. It timed out, so it remains an
open diagnostic target rather than a proof. The `(1449,12155) BB` target was
retried with the same budget and also timed out. Both non-rank-zero elliptic
targets therefore still need stronger descent tooling or a cover-level proof.
The strategy audit records the combined 10 frontier targets as
`exhausted-without-proof`: the local short Sage queue is exhausted, but the
residual no-point problem is still open.
The first external rank/cover-level target `(1625,5643) AA` now has a handoff for
covers `4,3`: Sage verifies the stored maps, finds local witnesses at the bad
primes, and still reports only diagnostic rank bounds `[0,2]` with
`rank_proof_status = runtime-error`.
All 8 rank-zero frontier targets now have the same handoff package shape. In
each case the maps verify, local witnesses exist at the checked bad primes, and
the bounded Sage probe remains diagnostic rather than proof.
The two non-rank-zero frontier targets now have the same handoff package shape:
`(209,5355) BB` remains a rank-one/Sha[2] separation target with rank bounds
`[1,3]`, while `(1449,12155) BB` remains an even-gap4 deeper-descent target with
rank bounds `[0,4]`.
The frontier handoff audit now checks these 10 handoff groups and 23 covers as
`handoff-not-proof`, with no strict promotion.
The strictification queue orders the same 10 targets by the strict proof object
needed next: 8 rank-zero rank proofs, 1 rank-one/Sha[2] separation, and 1 even
gap4 deeper descent.
The first recorded attempt, `sage-twodescent20` on `(1625,5643) AA`, timed out
under a 180-second budget and therefore leaves `strict_certificate_ready_count = 0`.
The follow-up rank-method probe shows `rank_bounds`, PARI `ellrank`, and
`selmer_rank` complete, while `rank_proof` remains a runtime error and
`two_descent` times out under a 90-second method budget. A batch cheap-method
probe over all 8 rank-zero frontier targets also completes, but every target
keeps `rank_bounds=[0,2]`, `selmer_rank=4`, and PARI `ellrank=[0,2,0,[]]`;
no target becomes a rank-zero proof candidate.

Export the current strict-proof handoff for the smallest residual target:

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

This produces JSON, Sage, and Magma handoff files. The Sage file has been checked
locally for syntax. Magma is not installed locally, so the Magma file is only a
handoff skeleton until a verified transcript is produced.

Probe that handoff with Sage:

```bash
uv run python scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

Current result:

```text
status = ok
rank_bounds = [0, 2]
rank_proof_status = runtime-error
rank_probable = 0
selmer_rank = 4
torsion_two_dimension = 2
cover_point_counts = [0, 0]
```

Sage's proof-rank interface explicitly reports that the rank is not provably
correct and suggests possible non-trivial `Sha(E/Q)[2]`. A follow-up run with
`--two-descent-second-limit 13` timed out at `45` seconds. This is useful
negative evidence for the local workflow, but still not a no-point proof for the
two cover quartics.

Run the targeted tests:

```bash
PARI_MT_ENGINE=single uv run pytest \
  tests/test_mixed_closure_curves.py \
  tests/test_mixed_closure_rank_cli.py \
  tests/test_mixed_closure_summary_cli.py \
  -q
```

The implementation entry points are:

```text
src/rational_distance/concordant/mixed_closure_curves.py
scripts/theory/rank_mixed_closure_curves.py
scripts/theory/summarize_mixed_closure_results.py
scripts/theory/sage_diagnose_mixed_closure_residuals.py
scripts/theory/pari_ell2cover_mixed_residuals.py
scripts/theory/summarize_mixed_closure_residual_covers.py
scripts/theory/audit_mixed_closure_rank0_certificates.py
scripts/theory/pari_bsd_mixed_closure_residuals.py
scripts/theory/audit_mixed_closure_residual_evidence.py
scripts/theory/audit_closure_quotient_paper_claims.py
scripts/theory/export_mixed_closure_residual_handoff.py
scripts/theory/sage_probe_mixed_closure_handoff.py
scripts/theory/sage_verify_mixed_closure_handoff_maps.py
scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py
scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py
scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py
scripts/theory/audit_mixed_closure_residual_open_frontier.py
scripts/theory/summarize_mixed_closure_rank_zero_frontier.py
scripts/theory/summarize_mixed_closure_non_rankzero_frontier.py
scripts/theory/audit_mixed_closure_residual_frontier_strategy.py
scripts/theory/audit_mixed_closure_frontier_handoffs.py
scripts/theory/summarize_mixed_closure_frontier_strictification.py
scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py
scripts/theory/sage_probe_mixed_closure_rank_methods.py
scripts/theory/batch_sage_probe_mixed_closure_rank_methods.py
scripts/theory/audit_mixed_closure_frontier_next_actions.py
scripts/theory/audit_mixed_closure_frontier_escalation_queue.py
scripts/theory/probe_mwrank_mixed_closure_rank.py
scripts/theory/audit_sage_cover_tool_capabilities.py
scripts/theory/audit_external_cover_descent_route.py
scripts/theory/audit_external_cover_certificate_intake.py
scripts/theory/audit_external_cover_certificate_frontier_intake.py
scripts/theory/export_external_cover_descent_packages.py
scripts/theory/sage_probe_mixed_closure_local_witnesses.py
scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py
scripts/theory/prioritize_mixed_closure_residual_covers.py
scripts/theory/audit_mixed_closure_residual_language.py
scripts/theory/audit_mixed_closure_priority_handoffs.py
scripts/theory/audit_closure_quotient_paper_structure.py
scripts/theory/audit_closure_quotient_partial_dependencies.py
scripts/theory/summarize_closure_quotient_ray_ledger.py
scripts/theory/summarize_closure_quotient_lambda_frontier.py
scripts/theory/audit_closure_quotient_ray_scale_invariance.py
scripts/theory/summarize_closure_quotient_rank_zero_family_candidates.py
scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py
scripts/theory/summarize_closure_quotient_rank_zero_proof_seeds.py
scripts/theory/summarize_closure_quotient_rank_zero_certifying_invariants.py
scripts/theory/audit_closure_quotient_rank_zero_forced_torsion.py
scripts/theory/audit_closure_quotient_rank_zero_seed_identities.py
scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py
scripts/theory/audit_closure_quotient_rank_zero_symbolic_descent_inputs.py
scripts/theory/audit_closure_quotient_rank_zero_isogeny_templates.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_obligations.py
scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py
scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_intake.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.py
scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_tangent_one_normal_forms.py
scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py
scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py
scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py
scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py
scripts/theory/audit_closure_quotient_lambda_route_partition.py
scripts/theory/audit_closure_quotient_lambda_mainline.py
scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py
scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py
scripts/theory/summarize_closure_quotient_partial_result.py
scripts/theory/audit_mixed_closure_even_model_identities.py
scripts/theory/audit_closure_quotient_partial_artifacts.py
```

The certificate-producing function is:

```text
certify_rank_zero_even_quotient()
```

## 5. Decision Framework

Use this as the current strict closure quotient framework:

```text
For each pair (A, B):
  build AA, BB, AB, BA quotients
  compute rank bounds for each quotient
  if AA or BB has certified rank 0:
    enumerate torsion on the centered even elliptic model
    pull back every torsion point
    if no affine pullback is a full closed square point:
      record a strict local closure quotient exclusion for this pair
  otherwise:
    keep the pair as unresolved by this tool
```

The framework does not accept root number as proof. It does not accept a bounded
height search as proof. It accepts only the rank-zero torsion certificate described
above.

At this stage, keep the framework as an offline certificate tool. Do not wire it into
the default `proof_status` path until that path has a pair-level certificate field.
The only acceptable future `proof_status` evidence is:

```text
AA/BB rank=0
torsion certificate status = certified
certifies_no_full_closed_square = true
```

## 6. Current Boundaries

The result does not prove Harborth's conjecture.

The result does not turn `AA/BB rank=0` into a universal pair decision procedure.
It applies only when the rank bounds close to `0/0`.

The result does not support the earlier guess that `AB` is the rank-zero killer.
In both datasets, `AB/BA` have no rank-zero rows.

There is a concrete reason to downgrade that guess. The mixed quotients have
universal affine points:

```text
AB: N=A gives y=2AB, and N=B gives y=A^2+B^2
BA: N=A gives y=A^2+B^2, and N=B gives y=2AB
```

These points do not require all four square conditions. They only show that the
mixed quotients carry built-in rational points.

The `AB/BA` quotients share the Weierstrass model

```text
E_mix: Y^2 = X^3 + C X^2 - D X - CD
C = 2(A^2 + AB + B^2)
D = (2AB)^2
```

and this model carries the explicit point

```text
P_mix = (-(A^2+B^2), (A+B)^2(B-A)).
```

For the specialization `(A,B)=(7,45)`, PARI verifies that `P_mix` lies on `E_mix`
and has `ellorder(P_mix)=0`. Hence `P_mix` is not a torsion point in the generic
family. In the two current datasets, the same point has `ellorder=0` for all `384`
distinct pairs. This explains why `AB/BA` should not be treated as rank-zero
obstruction candidates in this framework.

The midpoint-only outcome is an observed stronger pattern in the two datasets. The
certificate rule only needs the weaker condition: no affine pullback satisfies all
four square conditions.

## 7. Paper Path

This note can become a partial-result section with the following structure:

1. Define the closed curve `C^+_{A,B}` and the four genus-one quotients.
2. Prove the `AA/BB` centered even model and the rank-zero torsion pullback lemma.
3. State the certificate rule.
4. Present the two certified censuses.
5. State the remaining problems:
   the `AA/BB` residuals are explicit 2-cover no-point candidates, and need a strict
   no-point certificate before they can produce more rank-zero certificates.

The current evidence package also has an artifact audit:

```bash
uv run python scripts/theory/audit_closure_quotient_partial_artifacts.py \
  --out results/closure_quotient_partial_artifact_audit.json \
  --strict
```

This checks that the scripts, tests, result files, paper note, and worklogs needed
for the partial-result package are present. It does not check mathematical truth.
Current output:

```text
ready = True
required_file_count = 464
missing_files = []
```
