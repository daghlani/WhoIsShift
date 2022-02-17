# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from back.views import home, excel, files, file_add, create_shift, shift  # , file_edit
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('excel/<grp_name>', excel, name="excel"),
    path('files', files, name="files"),
    path('file_add', file_add, name="file_add"),
    path('shift_create', create_shift, name="shift_create"),
    path('shift/<grp_name>', shift, name="shift"),
    # path('file_edit/<file_pk>', file_edit, name="file_edit"),
]
