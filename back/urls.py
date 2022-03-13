# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from back.views import home, excel, files, file_add, shift_create_tr, shift, \
    profile  # , my_view , file_edit , shift_create
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('excel/<grp_name>', excel, name="excel"),
    path('files', files, name="files"),
    path('file_add', file_add, name="file_add"),
    # path('shift_create', shift_create, name="shift_create"),
    path('shift_create', shift_create_tr, name="shift_create"),
    path('shift/<grp_name>', shift, name="shift"),
    path('profile/<pk>', profile, name="profile"),
    # path('my_view', my_view, name="my_view"),
    # path('file_edit/<file_pk>', file_edit, name="file_edit"),
]
