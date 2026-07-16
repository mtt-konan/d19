"""Verify the exact dyadic obstruction for D_inf halving."""

from __future__ import annotations

from math import comb

Gaussian = tuple[int, int]


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def _mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _power(value: Gaussian, exponent: int) -> Gaussian:
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = _mul(result, value)
        value = _mul(value, value)
        exponent //= 2
    return result


def _divide_lambda(value: Gaussian) -> Gaussian:
    real, imaginary = value
    if (real + imaginary) % 2 or (imaginary - real) % 2:
        raise AssertionError(f"not divisible by 1+i: {value}")
    return (real + imaginary) // 2, (imaginary - real) // 2


def _lambda_valuation(value: Gaussian) -> int:
    if value == (0, 0):
        return 10**9
    valuation = 0
    while (value[0] + value[1]) % 2 == 0:
        value = _divide_lambda(value)
        valuation += 1
    return valuation


# Coefficients are ascending in c. The Sage producer independently checks
# that this polynomial is in the exact elimination ideal of the six Mumford
# coefficient equations.
ELIMINATION_POLYNOMIAL: tuple[Gaussian, ...] = (
    (4745893054341, 25610622340),
    (-878727109554, 2079369073884),
    (-371183289347, -503636744112),
    (106782453448, 13561791344),
    (-9952074358, 5948878392),
    (356741044, -725661880),
    (1926370, 37085584),
    (-537592, -974672),
    (16401, 12900),
    (-210, -68),
    (1, 0),
)

LAMBDA: Gaussian = (1, 1)


def _translated_coefficients(base: Gaussian, scale: int) -> list[Gaussian]:
    coefficients: list[Gaussian] = []
    for target_degree in range(11):
        coefficient = (0, 0)
        for degree, polynomial_coefficient in enumerate(ELIMINATION_POLYNOMIAL):
            if degree < target_degree:
                continue
            term = _mul(
                polynomial_coefficient,
                _mul(
                    (comb(degree, target_degree), 0),
                    _mul(
                        _power(base, degree - target_degree),
                        _power(LAMBDA, scale * target_degree),
                    ),
                ),
            )
            coefficient = _add(coefficient, term)
        coefficients.append(coefficient)
    return coefficients


def _residual(base: Gaussian, scale: int) -> tuple[int, tuple[int, ...]]:
    coefficients = _translated_coefficients(base, scale)
    valuations = [_lambda_valuation(value) for value in coefficients]
    minimum = min(valuations)
    residual = []
    for value, valuation in zip(coefficients, valuations, strict=True):
        if valuation != minimum:
            residual.append(0)
            continue
        normalized = value
        for _ in range(minimum):
            normalized = _divide_lambda(normalized)
        residual.append((normalized[0] + normalized[1]) % 2)
    return minimum, tuple(residual)


def _assert_residual(base: Gaussian, scale: int, minimum: int, expected: tuple[int, ...]) -> None:
    actual_minimum, actual_residual = _residual(base, scale)
    assert actual_minimum == minimum
    assert actual_residual == expected


def _roots_over_f2(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        value
        for value in (0, 1)
        if sum(coefficient * value**degree for degree, coefficient in enumerate(coefficients)) % 2
        == 0
    )


def verify_certificate() -> dict[str, object]:
    assert _add((1, 0), _power(LAMBDA, 2)) == (1, 2)
    assert _add((1, 2), _power(LAMBDA, 3)) == (-1, 4)
    assert _add((-1, 4), _power(LAMBDA, 4)) == (-5, 4)
    assert _add((1, 2), _power(LAMBDA, 4)) == (-3, 2)
    assert _add((-3, 2), _power(LAMBDA, 5)) == (-7, -2)
    assert _add((-7, -2), _power(LAMBDA, 6)) == (-7, -10)

    initial = (1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1)
    first = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
    second = (1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1)
    split = (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1)
    _assert_residual((0, 0), 0, 0, initial)
    _assert_residual((1, 0), 1, 10, first)
    _assert_residual((1, 0), 2, 20, second)
    _assert_residual((1, 2), 3, 30, split)
    assert _roots_over_f2(initial) == (1,)
    assert _roots_over_f2(first) == (0,)
    assert _roots_over_f2(second) == (1,)
    assert _roots_over_f2(split) == (0, 1)

    first_branch = (1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    first_terminal = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    _assert_residual((-1, 4), 4, 34, first_branch)
    _assert_residual((-5, 4), 5, 36, first_terminal)
    assert _roots_over_f2(first_branch) == (1,)
    assert _roots_over_f2(first_terminal) == ()

    second_branch = (1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0)
    penultimate = (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    second_terminal = (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    _assert_residual((1, 2), 4, 36, second_branch)
    _assert_residual((-3, 2), 5, 42, second_branch)
    _assert_residual((-7, -2), 6, 46, penultimate)
    _assert_residual((-7, -10), 7, 48, second_terminal)
    assert _roots_over_f2(second_branch) == (1,)
    assert _roots_over_f2(penultimate) == (1,)
    assert _roots_over_f2(second_terminal) == ()

    return {
        "status": "ok",
        "outcome": "D_inf_not_in_2J_Q2_i",
        "terminal_residual": "z^2+z+1",
        "fake_kernel_contribution_dimension": 1,
    }


def main() -> int:
    result = verify_certificate()
    print(
        "dinf status={status} outcome={outcome} terminal={terminal_residual} "
        "kernel_contribution={fake_kernel_contribution_dimension}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
