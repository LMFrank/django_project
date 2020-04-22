# -*- coding: utf-8 -*-
from django.urls import path, include
from users.views import UserDetailAPIView


urlpatterns = [
    path('me/', UserDetailAPIView.as_view()),
]
