import datetime
import yearfrac
from dateutil.relativedelta import relativedelta

from . import xl

# Testing hook.
today = datetime.date.today


def _date_from_int(nb):
    return xl.EXCEL_EPOCH + datetime.timedelta(days=nb-2)


@xl.register()
@xl.validate_args
def DATE(year: xl.Integer, month: xl.Integer, day: xl.Integer):
    """Returns the sequential serial number that represents a particular date.

    https://support.office.com/en-us/article/
        date-function-e36c0c8c-4104-49da-ab83-82328b832349
    """
    if not (0 < year < 9999):
        return xl.NumExcelError(
            f'Year must be between 1 and 9999, instead {year}')

    if year < 1900:
        year = 1900 + year

    # Excel starts counting at 1 and today is inclusive, thus +2
    delta = relativedelta(years=year-1900, months=month-1, days=day-1)
    result = ((xl.EXCEL_EPOCH + delta) - xl.EXCEL_EPOCH).days + 2

    if result <= 0:
        return xl.NumExcelError("Date result is negative.")

    return result


@xl.register()
def TODAY():
    """Returns the serial number of the current date.

    https://support.office.com/en-us/article/
        today-function-5eb3078d-a82c-4736-8930-2f51a028fdd9
    """
    # Excel starts counting at 1 and today is inclusive, thus +2
    return (today() - xl.EXCEL_EPOCH).days + 2


@xl.register()
@xl.validate_args
def YEARFRAC(start_date: xl.Number, end_date: xl.Number, basis: xl.Integer = 0):
    """Returns the fraction of the year represented by the number of whole
    days between two dates.

    https://support.office.com/en-us/article/
        yearfrac-function-3844141e-c76d-4143-82b6-208454ddc6a8
    """
    if start_date < 0:
        return xl.ValueExcelError(f'start_date {start_date} must be positive')

    if end_date < 0:
        return xl.ValueExcelError(f'end_date {end_date} must be positive')

    # Switch dates if start_date > end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    start_dt = _date_from_int(start_date)
    end_dt = _date_from_int(end_date)

    if basis == 0: # US 30/360
        return yearfrac.yearfrac(start_dt, end_dt, '30e360_matu')
    elif basis == 1: # Actual/actual
        return yearfrac.yearfrac(start_dt, end_dt, 'act_afb')
    elif basis == 2: # Actual/360
        return (end_date - start_date) / 360
    elif basis == 3: # Actual/365
        return (end_date - start_date) / 365
    elif basis == 4: # Eurobond 30/360
        return yearfrac.yearfrac(start_dt, end_dt, '30e360')
    else:
        return xl.ValueExcelError(
            f'basis must be 0, 1, 2, 3 or 4, got {basis}')
