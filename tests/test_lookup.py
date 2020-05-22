import unittest

from xlfunctions import xl, lookup


class LookupModuleTest(unittest.TestCase):

    def test_CHOOSE(self):
        range_00 = xl.RangeData([[1, 2],[3, 4]])
        range_01 = xl.RangeData([[2, 1],[3, 4]])
        range_02 = xl.RangeData([[1, 2],[4, 3]])
        choose_result_00 = lookup.CHOOSE('2', range_00, range_01, range_02)
        result_00 = xl.RangeData([[2, 1],[3, 4]])
        self.assertTrue(result_00.equals(choose_result_00))

    def test_VLOOOKUP(self):
        # Excel Doc example.
        range1 = xl.RangeData([
            [101, 'Davis', 'Sara'],
            [102, 'Fortana', 'Olivier'],
            [103, 'Leal', 'Karina'],
            [104, 'Patten', 'Michael'],
            [105, 'Burke', 'Brian'],
            [106, 'Sousa', 'Luis'],
        ])
        self.assertEqual(lookup.VLOOKUP(102, range1, 2, False), 'Fortana')
