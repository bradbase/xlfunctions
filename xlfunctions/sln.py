
# Excel reference: https://support.office.com/en-us/article/SLN-function-cdb666e5-c1c6-40a7-806a-e695edc2f1c8

from .excel_lib import BaseFunction


class SLN(BaseFunction):
    """"""

    @staticmethod
    def sln(cost, salvage, life):
        """"""

        if isinstance(cost, (int, float)) and isinstance(salvage, (int, float)) and isinstance(life, (int, float)):
            return (cost - salvage) / life
