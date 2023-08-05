"""This module contain test for `math_round_af` project."""


import pytest

from .main import get_rounded_number


CASES = {
    0: [
        (0.0, 0.0),
        (0.1, 0.0),
        (0.4, 0.0),
        (0.5, 1.0),
        (0.6, 1.0),
        (0.9, 1.0),
        (1.0, 1.0),
        (1.1, 1.0),
        (-0.0, 0.0),
        (-0.1, 0.0),
        (-0.4, 0.0),
        (-0.5, -1.0),
        (-0.6, -1.0),
        (-0.9, -1.0),
        (-1.0, -1.0),
        (-1.1, -1.0),
    ],
    1: [
        (0.00, 0.0),
        (0.01, 0.0),
        (0.04, 0.0),
        (0.05, 0.1),
        (0.06, 0.1),
        (0.09, 0.1),
        (0.10, 0.1),
        (0.11, 0.1),
        (-0.00, 0.0),
        (-0.01, 0.0),
        (-0.04, 0.0),
        (-0.05, -0.1),
        (-0.06, -0.1),
        (-0.09, -0.1),
        (-0.10, -0.1),
        (-0.11, -0.1),
    ]
}


@pytest.mark.parametrize("number, expected", CASES[0])
def test_get_rounded_number_0_expected(number, expected):
    """
    Test for `get_rounded_number` with `number_of_digits_after_separator`
    equal to 0.

    """
    assert get_rounded_number(number, 0) == expected


@pytest.mark.parametrize("number, expected", CASES[1])
def test_get_rounded_number_1_expected(number, expected):
    """
    Test for `get_rounded_number` with `number_of_digits_after_separator`
    equal to 1.

    """
    assert get_rounded_number(number, 1) == expected


@pytest.mark.parametrize("number", [i / 10 for i in range(-1000, 1000)])
def test_get_rounded_number_0_built_in(number):
    """
    Test for `get_rounded_number` with `number_of_digits_after_separator`
    equal to 0.

    """
    if str(number)[-1] == '5' and get_rounded_number(number, 0) % 2:
        assert abs(get_rounded_number(number, 0) - round(number, 0)) == 1.0
    else:
        assert get_rounded_number(number, 0) == round(number, 0)
