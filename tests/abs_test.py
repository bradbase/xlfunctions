
# Excel reference: https://support.office.com/en-us/article/abs-function-3420200f-5628-4e8c-99da-c99d7c87713c

import unittest

from xlfunctions import xAbs


class TestABS(unittest.TestCase):

    def test_abs(self):
        abs_result_00 = xAbs.xabs(-4)
        result_00 = 4
        self.assertEqual(result_00, abs_result_00)
