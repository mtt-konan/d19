#!/usr/bin/env sage
"""Generate the exact Q3a dyadic completion and squareclass certificate.

The generator starts with the absolute defining polynomial and the two exact
prime ideals above 2.  It works in the maximal order and uses the finite
primary quotients O/P^(2e+1); no p-adic factorization or bounded residue
search is used as a mathematical input.
"""

import json
import hashlib
import sys
from itertools import product
from pathlib import Path

from sage.all import (  # type: ignore[import-not-found]
    QQ,
    ZZ,
    NumberField,
    QuadraticField,
    PolynomialRing,
    identity_matrix,
    matrix,
    vector,
)

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
OUT = TASK / "q3a2-dyadic-matrices-payload.json"
Q2B_PAYLOAD = ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715/q2b-fixed-basis-payload.json"
sys.path.insert(0, str(ROOT))

F12_COEFFICIENTS = (
    1,
    -12,
    194,
    -788,
    623,
    -376,
    2716,
    4184,
    1647,
    68,
    -62,
    -4,
    1,
)


def qpair(value):
    value = QQ(value)
    return [int(value.numerator()), int(value.denominator())]


def encode_vector(values):
    return [[int(QQ(value).numerator()), int(QQ(value).denominator())] for value in values]


def to_integer_vector(values):
    values = [ZZ(value) for value in values]
    return [int(value) for value in values]


def build_field():
    Qx = PolynomialRing(QQ, "x")
    x = Qx.gen()
    f12 = Qx(F12_COEFFICIENTS)
    La = NumberField(f12, "a")
    O = La.maximal_order()
    primes = sorted(La.primes_above(2), key=lambda P: P.norm())
    if len(primes) != 2:
        raise AssertionError("the certified dyadic decomposition must have two primes")
    data = []
    for index, P in enumerate(primes, start=1):
        e = ZZ(P.ramification_index())
        f = ZZ(P.residue_class_degree())
        if (e, f) not in ((4, 1), (8, 1)):
            raise AssertionError(f"unexpected dyadic prime data {(e, f)}")
        data.append((index, P, e, f))
    return La, O, data


def power_coordinates(element):
    return [QQ(value) for value in element.list()]


def order_coordinates(La, O, element):
    ambient = vector(QQ, power_coordinates(element))
    coords = O.free_module().coordinate_vector(ambient)
    return tuple(QQ(value) for value in coords)


def encode_matrix(matrix):
    return [[int(value) for value in row] for row in matrix.rows()]


def build_order_data(La, O):
    basis = O.basis()
    basis_power = [power_coordinates(element) for element in basis]
    multiplication = []
    for left in basis:
        row = []
        for right in basis:
            row.append(to_integer_vector(order_coordinates(La, O, left * right)))
        multiplication.append(row)
    return {
        "basis_power_coordinates": basis_power,
        "basis_power_coordinates_shape": [len(basis_power), len(basis_power[0])],
        "multiplication_table": multiplication,
    }


def ideal_matrix(La, O, ideal):
    rows = [order_coordinates(La, O, element) for element in ideal.basis()]
    if any(any(value.denominator() != 1 for value in row) for row in rows):
        raise AssertionError("ideal basis is not integral in the maximal order basis")
    return matrix(ZZ, [to_integer_vector(row) for row in rows])


def hnf_for_ideal(La, O, ideal):
    matrix_ideal = ideal_matrix(La, O, ideal)
    hnf = matrix_ideal.hermite_form()
    if hnf.nrows() != 12 or hnf.ncols() != 12:
        raise AssertionError("unexpected ideal lattice rank")
    if hnf.det() <= 0 or any(hnf[row, column] != 0 for row in range(12) for column in range(row)):
        raise AssertionError("expected a positive upper-triangular row HNF")
    return hnf


def canonical_reducer(hnf):
    diagonal = [ZZ(hnf[index, index]) for index in range(12)]
    if any(value <= 0 for value in diagonal):
        raise AssertionError("HNF diagonal is not positive")

    def reduce_vector(vector_value):
        current = [ZZ(value) for value in vector_value]
        for index in range(12):
            quotient, remainder = current[index].quo_rem(diagonal[index])
            current[index] = remainder
            if quotient:
                for column in range(index + 1, 12):
                    current[column] -= quotient * hnf[index, column]
        if any(current[index] < 0 or current[index] >= diagonal[index] for index in range(12)):
            raise AssertionError("HNF reduction left a noncanonical coordinate")
        return tuple(int(value) for value in current)

    return reduce_vector


def multiplication_table_from_order_data(La, O):
    basis = O.basis()
    table = []
    for left in basis:
        row = []
        for right in basis:
            row.append(tuple(to_integer_vector(order_coordinates(La, O, left * right))))
        table.append(row)
    return table


def multiply_order(left, right, table):
    result = [0] * 12
    for left_index, left_value in enumerate(left):
        if left_value == 0:
            continue
        for right_index, right_value in enumerate(right):
            if right_value == 0:
                continue
            product_vector = table[left_index][right_index]
            for coordinate, value in enumerate(product_vector):
                result[coordinate] += left_value * right_value * value
    return result


def quotient_data(La, O, P, e):
    modulus_exponent = 2 * int(e) + 1
    hnf = hnf_for_ideal(La, O, P**modulus_exponent)
    reduce_vector = canonical_reducer(hnf)
    hnf_one = hnf_for_ideal(La, O, P)
    reduce_one = canonical_reducer(hnf_one)
    diagonal = [int(hnf[index, index]) for index in range(12)]
    residues = list(product(*(range(value) for value in diagonal)))
    if len(residues) != 2**modulus_exponent:
        raise AssertionError("primary quotient cardinality does not equal 2^(2e+1)")
    return {
        "precision_exponent": modulus_exponent,
        "ideal_hnf": encode_matrix(hnf),
        "ideal_hnf_p": encode_matrix(hnf_one),
        "diagonal": diagonal,
        "residue_count": len(residues),
        "reduce_vector": reduce_vector,
        "reduce_one": reduce_one,
        "one": reduce_vector(order_coordinates(La, O, La(1))),
        "residues": residues,
    }


def quotient_multiplication(left, right, quotient, table):
    return quotient["reduce_vector"](multiply_order(left, right, table))


def quotient_power(value, exponent, quotient, table):
    result = quotient["one"]
    base = value
    while exponent:
        if exponent & 1:
            result = quotient_multiplication(result, base, quotient, table)
        base = quotient_multiplication(base, base, quotient, table)
        exponent >>= 1
    return result


def quotient_inverse(value, quotient, table):
    # The residue field is F_2, so the unit group has order 2^(m-1) for
    # m=2e+1.  The exponent below is congruent to -1 modulo that order; the
    # resulting inverse is also checked by multiplication in the quotient.
    exponent = 2 ** quotient["precision_exponent"] - 1
    inverse = quotient_power(value, exponent, quotient, table)
    one = quotient["one"]
    if quotient_multiplication(value, inverse, quotient, table) != one:
        raise AssertionError("unit inverse exponent failed")
    return inverse


def in_ideal(vector_value, hnf):
    reducer = canonical_reducer(hnf)
    return reducer(vector_value) == (0,) * 12


def local_unit_residue(La, O, P, e, element, uniformizer, quotient, table):
    valuation = La.valuation(P)(element)
    integer_valuation = ZZ(e * valuation)
    if integer_valuation not in ZZ:
        raise AssertionError("local valuation is not integral")
    unit = element / uniformizer**integer_valuation
    if La.valuation(P)(unit) != 0:
        raise AssertionError("uniformizer did not remove the local valuation")
    denominator_ideal = O.fractional_ideal(1 / unit)
    integral_denominator_ideal = denominator_ideal.intersection(O.fractional_ideal(1))
    denominator = next(
        (candidate for candidate in integral_denominator_ideal.basis()
         if e * La.valuation(P)(candidate) == 0),
        None,
    )
    if denominator is None:
        raise AssertionError("no local unit denominator found in the integral intersection")
    numerator = denominator * unit
    if numerator not in O:
        raise AssertionError("local unit denominator did not clear integrality")
    denominator_coords = tuple(int(value) for value in order_coordinates(La, O, denominator))
    numerator_coords = tuple(int(value) for value in order_coordinates(La, O, numerator))
    denominator_residue = quotient["reduce_vector"](denominator_coords)
    numerator_residue = quotient["reduce_vector"](numerator_coords)
    denominator_inverse = quotient_inverse(denominator_residue, quotient, table)
    residue = quotient_multiplication(
        numerator_residue, denominator_inverse, quotient, table
    )
    if quotient["reduce_one"](residue) == (0,) * 12:
        raise AssertionError("a local unit reduced to the prime ideal")
    return integer_valuation, residue


def unit_squareclasses(quotient, table):
    residues = quotient["residues"]
    reduce_vector = quotient["reduce_vector"]
    one = quotient["one"]
    units = [value for value in residues if quotient["reduce_one"](value) != (0,) * 12]
    square_set = {
        quotient_multiplication(value, value, quotient, table) for value in units
    }
    represented = set(square_set)
    basis = []
    for candidate in units:
        if candidate in represented:
            continue
        basis.append(candidate)
        represented.update(
            quotient_multiplication(candidate, value, quotient, table)
            for value in tuple(represented)
        )
        if len(represented) == len(units):
            break
    expected_dimension = quotient["local_degree"] + 1
    if len(basis) != expected_dimension:
        raise AssertionError(
            f"unit squareclass dimension {len(basis)} != {expected_dimension}"
        )
    coordinate_map = {}
    for bits in product((0, 1), repeat=len(basis)):
        representative = one
        for bit, generator in zip(bits, basis, strict=True):
            if bit:
                representative = quotient_multiplication(representative, generator, quotient, table)
        for square in square_set:
            value = quotient_multiplication(representative, square, quotient, table)
            if value in coordinate_map and coordinate_map[value] != bits:
                raise AssertionError("unit squareclass coordinates are not unique")
            coordinate_map[value] = bits
    if len(coordinate_map) != len(units):
        raise AssertionError("unit squareclass coordinate map is incomplete")
    return basis, square_set, coordinate_map


def unit_coordinates(residue, coordinate_map):
    try:
        return coordinate_map[residue]
    except KeyError as error:
        raise AssertionError("residue is not represented by the unit squareclass basis") from error


def serialize_element(element):
    return encode_vector(power_coordinates(element))


def decode_payload_element(La, payload_element):
    a = La.gen()
    return La(
        sum(
            QQ(coordinate[0]) / QQ(coordinate[1]) * a**index
            for index, coordinate in enumerate(payload_element)
        )
    )


def load_ambient_elements(La):
    payload = json.loads(Q2B_PAYLOAD.read_text(encoding="utf-8"))
    elements = payload["s_unit_group"]["elements"]
    return {
        element["label"]: decode_payload_element(La, element["coordinates"])
        for element in elements
    }


def local_squareclass_vector(La, O, P, e, uniformizer, quotient, table, coordinate_map, element):
    valuation, residue = local_unit_residue(
        La, O, P, e, element, uniformizer, quotient, table
    )
    return [int(valuation % 2), *map(int, unit_coordinates(residue, coordinate_map))]


def matrix_columns(columns):
    if not columns:
        return []
    return [list(row) for row in zip(*columns)]


def f2_rref(rows):
    rows = [[int(value) & 1 for value in row] for row in rows]
    if not rows:
        return rows, []
    width = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column]:
                rows[row] = [left ^ right for left, right in zip(rows[row], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def f2_rank(rows):
    return len(f2_rref(rows)[1])


def f2_inverse(rows):
    size = len(rows)
    augmented = [
        [int(value) & 1 for value in row] + [int(index == column) for column in range(size)]
        for index, row in enumerate(rows)
    ]
    reduced, pivots = f2_rref(augmented)
    if pivots != list(range(size)):
        raise AssertionError("matrix is not invertible over F_2")
    return [row[size:] for row in reduced]


def f2_matmul(left, right):
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right))) % 2
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def f2_nullspace(rows):
    reduced, pivots = f2_rref(rows)
    width = len(rows[0]) if rows else 0
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector_value = [0] * width
        vector_value[free] = 1
        for row, pivot in reversed(list(enumerate(pivots))):
            vector_value[pivot] = sum(
                reduced[row][column] * vector_value[column]
                for column in free_columns
            ) % 2
        basis.append(vector_value)
    return basis


def extend_independent_columns(columns, dimension):
    result = [list(column) for column in columns]
    rank = f2_rank(matrix_columns(result))
    selected_standard = []
    for index in range(dimension):
        candidate = [int(row == index) for row in range(dimension)]
        trial = result + [candidate]
        trial_rank = f2_rank(matrix_columns(trial))
        if trial_rank > rank:
            result.append(candidate)
            selected_standard.append(index)
            rank = trial_rank
        if rank == dimension:
            break
    if rank != dimension:
        raise AssertionError("failed to extend the diagonal image to a basis")
    return result, selected_standard


def rank_mod_two(rows):
    rows = [list(map(int, row)) for row in rows]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][column] & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(len(rows)):
            if row != rank and rows[row][column] & 1:
                rows[row] = [left ^ right for left, right in zip(rows[row], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def pair_mul(left, right):
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def pair_pow(value, exponent):
    result = (1, 0)
    base = value
    while exponent:
        if exponent & 1:
            result = pair_mul(result, base)
        base = pair_mul(base, base)
        exponent >>= 1
    return result


def gaussian_quotient():
    uniformizer = (1, 1)
    power = pair_pow(uniformizer, 5)
    hnf = matrix(ZZ, [power, (-power[1], power[0])]).hermite_form()
    prime_hnf = matrix(ZZ, [uniformizer, (-uniformizer[1], uniformizer[0])]).hermite_form()

    def reducer(matrix_value):
        diagonal = [ZZ(matrix_value[index, index]) for index in range(2)]

        def reduce_value(value):
            current = [ZZ(value[0]), ZZ(value[1])]
            for index in range(2):
                quotient, remainder = current[index].quo_rem(diagonal[index])
                current[index] = remainder
                for column in range(index + 1, 2):
                    current[column] -= quotient * matrix_value[index, column]
            return (int(current[0]), int(current[1]))

        return reduce_value

    reduce_value = reducer(hnf)
    reduce_prime = reducer(prime_hnf)
    residues = list(product(*(range(int(hnf[index, index])) for index in range(2))))
    units = [value for value in residues if reduce_prime(value) != (0, 0)]
    square_set = {reduce_value(pair_mul(value, value)) for value in units}
    one = reduce_value((1, 0))
    represented = set(square_set)
    basis = []
    for candidate in units:
        if candidate in represented:
            continue
        basis.append(candidate)
        represented.update(reduce_value(pair_mul(candidate, value)) for value in tuple(represented))
        if len(represented) == len(units):
            break
    coordinate_map = {}
    for bits in product((0, 1), repeat=len(basis)):
        representative = one
        for bit, generator in zip(bits, basis, strict=True):
            if bit:
                representative = reduce_value(pair_mul(representative, generator))
        for square in square_set:
            value = reduce_value(pair_mul(representative, square))
            if value in coordinate_map and coordinate_map[value] != bits:
                raise AssertionError("Gaussian squareclass coordinates are not unique")
            coordinate_map[value] = bits
    if len(coordinate_map) != len(units):
        raise AssertionError("Gaussian squareclass coordinates are incomplete")
    requested_basis = [(0, 1), (3, 0), (1, 2)]
    requested_map = {}
    for bits in product((0, 1), repeat=len(requested_basis)):
        representative = one
        for bit, generator in zip(bits, requested_basis, strict=True):
            if bit:
                representative = reduce_value(pair_mul(representative, generator))
        for square in square_set:
            value = reduce_value(pair_mul(representative, square))
            if value in requested_map and requested_map[value] != bits:
                raise AssertionError("requested K squareclass basis is dependent")
            requested_map[value] = bits
    if len(requested_map) != len(units):
        raise AssertionError("requested K squareclass basis is incomplete")
    return {
        "uniformizer": uniformizer,
        "precision_exponent": 5,
        "ideal_hnf": encode_matrix(hnf),
        "ideal_hnf_prime": encode_matrix(prime_hnf),
        "residue_count": len(residues),
        "unit_square_count": len(square_set),
        "basis_residues": [list(value) for value in requested_basis],
        "reduce": reduce_value,
        "reduce_prime": reduce_prime,
        "square_set": square_set,
        "coordinate_map": requested_map,
    }


def k_element_pair(element):
    return (QQ(element[0]), QQ(element[1]))


def k_unit_residue(K, OK, PK, gaussian, element):
    valuation = ZZ(2 * K.valuation(PK)(element))
    unit = element / (1 + K.gen())**valuation
    if 2 * K.valuation(PK)(unit) != 0:
        raise AssertionError("K uniformizer did not remove valuation")
    denominator_ideal = OK.fractional_ideal(1 / unit)
    integral_denominator_ideal = denominator_ideal.intersection(OK.fractional_ideal(1))
    denominator = next(
        candidate
        for candidate in integral_denominator_ideal.basis()
        if 2 * K.valuation(PK)(candidate) == 0
    )
    numerator = denominator * unit
    if numerator not in OK:
        raise AssertionError("K denominator did not clear integrality")
    denominator_pair = tuple(QQ(value) for value in denominator.list())
    numerator_pair = tuple(QQ(value) for value in numerator.list())
    if any(value.denominator() != 1 for value in (*denominator_pair, *numerator_pair)):
        raise AssertionError("K local integral numerator/denominator is not integral")
    denominator_residue = gaussian["reduce"](tuple(int(value) for value in denominator_pair))
    numerator_residue = gaussian["reduce"](tuple(int(value) for value in numerator_pair))
    inverse = pair_pow(denominator_residue, 2**gaussian["precision_exponent"] - 1)
    inverse = gaussian["reduce"](inverse)
    residue = gaussian["reduce"](pair_mul(numerator_residue, inverse))
    if residue not in gaussian["coordinate_map"]:
        raise AssertionError("K unit residue has no squareclass coordinate")
    return valuation, residue


def k_squareclass_vector(K, OK, PK, gaussian, element):
    valuation, residue = k_unit_residue(K, OK, PK, gaussian, element)
    return [int(valuation % 2), *map(int, gaussian["coordinate_map"][residue])]


def relative_coordinates(La, K, i_absolute, basis_inverse, element):
    coefficients = basis_inverse * vector(QQ, power_coordinates(element))
    return [K(coefficients[index] + coefficients[index + 6] * K.gen()) for index in range(6)]


def relative_matrix(La, K, i_absolute, basis_inverse, element):
    a = La.gen()
    columns = [relative_coordinates(La, K, i_absolute, basis_inverse, element * a**index)
               for index in range(6)]
    return matrix(K, 6, 6, lambda row, column: columns[column][row])


def local_norm_squareclass(
    La,
    O,
    K,
    OK,
    PK,
    i_absolute,
    basis_inverse,
    P,
    other_P,
    e,
    other_e,
    gaussian,
    uniformizer,
    element,
):
    # lambda=1+i has absolute valuations 2 and 4 at the two dyadic primes.
    lambda_absolute = 1 + i_absolute
    lambda_K = 1 + K.gen()
    lambda_precision = 8
    self_ideal = P ** (int((e // 2) * lambda_precision))
    other_ideal = other_P ** (int((other_e // 2) * lambda_precision))
    idempotent = La.idealchinese([self_ideal, other_ideal], [1, 0])
    if idempotent not in O:
        raise AssertionError("CRT idempotent is not integral")
    if (idempotent - 1) not in self_ideal or idempotent not in other_ideal:
        raise AssertionError("CRT idempotent congruences failed")
    if idempotent**2 - idempotent not in lambda_absolute**lambda_precision * O:
        raise AssertionError("CRT idempotent is not lambda-adically idempotent")
    idempotent_matrix = relative_matrix(La, K, i_absolute, basis_inverse, idempotent)
    element_matrix = relative_matrix(La, K, i_absolute, basis_inverse, element)
    identity = identity_matrix(K, 6)
    patched_element = idempotent * element + 1 - idempotent
    self_relative_error = e * La.valuation(P)(patched_element / element - 1)
    other_error = other_e * La.valuation(other_P)(patched_element - 1)
    if self_relative_error < 2 * e + 1 or other_error < 2 * other_e + 1:
        raise AssertionError("CRT patch is not deep enough to preserve local squareclasses")
    determinant = (idempotent_matrix * element_matrix + identity - idempotent_matrix).det()
    local_valuation = ZZ(2 * K.valuation(PK)(determinant))
    expected_valuation = ZZ(e * La.valuation(P)(element))
    if local_valuation != expected_valuation:
        raise AssertionError(
            f"relative norm valuation {local_valuation} != local valuation {expected_valuation}"
        )
    return {
        "determinant": [qpair(value) for value in determinant.list()],
        "squareclass": k_squareclass_vector(K, OK, PK, gaussian, determinant),
        "idempotent_power_coordinates": serialize_element(idempotent),
        "lambda_precision_exponent": lambda_precision,
    }


def local_coordinate_record(La, O, P, e, f, table, ambient):
    quotient = quotient_data(La, O, P, e)
    quotient["local_degree"] = int(e * f)
    uniformizer = La.uniformizer(P)
    if e * La.valuation(P)(uniformizer) != 1:
        raise AssertionError("Sage uniformizer is not a local uniformizer")
    unit_basis, square_set, coordinate_map = unit_squareclasses(quotient, table)
    basis_rows = [[int(value) for value in row] for row in unit_basis]
    unit_power_coordinates = []
    for residue in unit_basis:
        element = sum(residue[index] * O.basis()[index] for index in range(12))
        unit_power_coordinates.append(serialize_element(element))
    local_witnesses = {}
    local_columns = {}
    for label, element in ambient.items():
        valuation, residue = local_unit_residue(
            La, O, P, e, element, uniformizer, quotient, table
        )
        local_witnesses[label] = {
            "valuation": int(valuation),
            "unit_residue": list(residue),
        }
        local_columns[label] = [int(valuation % 2), *map(int, unit_coordinates(residue, coordinate_map))]
    return {
        "index": int(P.norm()),
        "ramification_index": int(e),
        "residue_degree": int(f),
        "absolute_degree": int(e * f),
        "prime_basis": encode_matrix(ideal_matrix(La, O, P)),
        "prime_hnf": encode_matrix(hnf_for_ideal(La, O, P)),
        "uniformizer_power_coordinates": serialize_element(uniformizer),
        "quotient": {
            key: value
            for key, value in quotient.items()
            if key in ("precision_exponent", "ideal_hnf", "ideal_hnf_p", "diagonal", "residue_count")
        },
        "unit_basis_order_coordinates": basis_rows,
        "unit_basis_power_coordinates": unit_power_coordinates,
        "unit_square_count": len(square_set),
        "ambient_local_squareclass_columns": local_columns,
        "ambient_local_unit_residue_witnesses": local_witnesses,
    }


def main():
    La, O, prime_data = build_field()
    table = multiplication_table_from_order_data(La, O)
    ambient = load_ambient_elements(La)
    base_elements = {
        "lambda": ambient["zeta4"] * -1 + 1,
        "i": ambient["zeta4"] * -1,
        "three": La(3),
        "one_plus_two_i": 1 + 2 * ambient["zeta4"] * -1,
    }
    K = QuadraticField(-1, "iK")
    OK = K.maximal_order()
    PK = K.ideal(1 + K.gen())
    gaussian = gaussian_quotient()
    i_absolute = base_elements["i"]
    a = La.gen()
    relative_columns = [a**index for index in range(6)]
    relative_columns.extend(i_absolute * a**index for index in range(6))
    relative_basis_matrix = matrix(
        QQ,
        12,
        12,
        lambda row, column: power_coordinates(relative_columns[column])[row],
    )
    relative_basis_inverse = relative_basis_matrix.inverse()
    if relative_basis_matrix.det() != -QQ(1) / 2**34:
        raise AssertionError("relative K basis determinant changed")
    local_records = []
    for index, P, e, f in prime_data:
        record = local_coordinate_record(La, O, P, e, f, table, ambient)
        record["index"] = index
        quotient_for_base = quotient_data(La, O, P, e)
        quotient_for_base["local_degree"] = int(e * f)
        base_unit_data = unit_squareclasses(quotient_for_base, table)
        base_witnesses = {}
        base_columns_local = {}
        for label, element in base_elements.items():
            valuation, residue = local_unit_residue(
                La,
                O,
                P,
                e,
                element,
                La.uniformizer(P),
                quotient_for_base,
                table,
            )
            base_witnesses[label] = {"valuation": int(valuation), "unit_residue": list(residue)}
            base_columns_local[label] = [
                int(valuation % 2), *map(int, unit_coordinates(residue, base_unit_data[2]))
            ]
        record["base_squareclass_columns"] = base_columns_local
        record["base_local_unit_residue_witnesses"] = base_witnesses
        norm_basis_elements = [La.uniformizer(P)]
        norm_basis_elements.extend(
            sum(
                residue[index] * O.basis()[index] for index in range(12)
            )
            for residue in record["unit_basis_order_coordinates"]
        )
        record["basis_norm_squareclass_columns"] = [
            local_norm_squareclass(
                La,
                O,
                K,
                OK,
                PK,
                i_absolute,
                relative_basis_inverse,
                P,
                prime_data[1 if index == 1 else 0][1],
                e,
                prime_data[1 if index == 1 else 0][2],
                gaussian,
                La.uniformizer(P),
                element,
            )
            for element in norm_basis_elements
        ]
        print(
            "prime",
            index,
            "e",
            e,
            "unit basis",
            len(record["unit_basis_order_coordinates"]),
            "residues",
            record["quotient"]["residue_count"],
        )
        local_records.append(record)
    factor_columns = [
        local_records[0]["ambient_local_squareclass_columns"],
        local_records[1]["ambient_local_squareclass_columns"],
    ]
    product_columns = {
        label: factor_columns[0][label] + factor_columns[1][label]
        for label in ambient
    }
    base_columns = {
        label: local_records[0]["base_squareclass_columns"][label]
        + local_records[1]["base_squareclass_columns"][label]
        for label in base_elements
    }
    product_basis_labels = [
        "factor_1_uniformizer",
        *(f"factor_1_unit_{index}" for index in range(1, 6)),
        "factor_2_uniformizer",
        *(f"factor_2_unit_{index}" for index in range(1, 10)),
    ]
    if len(product_basis_labels) != 16:
        raise AssertionError("product basis must have sixteen squareclass coordinates")
    factor_norm_columns = [
        [item["squareclass"] for item in local_records[0]["basis_norm_squareclass_columns"]],
        [item["squareclass"] for item in local_records[1]["basis_norm_squareclass_columns"]],
    ]
    norm_columns = factor_norm_columns[0] + factor_norm_columns[1]
    norm_matrix = matrix_columns(norm_columns)
    from scripts.theory import berry_sextic_q2c_maps as q2c

    global_norm_columns = [
        k_squareclass_vector(
            K,
            OK,
            PK,
            gaussian,
            K(value[0]) + K(value[1]) * K.gen(),
        )
        for value in q2c.NORM_VALUES
    ]
    global_norm_matrix = matrix_columns(global_norm_columns)
    local_norm_of_ambient = [
        [
            sum(
                norm_matrix[row][column] * product_columns[label][column]
                for column in range(16)
            )
            % 2
            for label in ambient
        ]
        for row in range(4)
    ]
    if local_norm_of_ambient != global_norm_matrix:
        raise AssertionError("dyadic local norm columns disagree with global Q2c norms")
    localization_matrix = matrix_columns([product_columns[label] for label in ambient])
    diagonal_matrix = matrix_columns([base_columns[label] for label in base_elements])
    if f2_rank(diagonal_matrix) != 4:
        raise AssertionError("the four diagonal base squareclasses are dependent")
    extended_columns, complement_indices = extend_independent_columns(
        [base_columns[label] for label in base_elements], 16
    )
    complement_matrix = matrix_columns(extended_columns)
    complement_inverse = f2_inverse(complement_matrix)
    quotient_coordinate_matrix = complement_inverse[4:]
    quotient_block = [column for column in extended_columns[4:]]
    norm_on_quotient = f2_matmul(norm_matrix, matrix_columns(quotient_block))
    norm_kernel_basis = f2_nullspace(norm_on_quotient)
    h_lift_columns = [
        [
            sum(
                complement_matrix[row][column] * ([0, 0, 0, 0] + basis)[column]
                for column in range(16)
            )
            % 2
            for row in range(16)
        ]
        for basis in norm_kernel_basis
    ]
    ranks = {
        "diagonal_image_rank": f2_rank(diagonal_matrix),
        "product_squareclass_dimension": 16,
        "fake_quotient_dimension": 16 - f2_rank(diagonal_matrix),
        "product_norm_rank": f2_rank(norm_matrix),
        "norm_on_fake_quotient_rank": f2_rank(norm_on_quotient),
        "fake_norm_kernel_dimension": len(norm_kernel_basis),
        "ambient_localization_rank": f2_rank(localization_matrix),
        "fake_localization_rank": f2_rank(f2_matmul(quotient_coordinate_matrix, localization_matrix)),
    }
    if ranks["fake_norm_kernel_dimension"] != 8:
        raise AssertionError("the exact fake norm-kernel dimension changed")
    payload = {
        "schema_version": "berry-c1-q3a2-dyadic-matrices-v1",
        "field": {
            "absolute_polynomial_ascending": list(F12_COEFFICIENTS),
            "absolute_degree": 12,
            "maximal_order_discriminant": 5019340374016,
            "order_basis_power_coordinates": [
                [qpair(value) for value in row]
                for row in build_order_data(La, O)["basis_power_coordinates"]
            ],
            "order_one_coordinates": [
                int(value) for value in order_coordinates(La, O, La(1))
            ],
            "k_embedding_power_coordinates": serialize_element(i_absolute),
            "embedding_checks": {
                "i_squared": serialize_element(i_absolute**2),
                "minus_one": serialize_element(La(-1)),
                "relative_polynomial_at_a": serialize_element(
                    sum(
                        (QQ(constant) + QQ(i_coefficient) * i_absolute) * a**index
                        for index, (constant, i_coefficient) in enumerate(
                            ((-1, 0), (6, 14), (19, -40), (-52, -28), (-35, -8), (-2, -2), (1, 0))
                        )
                    )
                ),
            },
        },
        "order_multiplication_table": table,
        "local_records": local_records,
        "dyadic_factorization": {
            "rational_prime": 2,
            "prime_indices": [1, 2],
            "ramification_exponents": [4, 8],
            "residue_degrees": [1, 1],
            "identity": "(2) = P_1^4 P_2^8",
        },
        "ambient_power_basis_coordinates": {
            label: serialize_element(element) for label, element in ambient.items()
        },
        "q2b_payload_sha256": hashlib.sha256(Q2B_PAYLOAD.read_bytes()).hexdigest(),
        "ambient_labels": list(ambient),
        "base_squareclass_basis": ["lambda", "i", "three", "one_plus_two_i"],
        "base_squareclass_representatives": {
            label: serialize_element(element) for label, element in base_elements.items()
        },
        "product_squareclass_basis": product_basis_labels,
        "product_localization_columns": product_columns,
        "base_restriction_columns": base_columns,
        "product_basis_restriction_matrix": matrix_columns(
            [base_columns[label] for label in base_elements]
        ),
        "base_squareclass_local_certificate": {
            "basis": ["lambda", "i", "three", "one_plus_two_i"],
            "representatives": [[1, 1], [0, 1], [3, 0], [1, 2]],
            "ideal_hnf": gaussian["ideal_hnf"],
            "prime_hnf": gaussian["ideal_hnf_prime"],
            "precision_exponent": gaussian["precision_exponent"],
            "residue_count": gaussian["residue_count"],
            "unit_square_count": gaussian["unit_square_count"],
        },
        "relative_basis": {
            "order": ["1", "a", "a^2", "a^3", "a^4", "a^5"],
            "K_embedding": "i = -zeta4",
            "change_of_basis_determinant": qpair(relative_basis_matrix.det()),
        },
        "norm_matrix_rows": norm_matrix,
        "norm_basis_squareclass_columns": norm_columns,
        "global_norm_restriction_matrix": global_norm_matrix,
        "norm_localization_compatibility": True,
        "ambient_localization_matrix_rows": localization_matrix,
        "quotient_complement_standard_indices": complement_indices,
        "quotient_coordinate_matrix_rows": quotient_coordinate_matrix,
        "norm_matrix_on_fake_quotient_rows": norm_on_quotient,
        "norm_kernel_basis_quotient_rows": norm_kernel_basis,
        "norm_kernel_basis_product_lifts_columns": matrix_columns(h_lift_columns),
        "ranks": ranks,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
