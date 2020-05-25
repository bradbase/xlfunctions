import datetime
import functools
import inspect
import operator
import pandas
import re
import typing

COMPATIBILITY = 'EXCEL'
EXCEL_EPOCH = datetime.date(1900, 1, 1)
CELL_CHARACTER_LIMIT = 32767

# Alias to make code more readable.
RangeData = pandas.DataFrame

INTEGER_TYPES = (int,)
NUMBER_TYPES = INTEGER_TYPES + (float,)
RANGE_TYPES = (list, RangeData)
TEXT_TYPES = (str,)

Integer = typing.NewType('Integer', typing.Union[INTEGER_TYPES])
Number = typing.NewType('Number', typing.Union[NUMBER_TYPES])
Range = typing.NewType('Range', typing.Union[RANGE_TYPES])
Text = typing.NewType('Text', typing.Union[TEXT_TYPES])

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

CRITERIA_REGEX = '(\W*)(.*)'

CRITERIA_OPERATORS = {
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '<>': operator.ne,
    '>=': operator.ge,
    '>': operator.gt,
}


class ExcelError(Exception):

    def __init__(self, value, info=None):
        super().__init__(info)
        self.value = value
        self.info = info

    def _safe_value_str(self, value):
        try:
            return str(value)
        except:
            return '<unprintable>'

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


class NumberExcelError(ValueExcelError):

    def __init__(self, value, name='value'):
        self.value = value
        vtype = type(value).__name__
        value = self._safe_value_str(value)
        super().__init__(
            f'`{name}` "{value}" must be an int or float. Got: {vtype}')


class IntegerExcelError(ValueExcelError):

    def __init__(self, value, name='value'):
        self.value = value
        vtype = type(value).__name__
        value = self._safe_value_str(value)
        super().__init__(f'`{name}` "{value}" must be an int. Got: {vtype}')


class TextExcelError(ValueExcelError):

    def __init__(self, value, name='value'):
        self.value = value
        vtype = type(value).__name__
        value = self._safe_value_str(value)
        super().__init__(f'`{name}` "{value}" must be text. Got: {vtype}')


class RangeExcelError(ValueExcelError):

    def __init__(self, value, name='value'):
        self.value = value
        vtype = type(value).__name__
        value = self._safe_value_str(value)
        super().__init__(f'`{name}` "{value}" must be a range. Got: {vtype}')


class EmptyExcelError(ValueExcelError):

    def __init__(self, value, name='value'):
        self.value = value
        vtype = type(value).__name__
        value = self._safe_value_str(value)
        super().__init__(f'`{name}` "{value}" must be None or "". Got: {vtype}')


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


def is_integer(value):
    """Determines if a value is a number."""
    return isinstance(value, INTEGER_TYPES)


def is_number(value):
    """Determines if a value is a number."""
    return isinstance(value, NUMBER_TYPES)


def is_text(value):
    """Determines if a value is text."""
    return isinstance(value, TEXT_TYPES)


def is_range(value):
    """Determines if a value is a number."""
    return isinstance(value, RANGE_TYPES)


def is_empty(value):
    """Determines if a value is a number."""
    return value in [None, '']


def is_criteria(value):
    """Determines whether the value is a proper criteria."""
    # A criterium could be anything that can present a simple truthy value.
    return not is_range(value)


def is_error(value):
    """Determines if a value is an Excel error."""
    return isinstance(value, ExcelError)


def convert_integer(value, name=None):
    if is_integer(value):
        return value
    try:
        return int(float(value))
    except (ValueError, TypeError):
        raise IntegerExcelError(value, name)


def convert_number(value, name=None):
    if is_number(value):
        return value
    for type in NUMBER_TYPES:
        try:
            return type(value)
        except (ValueError, TypeError):
            pass
    raise NumberExcelError(value, name)


def convert_range(value, name=None):
    if not is_range(value):
        raise RangeExcelError(value, name)
    return value


def convert_text(value, name=None):
    try:
        return str(value)
    except (ValueError, TypeError):
        raise TextExcelError(value, name)

def convert_empty(value, name=None):
    if not is_empty(value):
        raise EmptyExcelError(value, name)
    return None


TYPE_TO_COVERTER = {
    Integer: convert_integer,
    Number: convert_number,
    Range: convert_range,
    Text: convert_text,
}


def _validate(vtype, val, name):
    converter = TYPE_TO_COVERTER.get(vtype, None)
    if converter is not None:
        return converter(val, name)

    # Support lists with value types
    if getattr(vtype, '__origin__', None) == list:
        return [_validate(vtype.__args__[0], item, name) for item in val]

    # Support unions
    if getattr(vtype, '__origin__', None) == typing.Union:
        for stype in vtype.__args__:
            try:
                return _validate(stype, val, name)
            except ExcelError:
                pass
        raise ValueExcelError(val)

    return val


def validate_args(func):

    @functools.wraps(func)
    def validate(*args, **kw):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kw)
        for pname, value in list(bound.arguments.items()):
            try:
                bound.arguments[pname] = _validate(
                    sig.parameters[pname].annotation, value, pname)
            except ExcelError as err:
                return err
        return func(*bound.args, **bound.kwargs)

    return validate


def flatten(values):
    """Fully recursive flattening."""
    flat = []
    if isinstance(values, RangeData):
        values = values.values.tolist()
    for value in values:
        if isinstance(value, RangeData):
            flat.extend(flatten(value.values.tolist()))
        elif isinstance(value, (list, tuple)):
            flat.extend(flatten(value))
        else:
            flat.append(value)
    return flat


def length(values):
    return len(flatten(values))


def parse_criteria(criteria):

    if is_number(criteria):
        def check(x):
            return x == criteria

    elif isinstance(criteria, str):
        search = re.search(CRITERIA_REGEX, criteria).group
        str_operator, str_value = search(1), search(2)

        operator = CRITERIA_OPERATORS.get(str_operator)
        if operator is None:
            operator = CRITERIA_OPERATORS['=']
            str_value = criteria

        try:
            value = convert_number(str_value)
        except ValueExcelError:
            value = str_value

        def check(probe):
            return operator(probe, value)

    else:
        def check(x):
            return False

    return check
