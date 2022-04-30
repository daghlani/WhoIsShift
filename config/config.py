excel_file_extension = 'xlsx'
excel_file_label = 'EXCEL FILE'
first_year_of_lunch = 1400
year_range = 10
days_of_week = {'en': 'days_of_week', 'fa': 'ایام هفته'}
date = {'en': 'date', 'fa': 'تاریخ'}
day_operator = {'en': 'day_operator', 'fa': 'شیفت روز'}
day_responsible = {'en': 'day_operator', 'fa': 'مسئول روز'}
night_operator = {'en': 'night_operator', 'fa': 'شیفت شب'}
night_responsible = {'en': 'day_operator', 'fa': 'مسئول شب'}
day_name = {'en': 'day_name', 'fa': 'نام روز'}
day = {'en': 'day', 'fa': 'روز'}
month = {'en': 'month', 'fa': 'ماه'}
year = {'en': 'year', 'fa': 'سال'}
# default_excel_presence_columns = [days_of_week['fa'], date['fa'], day_operator['fa'], night_operator['fa']]
default_excel_shift_columns = [day_name['fa'], day['fa'], month['fa'], year['fa'], day_operator['fa'],
                               day_responsible['fa'], night_operator['fa'], night_responsible['fa']]

owner_perms = [
    'can_see_management', 'can_add_shift_on_page',
    'Can view shift', 'Can change shift', 'Can delete shift',
    'Can view shift day', 'Can change shift day',
    'Can view friday', 'Can change friday',
    'Can view tuesday', 'Can change tuesday',
    'Can view thursday', 'Can change thursday',
    'Can view formal h', 'Can change formal h'
    'Can view profile',
]

WEEK_MAP = dict(
    Saturday='شنبه',
    Sunday='یکشنبه',
    Monday='دوشنبه',
    Tuesday='سه‌شنبه',
    Wednesday='چهارشنبه',
    Thursday='پنجشنبه',
    Friday='جمعه',
    SAT='شنبه',
    SUN='یکشنبه',
    MON='دوشنبه',
    TUE='سه‌شنبه',
    WED='چهارشنبه',
    THU='پنجشنبه',
    FRI='جمعه',
)
PRI_WEEK_MAP = dict(
    Saturday='SAT',
    Sunday='SUN',
    Monday='MON',
    Tuesday='TUE',
    Wednesday='WED',
    Thursday='THU',
    Friday='FRI',
    SAT='Saturday',
    SUN='Sunday',
    MON='Monday',
    TUE='Tuesday',
    WED='Wednesday',
    THU='Thursday',
    FRI='Friday',
)


class KeyValue:
    excel_file = 'فایل اکسل'
    name = 'نام'
    username = 'نام کاربری'
    password1 = 'گذرواژه'
    password2 = 'تکرار گذرواژه'
    in_shift = 'حضور در شیفت'
    first_name = 'نام'
    last_name = 'نام خانوادگی'
    pr_name = 'نام فارسی'
    email = 'ایمیل'
    prefix = 'نام اختصاری'
    owner = 'مالک'
    welcome_txt = 'خوش آمدید'
    j_date_t = 'امروز'
    row = 'ردیف'
    submit = 'ارسال'
    excel_file_is_valid = 'اطلاعات زیر صحیح است'
    shift_num = 'تلفن شیفت'
    loading_title = 'لطفا منتظر بمانید...'
    formally_holiday = 'تعطیلات رسمی'
    file_name = 'نام فایل'
    group = 'گروه'
    rest_number = 'تعداد روز استخراحت'
    normal_req = 'حداقل نفر روز عادی'
    tuesday_req = 'حداقل نفر سه‌شنبه'
    thursday_req = 'حداقل نفر پنجشنبه'
    friday_req = 'حداقل نفر جمعه'
    formally_holiday_req = 'حداقل نفر در تعطیلات رسمی'
    shift_count_limit = 'تعداد شیفت در ماه'
    shift_count = 'تعداد شیفت'
    type = 'روز'
    date = 'تاریخ'
    day = 'شیفت روز'
    day_st = 'روز'
    night_st = 'شب'
    day_res = 'مسئول روز'
    night = 'شیفت شب'
    night_res = 'مسئول شب'
    phone_number = 'شماره تلفن'
    chose_value = 'انتخاب کنید...'
    start_date = 'تارخ شروع'
    end_date = 'تاریخ پایان'


class MonthNames:
    year_first = 'از سال'
    year_last = 'تا سال'
    year = 'سال'
    month_first = 'از ماه'
    month_last = 'تا ماه'
    month = 'ماه'
    day_first = 'از روز'
    day_last = 'تا روز'
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
        ('', KeyValue.chose_value),
        (1, FAR), (2, ORD), (3, KHO),
        (4, TIR), (5, MOR), (6, SHA),
        (7, MEH), (8, ABA), (9, AZA),
        (10, DEY), (11, BAH), (12, ESF)
    ]

    JALALI_YEAR_CHOICES = []
    for r in range(first_year_of_lunch, (first_year_of_lunch + year_range)):
        JALALI_YEAR_CHOICES.append((r, r))
    JALALI_YEAR_CHOICES.append(('', KeyValue.chose_value))

    JALALI_DAY_CHOICES = []
    for r in range(1, 32):
        JALALI_DAY_CHOICES.append((r, r))
    # JALALI_DAY_CHOICES.append((None, 'Choose...'))


class Error:
    alphanumeric = dict(en='Only alphanumeric characters are allowed.', fa='تنها حروف البای انگلیسی مجاز است!')


class Success:
    upload_success = 'file uploaded successfully.'
