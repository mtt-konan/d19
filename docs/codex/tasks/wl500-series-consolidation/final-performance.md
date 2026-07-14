# Final Performance Verification

```text
baseline = 1748 passed, 2 warnings, 203.20s
final = 1363 passed, 0 warnings, 29.35s
wall_time_reduction = 85.56%
target = <=142.24s
target_headroom = 112.89s
status = passed
```

Command:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest --durations=50
```

Slowest 50 durations:

```text
5.40s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_profile_and_cache
3.63s call  tests/theory/aa_bb/test_d4_factor_twist.py::test_strict_cli_writes_one_deterministic_two_stage_payload
3.29s call  tests/test_probe_focus_template_modular.py::test_cli_can_emit_crt_summary
3.23s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_bucket_stats_and_analysis
3.22s call  tests/test_rational_ratio.py::test_sum_ab_product_square_residuals_from_root_grid_finds_known_residual
3.22s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_near_miss_limit
2.48s call  tests/theory/aa_bb/test_c3_cli.py::test_cli_writes_one_strict_deterministic_17_stage_payload
2.37s setup tests/theory/aa_bb/test_c3_cli.py::test_composition_has_exact_stage_order_and_allowlists
2.34s call  tests/test_probe_focus_template_modular.py::test_probe_many_reports_all_moduli
2.26s call  tests/test_probe_focus_template_modular.py::test_crt_summary_multiplies_stage_counts_for_coprime_moduli
2.22s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_safe_pair_sieve_python
2.21s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_mod_sieve_hidden_but_works
2.17s call  tests/test_chain_fast.py::TestChainFastNumpy::test_parallel_start_t1_resumes_subset
2.06s call  tests/test_fixed_ratio_sieve.py::test_fixed_ratio_mod_sieve_has_no_killer_modulus_because_universal_witness_survives
2.03s setup tests/theory/aa_bb/test_d4_factor_twist.py::test_stage_order_allowlists_and_serialization_are_exact
1.96s call  tests/test_probe_focus_template_modular.py::test_probe_focus_template_modular_tracks_survivors
1.73s call  tests/theory/aa_bb/test_c2_cli.py::test_cli_writes_one_deterministic_27_stage_payload
1.67s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_safe_pair_sieve_requires_python_backend
1.46s call  tests/test_concordant.py::TestConcordantCli::test_batch_cli_safe_pair_sieve_reduces_analyzed_pairs
1.36s call  tests/test_dscale_kn.py::test_reproduce_wl063_k10_hub
1.23s call  tests/test_concordant.py::TestConcordantCli::test_batch_cli_out_includes_diagnostic_summary
1.21s call  tests/theory/aa_bb/test_wl594_universal_closure_product_g0.py::test_wl594_certifies_the_parameterized_g0_input_without_claiming_an_obstruction
1.20s call  tests/test_ec.py::TestEcDatabase::test_database_run_matches_plain_search
1.18s call  tests/test_rational_ratio.py::test_sum_ab_product_square_bucket_summary_keeps_residual_guard
1.16s call  tests/theory/aa_bb/test_c1_cli.py::test_c1_strict_cli_is_the_only_subprocess_entrypoint
1.13s call  tests/theory/aa_bb/test_wl595_universal_closure_product_g4_route_death.py::test_wl595_accepts_the_scoped_route_death_certificate
1.11s call  tests/test_chain_fast.py::TestChainFastProfile::test_run_chain_fast_bucket_stats_match_parallel_python
1.08s call  tests/theory/aa_bb/test_wl595_universal_closure_product_g4_route_death.py::test_wl595_strict_cli_output
1.06s setup tests/theory/aa_bb/test_c2_cli.py::test_composition_has_exact_stage_and_allowlist_maps
1.05s call  tests/test_chain_fast.py::TestChainFastNumpy::test_python_workers_match_single_process
1.04s call  tests/test_chain_fast.py::TestChainFastNumpy::test_numpy_workers_match_single_process
0.99s call  tests/theory/aa_bb/test_c3_cli.py::test_invalid_c2_predecessor_fails_closed
0.93s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_chain_fast_cli_bucket_stats_requires_db
0.91s setup tests/theory/aa_bb/test_c2_allocation.py::test_full_stage_semantic_projections_have_frozen_digests
0.87s call  tests/theory/aa_bb/test_wl594_universal_closure_product_g0.py::test_wl594_strict_cli_output
0.84s call  tests/theory/aa_bb/test_d4_factor_twist.py::test_dependency_aware_adapters_match_zero_argument_builders
0.80s call  tests/test_chain_fast_cli.py::TestChainFastCLI::test_cli_fails_on_legacy_chain_db
0.79s setup tests/theory/aa_bb/test_c3_quotient_limits.py::test_full_stage_semantic_projections_have_frozen_digests
0.78s setup tests/theory/aa_bb/test_c2_global_descent.py::test_full_stage_semantic_projections_have_frozen_digests
0.78s call  tests/theory/aa_bb/test_c2_cli.py::test_composition_calls_each_canonical_builder_once
0.77s call  tests/test_chain_fast.py::TestChainFast::test_returns_list
0.70s call  tests/theory/aa_bb/test_wl595_universal_closure_product_g4_route_death.py::test_wl595_retains_g0_and_exact_g1_algebra
0.69s setup tests/theory/aa_bb/test_c2_character_system.py::test_full_stage_semantic_projections_have_frozen_digests
0.68s call  tests/theory/aa_bb/test_c3_quotient_limits.py::test_invalid_canonical_wl580_fails_closed
0.68s call  tests/test_ec.py::TestEcDatabase::test_analysis_script_outputs_json_and_html
0.65s call  tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py::test_wl590_adapter_matches_default_rejects_invalid_d0_and_does_not_rebuild
0.64s call  tests/test_rational_ratio.py::test_sum_ab_same_orientation_combined_valuation_summary_shows_many_local_patterns
0.64s call  tests/test_ec.py::TestEcDatabase::test_resume_reuses_same_run_id
0.62s call  tests/theory/aa_bb/test_c2_allocation.py::test_slice_fails_closed_on_unready_wl562
0.62s call  tests/theory/aa_bb/test_wl595_universal_closure_product_g4_route_death.py::test_wl595_checks_primitive_denominators_and_g4_scope
```
