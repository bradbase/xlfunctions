import decimal
import math
import numpy
import pandas
from typing import List, Union

from . import xl


@xl.register()
@xl.validate_args
def ABS(number: xl.Number):
    """Find the absolute value of provided value.

    https://support.office.com/en-us/article/
        abs-function-3420200f-5628-4e8c-99da-c99d7c87713c
    """
    return abs(number)


@xl.register()
@xl.validate_args
def LN(number: xl.Number):
    """Returns the natural logarithm of a number.

    https://support.office.com/en-us/article/
        ln-function-81fe1ed7-dac9-4acd-ba1d-07a142c6118f
    """
    return math.log(number)


@xl.register()
@xl.validate_args
def MOD(number: xl.Integer, divisor: xl.Integer):
    """Returns the remainder after number is divided by divisor.

    https://support.office.com/en-us/article/
        mod-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    """
    return number % divisor


@xl.register()
def PI():
    """Returns the number 3.14159265358979, the mathematical constant pi.

    Accurate to 15 digits.

    https://support.office.com/en-us/article/
        pi-function-264199d0-a3ba-46b8-975a-c4a04608989b
    """
    return math.pi


@xl.register()
@xl.validate_args
def POWER(number: xl.Number, power: xl.Number):
    """Returns the result of a number raised to a power.

    https://support.office.com/en-us/article/
        power-function-d3f2908b-56f4-4c3f-895a-07fb519c362a
    """
    return numpy.power(number, power)


@xl.register()
@xl.validate_args
def ROUND(
        number: xl.Number,
        num_digits: xl.Integer = 0,
        _rounding=decimal.ROUND_HALF_UP
):
    """Rounding half up

    https://support.office.com/en-us/article/
        ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c
    """
    number = decimal.Decimal(str(number))
    dc = decimal.getcontext()
    dc.rounding = _rounding
    ans = round(number, num_digits)
    return float(ans)


@xl.register()
@xl.validate_args
def ROUNDUP(number: xl.Number, num_digits: xl.Integer = 0):
    """Round up

    https://support.office.com/en-us/article/
         ROUNDUP-function-f8bc9b23-e795-47db-8703-db171d0c42a7
    """
    return ROUND(number, num_digits=num_digits, _rounding=decimal.ROUND_UP)


@xl.register()
@xl.validate_args
def ROUNDDOWN(number: xl.Number, num_digits: xl.Integer = 0):
    """Round down

    https://support.office.com/en-us/article/
        rounddown-function-2ec94c73-241f-4b01-8c6f-17e6d7968f53
    """
    return ROUND(number, num_digits=num_digits, _rounding=decimal.ROUND_DOWN)


@xl.register()
@xl.validate_args
def SQRT(number: xl.Number):
    """Returns a positive square root.

    https://support.office.com/en-us/article/
        sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf
    """
    if number < 0:
        return xl.NumExcelError(f'number {number} must be non-negative')

    return math.sqrt(number)


@xl.register()
def SUM(*numbers):
    """The SUM function adds values.

    https://support.office.com/en-us/article/
        sum-function-043e1c7d-7726-4e80-8f32-07b23e057f89
    """
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) == 0:
        return 0

    return sum(filter(xl.is_number, xl.flatten(numbers)))


@xl.register()
@xl.validate_args
def SUMIF(range: xl.Range, criteria, sum_range: xl.Range = None):
    """Adds the cells specified by a given criteria.

    https://support.office.com/en-us/article/
        sumif-function-169b8c99-c05c-4483-a712-1697a653039b
    """
    # WARNING:
    # - wildcards not supported

    if not xl.is_criteria(criteria):
        return 0

    check = xl.parse_criteria(criteria)

    if sum_range is None:
        sum_range = range

    range = xl.flatten(range)
    sum_range = xl.flatten(sum_range)

    # zip() will automatically drop any range values that have indexes larger
    # than sum_range's length.
    return sum([
        sval
        for cval, sval in zip(range, sum_range)
        if check(cval)
    ])


@xl.register()
@xl.validate_args
def SUMPRODUCT(*ranges: List[xl.Range]):
    """Returns the sum of the products of corresponding ranges or arrays.

    https://support.office.com/en-us/article/
        sumproduct-function-16753e75-9f68-4874-94ac-4d2145a2fd2e
    """
    if len(ranges) == 0:
        return xl.NullExcelError('Not enough arguments for function.')

    range1_len = xl.length(ranges[0])
    if range1_len == 0:
        return 0

    for range in ranges:
        range_len = xl.length(range)
        if range1_len != range_len:
            return xl.ValueExcelError(
                f"The length of the ranges does not match. Looking "
                f"for {range1_len} but given range has length {range_len}")
        if any(filter(xl.is_error, xl.flatten(range))):
            return xl.NaExcelError(
                "Excel Errors are present in the sumproduct items.")

    sumproduct = pandas.concat(ranges, axis=1)
    return sumproduct.prod(axis=1).sum()


@xl.register()
@xl.validate_args
def TRUNC(number: xl.Number, num_digits: xl.Integer = 0):
    """Truncate a number to the specified number of digits.

    https://support.office.com/en-us/article/
        trunc-function-8b86a64c-3127-43db-ba14-aa5ceb292721
    """
    # Simple case. We want to make sure to return an integer in this
    # case.
    if num_digits == 0:
        return math.trunc(number)

    return math.trunc(number * 10**num_digits) / 10**num_digits
