from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required
from back.models import ShiftGroup, FileObj, ExcelColumns, Profile, Shift, Tuesday, Thursday, Friday, ShiftDay
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import pandas as pd
import numpy as np
from config.config import *
from back.forms import DatePickerForm, FileEditForm, ShiftForm
from tools.jalali import *
from django.utils import timezone
from django.urls import reverse
from back.decorator import check_grp_owner
from back.functions import *


def glob_context():
    ctx = dict()
    ctx['loading_title'] = KeyValue.loading_title
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
    groups = ShiftGroup.objects.all()
    context = {'groups': groups}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def read_excel(list_of_columns, filepath):
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data, columns=list_of_columns).replace(np.nan, '--')
    df_list = df.values.tolist()
    return df_list


def excel(request, grp_name):
    context = glob_context()
    jalali_now = get_jalali_now()
    grp = ShiftGroup.objects.get(name=grp_name)
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
        # print(default_excel_presence_columns)
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
    grp = ShiftGroup.objects.get(owner=User.objects.get(username=username))
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


@check_grp_owner
def create_shift(request):
    context = glob_context()
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            selected_month = form.cleaned_data['j_month_num']
            selected_year = form.cleaned_data['j_year_num']
            selected_group = form.cleaned_data['group']
            if Shift.objects.filter(group=selected_group, j_month_num=selected_month,
                                    j_year_num=selected_year).exists():
                print('########################################\n'
                      '#######   duplicate shift!!!!!!  #######\n'
                      '########################################')
                return redirect('/')
            form_obj = form.save(commit=False)
            # form_obj.people_list = Profile.objects.filter(group=selected_group).values_list('user__username')
            form_obj.people_list = ','.join(
                list(Profile.objects.filter(group=selected_group, in_shift=True).values_list('user__username',
                                                                                             flat=True)))
            list_of_days = return_day_names(selected_year, selected_month)
            form_obj.days_name = ','.join(list_of_days)
            form_obj.days_count = len(list_of_days)
            form_obj.save()
            ################################################################################################
            days_list = form_obj.days_name.split(',')
            normal_limit_count = selected_group.normal_req
            tuesday_limit_count = selected_group.tuesday_req
            thursday_limit_count = selected_group.thursday_req
            friday_limit_count = selected_group.friday_req
            for ind,i in enumerate(days_list):
                group_tuesday_list = get_special_list(Tuesday,selected_group,form_obj)
                special_day_cal_(ind, i, 'Tuesday', tuesday_limit_count, group_tuesday_list, form_obj)
                group_thursday_list = get_special_list(Thursday,selected_group,form_obj)
                special_day_cal_(ind, i, 'Thursday', thursday_limit_count, group_thursday_list, form_obj)
                group_friday_list = get_special_list(Friday,selected_group,form_obj)
                special_day_cal_(ind, i, 'Friday', friday_limit_count   , group_friday_list, form_obj)
                normal_day_cal_(ind, i, normal_limit_count, form_obj)
            # for ind,i in enumerate(days_list):
                # normal_day_cal_(ind, i, 3, form_obj)
            ################################################################################################
            # try:
            #     group_tuesday_list = Tuesday.objects.get(group=selected_group).people_list.split(',')
            #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$tuesday model exist')
            # except Tuesday.DoesNotExist:
            #     print('model does not exist!!!!!!!!!!!!!!!!!!!11')
            #     Tuesday.objects.create(group=selected_group,people_list=form_obj.people_list)
            #     print('Tuesday object of group {} created!!!!!!!!!111'.format(selected_group))
            #     group_tuesday_list = Tuesday.objects.get(group=selected_group).people_list.split(',')
            # except Exception as err:
            #     print(err)
            # try:
            #     group_thursday_list = Thursday.objects.get(group=selected_group).people_list.split(',')
            #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$thursday model exist')
            # except Thursday.DoesNotExist:
            #     print('model does not exist!!!!!!!!!!!!!!!!!!!11')
            #     Thursday.objects.create(group=selected_group,people_list=form_obj.people_list)
            #     print('Thursday object of group {} created!!!!!!!!!111'.format(selected_group))
            #     group_thursday_list = Thursday.objects.get(group=selected_group).people_list.split(',')
            # except Exception as err:
            #     print(err)
            # try:
            #     group_friday_list = Friday.objects.get(group=selected_group).people_list.split(',')
            #     print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Friday model exist')
            # except Friday.DoesNotExist:
            #     print('model does not exist!!!!!!!!!!!!!!!!!!!11')
            #     Friday.objects.create(group=selected_group,people_list=form_obj.people_list)
            #     print('Friday object of group {} created!!!!!!!!!111'.format(selected_group))
            #     group_friday_list = Friday.objects.get(group=selected_group).people_list.split(',')
            # except Exception as err:
            #     print(err)
                # if i == 'Tuesday':
                #     group_shift_count = 5
                #     i_people = []
                #     for j in range(group_shift_count):
                #         a = group_tuesday_list.pop(0)
                #         i_people.append(a)
                #         group_tuesday_list.append(a)
                #     month_num = form_obj.j_month_num
                #     year_num = form_obj.j_year_num
                #     ShiftDay.objects.create(
                #         shift = form_obj,
                #         index_num = ind,
                #         j_month_num = month_num,
                #         j_year_num = year_num,
                #         group = form_obj.group,
                #         night_people_list = ','.join(i_people),
                #         day_people_list = '',
                #         type = 'Tuesday',
                #         day_responsible = None,
                #         night_responsible = None
                #     )
                # if i == 'Thursday':
                #     group_shift_count = 2
                #     i_people = []
                #     for j in range(group_shift_count):
                #         a = group_thursday_list.pop(0)
                #         i_people.append(a)
                #         group_thursday_list.append(a)
                #     month_num = form_obj.j_month_num
                #     year_num = form_obj.j_year_num
                #     ShiftDay.objects.create(
                #         shift = form_obj,
                #         index_num = ind,
                #         j_month_num = month_num,
                #         j_year_num = year_num,
                #         group = form_obj.group,
                #         night_people_list = ','.join(i_people),
                #         day_people_list = '',
                #         type = 'Thursday',
                #         day_responsible = None,
                #         night_responsible = None
                #     )
                # if i == 'Friday':
                #     group_shift_count = 1
                #     i_people = []
                #     for j in range(group_shift_count):
                #         a = group_friday_list.pop(0)
                #         i_people.append(a)
                #         group_friday_list.append(a)
                #     month_num = form_obj.j_month_num
                #     year_num = form_obj.j_year_num
                #     ShiftDay.objects.create(
                #         shift = form_obj,
                #         index_num = ind,
                #         j_month_num = month_num,
                #         j_year_num = year_num,
                #         group = form_obj.group,
                #         night_people_list = ','.join(i_people),
                #         day_people_list = '',
                #         type = 'Friday',
                #         day_responsible = None,
                #         night_responsible = None
                #     )
            ################################################################################################
            return redirect('/')
    else:
        form = ShiftForm()
    texts = dict()
    texts['row'] = KeyValue.row
    texts['submit'] = KeyValue.submit
    context['texts'] = texts
    context['form'] = form
    return render(request, 'back/shift_create.html', context)



def shift(request, grp_name):
    context = glob_context()
    jalali_now = get_jalali_now()
    grp = ShiftGroup.objects.get(name=grp_name)
    print(grp)
    try:
        selected_month = jalali_now[1]
        selected_year = jalali_now[0]
        form = DatePickerForm(initial={'month': selected_month, 'year': selected_year})
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            form = DatePickerForm(request.POST)
            if form.is_valid():
                selected_month = form.cleaned_data['month']
                selected_year = form.cleaned_data['year']
        all_days = list(ShiftDay.objects.filter(group=grp,j_year_num=selected_year,j_month_num=selected_month).values(
            'type',
            'j_day_num',
            'j_month_num',
            'j_year_num',
            'night_people_list',
            'day_people_list',
            'day_responsible',
            'night_responsible'
        ))
        print(all_days)
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
        print(er)
    return render(request, 'back/shift.html', context)
        