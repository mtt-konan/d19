# wl500-wl593 Evidence And Test Consolidation Plan

## Status

```text
plan_status = controller_accepted
execution_status = complete
scope = wl500-wl593 worklogs, audit scripts, tests, and direct consumers
active_research_route_changed = false
```

This is not documentation-only compression. Worklogs, executable evidence, and
tests are consolidated together. Runtime improvement must come from removing
redundant proof-chain execution and subprocess tests, never from dropping a
mathematical obligation.

## Baseline

| Range | Worklogs / lines | Scripts / lines | Tests / lines | Test functions | Subprocess calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| `500-529` | 30 / 4,977 | 30 / 14,044 | 30 / 6,559 | 146 | 30 |
| `530-585` | 57 / 8,452 | 57 / 9,559 | 57 / 6,245 | 290 | 57 |
| `586-593` | 7 / 2,116 | 7 / 5,110 | 7 / 921 | 28 | 2 |
| Total | 94 / 15,545 | 94 / 28,713 | 94 / 13,725 | 464 | 89 |

The range contains 57,983 lines across 282 WL-indexed files. Counts are not
proof-strength measures.

## Long-Term Objective

Replace the 94 artifacts of each kind with the smallest reviewable canonical
evidence graph that preserves every unique formula, finite proof datum,
converse, exceptional branch, local image, and route boundary; removes
superseded tests and per-WL subprocess launches; records provenance from every
old path; and makes future runtime grow with mathematical obligations rather
than narrated microsteps.

## C0 Verdict

Controller-accepted outcome:

```text
additional_irreducible_checkpoint_required
```

The original four semantic groups were directionally correct but missed two
mandatory tracked-input checkpoints. Current scripts consume proof inputs that
exist only under ignored `results/`:

- `wl522` loads all `wl491-wl521` result payloads;
- `wl527` loads `wl522` and `wl526` payloads;
- `wl529` loads selected pre-scope `wl495` data;
- `wl586` consumes exact `wl505`, `wl522`, and `wl527` payloads, while its
  tests use reduced synthetic fixtures.

Deleting those chains before materialization would weaken reproducibility.

## Canonical Graph

```text
A0 -> A1 -> A2
B0 -> B1
C1 -> C2 -> C3
D0u ----\
D0m -----+-> D5 -> D7 -> D17 -> D4
A0/A2 ---/
```

- `A0`: tracked exact finite-ledger inputs, including `wl505` witnesses, all
  43 entries, 22 taxonomy rows, and the 15-family `wl527` inventory.
- `A1`: finite-shell, ambient-point, MW/no-lift, and routing certificates.
- `A2`: taxonomy, point-level obstruction, failed uniform promotion, and
  no-claim boundary.
- `B0`: tracked selected `wl495` rows used by the prototype.
- `B1`: exact `wl528-wl529` prototype and square-locus closure.
- `C1`: `wl530-wl541`, exact target and local-method classification.
- `C2`: `wl542-wl568`, global descent and allocation-route exhaustion.
- `C3`: `wl569-wl585`, reconstruction, geometry, and quotient-route boundary.
- `D0u`, `D0m`: separate pure and mixed D0 kernels.
- `D5`, `D7`, `D17`: separate exact local-image kernels.
- `D4`: `wl586` cross-family evidence merged with `wl593` scoped route death.

The target is not one monolith. Extra modules are allowed only for an
irreducible proof obligation recorded in the C0 map.

## Retention Rules

Keep executable evidence when it contributes an exact certificate, finite
proof input, converse/exception proof, independent local/global obstruction,
or live theorem boundary. A separate builder/test is not justified only by
route selection, repeated no-claim flags, predecessor readiness, identical CLI
serialization, or counts already frozen in a canonical taxonomy.

Protected kernels are `wl528-wl529`, `wl535`, selected exhaustion
subcertificates in `wl539-wl585`, `wl587`, `wl589`, `wl590-wl593`, and the
completed `wl594` downstream boundary. Structural extraction must not change
formulas, quantifiers, representatives, bad-prime sets, local images,
positivity, exceptions, or theorem strength.

## Execution Gates

### C1: Schemas And Parity Oracles

Define minimal tracked schemas for `A0/B0`. Classify every field as finite
input, reproducible certificate, provenance, or disposable execution metadata.
Do not copy whole ignored payloads or treat `ready=True` as proof. Define exact
old/new projections before implementation.

C1 is complete. The accepted design uses five versioned canonical data files
plus one manifest, one standard-library loader/materializer, and focused parity
tests. It does not add a JSON-schema dependency or separate schema-file layer.

### C2: Semantic Implementation

Implement in this dependency order:

1. `A0`, then `B0`;
2. `A1/A2`;
3. `B1`;
4. `C1`, `C2`, `C3`;
5. `D4`, while keeping the six D kernels separate.

Each slice adds canonical code and focused tests, runs old/new parity, preserves
fail-closed behavior, uses a shared CLI runner, and is independently
reviewable. No legacy file is deleted in the same step that first replaces it.

The first C2 slice is Controller-accepted. It materializes the tracked A0/B0
inputs, validates the exact `43/8/22/15/2` projections and witness equations,
binds them to the `9b73cd4` source payloads, reconstructs consumable
`wl522`/`wl527`/`wl586`/`wl528` compatibility views, and fails closed without a
runtime `results/` fallback. The checked-in data and a fresh materialization
are byte-identical. No legacy consumer has been switched and no old file has
been removed. The next implementation slice is `A1/A2` only.

The `A1/A2` slice is also Controller-accepted. It replaces the recursive
`wl500-wl527` execution graph with genuine shell arithmetic, 12 deduplicated
cover certificates, exact MW/no-lift recomputation, the `wl491` point filter,
and 28 stage-specific semantic projections. The two new tracked projections
are source-hash and projection-hash bound by the manifest. Exactly one shared
CLI subprocess remains in the new tests. Legacy consumers and files are still
present; cutover and deletion remain closed. The next slice is protected B1
(`wl528-wl529`) design and parity extraction.

B1 is now Controller-accepted as one protected module, one focused test, and
one tracked Sage certificate. It preserves exact `wl528`/`wl529` semantics,
uses tracked B0 at runtime, and reduces the two per-WL CLI tests to one shared
smoke test. No cutover or deletion has occurred. The next semantic slice is
the `C1` group `wl530-wl541`; `C2/C3` remain later slices.

C1 is now Controller-accepted as six mathematical kernels and two focused test
files. It computes all twelve `wl530-wl541` stages once, preserves the protected
`wl535`, `wl539`, and `wl541` obligations, and replaces twelve CLI subprocesses
with one strict entrypoint. Legacy files remain in place. The next slice is C2
(`wl542-wl568`).

### Ignored-Result Cutover

The non-destructive cutover freezes the complete accepted semantic surface as
91 test-only projection digests: `5 A1 + 28 A2 + 2 B1 + 12 C1 + 27 C2 + 17 C3`.
Digests use canonical JSON with sorted keys, compact separators, and ASCII
encoding. Affected default tests now build canonical projections directly and
retain their formula, exception, no-claim, fail-closed, and strict CLI checks;
the C1 consolidated-result check uses computed evidence.

Materializer and regeneration tests live under `manual_tests/` and remain an
explicit migration tool. Its 30 selected ignored source payloads are frozen by
relative path, byte size, and SHA256 and are validated before JSON parsing;
missing, selection, path, size, and hash drift fail closed. Default pytest
continues to discover only `tests/`. No result, canonical payload, schema, or
digest was deleted or rewritten in this cutover.

### Non-Destructive Worklog Cutover

The bounded documentation cutover creates
`docs/work-logs/523-529-common-source-function-field-squareclass-consolidated.md`
and updates only the six named human-facing index/control documents:
`docs/work-logs/README.md`, `docs/work-logs/archive/README.md`,
`docs/NEXT_RESEARCH_GATE.md`, `docs/GLOSSARY.md`, `scripts/README.md`, and this
plan. Current readers are routed through the three consolidated histories
`491-522`, `523-529`, and `530-585`; wl586 and wl593 are read as D4 semantic
projections; wl587, wl589, wl590, wl591, and wl592 remain five protected
appendices; wl594+ remains downstream context.

The new history is human-only and runtime-independent. It preserves the
wl523-wl529 source result/script/test path strings and does not rewrite
manifest/loader provenance. This cutover does not delete worklogs or edit code,
tests, data, results, task anchors, protected kernels, D4, or wl594+.

### C3: Cutover And Pruning

After every old obligation has a passing destination, update imports, paths,
README/control references, and a provenance manifest. Remove superseded
scripts/tests rather than moving them into another active test namespace.
Retain only consolidated worklogs or justified mathematical appendices. A
separate Controller approval is required before deletion.

### C4: Verification And Performance

Use one baseline and one final full run:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest --durations=50
```

Intermediate slices use focused parity tests, targeted Ruff, reference scans,
and `git diff --check`. Success requires no lost obligation, unchanged claim
boundaries, no per-WL strict subprocess pattern in scope, all tests passing,
and at least 30% whole-suite wall-time reduction or evidence that the remaining
bottleneck is outside this range. Evaluate `xdist` only afterward.

Controller verification is complete. The pre-cutover baseline was `1748 passed,
2 warnings in 203.20s`; the final run is `1363 passed in 29.35s`, with no
warnings. This is an `85.56%` wall-time reduction and beats the `142.24s`
target by `112.89s`. Focused canonical/protected validation is `176 passed`,
and the explicit materializer suite is `36 passed`. The final gate also passes
targeted Ruff, format, static ignored-result-read scanning, and
`git diff --check`.

## Forbidden Work

No new WL or mathematics; no shell 11, support search, rank/Selmer work, fixed
family sample, or theorem-strength change; no reliance on ignored results after
cutover; no replacement of proof code by cached booleans; no unrelated
pre-`wl500` refactor; no file-count optimization that harms reviewability.

## Controller Contract

The upper agent owns sequence, review, parity acceptance, deletion, validation,
and commits. It delegates one narrow task at a time with:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh \
  --workspace /Users/konan/Desktop/d19 \
  --model gpt-5.6-luna \
  --reasoning max \
  "<focused task>"
```

Use `--read-only` for audits. Fast service is inherited from Codex config;
there is no `--fast` flag. Every Worker prompt starts by forbidding Codex,
`ask_codex.sh`, subagents, and delegation skills. Worker success is not
Controller acceptance.

## Stop Policy

Stop before implementation unless `A0/B0` have explicit schemas, provenance,
and parity projections. Stop before deletion until every affected semantic
group passes old/new parity. Keep uncertain evidence and open a narrower audit.
Stop consolidation when the active route is compact, reviewable, and the
runtime target is met.
