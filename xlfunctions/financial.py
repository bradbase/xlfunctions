import numpy_financial
import pandas

from . import xl


@xl.register()
def IRR(values, guess=None):
    """Returns the internal rate of return for a series of cash flows

    https://support.office.com/en-us/article/
        irr-function-64925eaa-9988-495b-b290-3ad0c163c1bc
    """
    if guess is not None and guess != 0:
        raise ValueError('"guess" value for IRR() is {guess} and not 0')

    return numpy_financial.irr(xl.flatten(values))


@xl.register()
def NPV(rate, *values):
    """Calculates the net present value of an investment by using a discount
    rate and a series of future payments (negative values) and income
    (positive values).

    https://support.office.com/en-us/article/
        npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568
    """
    if not len(values):
        return xl.ExcelError('#VALUE', 'value1 is required')

    cashflow = filter(xl.is_number, xl.flatten(values))

    if xl.COMPATIBILITY == 'PYTHON':
        return numpy_financial.npv(discount_rate, cashflow)

    return sum([
        float(val) * (1 + rate)**-(i+1)
        for (i, val) in enumerate(cashflow)
    ])


@xl.register()
def PMT(rate, nper, pv, fv=None, type=0):
    """Calculates the payment for a loan based on constant payments and
    a constant interest rate.

    https://support.office.com/en-us/article/
        pmt-function-0214da64-9a63-4996-bc20-214433fa6441
    """
    # WARNING fv & type not used yet - both are assumed to be their defaults (0)
    # fv = args[3]
    # type = args[4]

    if xl.COMPATIBILITY == 'PYTHON':
        when = 'end'
        if type != 0:
            when = 'begin'
        return numpy_financial.pmt(rate, nper, pv, fv=0, when=when)

    # return -pv * rate / (1 - power(1 + rate, -nper))
    return numpy_financial.pmt(rate, nper, pv, fv=0, when='end')


@xl.register()
def SLN(cost, salvage, life):
    """Returns the straight-line depreciation of an asset for one period.

    https://support.office.com/en-us/article/
        sln-function-cdb666e5-c1c6-40a7-806a-e695edc2f1c8
    """
    if not xl.is_number(cost):
        return xl.ExcelError(
            '#VALUE', f'cost must be a nyumber, got {type(cost)}.')
    if not xl.is_number(salvage):
        return xl.ExcelError(
            '#VALUE', f'cost must be a nyumber, got {type(salvage)}.')
    if not xl.is_number(life):
        return xl.ExcelError(
            '#VALUE', f'cost must be a nyumber, got {type(life)}.')

    return (cost - salvage) / life


@xl.register()
def xnpv(rate, values, dates):
    """Returns the net present value for a schedule of cash flows that
    is not necessarily periodic.

    https://support.microsoft.com/en-us/office/
        xnpv-function-1b42bbf6-370f-4532-a0eb-d67c16b664b7
    """
    if not xl.is_range(values):
        return xl.ValueError(f'`values` must be a range, got {type(values)}')

    if not xl.is_range(dates):
        return xl.ValueError(f'`dates` must be a range, got {type(dates)}')

    rate = float(rate)
    values = xl.flatten(values)
    dates = xl.flatten(dates)

    # TODO: Ignore non numeric cells and boolean cells.
    if len(values) != len(dates):
        return xl.NumError(
            f'`values` range must be the same length as `dates` range '
            f'in XNPV, {len(values)} != {len(dates)}')

    def npv(value, date):
        return value / power(1.0 + rate, (date - dates[0]) / 365)

    return sum([npv(value, date) for value, date in zip(values, dates)])
