from . import xl, xlerrors, xltypes


@xl.register()
@xl.validate_args
def OP_MUL(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlNumber:
    return left * right


@xl.register()
@xl.validate_args
def OP_DIV(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlNumber:
    if right == 0:
        raise xlerrors.DivZeroExcelError()
    return left / right


@xl.register()
@xl.validate_args
def OP_ADD(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlNumber:
    return left + right


@xl.register()
@xl.validate_args
def OP_SUB(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlNumber:
    return left - right


@xl.register()
def OP_EQ(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    return left == right


@xl.register()
def OP_NE(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    return left != right


@xl.register()
@xl.validate_args
def OP_GT(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    if isinstance(left, xltypes.Blank) or isinstance(right, xltypes.Blank):
        return False
    return left > right


@xl.register()
@xl.validate_args
def OP_LT(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    if isinstance(left, xltypes.Blank) or isinstance(right, xltypes.Blank):
        return False
    return left < right


@xl.register()
@xl.validate_args
def OP_GE(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    if isinstance(left, xltypes.Blank) or isinstance(right, xltypes.Blank):
        return False
    return left >= right


@xl.register()
@xl.validate_args
def OP_LE(
        left: xltypes.XlAnything,
        right: xltypes.XlAnything
) -> xltypes.XlBoolean:
    if isinstance(left, xltypes.Blank) or isinstance(right, xltypes.Blank):
        return False
    return left <= right


@xl.register()
@xl.validate_args
def OP_NEG(
        right: xltypes.XlNumber
) -> xltypes.XlNumber:
    return -1 * right


@xl.register()
@xl.validate_args
def OP_PERCENT(
        left: xltypes.XlNumber
) -> xltypes.XlNumber:
    return left * 0.01
