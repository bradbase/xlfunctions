
# Excel reference: https://support.office.com/en-us/article/min-function-61635d12-920f-4ce2-a70f-96f202dcc152

import unittest

import pandas as pd

from xlfunctions import xMin


class TestMin(unittest.TestCase):

    def test_min(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        xsum_result_00 = xMin.xmin(range_00)
        result_00 = 1
        self.assertEqual(result_00, xsum_result_00)
