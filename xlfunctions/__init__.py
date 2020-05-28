""""Excel Function Implementation

Full list of all functions:

https://support.office.com/en-us/article/
    excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188
"""
from .xl import FUNCTIONS, register  # noqa: F401
from .xlerrors import *  # noqa: F401, F403
from .xltypes import *  # noqa: F401, F403

# Make sure to register all functions
from . import (  # noqa: F401
    date,
    financial,
    logical,
    lookup,
    math,
    operator,
    statistics,
    text
)

name = "xlfunctions"
