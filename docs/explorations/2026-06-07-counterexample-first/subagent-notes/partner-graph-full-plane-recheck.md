Slice:

partner-graph-full-plane-recheck

Controller follow-up:

The exhaustive full-plane `G_M @ max_value=1M` scan recommended by this note has
now been completed in `docs/explorations/2026-06-07-next-step-hard-layer/`.
It scanned `338,225` vertices and `5,071,562` full-plane relation rows, found
`0` full-plane hits, and confirmed global min delta `1` in this stored graph
window. Keep the older bounded-sample notes below as historical context.

Goal:

Recheck whether old partner graph / `G_M` / island no-hit and delta claims used full-plane GEN-CLOSURE, then look for true full-plane closure hits first. If no hit appears, record the smallest full-plane near-misses and which old sum-only statements need downgraded wording.

Files inspected:

- `docs/PARTNER_GRAPH_THEORY.md`
- `scripts/partner/full_gm_closure_scan.py`
- `scripts/partner/full_gm_delta_stats.py`
- `scripts/partner/comp0_island_analysis.py`
- `scripts/partner/island_properties.py`
- `scripts/partner/verify_islands_unbounded.py`
- `tests/test_gm_closure_delta.py`
- `src/rational_distance/concordant/analysis.py`
- `src/rational_distance/concordant/factor_search.py`
- `src/rational_distance/results/gm_closure_delta.py`
- `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md`
- `docs/work-logs/066-gm-clarify-and-delta-near-miss.md`
- `docs/work-logs/093-closure-necessity-linear-relations-A9.md`
- `docs/work-logs/094-gen-closure-landing-A9.md`
- `docs/work-logs/094-k9-k10-ellrank-full-audit.md`
- `results/partner/partner_full_bfs_summary.json`
- `results/partner/full_gm_closure_scan_summary.json`
- `results/partner/full_gm_delta_summary.json`
- `results/partner/full_gm_delta_top.jsonl`
- `results/partner/partner_full_bfs_components.jsonl`
- `results/partner/comp0_island_analysis_1M_summary.json`
- `results/partner/island_properties_1M.json`
- `results/partner/island_unbounded_bfs.json`
- `results/partner/k10_ellrank_wl063.jsonl`
- `results/partner/k9k10_ellrank_full.jsonl`

Commands run:

- `rg -n "closure|delta|N_i|N_j|A \\+ B|A\\+B|sum|diff|abs|GEN|full-plane|island|G_M|partner" ...`
- `rg --files docs/work-logs docs | rg '(^|/)(018-025|041|052|063|066|093|094)'`
- `sed -n ...` and `nl -ba ... | sed -n ...` on the files listed above for line-numbered evidence.
- `PYTHONPATH=src uv run python scripts/theory/closure_necessity_relations.py --max-hyp 2000`
- `uv run pytest tests/test_gm_closure_delta.py -q`
- Inline bounded full-plane verifier over selected `results/partner` data. It used `find_concordant_by_factorization`, mirrored `analysis.gen_closure_hit`, and computed min full-plane delta over `sum=A+B`, `sum=|A-B|`, `diff=A+B`, and `diff=|A-B|`.
- `git status --short`

Search domain:

- Old full-`G_M` data: `results/partner/partner_full_bfs_summary.json` reports `338225` vertices, `350868` edges, `9580` components, and largest component size `309689` at `max_value=1000000`.
- Old full-`G_M` closure result: `results/partner/full_gm_closure_scan_summary.json` reports `338225` vertices and `0` closure hits, but the script checks only `N_i + N_j == A + B`.
- Old full-`G_M` delta result: `results/partner/full_gm_delta_summary.json` reports `829444` candidate pairs, `0` zero deltas, and global min `|delta| = 1`, but the helper and script compute only `(A+B) - (N_i+N_j)`.
- Island data: `results/partner/comp0_island_analysis_1M_summary.json` reports `8959` island components and `0` `closure_hits_total`; `results/partner/island_unbounded_bfs.json` reports those islands close to the exact original vertex sets under unbounded partner BFS. The island scripts use exact partner expansion, but their Harborth closure counter is also sum-only.
- Existing exact full-plane verifier: `scripts/theory/closure_necessity_relations.py --max-hyp 2000` checked `8220` safe-pass pairs, including `67` multi-N pairs, and found `0` sum hits and `0` non-sum full-plane hits.
- New bounded partner sample: `2293` unique `G_M` vertices sampled from the first `50` old sum-only near-miss rows plus their closest partner vertices, all `16` wl063 K9/K10 sample hubs, `1000` smallest-by-sum component vertices, `1000` deterministic stride vertices, and `250` vertices from components of size `<=2`.

Closure predicate:

- Current full-plane predicate is in `src/rational_distance/concordant/analysis.py:298`: `GEN-CLOSURE` means `{N1+N2, |N1-N2|} intersect {A+B, |A-B|} != empty`.
- `analysis.py:306-309` maps the four relations to plane regions: `sum=A+B`, `sum=|A-B|`, `diff=A+B`, and `diff=|A-B|`.
- `analysis.py:322-332` loops with `j` starting at `i`; this allows `N_i = N_j` for sum relations and requires distinct values for difference relations.
- The legacy compatibility helper is explicitly sum-only: `analysis.py:285-289` says `check_chain_compatibility` checks only `N1+N2 = A+B`.
- The old full-`G_M` scan is sum-only: `scripts/partner/full_gm_closure_scan.py:4` describes checking `N_i + N_j == A + B`, and `scripts/partner/full_gm_closure_scan.py:34-37` implements exactly that with distinct pairs.
- The old delta script is sum-only: `scripts/partner/full_gm_delta_stats.py:67-69` computes `delta = (a+b) - (n1+n2)`, and `src/rational_distance/results/gm_closure_delta.py:26-31` does the same in its helper.
- The old island closure counter is sum-only: `scripts/partner/comp0_island_analysis.py:17-19` describes `N_i + N_j == A + B`, and `scripts/partner/comp0_island_analysis.py:90-94` implements that check.

Exact or bounded:

- Exact for old question: the old full-`G_M` closure and delta data are exhaustive over the stored `G_M @ max_value=1M` vertices, but only for the inside-square sum relation.
- Exact for graph-island closure: `scripts/partner/verify_islands_unbounded.py:2-11` tests island components with unbounded partner BFS and shows they do not leak under the partner relation. This does not test full-plane Harborth closure.
- Exact for small full-plane domain: the `max_hyp=2000` current verifier found no GEN-CLOSURE hit in `8220` safe-pass pairs, including `67` multi-N pairs.
- Bounded for this partner recheck: the inline full-plane verifier covered `2293` selected partner vertices. It did not exhaust all `338225` `G_M @ max_value=1M` vertices.
- Not global: none of these finite windows proves anything for infinite `G_M`, larger `max_value`, or all non-coprime scaling strata.

Hits:

- Full-plane hits in the new bounded partner sample: `0 / 2293`.
- Full-plane hits in the existing `max_hyp=2000` verifier: `0` relation hits among `8220` safe-pass pairs.
- Old full-`G_M` sum-only hits: `0 / 338225` vertices.
- Old full-`G_M` sum-only delta zero count: `0 / 829444` candidate pairs.
- Old island sum-only closure hits: `0`, but this should not be quoted as full-plane unless rerun with GEN-CLOSURE.

Top near-misses:

The new bounded sample found minimum full-plane delta `1`. The first examples below show all four relation families.

| `(A,B)` | comp | k | relation | `N` row | value vs target | full-plane delta |
|---|---:|---:|---|---|---|---:|
| `(63,80)` | 6602 | 2 | `sum=A+B` | `(60,84)` | `144` vs `143` | `1` |
| `(92,440)` | 0 | 2 | `diff=A+B` | `(525,1056)` | `531` vs `532` | `1` |
| `(153,560)` | 15 | 3 | `sum=|A-B|` | `(204,204)` | `408` vs `407` | `1` |
| `(990,1575)` | 0 | 3 | `diff=|A-B|` | `(1320,1904)` | `584` vs `585` | `1` |
| `(3024,3675)` | 0 | 3 | `sum=A+B` | `(1260,5440)` | `6700` vs `6699` | `1` |
| `(12180,16236)` | 1758 | 2 | `sum=A+B` | `(12177,16240)` | `28417` vs `28416` | `1` |

Bounded sample counts:

- Sampled unique pairs: `2293`.
- Max `k` in sample: `10`.
- `k` distribution: `{2: 1645, 3: 436, 4: 149, 5: 32, 6: 12, 7: 3, 9: 10, 10: 6}`.
- Primary best-relation counts: `sum=A+B: 939`, `sum=|A-B|: 827`, `diff=A+B: 293`, `diff=|A-B|: 234`.
- `min_full_plane_delta <= 10` distribution: `{1: 19, 2: 9, 3: 9, 4: 11, 5: 11, 6: 12, 7: 28, 8: 5, 9: 4, 10: 3}`.

Observed patterns:

- The old partner `G_M` no-hit and delta statements are correct for `N_i + N_j = A+B`, but they are not full-plane GEN-CLOSURE statements. The code evidence is direct in `scripts/partner/full_gm_closure_scan.py:34-37`, `scripts/partner/full_gm_delta_stats.py:67-69`, and `src/rational_distance/results/gm_closure_delta.py:26-31`.
- `docs/PARTNER_GRAPH_THEORY.md:317-326` still presents the Harborth translation as only `N1+N2=A+B`, and `docs/PARTNER_GRAPH_THEORY.md:341-342` says the scanned range has no Harborth counterexample. That statement should be downgraded or annotated with the later wl093 full-plane correction.
- wl063 is also sum-only. It says the tool checks `N_i + N_j == A + B` at `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:10-14`, then phrases the result as `0` counterexamples at `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md:20-22`.
- wl066 is sum-only delta. It defines delta as `(A+B)-(N_i+N_j)` at `docs/work-logs/066-gm-clarify-and-delta-near-miss.md:135-143` and reports `0` hits / min `|delta|=1` at `docs/work-logs/066-gm-clarify-and-delta-near-miss.md:152-157`.
- wl093 fixed the semantics. It says the old predicate only checked `N1+N2=A+B` at `docs/work-logs/093-closure-necessity-linear-relations-A9.md:15-19`, gives the full-plane condition at `docs/work-logs/093-closure-necessity-linear-relations-A9.md:21-29`, and explicitly says the large-scale `max_hyp=5e6` extension is still sum-only while full-plane scale remains `max_hyp=2000` at `docs/work-logs/093-closure-necessity-linear-relations-A9.md:169-173`.
- Near-misses appear in all four full-plane relation families in the bounded partner sample. This matters because the old `full_gm_delta_top.jsonl` only ranks the `sum=A+B` relation.
- Some full-plane near-misses use equal `N` on sum relations, such as `(153,560)` with `(204,204)`. Any full-plane scan should mirror `analysis.gen_closure_hit`, not the old `combinations(ns, 2)` loop alone.
- High `k` did not produce a hit in this sample. The bounded sample included all `16` wl063 K9/K10 sample hubs and still found no full-plane closure hit.

What this rules out:

- It rules out treating the old `full_gm_closure_scan.py` and `full_gm_delta_stats.py` outputs as full-plane GEN-CLOSURE data.
- It rules out reading the island `closure_hits_total=0` as a full-plane Harborth no-hit. The island result proves graph components are closed under partner expansion, not that every full-plane relation was checked.
- It gives a bounded negative check for selected old near-misses, selected high-`k` hubs, and representative component samples under the current full-plane predicate.

What this does not rule out:

- It does not rule out a full-plane GEN-CLOSURE hit somewhere else among the `338225` `G_M @ max_value=1M` vertices.
- It does not rule out a hit in larger partner windows, infinite `G_M`, or max-value extensions.
- It does not close the gcd-scaling caveat. wl093 already marks that as independent of the sum-only to full-plane upgrade.
- It does not make the old full-`G_M` min delta `1` a full-plane global min. The new min `1` is only from a bounded sample.
- It does not prove soundness or unsoundness of the whole project. This slice only checks partner graph / `G_M` / island search semantics and bounded full-plane rechecks.

Recommended next attack:

1. Run an exhaustive full-plane `G_M @ max_value=1M` scan over all `338225` vertices, using `analysis.gen_closure_hit` for hits and a full-plane delta helper for near-misses. Preserve the four relation names and allow `i == j` for sum relations.
2. Do the smaller exact island pass first: rerun all `8959` islands / `22889` island vertices with full-plane GEN-CLOSURE and full-plane deltas. This should be cheap and will cleanly separate graph-island closure from Harborth closure.
3. Replace or annotate old ledger claims: `full G_M closure=0`, `full G_M min |delta|=1`, and island `closure_hits_total=0` should read `sum-only / inside-square` until a full-plane all-vertex scan exists.
4. Store full-plane result rows with fields `{A,B,k,component_id,relation,N1,N2,value,target,delta}` so later subagents do not have to infer which closure notion was used.

Plain-language summary:

旧 partner graph 数据没有错，但它回答的是较窄的问题：只问点在正方形里面时的闭合 `N1+N2=A+B`。现在项目采用的全平面问题还要检查外部三种关系，也就是还要看和/差是否等于 `A+B` 或 `|A-B|`。我用当前全平面规则复查了 `2293` 个有代表性的 partner 顶点，没有找到真闭合；最近只差 `1`，而且四种关系都出现了差 `1` 的 near-miss。主 ledger 应把旧 `G_M` 和 island 的 “0 closure / min delta” 降级为 “sum-only 证据”，直到跑完全 `338225` 顶点的 full-plane 扫描。
