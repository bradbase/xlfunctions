import mock
import pandas
import unittest

from xlfunctions import xl


class ExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(err.value, '#N/A')
        self.assertEqual(err.info, 'Not applicable')

    def test_str(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(str(err), '#N/A')


class SpecificExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.SpecificExcelError('Not applicable')
        self.assertEqual(err.value, None)
        self.assertEqual(err.info, 'Not applicable')


class NullExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NullError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NULL)


class DivZeroExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.DivZeroError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_DIV_ZERO)


class ValueExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.ValueError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_VALUE)


class RefExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.RefError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_REF)


class NameExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NameError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NAME)


class NumExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NumError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NUM)


class NaExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NaError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NA)


class FunctionsTest(unittest.TestCase):

    def test_register(self):
        fn = xl.Functions()

        def sample():
            pass

        fn.register(sample)
        self.assertDictEqual(dict(fn), {'sample': sample})

    def test_register_withName(self):
        fn = xl.Functions()

        def sample():
            pass

        fn.register(sample, 'mysample')
        self.assertDictEqual(dict(fn), {'mysample': sample})

    def test_getattr(self):
        fn = xl.Functions()

        def sample():
            pass

        fn.register(sample)
        self.assertEqual(fn.sample, sample)

    def test_getattr_withUnknown(self):
        fn = xl.Functions()
        with self.assertRaises(AttributeError):
            fn.sample

    def test_register_decorator(self):

        with mock.patch('xlfunctions.xl.FUNCTIONS', xl.Functions()):

            @xl.register()
            def sample():
                pass

            self.assertDictEqual(dict(xl.FUNCTIONS), {'sample': sample})


class XlModuleTest(unittest.TestCase):

    def test_is_number(self):
        self.assertTrue(xl.is_number(1))
        self.assertTrue(xl.is_number(1.0))
        self.assertFalse(xl.is_number('data'))

    def test_is_range(self):
        self.assertTrue(xl.is_range(pandas.DataFrame([1])))
        self.assertTrue(xl.is_range([1]))
        self.assertFalse(xl.is_range('data'))

    def test_is_empty(self):
        self.assertTrue(xl.is_empty(None))
        self.assertTrue(xl.is_empty(''))
        self.assertFalse(xl.is_empty('data'))

    def test_flatten(self):
        self.assertEqual(xl.flatten([1, [2, 3], [4]]), [1, 2, 3, 4])
        df = pandas.DataFrame([[1, 2], [3, 4]])
        self.assertEqual(xl.flatten(df), [1, 2, 3, 4])
        self.assertEqual(xl.flatten([df]), [1, 2, 3, 4])

    def test_length(self):
        self.assertEqual(xl.length([1, [2, 3], [4]]), 4)
        df = pandas.DataFrame([[1, 2], [3, 4]])
        self.assertEqual(xl.length(df), 4)
