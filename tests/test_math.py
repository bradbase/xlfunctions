import datetime
import mock
import pandas
import unittest

from xlfunctions import xl, math


class DateModuleTest(unittest.TestCase):

    def test_ABS(self):
        self.assertEqual(math.ABS(3), 3)
        self.assertEqual(math.ABS('-3.4'), 3.4)

    def test_ABS_with_bad_arg(self):
        self.assertIsInstance(math.ABS('bad'), xl.NumberExcelError)

    def test_LN(self):
        self.assertEqual(math.LN(2.718281828459045), 1)

    def test_LN_with_bad_arg(self):
        self.assertIsInstance(math.LN('bad'), xl.NumberExcelError)

    def test_MOD(self):
        self.assertEqual(math.MOD(1, 2), 1)

    def test_MOD_with_float(self):
        self.assertEqual(math.MOD(1.0, 2), 1)

    def test_MOD_with_string(self):
        self.assertEqual(math.MOD('1.0', 2), 1)

    def test_MOD_with_bad_arg(self):
        self.assertIsInstance(math.MOD('bad', 2), xl.IntegerExcelError)
        self.assertIsInstance(math.MOD(1, 'bad'), xl.IntegerExcelError)

    def test_PI(self):
        self.assertEqual(math.PI(), 3.141592653589793)

    def test_POWER(self):
        self.assertEqual(math.POWER(10, 2), 100)
        self.assertEqual(math.POWER('-1', 2), 1)
        self.assertEqual(math.POWER(2.5, 2), 6.25)

    def test_POWER_with_bad_arg(self):
        self.assertIsInstance(math.POWER('bad', 2), xl.NumberExcelError)
        self.assertIsInstance(math.POWER(10, 'bad'), xl.NumberExcelError)

    def test_ROUND(self):
        self.assertEqual(math.ROUND(0.6), 1)
        self.assertEqual(math.ROUND(1.3), 1)
        self.assertEqual(math.ROUND(1.25, 1), 1.3)

    def test_ROUND_with_bad_arg(self):
        self.assertIsInstance(math.ROUND('bad'), xl.NumberExcelError)
        self.assertIsInstance(math.ROUND(1.3, 'bad'), xl.IntegerExcelError)

    def test_ROUNDUP(self):
        self.assertEqual(math.ROUNDUP(0.6), 1)
        self.assertEqual(math.ROUNDUP(1.3), 2)
        self.assertEqual(math.ROUNDUP(1.24, 1), 1.3)

    def test_ROUNDUP_with_bad_arg(self):
        self.assertIsInstance(math.ROUNDUP('bad'), xl.NumberExcelError)
        self.assertIsInstance(math.ROUNDUP(1.3, 'bad'), xl.IntegerExcelError)

    def test_ROUNDDOWN(self):
        self.assertEqual(math.ROUNDDOWN(0.6), 0)
        self.assertEqual(math.ROUNDDOWN(1.3), 1)
        self.assertEqual(math.ROUNDDOWN(1.26, 1), 1.2)

    def test_ROUNDDOWN_with_bad_arg(self):
        self.assertIsInstance(math.ROUNDDOWN('bad'), xl.NumberExcelError)
        self.assertIsInstance(math.ROUNDDOWN(1.3, 'bad'), xl.IntegerExcelError)

    def test_SQRT(self):
        self.assertEqual(math.SQRT(4), 2)
        self.assertEqual(math.SQRT(4.0), 2.0)

    def test_SQRT_with_neg_number(self):
        self.assertIsInstance(math.SQRT(-4), xl.NumExcelError)

    def test_SQRT_with_bad_arg(self):
        self.assertIsInstance(math.SQRT('bad'), xl.NumberExcelError)

    def test_SUM(self):
        self.assertEqual(math.SUM(xl.RangeData([[1, 2],[3, 4]])), 10)
        self.assertEqual(math.SUM(1, 2, 3, 4.0), 10.0)

    def test_SUM_with_nonnumbers_in_range(self):
        self.assertEqual(math.SUM(xl.RangeData([[1, 'bad'],[3, 4]])), 8)

    def test_SUM_with_bad_Arg(self):
        self.assertEqual(math.SUM('foo'), 0)

    def test_SUM_empty(self):
        self.assertEqual(math.SUM(), 0)

    def test_SUMIF(self):
        self.assertEqual(math.SUMIF([0, 1, 2], '>=1', [10, 20, 30]), 50)

    def test_SUMIF_invalid_criteria(self):
        self.assertEqual(math.SUMIF([0, 1, 2], [0, 1], [10, 20, 30]), 0)

    def test_SUMIF_unspecified_sum_range(self):
        self.assertEqual(math.SUMIF([0, 1, 2, 3], ">=2"), 5)

    def test_SUMIF_with_invlaid_sum_range(self):
        self.assertIsInstance(
            math.SUMIF([0, 1, 2, 3], ">=2", 'bad'), xl.RangeExcelError)

    def test_SUMPRODUCT(self):
        range1 = xl.RangeData([[1], [10], [3]])
        range2 = xl.RangeData([[3], [1], [2]])
        self.assertEqual(math.SUMPRODUCT(range1, range2), 19)

    def test_SUMPRODUCT_ranges_with_different_sizes(self):
        range1 = xl.RangeData([[1], [10], [3]])
        range2 = xl.RangeData([[3], [3], [1], [2]])
        self.assertIsInstance(
            math.SUMPRODUCT(range1, range2), xl.ValueExcelError)

    def test_SUMPRODUCT_with_empty_frist_range(self):
        self.assertEqual(math.SUMPRODUCT(xl.RangeData([])), 0)

    def test_SUMPRODUCT_without_any_range(self):
        self.assertIsInstance(math.SUMPRODUCT(), xl.NullExcelError)

    def test_SUMPRODUCT_ranges_with_errors(self):
        range1 = xl.RangeData([[xl.NumExcelError('err')], [10], [3]])
        range2 = xl.RangeData([[3], [3], [1]])
        self.assertIsInstance(
            math.SUMPRODUCT(range1, range2), xl.NaExcelError)

    def test_SUMPRODUCT_with_invalid_range(self):
        self.assertIsInstance(math.SUMPRODUCT(1), xl.RangeExcelError)

    def test_TRUNC(self):
        self.assertEqual(math.TRUNC(0.6), 0)
        self.assertEqual(math.TRUNC(1.3), 1)
        self.assertEqual(math.TRUNC(1.26, 1), 1.2)

    def test_TRUNC_with_bad_arg(self):
        self.assertIsInstance(math.TRUNC('bad'), xl.NumberExcelError)
        self.assertIsInstance(math.TRUNC(1.3, 'bad'), xl.IntegerExcelError)
