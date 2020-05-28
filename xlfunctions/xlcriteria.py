import re

from . import operator, xlerrors, xltypes

CRITERIA_REGEX = r'(\W*)(.*)'

CRITERIA_OPERATORS = {
    '<': operator.OP_LT,
    '<=': operator.OP_LE,
    '=': operator.OP_EQ,
    '<>': operator.OP_NE,
    '>=': operator.OP_GE,
    '>': operator.OP_GT,
}


def parse_criteria(criteria):

    if isinstance(criteria, (str, xltypes.Text)):
        search = re.search(CRITERIA_REGEX, str(criteria)).group
        str_operator, str_value = search(1), search(2)

        operator = CRITERIA_OPERATORS.get(str_operator)
        if operator is None:
            operator = CRITERIA_OPERATORS['=']
            str_value = criteria

        value = str_value
        for XlType in (xltypes.Number, xltypes.DateTime, xltypes.Boolean):
            try:
                value = XlType.cast(str_value)
            except xlerrors.ValueExcelError:
                pass
            else:
                break

        def check(probe):
            return operator(probe, value)

        return check

    criteria = xltypes.ExcelType.cast_from_native(criteria)

    # No support for arrays right now.
    if isinstance(criteria, xltypes.Array):
        raise xlerrors.ValueExcelError('Array criteria not supported.')

    def check(x):
        return x == criteria

    return check
