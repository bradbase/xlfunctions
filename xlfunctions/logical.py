from typing import Tuple
from . import xl


@xl.register()
@xl.validate_args
def AND(*logicals: Tuple[xl.Expr]):
    """Determine if all conditions in a test are TRUE

    https://support.office.com/en-us/article/
        and-function-5f19b2e8-e1df-4408-897a-ce285a19e9d9
    """
    if not logicals:
        return xl.NullExcelError('logical1 is required')

    # Use delayed evaluation to minimize th amount of valaues to evaluate.
    for logical in logicals:
        val = logical()
        for item in xl.flatten([val]):
            if xl.is_empty(item):
                continue
            if not bool(item):
                return False

    return True


@xl.register()
@xl.validate_args
def OR(*logicals: Tuple[xl.Expr]):
    """Determine if any conditions in a test are TRUE.

    https://support.office.com/en-us/article/
        or-function-7d17ad14-8700-4281-b308-00b131e22af0
    """
    if not logicals:
        return xl.NullExcelError('logical1 is required')

    # Use delayed evaluation to minimize th amount of valaues to evaluate.
    for logical in logicals:
        val = logical()
        for item in xl.flatten([val]):
            if xl.is_empty(item):
                continue
            if bool(item):
                return True

    return False


@xl.register()
@xl.validate_args
def IF(
        logical_test: xl.Expr,
        value_if_true: xl.Expr,
        value_if_false: xl.Expr = None
):
    """Return one value if a condition is true and another value if it's false.

    https://support.office.com/en-us/article/
        if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2
    """
    # Use delayed evaluation to only evaluate the true or false value but not
    # both.
    return value_if_true() if logical_test() else value_if_false()
