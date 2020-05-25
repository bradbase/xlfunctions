from . import xl


@xl.register()
def AND(*logicals):
    """Determine if all conditions in a test are TRUE

    https://support.office.com/en-us/article/
        and-function-5f19b2e8-e1df-4408-897a-ce285a19e9d9
    """
    if not logicals:
        return xl.NullExcelError('logical1 is required')

    return all([
        bool(logical)
        for logical in xl.flatten(logicals)
        if not xl.is_empty(logical)
    ])


@xl.register()
def OR(*logicals):
    """Determine if any conditions in a test are TRUE.

    https://support.office.com/en-us/article/
        or-function-7d17ad14-8700-4281-b308-00b131e22af0
    """
    if not logicals:
        return xl.NullExcelError('logical1 is required')

    return any([
        bool(logical)
        for logical in xl.flatten(logicals)
        if not xl.is_empty(logical)
    ])


@xl.register()
def IF(logical_test, value_if_true, value_if_false=None):
    """Return one value if a condition is true and another value if it's false.

    https://support.office.com/en-us/article/
        if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2
    """
    return value_if_true if logical_test else value_if_false
