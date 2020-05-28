import datetime
import unittest

from xlfunctions import utils, xlerrors, xltypes


class ExcelTypeTest(unittest.TestCase):

    class MyType(xltypes.ExcelType):
        native_types = (int, type(None))

    def test__Blank__(self):
        blank = self.MyType(1).__Blank__()
        self.assertIsInstance(blank, xltypes.ExcelType)
        self.assertEqual(blank.value, None)

    def test__number__(self):
        self.assertEqual(self.MyType(1).__number__(), 1.0)

    def test__datetime__(self):
        with self.assertRaises(NotImplementedError):
            self.MyType(1).__datetime__()

    def test__repr__(self):
        self.assertEqual(repr(self.MyType(1)), '<MyType 1>')


class AbstractExcelTypeTest:

    value_zero = xltypes.Number(0)

    value1 = xltypes.Number(1)
    native1 = 1
    num1 = 1
    value1_float = 1
    value1_int = 1
    value1_text = '1'
    value1_bool = True
    value1_dt = datetime.datetime(1900, 1, 1)

    value2 = xltypes.Number(2)
    native2 = 2
    num2 = 2
    text2 = xltypes.Text('2')
    bool2 = xltypes.Boolean(True)
    dt2 = xltypes.DateTime(datetime.datetime(2020, 1, 1, 12, 0, 0))
    dt2_float = 6523831.0

    math_result_type = int

    def test__add__(self):
        res = self.value1 + self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1+self.num2)

    def test__add___with_native_addend(self):
        res = self.value1 + self.native2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1+self.num2)

    def test__add__with_Text(self):
        res = self.value1 + self.text2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1+self.num2)

    def test__add__with_unconvertible_Text(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            self.value1 + xltypes.Text('data')

    def test__add__with_Boolean(self):
        res = self.value1 + self.bool2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1+1)

    def test__add__with_DateTime(self):
        res = self.value1 + self.dt2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, self.num1+self.dt2_float)

    def test__sub__(self):
        res = self.value1 - self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1-self.num2)

    def test__sub___with_native_subtrahend(self):
        res = self.value1 - self.native2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1-self.num2)

    def test__mul__(self):
        res = self.value1 * self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1*self.num2)

    def test__mul___with_native_factor(self):
        res = self.value1 * self.num2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1*self.num2)

    def test__mul__with_DateTime(self):
        self.assertEqual(
                (self.value1 * self.dt2).value, self.num1*self.dt2_float)

    def test__truediv__(self):
        res = self.value1 / self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, self.num1/self.num2)

    def test__truediv___by_zero(self):
        with self.assertRaises(xlerrors.DivZeroExcelError):
            self.value1 / 0

    def test__truediv___with_native_divisor(self):
        res = self.value1 / self.native2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, self.num1/self.num2)

    def test__truediv__with_DateTime(self):
        self.assertEqual(
                (self.value1 / self.dt2).value, self.num1/self.dt2_float)

    def test__pow__(self):
        res = self.value1 ** self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1 ** self.num2)

    def test__pow___with_native_exponent(self):
        res = self.value1 ** self.num2
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, self.math_result_type)
        self.assertEqual(res.value, self.num1**self.num2)

    def test__pow__with_DateTime(self):
        self.assertEqual(
                (self.value1 ** self.dt2).value, self.num1**self.dt2_float)

    def test__lt__(self):
        res = self.value1 < self.value2
        self.assertIsInstance(res, xltypes.Boolean)
        self.assertIsInstance(res.value, bool)
        self.assertEqual(res.value, True)

    def test__lt___with_Text(self):
        self.assertEqual((self.value1 < xltypes.Text('data')).value, True)

    def test__lt___with_Boolean(self):
        self.assertEqual((self.value_zero < self.bool2).value, True)
        self.assertEqual((self.value2 < self.bool2).value, True)

    def test__lt___with_DateTime(self):
        self.assertEqual((self.value1 < self.dt2).value, True)

    def test__le__(self):
        self.assertEqual((self.value1 <= self.value2).value, True)
        self.assertEqual((self.value1 <= self.value1).value, True)
        self.assertEqual((self.value2 <= self.value1).value, False)

    def test__eq__(self):
        self.assertEqual((self.value1 == self.value2).value, False)
        self.assertEqual((self.value1 == self.value1).value, True)

    def test__ne__(self):
        self.assertEqual((self.value1 != self.value2).value, True)
        self.assertEqual((self.value1 != self.value1).value, False)

    def test__gt__(self):
        self.assertEqual((self.value1 > self.value2).value, False)
        self.assertEqual((self.value2 > self.value1).value, True)

    def test__ge__(self):
        self.assertEqual((self.value2 >= self.value1).value, True)
        self.assertEqual((self.value1 >= self.value1).value, True)
        self.assertEqual((self.value1 >= self.value2).value, False)

    def test__and__(self):
        self.assertEqual((self.value1 & self.value2).value, True)
        self.assertEqual((self.value1 & self.value_zero).value, False)

    def test__or__(self):
        self.assertEqual((self.value_zero | self.value1).value, True)
        self.assertEqual((self.value_zero | self.value_zero).value, False)

    def test__int__(self):
        self.assertEqual(int(self.value1), self.value1_int)
        self.assertEqual(
            int(xltypes.Number(self.value1_float)), self.value1_int)

    def test__float__(self):
        self.assertEqual(
            float(self.value1), self.value1_float)
        self.assertEqual(
            float(xltypes.Number(self.value1_float)), self.value1_float)

    def test__str__(self):
        self.assertEqual(str(self.value1), self.value1_text)

    def test__bool__(self):
        self.assertEqual(bool(self.value1), True)
        self.assertEqual(bool(self.value_zero), False)

    def test__Number__(self):
        self.assertEqual(self.value1.__Number__().value, self.num1)

    def test__Text__(self):
        text = self.value1.__Text__()
        self.assertIsInstance(text, xltypes.Text)
        self.assertEqual(text.value, self.value1_text)

    def test__Boolean__(self):
        boolean = self.value1.__Boolean__()
        self.assertIsInstance(boolean, xltypes.Boolean)
        self.assertEqual(boolean.value, True)

    def test__DateTime__(self):
        dt = self.value1.__DateTime__()
        self.assertIsInstance(dt, xltypes.DateTime)
        self.assertEqual(dt.value, self.value1_dt)

    def test__hash__(self):
        self.assertEqual(hash(self.value1), hash(self.value1.value))


class NumberTest(AbstractExcelTypeTest, unittest.TestCase):

    def test_is_whole(self):
        self.assertEqual(xltypes.Number(1).is_whole, True)
        self.assertEqual(xltypes.Number(1.0).is_whole, False)

    def test_is_decimal(self):
        self.assertEqual(xltypes.Number(1).is_decimal, False)
        self.assertEqual(xltypes.Number(1.0).is_decimal, True)

    def test__add__with_decimal_number(self):
        res = xltypes.Number(1) + xltypes.Number(2.0)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, 3.0)

    def test__add__with_native_float(self):
        res = xltypes.Number(1) + 2.0
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, 3.0)

    def test__sub__with_decimal_number(self):
        res = xltypes.Number(2) - xltypes.Number(1.0)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, 1.0)

    def test__sub__with_native_float(self):
        res = xltypes.Number(2) - 1.0
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, 1.0)

    def test__lt___with_decimal_number(self):
        self.assertEqual(
            (self.value1 < xltypes.Number(2.0)).value, True)

    def test__lt___with_native_int(self):
        self.assertEqual(
            (self.value1 < 2).value, True)

    def test__lt___with_native_float(self):
        self.assertEqual(
            (self.value1 < 2.0).value, True)

    def test__lt___with_Blank(self):
        self.assertEqual((
            xltypes.Number(-1) < xltypes.BLANK).value, True)
        self.assertEqual((
            self.value1 < xltypes.BLANK).value, False)

    def test__Blank__(self):
        blank = self.value1.__Blank__()
        self.assertIsInstance(blank, xltypes.Number)
        self.assertEqual(blank.value, 0)

    def test__repr__(self):
        self.assertEqual(repr(self.value1), '<Number 1>')


class TextTest(AbstractExcelTypeTest, unittest.TestCase):

    value_zero = xltypes.Text('')

    value1 = xltypes.Text('1')
    native1 = '1'
    num1 = 1
    value1_float = 1.0
    value1_int = 1
    value1_text = '1'
    value1_bool = True
    value1_dt = datetime.datetime(1900, 1, 1)

    value2 = xltypes.Text('2')
    native2 = '2'
    num2 = 2
    text2 = xltypes.Text('2')
    bool2 = xltypes.Boolean(True)

    def test__add__with_unconvertible_Text(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            self.value1 + xltypes.Text('data')

    def test__lt___with_Boolean(self):
        self.assertEqual((self.value1 < self.bool2).value, True)

    def test__lt___with_DateTime(self):
        # Text is always greater for comparison and is not converted.
        self.assertEqual((self.value1 < self.dt2).value, False)

    def test__int___with_unvonvertable_data(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            int(xltypes.Text('data'))

    def test__float___with_unvonvertable_data(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            float(xltypes.Text('data'))

    def test__number__(self):
        self.assertEqual(xltypes.Text('1').__number__(), 1)
        self.assertEqual(xltypes.Text('1.0').__number__(), 1.0)
        self.assertEqual(xltypes.Text('true').__number__(), 1)
        self.assertEqual(xltypes.Text('1900-01-01').__number__(), 1)

    def test__number___with_unvonvertable_data(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            xltypes.Text('data').__number__()

    def test__bool__(self):
        self.assertEqual(bool(xltypes.Text('true')), True)
        self.assertEqual(bool(xltypes.Text('false')), False)
        self.assertEqual(bool(xltypes.Text('data')), True)
        self.assertEqual(bool(xltypes.Text('')), False)

    def test__datetime__(self):
        self.assertEqual(
            xltypes.Text('1').__datetime__(), self.value1_dt)
        self.assertEqual(
            xltypes.Text('1900-01-01').__datetime__(), self.value1_dt)

    def test__Boolean__(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            self.value1.__Boolean__()
        boolean = xltypes.Text('true').__Boolean__()
        self.assertIsInstance(boolean, xltypes.Boolean)
        self.assertEqual(boolean.value, True)
        self.assertEqual(xltypes.Text('TRUE').__Boolean__().value, True)
        self.assertEqual(xltypes.Text('True').__Boolean__().value, True)
        self.assertEqual(xltypes.Text('False').__Boolean__().value, False)
        with self.assertRaises(xlerrors.ValueExcelError):
            self.assertEqual(xltypes.Text('').__Boolean__().value, False)

    def test__Blank__(self):
        blank = self.value1.__Blank__()
        self.assertIsInstance(blank, xltypes.Text)
        self.assertEqual(blank.value, '')


class BooleanTest(AbstractExcelTypeTest, unittest.TestCase):

    value_zero = xltypes.Boolean(False)

    value1 = xltypes.Boolean(True)
    native1 = True
    num1 = 1
    value1_float = 1.0
    value1_int = 1
    value1_text = 'True'
    value1_bool = True
    value1_dt = datetime.datetime(1999, 12, 31)

    value2 = xltypes.Boolean(True)
    native2 = True
    num2 = 1
    text2 = xltypes.Text('True')
    bool2 = xltypes.Boolean(True)

    def test__lt__(self):
        res = self.value_zero < self.value1
        self.assertIsInstance(res, xltypes.Boolean)
        self.assertIsInstance(res.value, bool)
        self.assertEqual(res.value, True)

    def test__lt___with_Text(self):
        self.assertEqual((self.value1 < xltypes.Text('data')).value, False)

    def test__lt___with_Boolean(self):
        self.assertEqual((self.value_zero < self.bool2).value, True)

    def test__lt___with_DateTime(self):
        self.assertEqual((self.value1 < self.dt2).value, False)

    def test__le__(self):
        self.assertEqual((self.value_zero <= self.value2).value, True)
        self.assertEqual((self.value_zero <= self.value_zero).value, True)
        self.assertEqual((self.value2 <= self.value_zero).value, False)

    def test__eq__(self):
        self.assertEqual((self.value_zero == self.value2).value, False)
        self.assertEqual((self.value_zero == self.value_zero).value, True)

    def test__ne__(self):
        self.assertEqual((self.value_zero != self.value2).value, True)
        self.assertEqual((self.value_zero != self.value_zero).value, False)

    def test__gt__(self):
        self.assertEqual((self.value_zero > self.value2).value, False)
        self.assertEqual((self.value2 > self.value_zero).value, True)

    def test__ge__(self):
        self.assertEqual((self.value2 >= self.value_zero).value, True)
        self.assertEqual((self.value_zero >= self.value_zero).value, True)
        self.assertEqual((self.value_zero >= self.value2).value, False)

    def test__and__(self):
        self.assertEqual((self.value2 & self.value2).value, True)
        self.assertEqual((self.value2 & self.value_zero).value, False)

    def test__or__(self):
        self.assertEqual((self.value_zero | self.value2).value, True)
        self.assertEqual((self.value_zero | self.value_zero).value, False)

    def test__bool__(self):
        self.assertEqual(bool(self.value2), True)
        self.assertEqual(bool(self.value_zero), False)

    def test__Blank__(self):
        blank = self.value1.__Blank__()
        self.assertIsInstance(blank, xltypes.Boolean)
        self.assertEqual(blank.value, False)


class DateTimeTest(AbstractExcelTypeTest, unittest.TestCase):

    value_zero = xltypes.DateTime(utils.EXCEL_EPOCH)

    value1 = xltypes.DateTime(datetime.datetime(1900, 1, 1))
    native1 = datetime.datetime(1900, 1, 1)
    num1 = 1
    value1_float = 1.0
    value1_int = 1
    value1_text = '1900-01-01 00:00:00'
    value1_bool = True
    value1_dt = datetime.datetime(1900, 1, 1)

    value2 = xltypes.DateTime(datetime.datetime(1900, 2, 1))
    native2 = datetime.datetime(1900, 2, 1)
    num2 = 32
    text2 = xltypes.Text('1900-02-01 00:00:00')
    bool2 = xltypes.Boolean(True)

    math_result_type = float

    def test__sub__(self):
        res = self.value1 - self.value2
        self.assertIsNot(res, self.value1)
        self.assertIsInstance(res, xltypes.Number)
        self.assertIsInstance(res.value, float)
        self.assertEqual(res.value, self.num1-self.num2)

    def test__bool__(self):
        self.assertEqual(bool(self.value1), True)
        self.assertEqual(bool(self.value_zero), True)

    def test__and__(self):
        # Bool of datetime will always be true.
        self.assertEqual((self.value1 & self.value2).value, True)
        self.assertEqual((self.value1 & self.value_zero).value, True)

    def test__or__(self):
        # Bool of datetime will always be true.
        self.assertEqual((self.value_zero | self.value1).value, True)
        self.assertEqual((self.value_zero | self.value_zero).value, True)

    def test__Blank__(self):
        blank = self.value1.__Blank__()
        self.assertIsNone(blank)

    def test__repr__(self):
        self.assertEqual(repr(self.value1), '<DateTime 1900-01-01T00:00:00>')


class BlankTest(unittest.TestCase):

    def test__add__(self):
        self.assertEqual((xltypes.BLANK + 1).value, 1)

    def test__sub__(self):
        self.assertEqual((xltypes.BLANK - 1).value, -1)

    def test__mul__(self):
        self.assertEqual((xltypes.BLANK * 1).value, 0)

    def test__truediv__(self):
        self.assertEqual((xltypes.BLANK / 1).value, 0)
        self.assertEqual((1 / xltypes.BLANK).value, 0)

    def test_pw__(self):
        self.assertEqual((xltypes.BLANK ** 1).value, 0)

    def test__lt__(self):
        self.assertEqual((xltypes.BLANK < 1).value, True)

    def test__le__(self):
        self.assertEqual((xltypes.BLANK <= 1).value, True)
        self.assertEqual((xltypes.BLANK <= 0).value, True)

    def test__eq__(self):
        self.assertEqual((xltypes.BLANK == 1).value, False)
        self.assertEqual((xltypes.BLANK == 0).value, True)
        self.assertEqual((xltypes.BLANK == 'data').value, False)
        self.assertEqual((xltypes.BLANK == '').value, True)
        self.assertEqual((xltypes.BLANK == True).value, False)    # noqa
        self.assertEqual((xltypes.BLANK == False).value, True)  # noqa

    def test__ne__(self):
        self.assertEqual((xltypes.BLANK != 1).value, True)
        self.assertEqual((xltypes.BLANK != 0).value, False)
        self.assertEqual((xltypes.BLANK != 'data').value, True)
        self.assertEqual((xltypes.BLANK != '').value, False)
        self.assertEqual((xltypes.BLANK != True).value, True)  # noqa
        self.assertEqual((xltypes.BLANK != False).value, False)  # noqa

    def test__gt__(self):
        self.assertEqual((xltypes.BLANK > 1).value, False)

    def test__ge__(self):
        self.assertEqual((xltypes.BLANK >= 1).value, False)
        self.assertEqual((xltypes.BLANK >= 0).value, True)

    def test__and__(self):
        self.assertEqual((xltypes.BLANK & 1).value, True)
        self.assertEqual((xltypes.BLANK & 1).value, True)
        with self.assertRaises(xlerrors.ValueExcelError):
            xltypes.BLANK & xltypes.BLANK

    def test__or__(self):
        self.assertEqual((xltypes.BLANK | 1).value, True)
        self.assertEqual((xltypes.BLANK | 1).value, True)
        with self.assertRaises(xlerrors.ValueExcelError):
            xltypes.BLANK | xltypes.BLANK

    def test__int__(self):
        self.assertEqual(int(xltypes.BLANK), 0)

    def test__float__(self):
        self.assertEqual(float(xltypes.BLANK), 0.0)

    def test__str__(self):
        self.assertEqual(str(xltypes.BLANK), '')

    def test__bool__(self):
        self.assertEqual(bool(xltypes.BLANK), False)

    def test__number__(self):
        self.assertEqual(xltypes.BLANK.__number__(), 0.0)

    def test__repr__(self):
        self.assertEqual(repr(xltypes.BLANK), '<BLANK>')


class ArrayTest(unittest.TestCase):

    def test__init__withbad_data(self):
        with self.assertRaises(xlerrors.ValueExcelError):
            xltypes.Array('bad')

    def test_flat(self):
        self.assertEqual(
            xltypes.Array([[1, 2, 3], [4, 5, 6]]).flat,
            [1, 2, 3, 4, 5, 6]
        )

    def test_cast_to_numbers(self):
        dt = datetime.datetime(1900, 1, 5)
        array = xltypes.Array([[1, None, dt], ['4.0', True, 6]])
        nums = array.cast_to_numbers()
        self.assertIsInstance(nums[0][0], xltypes.Number)
        self.assertEqual(nums.flat, [1, 0.0, 5.0, 4.0, 1, 6])

    def test_cast_to_numbers_with_errors(self):
        array = xltypes.Array([[1, object()]])
        nums = array.cast_to_numbers()
        self.assertEqual(nums.flat, [1, 0.0])

    def test_cast_to_booleans(self):
        dt = datetime.datetime(1900, 1, 5)
        array = xltypes.Array([[1, None, dt], ['4.0', True, 6]])
        bools = array.cast_to_booleans()
        self.assertIsInstance(bools[0][0], xltypes.Boolean)
        self.assertEqual(bools.flat, [True, False, True, True, True, True])

    def test_cast_to_texts(self):
        dt = datetime.datetime(1900, 1, 5)
        array = xltypes.Array([[1, None, dt], ['4.0', True, 6]])
        texts = array.cast_to_texts()
        self.assertIsInstance(texts[0][0], xltypes.Text)
        self.assertEqual(
            texts.flat,
            ['1', '', '1900-01-05 00:00:00', '4.0', 'True', '6'])


class ExprTest(unittest.TestCase):

    def test_init(self):

        def callable(arg):
            return arg

        expr = xltypes.Expr(callable, (1,), value=1)
        self.assertEqual(expr.callable, callable)
        self.assertEqual(expr.value, 1)

    def test_call(self):

        def callable(arg):
            return arg

        expr = xltypes.Expr(callable, (1,), value=1)
        self.assertEqual(expr(), 1)

    def test_ValueExpr(self):
        expr = xltypes.ValueExpr(1)
        self.assertEqual(expr.value, 1)
        self.assertEqual(expr(), 1)
