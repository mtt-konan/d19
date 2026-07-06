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
