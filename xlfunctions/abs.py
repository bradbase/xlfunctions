
# Excel reference: https://support.office.com/en-us/article/AVERAGE-function-047bac88-d466-426c-a32b-8f33eb960cf6

import logging
import itertools

from .excel_lib import BaseFunction


class xAbs(BaseFunction):
    """Find the average (mean) of provided values."""

    @staticmethod
    def xabs(value):
        """Find the absolute value of provided value."""

        if isinstance(value, (int, float)):
            return abs(value)

        else:
            return ExcelError("#VALUE!", "value {} must be an int or float. You provided {}".format( value, type(value)) )
