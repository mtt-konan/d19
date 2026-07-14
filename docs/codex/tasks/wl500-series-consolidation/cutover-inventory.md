# wl500-wl593 Cutover Inventory

## Snapshot

- Date: 2026-07-14.
- Scope: current wl500-wl593 consumers and provenance only.
- wl594 and wl595 are downstream context and are not deletion targets.
- This is a read-only inventory. No source, test, data, manifest, plan,
  README, worklog, result, active-task, or consumer was changed.
- The target file did not exist at the start of the audit.
- No tests, full suite, materialization, CLI, or mathematical computation was
  run by this audit.

## Scan Evidence

The two exact scans required by d4-extraction-design.md:870-887 were run
before this document was created.

### Exact scan 1: route-level references

~~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl586|wl593|wl586_route_selection|wl593_factor_twist_generalization_route_death' \
  docs scripts tests data
~~~~

Evidence: 198 matching lines, split by path root as data=6, docs=84,
scripts=50, tests=58.

### Exact scan 2: protected dependency boundary

~~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl587|wl589|wl590|wl591|wl592|D0u|D0m|D5|D7|D17' \
  scripts/theory/aa_bb tests/theory/aa_bb docs/codex/tasks/wl500-series-consolidation
~~~~

Evidence: 353 matching lines, split by path root as scripts=168,
tests=113, docs=72.

### Narrower range and result scans

The additional full-range label scan was:

~~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl(50[0-9]|51[0-9]|52[0-9]|53[0-9]|54[0-9]|55[0-9]|56[0-9]|57[0-9]|58[0-9]|59[0-3])' \
  docs scripts tests data
~~~~

Evidence: 9,645 matching lines in 355 paths. The path count is dominated by
historical worklog text and canonical JSON provenance fields; it is not a
count of executable consumers.

The legacy executable/test path inventories were also enumerated:

- 87 pre-D4 legacy scripts under scripts/theory/audit_* for wl500-wl585,
  including the wl530_wl585 consolidated checkpoint.
- 87 corresponding legacy tests under tests/test_closure_* for wl500-wl585,
  including the consolidated checkpoint test.
- 94 worklog/history paths matching the range: 93 numbered worklogs plus the
  530-585 consolidated checkpoint. wl588 has no owned triplet.

The exact path/symbol enumerators used for those sets were:

~~~~bash
rg --files scripts/theory | rg \
  'audit_closure_quotient_rank_zero_aa_bb_wl(50[0-9]|51[0-9]|52[0-9]|53[0-9]|54[0-9]|55[0-9]|56[0-9]|57[0-9]|58[0-9]|59[0-3])([^0-9]|_|$)' | sort
rg -n '^def build_' scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl5*.py | sort
rg --files tests | rg \
  'test_closure_quotient_rank_zero_aa_bb_wl(50[0-9]|51[0-9]|52[0-9]|53[0-9]|54[0-9]|55[0-9]|56[0-9]|57[0-9]|58[0-9]|59[0-3])([^0-9]|_|$)' | sort
~~~~

The exact route-level paths and symbols are listed below rather than inferred
from filename presence.

## Classification

- Runtime consumer: an executable/importable path used by the current runtime
  or legacy CLI graph to build evidence.
- Test/parity consumer: a test, compatibility view, or old builder used as an
  explicit parity oracle. It is not a canonical runtime dependency.
- Manifest/data consumer: a tracked JSON field or loader/materializer binding
  that records or constructs evidence inputs.
- README/control reference: an operational instruction or route-control
  document that may need a later cutover edit.
- Worklog/history provenance: narrative, source provenance, or historical
  command text. It is not a runtime loader merely because it names a script.
- Protected kernel dependency: a retained D0/local-image module or its focused
  test. These are not deletion candidates.
- Stale/unresolved reference: a current path that still requires an old
  route-level script, old manifest consumer path, or old operational command.

## Canonical Graph

The full destination map is the accepted C0 map in
docs/codex/tasks/wl500-series-consolidation/c0-obligation-map.md:27-46:

~~~~text
A0 -> A1 -> A2
B0 -> B1
C1 -> C2 -> C3
D0u ----\
D0m -----+-> D5 -> D7 -> D17 -> D4
A0/A2 ---/

500:A1 501:A1 502:A1 503:A1 504:A1 505:A0/A1 506:A1
507:A1 508:A1 509:A1 510:A1 511:A0/A1 512:A1 513:A1
514:A1 515:A1 516:A1 517:A0/A1 518:A2 519:A0/A1 520:A2
521:A2 522:A0/A2 523:A2 524:A2 525:A2 526:A2 527:A0/A2
528:B0/B1 529:B1
530:C1 531:C1 532:C1 533:C1 534:C1 535:C1
536:C1 537:C1 538:C1 539:C1 540:C1 541:C1
542:C2 543:C2 544:C2 545:C2 546:C2 547:C2 548:C2
549:C2 550:C2 551:C2 552:C2 553:C2 554:C2 555:C2
556:C2 557:C2 558:C2 559:C2 560:C2 561:C2 562:C2
563:C2 564:C2 565:C2 566:C2 567:C2 568:C2
569:C3 570:C3 571:C3 572:C3 573:C3 574:C3 575:C3
576:C3 577:C3 578:C3 579:C3 580:C3 581:C3 582:C3
583:C3 584:C3 585:C3
586:D4 587:D0u 589:D0m 590:D5 591:D7 592:D17 593:D4
530-585-consolidated:C1/C2/C3-parity-oracle
~~~~

The executable destinations and exact public symbols are:

| Destination | Exact current paths and symbols | Current role |
| --- | --- | --- |
| A0 | data/theory/aa_bb/wl500/a0-ledger.v1.json, a0-witnesses.v1.json, a0-taxonomy.v1.json, a0-inventory.v1.json; scripts/theory/aa_bb/consolidation_inputs.py:A0Bundle, load_a0, load_all, A0Bundle.to_wl522_view, to_wl527_view, to_wl586_inputs | Tracked finite inputs; the three to_* methods are compatibility views for parity only. |
| A1 | data/theory/aa_bb/wl500/a1-certificates.v1.json; scripts/theory/aa_bb/a1_ambient.py:verify_cover_certificate, a1_shells.py:evaluate_shell, a1_certificates.py:load_certificates, build_a1, project_a1 | Canonical finite-shell and cover certificates. |
| A2 | data/theory/aa_bb/wl500/a2-boundary-spec.v1.json; scripts/theory/aa_bb/a2_evidence.py:load_boundary_spec, build_a2, project_a2 | Canonical taxonomy, route, and no-claim boundary. |
| B0 | data/theory/aa_bb/wl500/b0-prototype-rows.v1.json; scripts/theory/aa_bb/consolidation_inputs.py:B0Document, load_b0, B0Document.to_wl528_view | Tracked selected wl495 rows. |
| B1 | data/theory/aa_bb/wl500/b1-sage-certificate.v1.json; scripts/theory/aa_bb/b1_prototype.py:load_sage_certificate, build_b1, semantic_projection, project_b1 | Canonical wl528-wl529 prototype and square-locus evidence. |
| C1 | scripts/theory/aa_bb/c1_pure_v_ell.py:build_c1, project_stage, semantic_projection; c1_local_tables.py:build_local_stages; c1_wl535.py:build_wl535; c1_wl539.py:build_wl539; c1_wl540.py:build_wl540; c1_wl541.py:build_wl541 | Canonical wl530-wl541, including protected method-exhaustion stages. |
| C2 | scripts/theory/aa_bb/c2_pure_v_ell.py:build_c2, project_stage, semantic_projection; c2_global_descent.py:build_c2_global_descent; c2_character_system.py:build_c2_character_system; c2_allocation.py:build_c2_allocation | Canonical wl542-wl568 descent and allocation evidence. |
| C3 | scripts/theory/aa_bb/c3_pure_v_ell.py:build_c3, project_stage, semantic_projection; c3_real_branch.py:build_c3_real_branch; c3_magnitude_descent.py:build_c3_magnitude_descent; c3_quotient_limits.py:build_c3_quotient_limits | Canonical wl569-wl585 reconstruction, geometry, and quotient boundary. |
| D4 | scripts/theory/aa_bb/d4_factor_twist.py:build_d4, project_stage, semantic_projection, main; D4_STAGES=("wl586","wl593") | Canonical two-stage route orchestrator. Runtime loads tracked A0/A1/A2 data and C3, then composes protected kernels. |

The exact D4 code-level edges are narrower than the visual order above:

~~~~text
D5  <- D0u, D0m
D7  <- D0m
D17 <- D0m
D4  <- A0, A2, C3, D0u, D0m, D5, D7, D17
~~~~

The call order in d4_factor_twist.py:1100-1147 is
wl587, wl589, wl590, wl591, wl592; the dependency metadata is serialized at
:1157-1164. D4 does not call legacy wl586 or wl593.

## Protected Kernels

These paths are retained and are not deletion candidates:

| Kernel | Exact path and symbols | Required destination |
| --- | --- | --- |
| D0u | scripts/theory/aa_bb/wl587_pure_u7_d0_relative_2_descent.py:build_wl587_pure_u7_d0_relative_2_descent; focused test tests/theory/aa_bb/test_wl587_pure_u7_d0_relative_2_descent.py | D4 kernel input wl587; retain fixed pure-u_7 D0 schema and zero-argument API. |
| D0m | scripts/theory/aa_bb/wl589_mixed_d0_relative_2_descent.py:build_wl589_mixed_d0_relative_2_descent; focused test tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py | D4 kernel input wl589; retain fixed mixed D0 schema and zero-argument API. |
| D5 | scripts/theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py:build_wl590_from_d0, build_wl590_p5_factor_twist_local_image_comparison; focused test tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py | D4 wl590 input; keep exact p=5 images and wrapper parity. |
| D7 | scripts/theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py:build_wl591_from_mixed_d0, build_wl591_mixed_p7_factor_twist_local_image; focused test tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py | D4 wl591 input; keep exact mixed p=7 image and wrapper parity. |
| D17 | scripts/theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py:build_wl592_from_mixed_d0, build_wl592_mixed_p17_factor_twist_local_image; focused test tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py | D4 wl592 input; keep exact mixed p=17 image and wrapper parity. |

The protected-module imports are intentional kernel dependencies:

- wl590...py:25-30 imports the pure and mixed D0 modules for frozen source and
  factor symbols.
- wl591...py:27-30 and wl592...py:27-30 import the mixed D0 module.
- d4_factor_twist.py:29-43 imports all five protected modules and
  :1102-1106 selects the dependency-aware entrypoints.
- d4_factor_twist.py:1138-1147 calls each protected entrypoint once and
  validates the returned certificate.

The legacy wl593 builder at
scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py:279-290
calls all five zero-argument wrappers and is therefore a legacy runtime
consumer of the protected boundary. It is not a D4 dependency.

## Route-Level Reference Inventory

### wl586

| Exact path | Symbol or field | Classification | Proposed non-destructive replacement |
| --- | --- | --- | --- |
| scripts/theory/aa_bb/wl586_route_selection.py:376-460 | build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death; imports legacy wl585; accepts wl505, wl522, wl527 payloads | Runtime consumer; stale/unresolved | Use scripts/theory/aa_bb/d4_factor_twist.py:build_d4; source A0/A2/C3 directly and project wl586 with project_stage/semantic_projection. |
| scripts/theory/aa_bb/wl586_route_selection.py:463-481 | CLI main, load_json(args.wl505/wl522/wl527), --out | Legacy result-loader runtime | Replace the operational command with D4 main; keep this CLI only as an explicit parity/deletion oracle until a later approved removal. |
| tests/theory/aa_bb/test_wl586_route_selection.py:16,130-242 | _module, build_wl586..., synthetic payloads, temporary CLI output | Test/parity consumer; unresolved legacy test | Move semantic coverage to test_d4_factor_twist.py; retain only an explicitly named legacy parity test until deletion approval. |
| scripts/theory/aa_bb/consolidation_inputs.py:198-199,249-250,272-273 | SOURCE_PROVENANCE[*].consumer_paths names the old wl586 script/test | Manifest/data consumer and stale metadata | Change only future consumer_paths to canonical A2/D4 and canonical parity tests; retain source_script_path and source_test_paths as provenance. |
| scripts/theory/aa_bb/consolidation_inputs.py:1569-1601 | A0Bundle.to_wl586_inputs() | Test/parity compatibility view, not runtime | Keep for old/new projection parity; do not make D4 call it. |
| data/theory/aa_bb/wl500/manifest.v1.json:230-284 | consumer_paths for A0 witnesses, taxonomy, and inventory | Manifest/data consumer; stale/unresolved before cutover | Point consumer metadata at d4_factor_twist.py and canonical A2 readers; preserve old paths under source provenance. |
| scripts/README.md:233-240 | Current command text says wl586 uses theory/aa_bb/wl586_route_selection.py | README/control reference; stale/unresolved | Document D4 as the route-level executable and leave the wl586 label as a stage/provenance label. |

### wl593

| Exact path | Symbol or field | Classification | Proposed non-destructive replacement |
| --- | --- | --- | --- |
| scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py:279-355 | build_wl593_factor_twist_generalization_route_death; INPUT_WORK_LOGS; five zero-argument builder calls | Runtime consumer; stale/unresolved legacy orchestrator | Use D4 build_d4 and select its wl593 stage; do not route D4 through this module. |
| scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py:358-373 | CLI main, optional --out, strict status | Legacy route CLI | Replace the operational command with D4 strict CLI; retain old CLI only for explicit parity/deletion testing. |
| tests/theory/aa_bb/test_wl593_factor_twist_generalization_route_death.py:10-131 | Direct import, build_wl593..., and strict subprocess test | Test/parity consumer; unresolved legacy test | Move route projection checks to test_d4_factor_twist.py; preserve old/new projection parity separately. |
| tests/theory/aa_bb/test_d4_factor_twist.py:17-20,211-230 | legacy_wl586, legacy_wl593, old/new semantic projection equality | Explicit test/parity consumer; allowed exception | Retain as the legacy oracle until the Controller approves deletion or converts it to a stable fixture. It must not be imported by D4 runtime. |
| scripts/README.md:264-268 | Current command text says wl593 uses the old route-death script | README/control reference; stale/unresolved | Point the current command to D4 and retain wl593 only as the semantic stage name. |
| docs/work-logs/593-factor-twist-generalization-route-death.md:1-178 | Historical conclusion and old validation commands | Worklog/history provenance, not runtime | Retain as provenance mapped to D4 wl593; do not treat its command text as a loader. |

The exact route-level scan also found these non-runtime references:

- scripts/theory/aa_bb/d4_factor_twist.py:3,68,710-725,993-1050,1132-1250:
  canonical stage labels and semantic allowlists, not legacy imports.
- tests/theory/aa_bb/test_c3_cli.py:325,
  test_c3_magnitude_descent.py:298,
  test_c3_quotient_limits.py:338,365, and
  test_c3_real_branch.py:347: negative tests or route-boundary strings that
  reject wl586; test/control references, not runtime consumers.
- scripts/theory/aa_bb/wl594_universal_closure_product_g0.py:471:
  downstream field wl581_wl593_modified; out of scope and not a dependency on
  the old wl593 builder. It must not be edited in this task.
- docs/NEXT_RESEARCH_GATE.md, docs/PROJECT_STATUS.md,
  docs/OPEN_DIRECTIONS.md, docs/codex/current-context.md,
  docs/codex/index.md, the consolidation plan and task designs, and the
  current/archive worklogs: narrative route status or provenance. None points
  a runtime loader at the old wl586/wl593 module.

## wl500-wl585 Legacy Consumers

The pre-D4 legacy artifacts are still present and still executable. Their
destination is the canonical graph, but their path-level cutover has not
occurred.

| Legacy range and exact path family | Legacy symbols/behavior | Classification | Canonical destination |
| --- | --- | --- | --- |
| scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl500_*.py through the literal wl527_*.py paths; 30 exact scripts in wl500-wl529 | Each has its literal build_wl<N>_<topic> and CLI main; the chain uses json_io.load_json predecessor payloads | Runtime consumers; many are ignored-result loaders | A0/A1/A2. Keep source script/test names in provenance; switch runtime imports/CLI paths only after projection parity. |
| scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.py and ...wl529_v5_l1_t5_square_locus.py | build_wl528_v5_l1_t5_function_field_prototype, build_wl529_v5_l1_t5_square_locus; wl529 loads selected wl495 data | Runtime consumers and legacy parity oracles | B0/B1 via build_b1, tracked b0-prototype-rows.v1.json, and tracked B1 Sage data. |
| scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl530_m1...py, the literal wl531... through wl585... paths, and wl530_wl585_consolidated_checkpoint.py | 57 exact scripts; each literal build_wl<N>..., plus consolidated build_wl530_wl585_consolidated_checkpoint | Runtime consumers and historical parity oracles | C1 for wl530-wl541, C2 for wl542-wl568, C3 for wl569-wl585. The consolidated oracle maps to the three canonical slice tests. |
| tests/test_closure_quotient_rank_zero_aa_bb_wl500_*.py through the literal wl585_*.py paths; 87 exact tests | Per-WL subprocess tests read temporary output; wl521, wl522, wl527 tests also read existing ignored results as fixtures | Test/parity consumers; unresolved until cutover | Replace with focused A1/A2/B1/C1/C2/C3 parity tests. Do not delete in this inventory turn. |
| tests/theory/aa_bb/test_b1_prototype.py:24-28,82+ | LEGACY wl528/wl529 result paths are read for comparison while build_b1 consumes tracked B0/Sage data | Test/parity consumer, not B1 runtime | Keep as explicit old/new parity until the legacy result fixture is replaced by a checked-in fixture or approved removal. |
| tests/theory/aa_bb/test_c1_pure_v_ell.py:23-80,208-218 | LEGACY_RESULTS and CONSOLIDATED_RESULT; test_secondary_consolidated_oracle_keeps_m2_open_and_m3_closed | Test/parity consumer | Replace with canonical C1 semantic projections and a retained no-claim fixture after parity acceptance. |
| scripts/theory/aa_bb/consolidation_inputs.py:1921-2050,2091-2355 | _read_source_payload, materialize_a0, materialize_b0, materialize_b1_sage_certificate, materialize_manifest, materialize_a1_certificates, materialize_a2_boundary_spec | Manifest/data materializer; explicit ignored-result input | Keep only as the explicit pre-cutover materialization path. Canonical loaders must continue using tracked JSON only. |

The exact old-to-canonical mapping is therefore:

~~~~text
wl500-wl527       -> A0/A1/A2
wl528-wl529       -> B0/B1
wl530-wl541       -> C1
wl542-wl568       -> C2
wl569-wl585       -> C3
wl530-wl585 audit -> C1/C2/C3 parity oracle
wl586             -> D4 stage wl586
wl587             -> retained D0u kernel
wl589             -> retained D0m kernel
wl590             -> retained D5 kernel
wl591             -> retained D7 kernel
wl592             -> retained D17 kernel
wl593             -> D4 stage wl593
wl588             -> no artifact and no destination; retain only "not created" history
~~~~

## Manifest And Data References

The tracked canonical data directory currently contains:

~~~~text
data/theory/aa_bb/wl500/a0-ledger.v1.json
data/theory/aa_bb/wl500/a0-witnesses.v1.json
data/theory/aa_bb/wl500/a0-taxonomy.v1.json
data/theory/aa_bb/wl500/a0-inventory.v1.json
data/theory/aa_bb/wl500/a1-certificates.v1.json
data/theory/aa_bb/wl500/a2-boundary-spec.v1.json
data/theory/aa_bb/wl500/b0-prototype-rows.v1.json
data/theory/aa_bb/wl500/b1-sage-certificate.v1.json
data/theory/aa_bb/wl500/manifest.v1.json
~~~~

The data fields fall into three different classes:

1. source_work_log, work_logs, source_payloads, source_result_path,
   source_script_path, source_test_paths, and source_worklog_path are
   provenance/materialization metadata. They identify old evidence and must
   not be confused with a D4 runtime import.
2. The five manifest.v1.json:211-306 consumer_paths entries are current
   consumer metadata. They still name old wl522, wl527, wl528, wl529, and
   wl586 paths. These are stale/unresolved for cutover and must be updated
   later to canonical A0/A1/A2/B1/D4 consumers while preserving the source
   paths as provenance.
3. a0-*, b0-*, a1-certificates, a2-boundary-spec, and the B1 Sage artifact
   are tracked runtime inputs. The canonical runtime validates them; it does
   not load an old result payload.

scripts/theory/aa_bb/consolidation_inputs.py:1-5 explicitly documents that
only the materializer knows about ignored results and that runtime loaders read
tracked canonical files. load_all:2358-2366, load_a0:1677, and load_b0:1697
confirm that boundary. b1_prototype.py:165-169 likewise loads the tracked Sage
artifact, while LEGACY_SOURCE:33-37 is provenance for the explicit
refresh/parity boundary, not a B1 runtime read.

## Ignored Results: Runtime Input Decision

The result directory was inspected without changing it:

- There are 90 matching wl500-wl593 JSON files under results/, covering 88 WL
  ids: every id wl500-wl585, plus wl587 and wl589; wl530 and wl536 each have
  two files. There are no result files for wl586, wl588, or wl590-wl593.
- All 90 are ignored by /Users/konan/Desktop/d19/.gitignore:23-28 under
  results/**. git ls-files results contains eight unrelated tracked result
  package files and no wl500-wl593 result payload.
- git check-ignore -v returned .gitignore:26:/results/** for the current
  wl529, wl587, and wl589 paths.

The answer to whether ignored results are still runtime inputs is split by
execution layer:

- Yes, for the legacy pre-cutover graph. The old wl500-wl585 CLIs take
  predecessor result paths through load_json; the old wl586 CLI explicitly
  loads wl505, wl522, and wl527 at :471-475; old wl529 loads wl495 at its CLI
  boundary; and legacy tests such as
  tests/theory/aa_bb/test_consolidation_inputs.py:30-65,
  tests/test_closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis.py,
  ...wl522_support_cover_taxonomy.py, and
  ...wl527_function_field_squareclass_proof_data.py read ignored results.
- Yes, for explicit materialization and parity only. The materialize_* functions
  and the B1/C1 legacy parity fixtures read result files to reconstruct or
  compare tracked canonical data.
- No, for canonical runtime. D4 main:1288-1306 loads tracked A0/A1/A2 data
  and C3, then calls build_d4; d4_factor_twist.py contains no results/,
  audit_closure_, importlib, filesystem glob, or subprocess fallback. The D4
  runtime does not use the ignored result files.
- The protected D0 CLIs have default result output strings at
  wl587...py:1223 and wl589...py:1177; those are write destinations, not D4
  input reads. D5/D7/D17 use temporary or caller-selected output paths.

Therefore ignored results are not safe to delete during this inventory: they
remain inputs to legacy/materialization/parity paths. They are not permanent
proof inputs for the canonical D4 runtime and must not be introduced as a D4
fallback.

## README, Control, And History

The current operational reference requiring a later edit is:

- scripts/README.md:233-268 directly instructs users to run the old wl586 and
  wl593 scripts, and lists the retained kernels as separate per-WL commands.
  Replace only the current executable instructions with canonical
  A0/A1/A2/B1/C1/C2/C3/D4 commands; retain historical WL labels and protected
  kernel descriptions.

The following are historical/control references, not runtime loaders:

- docs/CLOSURE_QUOTIENT_MAINLINE.md and docs/GLOSSARY.md narrate the
  wl500-wl593 route and link to worklogs.
- docs/NEXT_RESEARCH_GATE.md, docs/PROJECT_STATUS.md, and
  docs/OPEN_DIRECTIONS.md record frozen route status, no-claim boundaries, and
  the downstream wl594/wl595 handoff.
- docs/REPOSITORY_STRUCTURE_MIGRATION_MANIFEST.md and
  docs/REPOSITORY_STRUCTURE_PLAN.md record earlier path migration history.
- docs/WL500_SERIES_CONSOLIDATION_PLAN.md, docs/codex/current-context.md,
  docs/codex/index.md, the consolidation task design files, and
  docs/work-logs/README.md are control, design, or provenance records.
- The current and archived worklogs under docs/work-logs/ and
  docs/work-logs/archive/ are history. Their embedded commands and old paths
  do not constitute runtime consumers. The 586 and 593 worklogs are retained
  as provenance for the two D4 stage projections.

No narrative reference needs to be removed for the cutover. A narrative path
becomes a blocker only if an executable loader or current operational command
still resolves it.

## Unresolved Consumers

These are the unresolved items that prevent a destructive gate from opening:

1. scripts/theory/aa_bb/wl586_route_selection.py remains a legacy runtime
   builder and CLI over old wl505/wl522/wl527 payload shapes.
2. scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py
   remains a legacy runtime orchestrator that rebuilds all five protected
   kernels through zero-argument wrappers.
3. The 87 pre-D4 scripts/theory/audit_*_wl500-wl585 files remain executable
   legacy consumers, including recursive result-loader edges.
4. The 87 tests/test_closure_*_wl500-wl585 tests remain per-WL subprocess
   consumers, and the direct wl586/wl593 tests remain present.
5. data/theory/aa_bb/wl500/manifest.v1.json:211-306 still declares old
   script/test paths in consumer_paths.
6. scripts/theory/aa_bb/consolidation_inputs.py:149-306 duplicates those old
   consumer paths in SOURCE_PROVENANCE, so manifest validation currently binds
   the old metadata.
7. scripts/README.md:233-268 still presents the old route-level scripts as
   the current operational entrypoints.
8. Explicit parity consumers remain by design:
   tests/theory/aa_bb/test_d4_factor_twist.py,
   test_consolidation_inputs.py, test_b1_prototype.py, and
   test_c1_pure_v_ell.py. These are allowed only as named parity/provenance
   exceptions; they must not become D4 runtime imports.

The following are not unresolved consumers:

- Protected D0u/D0m/D5/D7/D17 imports in D4 and their focused tests.
- Historical worklog and route-status prose.
- The downstream wl594/wl595 references found by the protected scan.
- The absent wl588 artifact, which is explicitly a not-created checkpoint.

## Focused Validation Commands

These commands are recorded for the later non-destructive cutover and were not
run in this inventory turn.

~~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl586|wl593|wl586_route_selection|wl593_factor_twist_generalization_route_death' \
  docs scripts tests data

rg -n -uu --glob '!**/__pycache__/**' \
  'wl587|wl589|wl590|wl591|wl592|D0u|D0m|D5|D7|D17' \
  scripts/theory/aa_bb tests/theory/aa_bb docs/codex/tasks/wl500-series-consolidation

rg -n -uu --glob '!**/__pycache__/**' \
  'results/|audit_closure_|importlib|subprocess|\.glob\(|\.rglob\(|wl594|wl595' \
  scripts/theory/aa_bb/d4_factor_twist.py \
  scripts/theory/aa_bb/consolidation_inputs.py
~~~~

The third scan is expected to find materializer/provenance strings in
consolidation_inputs.py, but no results/ or legacy fallback in D4. It must not
be interpreted as permission to remove the materializer boundary.

The focused proof/parity gate specified by D4 is:

~~~~bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl587_pure_u7_d0_relative_2_descent.py \
  tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py \
  tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py \
  tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py \
  tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py \
  tests/theory/aa_bb/test_d4_factor_twist.py
~~~~

Also required after a later cutover are targeted Ruff, formatter checking,
py_compile, deterministic temporary D4 CLI output, and git diff --check. The
full-suite performance command belongs to the later C4 gate and was not run
here.

## Deletion-Gate Verdict

~~~~text
deletion_gate = CLOSED
cutover_performed = false
deletion_performed = false
wl594_entered = false
~~~~

The canonical graph and D4 destination exist, and the active anchor records
Controller acceptance of the non-destructive D4 implementation. That is not
enough to open deletion. Current evidence still contains legacy runtime
consumers, old operational README commands, old manifest consumer paths, old
per-WL tests, and legacy/materialization uses of ignored results. The required
separate Controller approval is absent, and this turn intentionally performed
no parity or test rerun.

The next permitted change is a non-destructive consumer cutover that updates
imports, operational paths, and manifest consumer_paths while retaining old
worklogs, scripts, tests, and provenance. Deletion remains limited to a later
approved removal of superseded wl586/wl593 assets; D0u, D0m, D5, D7, D17 and
their focused tests remain protected.
