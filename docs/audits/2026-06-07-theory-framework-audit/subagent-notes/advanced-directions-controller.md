Slice:
advanced-directions-controller（controller 本地补审；原计划第 7 个 subagent 因 agent 数量限制未启动）

Files inspected:
- `docs/THEORY_DIRECTIONS.md`
- `docs/THEORY_DIRECTIONS_ADVANCED.md`
- `docs/OPEN_DIRECTIONS.md`
- `docs/PROJECT_STATUS.md`
- `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md`
- `docs/work-logs/090-f2-chabauty-tooling-survey.md`
- `docs/work-logs/092-direction5-heegner-decider-redundant.md`
- `src/rational_distance/concordant/heegner_height.py`
- `src/rational_distance/proof_status/methods.py`
- `tests/test_proof_status.py`

Commands run:
- Targeted `nl -ba` / `rg -n` reads of the files above.
- Covered by full `uv run pytest -q` and focused proof-status tests in the main command log.

Claims checked:
- Heegner/height route is not a current no-solution decider.
- Chabauty, Brauer-Manin, K3 are open long-term routes, not dead routes.
- Second descent / L-function rank tools are not current high-ROI rank filters because PARI already certifies many sampled ranks, but this does not kill those topics mathematically.
- A1 strict proof must be downgraded after wl084.

Fatal findings:
- None as current active claims. The docs mostly avoid declaring these long-term routes mathematically dead.

High-risk findings:
- `THEORY_DIRECTIONS_ADVANCED.md` contains mixed Heegner wording. Its top status table says height-bound upgrade is redundant after wl092, and the implementation says `heegner` never returns `no_solution`; later sections still describe future work to add canonical-height bounds and upgrade `inconclusive` to strict `no_solution`. That is a stale plan, not current proof machinery.
- `THEORY_DIRECTIONS_ADVANCED.md` says direction six and nine have "0" expected benefit as rank tools because PARI already gives exact rank on sampled data. This is a project-priority statement, not a theorem that L-functions or second descent are useless.

Medium/low findings:
- `OPEN_DIRECTIONS.md` is honest that engineering max-hyp increases are empirical and not proof.
- `OPEN_DIRECTIONS.md` correctly flags A1 strict proof as not done after wl084.
- Chabauty, Brauer-Manin, and K3 remain open; no inspected current file proves them dead.

Non-issues worth noting:
- `heegner_height.py` explicitly states its scan is diagnostic and cannot prove global non-existence without a future certified height theorem.
- `run_heegner_height` returns `solution_found` only for a positive witness; otherwise it returns `inconclusive` or `skipped`, never `no_solution`.

Open uncertainties:
- I did not verify external theorem statements from papers or PDFs. This slice only checks local repo claims and implementation status.

Recommended updates to main claim ledger:
- Mark Heegner/height as "diagnostic/witness finder; no longer needed for integer-N exhaustion after factor_concordant."
- Mark Chabauty/Brauer-Manin/K3 as "open long-term, not killed."
- Mark A1 strict proof as "superseded by wl084; empirical only."

Plain-language summary:
长期方向没有被仓库真正判死。更准确的状态是：有些方向暂时不划算，有些需要重工具，有些只适合找 witness 或做诊断。项目不能因为一次有限实验、一次工具替代，直接说这些数学路线已经死了。
