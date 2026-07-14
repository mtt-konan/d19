# Active Task: Berry Sextic Genus-2 Classification

- Status: complete
- Updated: 2026-07-15
- Task id: `berry-sextic-genus2-classification-20260715`
- User goal: classify all rational fourth-distance points on the single selected Berry degree-6 pilot by solving the two exact genus-2 obligations over `K=Q(i)`.
- Scope: only `v^2=g6(t)` and `i*v^2=g6(t)` with `t in P^1(Q)`, including projective charts, maps, converse, local/global arithmetic, rational-`t` enforcement, and reconstruction.
- Policy scope: `berry-sextic-genus2-classification-20260715`
- ExecutionPolicy: external
- ExecutionPolicy source: user instruction and project `AGENTS.md`
- Execution protocol skills: `agent-memory-stack-lite-demo`, `context-memory-index`
- Lite Demo role: memory-only
- Controller boundary: the top-level agent delegates exactly one narrow task at a time through `ask_codex.sh` using `gpt-5.6-luna` and `reasoning=max`, then independently verifies the result.

## Stable Module Protection

- Protected behavior: `wl587`-`wl596`, the accepted post-wl596 route audit, Berry literature note, and committed pilot feasibility certificate remain frozen inputs.
- Necessity: the new task needs only new task-local proof artifacts and narrowly justified extensions of the Berry pilot tooling.
- Evidence chain: commits `2d70086`, `68cb1e9`, and `44078d2` separately preserve the three required initial themes; the worktree was clean at task start.
- Impact scope: new files under this task directory plus Berry-specific scripts/tests only when a B-stage proof obligation requires them.
- Do not change: numbered `wl` checkpoints, other Berry sextics, general D19 theorem status, or unrelated rank/Selmer machinery.
- Regression check: focused tests, proof-enabled Sage checks where applicable, targeted Ruff/format, `git diff --check`, and final full pytest if repository code is integrated.

## Current Step

Complete. B5 outcome: `precise_genus2_arithmetic_blocker`.

## Completed Steps

- Initial repository gate: the three accepted themes are separately committed as `2d70086`, `68cb1e9`, and `44078d2`; the worktree is clean.
- Frozen input audit: the pilot certificate proves the exact support set `{1,i}` and records the two genus-2 obligations without claiming their point sets or ranks.
- B0 draft: `b0-covering-certificate.md`, `scripts/theory/berry_sextic_b0.py`, and its focused test pass their internal exact checks; Controller accepted the exact partial results and retained the unresolved dyadic branch as the final blocker.
- B0 reduction audit: actual good reduction is proved outside `{(1+i),(94*i-169)}` and actual bad reduction at `(94*i-169)` is proved for both twists; `(1+i)` is the exact remaining blocker.
- Rejected B0 overclaim: `PGL2(O)\PGL2(K)/PGL2(O)` has one radial parameter, but the right integral factor acts on the branch sextic. Without a stabilizer/invariance proof or a complete lattice-direction audit, the fixed-center `r` strata do not classify every possible generalized model.
- Final Controller decision: the complete covering data and odd-prime reduction result are accepted; actual reduction at `(1+i)` remains unresolved for both twists, so B1-B4 are not entered.

## Next Exact Step

None; task complete at the accepted B5 blocker. Reopening requires the exact
dyadic quotient-lattice/stable-model theorem stated in `final-outcome.md`.

## Allowed Changes

- This task anchor, its task-local reports, and its pointer in `docs/codex/index.md`.
- Berry-pilot-specific proof-data scripts and focused tests required by an accepted B0-B4 result.
- Thematic commits after Controller acceptance of each phase.

## Forbidden Changes

- Do not create `wl597` or edit `wl587`-`wl596`.
- Do not process other Berry sextics or claim a degree-6 family theorem.
- Do not invoke Bombieri-Lang.
- Do not use bounded searches, heuristic analytic ranks, or software failure as exclusion evidence.
- Do not discard infinity, node, factor-zero, or degenerate-chart fibers.
- Workers must not invoke Codex, `ask_codex.sh`, subagents, or delegation skills.

## Validation Gates

- B0: exact equations, projective smoothness/singularity audit, maps, converse, bad places, exceptional fibers, and trivial points.
- B1: exact local solubility and `K`-rational torsion for both curves, tied to the global classification.
- B2: rigorous Jacobian torsion, 2-Selmer/rank upper bounds, generators/saturation as required, with proof flags.
- B3: exact enforcement of `t in P^1(Q)` by a justified global method.
- B4: complete surviving rational-`t` enumeration and exact four-distance reconstruction.
- B5: exactly one of `selected_berry_sextic_excluded`, `strict_four_distance_point_found`, or `precise_genus2_arithmetic_blocker`.

## Rejected Paths

- Polynomial factorization as a claimed Jacobian decomposition.
- Detached local-prime tables.
- Unrestricted `K`-point searches without rational-`t` enforcement.
- Coordinate rewrites or tool capability inventories presented as mathematical progress.
