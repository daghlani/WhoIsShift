excel_file_extension = 'xlsx'
excel_file_label = 'EXCEL FILE'
first_year_of_lunch = 1400
year_range = 10
days_of_week = {'en': 'days_of_week', 'fa': 'ایام هفته'}
date = {'en': 'date', 'fa': 'تاریخ'}
day_operator = {'en': 'day_operator', 'fa': 'شیفت روز'}
night_operator = {'en': 'night_operator', 'fa': 'شیفت شب'}
# default_excel_presence_columns = [days_of_week['fa'], date['fa'], day_operator['fa'], night_operator['fa']]


class KeyValue:
    row = 'ردیف'
    submit = 'ارسال'
    shift_num = 'تلفن شیفت'
    loading_title = 'لطفا منتظر بمانید...'
    file_name = 'نام فایل'
    group = 'گروه'
    normal_req = 'حداقل نفر روز عادی'
    tuesday_req = 'حداقل نفر سه‌شنبه'
    thursday_req = 'حداقل نفر پنجشنبه'
    friday_req = 'حداقل نفر جمعه'
    shift_count_limit = 'تعداد شیفت در ماه'
    shift_count = 'تعداد شیفت'
    type = 'روز'
    date = 'تاریخ'
    day = 'شیفت روز'
    day_res = 'مسئول روز'
    night = 'شیفت شب'
    night_res = 'مسئول شب'


class MonthNames:
    year = 'سال'
    month = 'ماه'
    day = 'روز'
    FAR = 'فروردین'
    ORD = 'اردیبهشت'
    KHO = 'خرداد'
    TIR = 'تیر'
    MOR = 'مرداد'
    SHA = 'شهریور'
    MEH = 'مهر'
    ABA = 'آبان'
    AZA = 'آذر'
    DEY = 'دی'
    BAH = 'بهمن'
    ESF = 'اسفند'
    list_names = [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور', 'مهر',
        'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]

    JALALI_MONTH_CHOICES = [
        (1, FAR), (2, ORD), (3, KHO),
        (4, TIR), (5, MOR), (6, SHA),
        (7, MEH), (8, ABA), (9, AZA),
        (10, DEY), (11, BAH), (12, ESF)
    ]

    JALALI_YEAR_CHOICES = []
    for r in range(first_year_of_lunch, (first_year_of_lunch + year_range)):
        JALALI_YEAR_CHOICES.append((r, r))
