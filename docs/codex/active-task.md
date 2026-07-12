# Active Task

- Status: active
- Updated: 2026-07-12
- Task id: m2-wl535-q-root-square-quartic-resolution
- Goal: Resolve the exact `wl535` q-root-coordinate square/quartic proposition by a uniform proof, a strict counterexample, or one genuinely smaller exact arithmetic obstruction.
- Scope: Odd primes `ell ≡ 1 (mod 4)`; only `support=v_ell|L=1|T=ell|d=(ell,1,ell)`; only rational `(q,V)` satisfying the four exact `wl535` conditions.
- Object layer: rational points on the exact `wl535` q-root square/quartic system; not finite search, not a general elliptic quotient diagnostic, and not theorem-level Selmer.
- Current proof obligation: For every odd prime `ell ≡ 1 (mod 4)`, prove no rational pair `(q,V)` has `ell-q^2` square, `ell*q^2+4` square, `ell*q^4+4*q^2-4*ell>0`, and `V^2=G_ell(q^2)`, or exhibit a strict rational counterexample, or reduce it to one genuinely smaller exact arithmetic lemma.
- Accepted outcomes: rigorous proof; rigorous counterexample; or precise failure point with one exact missing lemma and proof that all earlier reductions are complete.
- Allowed changes: one worklog only if a real theorem/counterexample/exact new failure point results; matching audit script/test if a computation is part of the certificate; route handoff synchronization.
- Forbidden changes: no shell 11, no finite search presented as mathematical progress, no new support family, no broad rank/Selmer diagnostics, no old package-`x` / `S~`, no M3, and no commit.
- Stable boundaries: `wl529`, `wl530`, `wl531`, `wl532`, `wl533`, `wl534`, and `wl535` are inputs. Preserve the validated q-root equivalence, chart-inverse branches, and all earlier exact lifts unless a concrete error is found.
- Current step: The `wl530-wl585` consolidated checkpoint independently rechecks the key identities and exceptions and marks the elliptic-quotient subroute exhausted. The exact `wl535` proposition remains open.
- Completed steps: `wl530` derives M1; `wl531`-`wl535` give the exact q-root proposition; `wl536`-`wl580` exhaust local, descent, valuation, allocation, and reconstruction routes; `wl581`-`wl585` exhaust lower-genus and elliptic-quotient reformulations; the consolidated checkpoint verifies the chain and its claim boundaries.
- Next exact step: Do not create `wl586` for another equivalent model or quotient. Accept only: a direct proof of `wl535`; a strict counterexample; or a genuinely smaller arithmetic proposition with an explicit proof of which parameter, freedom, or square lift has been removed. M2 and M3 remain closed to advancement until one of these occurs.
- Validation gates: direct algebra review; explicit positivity, square-X, lift, and all exceptional-denominator handling; focused pytest; targeted ruff; strict certificate if any.
- Stop condition: A rigorous resolution or one strictly smaller exact lemma is recorded and independently checked; do not enter M3.
- Delegation preference: all future subagent tasks use `gpt 5.6 luna max`; do not alter tasks already running when this preference was set.
