# cython: boundscheck=False, wraparound=False, cdivision=True, language_level=3
"""Cython kernel for the pivot-on-N concordant (A, N) generator.

Mirrors `rational_distance.concordant.fast_multi_n.iter_concordant_a_n` but does
the smallest-prime-factor sieve, the per-A divisor enumeration of A**2, and the
(A, N) emission entirely in C, writing straight into numpy arrays — eliminating
~130M Python-level generator yields / tuple allocations at max_hyp=5e6.

Identity:  A^2 + N^2 = h^2  <=>  (h-N)(h+N) = A^2, so each concordant (A, N)
is a divisor pair (p, q=A^2/p), p<q, p≡q (mod 2), with N=(q-p)/2.
"""

import numpy as np

cimport numpy as cnp
from libc.stdlib cimport free, malloc, qsort

cnp.import_array()


cdef int _cmp_ll(const void* x, const void* y) noexcept nogil:
    cdef long long a = (<long long*> x)[0]
    cdef long long b = (<long long*> y)[0]
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


cdef inline long long _gcd(long long x, long long y) noexcept nogil:
    cdef long long t
    while y != 0:
        t = x % y
        x = y
        y = t
    return x


def generate(long long max_leg):
    """Return (n_arr int64, a_arr int32) of every (A, N), 2<=A<=max_leg, N>=1.

    Two passes (count, then fill the numpy arrays directly) so peak memory is
    just the output arrays — no over-allocated C scratch / memcpy doubling.
    """
    cdef long long limit = max_leg
    if limit < 2:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int32)

    cdef int* spf = NULL
    cdef long long* primes = NULL
    cdef int* exps = NULL
    cdef long long* divs = NULL
    cdef long long i, j
    cdef int MAXP = 40            # >= number of distinct prime factors of any A<=5e6
    cdef long long dcap = 1 << 16
    cdef long long a, m, a_sq, q, n, d, pk, base, p
    cdef long long cnt = 0
    cdef int nprime, e, t, idx, cur, ndiv, ei
    cdef int pass_id
    cdef long long* np_n = NULL
    cdef int* np_a = NULL
    cdef cnp.ndarray narr = np.empty(0, dtype=np.int64)
    cdef cnp.ndarray aarr = np.empty(0, dtype=np.int32)

    # try/finally so the malloc'd C buffers are freed on every exit path
    # (incl. a MemoryError from np.empty below); free(NULL) is a safe no-op.
    try:
        # --- smallest-prime-factor sieve (spf[i] = least prime dividing i) ---
        spf = <int*> malloc((limit + 1) * sizeof(int))
        if spf == NULL:
            raise MemoryError()
        for i in range(limit + 1):
            spf[i] = 0
        for i in range(2, limit + 1):
            if spf[i] == 0:
                j = i
                while j <= limit:
                    if spf[j] == 0:
                        spf[j] = <int> i
                    j += i

        # per-A scratch: prime powers of A, and the divisor list of A^2
        primes = <long long*> malloc(MAXP * sizeof(long long))
        exps = <int*> malloc(MAXP * sizeof(int))
        divs = <long long*> malloc(dcap * sizeof(long long))
        if primes == NULL or exps == NULL or divs == NULL:
            raise MemoryError()

        for pass_id in range(2):
            if pass_id == 1:
                narr = np.empty(cnt, dtype=np.int64)
                aarr = np.empty(cnt, dtype=np.int32)
                np_n = <long long*> cnp.PyArray_DATA(narr)
                np_a = <int*> cnp.PyArray_DATA(aarr)
                cnt = 0
            for a in range(2, limit + 1):
                # factor a via spf
                m = a
                nprime = 0
                while m > 1:
                    p = spf[m]
                    e = 0
                    while m % p == 0:
                        m //= p
                        e += 1
                    primes[nprime] = p
                    exps[nprime] = e
                    nprime += 1

                # build all divisors of a^2 (each prime exponent doubled)
                divs[0] = 1
                ndiv = 1
                for idx in range(nprime):
                    base = primes[idx]
                    ei = 2 * exps[idx]
                    cur = ndiv
                    pk = 1
                    for t in range(ei):
                        pk *= base
                        for j in range(cur):
                            divs[ndiv] = divs[j] * pk
                            ndiv += 1

                a_sq = a * a
                # each divisor p < a gives q = a^2/p > a; emit N if parity matches
                for idx in range(ndiv):
                    d = divs[idx]
                    if d >= a:
                        continue
                    q = a_sq // d
                    if ((d + q) & 1) != 0:
                        continue
                    if pass_id == 1:
                        np_n[cnt] = (q - d) >> 1
                        np_a[cnt] = <int> a
                    cnt += 1

        return narr, aarr
    finally:
        free(spf)
        free(primes)
        free(exps)
        free(divs)


def emit_pairs(cnp.ndarray[cnp.int64_t, ndim=1] n_sorted,
               cnp.ndarray[cnp.int32_t, ndim=1] a_sorted,
               cnp.ndarray[cnp.int64_t, ndim=1] ms,
               cnp.ndarray[cnp.int64_t, ndim=1] me,
               long long factor,
               long long maxbucket,
               int shard=0, int nshards=1):
    """For every multi-bucket [ms[k], me[k]) of N-sorted relations, emit each
    coprime, not-both-even A-pair (ai<aj) as (pkey=ai*factor+aj, N).

    Relations are sorted by N only, so each bucket's A-values are re-sorted in C.
    With nshards>1, only pairs whose smaller leg ai % nshards == shard are emitted
    (lets callers shard the buffer / parallelise by residue). Two passes (count,
    then fill) keep peak memory at just the output arrays.
    """
    cdef long long nb = ms.shape[0]
    cdef long long bi, s, e, i, j, cnt = 0
    cdef long long ai, aj, nval, m
    cdef int pass_id
    cdef long long* buf = NULL
    cdef long long* opk = NULL
    cdef long long* onn = NULL
    cdef cnp.ndarray pkeys = np.empty(0, dtype=np.int64)
    cdef cnp.ndarray nns = np.empty(0, dtype=np.int64)

    # try/finally so buf is freed even if np.empty below raises MemoryError
    try:
        buf = <long long*> malloc((maxbucket if maxbucket > 0 else 1) * sizeof(long long))
        if buf == NULL:
            raise MemoryError()

        for pass_id in range(2):
            if pass_id == 1:
                pkeys = np.empty(cnt, dtype=np.int64)
                nns = np.empty(cnt, dtype=np.int64)
                opk = <long long*> cnp.PyArray_DATA(pkeys)
                onn = <long long*> cnp.PyArray_DATA(nns)
                cnt = 0
            for bi in range(nb):
                s = ms[bi]
                e = me[bi]
                m = e - s
                nval = n_sorted[s]
                for i in range(m):
                    buf[i] = a_sorted[s + i]
                qsort(buf, m, sizeof(long long), &_cmp_ll)
                for i in range(m):
                    ai = buf[i]
                    if nshards > 1 and (ai % nshards) != shard:
                        continue
                    for j in range(i + 1, m):
                        aj = buf[j]
                        if (ai & 1) == 0 and (aj & 1) == 0:
                            continue
                        if _gcd(ai, aj) != 1:
                            continue
                        if pass_id == 1:
                            opk[cnt] = ai * factor + aj
                            onn[cnt] = nval
                        cnt += 1
        return pkeys, nns
    finally:
        free(buf)
