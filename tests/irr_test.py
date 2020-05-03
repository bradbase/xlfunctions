
# Excel reference: https://support.office.com/en-us/article/irr-function-64925eaa-9988-495b-b290-3ad0c163c1bc

import unittest

import pandas as pd

from xlfunctions import IRR
from xlfunctions.exceptions import ExcelError


class TestIRR(unittest.TestCase):

    def test_irr_basic(self):
        range_00 = pd.DataFrame([[-100, 39, 59, 55, 20]])
        self.assertEqual(round(IRR.irr(range_00, 0), 7), 0.2809484)


    def test_irr_with_guess_non_null(self):
        with self.assertRaises(ValueError):
            IRR.irr([-100, 39, 59, 55, 20], 2)
