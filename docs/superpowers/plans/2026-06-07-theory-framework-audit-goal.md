# d19 Theory Framework Audit Goal Prompt

> **Purpose:** This document is the long-form brief for a Codex `/goal` run.
> Keep the actual `/goal` command short and point it here. Do not paste this
> whole file into the goal objective.

## Recommended `/goal` Command

Use this short command from the repository root:

```text
/goal 审查 d19 仓库的理论框架是否存在会推翻上层结论的致命错误。以 docs/superpowers/plans/2026-06-07-theory-framework-audit-goal.md 为控制说明，重点查：错误归约、不安全筛、有限实验被当成证明、分支被过早写死、代码和文档结论不一致。忽略不影响结论的小证明瑕疵。允许分派 subagent 分支审查；过程少输出，最终集中产出文档合集和总报告。
```

If the UI accepts an explicit budget, use a large budget. A realistic first
pass is `80000` to `120000` tokens. If the budget is smaller, split the audit
by branch rather than trying to cover everything shallowly.

## Why This Should Be A Goal

This task is too large for a single normal turn because it needs to:

- read the current direction docs and the historical worklogs;
- compare high-level claims against the implementation;
- distinguish proven facts, finite experiments, conjectures, and abandoned
  routes;
- look for dependency breaks that could invalidate later conclusions;
- produce a durable audit artifact rather than only a chat summary.

The goal is not to prove or disprove Harborth's conjecture. The goal is to
verify whether the repository's current internal theory map is sound enough to
support the next round of exploration.

## Main Audit Objective

Audit the d19 repository as a self-built theoretical framework around the
rational-distance-to-square problem. Look for fatal or near-fatal errors that
would directly affect top-level conclusions, route status, or future search
strategy.

Use plain Chinese. The project contains many math terms, but the report should
explain them in ordinary language first, then give the exact formula or file
evidence.

## Reporting Mode

Do not print conclusions after every phase. This audit should be document-first:

- Keep intermediate conclusions in working documents, not in chat.
- Only send short progress updates when the environment requires a response,
  when a blocker appears, or when a fatal candidate needs the controller to
  pause and trace it deeply.
- Do not paste subagent reports into chat. Save them as files and summarize
  them only in the final response.
- The final answer should be a short pointer to the generated document set,
  plus the top fatal/high-risk results. The full reasoning should live in the
  audit files.

The preferred user experience is:

```text
审查过程中少打扰；最后一次性给出结论、证据链、风险分级和后续建议。
```

## Subagent Strategy

Use subagents when available. The controller agent should preserve context by
owning the global claim ledger and assigning narrow, independent audit slices to
fresh subagents. If no subagent tool is available in the current environment,
run the same slices serially.

Do not give a subagent the whole repository brief unless necessary. Give each
subagent:

- its branch or claim slice;
- the exact files to inspect first;
- the severity standard from this document;
- the required output schema;
- permission to run only light, targeted commands unless explicitly needed.

Subagents should write their findings to files under:

```text
docs/audits/YYYY-MM-DD-theory-framework-audit/
```

Recommended subagent slices:

1. `reduction-chain`: point/chain/reduced-pair/concordant reductions.
2. `safe-filters`: safe-pair, modular, gcd-aware, and proof-status filters.
3. `concordant-multi-n`: multi-`N`, high-rank, closure condition, literature
   translation.
4. `chain-fast-baseline`: baseline search semantics, numpy/Python boundaries,
   near-miss/result storage claims.
5. `partner-graph`: partner graph, `G_M`, islands, component claims.
6. `legacy-paused-routes`: `parametric`, `ec`, `chain`, and whether their
   paused status is justified.
7. `advanced-directions`: finite descent, Sha/Selmer, Chabauty, Heegner,
   Brauer-Manin, K3, and whether any direction was incorrectly declared dead.

Subagent output schema:

```text
Slice:
Files inspected:
Commands run:
Claims checked:
Fatal findings:
High-risk findings:
Medium/low findings:
Non-issues worth noting:
Open uncertainties:
Recommended updates to main claim ledger:
Plain-language summary:
```

Controller responsibilities:

- Create or maintain the master claim ledger.
- De-duplicate overlapping subagent findings.
- Re-check any fatal or high-risk finding directly before accepting it.
- Keep final severity decisions centralized.
- Do not let subagents decide that the whole project is sound or unsound; they
  only judge their slice.
- Merge all slice notes into a final report and appendices.

## What Counts As Fatal

Treat an issue as fatal when it can directly invalidate a high-level conclusion
or make a branch status wrong.

Examples:

- A claimed necessary condition is not actually necessary, so a "safe" sieve
  could silently remove a real solution.
- A reduction from the square-distance problem to `(A, B, N)` loses cases or
  adds hidden assumptions without saying so.
- A finite scan result is written as if it were a proof for all cases.
- A branch is marked as dead or exhausted because of a result that only applies
  to a narrower setting.
- A code path used to generate authoritative data does not implement the math
  condition described in the docs.
- A later conclusion depends on an older worklog that has since been corrected,
  but the later conclusion was not updated.
- A "no solution" label means "not found in this bound" in code but is used as
  "proved impossible" in docs.

## What Does Not Matter For This Audit

Do not spend much time on small issues that do not change conclusions.

Examples:

- Notation inconsistency where the formula is still unambiguous.
- A proof sketch missing a routine algebra step, if the statement is separately
  tested or easy to patch.
- Performance improvements, unless performance limitations caused a false
  mathematical claim.
- Old archived wording that is clearly marked historical and no current doc
  relies on it.
- Minor CLI ergonomics, formatting, or style.

## High-Level Conclusions To Stress-Test

Start from these current repository claims and verify their dependency chains.
For each one, classify it as `proven`, `empirical`, `engineering baseline`,
`conjectural`, `obsolete`, or `unclear`.

1. `concordant` is the active main direction.
2. `chain-fast` is the trusted baseline searcher for the four-vertex square
   problem.
3. `parametric`, `ec`, and `chain` are currently paused rather than deleted.
4. The pair-level `mod1680` concordant pre-sieve is an empty sieve and should
   not be treated as a useful runtime filter.
5. The reduced `(A, B)` safe-pair sieve conditions are safe for the full
   chain-oriented setting:
   `A` odd, `B` odd, and `(A + B) % 4 == 0`.
6. A full square-chain counterexample would imply at least two concordant `N`
   values for the same `(A, B)`, with `N1 + N2 = A + B`.
7. Multi-`N` pairs exist and are meaningful, but currently observed examples do
   not satisfy the closing condition.
8. Positive rank or strong concordance explains why many half-solutions can
   exist, but it does not by itself give a full square solution.
9. `proof_status` and fast-core are engineering tools for large-scale
   diagnosis, not a global proof of Harborth's conjecture.
10. Partner-graph / component / island results are experimental structure
    evidence unless a file explicitly proves the corresponding algebraic
    statement.
11. Long-term directions such as Heegner points, Chabauty, Brauer-Manin, finite
    descent, and K3 viewpoints are not "dead" merely because an early local
    experiment was negative.
12. The repository has not found a four-vertex square solution, and it should
    not claim the conjecture is proved unless a complete proof artifact exists.

## Required Source Map

Use these files as the first-pass source map:

- `README.md`
- `docs/DIRECTIONS.md`
- `docs/PROJECT_STATUS.md`
- `docs/CURRENT_FINDINGS.md`
- `docs/GLOSSARY.md`
- `docs/MATH.md`
- `docs/MULTI_CONCORDANT_N_STRATEGY.md`
- `docs/MULTI_N_FILTER_LADDER.md`
- `docs/PARTNER_GRAPH_THEORY.md`
- `docs/PROOF_STATUS_FAST_MODE.md`
- `docs/OPEN_DIRECTIONS.md`
- `docs/THEORY_DIRECTIONS.md`
- `docs/THEORY_DIRECTIONS_ADVANCED.md`
- `docs/IMPLEMENTATION.md`
- recent worklogs, especially `docs/work-logs/073-*.md` through
  `docs/work-logs/104-*.md`
- relevant tests under `tests/`
- relevant implementation under `src/rational_distance/`
- relevant scripts under `scripts/`
- authoritative result summaries under `results/`

Do not bulk-read giant result files unless needed. Prefer summaries, schemas,
catalogs, tests, and small representative samples.

## Required Method

### Phase 1: Build A Claim Ledger

Create a table of major claims.

For each claim, record:

- claim text in plain Chinese;
- exact source file and line reference;
- status: proven, empirical, engineering baseline, conjectural, obsolete, or
  unclear;
- upstream dependencies;
- downstream conclusions that rely on it;
- whether code/tests/results support it;
- possible fatal failure mode.

The claim ledger is the backbone of the audit. Do not jump directly into
random proof checking.

If using subagents, the controller should create the first ledger skeleton
before dispatching. Subagents then fill in branch-specific evidence and risk
notes.

### Phase 2: Check Reductions Before Checking Computation

Prioritize the math translations that connect one layer to another:

- point-to-square-distance formulation;
- chain / 4-chain formulation;
- reduced `(A, B)` pair generation;
- fixed `(A, B)` plus common-leg `N`;
- concordant curve
  `Y^2 = X(X + A^2)(X + B^2)` with `X = N^2`;
- full closure condition `N1 + N2 = A + B`;
- any normalization or gcd reduction.

For each reduction, ask:

- Is it one-way or two-way?
- Does it require positivity, coprimality, parity, primitive triples, ordering,
  or normalization?
- Are those assumptions stated where later conclusions use the reduction?
- Does the code enforce the same assumptions?
- Could a real counterexample fall outside the reduced search domain?

### Phase 3: Audit The "Safe" Filters

For every filter that is called safe, necessary, or proof-producing:

- identify the exact theorem or proof sketch;
- identify the exact implementation;
- identify the tests that would catch false rejection;
- check if the filter is safe only under a narrower mode;
- check if docs clearly distinguish full concordant view from full-chain view.

Pay special attention to:

- reduced `(A, B)` safe-pair sieve;
- chain closure modular sieves;
- gcd-aware mod-12 / `D_g` sieve;
- `proof_status` no-solution labels;
- any filter moved from `chain-fast` to `concordant` or vice versa.

### Phase 4: Separate Proofs From Experiments

For each major conclusion, label it honestly:

- `proved in repo`: complete argument is present and assumptions are explicit;
- `proved externally`: relies on cited theorem or paper;
- `tested`: finite scan only;
- `engineering confidence`: tests and code behavior support it, but not a math
  theorem;
- `hypothesis`: plausible direction, not settled;
- `obsolete`: historical result superseded by later work.

Look for wording drift. A common failure mode is:

```text
"no counterexample up to bound" -> "probably impossible" -> "impossible"
```

Flag any place where that drift affects current direction choices.

### Phase 5: Code And Test Cross-Check

Run light verification commands first:

```bash
git status --short --branch
uv run pytest -q
uv run ruff check .
```

Then run targeted commands only when they clarify a claim. Examples:

```bash
uv run python scripts/search.py concordant --pair 264,420 --no-progress
uv run python scripts/search.py concordant --max-hyp 100 --ec-bound 100000 --no-progress
uv run python scripts/search.py chain-fast --max-hyp 200 --no-progress
uv run python scripts/prove_no_solution.py --max-hyp 100 --db .cache/audit-proof-status.sqlite3 --force --no-progress
```

Avoid huge reruns unless the goal explicitly has enough budget and time. The
audit is about logical soundness first, not extending search bounds.

### Phase 6: Branch Status Review

For each branch or direction, answer:

- What was it trying to prove or find?
- What evidence currently supports it?
- What evidence currently weakens it?
- Is it active, baseline, paused, archived, or still open?
- Is that status justified by a fatal mathematical reason, an engineering
  tradeoff, or just current prioritization?
- Could the branch still matter later as a counterexample generator, proof
  tool, or sanity check?

Branches to cover:

- `concordant`
- `chain-fast`
- `proof_status`
- multi-`N` / high-rank concordant curves
- safe-pair / modular / gcd-aware sieves
- partner graph / `G_M` / island analysis
- `parametric`
- `ec`
- `chain`
- finite descent / Sha / Selmer / Chabauty / Heegner / Brauer-Manin / K3

### Phase 7: Produce Durable Artifacts

Create a document set under:

```text
docs/audits/YYYY-MM-DD-theory-framework-audit/
```

Recommended files:

```text
docs/audits/YYYY-MM-DD-theory-framework-audit/README.md
docs/audits/YYYY-MM-DD-theory-framework-audit/claim-ledger.md
docs/audits/YYYY-MM-DD-theory-framework-audit/risk-register.md
docs/audits/YYYY-MM-DD-theory-framework-audit/branch-status.md
docs/audits/YYYY-MM-DD-theory-framework-audit/commands-run.md
docs/audits/YYYY-MM-DD-theory-framework-audit/subagent-notes/
```

The main `README.md` should include:

- executive summary in plain Chinese;
- fatal findings, if any;
- near-fatal or high-risk findings;
- non-fatal cleanup items;
- branch status matrix;
- claim ledger summary;
- exact commands run and results;
- recommended next exploration priorities;
- explicit statement of residual uncertainty.

The appendices should preserve enough detail that future agents can continue
without re-reading the entire repository from scratch.

## Finding Format

Every serious finding must use this structure:

```text
Severity: fatal | high | medium | low | non-issue
Claim:
Where it appears:
Why it matters:
Evidence:
Reproduction or check:
Affected top-level conclusions:
Recommended action:
Plain-language explanation:
```

Use `fatal` sparingly. A fatal issue should change what the project believes or
which branch is considered closed.

## Output Style

Write in Chinese. Use simple explanations before technical formulas.

Preferred wording:

```text
普通话说，这一步是在把“找一个点”换成“找四个整数能不能围成闭环”。
真正要检查的是：这个替换有没有漏掉某些点，或者偷偷加了额外条件。
```

Avoid vague statements such as:

```text
显然成立
应该没问题
这个方向已经死了
实验说明不可能
```

Replace them with:

```text
在 reduced pair 这个前提下成立。
目前只验证到 max_hyp=...
这个方向现在不是主线，但没有被数学上排除。
这里需要补一个明确的一向/双向说明。
```

## Guardrails

- Do not claim a global proof from finite scans.
- Do not treat archived worklogs as current truth unless current docs still
  depend on them.
- Do not trust names like `safe`, `proof`, or `no_solution` without checking
  their exact scope.
- Do not rewrite code unless a tiny diagnostic script is necessary. The goal is
  audit, not implementation.
- Do not get stuck on formatting or minor proof polish.
- If a potential fatal issue appears, stop expanding breadth and trace that
  issue deeply enough to confirm or downgrade it.
- If the same blocker repeats for multiple goal turns, report it honestly
  instead of pretending the audit is complete.

## Progress And Silence Rules

Do not output phase-by-phase conclusions in chat. Prefer this cadence:

1. At the start, say only that the audit will run mostly silently and write
   intermediate material to `docs/audits/...`.
2. During the audit, stay quiet unless blocked, unless a potential fatal issue
   requires focused tracing, or unless the platform requires a progress message.
3. If a progress message is necessary, say what is being processed, not what
   the conclusion is.
4. At the end, provide the report paths and a concise final summary.

Good progress update:

```text
正在把 safe filters 和 proof_status 的结论链拆到 claim ledger，暂不输出判断，最后统一汇总。
```

Avoid:

```text
safe_sieve 看起来没问题，partner graph 可能有风险……
```

## Completion Criteria

Do not mark the goal complete until all are true:

- The claim ledger exists in the final report or appendix.
- Every high-level conclusion listed above has a status.
- Every active/baseline/paused branch has a short justification.
- Any fatal or high-risk issue has file evidence and a recommended action.
- The report distinguishes proof, experiment, conjecture, and obsolete history.
- Verification commands attempted are listed with outcomes.
- Subagent notes, if subagents were used, are saved under the audit directory.
- The controller has directly re-checked every fatal/high-risk subagent finding.
- The final response tells the user exactly which files were created.

If no fatal issue is found, say that plainly, but still list residual risks.

## Recommended First Normal Turn After Starting The Goal

After starting the goal, the first actual audit turn should do this:

```text
先建立 claim ledger，不急着证明任何一个分支对错。请读取 README.md、
docs/DIRECTIONS.md、docs/PROJECT_STATUS.md、docs/CURRENT_FINDINGS.md、
docs/MULTI_CONCORDANT_N_STRATEGY.md、docs/PROOF_STATUS_FAST_MODE.md、
docs/PARTNER_GRAPH_THEORY.md 和最近 073-104 的 worklogs 索引，整理当前
顶层结论、依赖关系、风险点。第一轮只产出审查地图，不做大规模实验。
```

This keeps the audit from turning into a random walk through math details.
