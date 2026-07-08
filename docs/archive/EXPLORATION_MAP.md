# Exploration Map

这份文档是路线总览，不再记录每个 wl 的细节。细节见
[worklog index](../work-logs/README.md)。

## Timeline

```text
wl001-wl027
  chain-fast / parametric / GPU / safe-pair early archive.

wl028-wl052
  proof_status, concordant elliptic curves, PARI rank/Selmer, F2-rank.
  Result: good tooling; old rank filter does not solve the problem.

wl053-wl072
  partner graph, K_n hubs, cycles, fast-core infrastructure.
  Result: structure map and speed; no proof obstruction.

wl073-wl104
  GEN-CLOSURE correction, mod-p^2 path, full-space scans.
  Result: full-plane closure language fixed; pure modular proof route closed.

wl105-wl161
  fixed-ratio and sum=A+B branch.
  Result: many models; no proof.

wl162-wl202
  R_lambda and centerline.
  Result: centerline closed via Yang Ji translation; non-center remains open.

wl203-wl293
  wl218 full-plane reciprocal theorem attempt.
  Result: route did not close; kept exact four-branch target and failure boundary.

wl294-wl362
  closure quotient foundation and residual frontier.
  Result: AA/BB rank-zero certificate works; residual covers remain candidates.

wl363-current
  lambda mainline and rank-zero Selmer package attempt.
  Result: current mainline; not yet a theorem.
```

## Current Shape

The project has three layers:

```text
pair-level evidence
  -> strict for stored certificates, but finite

lambda/ray-level certificates
  -> real progress from closure quotients

family theorem
  -> still open; needs Selmer/rank-zero proof
```

The active work is trying to move from the second layer to the third.

## Main Lessons

- Counting more candidates is not proof progress.
- `AA/BB rank=0 + torsion pullback` is the cleanest strict tool found so far.
- `AB/BA` failed as a rank-zero tool for structural reasons.
- GEN-CLOSURE fixed the inside-square/full-plane mistake.
- Centerline cases are closed by Yang Ji, not by new d19 machinery.
- Partner graph, high `k`, and old fixed-ratio routes are diagnostic, not proof.
- The current hard point is a uniform rank-zero/Selmer theorem on `lambda`.

## Reading Order

For current work:

1. [PROJECT_STATUS.md](../PROJECT_STATUS.md)
2. [CLOSURE_QUOTIENT_MAINLINE.md](../CLOSURE_QUOTIENT_MAINLINE.md)
3. [OPEN_DIRECTIONS.md](../OPEN_DIRECTIONS.md)
4. [worklog index](../work-logs/README.md)

For old route archaeology, read only the relevant consolidated worklog.
