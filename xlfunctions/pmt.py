
# Excel reference: https://support.office.com/en-us/article/PMT-function-0214da64-9a63-4996-bc20-214433fa6441


from numpy import power
from numpy_financial import pmt as nppmt

from .excel_lib import BaseFunction

class PMT(BaseFunction):
    """"""

    @staticmethod
    def pmt(rate, nper, present_value, fv=None, type=0):
        """"""

        # WARNING fv & type not used yet - both are assumed to be their defaults (0)
        # fv = args[3]
        # type = args[4]

        if PMT.COMPATIBILITY == 'PYTHON':
            when = 'end'
            if type != 0:
                when = 'begin'
            return nppmt(rate, nper, present_value, fv=0, when=when)

        else:
            # return -present_value * rate / (1 - power(1 + rate, -nper))
            return nppmt(rate, nper, present_value, fv=0, when='end')
