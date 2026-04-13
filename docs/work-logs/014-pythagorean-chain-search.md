# 014 — Pythagorean 4-Cycle Search (Chain Method)

## Problem statement

The rational-distance unit-square problem asks for a point P = (x, y) with rational distances to all four corners A(0,0), B(1,0), C(1,1), D(0,1). If we write P = (a/k, b/k) where a, b, k are positive integers and k = a+c = b+d (with c = k-a, d = k-b), the four distance conditions become:

```
a² + b² = x₁²
b² + c² = x₂²
c² + d² = x₃²
d² + a² = x₄²
a + c = b + d     ← unit-square constraint (5th equation)
```

All five conditions must hold simultaneously (with x₁…x₄ rational, equivalently integer when scaled by k).

## Motivation for the chain approach

The 5th equation `a + c = b + d` pins the solution to the unit square specifically. Dropping it yields the **generalised rectangle problem**: find a point (a, b) with rational distances to all four corners of the (a+c) × (b+d) rectangle. Solutions to this relaxed system may exist even if the unit-square problem has none.

Geometrically, the 4 equations define a **Pythagorean 4-cycle** — a 4-cycle in the graph G where nodes are positive integers and there is an edge (p, q) whenever p² + q² is a perfect square (i.e., (p, q, h) is a Pythagorean triple for some integer h).

## Algorithm

1. **Build adjacency lists** (numpy-vectorised):  
   For each `a ∈ [1, max_val]`, compute `a² + b²` for all `b` simultaneously using a numpy int64 array, then apply an integer-sqrt check (`floor(sqrt(·))² == ·`) with ±1 correction for float rounding. Store `adj[a]` = list of neighbours and `hyp[a][b]` = hypotenuse.

2. **Find 4-cycles** (triple-nested loop + set intersection):  
   For each (a, b, c) where (a,b) and (b,c) are edges, compute  
   `D = adj_set[c] ∩ adj_set[a]`  
   Every `d ∈ D` closes the 4-cycle (a, b, c, d).

3. **Canonical deduplication** (dihedral group D₄):  
   Each undirected cycle appears under 8 symmetries (4 rotations × 2 reflections). We keep only the lexicographically smallest representative.

4. **5th-constraint filter** (`--require-square`):  
   After finding all cycles, optionally retain only those with `a + c == b + d`.

## Results

| max_val | 4-cycles found | satisfy a+c=b+d | time  |
|---------|---------------|-----------------|-------|
| 100     | 206           | 0               | <0.1s |
| 500     | 2525+         | 0               | ~1s   |

No solution satisfying the 5th constraint was found up to `max_val = 500`, consistent with the Harborth conjecture.  The smallest 4-cycle is (3, 4, 3, 4) representing the centre of a 6 × 8 rectangle at equal distances of 5 from all four corners.

## Files changed

| File | Change |
|------|--------|
| `src/rational_distance/search_chain.py` | New module: `find_chains`, `ChainResult`, `_build_adjacency` |
| `scripts/search.py` | Added `chain` subcommand + `_run_chain` runner |
| `tests/test_all.py` | 6 new tests for `search_chain` (59 total, all pass) |

## Usage

```bash
# All Pythagorean 4-cycles up to 200
uv run python scripts/search.py chain --max-val 200

# Only solutions that also satisfy the unit-square constraint
uv run python scripts/search.py chain --max-val 500 --require-square

# Save to JSON for later analysis
uv run python scripts/search.py chain --max-val 1000 --out chain.json
```
