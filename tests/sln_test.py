
# Excel reference: https://support.office.com/en-us/article/sln-function-cdb666e5-c1c6-40a7-806a-e695edc2f1c8

import unittest

from xlfunctions import SLN


class TestSLN(unittest.TestCase):

    def test_sln(self):
        sln_result_00 = SLN.sln(30000, 7500, 10)
        result_00 = 2250
        self.assertEqual(result_00, sln_result_00)
