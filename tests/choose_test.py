
# Excel reference: https://support.office.com/en-us/article/CHOOSE-function-fc5c184f-cb62-4ec7-a46e-38653b98f5bc

import unittest

import pandas as pd

from xlfunctions import Choose


class TestChoose(unittest.TestCase):

    def test_choose(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        range_01 = pd.DataFrame([[2, 1],[3, 4]])
        range_02 = pd.DataFrame([[1, 2],[4, 3]])
        choose_result_00 = Choose.choose('2', range_00, range_01, range_02)
        result_00 = pd.DataFrame([[2, 1],[3, 4]])
        self.assertTrue(result_00.equals(choose_result_00))
