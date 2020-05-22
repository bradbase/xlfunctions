import datetime
import pandas

COMPATIBILITY = 'EXCEL'
EXCEL_EPOCH = datetime.date(1900, 1, 1)
CELL_CHARACTER_LIMIT = 32767

NUMBER_TYPES = (int, float)

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
        self.value = value
        self.info = info

    def __str__(self):
        return self.value


class SpecificExcelError(ExcelError):
    value = None

    def __init__(self, info=None):
        self.info = info


class NullError(SpecificExcelError):
    value = ERROR_CODE_NULL


class DivZeroError(SpecificExcelError):
    value = ERROR_CODE_DIV_ZERO


class ValueError(SpecificExcelError):
    value = ERROR_CODE_VALUE


class RefError(SpecificExcelError):
    value = ERROR_CODE_REF


class NameError(SpecificExcelError):
    value = ERROR_CODE_NAME


class NumError(SpecificExcelError):
    value = ERROR_CODE_NUM


class NaError(SpecificExcelError):
    value = ERROR_CODE_NA


class Functions(dict):

    def register(self, func, name=None):
        if name is None:
            name = func.__name__
        self[name] = func

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


FUNCTIONS = Functions()


def register(name=None):
    """Decorator to register a function."""

    def registerFunction(func):
        FUNCTIONS.register(func, name)
        return func

    return registerFunction


def is_number(value):
    """Determines if a value is a number."""
    return isinstance(value, NUMBER_TYPES)


def is_range(value):
    """Determines if a value is a number."""
    return isinstance(value, (pandas.DataFrame, list))


def is_empty(value):
    """Determines if a value is a number."""
    return value in [None, '']


def flatten(values):
    """Fully recursive flattening."""
    flat = []
    if isinstance(values, pandas.DataFrame):
        values = values.values.tolist()
    for value in values:
        if isinstance(value, pandas.DataFrame):
            flat.extend(flatten(value.values.tolist()))
        elif isinstance(value, (list, tuple)):
            flat.extend(flatten(value))
        else:
            flat.append(value)
    return flat


def length(values):
    return len(flatten(values))
