from config.config import WEEK_MAP


def persian_to_eng_number(mynum):
    mynum = str(mynum)
    return mynum.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def eng_to_persian_number(number):
    number = str(number)
    return number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


def week_map(week_day):
    # return WEEK_MAP[week_day]
    return WEEK_MAP[week_day.upper()]
