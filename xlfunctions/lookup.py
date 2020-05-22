import pandas

from . import xl


@xl.register()
def CHOOSE(index_num, *values):
    """Uses index_num to return a value from the list of value arguments.

    https://support.office.com/en-us/article/
        choose-function-fc5c184f-cb62-4ec7-a46e-38653b98f5bc
    """
    if isinstance(index_num, str):
        index_num = int(index_num)

    if index_num <= 0 or index_num > 254:
        return xl.ExcelError(
            "#VALUE!", f"{index_num} must be between 1 and 254")

    if index_num > len(values):
        return xl.ExcelError(
            "#VALUE!",
            f"{index} must not be larger than the number of "
            f"values: {len(values)}")

    idx = index_num - 1
    return values[idx]


@xl.register()
def VLOOKUP(lookup_value, table_array, col_index_num, range_lookup=False):
    """Looks in the first column of an array and moves across the row to
    return the value of a cell.

    https://support.office.com/en-us/article/
        vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1
    """
    if range_lookup:
        raise NotImplementedError("Excact match only supported at the moment.")

    if col_index_num > xl.length(table_array):
        return xl.ValueError(
            'col_index_num is greater than the number of cols in table_array')

    table_array = table_array.set_index(0)

    if lookup_value not in table_array.index:
        return xl.NaError('lookup_value not in first column of table_array')

    return table_array.loc[lookup_value].values[0]
