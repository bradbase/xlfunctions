import mock
import typing
import unittest

from xlfunctions import xl


class NoStr:
    def __str__(self):
        raise ValueError()


class ExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(err.value, '#N/A')
        self.assertEqual(err.info, 'Not applicable')

    def test_str(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(str(err), '#N/A')

    def test_eq(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(err, err)

    def test_eq_to_string(self):
        err = xl.ExcelError('#N/A', 'Not applicable')
        self.assertEqual(err, '#N/A')


class SpecificExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.SpecificExcelError('Not applicable')
        self.assertEqual(err.value, None)
        self.assertEqual(err.info, 'Not applicable')


class NullExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NullExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NULL)


class DivZeroExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.DivZeroExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_DIV_ZERO)


class ValueExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.ValueExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_VALUE)


class RefExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.RefExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_REF)


class NameExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NameExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NAME)


class NumExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NumExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NUM)


class NaExcelErrorTest(unittest.TestCase):

    def test_error(self):
        err = xl.NaExcelError('Error')
        self.assertEqual(str(err), xl.ERROR_CODE_NA)


class NumberExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.NumberExcelError('bad', 'field')
        self.assertEqual(
            err.info, '`field` "bad" must be an int or float. Got: str')


class IntegerExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.IntegerExcelError('bad', 'field')
        self.assertEqual(
            err.info, '`field` "bad" must be an int. Got: str')


class TextExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.TextExcelError(42, 'field')
        self.assertEqual(
            err.info, '`field` "42" must be text. Got: int')


class RangeExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.RangeExcelError('bad', 'field')
        self.assertEqual(
            err.info, '`field` "bad" must be a range. Got: str')


class EmptyExcelErrorTest(unittest.TestCase):

    def test_init(self):
        err = xl.EmptyExcelError('bad', 'field')
        self.assertEqual(
            err.info, '`field` "bad" must be None or "". Got: str')


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

    def test_is_integer(self):
        self.assertTrue(xl.is_integer(1))
        self.assertFalse(xl.is_integer(1.0))
        self.assertFalse(xl.is_integer('data'))

    def test_is_number(self):
        self.assertTrue(xl.is_number(1))
        self.assertTrue(xl.is_number(1.0))
        self.assertFalse(xl.is_number('data'))

    def test_is_text(self):
        self.assertFalse(xl.is_text(1))
        self.assertFalse(xl.is_text(1.0))
        self.assertTrue(xl.is_text('data'))

    def test_is_range(self):
        self.assertTrue(xl.is_range(xl.RangeData([1])))
        self.assertTrue(xl.is_range([1]))
        self.assertFalse(xl.is_range('data'))

    def test_is_empty(self):
        self.assertTrue(xl.is_empty(None))
        self.assertTrue(xl.is_empty(''))
        self.assertFalse(xl.is_empty('data'))

    def test_is_criteria(self):
        self.assertTrue(xl.is_criteria(None))
        self.assertTrue(xl.is_criteria(''))
        self.assertTrue(xl.is_criteria('data'))
        self.assertFalse(xl.is_criteria(xl.RangeData([1])))

    def test_is_error(self):
        self.assertTrue(xl.is_error(xl.ValueExcelError()))
        self.assertFalse(xl.is_error('data'))

    def test_flatten(self):
        self.assertEqual(xl.flatten([1, [2, 3], [4]]), [1, 2, 3, 4])
        df = xl.RangeData([[1, 2], [3, 4]])
        self.assertEqual(xl.flatten(df), [1, 2, 3, 4])
        self.assertEqual(xl.flatten([df]), [1, 2, 3, 4])

    def test_length(self):
        self.assertEqual(xl.length([1, [2, 3], [4]]), 4)
        df = xl.RangeData([[1, 2], [3, 4]])
        self.assertEqual(xl.length(df), 4)

    def test_convert_integer(self):
        self.assertEqual(xl.convert_integer(1), 1)
        self.assertEqual(xl.convert_integer(1.1), 1)
        self.assertEqual(xl.convert_integer('1.1'), 1)

    def test_convert_integer_with_conversion_error(self):
        with self.assertRaises(xl.IntegerExcelError):
            xl.convert_integer('bad')

    def test_convert_number(self):
        self.assertEqual(xl.convert_number(1), 1)
        self.assertEqual(xl.convert_number(1.1), 1.1)
        self.assertEqual(xl.convert_number('1.1'), 1.1)

    def test_convert_number_with_conversion_error(self):
        with self.assertRaises(xl.NumberExcelError):
            xl.convert_number('bad')

    def test_convert_range(self):
        self.assertIsNotNone(xl.convert_range(xl.RangeData()))

    def test_convert_range_with_conversion_error(self):
        with self.assertRaises(xl.RangeExcelError):
            xl.convert_range('bad')

    def test_convert_text(self):
        self.assertEqual(xl.convert_text(1), '1')
        self.assertEqual(xl.convert_text(1.1), '1.1')
        self.assertEqual(xl.convert_text('1.1'), '1.1')
        self.assertEqual(xl.convert_text('data'), 'data')

    def test_convert_text_with_conversion_error(self):
        with self.assertRaises(xl.TextExcelError):
            xl.convert_text(NoStr())

    def test_convert_empty(self):
        self.assertIsNone(xl.convert_empty(None))
        self.assertIsNone(xl.convert_empty(''))

    def test_convert_empty_with_non_empty_value(self):
        with self.assertRaises(xl.EmptyExcelError):
            xl.convert_empty(0)
        with self.assertRaises(xl.EmptyExcelError):
            xl.convert_empty('data')

    def test_validate_args(self):

        @xl.validate_args
        def func(arg: xl.Number):
            return arg

        self.assertEqual(func('1'), 1)

    def test_validate_args_fail(self):

        @xl.validate_args
        def func(arg: xl.Number):
            return arg

        self.assertIsInstance(func('bad'), xl.NumberExcelError)

    def test_validate_args_with_list(self):

        @xl.validate_args
        def func(*args: typing.List[xl.Number]):
            return args

        self.assertEqual(func('1', 2), (1, 2))

    def test_validate_args_with_union(self):

        @xl.validate_args
        def func(arg: typing.Union[xl.Number, xl.Text]):
            return arg

        self.assertEqual(func('data'), 'data')
        self.assertEqual(func(1), 1)
        self.assertIsInstance(func(NoStr()), xl.ValueExcelError)

    def test_validate_args_without_type(self):

        @xl.validate_args
        def func(arg):
            return arg

        obj = object()
        self.assertEqual(func(obj), obj)

    def test_parse_criteria(self):
        check = xl.parse_criteria('>3')
        self.assertTrue(check(4))
        self.assertFalse(check(2))

    def test_parse_criteria_with_implicit_operator(self):
        # Assumes equality.
        check = xl.parse_criteria('1')
        self.assertTrue(check(1))
        self.assertFalse(check(2))

    def test_parse_criteria_with_implicit_operator_string_value(self):
        # Assumes equality.
        check = xl.parse_criteria('data')
        self.assertTrue(check('data'))
        self.assertFalse(check(2))

    def test_parse_criteria_with_simple_number(self):
        check = xl.parse_criteria(1)
        self.assertTrue(check(1))
        self.assertFalse(check(2))

    def test_parse_criteria_with_unknown_type_or_value(self):
        check = xl.parse_criteria(object())
        # Always false.
        self.assertFalse(check('data'))
        self.assertFalse(check(2))
