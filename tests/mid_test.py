
# Excel reference: https://support.office.com/en-us/article/mid-midb-functions-d5f9e25c-d7d6-472e-b568-4ecb12433028

import unittest

from xlfunctions import Mid
from xlfunctions.exceptions import ExcelError


class TestMid(unittest.TestCase):

    def test_start_num_must_be_integer(self):
        self.assertIsInstance(Mid.mid('Romain', 1.1, 2), ExcelError )


    def test_num_chars_must_be_integer(self):
        self.assertIsInstance(Mid.mid('Romain', 1, 2.1), ExcelError )


    def test_start_num_must_be_superior_or_equal_to_1(self):
        self.assertIsInstance(Mid.mid('Romain', 0, 3), ExcelError )


    def test_num_chars_must_be_positive(self):
        self.assertIsInstance(Mid.mid('Romain', 1, -1), ExcelError )


    def test_mid(self):
        self.assertEqual(Mid.mid('Romain', 3, 4), 'main')
        self.assertEqual(Mid.mid('Romain', 1, 2), 'Ro')
        self.assertEqual(Mid.mid('Romain', 3, 6), 'main')
