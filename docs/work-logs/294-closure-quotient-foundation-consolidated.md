# wl290, wl294-wl321 - closure quotient foundation consolidated

## Summary

This replaces the old wl290 mixed-closure smoke log and wl294-wl321
closure-quotient foundation logs.

普通话说：这一段原来记录了从“发现闭合商曲线有用”到“把 residual cover
全部整理成候选包”的过程。主线结论不是“证明快完成了”，而是：

```text
AA/BB rank 0 + torsion pullback gives strict finite certificates.
AB/BA did not become a rank-zero killing tool.
The remaining AA/BB residual rows are explicit 2-cover / Selmer-gap targets,
still candidate-not-proof.
```

## What This Block Established

- The old concordant curve loses the closure relation `M=A+B-N`.
- The four closure-aware quotients are `AA`, `BB`, `AB`, and `BA`.
- On the two stored datasets, `AB/BA` had no rank-zero rows.
- `AA/BB` produced `275` certified rank-zero quotient rows.
- Those `275` rows strictly exclude `220` distinct `(A,B)` candidates.
- Every certified `AA/BB` row pulled back exactly two affine points.
- All affine pullbacks were the midpoint `N=M=(A+B)/2`.
- No certified affine pullback was a full closed square point.
- The centered even quartic model and its maps to/from the elliptic curve were
  checked symbolically.
- The remaining `12` uncertain `AA/BB` rows were compressed into `27`
  explicit no-point-cover candidates.
- The `27` covers are everywhere locally soluble in the PARI `ell2cover`
  sense; bounded search did not find rational points, but bounded search is
  not a proof.
- All `27` stored cover-to-elliptic maps were verified by Sage.
- All `27` candidate covers have bad-prime local witnesses; this supports the
  Sha[2] candidate picture, not a no-point proof.
- The residual Selmer ledger split the `27` covers into:
  `20` rank0-Sha[2]-gap2 candidates, `3` rank1-Sha[2]-gap2 open candidates,
  and `4` even-rank-Sha[2]-gap4 open candidates.
- For the `20` rank0-Sha[2]-gap2 covers, a conditional torsion-preimage audit
  found no rational preimages, conditional on the corresponding elliptic curve
  really having rank zero.

## Main Numbers To Keep

```text
hard-case pairs = 320
local-global residual pairs = 64
quotient rows = 1536

AA/BB rank-zero certificate rows = 275
strictly excluded distinct pairs = 220
affine preimage classification rows = 275
affine preimage points = 550
violations = 0

AA/BB uncertain rank rows = 12
candidate cover total = 27
bad-prime local witness checks = 251
unresolved bad-prime checks = 0
rank0-sha2-gap2 covers = 20
rank1-sha2-gap2-open covers = 3
even-rank-sha2-gap4-open covers = 4
```

## What Was Dropped

Dropped from the human worklog set:

- one-log-per-script implementation notes;
- repeated command transcripts;
- priority queue bookkeeping;
- handoff file inventory;
- paper claim gate churn;
- language-audit plumbing.

Kept in the mainline:

- the mathematical statement of the closure quotients;
- the strict `AA/BB rank=0` torsion-pullback rule;
- the exact certificate counts;
- the residual-cover boundary: these are explicit Sha[2] candidates, not
  proofs;
- the remaining route: prove the Selmer/rank-zero gaps structurally, not by
  adding more candidate counts.

## Boundary

This block does not prove Harborth.

It proves only the stored rank-zero `AA/BB` certificates. The residual covers
remain candidate-not-proof: `hyperellratpoints` and other bounded-search
evidence do not prove no rational point, and BSD diagnostics are not strict
rank certificates.
