# -*- coding: utf-8 -*-
from django.urls import re_path

from verifications import views


app_name = 'verifications'
urlpatterns = [
    # 图片验证码
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    # 短信验证码
    re_path(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]