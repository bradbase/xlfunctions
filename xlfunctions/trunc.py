
# Excel reference: https://support.office.com/en-us/article/trunc-function-8b86a64c-3127-43db-ba14-aa5ceb292721

import math
from .excel_lib import BaseFunction

class Trunc(BaseFunction):
    """Sum all provided values."""

    @staticmethod
    def trunc(number, num_digits=0):
        """Truncate a number to the specified number of digits."""

        if isinstance(number, (int, float)):
            # Simple case. We want to make sure to return an integer in this
            # case.
            if num_digits == 0:
                return math.trunc(number)
            return math.trunc(number * 10**num_digits) / 10**num_digits
        else:
            return ExcelError(
                '#VALUE!', '{} must be a number. You gave me a {}'.format(
                    number, type(number)))
