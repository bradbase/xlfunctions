""""Excel Function Implementation

Full list of all functions:

https://support.office.com/en-us/article/
    excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188
"""

name = "xlfunctions"

from .xl import FUNCTIONS, ExcelError, register

# Make sure to register all functions
from . import date, financial, logical, lookup, math, operator, statistics, text
