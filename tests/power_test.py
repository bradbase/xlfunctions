
# Excel reference: https://support.office.com/en-us/article/power-function-d3f2908b-56f4-4c3f-895a-07fb519c362a

import unittest

from xlfunctions import Power
from xlfunctions.exceptions import ExcelError

from .xlfunctions_test import xlfunctionsTestCase


class TestPower(xlfunctionsTestCase):

    def test_first_argument_validity(self):
        self.assertEqual( 1, Power.power(-1, 2) )


    def test_second_argument_validity(self):
        self.assertEqual( 1, Power.power(1, 0) )


    def test_integers(self):
        self.assertEqual(Power.power(5, 2), 25)


    def test_floats(self):
        self.assertEqual(Power.power(98.6, 3.2), 2401077.2220695773)


    def test_fractions(self):
        self.assertEqual(Power.power(4,5/4), 5.656854249492381)
