# wl028-wl052 - proof-status and elliptic-curve foundation consolidated

## Summary

This replaces the old wl028-wl052 worklogs.

普通话说：这一段把项目从早期搜索推进到 `proof_status`、concordant
elliptic curves、PARI `ellrank/ell2cover`、multi-`N` catalog 和 F2-rank
诊断。它给了很多严格工具和有限范围证据，但没有给出全局证明。

## What This Block Established

- `proof_status` became the main finite-check pipeline.
- Legacy chain/EC entrypoints were separated from current code.
- PARI `ellrank` was normalized to the 4-tuple interface:
  `[rank_lower, rank_upper, sha2_lower, generators]`.
- `ell2cover` became the standard way to materialize 2-cover / Sha[2]
  candidate quartics.
- The old Heegner-height direction was downgraded: useful for finding
  witnesses, not a global decider without a proved height bound.
- A finite Peschmann-style descent checked the stored hard cases up to
  `N <= 10^8`; this is finite evidence, not Harborth.
- Large hard-case/Sha[2] scans found many local-global style candidates.
- `chain_closure_mod_sieve` gave a strong mod-`p^2` finite filter for the
  stored hard cases.
- Multi-concordant-`N` scans showed that multiple concordant values are common
  enough to require their own layer.
- F2-rank classification was added as an information layer, not as a
  no-solution proof.
- The max-hyp 100k audit confirmed many rank and F2-rank facts in range.

## Main Numbers To Keep

```text
hard_case baseline = 320
max_hyp=10000 hard_case count = 326
chain_closure_mod_p2 hard_case survivors = 18 / 4653
finite descent checked N <= 10^8 for the stored 320 hard cases
F2-rank >= 3 candidates at max_hyp=50000 = 110
F2-rank >= 3 candidates at max_hyp=100000 = 190
```

## Boundary

This block did not prove Harborth. It built the finite-search, rank/Selmer,
Sha[2], and multi-`N` instrumentation later work relies on.

The important correction that survived is methodological:

```text
rank/Selmer diagnostics can explain why simple filters fail;
they are not themselves a no-point proof unless the rank/no-point claim is
certified by a strict argument.
```
