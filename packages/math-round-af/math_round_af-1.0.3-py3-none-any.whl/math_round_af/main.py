"""This module contain function for mathematical rounding of float numbers."""


def get_rounded_number(
        number: float,
        number_of_digits_after_separator: int = 0,
) -> float:
    """
    Return rounded float number.

    Parameters
    ----------
    number : float
        Number to be rounded.
    number_of_digits_after_separator
        Number of digits after
        decimal separator in `number`.

    Returns
    -------
    float
        Rounded float number.

    """
    if number_of_digits_after_separator < 0:
        raise ValueError(
            '`number_of_digits_after_separator` '
            'must to be positive integer number.'
        )
    sign = -1.0 if number < 0 else 1.0
    _number = abs(number)
    _multiplier = int('1' + '0' * number_of_digits_after_separator)
    _number_without_separator = _number * _multiplier
    _integer_part = int(_number_without_separator)
    _first_discarded_digit = int(
        (_number_without_separator - _integer_part) * 10
    )
    if _first_discarded_digit >= 5:
        _integer_part += 1
    result = _integer_part / _multiplier * sign
    return result
