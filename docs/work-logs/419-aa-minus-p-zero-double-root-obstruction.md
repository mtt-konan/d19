# AA Minus-P Zero-Double-Root Obstruction

## Question

Can the remaining `formal_lift_compatibility` case for
`rank-zero-selmer-AA-kernel-minus-p`,

```text
ell | T^2 + 4*L^2
```

be closed by either of the naive tracked parameters `x` or `x + 64*L^2`?

## Result

No. The package transcript now records explicit `Q_5` local points showing
that both naive promotions are false.

For `ell=5`, `L=T=1`, the package model is

```text
y^2 = x^3 + 24*x^2 + 400*x.
```

The point with `x=2` exists locally because the right-hand side is `904`,
with `v_5(904)=0` and residue `4 mod 5`. But `2` is not a square modulo `5`.
So the original descent coordinate `x` is not always trivial.

The earlier `x=-9949` example remains: the right-hand side has square
valuation and square unit residue, while `x + 64*L^2` has odd `5`-adic
valuation. So the normalized tangent-one coordinate

```text
1 - X = (x + 64*L^2)/(64*L^2)
```

is not always trivial either.

## Sage Check

```bash
sage -c 'L=T=1; d=T*T+4*L*L; a2=32*L*L-8*T*T; a4=16*d*d
for x in [2,-9949]:
    rhs=x**3+a2*x*x+a4*x
    n=rhs; v=0
    while n % 5 == 0:
        v += 1; n //= 5
    q=x+64*L*L; m=q; w=0
    while m % 5 == 0 and m != 0:
        w += 1; m //= 5
    print(f"x={x} rhs={rhs} v5_rhs={v} rhs_unit_mod5={n%5} x_mod5={x%5} x_plus_64={q} v5_x_plus_64={w} x_plus_64_unit_mod5={m%5}")'
```

Output:

```text
x=2 rhs=904 v5_rhs=0 rhs_unit_mod5=4 x_mod5=2 x_plus_64=66 v5_x_plus_64=0 x_plus_64_unit_mod5=1
x=-9949 rhs=-982406294525 v5_rhs=2 rhs_unit_mod5=4 x_mod5=1 x_plus_64=-9885 v5_x_plus_64=1 x_plus_64_unit_mod5=3
```

## Boundary

This is not a local-image theorem and does not prove the package. It narrows
the remaining formal-lift problem: the zero-double-root case needs a corrected
local image statement, likely with component or valuation data, before it can
feed a Selmer bound.
