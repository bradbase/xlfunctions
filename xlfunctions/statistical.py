import numpy

from . import xl


@xl.register()
def AVERAGE(*numbers):
    """Returns the average (arithmetic mean) of the arguments.

    https://support.office.com/en-us/article/
        average-function-047bac88-d466-426c-a32b-8f33eb960cf6
    """
    # However, if no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    return numpy.average(filter(xl.is_number, xl.flatten(values)))


@xl.register()
def COUNT(*values):
    """Counts the number of cells that contain numbers, and counts numbers
    within the list of arguments.

    https://support.office.com/en-us/article/
        count-function-a59cd7fc-b623-4d93-87a4-d23bf411294c
    """
    if not len(values) or values[0] is None:
        return xl.ExcelError('#VALUE', 'value1 is required')

    if len(list(args)) > 255:
        return ExcelError(
            '#VALUE',
            f"Can only have up to 255 supplimentary arguments. "
            f"Provided: {len(args)}")

    return len(filter(xl.is_number, xl.flatten(values)))


@xl.register()
def COUNTA(*values):
    """Counts the number of cells that are not empty in a range.

    https://support.office.com/en-us/article/
        counta-function-7dc98875-d5c1-46f1-9a82-53f3219e2509
    """
    if not len(values) or values[0] is None:
        return xl.ExcelError('#VALUE', 'value1 is required')

    if len(list(args)) > 255:
        return ExcelError(
            '#VALUE',
            f"Can only have up to 255 supplimentary arguments. "
            f"Provided: {len(args)}")

    return len(filter(xl.is_empty, xl.flatten(values)))


@xl.register()
def MAX(*numbers):
    """Returns the largest value in a set of values.

    https://support.office.com/en-us/article/
        max-function-e0012414-9ac8-4b34-9a47-73e662c08098
    """
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    # Make sure that numbers are all numbers or data frames. (Note that in
    # data frames text and empty cells are allowed and ignored.)
    for number in numbers:
        if not is_number(number) and not xl.is_range(number):
            return xl.ExcelError('#VALUE', f"{number} is not a number.")

    return max(xl.flatten(numbers))


@xl.register()
def MIN(*numbers):
    """Returns the smallest number in a set of values.

    https://support.office.com/en-us/article/
        min-function-61635d12-920f-4ce2-a70f-96f202dcc152
    """
    # If no non numeric cells, return zero (is what excel does)
    if len(numbers) < 1:
        return 0

    # Make sure that numbers are all numbers or data frames. (Note that in
    # data frames text and empty cells are allowed and ignored.)
    for number in numbers:
        if not is_number(number) and not xl.is_range(number):
            return xl.ExcelError('#VALUE', f"{number} is not a number.")

    return min(xl.flatten(numbers))
