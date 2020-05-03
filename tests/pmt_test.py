
# Excel reference: https://support.office.com/en-us/article/npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568

import unittest

from xlfunctions import PMT
from xlfunctions.exceptions import ExcelError

from .xlfunctions_test import xlfunctionsTestCase


class TestPMT(xlfunctionsTestCase):

    def test_pmt_basic(self):
        self.assertEqualTruncated( PMT.pmt(0.08/12, 10, 10000), -1037.03)
