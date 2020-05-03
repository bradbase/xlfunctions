# Excel reference: https://support.office.com/en-us/article/right-rightb-functions-240267ee-9afa-4639-a02b-f19e1786cf2f

import unittest

from xlfunctions import Right


class TestRight(unittest.TestCase):

    def test_right(self):
        self.assertEqual(Right.right("Sale Price", 5), "Price")
        self.assertEqual(Right.right("Stock Number"), "r")
