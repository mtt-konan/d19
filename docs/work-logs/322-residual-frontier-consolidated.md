# wl322-wl362 - residual frontier consolidated

## Summary

This replaces the old wl322-wl362 residual-frontier worklogs.

普通话说：这一段原来写了很多 Sage/mwrank 重跑、handoff、外部证书模板和论文 gate。
主线结论其实只有一个：逐 cover 严格化路线没有闭合；没有任何 residual target 被提升成证明。

## What This Block Established

- The residual frontier was split into 10 targets and 23 candidate covers.
- 8 rank-zero targets all kept the same open pattern:
  `rank_bounds=[0,2]`, `selmer_rank=4`, and no strict rank-zero certificate.
- Longer Sage and `mwrank` probes did not close any target.
- The two non-rank-zero targets remained separate open routes:
  rank-one/Sha[2] separation and even-gap4 deeper descent.
- Sage did not expose a direct no-point certificate path for the genus-one
  quartic covers.
- The strict route was therefore moved to external cover descent /
  Mordell-Weil sieve packages.
- The external-certificate intake existed only as a gate; no certificate
  package was ready.
- Paper/artifact/dependency gates checked traceability and wording, not
  mathematics.

## Final Status

```text
frontier_target_count = 10
frontier_cover_count = 23
strict_certificate_ready_count = 0
rank_zero_proof_candidate_count = 0
external_certificate_ready_count = 0
family_exclusion_proved_count = 0
```

## Keep / Drop

Kept for the mainline:

- the residual frontier exists;
- the cheap and medium Sage/mwrank routes did not close it;
- future progress needs external no-point certificates or stronger descent;
- this is not the current lambda/Selmer mainline.

Dropped from the main worklog set:

- per-target failed recheck logs;
- repeated command transcripts;
- handoff-file inventory;
- paper-gate plumbing details.

The detailed machine-readable state still lives in `results/` and the scripts
that generated those results. This file is the human-readable project summary.

## Boundary

No residual cover is proved pointless here. No rank-zero theorem, Selmer bound,
or lambda-family exclusion is proved by this block.
