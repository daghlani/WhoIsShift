from back.models import ShiftDay
from back import models
from tools.jalali import jalali_timedelta


def printer(s, side_space=3, side_str=6, char='#'):
    s_len = len(s)
    side_space_len = side_space * 2
    side_str_len = side_str * 2
    all_char = s_len + side_space_len + side_str_len
    _str = all_char * char + '\n' + side_str * char + side_space * ' ' + s + side_space * ' ' + \
           side_str * char + '\n' + all_char * char
    print(_str)


def index_changer(first, second, list):
    in_f = list[first]
    in_s = list[second]
    list[first] = in_s
    list[second] = in_f
    return list


def get_class(kls):
    return getattr(models, kls)


def check_last_n_days(y, m, d, group, name, n=2):
    print('name: ', name)
    counter = 0
    while counter < n:
        counter += 1
        # print('counter is : ', counter)
        delta_day = jalali_timedelta(y, m, d, -1 * counter)
        # print(delta_day)
        try:
            obj_ = ShiftDay.objects.get(group=group, j_day_num=delta_day[2], j_month_num=delta_day[1],
                                        j_year_num=delta_day[0])
            night_people = obj_.night_people_list
            day_people = obj_.day_people_list
            if name in day_people or name in night_people:
                # print("%s is in day_list: %s" % (name, day_people))
                print(">>>>>>>>>>>>>>>>>>OR<<<<<<<<<<<<<<<<<<")
                print("%s is in night_list: %s" % (name, night_people))
                return False
        except ShiftDay.DoesNotExist:
            continue
        except Exception as err:
            # print(err)
            return False
    return True


def special_day_cal_(ind, j, d_type, d_count, people_group_type_list, form_obj):
    if j == d_type:
        i_people = []
        unavailable_people = []
        print('start people_group_type_list of {} is :-----------------{}---------------------'.format(d_type,
                                                                                                       people_group_type_list))
        for _time in range(d_count):
            # people_group_type_list = unavailable_people + people_group_type_list
            # for pr_index, pr in enumerate(range(d_count)):
            # print(pr_index)
            y = form_obj.j_year_num
            m = form_obj.j_month_num
            d = ind + 1
            group = form_obj.group
            print('people of day {} is: {}'.format(d_type, people_group_type_list))
            # person = people_group_type_list[0]
            # for any in people_group_type_list:
            while True:
                print('using list is: ', people_group_type_list)
                # person = any
                person = people_group_type_list[0]
                # print(y,m,d)
                if check_last_n_days(y=y, m=m, d=d, group=group, name=person):
                    a = people_group_type_list.pop(0)
                    i_people.append(a)
                    people_group_type_list.append(a)
                    print(i_people)
                    break
                else:
                    print('changing list......')
                    print('list was: ', people_group_type_list)
                    # index_changer(0,1,people_group_type_list)
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
            type=d_type,
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


def normal_day_cal_(ind, j, d_count, form_obj):
    if j not in ['Tuesday', 'Thursday', 'Friday']:
        people_list = form_obj.people_list.split(',')
        i_people = []
        unavailable_people = []
        print('start people_list is :-----------------{}---------------------'.format(people_list))
        for _time in range(d_count):
            y = form_obj.j_year_num
            m = form_obj.j_month_num
            d = ind + 1
            group = form_obj.group
            while True:
                print('using list is: ', people_list)
                person = people_list[0]
                if check_last_n_days(y=y, m=m, d=d, group=group, name=person):
                    a = people_list.pop(0)
                    i_people.append(a)
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
            type=j,
            day_responsible=None,
            night_responsible=None
        )
        shift_obj_ = form_obj
        shift_obj_.people_list = ','.join(people_list)
        shift_obj_.save()


def get_special_list(model, selected_group, form_obj):
    try:
        group_list = model.objects.get(group=selected_group).people_list.split(',')
    # except model.DoesNotExist:
    except Exception as err:
        print(err)
        print('probably model does not exist!!!!!!!!!!!!!!!!!!!')
        model.objects.create(group=selected_group, people_list=form_obj.people_list)
        print('{} object of group {} created!!!!!!!!!!!!!!!!!!'.format(model, selected_group))
        group_list = model.objects.get(group=selected_group).people_list.split(',')
    return group_list
