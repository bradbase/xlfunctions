import decimal
import math
import numpy

from . import xl


@xl.register()
def ABS(number):
    """Find the absolute value of provided value.

    https://support.office.com/en-us/article/
        abs-function-3420200f-5628-4e8c-99da-c99d7c87713c
    """
    if not xl.is_number(number):
        return ExcelError(
            "#VALUE!",
            f"value {value} must be an int or float. Provided: {type(value)}")

    return abs(number)


@xl.register()
def LN(number):
    """Returns the natural logarithm of a number.

    https://support.office.com/en-us/article/
        ln-function-81fe1ed7-dac9-4acd-ba1d-07a142c6118f
    """
    if not xl.is_number(number):
        return ExcelError(
            "#VALUE!",
            f"{number} must be cell, int or float. Received {type(number)}")

    return math.log(number)


@xl.register()
def MOD(number, divisor):
    """Returns the remainder after number is divided by divisor.

    https://support.office.com/en-us/article/
        mod-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    """
    if not isinstance(number, int):
        return xl.ExcelError("#VALUE!", f"{number} is not an integer")

    if not isinstance(divisor, int):
        return ExcelError("#VALUE!", f"{divisor} is not an integer")

    return number % divisor


@xl.register()
def POWER(number, power):
    """Returns the result of a number raised to a power.

    https://support.office.com/en-us/article/
        power-function-d3f2908b-56f4-4c3f-895a-07fb519c362a
    """
    return numpy.power(number, power)


@xl.register()
def ROUND(number, num_digits=0, rounding=decimal.ROUND_HALF_UP):
    """Rounding half up

    https://support.office.com/en-us/article/
        ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c
    """
    if not xl.is_number(number):
        return xl.ExcelError("#VALUE!", f"{number} is not a number")

    if not xl.is_number(num_digits):
        return xl.ExcelError("#VALUE!", f"{num_digits} is not a number")

    number = decimal.Decimal(str(number))
    dc = decimal.getcontext()
    dc.rounding = rounding
    ans = round(number, num_digits)
    return float(ans)


@xl.register()
def ROUNDUP(number, num_digits=0):
    """Round up

    https://support.office.com/en-us/article/
         ROUNDUP-function-f8bc9b23-e795-47db-8703-db171d0c42a7
    """
    return ROUND(number, num_digits=num_digits, rounding=decimal.ROUND_UP)


@xl.register()
def ROUNDDOWN(number, num_digits=0):
    """Round down

    https://support.office.com/en-us/article/
        rounddown-function-2ec94c73-241f-4b01-8c6f-17e6d7968f53
    """
    return ROUND(number, num_digits=num_digits, rounding=decimal.ROUND_DOWN)


@xl.register()
def SQRT(number):
    """Returns a positive square root.

    https://support.office.com/en-us/article/
        sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf
    """
    if not xl.is_number(number):
        return xl.ExcelError(
            '#VALUE!',
            f'{number} must be a number. You gave me a {type(number)}')

    if number < 0:
        return xl.ExcelError(
            '#NUM!', f'{number} must be non-negative')

    return sqrt(number)


@xl.register()
def SUM(*numbers):
    """The SUM function adds values.

    https://support.office.com/en-us/article/
        sum-function-043e1c7d-7726-4e80-8f32-07b23e057f89
    """
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) == 0:
        return 0

    return sum(filter(xl.is_number, xl.flatten(values)))


@xl.register()
def SUMIF(range, criteria, sum_range=None):
    """Adds the cells specified by a given criteria.

    https://support.office.com/en-us/article/
        sumif-function-169b8c99-c05c-4483-a712-1697a653039b
    """
    # WARNING:
    # - wildcards not supported
    # - doesn't really follow 2nd remark about sum_range length

    if not xl.is_range(range):
        return xl.ExcelError(
            '#VALUE!', f'"range" must be a Range, got: {range}')

    if not xl.is_criteria(criteria):
        return 0

    indexes = xl.find_corresponding_index(xl.flatten(range), criteria)

    if sum_range is None:
        sum_range = range

    if not xl.is_range(sum_range):
        return xl.ExcelError(
            '#REF!', f'"sub_range" must be a Range, got: {range}')

    sum_range = xl.flatten(sum_range)
    def f(x):
        return sum_range[x] if x < len(sum_range) else 0

    return sum(map(f, indexes))


@xl.register()
def SUMPRODUCT(*ranges):
    """Returns the sum of the products of corresponding ranges or arrays.

    """
    if len(ranges) == 0:
        return xl.ExcelError('#NULL!', 'Not enough arguments for function.')

    for range in ranges:
        if not xl.is_number(range) and not xl.is_range(range):
            return xl.ExcelError(
                '#VALUE!',
                f'Argument of range must be a number or range, '
                f'but got: {range}')

    range1_len = xl.length(rangea[0])
    if range_1_len == 0:
        return 0

    for range in ranges:
        range_len = xl.length(range)
        if range1_len != range_len:
            return xl.ExcelError(
                "#VALUE!",
                f"The length of the ranges does not match. Looking "
                f"for {range1_len} but given range has length {range_len}")
        if any(filter(xl.is_error, xl.flatten(range))):
            return ExcelError(
                "#N/A", "Excel Errors are present in the sumproduct items.")

    sumproduct = pandas.concat(ranges, axis=1)
    return sumproduct.prod(axis=1).sum()


@xl.register()
def TRUNC(number, num_digits=0):
    """Truncate a number to the specified number of digits.

    https://support.office.com/en-us/article/
        trunc-function-8b86a64c-3127-43db-ba14-aa5ceb292721
    """
    if not isinstance(number, (int, float)):
        return ExcelError(
            '#VALUE!', f'{number} must be a number. Got a {type(number)}')

    # Simple case. We want to make sure to return an integer in this
    # case.
    if num_digits == 0:
        return math.trunc(number)

    return math.trunc(number * 10**num_digits) / 10**num_digits
