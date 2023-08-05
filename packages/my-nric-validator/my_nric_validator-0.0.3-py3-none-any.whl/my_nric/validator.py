import datetime as dt


def remove_dash(number):
    # Remove - from the input if any
    return number.replace("-", "").strip()


def get_birth_date(number):
    number = remove_dash(number)
    year = int(number[0:2])
    month = int(number[2:4])
    day = int(number[4:6])

    try:
        return dt.date(year + 1900, month, day)
    except ValueError:
        pass
    try:
        return dt.date(year + 2000, month, day)
    except ValueError:
        raise ValueError('Invalid value')


def validate_birth_place(number):
    # Use to validate the birth place value in the NRIC is exists
    bp_data = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "71",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "98",
        "99",
    ]

    number = remove_dash(number)
    number = number[6:8]
    results = number in bp_data

    if not results:
        raise ValueError('Invalid value')

    return results


def get_gender(number):
    number = remove_dash(number)
    # - 1 index is the last string/char
    last_char = number[-1]
    result = "Male"
    if int(last_char) % 2 == 0:
        # if Even then is Female
        result = "Female"

    return result



def validate_nric(number):
    """Check if the number is a valid Malaysian NRIC. it check length,
    formatting and birth date and place."""
    try:
        number = remove_dash(number)
        if len(number) != 12:
            raise ValueError('Invalid value')
        if not number.isdigit():
            raise ValueError('Invalid value')
        get_birth_date(number)
        validate_birth_place(number)
        return True
    except ValueError as e:
        return False
