# 031-heegner-height-diagnostic

## Summary

Direction five is now wired into the proof-status pipeline as a conservative
`heegner` diagnostic method.

This is **not** the full Heegner-height proof engine yet.  The method can find a
positive chain witness if one appears in the scanned rank-one Mordell-Weil cosets,
but it deliberately does **not** return `no_solution` from a bounded scan.

## Code landed

- New module: `src/rational_distance/concordant/heegner_height.py`
- New method body: `proof_status/methods.py::run_heegner_height`
- Backward-compatible symbol: `run_heegner_stub(...) -> run_heegner_height(...)`
- Default pipeline method name remains `heegner`
- CLI knobs:
  - `--heegner-multiple-bound`
  - `--heegner-height-bound`
- Regression test for `(A, B) = (7, 45)`:
  - default scan has exact rank `[1, 1]`
  - `concordant_n == [24]`
  - `chain_compatible_n == []`

## Mathematical safety contract

For a rank-one curve

\[
E: y^2 = x(x + A^2)(x + B^2),
\]

the implementation takes the generator returned by PARI `ellrank`, computes
PARI `ellheight`, then scans points

\[
nG + T
\]

where `T` ranges over the known torsion points and `|n| <= bound`.

For each scanned point it checks:

1. whether `x` is a positive integer square `N²`;
2. whether `N² + A²` and `N² + B²` are both squares;
3. whether `N` satisfies the full chain-closure compatibility test.

Outcomes:

- `solution_found` if a real chain-compatible `N` is found;
- `inconclusive` for rank-one scans with no witness;
- `inconclusive` when PARI proves rank one but returns no generator list;
- `skipped` for exact rank not equal to one;
- never `no_solution` from this method yet.

The missing piece for a strict proof is still a certified global height bound (or
an equivalent theorem proving that all square-X cosets have been exhausted).

## Validation commands

```bash
uv run pytest tests/test_proof_status.py -q
uv run ruff check \
  src/rational_distance/concordant/heegner_height.py \
  src/rational_distance/proof_status/methods.py \
  src/rational_distance/proof_status/workflow.py \
  scripts/prove_no_solution.py \
  tests/test_proof_status.py
```

Results:

```text
21 passed
All checks passed!
```

## max_hyp=500 proof-status run

Command:

```bash
/usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --max-hyp 500 \
  --db .cache/proofs_500_heegner.sqlite3 \
  --no-progress
```

Runtime:

```text
real 4.74
user 2.80
sys  1.90
```

Status histogram:

```text
Total pairs:      6172
no_solution:      5852  (94.82%)
solution_found:      0  ( 0.00%)
hard_case:         320  ( 5.18%)
unknown:             0
```

Method-outcome breakdown:

```text
safe_sieve:         no_solution 5632, pass 540
factor_concordant:  no_solution 220, inconclusive 320
rank_zero:          inconclusive 320
heegner:            inconclusive 118, skipped 202
chabauty:           skipped 320
brauer_manin:       skipped 320
```

Hard-case rank distribution:

```text
rank=1: 118
rank=2: 155
rank=3:  43
rank=4:   4
```

Heegner details:

```text
rank-one scan ran:                  116
rank-one but missing PARI generator:  2
rank-not-one skipped:               202
```

Important interpretation: this exactly matches the previous `max_hyp=500`
rank-one count (118).  The new method records height/generator diagnostics but
intentionally leaves the final status as `hard_case` unless it finds a real chain
witness.

## max_hyp=1000 proof-status run

Command:

```bash
/usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --max-hyp 1000 \
  --db .cache/proofs_1000_heegner_v2.sqlite3 \
  --no-progress
```

Runtime:

```text
real 19.63
user 12.68
sys   8.14
```

Status histogram:

```text
Total pairs:     24197
no_solution:     23011  (95.10%)
solution_found:      0  ( 0.00%)
hard_case:        1186  ( 4.90%)
unknown:             0
```

Method-outcome breakdown:

```text
safe_sieve:         no_solution 22077, pass 2120
factor_concordant:  no_solution   934, inconclusive 1186
rank_zero:          inconclusive 1186
heegner:            inconclusive  392, skipped 794
chabauty:           skipped 1186
brauer_manin:       skipped 1186
```

Hard-case rank distribution:

```text
rank=1: 392
rank=2: 560
rank=3: 213
rank=4:  20
rank=5:   1
```

Heegner details:

```text
rank-one scan ran:                  387
rank-one but missing PARI generator:  5
rank-not-one skipped:               794
```

## Takeaway

The conservative direction-five implementation is now useful for collecting
rank-one generator/canonical-height evidence at scale.  It does not reduce the
hard-case count yet, by design.  The next mathematical task is to turn these
bounded scans into certified exclusions by proving a global height bound for the
chain-compatible square-X condition.
