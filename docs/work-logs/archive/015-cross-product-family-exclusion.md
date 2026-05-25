# 015 — Cross-Product Family Exclusion from Chain Search

## Summary

Identified and excluded a provably-impossible sub-family from the Pythagorean
4-cycle search, reducing the search space to only those solutions that could
theoretically satisfy the Harborth conjecture.

## The cross-product family

Any two Pythagorean pairs (p,q) and (m,n) generate a Pythagorean 4-cycle:

```
(a, b, c, d) = (pm, qm, qn, pn)
```

Verification:
- a²+b² = m²(p²+q²) = (m·h₁)²  ✓
- b²+c² = q²(m²+n²) = (q·h₂)²  ✓
- c²+d² = n²(p²+q²) = (n·h₁)²  ✓
- d²+a² = p²(m²+n²) = (p·h₂)²  ✓

This family is characterised by **ac = bd** (both equal pqmn).

## Proof it can never satisfy the unit-square constraint

```
a + c - (b + d) = pm + qn - qm - pn = (p-q)(m-n)
```

For any Pythagorean pair: p≠q (otherwise p²+q²=2p², not a perfect square).
Therefore (p-q)(m-n) ≠ 0, so **a+c ≠ b+d always** for this family.

## Two families of Pythagorean 4-cycles

| Family | Condition | Can satisfy a+c=b+d | Example |
|--------|-----------|---------------------|---------|
| Cross-product | ac = bd | **No (proven)** | (15,20,48,36) |
| General | ac ≠ bd | Unknown | (25,60,91,312) |

The general family (ac≠bd) is the only one relevant to the Harborth conjecture.
It typically involves 3–4 distinct primitive Pythagorean triples per cycle.

## Smallest general-family solution

```
(25, 60, 91, 312)   rect=116×372
  25² +  60² =  65²   (5,12,13)×5
  60² +  91² = 109²   (60,91,109) primitive
  91² + 312² = 325²   (7,24,25)×13
 312² +  25² = 313²   (312,25,313) primitive
```

Uses 4 distinct primitive triples. a+c=116, b+d=372 ≠ equal.

## Changes

| File | Change |
|------|--------|
| `src/rational_distance/search_chain.py` | Add `ac == bd` guard + updated docstring |
| `tests/test_all.py` | Updated chain tests for new filtering (65 tests, all pass) |

## Results

With `max_val=500`: 10 general-family solutions found, 0 satisfy unit-square
constraint — consistent with Harborth conjecture.
