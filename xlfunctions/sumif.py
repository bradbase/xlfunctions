# Excel reference: https://support.office.com/en-us/article/SUMIF-function-169b8c99-c05c-4483-a712-1697a653039b

from pandas import DataFrame

from .excel_lib import BaseFunction

class SumIf(BaseFunction):

    @staticmethod
    def sumif(range, criteria, sum_range=None):

        # WARNING:
        # - wildcards not supported
        # - doesn't really follow 2nd remark about sum_range length

        if not isinstance(range, DataFrame):
            return TypeError('%s must be a Range' % str(range))

        # ugly...
        if isinstance(criteria, DataFrame) and not isinstance(criteria , (str, bool)):
            return 0

        indexes = SumIf.find_corresponding_index(SumIf.flatten(range.values), criteria)

        if sum_range is None:
            sum_range = range

        if not isinstance(sum_range, DataFrame):
            return TypeError('%s must be a Range' % str(sum_range))

        sum_range = SumIf.flatten(sum_range.values)
        def f(x):
            return sum_range[x] if x < len(sum_range) else 0

        return sum(map(f, indexes))
