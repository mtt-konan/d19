"""Exact checks for the primitive 2-adic parity lemma."""

from itertools import product


def equations_mod(m, w, e, f, a, b, c, d):
    return (
        (w * w + e * e + f * f) % m,
        ((w + e) ** 2 + f * f - 2 * a * a) % m,
        ((w - e) ** 2 + f * f - 2 * b * b) % m,
        ((w + f) ** 2 + e * e - 2 * c * c) % m,
        ((w - f) ** 2 + e * e - 2 * d * d) % m,
    )


def test_mod_two_and_mod_four_leave_only_w_even_pattern():
    allowed = []
    for w, e, f, a, b, c, d in product(range(4), repeat=7):
        if all(x % 2 == 0 for x in (w, e, f, a, b, c, d)):
            continue
        if equations_mod(4, w, e, f, a, b, c, d)[1:] != (0, 0, 0, 0):
            continue
        if (w * w + e * e + f * f - a * a - b * b) % 4:
            continue
        if (w * w + e * e + f * f - c * c - d * d) % 4:
            continue
        parity = tuple(x % 2 for x in (w, e, f, a, b, c, d))
        if parity not in allowed:
            allowed.append(parity)
    assert allowed == [(0, 1, 1, 1, 1, 1, 1)]


def test_odd_square_difference_forces_four_dividing_w():
    for w, e, f, a, b, c, d in product(range(16), repeat=7):
        if w % 4 in (0, 2) and e % 2 == f % 2 == 1 and a % 2 == b % 2 == c % 2 == d % 2 == 1:
            if (a * a - b * b - 2 * w * e) % 16:
                continue
            if (c * c - d * d - 2 * w * f) % 16:
                continue
            assert w % 4 == 0
