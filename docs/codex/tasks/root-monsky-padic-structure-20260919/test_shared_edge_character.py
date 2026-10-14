"""Focused checks for the proved content character and its exact scope."""

from itertools import combinations, product
from math import gcd, isqrt

import sympy as sp


def chi2(value):
    assert value % 2
    return 1 if value % 8 in (1, 7) else -1


def character(u, v):
    assert v % 4 == 0
    return chi2(u) * (1 if (v // 4) % 2 == 0 else -1)


def corners(x, y, n):
    return [(x - a * n, y - b * n) for a, b in ((0, 0), (1, 0), (0, 1), (1, 1))]


def test_primitive_q2_branch_has_exact_mod8_description():
    squares = {0, 1, 4}
    for x, y, n in product(range(8), repeat=3):
        if x % 2 == y % 2 == n % 2 == 0:
            continue
        passes = all((u * u + v * v) % 8 in squares for u, v in corners(x, y, n))
        expected = n % 4 == 0 and (
            (x % 2 == 1 and y % 4 == 0) or (y % 2 == 1 and x % 4 == 0)
        )
        assert passes == expected


def test_corner_contents_preserve_primitive_gcd_conditions():
    for x, y, n in ((3, 4, 24), (21, 28, 12), (-21, 28, 20), (7, 0, 24)):
        assert gcd(gcd(x, y), n) == 1
        contents = [gcd(u, v) for u, v in corners(x, y, n)]
        assert all(gcd(g, n) == 1 for g in contents)
        assert all(gcd(g, h) == 1 for g, h in combinations(contents, 2))


def test_opposite_corner_identity_is_independent_of_signs():
    u, v, n = sp.symbols("u v n")
    for sign_u, sign_v in product((-1, 1), repeat=2):
        expression = (u + sign_u * n) ** 2 + (v + sign_v * n) ** 2
        expected = u**2 + v**2 + 2 * n * (sign_u * u + sign_v * v) + 2 * n**2
        assert sp.expand(expression - expected) == 0


def test_content_character_handles_signs_contents_and_zero_leg():
    for m, n in product(range(1, 16, 2), range(-14, 15, 2)):
        if gcd(m, n) != 1:
            continue
        for content, sign_u in product((1, 3, 5, 7, 15, 17, 49, 119), (-1, 1)):
            u = sign_u * content * (m * m - n * n)
            v = content * 2 * m * n
            r = content * (m * m + n * n)
            assert u * u + v * v == r * r
            assert gcd(u, v) == content
            assert character(u, v) == chi2(content)


def test_character_transport_exhausts_its_finite_residue_domain():
    for x, y, n in product((1, 3, 5, 7), (0, 4), (4, 8)):
        labels = [character(u, v) for u, v in corners(x, y, n)]
        c = labels[0]
        assert labels == ([c, -c, -c, c] if n == 4 else [c, c, c, c])


def test_scope_witnesses_separate_q2_solubility_and_rational_lifts():
    q2_only = [u * u + v * v for u, v in corners(1, 4, 12)]
    assert q2_only == [17, 137, 65, 185]
    assert all(value % 8 == 1 for value in q2_only)
    assert 12 % 8 != 0

    surviving = corners(3, 4, 24)
    assert [gcd(u, v) for u, v in surviving] == [1, 1, 1, 1]
    assert [character(u, v) for u, v in surviving] == [1, 1, 1, 1]
    norms = [u * u + v * v for u, v in surviving]
    assert norms == [25, 457, 409, 841]
    assert [isqrt(value) ** 2 == value for value in norms] == [True, False, False, True]


def test_common_similarity_does_not_change_normalized_point():
    z, w, q = sp.symbols("z w q", nonzero=True)
    assert sp.cancel((z / q) / (w / q) - z / w) == 0
