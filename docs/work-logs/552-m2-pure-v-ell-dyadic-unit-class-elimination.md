# M2 Pure v_ell Dyadic Unit-Class Elimination

## Question

After `wl551` reduces the odd squarefree factor to a rational odd integer
`r`, which Gaussian unit class can occur in

```text
delta=eta*r*gamma^2,
eta in {1,i} modulo unit squares?
```

## The ell = 5 mod 8 Branch

Put `L=ell-1` and

```text
E=4*L*Q^2*D^2,
F=R-E,
delta=E+i*F.
```

Here `wl545` gives `Q,D` odd and `v_2(L)=2`. Hence `v_2(E)=4`, while
`R` is odd, so `F` is odd. Since `wl548` gives
`v_(1+i)(delta)=0`, the factor `gamma=m+i*n` is also a `1+i`-unit; therefore
`m,n` have opposite parity. Consequently

```text
gamma^2=(m^2-n^2)+2*i*m*n
```

has odd real part and even imaginary part. Multiplication by the odd rational
`r` preserves this parity pattern. But `delta` has even real part and odd
imaginary part. Thus `eta=1` is impossible and

```text
eta=i modulo Gaussian unit squares.
```

## The ell = 1 mod 8 Branch

Now `v_2(L)>=3`, `v_2(Q)>=3`, and `D` is odd, so `v_2(E)>=11`.
The `wl548` congruence says `R/4` is odd, hence `F/4` is odd. Also

```text
v_(1+i)(delta)=4.
```

Write

```text
gamma=(1+i)^2*gamma_0.
```

Then `gamma_0` is a `1+i`-unit and

```text
gamma^2=-4*gamma_0^2.
```

After dividing the class equation by `-4`, the normalized left side has even
real part and odd imaginary part, while `r*gamma_0^2` has odd real part and
even imaginary part. The same parity comparison again forces

```text
eta=i modulo Gaussian unit squares.
```

## Reduced Coordinate Equations

The two unit classes from `wl551` collapse uniformly to one. In the
`ell ≡ 5 (mod 8)` branch, writing `gamma=m+i*n` gives exactly

```text
E=-2*r*m*n,
F= r*(m^2-n^2).
```

In the `ell ≡ 1 (mod 8)` branch, writing
`gamma=(1+i)^2*(m+i*n)` and dividing by `-4` gives the analogous normalized
pair

```text
-E/4=-2*r*m*n,
-F/4= r*(m^2-n^2).
```

Signs may be absorbed by replacing `m` or `n`; the unit class itself is fixed.

## Strict Reduction And Next Gate

There is no remaining Gaussian unit choice on the trivial real-unit branch.
The next exact gate is the single `eta=i` coordinate system for rational
squarefree `r`, coupled to one `wl546` orientation or positivity.

## Boundary

This does not solve the coordinate equations, choose `r`, use positivity,
handle the nontrivial real-unit class, prove the full `wl535` proposition, or
enter M3.
