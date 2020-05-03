
# Excel reference: https://support.office.com/en-us/article/sum-function-043e1c7d-7726-4e80-8f32-07b23e057f89

import unittest

import pandas as pd

from xlfunctions import xSum


class TestSum(unittest.TestCase):

    def test_sum_dataframe(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        xsum_result_00 = xSum.xsum(range_00)
        result_00 = 10
        self.assertEqual(result_00, xsum_result_00)


    def test_sum_numbers(self):
        xsum_result_00 = xSum.xsum(1, 2.0, 3, 4.0)
        result_00 = 10
        self.assertEqual(result_00, xsum_result_00)


    def test_sum_numbers(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        xsum_result_00 = xSum.xsum(range_00, 1, 2.0, 3, 4.0)
        result_00 = 20
        self.assertEqual(result_00, xsum_result_00)
