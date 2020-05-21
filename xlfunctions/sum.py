
# Excel reference: https://support.office.com/en-us/article/SUM-function-043e1c7d-7726-4e80-8f32-07b23e057f89

from pandas import DataFrame

from .excel_lib import BaseFunction

class xSum(BaseFunction):
    """Sum all provided values."""

    @staticmethod
    def xsum(*args):
        """Sum all provided values."""

        # however, if no non numeric cells, return zero (is what excel does)
        if len(args) < 1:
            return 0

        else:
            sum_list = []
            for arg in args:
                if not isinstance(arg, (int, float, DataFrame)):
                    raise NotImplementedError("An argument you've supplied is of type {} but needs to be one of int, float or DataFrame".format(type(arg)))

                if isinstance(arg, (int, float)):
                    sum_list.append(arg)

                else:
                    sum_list += [item for item in xSum.flatten(arg) if isinstance(item, (int, float))]

            return sum(sum_list)

        
