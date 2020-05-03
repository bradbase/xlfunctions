
# Excel reference: https://support.office.com/en-us/article/roundup-function-f8bc9b23-e795-47db-8703-db171d0c42a7

import unittest

from xlfunctions import xRound
from xlfunctions.exceptions import ExcelError

class Test_Roundup(unittest.TestCase):

    def test_nb_must_be_number(self):
        self.assertIsInstance(xRound.roundup('er', 1), ExcelError )


    def test_nb_digits_must_be_number(self):
        self.assertIsInstance(xRound.roundup(2.323, 'ze'), ExcelError )


    def test_positive_number_of_digits(self):
        self.assertEqual(xRound.roundup(3.2,0), 4)


    def test_negative_number_of_digits(self):
        self.assertEqual(xRound.roundup(31415.92654, -2), 31500)


    def test_round(self):
        self.assertEqual(xRound.roundup(76.9,0), 77)
        self.assertEqual(xRound.roundup(3.14159, 3), 3.142)
        self.assertEqual(xRound.roundup(-3.14159, 1), -3.2)
