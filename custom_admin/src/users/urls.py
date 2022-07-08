# -*- coding: utf-8 -*-
from django.urls import path
from .views import Register


urlpatterns = [path('register/', Register.as_view(), name='register'), ]