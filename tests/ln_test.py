
# Excel reference: https://support.office.com/en-us/article/ln-function-81fe1ed7-dac9-4acd-ba1d-07a142c6118f

import unittest

from xlfunctions import Ln

from .xlfunctions_test import xlfunctionsTestCase


class TestLn(xlfunctionsTestCase):

    def test_ln(self):
        ln_result_00 = Ln.ln(86)
        result_00 = 4.4543473
        self.assertEqual(result_00, round(ln_result_00, 7))


    def test_ln_not_rounded(self):
        ln_result_02 = Ln.ln(2.7182818)
        result_02 = 1 # this is in error but is what's in the LN function examples from MS.
        self.assertEqualRounded(result_02, ln_result_02)
