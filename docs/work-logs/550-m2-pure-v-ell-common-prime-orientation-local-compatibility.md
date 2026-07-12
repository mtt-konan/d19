# M2 Pure v_ell Common-Prime Orientation Local Compatibility

## Question

Does coupling the `wl549` square-root condition to either fixed `wl546`
Gaussian orientation produce a new obstruction at the same common odd prime?

## Quadratic Etale Setup

Let `p` be an odd divisor of `ell-1` from the `wl549` support. Work in

```text
K_p=F_p[i],  i^2=-1,
```

which is either a field or the split quadratic algebra. Conjugation sends
`i` to `-i`. The fixed Gaussian factor

```text
pi_0=a_0+i*b_0
```

has norm `ell ≡ 1 (mod p)`, hence is a unit of norm one in `K_p`.

For `z=x+i*y` with nonzero norm,

```text
z^2/Norm(z)=z/conjugate(z).
```

Every norm-one unit `h` has this form. Indeed, if `h != -1`, take `z=1+h`;
then `conjugate(z)=z/h`. If `h=-1`, take `z=i`. These choices are units in
both the field and split cases.

## First Orientation

Suppose `q in F_p` and `A^2+q^2=1`. Put

```text
w=A+i*q,
h=w/pi_0.
```

Then `Norm(h)=1`, so choose `z=x+i*y` as above. Taking imaginary parts of

```text
pi_0*z^2/Norm(z)=w
```

gives

```text
q = [b_0*(x^2-y^2)+2*a_0*x*y]/(x^2+y^2).
```

This is exactly the first `wl546` orientation modulo `p`.

## Second Orientation

Instead put `w=q+i*A`. The same argument, now taking real parts, gives

```text
q = [a_0*(x^2-y^2)-2*b_0*x*y]/(x^2+y^2),
```

which is the second `wl546` orientation. Thus each orientation separately
realizes every `q` for which `1-q^2` is a square.

## Apply wl549

At a `wl549` common-prime root, `t=q^2` is square and

```text
1-t=t^2/4.
```

Choosing either square root `q` of `t` and `A=+/-t/2` supplies
`A^2+q^2=1`. Therefore both fixed Gaussian orientations are locally
compatible with every surviving root-square class.

## Exact Failure Point

The common prime cannot eliminate an odd class by coupling its root condition
to a single `wl546` orientation: the orientation equation is automatically
soluble there. A strict next step must use global compatibility among the
integer orientation equation and the Gaussian class equation, couple distinct
places, or use the real positivity inequality. Same-prime orientation tables
are exhausted.

## Boundary

This is local compatibility, not a global integer solution and not evidence
that a squareclass occurs globally. It does not solve the odd class equation,
use positivity, handle the nontrivial real-unit class, prove `wl535`, or enter
M3.
