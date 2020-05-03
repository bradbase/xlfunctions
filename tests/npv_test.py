
# Excel reference: https://support.office.com/en-us/article/npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568

import unittest

import pandas as pd

from xlfunctions import NPV
from xlfunctions.exceptions import ExcelError

from .xlfunctions_test import xlfunctionsTestCase


class TestNPV(xlfunctionsTestCase):

    def test_npv_basic(self):
        range_00 = pd.DataFrame([[1, 2, 3]])
        self.assertEqual(round(NPV.npv(0.06, range_00), 7), 5.2422470)
        self.assertEqual(round(NPV.npv(0.06, 1, 2, 3), 7), 5.2422470)
        self.assertEqual(round(NPV.npv(0.06, 1), 7), 0.9433962)

        self.assertEqual(round(NPV.npv(0.1, -10000, 3000, 4200, 6800), 2), 1188.44)

        range_01 = pd.DataFrame([[8000, 9200, 10000, 12000, 14500]])
        self.assertEqual(round(NPV.npv(0.08, range_01) + -40000, 2), 1922.06)
        self.assertEqual(round(NPV.npv(0.08, range_01, -9000) + -40000, 2), -3749.47)
