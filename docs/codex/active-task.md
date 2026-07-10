# Active Task

- Status: complete
- Updated: 2026-07-10
- Task id: wl529-v5-l1-t5-square-locus
- Goal: Recover and complete `wl529` for the existing `wl528` prototype by constructing the specialization-square locus for `(N^2+16)(M^2+16)`, proving or refuting rational square specializations in the required nonexceptional positivity domain `|t|<5`, and stopping after this one-family analysis.
- Scope: The already selected `support=v_5|L=1|T=5|d=(5,1,5)` prototype only, represented by `AA_A1_B4_v_5_m_tail_refresh_candidate` and `BB_A4_B1_v_5_m_tail_refresh_candidate`.
- Object layer: one-family square-specialization locus over the `wl528` function-field prototype; not theorem-level Selmer and not old package-x / `S~`.
- Allowed changes: `wl529` worklog/script/focused test/result JSON, plus handoff docs and this task anchor.
- Forbidden changes: no shell 11, no new supports, no other cover family, no broad rank/Selmer diagnostics, no old package-x / `S~` bridge, no rank-zero/Sha/family-exclusion/uniform `M_tail` claim, no commit.
- Stable boundaries: keep generic function-field nonsquareness separate from specialization-square analysis; explicitly record that divisor parity, by itself, does not rule out every rational square specialization.
- Current step: Complete.
- Completed steps: Read the `wl528` worklog/script/test and current handoff/context docs; reloaded the route guardrails; derived the key identity `16P = (t^2+39)^2 + 6400`; confirmed the square-locus reduces to a genus-one problem in the centered-even parameter `t`; added the `wl529` worklog/script/test/result artifact; proved the square-locus genus-one certificate and the `t=0` no-lift fact on the prototype quartic; synchronized handoff docs; reran focused `wl528` + `wl529` pytest and targeted ruff.
- Next exact step: None; stop after reporting the one-family square-locus result.
- Validation gates: `UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest tests/test_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`; `UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py tests/test_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py`; regenerate the `wl529` result JSON with its script.
- Stop condition: Stop after this one square-locus analysis, report proved/refuted/model-only status, and do not advance to another family or roadmap step.
