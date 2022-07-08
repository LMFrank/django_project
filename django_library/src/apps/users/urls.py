# -*- coding: utf-8 -*-
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from users import views

app_name = 'users'
urlpatterns = [
    # 用户注册
    path('users/', views.UserView.as_view(), name='register'),
    # 判断用户名是否已注册
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否已注册
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 登录验证
    path('authorizations/', obtain_jwt_token),

]