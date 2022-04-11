from back.models import ShiftDay, Profile, ShiftGroup
from config.config import PRI_WEEK_MAP
from back import models
from django.db.models import F
from tools.jalali import jalali_timedelta
from back.logger import logger
from tools.jalali import gregorian_to_jalali
import pandas as pd
import numpy as np
from datetime import datetime
import pytz


def get_time_obj(t_zone='Asia/Tehran'):
    tz = pytz.timezone(t_zone)
    return datetime.now(tz)


def printer(s, side_space=3, side_str=6, char='#'):
    s_len = len(s)
    side_space_len = side_space * 2
    side_str_len = side_str * 2
    all_char = s_len + side_space_len + side_str_len
    _str = all_char * char + '\n' + side_str * char + side_space * ' ' + s + side_space * ' ' + \
           side_str * char + '\n' + all_char * char
    print(_str)


def handle_uploaded_file(file, file_name):
    with open(file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def read_excel_column(filepath):
    df = pd.read_excel(filepath)
    return list(df.columns)


def read_excel(list_of_columns, filepath):
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data, columns=list_of_columns).replace(np.nan, '--')
    df_list = df.values.tolist()
    return df_list


def index_changer(first, second, list_):
    in_f = list_[first]
    in_s = list_[second]
    list_[first] = in_s
    list_[second] = in_f
    return list_


def get_class(kls):
    return getattr(models, PRI_WEEK_MAP[kls.upper()])


# def maintain_day(day_type):
#     day = ShiftDay.objects.get(type=day_type)
#     people_of_day = day.night_people_list.split(',')
#     _type, _date, _grp = day_type.split('__')
#     grp = ShiftGroup.objects.get(prefix=_grp)
#     standard_count = grp.get_req_of_type(_type)
#     if standard_count == len(people_of_day):
#         return True
#     else:
#
#         available_people = list(Profile.objects.filter(group=grp, shift_count__lt=standard_count).values_list(
#             'user__username', flat=True))
#         # remove people who are in available list and already are in people of day.
#         for i in available_people:
#             if i in people_of_day:
#                 available_people.pop(available_people.index(i))
#
#         _year, _month, _day = _date.split('/')
#         for i in list(range(standard_count - len(people_of_day))):
#             try:
#                 person = available_people[0]
#             except Exception as err:
#                 logger.debug(err)
#                 continue
#             if check_last_n_days(_year, _month, _day, grp, person, grp.shift_count_limit):
#                 people_of_day.append(person)
#                 available_people.pop(available_people.index(person))
#                 Profile.objects.filter(group=grp, user__username=person).update(shift_count=F('shift_count') + 1)
#         day.night_people_list = people_of_day
#         day.save()


# def check_last_n_days(y, m, d, group, name,  shift_count_num, n=2):
def check_last_n_days(y, m, d, group, name, shift_count_num):
    print('name: ', name)
    counter = 0
    n = group.rest_number
    if Profile.objects.get(user__username=name).shift_count >= shift_count_num:
        return False
    while counter < n:
        counter += 1
        delta_day = jalali_timedelta(y, m, d, -1 * counter)
        try:
            print(group, delta_day)
            obj_ = ShiftDay.objects.get(group=group, j_day_num=delta_day[2], j_month_num=delta_day[1],
                                        j_year_num=delta_day[0])
            night_people = obj_.night_people_list
            day_people = obj_.day_people_list
            if name in day_people or name in night_people:
                printer("%s is in night_list: %s" % (name, night_people))
                return False
        except ShiftDay.DoesNotExist:
            continue
        except Exception as err:
            logger.error(err)
            return False
    return True


# ToDo fix bug of add same person when all people can not add in calculating day, so current person will be added
#  multiple time, when the day need more than one people

def check_shift_day_exists(type_, grp):
    return ShiftDay.objects.filter(type='{}__{}'.format(type_, grp.prefix)).exists()


def special_day_cal_(ind, j, d_type, d_count, group_shift_count, people_group_type_list, form_obj, u_holiday_days=None,
                     u_holiday=None):
    group = form_obj.group
    if check_shift_day_exists(j, group):
        printer('type {} exists'.format('{}__{}'.format(j, group.prefix)))
        return
    j_name, j_date = j.split('__')
    greg_j_date_y, greg_j_date_m, greg_j_date_d = j_date.split('/')
    y, m, d = gregorian_to_jalali(int(greg_j_date_y), int(greg_j_date_m), int(greg_j_date_d))
    if j_name == d_type:
        i_people = []
        unavailable_people = []
        is_formal_ = False
        if u_holiday is not None and u_holiday_days is not None:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(d, u_holiday, u_holiday_days)
            if str('{}/{}'.format(m, d)) in u_holiday_days:
                is_formal_ = True
                d_count = u_holiday
                print('d_count is: ', d_count)
        print('d_count is: ', d_count)
        print('start people_group_type_list of {} is :-----------------{}---------------------'.format(
            d_type, people_group_type_list))
        for _time in range(d_count):
            print('people of day {} is: {}'.format(d_type, people_group_type_list))
            while True:
                print('using list is: ', people_group_type_list)
                try:
                    person = people_group_type_list[0]
                except Exception as err:
                    logger.debug(err)
                    print(err)
                    break
                if check_last_n_days(y=y, m=m, d=d, group=group, name=person, shift_count_num=group_shift_count):
                    a = people_group_type_list.pop(0)
                    i_people.append(a)
                    Profile.objects.filter(group=group, user__username=person).update(
                        shift_count=F('shift_count') + 1)
                    people_group_type_list.append(a)
                    break
                else:
                    print('changing list......')
                    print('list was: ', people_group_type_list)
                    u = people_group_type_list.pop(0)
                    unavailable_people.append(u)
                    print('unavailable_people list is: ', unavailable_people)
                    print('now list is: ', people_group_type_list)
                    continue
        people_group_type_list = unavailable_people + people_group_type_list
        ShiftDay.objects.create(
            shift=form_obj,
            index_num=ind,
            j_day_num=d,
            j_month_num=m,
            j_year_num=y,
            group=group,
            night_people_list=','.join(i_people),
            day_people_list='',
            type='{}__{}'.format(j, group.prefix),
            is_formally_holiday=is_formal_,
            day_responsible=None,
            night_responsible=None
        )
        print('______________________________________________________')
        print('finally list is: ', people_group_type_list)
        print('______________________________________________________')
        print('Updating {} record of {} ....'.format(d_type, group))
        type_obj_ = get_class(d_type).objects.get(group=form_obj.group)
        type_obj_.people_list = ','.join(people_group_type_list)
        type_obj_.save()
        print('Updating {} record of {} Done'.format(d_type, group))
        print(100 * '-')


def normal_day_cal_(ind, j, d_count, group_shift_count, form_obj, u_holiday_days=None, u_holiday=None):
    group = form_obj.group
    people_list = form_obj.people_list.split(',')
    j_name, j_date = j.split('__')
    greg_j_date_y, greg_j_date_m, greg_j_date_d = j_date.split('/')
    if check_shift_day_exists(j, group):
        printer('type {} exists'.format(j))
        return
    y, m, d = gregorian_to_jalali(int(greg_j_date_y), int(greg_j_date_m), int(greg_j_date_d))
    if j_name not in ['Tue', 'Thu', 'Fri']:
        i_people = []
        unavailable_people = []
        is_formal_ = False
        if u_holiday is not None and u_holiday_days is not None:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(d, u_holiday, u_holiday_days)
            if str('{}/{}'.format(m, d)) in u_holiday_days:
                is_formal_ = True
                d_count = u_holiday
                print('d_count is: ', d_count)
        print('d_count is: ', d_count)
        print('start people_list is :-----------------{}---------------------'.format(people_list))
        for _time in range(d_count):
            while True:
                print('using list is: ', people_list)
                try:
                    person = people_list[0]
                except Exception as err:
                    logger.debug(err)
                    break
                if check_last_n_days(y=y, m=m, d=d, group=group, name=person, shift_count_num=group_shift_count):
                    a = people_list.pop(0)
                    i_people.append(a)
                    Profile.objects.filter(group=group, user__username=person).update(shift_count=F('shift_count') + 1)
                    people_list.append(a)
                    print(i_people)
                    break
                else:
                    print('changing list......')
                    print('list was: ', people_list)
                    u = people_list.pop(0)
                    unavailable_people.append(u)
                    print('unavailable_people list is: ', unavailable_people)
                    print('now list is: ', people_list)
                    continue
        people_list = unavailable_people + people_list
        ShiftDay.objects.create(
            shift=form_obj,
            index_num=ind,
            j_day_num=d,
            j_month_num=m,
            j_year_num=y,
            group=group,
            night_people_list=','.join(i_people),
            day_people_list='',
            type='{}__{}'.format(j, group.prefix),
            is_formally_holiday=is_formal_,
            day_responsible=None,
            night_responsible=None
        )
        shift_obj_ = form_obj
        shift_obj_.people_list = ','.join(people_list)
        shift_obj_.save()


def get_special_list(model, _group, form_obj):
    try:
        group_list = model.objects.get(group=_group).people_list.split(',')
    # except model.DoesNotExist:
    except Exception as err:
        logger.error(err)
        print('probably model does not exist!!!!!!!!!!!!!!!!!!!')
        model.objects.create(group=_group, people_list=form_obj.people_list, back_people_list=form_obj.people_list)
        print('{} object of group {} created!!!!!!!!!!!!!!!!!!'.format(model, _group))
        group_list = model.objects.get(group=_group).people_list.split(',')
    return group_list


def update_special_day_backup(group, model):
    try:
        group_sp_day = model.objects.get(group=group)
        people_ = group_sp_day.people_list
        group_sp_day.back_people_list = people_
        group_sp_day.save()
    except model.DoesNotExist as err:
        logger.error(err)
