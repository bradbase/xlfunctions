import mock
import unittest

from xlfunctions import xl, date, financial


class FinancialModuleTest(unittest.TestCase):

    def test_IRR(self):
        self.assertAlmostEqual(
            financial.IRR(xl.RangeData([[-100, 39, 59, 55, 20]])), 0.2809484)

    def test_IRR_with_guess_non_null(self):
        with self.assertRaises(NotImplementedError):
            financial.IRR(xl.RangeData([[-100, 39, 59]]), 2)

    def test_NPV(self):
        self.assertAlmostEqual(
            financial.NPV(0.06, xl.RangeData([[1, 2, 3]])), 5.2422470)
        self.assertAlmostEqual(
            financial.NPV(0.06, 1, 2, 3), 5.2422470)
        self.assertAlmostEqual(
            financial.NPV(0.06, 1), 0.9433962)
        self.assertAlmostEqual(
            financial.NPV(0.1, -10000, 3000, 4200, 6800), 1188.44, 2)

        range1 = xl.RangeData([[8000, 9200, 10000, 12000, 14500]])
        self.assertAlmostEqual(
            financial.NPV(0.08, range1) + -40000, 1922.06, 2)
        self.assertAlmostEqual(
            financial.NPV(0.08, range1, -9000) + -40000, -3749.47, 2)

    @mock.patch.object(xl, 'COMPATIBILITY', 'PYTHON')
    def test_NPV_in_python_mode(self):
        self.assertAlmostEqual(financial.NPV(0.06, 1, 2, 3), 5.556781772872908)
        self.assertAlmostEqual(financial.NPV(0.06, 1), 1.0)

    def test_NPV_without_values(self):
        self.assertIsInstance(financial.NPV(3.4), xl.ValueExcelError)

    def test_PMT(self):
        self.assertAlmostEqual(financial.PMT(0.08/12, 10, 10000), -1037.03, 2)

    @mock.patch.object(xl, 'COMPATIBILITY', 'PYTHON')
    def test_PMT_in_python_mode(self):
        self.assertAlmostEqual(
            financial.PMT(0.08/12, 10, 10000), -1037.03, 2)
        self.assertAlmostEqual(
            financial.PMT(0.08/12, 10, 10000, type=1), -1030.164, 2)

    def test_SLN(self):
        self.assertEqual(financial.SLN(30000, 7500, 10), 2250)

    def test_XNPV(self):
        range_00 = xl.RangeData(
            [[-10000, 2750, 4250, 3250, 2750]])
        range_01 = xl.RangeData(
            [[date.DATE(2008, 1, 1),
              date.DATE(2008, 3, 1),
              date.DATE(2008, 10, 30),
              date.DATE(2009, 2, 15),
              date.DATE(2009, 4, 1)
            ]])
        self.assertAlmostEqual(
            financial.XNPV(0.09, range_00, range_01), 2086.65, 2)

    def test_XNPV_length_mismatch(self):
        range_00 = [-10000, 2750, 4250]
        range_01 = [date.DATE(2008, 1, 1), date.DATE(2008, 3, 1)]
        self.assertIsInstance(
            financial.XNPV(0.09, range_00, range_01), xl.NumExcelError)
