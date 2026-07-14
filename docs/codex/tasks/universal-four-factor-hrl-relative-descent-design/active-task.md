# Active Task

- Status: complete
- Updated: 2026-07-14
- Task id: universal-four-factor-hrl-relative-descent-design
- Role: sole mathematical Worker; no delegation or agent invocation.
- Goal: Independently certify the declared 21-generator radical-linear data and audit the relative-descent twist family for `H_RL`.
- Scope: Start strictly after `accepted_outcome=non_base_pullback_candidate_ready`. Reproduce the 160-by-21 parity matrix, rank 14, seven kernel generators, one-dimensional radical-linear quotient, the exact divisor of `H_RL`, and the `H_A` pullback identity. Then determine the exact twist-parameter quotient for `Y^2=d*H_RL` before any local-prime tables.
- Frozen inputs: `wl587`-`wl595` and both completed Picard-audit reports. Do not create `wl596`.
- Required retained data: separate `T=A+B` and physical `T=|A-B|`; positive square `x=t^2`; real intervals; midpoint, endpoints, factor-zero, infinity, collision, and denominator charts; all four factor lifts; exact AA/BB image; `p=2`; primitive/gcd and denominator conditions.
- Forbidden: modifying frozen checkpoints; numbered worklogs; local-prime tables; Selmer/rank; D2; D5; M3; broad point searches; full pytest.
- Allowed changes: this task anchor, one executable proof-data certificate, one focused test module, one concise audit report, and the task pointer in `docs/codex/index.md`.
- Current step: Complete. The independent certificate and focused audit report are materialized.
- Completed result: The matrix certificate reproduces the 21 columns, 160 rows, rank 14, seven kernel supports, one-dimensional radical-linear quotient, exact `H_RL` divisor, and `H_A` identity/pullback class. The intrinsic unscaled twist quotient is `K^*/K^{*2}`; after the common-scale chart it is `k^*/k^{*2}`. The optional deck-orbit quotient kills only `[-1]` and `[Delta]` and remains infinite. No finite parameter-uniform support theorem follows from the retained geometric data.
- Stop outcomes: `finite_twist_support_ready`, `candidate_automatic_on_restricted_image`, or `precise_twist_support_blocker`.
- Accepted outcome: `precise_twist_support_blocker`.
- Validation: focused tests passed (`4 passed`); targeted Ruff and format checks passed; `git diff --check` passed; full pytest was not run.
