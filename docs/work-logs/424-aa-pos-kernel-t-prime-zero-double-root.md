# AA Pos Kernel T-Prime Zero-Double-Root

## Question

For `rank-zero-selmer-AA-kernel-pos-2sqrt-q`, what is the correct odd-prime
formal-lift image at

```text
ell | T?
```

## Result

It is not uniformly `{1}`. The zero-double-root branch splits according to
whether `-1` is a local square:

```text
if -1 is not a square:  local image = the two unit classes
if -1 is a square:      local image = all four squareclasses
```

普通话说：这个分支不是完全管住，也不是完全放开；它取决于这个局部域里 `-1`
是不是平方。

## Proof Shape

For the model

```text
y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
```

write

```text
e  = v(T) >= 1
s  = 64*L^2
a2 = -s - 8*T^2
a4 = 16*T^4
Q(x) = x^2 + a2*x + a4.
```

The unit squareclass of `a2` is the squareclass of `-1`.

The valuation split is:

- `v(x) < 0`: `Q(x)` is `x^2` times a square, so a local point forces `x`
  to be square;
- `v(x) = 0`: `x` is a unit class;
- `0 < v(x) < 4v(T)`: `Q(x)` is `a2*x` times a square, so this range exists
  only when `-1` is square;
- `v(x) = 4v(T)`: `x` has even valuation, hence unit class;
- `v(x) > 4v(T)`: `Q(x)` is `a4` times a square, so a local point forces
  `x` to be square.

This gives the upper bound. The allowed classes occur by taking `x` with
large negative even valuation for the trivial class, using a finite-field
residue with `x0` nonsquare and `x0-s` square for the nonsquare unit class,
and, when `-1` is square, taking `x=pi*u` for the two ramified classes.

## Boundary

This closes the odd-prime formal-lift cases for this package, but it does
not prove the dyadic condition, the global Selmer bound, rank zero, or any
lambda-family exclusion.
