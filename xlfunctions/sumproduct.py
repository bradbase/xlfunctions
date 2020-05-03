
# Excel reference: https://support.office.com/en-us/article/SUMPRODUCT-function-16753e75-9f68-4874-94ac-4d2145a2fd2e

from functools import reduce

from pandas import concat
from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError

class Sumproduct(BaseFunction):
    """"""

    @staticmethod
    def sumproduct(range_1, *ranges):
        """"""

        if not isinstance(range_1, (int, float, DataFrame)):
            raise NotImplementedError("Argument for range_1 is of type {} but needs to be one of int, float or DataFrame".format(type(range_1)))

        range_length = len(range_1)

        for range in ranges: # if a range has no values (i.e if it's empty)
            if not isinstance(range, (int, float, DataFrame)):
                raise NotImplementedError("An argument you've supplied is of type {} but needs to be one of int, float or DataFrame".format(type(range)))

            this_range_len = len(range)
            if range_length != this_range_len:
                return ExcelError("#VALUE!", "The length of the ranges does not match. Looking for {} and you've given me a range of length {}".format(range_length, this_range_len))

            if this_range_len == 0:
                return 0

        sumproduct_ranges = [range_1]
        for range in ranges:
            for item in range:
                # If there is an ExcelError inside a Range, sumproduct should output an ExcelError
                if isinstance(item, ExcelError):
                    return ExcelError("#N/A", "ExcelErrors are present in the sumproduct items")

            sumproduct_ranges.append(range)

        sumproduct = concat(sumproduct_ranges, axis=1)

        return sumproduct.prod(axis=1).sum()
