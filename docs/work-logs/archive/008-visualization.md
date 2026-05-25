# Work Log 008 — Interactive Visualization

## Summary

Added `scripts/visualize.py` — a self-contained tool that reads any JSON results
file and generates an interactive HTML report using Plotly.js.

## Changes

- **New file**: `scripts/visualize.py`
- **New dependency**: `plotly` added to `pyproject.toml` (via `uv add plotly`)

## Usage

```bash
uv run python scripts/visualize.py results.json          # generates results.html + opens browser
uv run python scripts/visualize.py results.json --inside # only points inside unit square
uv run python scripts/visualize.py results.json --out report.html --no-open
```

## Visualizations Included

1. **Main scatter plot** — all points on the plane, colored by which vertex has
   the irrational distance (B=blue, C=green, D=orange, none/4-vertex=purple).
   Unit square is outlined with a dashed border.

2. **Missing-vertex bar chart** — counts of which vertex is irrational for each
   solution point.

3. **Denominator histogram** — distribution of the coordinate denominator across
   all solutions.

4. **dA vs dB scatter** — distance to A plotted against distance to B for all
   points where both are rational.

5. **dC vs dD scatter** — same for C and D.

6. **Points colored by denominator** — scatter with Viridis colorscale to
   reveal whether small/large denominators cluster spatially.

7. **Pattern Insights panel** — auto-generated observations based on the data.

## Key Patterns Observed

Running on `results_3v.json` (402 points, scale=80):

| Observation | Detail |
|---|---|
| A(0,0) never irrational | Expected — A is the parametric anchor; dA is always rational by construction |
| B and D equally irrational | B=184, D=184 — reflects D4 diagonal symmetry (y=x reflection swaps B↔D) |
| C rarely irrational | C=34 vs B/D=184 — the opposite diagonal vertex is structurally easier to hit rationally |
| Only ~13% inside unit square | 52/402 inside; majority of solutions lie outside |
| All points come in (x,y)/(y,x) pairs | 201 symmetric pairs — the parametrization and dedup produce mirror images along y=x |
| Most points in "top strip" (0<x<1, y>1) | 222 top vs 114 right vs 52 inside vs 14 far |

## Potential Search-Space Narrowing (observations)

- Restricting search to inside the unit square reduces candidates by ~87%.
  The user already has a planned `--inside` constraint (theoretically motivated).
- B and D are structurally equivalent; any solution found with dB irrational has
  a mirror with dD irrational — no need to search both.
- The "top strip" (y>1) dominates; if adding an upper bound on y could be
  theoretically justified, it would cut space significantly.
- The C-vertex being rarely irrational suggests the parametrization preferentially
  produces rational dC; it may not be the "hard" constraint.

## Notes

- The HTML is self-contained (Plotly loaded from CDN) and works offline once
  Plotly is cached, or on any machine with internet access.
- Generated HTML files (`*.html`) are not committed to git (see `.gitignore`).
- Supports `--inside` flag to filter to unit-square points only for focused
  analysis when using the planned interior constraint.
