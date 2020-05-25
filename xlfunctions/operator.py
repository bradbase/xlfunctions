from typing import Optional

from . import xl

@xl.register()
@xl.validate_args
def OP_MUL(left: xl.Number, right: xl.Number):
    return left * right


@xl.register()
@xl.validate_args
def OP_DIV(left: xl.Number, right: xl.Number):
    if right == 0:
        return xl.DivZeroExcelError()
    return left / right


@xl.register()
@xl.validate_args
def OP_ADD(left: xl.Number, right: xl.Number):
    return left + right


@xl.register()
@xl.validate_args
def OP_SUB(left: xl.Number, right: xl.Number):
    return left - right


@xl.register()
def OP_EQ(left, right):
    return left == right


@xl.register()
def OP_NE(left, right):
    return left != right


@xl.register()
@xl.validate_args
def OP_GT(left: Optional[xl.Number], right: Optional[xl.Number]):
    if left is None or right is None:
        return False
    return left > right


@xl.register()
@xl.validate_args
def OP_LT(left: Optional[xl.Number], right: Optional[xl.Number]):
    if left is None or right is None:
        return False
    return left < right


@xl.register()
@xl.validate_args
def OP_GE(left: Optional[xl.Number], right: Optional[xl.Number]):
    if left is None or right is None:
        return False
    return left >= right


@xl.register()
@xl.validate_args
def OP_LE(left: Optional[xl.Number], right: Optional[xl.Number]):
    if left is None or right is None:
        return False
    return left <= right


@xl.register()
@xl.validate_args
def OP_NEG(right: xl.Number):
    return -1 * right


@xl.register()
@xl.validate_args
def OP_PERCENT(left: xl.Number):
    return left * 0.01
