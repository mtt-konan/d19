# Active Task: Berry Sextic Genus-2 Classification

- Status: active
- Updated: 2026-07-16
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

The bounded C_1 Magma gate is recorded in
`segmented-free-magma-route-audit.md` with outcome
`segmented_free_magma_route_ready`. Through proxy `127.0.0.1:7897`, the four
field/order, S-unit, local, and scalar-rebuild stages complete in respectively
`0.06`, `0.78`, `0.07`, and `0.03` Magma seconds. The earlier monolithic
`TwoSelmerGroup` timeout remains only a service-limit observation. No Selmer
result or local Kummer image is claimed.

## Completed Steps

- Initial repository gate: the three accepted themes are separately committed as `2d70086`, `68cb1e9`, and `44078d2`; the worktree is clean.
- Frozen input audit: the pilot certificate proves the exact support set `{1,i}` and records the two genus-2 obligations without claiming their point sets or ranks.
- B0 draft: `b0-covering-certificate.md`, `scripts/theory/berry_sextic_b0.py`, and its focused test pass their internal exact checks; Controller accepted the exact partial results and retained the unresolved dyadic branch as the final blocker.
- B0 reduction audit: actual good reduction is proved outside `{(1+i),(94*i-169)}` and actual bad reduction at `(94*i-169)` is proved for both twists; `(1+i)` is the exact remaining blocker.
- Rejected B0 overclaim: `PGL2(O)\PGL2(K)/PGL2(O)` has one radial parameter, but the right integral factor acts on the branch sextic. Without a stabilizer/invariance proof or a complete lattice-direction audit, the fixed-center `r` strata do not classify every possible generalized model.
- Final Controller decision: the complete covering data and odd-prime reduction result are accepted; actual reduction at `(1+i)` remains unresolved for both twists, so B1-B4 are not entered.
- User correction: keep commit `dccbd9a` as a B0 checkpoint, but withdraw the route claim that full dyadic stable reduction must precede B1/B2. An arithmetic blocker is allowed only if exact 2-Selmer progress specifically fails at the dyadic local Kummer image.
- Post-B0 feasibility audit: `C_i(K_(1+i))` is empty by an exact valuation/unit-square obstruction; exact good-prime Jacobian orders give `J_1(K)_tors=J_i(K)_tors=0`; the model-supported finite set is `{(1+i),(94*i-169)}` and the conservative Berry-closed support adds `(-94*i-169)`; no exact genus-2 Jacobian 2-Selmer route is installed. Minimality of the support is not claimed.
- Free Magma audit: the public Calculator accepts automated XML submissions and exactly constructs the selected `JacHyp` over `Q(i)`; the fast probe confirms `TwoSelmerGroup` and `TwoCoverDescent` are present, while `LocalKummerImage` is absent. The full `TwoSelmerGroup(J)` call is terminated by the public 60-second limit, and the `Al := "TwoSelmerGroupData"` intermediate-data path rejects non-rational base fields. This is a service-limit/capability result, not an arithmetic blocker.
- Segmented C_1 gate: local Sage independently verifies the degree-12 field, maximal-order discriminant `5019340374016`, trivial class group, unit group `C4 x Z^5`, complete support decomposition, and strict local quotient targets `5` at `(1+i)` and `2` at `(94*i-169)`. The model support has six primes above `Q(i)` and squareclass dimension `12`; the conservative Magma support has ten primes and dimension `16`. Magma independently computes the class, unit and S-unit data in `0.78` seconds and emits generators in the fixed absolute-field power basis. The public global timeout remains a service limit, not an arithmetic blocker.
- Q1 correction: the conservative `16` dimensions are explicitly only the ambient `V_S` S-unit coordinate space. The exact constant quotient `F_L=L^*/(L^{*2}K^*)`, the separate norm-square kernel, the local fake quotient at `pi`, and the ambient-to-local localization map are now defined without claiming their dimensions or matrices. `D_inf` is retained only as a fake-map kernel inclusion with trivial fake class.
- Q2a: `q2a-local-kummer-generators.md` constructs the tangent-normalized local classes of `D_12` and `D_r`, gives the full four-dimensional `H_pi` basis, and proves the two classes are independent and complete for `I_pi` using the accepted local dimension 2. Global ambient localization remains open.
- Q2b audit: `q2b-coordinate-audit.md` first identified the missing fixed payload. `q2b-fixed-basis-report.md` now records the successful Magma transcript, all sixteen absolute power-basis S-unit elements, multiplication table, and `K` embedding.
- Q2c: `q2c-constant-norm-localization.md` computes and verifies `M_const`, `M_norm`, the odd-`pi` localization map, and global norm-square ambient lifts for both Q2a classes. The canonical lifts are `epsilon_1` for `beta_12` and `epsilon_1+epsilon_4` for `beta_r`.

## Next Exact Step

Q1 has been corrected in `q1-fake-descent-certificate.md`: the conservative
16 dimensions are only the ambient `V_S` coordinates. The exact constant
quotient, norm-square kernel, local fake quotient, and localization map are
separate objects with dimensions/matrices not yet computed.

Q2 is complete at the odd bad prime: its local image has explicit generators,
and the corrected global ambient/norm/localization comparison is verified.
Q3a1 is now recorded in the independent anchor
`docs/codex/tasks/berry-q3a-dyadic-kernel-20260715/active-task.md` and report
`q3a1-dyadic-fake-kernel-boundary.md`. It fixes the dyadic algebra and formal
maps but deliberately does not claim a dyadic basis, local image, or kernel.
Q3a2 is now exact.  The primary quotients of the two certified global primes
above `2` give `dim W_varpi=16`, `rank B_varpi=4`, `dim F_varpi=12`, and
`dim H_varpi=8`.  The exact sixteen-column global ambient localization matrix
has rank `16`, and its fake quotient has rank `12`.  The report and payload
are in the independent Q3a anchor directory.  No Selmer or rank conclusion is
formed from Q2/Q3a1/Q3a2.
The former `precise_C1_etale_descent_blocker` judgment in `692f49d` is
withdrawn as a modeling error and retained only as a historical failure
record.  The exact global-prime completion matrices now replace that route.
The finite-precision local `Factorization(g6v)` display and the
`E_2 subset E_4` branch remain excluded as required inputs.

## Completed Q3a2

The prior `precise_C1_etale_descent_blocker` judgment from commit `692f49d`
remains withdrawn as a modeling error.  Q3a2 is completed by
`q3a2-dyadic-diagonal-norm-matrices.md`, its exact Sage producer, serialized
payload, standalone verifier, and focused test.

Q3a3 now has one Controller-verified nonzero class,
`H_varpi=(0,1,1,1,0,1,1,0)`, coming from the exact local point above `t=i`.
The independent exact halving audit now proves
`D_inf not in 2J(Q_2(i))`, so the fake kernel has a certified nonzero line and
`dim(I_varpi)<=4`.  The exact group-scheme sequence now completes the kernel:
Q3a2's injective constant restriction identifies the local sign quotient,
and the relative factor degrees `2,4` make its norm trivial.  Thus the
cohomological fake kernel is one-dimensional and is realized by `D_inf`.
Consequently

```text
ker(delta_varpi)=<D_inf>,
dim I_varpi=4.
```

This completes Q3a only.  The bounded checkpoint now requires Controller
review before any Q3b-Q4 task is selected; no global Selmer or rank conclusion
has been formed.


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
