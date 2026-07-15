# Berry Sextic Post-B0 Feasibility Audit

## Verdict

The accepted B0 checkpoint `dccbd9a` is preserved. A complete dyadic
stable-model classification is **not** a prerequisite for B1/B2.

The `i`-twist is locally insoluble at `K_(1+i)`, so it is excluded before any
global Selmer computation. Both Jacobians have rigorous trivial torsion from
good-prime specialization. The installed Sage toolchain can reproduce exact
finite-field Jacobian orders and the base-field S-squareclass container, but it
does not expose an exact genus-2 Jacobian 2-Selmer or local Kummer-image route.
No arithmetic blocker is promoted: no concrete 2-Selmer computation was set up.

## 1. Dyadic Local Obstruction

Let `pi=1+i` in `K_(1+i)=Q_2(i)`. Then

```text
pi^2=2*i,        2=-i*pi^2.
```

For `C_i`, write

```text
v^2=f(t),        f(t)=(-i)*g6(t).
```

Every unit square is `1 mod pi^2`: a unit is `1+pi*a`, and
`(1+pi*a)^2=1+2*pi*a+pi^2*a^2`. Also `i` and `-i` are both `1+pi mod pi^2`.

### Finite chart

Put `z=t+1`. For the exact Taylor expansion `f(z-1)=sum c_j z^j`, the
coefficient valuations and their unit residues are

```text
j                         0  1  2  3  4  5  6
v_pi(c_j)                11 10  8  9  3  2  0
(c_j/pi^v) mod pi         1  1  1  1  1  1  1
```

The exact valuation partition is

| condition | `v_pi(f(t))` | reason |
|---|---:|---|
| `v_pi(z)=0` | `0` | `f(t)=1+pi mod pi^2` |
| `v_pi(z)=1` | `6` | unique lowest term is `c_6 z^6`; the two valuation-7 terms cancel after normalization |
| `v_pi(z)=2` | `13` | exact four-residue calculation below |
| `v_pi(z)>=3` | `11` | unique lowest term is `c_0` |

For the only cancellation branch, set `z=pi^2*u` with `u` a unit. Exact
division gives

```text
Q(u)=pi^(-11)*f(-1+pi^2*u)
    = i+(3+i)u+(1+i)u^2+(8+4*i)u^3
      +(2-3*i)u^4+(3+5*i)u^5+(1-i)u^6.
```

The four unit classes modulo `pi^3` give:

| `u mod pi^3` | `v_pi(Q(u))` | `Q(u)/pi^2 mod pi` |
|---|---:|---:|
| `1` | `2` | `1` |
| `1+pi` | `2` | `1` |
| `1+pi^2` | `2` | `1` |
| `1+pi+pi^2` | `2` | `1` |

Thus the even-valuation branches have normalized unit `1+pi mod pi^2`,
which is not a square, and the other branches have odd valuation. This also
proves `f(t)` is never zero in the finite chart, so factor-zero/branch fibers
are not silently omitted.

### Infinity and nonintegral finite points

For `v_pi(t)<0`, use `x=1/t` and `w=v/t^3`; then `v_pi(x)>=1` and

```text
w^2=(-i)*g6_star(x),
g6_star(x)=1+(-2-2*i)x+(-35-8*i)x^2+(-52-28*i)x^3
           +(19-40*i)x^4+(6+14*i)x^5-x^6.
```

Direct reduction gives `(-i)*g6_star(x)=1+pi mod pi^2` and valuation zero for
every `x in pi*O`. The same statement at `x=0` is the explicit infinity
chart, where `w^2=-i`. Hence no point is present at infinity either.

Therefore

```text
C_i(K_(1+i)) = empty set.
```

The exact Sage proof-data is
`scripts/theory/berry_sextic_post_b0.sage`.

## 2. Rigorous Jacobian Torsion

At every listed good prime, Sage computed `N1=#C(F_q)`, `N2=#C(F_{q^2})`,
and `#J(F_q)` exactly with `proof.all(True)`. The characteristic polynomial
calculation used is

```text
a1=q+1-N1,
a2=(N2-q^2-1+a1^2)/2,
#J(F_q)=q^2+1+a2-(q+1)*a1.
```

| rational `p` | residue `q` | `(N1,N2)` for `C_1` | `#J_1(F_q)` | `(N1,N2)` for `C_i` | `#J_i(F_q)` |
|---:|---:|---:|---:|---:|---:|
| 3 inert | 9 | `(8,106)` | `76=2^2*19` | `(8,106)` | `76=2^2*19` |
| 5 split | 5 | `(7,39)` | `39=3*13` | `(5,39)` | `27=3^3` |
| 7 inert | 49 | `(58,2448)` | `2857` | `(58,2448)` | `2857` |
| 13 split | 13 | `(10,188)` | `131` | `(18,188)` | `243=3^5` |
| 17 split | 17 | `(16,342)` | `282=2*3*47` | `(16,342)` | `282=2*3*47` |
| 29 split | 29 | `(35,895)` | `1031` | `(25,895)` | `731=17*43` |
| 37 split | 37 | `(56,1344)` | `2203` | `(20,1344)` | `835=5*167` |

All these primes are outside the exact discriminant support, hence are good
for both twists. The raw gcd of all displayed orders is `1` for each Jacobian.
The primary-safe specialization bound is also `1`: for every rational prime
`ell`, use only rows whose residue characteristic is not `ell`, because
reduction is injective on `ell`-primary torsion at those rows. This handles the
residue-characteristic primary parts correctly and gives

```text
J_1(K)_tors = 0,        J_i(K)_tors = 0.
```

## 3. Conservative Descent Support

For either selected twist,

```text
Disc(g6)       =(i-1)^75*(94*i-169),
Disc((-i)*g6)  =(-i)^10*Disc(g6).
```

The leading coefficients are `1` and `-i`, both units. Since
`2=-i*pi^2`, a finite support sufficient for the selected Jacobian/twist
2-descent is

```text
S_model = {(1+i), (94*i-169)}.
```

Outside `2*Disc(f)` and the leading coefficient, the branch algebra is etale
and the displayed hyperelliptic model is smooth. Divisor-evaluation Kummer
classes are unramified there, so their valuations are even; no other finite
place is needed in this standard unramified-outside-support setup. This proves
sufficiency, not minimality across all equivalent descent presentations.

A conservative finite set is

```text
S_cons = {(1+i), (94*i-169), (-94*i-169)}.
```

The conjugate prime is an extra for the conjugate/Berry norm pullback, not for
either individual Jacobian. The leading coefficient and twist unit contribute
no finite prime. The unique archimedean place is complex and can be listed for
bookkeeping only; it has no real sign condition. The chart-fiber primes
`2,5,43,53` are optional coordinate-separability support, not Jacobian
2-descent support.

As a live exact API check, Sage returned

```text
K.selmer_generators([ (1+i), (94*i-169) ], 2, proof=True, orders=True)
([i-1, 94*i-169, i], [2,2,2]).
```

This is only the exact `K^*/K^2` S-squareclass container, not a Jacobian
2-Selmer computation.

## 4. Live Toolchain

The local environment has `/usr/local/bin/sage`, Sage `10.9` (2026-05-04).
With `proof.all(True)`:

- finite-field `HyperellipticCurve(f).jacobian().cardinality()` works exactly;
- number-field Jacobian cardinality raises `NotImplementedError` because the
  method is implemented only over finite fields;
- `C.two_descent`, `J.two_descent`, `J(K).torsion_subgroup`,
  `J(K).selmer_group`, `C.local_points`, and `J.local_kummer_image` are absent;
- `J(K).rational_points(proof=True)` rejects the proof keyword, and no point
  search was used;
- no `magma`, `Magma`, `magma-cli`, or `magma64` executable is installed.

The Sage Magma interface source is present, but that is not an installed Magma
route.

The free University of Sydney Magma Calculator was then tested through its
public XML endpoint. On Magma V2.29-8, the fast exact probe constructs `C_1`
and its `JacHyp` over `Q(i)` and returns

```text
HAS_TWO_SELMER_GROUP true
HAS_TWO_COVER_DESCENT true
HAS_RANK_BOUNDS true
HAS_LOCAL_KUMMER_IMAGE false
```

The `TwoSelmerGroup(J::JacHyp)` signature advertises number-field support.
However, the exact call on the selected `J_1` was terminated by the public
60-second limit before returning any Selmer data. The optional
`Al := "TwoSelmerGroupData"` path fails immediately with

```text
TwoSelmerGroupData: J must have the rationals as its base field.
```

Thus the public service is a usable capability and short-check oracle, but it
does not currently provide the required exact Selmer result or a local Kummer
image. The observed failure is a service timeout, not an arithmetic blocker.
Reproducible submissions are
`scripts/theory/berry_sextic_magma_capabilities.m` and
`scripts/theory/berry_sextic_magma_two_selmer.m`, submitted by
`scripts/utility/magma_calculator.py`.

## Next Smallest Step

Run the same exact `TwoSelmerGroup(J_1)` input in a Magma environment without
the public 60-second limit, or use the sufficient support `S_model` to
implement the local Kummer images at `(1+i)` and `(94*i-169)` directly. This is
a next step, not a claimed Selmer bound or blocker.
