name = "xlfunctions"

from .xl import FUNCTIONS, ExcelError

# Make sure to register all functions
from . import date, financial, lookup, math, statistics, text
