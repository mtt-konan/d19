# Commands Run

本文件只记录本次审查实际跑过或读取过的关键命令。大范围重跑没有做；本次目标是查逻辑链和结论边界，不是扩大搜索上限。

## Required Verification

| Command | Outcome | Notes |
|---|---|---|
| `git status --short --branch` | pass | `## main...origin/main`，审查开始时已有未跟踪控制说明文件。 |
| `uv run pytest -q` | pass | `335 passed, 2 warnings in 31.45s`。警告是两个未注册的 `pytest.mark.slow`。 |
| `uv run ruff check .` | fail | `250 errors`。主要是既有 archive/scripts/tests 风格问题，如 `F541`、`B905`、`E501`、`RUF003`、`E402`。未作为理论错误处理。 |

## Focused Tests

| Command | Outcome | Notes |
|---|---|---|
| `uv run pytest -q tests/test_coprime_mod12.py tests/test_proof_status.py tests/test_proof_status_fast_core.py tests/test_prove_no_solution_fast_mode.py tests/test_dual_closure_sieve.py` | pass | `68 passed in 0.64s`。覆盖 gcd-aware、proof_status、fast-core、旧 dual closure 回归。 |
| Subagent: `uv run pytest tests/test_chain_fast.py tests/test_chain_fast_cli.py -q` | pass | `45 passed`，见 `subagent-notes/chain-fast-baseline.md`。 |
| Subagent: `uv run pytest tests/test_gm_closure_delta.py tests/test_cycle_relations.py tests/test_dscale_kn.py` | pass | `19 passed`，见 `subagent-notes/partner-graph.md`。 |
| Subagent: `uv run pytest -q tests/test_fast_multi_n.py tests/test_half_points.py tests/test_two_descent_rank.py` | pass | `17 passed`，见 `subagent-notes/concordant-multi-n.md`。 |
| Subagent: `uv run pytest tests/test_parametric.py tests/test_ec.py tests/test_chain.py tests/test_cli.py -q` | pass | `70 passed`，见 `subagent-notes/legacy-paused-routes.md`。 |
| Subagent: safe-filters targeted smoke checks | pass / diagnostic | 未跑完整测试；做了 targeted `rg`/`nl` 取证和轻量 `PYTHONPATH=src uv run python` smoke checks，见 `subagent-notes/safe-filters.md`。 |

## Smoke / Diagnostic Commands

| Command | Outcome | Notes |
|---|---|---|
| `uv run python scripts/search.py concordant --pair 264,420 --no-progress` | pass | Default PARI/EC bounded diagnostic found `N=[77,315]`; not a proof path. |
| `uv run python scripts/search.py concordant --pair 264,420 --method factor --no-progress` | fail | CLI option is not `--method`; help shows correct flag is `--concordant-method`. |
| `uv run python scripts/search.py concordant --help` | pass | Confirms `--concordant-method {ec,factor}` and that `factor` has no upper bound. |
| `uv run python scripts/search.py concordant --pair 264,420 --concordant-method factor --no-progress` | pass | Factor path found exhaustive `concordant_n=[77,315,352,1440]`; no sum-closure `chain_compatible`. |
| `uv run python scripts/search.py chain-fast --max-hyp 200 --no-progress` | pass | Bounded baseline search found 0 unit-square 4-cycle solutions. |
| `uv run python scripts/prove_no_solution.py --pair 7,45 --db /tmp/d19-audit-proof-status.sqlite3 --force --no-progress` | pass | One pair processed; `no_solution=1`, by `safe_sieve pass` then `chain_closure_mod_sieve no_solution`. |
| `uv run python - <<'PY' ... import rational_distance ... PY` | fail | Missing `PYTHONPATH=src`; rerun below with corrected environment. |
| `PYTHONPATH=src uv run python - <<'PY' ... run_factor_concordant ... PY` | pass | `(264,420)` gives 4 `N`, no GEN-CLOSURE; `(6,15)` and `(8,20)` each have one concordant `N` and no closure. |
| `PYTHONPATH=src uv run python - <<'PY' ... safe_pair_sieve ... PY` | pass | Shows `classify_reduced_pair` can reject non-coprime `(6,15)`, confirming it must stay coprime-only. |

## SQLite / Result Checks

| Command | Outcome | Notes |
|---|---|---|
| `sqlite3 -readonly results/chain.db ".schema chain_runs"` | pass | Shows old schema with `chain_runs` only; no current `chain_meta` marker. |
| `sqlite3 -readonly results/proof_status.db "SELECT status, COUNT(*) ..."` | pass | Existing DB has `hard_case=4653`, `no_solution=94658`; stale relative to wl094 code semantics. |
| `sqlite3 -readonly results/proof_status.db "SELECT method, outcome, COUNT(*) ..."` | pass | Existing DB has `factor_concordant|inconclusive|4989`, showing pre-GEN-CLOSURE semantics. |

## Notes

- Several large result files were not bulk-read. The audit used summaries, schemas, tests, and small representative samples.
- No source code was modified.
- Audit files under `docs/audits/2026-06-07-theory-framework-audit/` were created in this run.
