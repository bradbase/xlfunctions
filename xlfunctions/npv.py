
# Excel reference: https://support.office.com/en-us/article/npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568

from pandas import DataFrame
from numpy_financial import npv as npnpv

from .excel_lib import BaseFunction

class NPV(BaseFunction):
    """"""

    @staticmethod
    def npv(discount_rate, *args):
        """"""

        if len(args) < 1:
            raise Exception("NPV needs a value_1")

        cashflow = []

        for item in args:
            if isinstance(item, DataFrame):
                cashflow.extend( NPV.flatten( item.values ) )

            elif isinstance(item, (int, float)):
                cashflow.append(item)


        if NPV.COMPATIBILITY == 'PYTHON':
            return npnpv(discount_rate, cashflow)

        else:
            return sum([float(x)*(1+discount_rate)**-(i+1) for (i, x) in enumerate(cashflow)])
