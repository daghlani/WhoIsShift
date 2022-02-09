from datetime import datetime, timedelta


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gm > 2:
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def jalali_to_gregorian(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if jm < 7:
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while gm < 13 and gd > sal_a[gm]:
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]


ary = [1, 5, 9, 13, 17, 22, 26, 30]


def j_leap_check(year):
    if year % 33 in ary:
        return True
    else:
        return False


def greg_to_datetime(gy, gm, gd):
    return datetime.strptime('{}-{}-{}'.format(gy, gm, gd), "%Y-%m-%d")


def get_last_day_in_jalali(month_number, year):
    if 1 <= month_number < 7:
        return 31
    elif 7 <= month_number < 12:
        return 30
    elif month_number == 12:
        if j_leap_check(year):
            return 30
        else:
            return 29


def gregorian_to_jalali_str(gr_datetime, time_format='{}-{}-{}'):
    in_t = gregorian_to_jalali(gr_datetime.year, gr_datetime.month, gr_datetime.day)
    return time_format.format(in_t[0], in_t[1], in_t[2])


def dates_between_as_name(start_date, end_date):
    delta = end_date - start_date  # as timedelta
    days = [(start_date + timedelta(days=i)).strftime("%A") for i in range(delta.days + 1)]
    return days


def return_day_names(jalali_year, jalali_month):
    first_y, first_m, first_d = jalali_to_gregorian(jalali_year, jalali_month, 1)
    end_y, end_m, end_d = jalali_to_gregorian(jalali_year, jalali_month,
                                              get_last_day_in_jalali(jalali_month, jalali_year))
    first_of_month = greg_to_datetime(first_y, first_m, first_d)
    end_of_month = greg_to_datetime(end_y, end_m, end_d)
    return dates_between_as_name(first_of_month, end_of_month)
