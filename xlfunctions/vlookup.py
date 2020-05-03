
# https://support.office.com/en-us/article/VLOOKUP-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1

from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError

class VLookup(BaseFunction):
    """"""

    @staticmethod
    def vlookup(lookup_value, table_array, col_index_num, range_lookup=False):
        """"""

        if range_lookup:
            raise NotImplementedError("Excact match only supported at the moment.")

        if col_index_num > len(table_array):
            return ExcelError('#VALUE', 'col_index_num is greater than the number of cols in table_array')

        table_array = table_array.set_index(0)

        if not range_lookup:
            if lookup_value not in table_array.index:
                return ExcelError('#N/A', 'lookup_value not in first column of table_array')

            else:
                return table_array.loc[lookup_value].values[0]
