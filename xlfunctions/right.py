
from .excel_lib import BaseFunction
from .exceptions import ExcelError


class Right(BaseFunction):
    """"""

    @staticmethod
    def right(text, number_of_chars = 1):
        """"""

        if not isinstance(number_of_chars, int):
            return ExcelError("#VALUE!", "RIGHT function number of cars must be int, you've given me {}".format( type(number_of_chars) ))

        text = str(text)

        return text[-number_of_chars:]
