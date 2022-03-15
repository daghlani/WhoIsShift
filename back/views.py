from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required
from back.models import ShiftGroup, FileObj, ExcelColumns, Profile, Shift, Tuesday, Thursday, Friday, ShiftDay
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db.models import Q, Sum, F
import pandas as pd
import numpy as np
from config.config import *
from back.forms import DatePickerForm, FileEditForm, ShiftForm  # , testForm
from tools.jalali import *
from django.utils import timezone
from django.urls import reverse
from back.decorator import check_grp_owner
from back.functions import *
from threading import Thread
from back.logger import logger
# from django.contrib.auth.models import Group, Permission

group_init()

# new_group, created = Group.objects.get_or_create(name='owners')
# perm1 = Permission.objects.get(name='Can add shift')
# perm2 = Permission.objects.get(name='Can delete shift')
# perm3 = Permission.objects.get(name='Can view shift')
# perm4 = Permission.objects.get(name='can_see_management')
# perm5 = Permission.objects.get(name='can_add_shift_on_page')
# new_group.permissions.add(perm1)
# new_group.permissions.add(perm2)
# new_group.permissions.add(perm3)
# new_group.permissions.add(perm4)
# new_group.permissions.add(perm5)


def glob_context():
    ctx = dict()
    ctx['loading_title'] = KeyValue.loading_title
    ctx['j_date_t'] = KeyValue.j_date_t
    ctx['welcome_txt'] = KeyValue.welcome_txt
    return ctx


def get_jalali_now():
    now = timezone.now()
    return gregorian_to_jalali(now.year, now.month, now.day)


def handle_uploaded_file(file, file_name):
    with open(file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def read_excel_column(filepath):
    df = pd.read_excel(filepath)
    return list(df.columns)


def home(request):
    context = glob_context()
    groups = ShiftGroup.objects.all()
    context['groups'] = groups
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required()
def profile(request, pk):
    context = glob_context()
    user_data = Profile.objects.get(user__id=pk)
    bool_dict = {'True': 'ok', 'False': 'no'}
    context.update(user_data=user_data)
    context.update(bool_dict=bool_dict)
    return render(request, 'back/profile.html', context)


def read_excel(list_of_columns, filepath):
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data, columns=list_of_columns).replace(np.nan, '--')
    df_list = df.values.tolist()
    return df_list


def excel(request, grp_name):
    context = glob_context()
    jalali_now = get_jalali_now()
    grp = ShiftGroup.objects.get(name=grp_name)
    form = DatePickerForm()
    try:
        if request.method == 'POST':
            form = DatePickerForm(request.POST)
            if form.is_valid():
                selected_month = form.cleaned_data['month']
                selected_year = form.cleaned_data['year']
            else:
                selected_month = jalali_now[1]
                selected_year = jalali_now[0]
        else:
            form = DatePickerForm(initial={'month': jalali_now[1], 'year': jalali_now[0]})
            selected_month = jalali_now[1]
            selected_year = jalali_now[0]
        related_excel_obj = FileObj.objects.filter(group_owner=grp, month=selected_month, year=selected_year)
        related_excel_file = [a for a in related_excel_obj][0]
        list_of_columns = read_excel_column(related_excel_file.file)
        default_excel_presence_columns = related_excel_file.related_column.column_to_list()
        if all(item in list_of_columns for item in default_excel_presence_columns):
            data = read_excel(default_excel_presence_columns, related_excel_file.file)
            data_dic = list()
            for i in data:
                i_dic = dict()
                for ind, j in enumerate(i):
                    i_dic[ind] = j
                data_dic.append(i_dic)
            tbl_col = dict()
            for x_ind, x in enumerate(default_excel_presence_columns):
                tbl_col[x_ind] = x
            context['data'] = {'data_dic': data_dic, 'tbl_col': tbl_col}
        else:
            context['data'] = {}
    except Exception as err:
        logger.error(err)
        print(err)
    finally:
        texts = dict()
        texts['row'] = KeyValue.row
        texts['submit'] = KeyValue.submit
        context['texts'] = texts
        context['form'] = form
    return render(request, 'back/show_excel.html', context)


@check_grp_owner
def files(request):
    context = glob_context()
    username = request.user
    grp = ShiftGroup.objects.get(owner=User.objects.get(username=username))
    texts = dict()
    texts['file_name'] = KeyValue.file_name
    texts['group'] = KeyValue.group
    file_objs = FileObj.objects.filter(group_owner=grp)
    context['files'] = file_objs
    context['texts'] = texts
    return render(request, 'back/files_list.html', context)


@check_grp_owner
def file_add(request):
    username = request.user
    context = glob_context()
    if request.method == 'POST':
        form = FileEditForm(request.POST, request.FILES)
        if form.is_valid():
            fj = form.save(commit=False)
            fj.group_owner = ShiftGroup.objects.get(owner__username=username)
            form.save()
            return redirect('/files')
    else:
        form = FileEditForm()
    texts = dict()
    texts['row'] = KeyValue.row
    texts['submit'] = KeyValue.submit
    context['texts'] = texts
    context['form'] = form
    return render(request, 'back/file_add.html', context)


def shift(request, grp_name):
    context = glob_context()
    jalali_now = get_jalali_now()
    grp = ShiftGroup.objects.get(name=grp_name)
    try:
        selected_month = jalali_now[1]
        selected_year = jalali_now[0]
        form = DatePickerForm(initial={'month': selected_month, 'year': selected_year})
        if request.method == 'POST':
            form = DatePickerForm(request.POST)
            if form.is_valid():
                selected_month = form.cleaned_data['month']
                selected_year = form.cleaned_data['year']
        all_days = list(ShiftDay.objects.filter(group=grp, j_year_num=selected_year, j_month_num=selected_month).values(
            'type', 'is_formally_holiday', 'j_day_num', 'j_month_num', 'j_year_num', 'night_people_list',
            'day_people_list', 'day_responsible', 'night_responsible', 'night_pr_people_list', 'day_pr_people_list'
        ))
        context['days'] = all_days
        texts = dict()
        texts['row'] = KeyValue.row
        texts['submit'] = KeyValue.submit
        texts['row'] = KeyValue.row
        texts['type'] = KeyValue.type
        texts['date'] = KeyValue.date
        texts['day'] = KeyValue.day
        texts['day_res'] = KeyValue.day_res
        texts['night'] = KeyValue.night
        texts['night_res'] = KeyValue.night_res
        context['texts'] = texts
        context['form'] = form
    except Exception as er:
        logger.error(er)
        print(er)
    return render(request, 'back/shift.html', context)


@check_grp_owner
def shift_create_tr(request):
    context = glob_context()
    if request.method == 'POST':
        try:
            form = ShiftForm(request.POST)
            if form.is_valid():
                start_date = datetime_to_jalali(form.cleaned_data['start_date'])
                end_date = datetime_to_jalali(form.cleaned_data['end_date'])
                selected_year_first = start_date[0]
                selected_year_last = end_date[0]
                selected_month_first = start_date[1]
                selected_month_last = end_date[1]
                selected_day_first = start_date[2]
                selected_day_last = end_date[2]
                sel_un_hol_first = form.cleaned_data['formally_holiday_first']
                sel_un_hol_last = form.cleaned_data['formally_holiday_last']
                selected_formally_holiday = ['{}/{}'.format(selected_month_first, i) for i in sel_un_hol_first] + \
                                            ['{}/{}'.format(selected_month_last, i) for i in sel_un_hol_last]
                selected_group = ShiftGroup.objects.get(owner__username=request.user)
                previous_day = jalali_timedelta(selected_year_first, selected_month_first, selected_day_first, -1)
                if not ShiftDay.objects.filter(j_year_num=previous_day[0], j_month_num=previous_day[1],
                                               j_day_num=previous_day[2]).exists():
                    printer('There is a gap between your chosen dates. please select correct dates.')
                    return redirect('/')
                form_obj = form.save(commit=False)
                form_obj.j_year_num_first = selected_year_first
                form_obj.j_year_num_last = selected_year_last
                form_obj.j_month_num_first = selected_month_first
                form_obj.j_month_num_last = selected_month_last
                form_obj.j_day_num_first = selected_day_first
                form_obj.j_day_num_last = selected_day_last
                form_obj.people_list = ','.join(
                    list(Profile.objects.filter(group=selected_group, in_shift=True).values_list('user__username',
                                                                                                 flat=True)))
                list_of_days = return_day_names_of_period(
                    jalali_year_first=selected_year_first,
                    jalali_year_last=selected_year_last,
                    jalali_month_first=selected_month_first,
                    jalali_month_last=selected_month_last,
                    first_day=selected_day_first,
                    last_day=selected_day_last
                )
                form_obj.days_name = ','.join(list_of_days)
                form_obj.days_count = len(list_of_days)
                form_obj.group = selected_group
                form_obj.save()
                ################################################################################################
                days_list = form_obj.days_name.split(',')
                normal_limit_count = selected_group.normal_req
                tuesday_limit_count = selected_group.tuesday_req
                thursday_limit_count = selected_group.thursday_req
                friday_limit_count = selected_group.friday_req
                formally_holiday_limit_count = selected_group.formally_holiday_req
                shift_count_limit_count = selected_group.shift_count_limit

                Profile.objects.filter(group=form_obj.group).update(shift_count=0)

                update_special_day_backup(selected_group, Tuesday)
                update_special_day_backup(selected_group, Thursday)
                update_special_day_backup(selected_group, Friday)

                def calc():
                    for ind, i in enumerate(days_list):
                        group_tuesday_list = get_special_list(Tuesday, selected_group, form_obj)
                        special_day_cal_(ind, i, 'Tue', tuesday_limit_count, shift_count_limit_count,
                                         group_tuesday_list,
                                         form_obj, u_holiday_days=selected_formally_holiday,
                                         u_holiday=formally_holiday_limit_count)
                        group_thursday_list = get_special_list(Thursday, selected_group, form_obj)
                        special_day_cal_(ind, i, 'Thu', thursday_limit_count, shift_count_limit_count,
                                         group_thursday_list,
                                         form_obj, u_holiday_days=selected_formally_holiday,
                                         u_holiday=formally_holiday_limit_count)
                        group_friday_list = get_special_list(Friday, selected_group, form_obj)
                        special_day_cal_(ind, i, 'Fri', friday_limit_count, shift_count_limit_count,
                                         group_friday_list,
                                         form_obj)
                        normal_day_cal_(ind, i, normal_limit_count, shift_count_limit_count, form_obj,
                                        u_holiday_days=selected_formally_holiday,
                                        u_holiday=formally_holiday_limit_count)
                    all_days_of_first_month = ShiftDay.objects.filter(group=form_obj.group,
                                                                      j_month_num=selected_month_first,
                                                                      j_year_num=selected_year_first)
                    all_days_of_last_month = ShiftDay.objects.filter(group=form_obj.group,
                                                                     j_month_num=selected_month_last,
                                                                     j_year_num=selected_year_last)
                    for day in all_days_of_first_month:
                        persian_list = []
                        pp_list = day.night_people_list.split(',')
                        if pp_list[0] != '':
                            for pr in pp_list:
                                persian_list.append(Profile.objects.get(user__username=pr).last_name)
                        day.night_pr_people_list = ','.join(persian_list)
                        day.save()
                    for day in all_days_of_last_month:
                        persian_list = []
                        pp_list = day.night_people_list.split(',')
                        if pp_list[0] != '':
                            for pr in pp_list:
                                persian_list.append(Profile.objects.get(user__username=pr).last_name)
                        day.night_pr_people_list = ','.join(persian_list)
                        day.save()

                x = Thread(target=calc)
                x.start()
                ################################################################################################
                return redirect('/')
            else:
                logger.error('form is not valid............')
        except Exception as err:
            form = ShiftForm()
            logger.error(err)
            print(err)
    else:
        form = ShiftForm()
    texts = dict()
    texts['row'] = KeyValue.row
    texts['submit'] = KeyValue.submit
    context['texts'] = texts
    context['form'] = form
    return render(request, 'back/shift_create.html', context)
