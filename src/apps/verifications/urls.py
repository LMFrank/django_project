# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views


app_name = 'verifications'
urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    re_path(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]