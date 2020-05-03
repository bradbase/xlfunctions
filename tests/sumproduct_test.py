
# Excel reference: https://support.office.com/en-us/article/sumproduct-function-16753e75-9f68-4874-94ac-4d2145a2fd2e

import unittest

import pandas as pd

from xlfunctions import Sumproduct
from xlfunctions.exceptions import ExcelError


class TestSumProduct(unittest.TestCase):

    def test_ranges_with_different_sizes(self):
        range1 = pd.DataFrame([[1], [10], [3]])
        range2 = pd.DataFrame([[3], [3], [1], [2]])

        self.assertIsInstance(Sumproduct.sumproduct(range1, range2), ExcelError )


    def test_regular(self):
        range1 = pd.DataFrame([[1], [10], [3]])
        range2 = pd.DataFrame([[3], [1], [2]])

        self.assertEqual(Sumproduct.sumproduct(range1, range2), 19)
