
ERROR_CODE_NULL = '#NULL!'
ERROR_CODE_DIV_ZERO = "#DIV/0!"
ERROR_CODE_VALUE = "#VALUE!"
ERROR_CODE_REF = "#REF!"
ERROR_CODE_NAME = "#NAME?"
ERROR_CODE_NUM = "#NUM!"
ERROR_CODE_NA = "#N/A"

ERROR_CODES = (
    ERROR_CODE_NULL,
    ERROR_CODE_DIV_ZERO,
    ERROR_CODE_VALUE,
    ERROR_CODE_REF,
    ERROR_CODE_NAME,
    ERROR_CODE_NUM,
    ERROR_CODE_NA,
)


class ExcelError(Exception):

    def __init__(self, value, info=None):
        super().__init__(info)
        self.value = value
        self.info = info

    @classmethod
    def is_error(cls, value):
        return isinstance(value, cls)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        return id(self) == id(other)


class SpecificExcelError(ExcelError):
    value = None

    def __init__(self, info=None):
        super().__init__(self.value, info)


class NullExcelError(SpecificExcelError):
    value = ERROR_CODE_NULL


class DivZeroExcelError(SpecificExcelError):
    value = ERROR_CODE_DIV_ZERO


class ValueExcelError(SpecificExcelError):
    value = ERROR_CODE_VALUE


class RefExcelError(SpecificExcelError):
    value = ERROR_CODE_REF


class NameExcelError(SpecificExcelError):
    value = ERROR_CODE_NAME


class NumExcelError(SpecificExcelError):
    value = ERROR_CODE_NUM


class NaExcelError(SpecificExcelError):
    value = ERROR_CODE_NA
