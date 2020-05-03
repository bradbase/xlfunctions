
# Excel reference: https://support.office.com/en-us/article/max-function-e0012414-9ac8-4b34-9a47-73e662c08098

import unittest

import pandas as pd

from xlfunctions import xMax


class TestMax(unittest.TestCase):

    def test_max(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        xsum_result_00 = xMax.xmax(range_00)
        result_00 = 4
        self.assertEqual(result_00, xsum_result_00)
