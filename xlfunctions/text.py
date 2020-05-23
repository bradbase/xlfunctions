from . import xl


@xl.register()
@xl.validate_args
def CONCAT(*texts):
    """The CONCAT function combines the text from multiple ranges and/or
    strings, but it doesn't provide delimiter or IgnoreEmpty arguments.

    https://support.office.com/en-us/article/
        concat-function-9b1a9a3f-94ff-41af-9736-694cbd6b4ca2
    """
    if len(texts) > 254:
        return xl.ValueExcelError(
            f"Can't concat more than 254 arguments. Provided: {len(texts)}")

    texts = xl.flatten(texts)
    return ''.join([
        str(text) for text in xl.flatten(texts)
        if xl.is_text(text) or xl.is_number(text)
    ])


@xl.register()
@xl.validate_args
def MID(text: xl.Text, start_num: xl.Integer, num_chars: xl.Integer):
    """Returns a specific number of characters from a text string, starting
    at the position you specify, based on the number of characters you specify.

    https://support.office.com/en-us/article/
        mid-midb-functions-d5f9e25c-d7d6-472e-b568-4ecb12433028
    """
    text = str(text)

    if len(text) > xl.CELL_CHARACTER_LIMIT:
        return xl.ValueExcelError(
            f'Text is too long. Is {len(text)} but needs to '
            f'be {xl.CELL_CHARACTER_LIMIT} or less.')

    if start_num < 1:
        return xl.NumExcelError(f'{start_num} is < 1')

    if num_chars < 0:
        return xl.NumExcelError(f'{num_chars} is < 0')

    start_idx = start_num - 1
    return text[start_idx:start_idx+num_chars]


@xl.register()
@xl.validate_args
def RIGHT(text: xl.Text, num_chars: xl.Integer = 1):
    """Returns the last character or characters in a text string.

    https://support.office.com/en-us/article/
        right-rightb-functions-240267ee-9afa-4639-a02b-f19e1786cf2f
    """
    text = str(text)
    return text[-num_chars:]
