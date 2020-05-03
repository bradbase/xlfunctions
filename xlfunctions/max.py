
# Excel reference: https://support.office.com/en-us/article/MAX-function-e0012414-9ac8-4b34-9a47-73e662c08098

from numpy import maximum as npmaximum
from pandas import DataFrame

from .excel_lib import BaseFunction


class xMax(BaseFunction):
    """Finds the maximum of provided values."""

    @staticmethod
    def xmax(*args):
        """Finds the maximum of provided values."""
        # however, if no non numeric cells, return zero (is what excel does)
        if len(args) < 1:
            return 0

        else:
            max_list = []
            for arg in args:
                if not isinstance(arg, (int, float, DataFrame)):
                    raise NotImplementedError("An argument you've supplied is of type {} but needs to be one of int, float or DataFrame".format(type(arg)))

                if isinstance(arg, (int, float)):
                    max_list.append(arg)
                else:
                    max_list.append(arg.max().max())

            if len(max_list) == 1:
                return max_list[0]

            else:
                return npmaximum(*max_list)
