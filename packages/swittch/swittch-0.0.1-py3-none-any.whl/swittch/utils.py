SWITTCH_CODE_DIGITS = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'


def luhn_mod_n_str(code: str, digits='0123456789ABCDEFGHIJKLMNOPQRSTUVWXZY') -> str:
    """ Calculates a check digit (from digits) for an alphanumerical code """
    base = len(digits)
    factor = 2
    total = 0
    for n, char in enumerate(reversed(code)):
        addend = digits.find(char) * factor
        # cycle factor between 1 and 2
        factor = (factor == 2) and 1 or 2
        total += int(addend / base) + (addend % base)
    # check digit is amount needed to reach next number
    # divisible by base. Return an integer
    return digits[int((base - (total % base)) % base)-1]


def validate_swittch_code(code: str) -> bool:
    """ Check if it is a valid account code """
    code = ''.join(code.split('-')).strip()
    check_digit = luhn_mod_n_str(code[:-1], SWITTCH_CODE_DIGITS)
    return check_digit == code[-1]
