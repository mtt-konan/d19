# Active Task

- Status: complete
- Updated: 2026-07-14
- Task id: universal-four-factor-hrl-exact-evaluation-support-audit
- Base commit: `8f5a255`
- Role: sole mathematical Worker; no Codex, ask_codex, subagents, or delegation.
- Goal: Audit only twist classes actually realized as `[H_RL(P)]` by exact rational AA/BB restricted-image points on the individual four-factor cover.
- Scope: Derive the exact primitive/source-coordinate evaluation with all four chosen radicals, then audit support at odd valuations, p=2, numerators, primitive gcds, denominators, real intervals, positive square `x=t^2`, and every retained boundary for both `T=A+B` and physical `T=|A-B|`.
- Frozen inputs: completed HRL design task, `wl587`-`wl595`, and commit `8f5a255`. Do not create `wl596`.
- Forbidden: repeating the generic infinity of `K^*/K^{*2}` as the conclusion; arbitrary formal twists; generic nonsquare evidence; broad point searches; local-prime tables; rank/Selmer; D2; D5; M3; full pytest.
- Allowed changes: this task anchor, one concise report, and a small certificate/focused test only if it certifies derived formulas or the reduced exact proposition. Update only this task pointer in `docs/codex/index.md`.
- Required outcomes: `finite_realized_twist_support_ready`, `realized_infinite_support_family`, or `precise_evaluation_support_blocker`.
- Current step: Complete. The exact source evaluation is certified and the support question is reduced to the closure-compatible squareclass of `q1*q2`.
- Accepted outcome: `precise_evaluation_support_blocker`.
- Completed result: For every exact four-lift point, `[H_RL(P)]=[epsilon1*epsilon2*q1*q2*Delta_bar^e]`, with `q_i` dividing `Delta_bar`; denominator valuations are even and all odd support outside `Delta_bar` is excluded. The remaining exact proposition is the `q1*q2` divisor-allocation problem on both closure branches, including p=2 and shared gcds.
- Validation: focused tests passed (`4 passed`); targeted Ruff and format checks passed; `git diff --check` passed; no full pytest.
