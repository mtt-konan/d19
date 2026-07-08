# Current Findings

This is the compact claim ledger. Details live in the consolidated worklogs.

## Confirmed

- Concordant form is the right language for fixed `(A,B)` and common leg `N`.
- GEN-CLOSURE is the right full-plane closure condition:

```text
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}
```

- The old sum-only condition `N1+N2=A+B` covers only the inside-square branch.
- Closure quotient curves recover information lost by the old `E_{A,B}` curve.
- `AA/BB rank=0 + torsion pullback` is a strict certificate.
- Certified `AA/BB` rank-zero rows pull back only to midpoint points.
- Yang Ji closes the midpoint/centerline branch.
- `AB/BA` is not a rank-zero killing tool.

## Not Confirmed

- No global Harborth proof.
- No uniform rank-zero theorem yet.
- No proof that all residual two-cover candidates are pointless.
- No reason to treat increasing candidate/certificate counts as proof progress.

## Useful But Historical

- `proof_status`, PARI rank/Selmer, F2-rank, partner graph, fixed-ratio,
  reciprocal, and modular routes produced tools and negative information.
- They are not current proof engines.
- Their status is summarized in [EXPLORATION_MAP.md](./EXPLORATION_MAP.md).

## Current Test Of Progress

A new result matters if it does one of these:

- turns a candidate into a strict certificate;
- proves a reusable local-image theorem;
- proves a dyadic condition;
- proves a global Selmer dimension bound;
- closes a family of `lambda=A/B` ratios.

Everything else is supporting evidence or cleanup.
