from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required
from back.models import ShiftGroup, FileObj, ExcelColumns
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import pandas as pd
import numpy as np
from config.config import *
from back.forms import DatePickerForm, FileEditForm
from tools.jalali import *
from django.utils import timezone
from django.urls import reverse
from back.decorator import check_grp_owner


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
