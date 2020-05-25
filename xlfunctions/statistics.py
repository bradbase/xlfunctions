import numpy

from . import xl


@xl.register()
@xl.validate_args
def AVERAGE(*numbers):
    """Returns the average (arithmetic mean) of the arguments.

    https://support.office.com/en-us/article/
        average-function-047bac88-d466-426c-a32b-8f33eb960cf6
    """
    numbers = xl.flatten(numbers)

    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    return numpy.average(list(filter(xl.is_number, numbers)))


@xl.register()
@xl.validate_args
def COUNT(*values):
    """Counts the number of cells that contain numbers, and counts numbers
    within the list of arguments.

    https://support.office.com/en-us/article/
        count-function-a59cd7fc-b623-4d93-87a4-d23bf411294c
    """
    values = xl.flatten(values)
    if not len(values) or values[0] is None:
        return xl.ValueExcelError('value1 is required')

    if len(values) > 255:
        return xl.ValueExcelError(
            f"Can only have up to 255 supplimentary arguments. "
            f"Provided: {len(values)}")

    return len(list(filter(xl.is_number, values)))


@xl.register()
@xl.validate_args
def COUNTA(*values):
    """Counts the number of cells that are not empty in a range.

    https://support.office.com/en-us/article/
        counta-function-7dc98875-d5c1-46f1-9a82-53f3219e2509
    """
    values = xl.flatten(values)
    if not len(values) or values[0] is None:
        return xl.NullExcelError('value1 is required')

    if len(values) > 255:
        return xl.ValueExcelError(
            f"Can only have up to 255 supplimentary arguments. "
            f"Provided: {len(values)}")

    return len(list(filter(lambda x: not xl.is_empty(x), values)))


@xl.register()
@xl.validate_args
def MAX(*numbers):
    """Returns the largest value in a set of values.

    https://support.office.com/en-us/article/
        max-function-e0012414-9ac8-4b34-9a47-73e662c08098
    """
    numbers = xl.flatten(numbers)
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    return max(filter(xl.is_number, numbers))


@xl.register()
@xl.validate_args
def MIN(*numbers):
    """Returns the smallest number in a set of values.

    https://support.office.com/en-us/article/
        min-function-61635d12-920f-4ce2-a70f-96f202dcc152
    """
    numbers = xl.flatten(numbers)

    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    return min(filter(xl.is_number, numbers))
