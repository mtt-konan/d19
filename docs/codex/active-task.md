# Active Task

- Status: checkpoint_complete
- Updated: 2026-07-13
- Task id: shared-p5-factor-twist-local-image
- Goal: Determine whether the two frozen D0 factor-cover collections have a common nontrivial `Q_5` local twist restriction, or prove that the shared-`p=5` mechanism is empty or family-specific.
- Scope: only the `p=5` local images of the 16 real/`Q_2` survivors in `wl587` and `wl589`; both source/factor models are read-only, and every normalized pole, boundary, factor-zero, positivity, and exact-lift condition must remain explicit.
- Object layer: local images of the relative constant factor-twist covers; not a Picard-square-root identification, equivalent model, fixed-cover rank computation, D2 theorem, or theorem-level Selmer object.
- Current proof obligation: Compute the exact sets `I_{5,u}` and `I_{5,m}` of `Q_5` squareclasses represented by locally soluble normalized factor covers, map them back to the named D0 representatives, and decide whether they impose one shared nontrivial restriction.
- Accepted outcomes: exact nonempty local-image sets for both families with a stated shared restriction; exact deletion of named D0 representatives; or a precise shared-`p=5` route-death certificate proving that this place supplies no common nontrivial restriction.
- Allowed changes: one short-path `wl590` script/test and worklog only after an accepted exact local-image or route-death outcome; control-document synchronization. All mathematical construction is delegated through Codex CLI.
- Forbidden changes: no edits to `wl587` or `wl589`; no primes other than `5`; no broader D1/D2; no `wl535` re-entry, pure-`v_ell` refinement, equivalent model/quotient, shell 11, finite search as progress, new support computation, rank/Selmer diagnostics, old package-`x` / `S~`, M3, or commit before controller review.
- Stable boundaries: `wl529`, `wl530`, `wl531`, `wl532`, `wl533`, `wl534`, and `wl535` are inputs. Preserve the validated q-root equivalence, chart-inverse branches, and all earlier exact lifts unless a concrete error is found.
- Current step: completed by `wl590`; no further prime or local row is entered here.
- Result: `I_{5,u}=empty set`; `I_{5,m}={[5]}`. The place is family-specific,
  not a shared surviving restriction; this is route death for the shared-p5
  mechanism and a fixed-cover local exclusion for the pure representative.
- Evidence: `docs/work-logs/590-p5-factor-twist-local-image-comparison.md`,
  `scripts/theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py`, and
  its focused test.
- Completed steps: `wl530` derives M1; `wl531`-`wl535` give the exact q-root proposition; `wl536`-`wl580` exhaust local, descent, valuation, allocation, and reconstruction routes; `wl581`-`wl585` exhaust lower-genus and elliptic-quotient reformulations; the consolidated checkpoint verifies the chain and its claim boundaries.
- Strategic route-freeze certificate: `wl539` closes repeated good-reduction residue tables; `wl541` closes the parameter-prime standalone route; `wl542` closes negative-denominator places as automatic local squares; `wl568` and `wl580` prove allocation/descent self-consistency reconstructs the source system; `wl582`, `wl584`, and `wl585` prove the available elliptic quotients either forget a required lift or recover the original restricted problem. These finite, named tool classes cannot supply a new uniform invariant without an additional arithmetic input not present in them.
- Certificate boundary: This freezes only the currently instantiated candidate tools. It is not a theorem that every future Hilbert-symbol, Brauer-Manin, reciprocity, family-Chabauty, or other global invariant is impossible.
- Next exact step: current task only; no other local row or later stage is entered here.
- Validation gates: exact `Q_5` local-solubility proof rather than bounded search; both directions between normalized local points and reported squareclasses; all exceptional branches; mapping to all 16 named representatives in each family; focused pytest; targeted ruff; strict certificate.
- Stop condition: met. The exact images are `I_{5,u}=empty set` and `I_{5,m}={[5]}`; all pure representatives and 12 mixed representatives are deleted, while `5,3045,66045,91205` survive. Do not process another prime.
- Delegation preference: all future Codex CLI subagent tasks use `--model gpt-5.6-luna --reasoning max`; `max` is the reasoning level, not part of the model name. `--reasoning xhigh` is also verified as supported. Do not alter tasks already running when this preference was set.
