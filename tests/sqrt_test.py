
# Excel reference: https://support.office.com/en-us/article/sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf

import unittest

from xlfunctions import Sqrt
from xlfunctions.exceptions import ExcelError


class Test_Sqrt(unittest.TestCase):

    def test_first_argument_validity(self):
        self.assertIsInstance(Sqrt.sqrt(-16), ExcelError )


    def test_positive_integers(self):
        self.assertEqual(Sqrt.sqrt(16), 4)


    def test_float(self):
        self.assertEqual(Sqrt.sqrt(.25), .5)
