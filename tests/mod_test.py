
# Excel reference: https://support.office.com/en-us/article/MOD-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3

import unittest

from xlfunctions import Mod
from xlfunctions.exceptions import ExcelError


class TestMod(unittest.TestCase):

    def test_first_argument_validity(self):
        self.assertIsInstance(Mod.mod(2.2, 1), ExcelError )


    def test_second_argument_validity(self):
        self.assertIsInstance(Mod.mod(2, 1.1), ExcelError )


    def test_output_value(self):
        self.assertEqual(Mod.mod(10, 4), 2)
