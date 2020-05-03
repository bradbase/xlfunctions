
# Excel reference: https://support.microsoft.com/en-us/office/xnpv-function-1b42bbf6-370f-4532-a0eb-d67c16b664b7

import unittest

import pandas as pd

from xlfunctions import XNPV
from xlfunctions import xDate
from xlfunctions.exceptions import ExcelError

from .xlfunctions_test import xlfunctionsTestCase


class TestNPV(xlfunctionsTestCase):

    def test_npv_basic(self):
        range_00 = pd.DataFrame([[-10000, 2750, 4250, 3250, 2750]])
        range_01 = pd.DataFrame([[xDate.xdate(2008, 1, 1),
                                xDate.xdate(2008, 3, 1),
                                xDate.xdate(2008, 10, 30),
                                xDate.xdate(2009, 2, 15),
                                xDate.xdate(2009, 4, 1)
                                ]])
        self.assertEqual(round(XNPV.xnpv(0.09, range_00, range_01), 2), 2086.65)
