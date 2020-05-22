import datetime
import yearfrac

from . import xl

# Testing hook.
today = datetime.date.today

@xl.register()
def DATE(year, month, day):
    """Returns the sequential serial number that represents a particular date.

    https://support.office.com/en-us/article/
        date-function-e36c0c8c-4104-49da-ab83-82328b832349
    """

    if not isinstance(year, int):
        try:
            year = int(year)
        except ValueError:
            return xl.ValueError(f'{year} is not an integer')

    if not isinstance(month, int):
        try:
            month = int(month)
        except ValueError:
            return xl.ValueError(f'{month} is not an integer')

    if not isinstance(day, int):
        try:
            day = int(day)
        except ValueError:
            return xl.ValueError(f'{day} is not an integer')

    if not (0 < year < 9999):
        return xl.NumError(f'Year must be between 1 and 9999, instead {year}')

    if year < 1900:
        year = 1900 + year

    # Takes into account negative month and day values.
    year, month, day = normalize_year(year, month, day)

    date_0 = datetime.date(1900, 1, 1)
    date = datetime.date(year, month, day)
    result = (datetime.date(year, month, day) - date_0).days + 2

    if result <= 0:
        return xl.NumError("Date result is negative.")

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
def YEARFRAC(start_date, end_date, basis = 0):
    """Returns the fraction of the year represented by the number of whole
    days between two dates.

    https://support.office.com/en-us/article/
        yearfrac-function-3844141e-c76d-4143-82b6-208454ddc6a8
    """

    if not xl.is_number(start_date):
        return xl.ValueError(
            f'start_date {start_date} must be a number. Got {type(start_date)}')

    if not xl.is_number(end_date):
        return xl.ValueError(
            f'end_date {end_date} must be a number. Got {type(end_date)}')

    if start_date < 0:
        return xl.ValueError(f'start_date {start_date} must be positive')

    if end_date < 0:
        return xl.ValueError(f'end_date {end_date} must be positive')

    # Switch dates if start_date > end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    start_dt = datetime.date(*date_from_int(start_date))
    end_dt = datetime.date(*date_from_int(end_date))

    if basis == 0: # US 30/360
        d2 = 30 if d2 == 31 and (d1 == 31 or d1 == 30) else min(d2, 31)
        d1 = 30 if d1 == 31 else d1
        count = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
        return count / 360
    elif basis == 1: # Actual/actual
        return yearfrac.act_afb(start_dt, end_dt)
    elif basis == 2: # Actual/360
        result = (end_date - start_date) / 360
    elif basis == 3: # Actual/365
        return yearfrac.d30365(start_dt, end_dt)
    elif basis == 4: # Eurobond 30/360
        return yearfrac.d30360e(start_dt, end_dt)

    else:
        return xl.ValueError(f'basis must be 0, 1, 2, 3 or 4, got {basis}')


def normalize_year(year, month, day):
    if month <= 0:
        year -= int(abs(month) / 12 + 1)
        month = 12 - (abs(month) % 12)
        normalize_year(year, month, day)
    elif month > 12:
        year += int(month / 12)
        month = month % 12

    if day <= 0:
        day += get_max_days_in_month(month, year)
        month -= 1
        year, month, day = normalize_year(year, month, day)

    else:
        if month in (4, 6, 9, 11) and day > 30:
            month += 1
            day -= 30
            year, month, day = normalize_year(year, month, day)
        elif month == 2:
            if (is_leap_year(year)) and day > 29:
                month += 1
                day -= 29
                year, month, day = normalize_year(year, month, day)
            elif (not is_leap_year(year)) and day > 28:
                month += 1
                day -= 28
                year, month, day = normalize_year(year, month, day)
        elif day > 31:
            month += 1
            day -= 31
            year, month, day = normalize_year(year, month, day)

    return (year, month, day)


def get_max_days_in_month(month, year):
    if not xl.is_number(year) or not xl.is_number(month):
        raise TypeError("All inputs must be a number")
    if year <= 0 or month <= 0:
        raise TypeError("All inputs must be strictly positive")

    if month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    else:
        return 31


def is_leap_year(year):
    if not xl.is_number(year):
        raise TypeError("%s must be a number" % str(year))
    if year <= 0:
        raise TypeError("%s must be strictly positive" % str(year))

    # Watch out, 1900 is a leap according to Excel
    #   => https://support.microsoft.com/en-us/kb/214326
    return (
        year % 4 == 0 and year % 100 != 0 or year % 400 == 0) or year == 1900


def date_from_int(nb):
    if not xl.is_number(nb):
        raise TypeError("%s is not a number" % str(nb))

    # origin of the Excel date system
    current_year = 1900
    current_month = 0
    current_day = 0

    while(nb > 0):
        if not is_leap_year(current_year) and nb > 365:
            current_year += 1
            nb -= 365
        elif is_leap_year(current_year) and nb > 366:
            current_year += 1
            nb -= 366
        else:
            current_month += 1
            max_days = get_max_days_in_month(current_month, current_year)

            if nb > max_days:
                nb -= max_days
            else:
                current_day = nb
                nb = 0

    return (int(current_year), int(current_month), int(current_day))
