# 016 — Primitive Pythagorean Decomposition Display

## Summary

Each solution to the Pythagorean 4-cycle now shows the full primitive-triple
decomposition for all four edges.  This makes it easy to see which primitive
triples underlie a solution and how many times they are scaled.

## Main Changes

### `src/rational_distance/search_chain.py`

Added module-level helpers:

- **`_primitive_decomp(a, b, h) → (k, P, Q, H)`**
  Returns the scale factor `k = gcd(a, b)` and the primitive triple `(P, Q, H)`
  where `P = a//k`, `Q = b//k`, `H = h//k`.  By construction `gcd(P, Q) = 1`
  and `P² + Q² = H²`.

- **`_edge_str(a, b, h) → str`**
  Formats one edge as `"a²+b²=h²  →  (P,Q,H)"` (primitive) or
  `"a²+b²=h²  →  k×(P,Q,H)"` (scaled).

Updated `ChainResult`:

- **`edges() → list[str]`** — property returning the four edge strings for
  `x1..x4`.
- **`__str__`** — now multi-line; header row followed by one indented edge line
  per `x1..x4`.  Removed the old compact `hyp=(…)` column.

Updated **`results_to_json`** to include an `"edges"` list per result, where
each entry carries `{leg1, leg2, hyp, scale, primitive}`.

### `scripts/search.py`

`_run_chain`: replaced the dense tabular display with `str(r)` per result,
showing the full multi-line decomposition.

### `tests/test_all.py`

`test_chain_result_str`: updated assertion from `"hyp=" in s` to checking for
`x1:`/`x2:`/`x3:`/`x4:` labels and `→` in the output.

## Example Output

```
(25,60,91,312)  rect=116×372  sq=✗
  x1: 25²+60²=65²   →   5×(5,12,13)
  x2: 60²+91²=109²  →   (60,91,109)
  x3: 91²+312²=325² →  13×(7,24,25)
  x4: 312²+25²=313² →   (312,25,313)
```

The smallest general-family solution uses four distinct primitive triples:
`(3,4,5)`, `(60,91,109)`, `(7,24,25)`, `(312,25,313)` — the last two are
primitive, the first two are scaled by 5 and 13 respectively.

## Tests

All 65 tests pass.
