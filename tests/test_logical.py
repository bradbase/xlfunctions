import unittest
from xlfunctions import xl, logical


class LogicalModuleTest(unittest.TestCase):

    def test_AND(self):
        self.assertEqual(logical.AND(3, True, None), True)
        self.assertEqual(logical.AND(True, 0), False)

    def test_AND_without_any_args(self):
        self.assertIsInstance(logical.AND(), xl.NullExcelError)

    def test_OR(self):
        self.assertEqual(logical.OR(3, True, None), True)
        self.assertEqual(logical.OR(False, 0), False)

    def test_OR_without_any_args(self):
        self.assertIsInstance(logical.OR(), xl.NullExcelError)

    def test_IF(self):
        self.assertEqual(logical.IF(True, 1, 2), 1)
        self.assertEqual(logical.IF(False, 1, 2), 2)
