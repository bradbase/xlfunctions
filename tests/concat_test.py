
# Excel reference: https://support.office.com/en-us/article/concat-function-9b1a9a3f-94ff-41af-9736-694cbd6b4ca2

import unittest

import pandas as pd

from xlfunctions import Concat

class TestConcat(unittest.TestCase):

    def test_concat(self):

        concat_result_00 = Concat.concat("SPAM", " ", "SPAM", " ", "SPAM", " ", "SPAM")
        result_00 = "SPAM SPAM SPAM SPAM"
        self.assertTrue(result_00, concat_result_00)

        concat_result_01 = Concat.concat("SPAM", " ", pd.DataFrame([[1, 2],[3, 4]]), " ", "SPAM", " ", "SPAM")
        result_01 = "SPAM 1234 SPAM SPAM"
        self.assertTrue(result_01, concat_result_01)

        concat_result_02 = Concat.concat("SPAM", "SPAM", "SPAM")
        result_02 = "SPAMSPAMSPAM"
        self.assertTrue(result_02, concat_result_02)
