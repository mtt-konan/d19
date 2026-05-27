# Proof Status Kernel Optimizations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce proof-status and AB sieve benchmarking runtime by removing unnecessary modulus work, reusing concordant-N computations, replacing divisor scanning with factor-based enumeration, and making pair generation stream-friendly for larger order benchmarks.

**Architecture:** Keep public behavior stable while tightening the hot path in four places: early-stop the chain-closure sieve once one killer modulus is found, propagate a per-pair concordant-N cache through proof_status compute paths, replace `diff` trial scanning in `factor_search.py` with divisor generation from the factorization of `B-A` and `B+A`, and expose iterator-based pair generation so benchmarking code can avoid unnecessary list materialization. All changes stay in Python and preserve current CLI outputs except for optional new metadata used by tests.

**Tech Stack:** Python, pytest, sqlite3, existing `rational_distance` workflow/benchmark modules

---

### Task 1: Add regression tests for hot-path behavior

**Files:**
- Modify: `tests/test_proof_status.py`
- Modify: `tests/test_concordant.py`
- Modify: `tests/test_ab_sieve_benchmark.py`

- [ ] **Step 1: Add failing tests for chain-closure early stop and proof_status concordant cache**
- [ ] **Step 2: Add failing tests for factor-search correctness under the new divisor-generation path**
- [ ] **Step 3: Add failing tests for iterator-based pair generation and benchmark limiting without full materialization assumptions**
- [ ] **Step 4: Run focused pytest selection and verify failures are for the expected missing behavior**

### Task 2: Implement proof_status hot-path reductions

**Files:**
- Modify: `src/rational_distance/proof_status/methods.py`
- Modify: `src/rational_distance/proof_status/workflow.py`
- Modify: `src/rational_distance/proof_status/ab_sieve_methods.py`
- Modify: `src/rational_distance/concordant/chain_closure_sieve.py`

- [ ] **Step 1: Change chain-closure method to stop at first killer modulus while keeping current details schema meaningful**
- [ ] **Step 2: Introduce a per-pair proof_status evaluation context that shares concordant-N results across methods in both serial and parallel compute paths**
- [ ] **Step 3: Re-run focused pytest selection and verify new tests pass**

### Task 3: Replace factor-search divisor scan with factor-based enumeration

**Files:**
- Modify: `src/rational_distance/concordant/factor_search.py`
- Test: `tests/test_concordant.py`

- [ ] **Step 1: Implement factorization helpers and divisor generation from `B-A` and `B+A`**
- [ ] **Step 2: Preserve output ordering/dedup semantics and existing API**
- [ ] **Step 3: Re-run focused factor-search tests and verify parity with old mathematical behavior**

### Task 4: Add stream-friendly pair generation and wire benchmark entry points

**Files:**
- Modify: `src/rational_distance/concordant/pairs.py`
- Modify: `scripts/benchmark_ab_sieve_orders.py`
- Test: `tests/test_ab_sieve_benchmark.py`
- Test: `tests/test_concordant.py`

- [ ] **Step 1: Add iterator/list split to pair generation without breaking legacy callers**
- [ ] **Step 2: Update benchmark CLI to consume only the needed prefix when `--limit` is set and keep existing JSON fields stable**
- [ ] **Step 3: Run focused benchmark/pair tests and then a combined pytest pass for all touched areas**
