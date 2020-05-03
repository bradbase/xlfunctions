
# Excel reference: https://support.office.com/en-us/article/concat-function-9b1a9a3f-94ff-41af-9736-694cbd6b4ca2

import itertools

from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError


class Concat(BaseFunction):
    """"""

    @staticmethod
    def concat(*args):
        """The CONCAT function combines the text from multiple ranges and/or strings, but it doesn't provide delimiter or IgnoreEmpty arguments."""
        if len(args) > 254:
            return ExcelError("#VALUE!", "Can't concat more than 254 arguments. You provided {}".format( len(args) ))

        joinable = []
        for item in args:
            if isinstance(item, str):
                joinable.append(item)

            elif isinstance(item, DataFrame):
                joinable.extend( [str(item) for item in itertools.chain( *item.values.tolist() ) ] )

            elif isinstance(item, list):
                joinable.extend( list )

            elif isinstance(item, (int, float)):
                joinable.extend( str(list) )

        return ''.join(joinable)
