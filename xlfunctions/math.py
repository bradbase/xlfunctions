import decimal
import math
import numpy
import pandas
from typing import Tuple

from . import xl, xlerrors, xltypes, xlcriteria


@xl.register()
@xl.validate_args
def ABS(
        number: xltypes.XlNumber
) -> xltypes.XlNumber:
    """Find the absolute value of provided value.

    https://support.office.com/en-us/article/
        abs-function-3420200f-5628-4e8c-99da-c99d7c87713c
    """
    return abs(number)


@xl.register()
@xl.validate_args
def LN(
        number: xltypes.XlNumber
) -> xltypes.XlNumber:
    """Returns the natural logarithm of a number.

    https://support.office.com/en-us/article/
        ln-function-81fe1ed7-dac9-4acd-ba1d-07a142c6118f
    """
    return math.log(number)


@xl.register()
@xl.validate_args
def MOD(
        number: xltypes.XlNumber,
        divisor: xltypes.XlNumber
) -> xltypes.XlNumber:
    """Returns the remainder after number is divided by divisor.

    https://support.office.com/en-us/article/
        mod-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    """
    return number % divisor


@xl.register()
def PI() -> xltypes.XlNumber:
    """Returns the number 3.14159265358979, the mathematical constant pi.

    Accurate to 15 digits.

    https://support.office.com/en-us/article/
        pi-function-264199d0-a3ba-46b8-975a-c4a04608989b
    """
    return math.pi


@xl.register()
@xl.validate_args
def POWER(
        number: xltypes.XlNumber,
        power: xltypes.XlNumber
) -> xltypes.XlNumber:
    """Returns the result of a number raised to a power.

    https://support.office.com/en-us/article/
        power-function-d3f2908b-56f4-4c3f-895a-07fb519c362a
    """
    return numpy.power(number, power)


@xl.register()
@xl.validate_args
def ROUND(
        number: xltypes.XlNumber,
        num_digits: xltypes.XlNumber = 0,
        _rounding=decimal.ROUND_HALF_UP
):
    """Rounding half up

    https://support.office.com/en-us/article/
        ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c
    """
    number = decimal.Decimal(str(number))
    dc = decimal.getcontext()
    dc.rounding = _rounding
    ans = round(number, int(num_digits))
    return float(ans)


@xl.register()
@xl.validate_args
def ROUNDUP(
        number: xltypes.XlNumber,
        num_digits: xltypes.XlNumber = 0
) -> xltypes.XlNumber:
    """Round up

    https://support.office.com/en-us/article/
         ROUNDUP-function-f8bc9b23-e795-47db-8703-db171d0c42a7
    """
    return ROUND(number, num_digits=num_digits, _rounding=decimal.ROUND_UP)


@xl.register()
@xl.validate_args
def ROUNDDOWN(
        number: xltypes.XlNumber,
        num_digits: xltypes.XlNumber = 0
) -> xltypes.XlNumber:
    """Round down

    https://support.office.com/en-us/article/
        rounddown-function-2ec94c73-241f-4b01-8c6f-17e6d7968f53
    """
    return ROUND(number, num_digits=num_digits, _rounding=decimal.ROUND_DOWN)


@xl.register()
@xl.validate_args
def SQRT(
        number: xltypes.XlNumber
) -> xltypes.XlNumber:
    """Returns a positive square root.

    https://support.office.com/en-us/article/
        sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf
    """
    if number < 0:
        raise xlerrors.NumExcelError(f'number {number} must be non-negative')

    return math.sqrt(number)


@xl.register()
@xl.validate_args
def SUM(
        *numbers: Tuple[xltypes.XlNumber]
) -> xltypes.XlNumber:
    """The SUM function adds values.

    https://support.office.com/en-us/article/
        sum-function-043e1c7d-7726-4e80-8f32-07b23e057f89
    """
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) == 0:
        return 0

    return sum(numbers)


@xl.register()
@xl.validate_args
def SUMIF(
        range: xltypes.XlArray,
        criteria: xltypes.XlAnything,
        sum_range: xltypes.XlArray = None
) -> xltypes.XlNumber:
    """Adds the cells specified by a given criteria.

    https://support.office.com/en-us/article/
        sumif-function-169b8c99-c05c-4483-a712-1697a653039b
    """
    # WARNING:
    # - wildcards not supported

    check = xlcriteria.parse_criteria(criteria)

    if sum_range is None:
        sum_range = range

    range = range.flat
    sum_range = sum_range.cast_to_numbers().flat

    # zip() will automatically drop any range values that have indexes larger
    # than sum_range's length.
    return sum([
        sval
        for cval, sval in zip(range, sum_range)
        if check(cval)
    ])


@xl.register()
@xl.validate_args
def SUMPRODUCT(
        *arrays: Tuple[xltypes.XlArray]
) -> xltypes.XlNumber:
    """Returns the sum of the products of corresponding arrays or arrays.

    https://support.office.com/en-us/article/
        sumproduct-function-16753e75-9f68-4874-94ac-4d2145a2fd2e
    """
    if len(arrays) == 0:
        raise xlerrors.NullExcelError('Not enough arguments for function.')

    array1_shape = arrays[0].shape
    if array1_shape == (0, 0):
        return 0

    for array in arrays:
        array_shape = array.shape
        if array1_shape != array_shape:
            raise xlerrors.ValueExcelError(
                f"The shapes of the arrays do not match. Looking "
                f"for {array1_shape} but given array has {array_shape}")
        if any(filter(xlerrors.ExcelError.is_error, xl.flatten(array))):
            raise xlerrors.NaExcelError(
                "Excel Errors are present in the sumproduct items.")

    sumproduct = pandas.concat(arrays, axis=1)
    return sumproduct.prod(axis=1).sum()


@xl.register()
@xl.validate_args
def TRUNC(
        number: xltypes.XlNumber,
        num_digits: xltypes.XlNumber = 0
) -> xltypes.XlNumber:
    """Truncate a number to the specified number of digits.

    https://support.office.com/en-us/article/
        trunc-function-8b86a64c-3127-43db-ba14-aa5ceb292721
    """
    # Simple case. We want to make sure to return an integer in this
    # case.
    if num_digits == 0:
        return math.trunc(number)

    num_digits = int(num_digits)

    return math.trunc(number * 10**num_digits) / 10**num_digits
