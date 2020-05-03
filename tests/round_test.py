
# Excel reference: https://support.office.com/en-us/article/round-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c

import unittest

from xlfunctions import xRound
from xlfunctions.exceptions import ExcelError


class Test_Round(unittest.TestCase):

    def test_nb_must_be_number(self):
        self.assertIsInstance(xRound.xround('er', 1), ExcelError )


    def test_nb_digits_must_be_number(self):
        self.assertIsInstance(xRound.xround(2.323, 'ze'), ExcelError )


    def test_positive_number_of_digits(self):
        self.assertEqual(xRound.xround(2.675, 2), 2.68)


    def test_negative_number_of_digits(self):
        self.assertEqual(xRound.xround(2352.67, -2), 2400)


    def test_round(self):
        self.assertEqual(xRound.xround(2.15, 1), 2.2)
        self.assertEqual(xRound.xround(2.149, 1), 2.1)
        self.assertEqual(xRound.xround(-1.475, 2), -1.48)
        self.assertEqual(xRound.xround(21.5, -1), 20)
        self.assertEqual(xRound.xround(626.3,-3), 1000)
        self.assertEqual(xRound.xround(1.98,-1), 0)
        self.assertEqual(xRound.xround(-50.55,-2), -100)
