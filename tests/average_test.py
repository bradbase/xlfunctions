
# Excel reference: https://support.office.com/en-us/article/AVERAGE-function-047bac88-d466-426c-a32b-8f33eb960cf6

import unittest

from openpyxl import load_workbook
import pandas as pd

from xlfunctions import Average


class TestAverage(unittest.TestCase):

    def test_average_dataframe(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        average_result_00 = Average.average(range_00)
        result_00 = 2.5
        self.assertEqual(result_00, average_result_00)


    def test_average_numbers(self):
        average_result_00 = Average.average(1, 2.0, 3, 4.0)
        result_00 = 2.5
        self.assertEqual(result_00, average_result_00)


    def test_average_mixed(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        average_result_00 = Average.average(range_00, 1, 2, 3, 4)
        result_00 = 2.5
        self.assertEqual(result_00, average_result_00)
