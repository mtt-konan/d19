# d19 Counterexample-First Exploration Goal Prompt

> **Purpose:** This is a long-form brief for a Codex `/goal` run focused on
> finding, constructing, or explaining the absence of counterexamples. Keep the
> actual `/goal` command short and point it here.

## Recommended `/goal` Command

Use this short command from the repository root:

```text
/goal 以“反例优先”的方式探索 d19/Harborth 方向。以 docs/superpowers/plans/2026-06-07-counterexample-first-exploration-goal.md 为控制说明，先主动找真反例或 GEN-CLOSURE 闭合命中，再找近反例、边界族和会打破筛/归约的样本；允许分派 subagent 并行搜索；过程少输出，最终集中产出文档合集、候选数据和下一步证明/构造路线。
```

If a token budget can be set, use at least `100000` tokens for a serious first
pass. If budget is limited, run only Phase 1-3 and save the remaining phases as
next tasks.

## Short Answer

Yes, this problem is suitable for a counterexample-first workflow, but the
target must be stated carefully.

Ordinary-language version:

```text
先不要急着证明“永远不可能”。先尽量找一个会闭合的例子。
如果找不到，就把所有差一点成功的例子收集起来，看它们到底卡在哪里。
真正有价值的不是“又没找到”，而是从“为什么每次都差一点”里面提炼出新定理。
```

However, "not finding a counterexample" is not a proof by itself. It becomes
useful only when it leaves behind one of these:

- a real counterexample candidate;
- a family that gets arbitrarily close to closure;
- a sharp obstruction pattern that can be turned into a theorem;
- a local-global residual set that tells us which proof methods are too weak;
- a better generator that attacks the part of the search space old scans barely
  touched.

## What Counts As A Counterexample Here

Use three levels. Do not mix them.

### Level 1: Full Harborth Counterexample

This would be an actual point in the plane whose distances to the four unit
square vertices are all rational.

In the integer chain language, it corresponds to positive integers satisfying
the full four-distance structure and the correct geometric closure relation.

If found, stop and verify independently with exact arithmetic.

### Level 2: GEN-CLOSURE Hit

For a fixed `(A, B)`, enumerate all integer concordant `N` such that:

```text
N^2 + A^2 = square
N^2 + B^2 = square
```

Then look for two `N` values satisfying the full-plane closure condition:

```text
{N1 + N2, |N1 - N2|} intersects {A + B, |A - B|}
```

This is the right target after the audit. The old condition
`N1 + N2 = A + B` only covers points inside the square. Full-plane attack must
use the four-relation GEN-CLOSURE condition.

### Level 3: Near-Counterexample / Breakpoint

If Level 1-2 fail, collect samples that almost work:

- at least two concordant `N` values;
- small closure delta:
  `min |N_i +/- N_j - (A +/- B)|`;
- survivor after `gcd_aware_kills`;
- survivor after full-plane modular closure sieve;
- high `k = number of concordant N`;
- high rank / unusual F2 signature;
- non-coprime `gcd(A,B)` classes where existing filters are weakest;
- examples where a "safe" or "obvious" heuristic fails.

Near-counterexamples are not failures. They are the raw material for the next
proof attempt.

## Current Best Attack Surface

Based on the 2026-06-07 theory audit, prioritize these zones:

1. **Full-space non-coprime pairs.**
   Reduced/coprime is not WLOG. A minimal global counterexample only forces
   `gcd(A,B,N1,N2)=1`, not `gcd(A,B)=1`.
2. **GEN-CLOSURE, not sum-only closure.**
   The full-plane relation includes sums and differences against both
   `A+B` and `|A-B|`.
3. **Residual pairs after the sound three-stage pipeline.**
   The known pipeline is:
   `gcd_aware_kills -> chain_closure_mod_sieve(full_plane=True) -> exact GEN-CLOSURE`.
4. **Local-global survivors.**
   Some pairs survive every tested modular obstruction. These are better
   proof targets than easy pairs killed by mod 9 or 25.
5. **High-multiplicity multi-N pairs.**
   More concordant `N` values means more chances to satisfy a closure relation.
6. **Near-zero closure deltas.**
   If exact closure never appears, the distribution of closest misses may reveal
   a hidden congruence or factorization obstruction.

## What Not To Do

- Do not treat finite 0 hits as proof.
- Do not use old sum-only scripts for full-plane conclusions.
- Do not rely on default `concordant` CLI as an exhaustive proof path unless
  `--concordant-method factor` or proof-status factor path is explicitly used.
- Do not let `safe_sieve` classify arbitrary non-coprime manual pairs as a
  strong proof result.
- Do not only extend bounds blindly. Every large scan should also collect
  near-miss structure.

## Suggested Document Set

Create:

```text
docs/explorations/YYYY-MM-DD-counterexample-first/
```

Recommended files:

```text
docs/explorations/YYYY-MM-DD-counterexample-first/README.md
docs/explorations/YYYY-MM-DD-counterexample-first/search-log.md
docs/explorations/YYYY-MM-DD-counterexample-first/candidates.md
docs/explorations/YYYY-MM-DD-counterexample-first/near-misses.md
docs/explorations/YYYY-MM-DD-counterexample-first/negative-evidence.md
docs/explorations/YYYY-MM-DD-counterexample-first/proof-leads.md
docs/explorations/YYYY-MM-DD-counterexample-first/subagent-notes/
```

If data is produced, save machine-readable outputs under:

```text
results/counterexample_first/YYYY-MM-DD/
```

Every result file must include:

- date;
- command;
- code commit;
- max bound;
- coprime/full-space scope;
- closure predicate used;
- whether concordant `N` enumeration was exact or bounded.

## Subagent Strategy

Use subagents when available. The controller keeps the global scoreboard and
final judgment; subagents search independent attack surfaces.

Recommended slices:

1. `full-space-scan-extension`
   - Extend or reproduce `noncoprime_full_scan_fast.py` at a chosen bound.
   - Verify it uses full-plane GEN-CLOSURE.
   - Save aggregate counts and any hits.
2. `near-miss-min-delta`
   - Modify or wrap existing exact pair enumeration to record closest closure
     deltas, not just exact hits.
   - Focus on residual pairs after `gcd_aware_kills` and full-plane mod sieve.
3. `gcd-strata-search`
   - Split non-coprime space by `g = gcd(A,B)` and identify weak strata:
     especially `3|g`, `4|g`, `12|g`, and `D_g = 1`.
4. `high-k-multi-n`
   - Search for pairs with unusually many concordant `N` values.
   - Check whether high `k` improves closure delta.
5. `partner-graph-full-plane-recheck`
   - Recheck old partner graph no-hit data under full-plane GEN-CLOSURE rather
     than sum-only closure.
6. `constructive-families`
   - Try to generate families satisfying one or more closure relations first,
     then test whether concordant square conditions can be forced.
7. `filter-breakers`
   - Look for pairs where old/heuristic filters disagree with exact
     GEN-CLOSURE, especially non-coprime manual pairs.

Subagent output schema:

```text
Slice:
Goal:
Files inspected:
Commands run:
Search domain:
Closure predicate:
Exact or bounded:
Hits:
Top near-misses:
Observed patterns:
What this rules out:
What this does not rule out:
Recommended next attack:
Plain-language summary:
```

Controller responsibilities:

- Do not let subagents independently declare "no counterexample globally".
- Re-run or independently verify any hit.
- Merge near-miss tables into a single ranked list.
- Convert repeated near-miss patterns into candidate lemmas.
- Keep final output concise; put details in files.

## Phase 1: Establish Baseline And Reproducibility

Run:

```bash
git status --short --branch
git rev-parse HEAD
uv run pytest -q
```

Then reproduce one known full-space summary at a small bound:

```bash
PYTHONPATH=src uv run python scripts/multi_n/noncoprime_full_scan_fast.py \
  --max-hyp 10000 \
  --workers 1
```

Expected:

- no closure hits at this bound;
- output saved under `results/multi_n/full_scan_max10000.json`;
- the script uses `find_killer_modulus(..., full_plane=True)`.

Do not move to larger scans until the small baseline is understood.

## Phase 2: Exact Counterexample Search

Attack exact GEN-CLOSURE hits.

Primary command:

```bash
PYTHONPATH=src uv run python scripts/multi_n/noncoprime_full_scan_fast.py \
  --max-hyp <BOUND> \
  --workers <N>
```

Recommended staged bounds:

```text
10000 -> 100000 -> 1000000 -> 5000000 if resources allow
```

For every closure hit:

1. Save `(A, B, gcd(A,B), concordant_N)`.
2. Verify each `N` satisfies both square conditions.
3. Verify the exact GEN-CLOSURE relation.
4. Convert the integer data back into the plane/rational-distance statement.
5. Run an independent check using a second script or small ad hoc exact
   arithmetic verifier.
6. If verified, stop the broad scan and write a candidate report.

## Phase 3: Near-Miss Search

If no exact hit appears, collect closest misses.

For each pair with at least two exact concordant `N`, compute:

```text
delta = min(
  |N_i + N_j - (A+B)|,
  |N_i + N_j - |A-B||,
  ||N_i - N_j| - (A+B)|,
  ||N_i - N_j| - |A-B||
)
```

Save the top 100 or top 1000 smallest deltas with:

- `(A, B)`;
- `gcd(A,B)`;
- `concordant_N`;
- relation type;
- delta;
- `D_g`;
- which stage killed or did not kill it;
- factorization of relevant values if cheap.

This is important because "no exact hit" only becomes useful when the miss
pattern is visible.

## Phase 4: Constructive Search

Try the reverse direction:

```text
first force one closure relation, then ask if square conditions can survive.
```

Examples:

- Pick `A, B, N1`, set `N2 = A+B-N1` or `N2 = |A-B|-N1`, then test whether
  both `N1` and `N2` are concordant for `(A,B)`.
- Pick a gcd stratum `g`, enforce the required divisor `D_g` on the closure
  target, then solve for concordant `N`.
- Generate high-rank or strongly concordant candidate `(A,B)` first, then test
  whether any two integer square-x points close.

The constructive route may fail, but it can reveal which equation becomes
overdetermined.

## Phase 5: Filter-Breaker Search

Find examples that break naive statements even if they do not break the main
conjecture.

Targets:

- non-coprime pairs rejected by old coprime-only `safe_sieve` but not by
  gcd-aware logic;
- pairs surviving all tested modular closure sieves;
- pairs where sum-only says no but full-plane relation still survives;
- high-rank pairs with few integer `N`;
- high-`k` pairs with no closure.

These examples are valuable because they prevent future proofs from using
false shortcuts.

## Phase 6: Convert Absence Into Proof Leads

At the end, do not say "therefore no counterexample." Instead, produce proof
leads:

- Which gcd strata dominate survivors?
- Which closure relation comes closest most often?
- Are near misses always blocked by a small modulus, parity, or divisor?
- Does `delta` have a common factor pattern?
- Are survivors concentrated in `D_g = 1`, `12|g`, or another family?
- Does high `k` fail because `N` values are too large, too sparse, or locked in
  wrong congruence classes?
- Can any observed pattern be stated as a lemma with exact assumptions?

## Hit Report Format

If a hit is found:

```text
Severity: potential counterexample
Pair:
gcd:
Concordant N set:
Witness N1,N2:
Relation:
Square checks:
Plane reconstruction:
Independent verification:
Files/commands:
Remaining doubts:
```

## Near-Miss Report Format

For near misses:

```text
Rank:
Pair:
gcd:
Concordant N set:
Closest relation:
Delta:
Pipeline stage:
Why it is interesting:
Possible lemma:
```

## Progress And Silence Rules

Do not output conclusions after each scan. Save results to the exploration
directory and only send short progress updates if needed.

Good progress update:

```text
正在跑 full-space GEN-CLOSURE 和 near-miss delta 收集，结果先写入 docs/explorations/...，最后统一汇总。
```

Avoid:

```text
这轮又证明没有反例。
```

## Completion Criteria

Do not mark the goal complete until:

- exact hit search was attempted or explicitly bounded by resources;
- near-miss data exists, not just a 0-hit summary;
- non-coprime/full-space scope is clearly separated from reduced/coprime scope;
- old sum-only closure is not used for full-plane claims;
- every produced result has command, commit, bound, and predicate metadata;
- final docs explain what was searched and what remains unsearched;
- final docs contain either verified counterexample candidates or ranked proof
  leads from near misses.

## Final Answer Shape

The final chat response should be short:

```text
反例优先探索已完成。文档合集在 ...
没有/发现了 GEN-CLOSURE 命中。最重要的 near-miss 是 ...
下一步最值得证明的是 ...
```

Put all detailed tables and reasoning in the document set.
