import datetime
import mock
import pandas
import unittest

from xlfunctions import xl, date


class DateModuleTest(unittest.TestCase):

    def test_DATE(self):
        self.assertEqual(date.DATE(2000, 1, 1), 36526)
        self.assertEqual(date.DATE(2008, 11, 3), 39755)
        self.assertEqual(date.DATE(2024, 1, 1), 45292)
        self.assertEqual(date.DATE(2025, 1, 1), 45658)
        self.assertEqual(date.DATE(2026, 1, 1), 46023)

    def test_DATE_with_short_year(self):
        self.assertEqual(date.DATE(99, 1, 1), date.DATE(1999, 1, 1))

    def test_DATE_with_string_components(self):
        self.assertEqual(date.DATE('2026', '1', '1'), 46023)

    def test_DATE_year_must_be_integer(self):
        self.assertIsInstance(date.DATE('bad', 1, 1), xl.IntegerExcelError)

    def test_DATE_month_must_be_integer(self):
        self.assertIsInstance(date.DATE(2000, 'bad', 1), xl.IntegerExcelError)

    def test_DATE_day_must_be_integer(self):
        self.assertIsInstance(date.DATE(2000, 1, 'bad'), xl.IntegerExcelError)

    def test_DATE_year_must_be_positive(self):
        self.assertIsInstance(date.DATE(-1, 1, 1), xl.NumExcelError)

    def test_DATE_year_must_have_less_than_10000(self):
        self.assertIsInstance(date.DATE(10000, 1, 1), xl.NumExcelError)

    def test_DATE_result_must_be_positive(self):
        self.assertIsInstance(date.DATE(1900, 1, -1), xl.NumExcelError)

    def test_DATE_not_stricly_positive_month_substracts(self):
        self.assertEqual(date.DATE(2009, -1, 1), date.DATE(2008, 11, 1))

    def test_DATE_not_stricly_positive_day_substracts(self):
        self.assertEqual(date.DATE(2009, 1, -1), date.DATE(2008, 12, 30))

    def test_DATE_month_superior_to_12_change_year(self):
        self.assertEqual(date.DATE(2009, 14, 1), date.DATE(2010, 2, 1))

    def test_DATE_day_superior_to_365_change_year(self):
        self.assertEqual(date.DATE(2009, 1, 400), date.DATE(2010, 2, 4))

    def test_DATE_year_for_29_feb(self):
        self.assertEqual(date.DATE(2008, 2, 29), 39507)

    def test_TODAY(self):
        with mock.patch.object(
                date, 'today', lambda: datetime.date(2000, 1, 1)):
            self.assertEqual(date.TODAY(), 36526)

    def test_YEARFRAC_start_date_must_be_number(self):
        self.assertIsInstance(date.YEARFRAC('bad', 1), xl.NumberExcelError)

    def test_YEARFRAC_end_date_must_be_number(self):
        self.assertIsInstance(date.YEARFRAC(1, 'bad'), xl.NumberExcelError)

    def test_YEARFRAC_start_date_must_be_positive(self):
        self.assertIsInstance(date.YEARFRAC(-1, 0), xl.ValueExcelError)

    def test_YEARFRAC_end_date_must_be_positive(self):
        self.assertIsInstance(date.YEARFRAC(0, -1), xl.ValueExcelError)

    def test_YEARFRAC_basis_must_be_between_0_and_4(self):
        self.assertIsInstance(date.YEARFRAC(1, 2, 5), xl.ValueExcelError)
        self.assertIsInstance(date.YEARFRAC(1, 2, -1), xl.ValueExcelError)

    def test_YEARFRAC_yearfrac_basis_0(self):
        # From Excel docs.
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2012, 1, 1), date.DATE(2012, 7, 30), 0),
            0.58055556)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20)),
            7.30277777777778)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20), 0),
            7.30277777777778)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2024, 1, 1), date.DATE(2025, 1, 1), 0), 1)

    def test_YEARFRAC_yearfrac_basis_1(self):
        # From Excel docs.
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2012, 1, 1), date.DATE(2012, 7, 30), 1),
            0.57650273)

    def test_YEARFRAC_yearfrac_basis_2(self):
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20), 2),
            7.405555556)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2024, 1, 1), date.DATE(2025, 1, 1), 2),
            1.01666666666667)

    def test_YEARFRAC_yearfrac_basis_3(self):
        # From Excel docs.
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2012, 1, 1), date.DATE(2012, 7, 30), 3),
            0.57808219)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20), 3),
            7.304109589)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2024, 1, 1), date.DATE(2025, 1, 1), 3),
            1.0027397260274)

    def test_YEARFRAC_yearfrac_basis_4(self):
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20), 4),
            7.302777778)
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2024, 1, 1), date.DATE(2025, 1, 1), 4), 1)

    def test_YEARFRAC_yearfrac_inverted(self):
        self.assertAlmostEqual(
            date.YEARFRAC(date.DATE(2015, 4, 20), date.DATE(2008, 1, 1)),
            date.YEARFRAC(date.DATE(2008, 1, 1), date.DATE(2015, 4, 20)))
